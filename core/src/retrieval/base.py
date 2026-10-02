import torch
import faiss
import numpy as np

class RetrievalDatabase:
    """
    Wrapper for FAISS Index.
    """
    def __init__(self, embedding_dim):
        self.dimension = embedding_dim
        # L2 Distance Index
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.stored_data = [] # To store metadata (dates, raw values)
        self._cached_data = None
        
    def add_items(self, embeddings, data_values):
        """
        embeddings: numpy array [N, dim]
        data_values: numpy array [N, data_dim] (The actual weather values)
        """
        if embeddings.shape[1] != self.dimension:
            raise ValueError("Dimension mismatch")

        self.index.add(embeddings)
        self.stored_data.append(data_values) # List of arrays
        self._cached_data = None  # invalidate cached concatenation
        
    def query(self, query_embedding, k=3):
        """
        Find k nearest neighbors.

        Args:
            query_embedding: numpy array [Batch, dim]
            k: number of neighbors

        Returns:
            torch.Tensor [Batch, k, data_dim]
        """
        total_refs = self.index.ntotal
        if total_refs == 0:
            raise ValueError("RetrievalDatabase is empty. Call add_items() before query().")
        if k > total_refs:
            raise ValueError(
                f"k={k} is larger than the number of stored items ({total_refs}). "
                "Reduce k or add more items."
            )

        distances, indices = self.index.search(query_embedding, k)

        if np.any(indices < 0):
            raise RuntimeError(
                "FAISS returned invalid indices (<0) despite k <= n_total. "
                "This indicates a corrupted index or inconsistent state."
            )

        # Cache concatenated data to avoid repeated memory allocation.
        # stored_data is non-empty here: the total_refs check above guarantees it.
        if self._cached_data is None:
            self._cached_data = np.concatenate(self.stored_data, axis=0).astype(np.float32)

        all_data = self._cached_data

        # Vectorized lookup
        retrieved_values = all_data[indices]

        return torch.tensor(retrieved_values, dtype=torch.float32)
