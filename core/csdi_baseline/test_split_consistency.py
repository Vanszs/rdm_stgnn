"""
One authority for the train/val/test split, checked against its copies.

The split lives in three places for three different reasons:

  src/train.py                    the authority (used by RDM-STGNN)
  csdi_baseline/build_data.py     plain constants, so the adapter runs without torch
  csdi_baseline/train_csdi.py     constants, so CSDI training runs without torch

These copies are only safe while they agree. If one drifts, CSDI's normalisation
statistics would be computed on a different train set than RDM-STGNN's, which
silently breaks the like-for-like comparison in Tabel 3.18. This test makes that
drift loud.
"""
import os
import sys
import unittest

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.dirname(HERE)
sys.path.insert(0, CORE)

from src.train import temporal_split  # noqa: E402  (authority)

import build_data  # noqa: E402
import train_csdi  # noqa: E402


def _ts(v):
    """Normalise a boundary to a comparable timestamp (the copies use str vs datetime64)."""
    return pd.Timestamp(str(v))


class SplitBoundaryConsistencyTest(unittest.TestCase):
    def _authority(self):
        import inspect

        sig = inspect.signature(temporal_split)
        return _ts(sig.parameters["train_end"].default), _ts(sig.parameters["val_end"].default)

    def test_csvd_copies_match_authority(self):
        a_train, a_val = self._authority()
        self.assertEqual(_ts(build_data.TRAIN_END), a_train,
                         "build_data.TRAIN_END drifted from src.train.temporal_split")
        self.assertEqual(_ts(build_data.VAL_END), a_val,
                         "build_data.VAL_END drifted from src.train.temporal_split")

    def test_train_csdi_copies_match_authority(self):
        a_train, a_val = self._authority()
        self.assertEqual(_ts(train_csdi.TRAIN_END), a_train,
                         "train_csdi.TRAIN_END drifted from src.train.temporal_split")
        self.assertEqual(_ts(train_csdi.VAL_END), a_val,
                         "train_csdi.VAL_END drifted from src.train.temporal_split")

    def test_all_three_agree(self):
        self.assertEqual(_ts(build_data.TRAIN_END), _ts(train_csdi.TRAIN_END))
        self.assertEqual(_ts(build_data.VAL_END), _ts(train_csdi.VAL_END))


if __name__ == "__main__":
    unittest.main()
