"""Guards the web/API <-> core contract: feature order and retrieval catalog identity."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))

from api.services.inference_service import CANDIDATE_FEATURE_COLS  # noqa: E402
from core.src.inference import load_model_and_stats  # noqa: E402

CHECKPOINT = os.path.join(ROOT, "core", "models", "diffusion_chkpt.pth")


def test_checkpoint_features_and_catalog_match_api_contract():
    model_wrapper, _stats, retrieval_db, catalog = load_model_and_stats(CHECKPOINT)
    assert list(model_wrapper.config["feature_cols"]) == CANDIDATE_FEATURE_COLS
    assert retrieval_db.index.ntotal + 1 == len(catalog)
