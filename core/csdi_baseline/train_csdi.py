"""
Train CSDI (Tashiro et al., NeurIPS 2021) on the Pangrango 5-node ERA5 dataset.

Vendored model code (diff_models.py, main_model.py, utils.py) is the official
ermongroup/CSDI implementation, unmodified. This script only supplies the data
and configuration so the comparison with RDM-STGNN is like-for-like:

  * history_length = 6, pred_length = 1   (thesis: t-6..t-1 -> t+1)
  * DDIM 20 inference steps, 30 ensemble members
  * split boundaries identical to core/src/train.py (thesis Tabel 3.10)

Config changes from CSDI's `base_forecasting.yaml` are forced here and the reason
is recorded in docs/CSDI_COMPARISON.md:

  * is_linear: False   -> uses torch's nn.TransformerEncoder instead of the
                          `linear_attention_transformer` package. Same published
                          architecture family (the linear variant is an
                          efficiency swap for long sequences: 168 steps in the
                          electricity benchmark vs 7 here). Removes the only
                          missing dependency and fits 4 GB VRAM.
  * batch_size: 16     -> 4 GB VRAM (RTX 3050 Laptop).
  * layers/channels    -> reduced from 4/64 only if OOM; recorded if changed.
  * target_strategy: "all" -> CSDI's "test" strategy subsamples
                          num_sample_features channels per batch, which would
                          randomly drop the MAIN precipitation/wind/humidity
                          target channels we must evaluate.

Run:  cd core/csdi_baseline && python train_csdi.py [--epochs N] [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import pickle
import sys
import time

import numpy as np
import torch
import yaml
from torch.utils.data import DataLoader, Dataset

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from main_model import CSDI_Forecasting  # noqa: E402

HISTORY_LENGTH = 6
PRED_LENGTH = 1
SEQ_LENGTH = HISTORY_LENGTH + PRED_LENGTH

# Thesis split boundaries.
TRAIN_END = np.datetime64("2018-12-31 16:00")
VAL_END = np.datetime64("2021-12-31 16:00")

DATA_DIR = os.path.join(HERE, "data", "pangrango")
OUT_DIR = os.path.join(HERE, "save")
SEED = 1


def load_arrays():
    with open(os.path.join(DATA_DIR, "data.pkl"), "rb") as f:
        main_data, mask_data = pickle.load(f)
    with open(os.path.join(DATA_DIR, "meanstd.pkl"), "rb") as f:
        mean_data, std_data = pickle.load(f)
    # Timestamps come from the canonical parquet so splits match the RDM-STGNN run.
    import pandas as pd
    df = pd.read_parquet(os.path.join(os.path.dirname(HERE), "data", "raw",
                                      "pangrango_era5_5node_2005_2025.parquet"))
    ts = np.sort(pd.to_datetime(df["date"]).dt.tz_localize(None).unique())
    return main_data, mask_data, mean_data, std_data, ts


class PangrangoForecast(Dataset):
    """Sliding windows over the flat [T,N] array, split by thesis boundaries."""

    def __init__(self, main_data, mask_data, ts, mode="train"):
        self.main = main_data
        self.mask = mask_data
        self.ts = ts
        if mode == "train":
            self.starts = np.where(ts <= TRAIN_END)[0]
        elif mode == "valid":
            self.starts = np.where((ts > TRAIN_END) & (ts <= VAL_END))[0]
        else:
            self.starts = np.where(ts > VAL_END)[0]
        # Need SEQ_LENGTH consecutive timestamps.
        self.starts = self.starts[self.starts + SEQ_LENGTH <= len(ts)]

    def __len__(self):
        return len(self.starts)

    def __getitem__(self, i):
        s = self.starts[i]
        target_mask = self.mask[s:s + SEQ_LENGTH].copy()
        target_mask[-PRED_LENGTH:] = 0.0          # predict the last step
        return {
            "observed_data": self.main[s:s + SEQ_LENGTH],
            "observed_mask": self.mask[s:s + SEQ_LENGTH],
            "gt_mask": target_mask,
            "timepoints": np.arange(SEQ_LENGTH) * 1.0,
            "feature_id": np.arange(self.main.shape[1]) * 1.0,
        }


def build_config(epochs: int, batch_size: int, layers: int, channels: int) -> dict:
    return {
        "train": {"epochs": epochs, "batch_size": batch_size, "lr": 1.0e-3,
                  "itr_per_epoch": 1.0e8},
        "diffusion": {
            "layers": layers, "channels": channels, "nheads": 8,
            "diffusion_embedding_dim": 128, "beta_start": 0.0001,
            "beta_end": 0.5, "num_steps": 50, "schedule": "quad",
            "is_linear": False,
        },
        "model": {
            "is_unconditional": 0,
            "timeemb": 128, "featureemb": 16,
            "target_strategy": "all",
            "num_sample_features": 64,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--layers", type=int, default=4)
    ap.add_argument("--channels", type=int, default=64)
    ap.add_argument("--val-windows", type=int, default=2048)
    ap.add_argument("--no-resume", action="store_true",
                    help="Ignore csdi_resume.pth and train from scratch.")
    ap.add_argument("--dry-run", action="store_true", help="one batch, check VRAM + loss")
    args = ap.parse_args()

    torch.manual_seed(SEED)
    np.random.seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    if device.type == "cuda":
        print(f"  {torch.cuda.get_device_name(0)}  "
              f"VRAM {torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB")

    main_data, mask_data, mean_data, std_data, ts = load_arrays()
    print(f"data: {main_data.shape}  timestamps {ts[0]} .. {ts[-1]}")

    tr = PangrangoForecast(main_data, mask_data, ts, "train")
    va = PangrangoForecast(main_data, mask_data, ts, "valid")
    print(f"windows: train {len(tr)}  valid {len(va)}")

    cfg = build_config(args.epochs, args.batch_size, args.layers, args.channels)
    target_dim = main_data.shape[1]
    model = CSDI_Forecasting(cfg, device, target_dim=target_dim).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"target_dim={target_dim}  params={n_params/1e6:.2f} M")

    train_loader = DataLoader(tr, batch_size=args.batch_size, shuffle=True)
    # Validation only selects the best checkpoint, so a bounded random subset is
    # enough. Full 26,304-window validation with loss_valid (50 diffusion steps
    # per batch) costs ~27 min/epoch on this 4 GB GPU for no additional signal.
    rng = np.random.default_rng(SEED)
    n_val = min(args.val_windows, len(va))
    va_small = torch.utils.data.Subset(va, rng.choice(len(va), size=n_val, replace=False))
    valid_loader = DataLoader(va_small, batch_size=args.batch_size, shuffle=False)
    print(f"validation windows used: {n_val} of {len(va)}")
    opt = torch.optim.Adam(model.parameters(), lr=cfg["train"]["lr"])

    # Resumable: a 4-hour run must survive an interruption. The rolling state is
    # written every epoch alongside the best-checkpoint file.
    RESUME = os.path.join(OUT_DIR, "csdi_resume.pth")
    start_epoch = 1
    best_val = float("inf")
    if os.path.exists(RESUME) and not args.no_resume:
        st = torch.load(RESUME, map_location=device, weights_only=False)
        if st.get("config") == cfg:
            model.load_state_dict(st["model"])
            opt.load_state_dict(st["optimizer"])
            start_epoch = st["epoch"] + 1
            best_val = st["best_val"]
            print(f"resumed from epoch {st['epoch']} (best_val {best_val:.4f}); "
                  f"continuing at {start_epoch}")
        else:
            print("resume file found but config differs — starting fresh")

    if args.dry_run:
        batch = next(iter(train_loader))
        t0 = time.time()
        loss = model(batch, is_train=1)
        loss.backward()
        opt.step()
        if device.type == "cuda":
            print(f"peak VRAM: {torch.cuda.max_memory_allocated()/1e9:.2f} GB")
        print(f"dry-run loss={float(loss):.4f}  step time={time.time()-t0:.2f}s  OK")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    t_start = time.time()
    for epoch in range(start_epoch, args.epochs + 1):
        model.train()
        tr_loss, n_tr = 0.0, 0
        for batch in train_loader:
            loss = model(batch, is_train=1)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tr_loss += float(loss)
            n_tr += 1
        model.eval()
        va_loss, n_va = 0.0, 0
        with torch.no_grad():
            for batch in valid_loader:
                va_loss += float(model(batch, is_train=0))
                n_va += 1
        tr_loss /= max(n_tr, 1)
        va_loss /= max(n_va, 1)
        if va_loss < best_val:
            best_val = va_loss
            torch.save({"model": model.state_dict(), "config": cfg,
                        "target_dim": target_dim, "epoch": epoch,
                        "best_val": best_val, "mean": mean_data, "std": std_data},
                       os.path.join(OUT_DIR, "csdi_pangrango.pth"))
        # Rolling resume state, written EVERY epoch — otherwise an interrupted run
        # would lose any epoch that did not improve the validation loss.
        torch.save({"model": model.state_dict(), "optimizer": opt.state_dict(),
                    "config": cfg, "target_dim": target_dim, "epoch": epoch,
                    "best_val": best_val, "mean": mean_data, "std": std_data}, RESUME)
        print(f"epoch {epoch:3d}/{args.epochs}  train {tr_loss:.4f}  val {va_loss:.4f}  "
              f"best {best_val:.4f}  {time.time()-t_start:.0f}s", flush=True)

    print(f"done. best val {best_val:.4f}  checkpoint save/csdi_pangrango.pth")


if __name__ == "__main__":
    main()