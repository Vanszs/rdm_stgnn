"""
FAISS retrieval database (ablation evidence / scientific falsification path).

The retrieval module is kept so the thesis ablation table can be falsified
honestly: the `diff_retrieval` and `full_model` scenarios must run real
nearest-neighbour lookups so measured gains are attributable to retrieval and
not to an extra trainable MLP. Safety properties that follow:

1. FAISS is imported lazily (first `add_items` call) and the public state is
   plain NumPy/PyTorch. The denoiser never receives a fake "retrieved" tensor:
   callers that ablate retrieval pass `retrieved=None` so the `retrieval_mlp`
   branch is a true structural bypass (zero contribution, no injected bias).
2. Only embeddings and value rows are staged, as contiguous float32 arrays; the
   rest of the source table stays with the caller, so peak memory is bounded by
   the two staged blocks plus the single FAISS store - no hidden full-table
   copies.
"""

from __future__ import annotations

import threading

import numpy as np
import torch

_FAISS_LOCK = threading.Lock()
_FAISS = None


def _faiss():
    """Import faiss on first index construction only (lazy dependency)."""
    global _FAISS
    with _FAISS_LOCK:
        if _FAISS is None:
            import faiss as _faiss_mod

            _FAISS = _faiss_mod
    return _FAISS


class RetrievalDatabase:
    """
    FAISS IndexFlatL2 wrapper over staged contiguous float32 arrays.

    Keeps the historical contract:

    - ``add_items(embeddings, data_values)`` - stage float32 vectors + values.
    - ``query(query_embedding, k)`` - return ``[B, k, data_dim]`` float32 torch
      tensor (FAISS search runs inside).
    - ``index`` / ``stored_data`` - read directly by training/eval pipelines.
    """

    def __init__(self, embedding_dim):
        self.dimension = int(embedding_dim)
        self.index = None
        self.stored_data = []  # staged value blocks (np.ndarray, float32)
        self._cached_data = None
        self._build_lock = threading.Lock()

    def _concat(self, blocks):
        if not blocks:
            return None
        if len(blocks) == 1:
            return np.ascontiguousarray(blocks[0], dtype=np.float32)
        return np.concatenate(blocks, axis=0).astype(np.float32, copy=False)

    def add_items(self, embeddings, data_values):
        """
        Stage float32 projections. embeddings: numpy [N, dim]; data_values:
        numpy [N, data_dim].

        The FAISS index is built lazily on the first call: import cost and the
        OpenMP/OMP_DUPLICATE_LIB_OK fallback warning are paid by the retrieval
        path only (never burns for pure-ablation callers that skip add_items).
        """
        with self._build_lock:
            embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)
            data_values = np.ascontiguousarray(data_values, dtype=np.float32)
            if embeddings.ndim != 2 or embeddings.shape[1] != self.dimension:
                raise ValueError(
                    f"Dimension mismatch: expected [N, {self.dimension}], got {embeddings.shape}"
                )
            if embeddings.shape[0] != data_values.shape[0]:
                raise ValueError(
                    f"Embedding/value count mismatch: "
                    f"{embeddings.shape[0]} vs {data_values.shape[0]}"
                )
            self.stored_data.append(data_values)
            self._cached_data = None  # invalidate the cached concatenation

            if self.index is None:
                self.index = _faiss().IndexFlatL2(self.dimension)
            self.index.add(embeddings)

    def ensure_index_built(self):
        """Return the underlying FAISS index (built on add_items)."""
        return self.index

    def query(self, query_embedding, k=3):
        """
        Find k nearest neighbors.

        Args:
            query_embedding: numpy array [Batch, dim]
            k: number of neighbors

        Returns:
            torch.Tensor [Batch, k, data_dim]
        """
        total_refs = self.index.ntotal if self.index is not None else 0
        if total_refs == 0:
            raise ValueError("RetrievalDatabase is empty. Call add_items() before query().")
        if k > total_refs:
            raise ValueError(
                f"k={k} is larger than the number of stored items ({total_refs}). "
                "Reduce k or add more items."
            )

        q = np.ascontiguousarray(query_embedding, dtype=np.float32)
        distances, indices = self.index.search(q, k)

        if np.any(indices < 0):
            raise RuntimeError(
                "FAISS returned invalid indices (<0) despite k <= n_total. "
                "This indicates a corrupted index or inconsistent state."
            )

        # Cache the concatenated value table once; staging order guarantees it
        # matches the FAISS key order (same append sequence).
        if self._cached_data is None:
            self._cached_data = torch.from_numpy(self._concat(self.stored_data))

        # Vectorized pure-tensor lookup (no extra np->torch round-trip).
        all_data = self._cached_data
        idx = torch.from_numpy(indices).to(dtype=torch.long)
        data_dim = int(all_data.shape[1])
        retrieved_values = all_data[idx.reshape(-1)].view(len(indices), k, data_dim)
        return retrieved_values.to(torch.float32)

    def reset(self):
        """
        Free every buffer the wrapper owns. Call after use in long-lived
        processes (eval scenarios / notebooks) - plain references, so the
        FAISS store is garbage-collected with the wrapper.
        """
        with self._build_lock:
            self.index = None
            self._cached_data = None
            self.stored_data = []


__all__ = ["RetrievalDatabase"]
