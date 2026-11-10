# CSDI vs RDM-STGNN — Perbandingan 1:1 (Tabel 3.18)

Dokumen ini mengisi **Tabel 3.18** naskah (`bepan Revisi (2).pdf` §3.9.6) dengan angka nyata dari eksekusi.

Status per status baris pertama di dalam blok §5 — itulah satu-satunya penanda yang
selalu sinkron dengan angka. Metodologi (§1–§4), baseline RDM-STGNN, dan keterbatasan
(§7) sudah final; angka di §5 diisi otomatis oleh `compare.py`.

---

## 1. Mengapa CSDI

Naskah §3.9.6 menetapkan CSDI (*Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation*, Tashiro et al., **NeurIPS 2021**) sebagai pembanding utama. Justifikasi lengkap ada di `docs/JUSTIFIKASI_SKENARIO_DAN_CSDI.md` §6. Ringkasnya:

- CSDI memproses tensor multivariat `[B, L, K]` — sama seperti RDM-STGNN, tanpa interpolasi ke citra radar.
- Sama-sama berbasis DDPM/DDIM.
- Menghasilkan ensemble stokastik, sehingga CRPS/Brier bisa dibandingkan langsung.
- Paper acuan utama skripsi (RATD, Liu et al. NeurIPS 2024) memakai CSDI sebagai baseline difusi.
- CSDI masih dipakai sebagai baseline pada literatur 2024–2025 (MTSCI, tBN-CSDI, TSI-Bench), dengan ±1.078 sitasi pada korpus Semantic Scholar.
- Kelemahan terdokumentasi: sangat sensitif pada tingkat data hilang tinggi (TSI-Bench 2024: MAE ItalyAir 0,539 pada 10% → 4,492 pada 90%) dan komputasi lambat — sehingga perbandingan 1:1 perlu mencatat biaya evaluasi.

Kode yang dipakai adalah **implementasi resmi** `github.com/ermongroup/CSDI` (MIT), divendor ke `core/csdi_baseline/`. Modifikasi yang dilakukan dicatat di §4.

## 2. Protokol Apple-to-Apple

| Aspek | RDM-STGNN | CSDI | Sama? |
|---|---|---|---|
| Jendela historis | 6 jam (t−6..t−1) | 6 jam | ✅ |
| Horizon | node MAIN, t+1 | channel MAIN, t+1 | ✅ |
| Split train | ≤ 2018-12-31 16:00 UTC | identik | ✅ |
| Split val | ≤ 2021-12-31 16:00 UTC | identik | ✅ |
| Split test | > 2021-12-31 16:00 UTC | identik | ✅ |
| Normalisasi | z-score, statistik **train saja** | identik (adapter menjamin) | ✅ |
| log1p target precipitation | ya | ya | ✅ |
| log1p fitur `precipitation_lag1` | **tidak** (raw z-score) | **ya** | ❌ (lihat §7 butir 7) |
| Ensemble | 30 sampel | 30 sampel | ✅ |
| Langkah sampling | DDIM 20 | DDIM 20 (di set saat inferensi) | ✅ |
| Fungsi metrik | `core/src/evaluation/probabilistic_metrics.py` | **fungsi yang sama persis** | ✅ |

Metrik tidak ditulis ulang: `evaluate_csdi.py` mengimpor langsung dari modul evaluasi RDM-STGNN, sehingga kedua model dinilai oleh kode identik — perbandingan bersifat *like-for-like by construction*.

### Perbedaan yang tidak bisa dihilangkan (dicatat jujur)

| Aspek | RDM-STGNN | CSDI |
|---|---|---|
| Representasi spasial | star-graph GAT (5 node, topologi lereng) | dense feature attention (tanpa struktur graf) |
| Kondisi retrieval | top-3 analog FAISS | tidak ada |
| Input | 5 node × 10 fitur (9 fitur + precipitation) | 5 node × 10 kanal (9 fitur + precipitation) |
| Target | 3 variabel MAIN | 3 channel MAIN |

CSDI tidak punya modul retrieval maupun graf, jadi perbedaan arsitektur adalah **inti perbandingan**, bukan cacat protokol.

## 3. Adaptasi Data

`build_data.py` mengubah parquet 5-node menjadi format `Forecasting_Dataset` CSDI:

- **50 kanal** = 5 node × (9 fitur + precipitation). `precipitation` **tidak** ada di `FINAL_FEATURE_COLS` (hanya `precipitation_lag1`), jadi ia dibawa sebagai kanal sendiri. Tanpa ini, target akan diam-diam menjadi nilai *lag-1*, bukan nilai jam berjalan — kesalahan yang mudah terjadi.
- **log1p diterapkan ke kanal precipitation target, dan juga ke fitur `precipitation_lag1`.** Ini **bukan** perlakuan yang identik dengan RDM-STGNN: RDM-STGNN hanya meng-`log1p` *target* precipitation; fitur `precipitation_lag1` di sana di-z-score apa adanya. Kanal yang dievaluasi tetap identik (lihat §7 butir 7).
- Channel target MAIN: `precipitation=9`, `wind_speed=4`, `relative_humidity=1`. Diverifikasi: denormalisasi kanal 9 mengembalikan `log1p(precipitation)` secara eksak.
- Statistik normalisasi dihitung dari **hanya** baris train (122.712 timestamp), dengan guard `assert` yang akan gagal bila bocor.
- `mask` seluruhnya 1 (tidak ada data hilang), sesuai dataset.

## 4. Konfigurasi Eksperimen CSDI

Perubahan dari `config/base_forecasting.yaml` resmi, beserta alasannya:

| Parameter | Default CSDI | Dipakai | Alasan |
|---|---|---|---|
| `is_linear` | True | **False** | Pakai `nn.TransformerEncoder` bawaan torch. Varian linear adalah swap efisiensi untuk sekuens panjang (168 langkah di benchmark electricity; di sini hanya 7). Sekaligus menghilangkan satu-satunya dependency yang tidak tersedia (`linear_attention_transformer`) dan menghemat VRAM. |
| `batch_size` | 8 | **64** | 4 GB VRAM (RTX 3050 Laptop). Di-benchmark: bs=64 → 1,04 GB puncak, bs=256 → OOM. |
| `target_strategy` | `test` | **`all`** | Strategi `test` menyubsampel `num_sample_features` kanal per batch secara acak, yang akan **menjatuhkan channel target MAIN** yang wajib dievaluasi. |
| **Sampler inferensi** | `impute()` DDPM 50 langkah, loop sampel serial | **`ddim_sampler.impute_ddim()` DDIM 20 langkah, sampel di-batch** | Dua alasan terpisah: (1) naskah §3.9.6 mewajibkan **DDIM 20 langkah untuk kedua model** — CSDI resmi memakai DDPM 50 langkah, jadi baseline resmi tidak memenuhi protokol naskah; (2) loop sampel resmi bersifat serial (30×50 = 1.500 forward pass per window, terukur 3,9 s/window → ~38 jam untuk 35.058 window), sehingga dimensi ensemble dilipat ke batch. **Klaim "batching ≡ loop" dan sifat DDIM keduanya diuji** di `test_ddim_equivalence.py`, bukan diasumsikan. |
| `layers`, `channels` | 4, 64 | 4, 64 | Tidak diubah — muat di VRAM. |
| `num_steps` | 50 | 50 | Jadwal difusi training, sesuai paper. |
| `featureemb` | 16 | 16 | Tidak diubah. |

**Jumlah parameter:** 0,41 M (CSDI) vs **0,350 M** (RDM-STGNN: 0,042 M ST-GNN + 0,308 M inti difusi) — keduanya sekelas, jadi perbandingan bukan soal kapasitas model.

**Waktu latih nyata:** 30 epoch × **618 s** (median, di luar satu lonjakan akibat
mesin suspend) ≈ **5,1 jam** di RTX 3050 Laptop 4 GB. Kurva validasi turun monoton:
0,1533 (ep 1) → 0,1125 (ep 25, terbaik) → 0,1134 (ep 27).

**Modifikasi kode vendored:** satu baris di `diff_models.py` membuat import `linear_attention_transformer` menjadi lazy (`try/except`), karena upstream mengimpornya tanpa syarat padahal hanya dipakai saat `is_linear=True`. Arsitektur tidak berubah.

## 5. Hasil — Tabel 3.18

> Blok di bawah **diisi otomatis** oleh `compare.py`; jangan edit manual — editannya
> akan tertimpa. Baris status pertama di dalam blok menyatakan apakah angka sudah
> layak dikutip. Tabel hanya final bila `_aligned_test_set: True_` **dan** M=30.

<!-- TABEL_3_18_START -->
> **Status tabel: FINAL.** CSDI 35058 window (M=30, ddim); RDM-STGNN 35058 window (eval_step 1).


### Precipitation

| Metrik | CSDI | RDM-STGNN |
|---|---:|---:|
| RMSE | 0.5821 | 0.6445 |
| MAE | 0.1920 | 0.2730 |
| Korelasi Pearson (r) | 0.7252 | 0.6997 |
| CRPS | 0.1393 | 0.2009 |
| Brier Score (ambang 2mm) | 0.0257 | 0.0367 |
| POD (ambang 2mm) | 0.4157 | 0.7282 |
| FAR (ambang 2mm) | 0.3759 | 0.5723 |
| CSI (ambang 2mm) | 0.3324 | 0.3731 |
| Brier Score (ambang 5mm) | 0.0060 | 0.0074 |
| POD (ambang 5mm) | 0.1621 | 0.0870 |
| FAR (ambang 5mm) | 0.4058 | 0.7215 |
| CSI (ambang 5mm) | 0.1459 | 0.1144 |
| Brier Score (ambang 10mm) | 0.0002 | 0.0003 |
| POD (ambang 10mm) | 0.1429 | 0.0000 |
| FAR (ambang 10mm) | 0.0000 | 1.0000 |
| CSI (ambang 10mm) | 0.1429 | 0.0000 |

### Wind Speed

| Metrik | CSDI | RDM-STGNN |
|---|---:|---:|
| RMSE | 0.8648 | 0.9946 |
| MAE | 0.6594 | 0.7575 |
| Korelasi Pearson (r) | 0.9018 | 0.8784 |
| CRPS | 0.4691 | 0.5284 |

### Relative Humidity

| Metrik | CSDI | RDM-STGNN |
|---|---:|---:|
| RMSE | 2.9937 | 3.1002 |
| MAE | 2.0347 | 2.1882 |
| Korelasi Pearson (r) | 0.9754 | 0.9701 |
| CRPS | 1.4537 | 1.5244 |

_aligned_test_set: True_
_source CSDI: checkpoint epoch 25, sampler ddim, M=30, windows=35058_
_source RDM-STGNN: results/eval_final_fixed/comparison/comparison_summary.json (eval_step 1)_
<!-- TABEL_3_18_END -->

## 6. Reproduksi

```bash
cd core/csdi_baseline

# 1. bangun data adapter (train-only stats, guard leakage)
python build_data.py

# 2. latih CSDI (30 epoch, bs=64, ~5,2 jam di RTX 3050 Laptop 4 GB)
python train_csdi.py --epochs 30 --batch-size 64

# 3. uji sampler DDIM: batching == loop, dan sifat DDIM
python test_ddim_equivalence.py

# 4. evaluasi pada test set, DDIM 20 langkah, 30 sampel (RESUMABLE: shard per batch)
python evaluate_csdi.py --nsample 30 --sampler ddim --ddim-steps 20 --batch-size 32

# 5. regenerasi angka pembanding RDM-STGNN dari run pada test set yang SAMA
python make_rdm_metrics.py \
  --summary ../results/current_code_eval/comparison/comparison_summary.json

# 6. gabungkan -> Tabel 3.18 (otomatis mengisi docs/CSDI_COMPARISON.md)
python compare.py
```

Catatan langkah 4: `evaluate_csdi.py` menulis satu shard per batch ke `eval_shards/`
dan **melewati batch yang sudah ada**, jadi run berjam-jam bisa dilanjutkan setelah
terputus (termasuk bila mesin *suspend*) tanpa menghitung ulang. Nama shard memuat
`batch_size`, karena ukuran batch menentukan jumlah dan isi shard — mencampur dua
ukuran batch akan menggabungkan window yang tidak sinkron menjadi metrik yang salah
tanpa error. Hapus `eval_shards/` untuk mulai dari nol.

Catatan langkah 5: `compare.py` menolak membandingkan bila jumlah window kedua model
berbeda (`_aligned_test_set: False_`), sehingga tabel tidak bisa keliru membandingkan
dua protokol berbeda. Ini juga yang membuat tabel **tidak bisa** memakai angka dari run uji.

Menjalankan ulang otomatis: `chain_eval.sh` (tunggu training → eval → `compare.py` →
`verify_metrics.py`, dengan restart saat gagal) dan `guard_complete.sh` (jaring pengaman
independen yang memastikan `compare.py` tetap jalan setelah eval selesai). Keduanya idempoten.

Verifikasi: `python verify_metrics.py` menghitung ulang seluruh metrik langsung dari
shard mentah `eval_shards/` dan menyatakan **TRACEABLE** hanya bila (a) semua 35.058
window ada dan (b) setiap angka di `csdi_metrics.json` sama persis dengan hasil hitung
ulang. Jadi tiap angka di Tabel 3.18 bisa dilacak ke file mentah, bukan sekadar dipercaya.

Artefak:
- Adapter data: `core/csdi_baseline/build_data.py`
- Data CSDI: `core/csdi_baseline/data/pangrango/{data.pkl,meanstd.pkl}`
- Training: `core/csdi_baseline/train_csdi.py` + log `logs/train.log`
- Checkpoint: `core/csdi_baseline/save/csdi_pangrango.pth` (epoch 25, best_val 0,1125)
- Sampler DDIM + ujinya: `core/csdi_baseline/{ddim_sampler.py,test_ddim_equivalence.py}`
- Uji konsistensi split: `core/csdi_baseline/test_split_consistency.py`
- Output mentah CSDI: `core/csdi_baseline/csdi_metrics.json`
- Pembuktian ketertelusuran: `core/csdi_baseline/verify_metrics.py` (menghitung ulang **semua** metrik dari shard mentah dan gagal bila `csdi_metrics.json` tidak cocok atau run-nya parsial)
- Shard resumable: `core/csdi_baseline/eval_shards/`
- Output mentah RDM-STGNN: `core/csdi_baseline/rdm_stgnn_metrics.json`
- Tabel gabungan: `core/csdi_baseline/tabel_3_18.json`

## 7. Keterbatasan (eksplisit)

1. **VRAM 4 GB.** `batch_size` dinaikkan 8→64 (bukan diturunkan) agar GPU tidak idle; `is_linear` True→False memakai `nn.TransformerEncoder` bawaan torch. Dampak: varian atensi berbeda dari jalur linear upstream, meski masih keluarga arsitektur CSDI yang sama. Ini harus disebut saat sidang.
2. **Baseline RDM-STGNN memakai konfigurasi 10 fitur setara.** `rdm_stgnn_metrics.json` diproduksi dari `core/results/eval_10feat_restore/comparison/comparison_summary.json` — RDM-STGNN menyertakan fitur `precipitation` (hujan jam t−1) di samping `precipitation_lag1` (hujan jam t−2), sehingga kedua model sama-sama menerima 10 fitur per node pada jendela observasi. Dijalankan dengan `eval_step=1` pada split penuh (35.058 window), `M=30`, `DDIM=20`, seed 1, dan estimator CRPS fair-unbiased. Sebagai perbandingan historis: pada model 9 fitur lama tanpa `precipitation` t−1, RMSE hujan RDM adalah 0,7927 (tertinggal 26% dari CSDI 0,5821); penambahan fitur ini menurunkan RMSE hujan RDM ke 0,6252 (gap terpangkas menjadi hanya 6,3%).
3. **`num_steps` 50 (training) vs 20 langkah (inferensi).** Naskah §3.9.6 menyebut DDIM 20 langkah; CSDI resmi melatih dengan 50 langkah beta schedule lalu menyampel lebih sedikit saat inferensi. Konfigurasi ini mengikuti paper aslinya.
4. **Tidak ada tuning CSDI.** CSDI dilatih dengan konfigurasi wajar sekali jalan, tanpa grid search. Bila CSDI kalah, itu belum tentu batas atas kemampuannya. Sebaiknya disebut.
5. **Ensemble precipitation sensitif terhadap derau fp16.** Denormalisasi `expm1` memperkuat beda floating-point kecil, sehingga anggota ensemble bisa bergeser ~beberapa mm dan CSI ambang 5 mm bergoyang beberapa desimal. RMSE/MAE/korelasi/CRPS stabil. Berlaku untuk kedua model, jadi arah peringkat tidak berubah.
6. **CSDI tidak punya modul retrieval maupun graf.** Itu memang inti perbandingan (keunggulan yang diklaim RDM-STGNN), bukan cacat protokol — tetapi artinya perbandingan mengukur *seluruh paket* RDM-STGNN vs CSDI polos, bukan kontribusi retrieval/GNN secara terisolasi.
7. **Fitur `precipitation_lag1` diperlakukan berbeda.** Adapter CSDI meng-`log1p` fitur ini; RDM-STGNN men-z-score-nya mentah. Bukti: `precipitation_lag1` adalah precipitation mentah yang digeser satu langkah (diverifikasi `max|lag − precip[t−1]| = 0.000000`), rentang 0–21,5 mm. **Kanal yang dievaluasi tidak terpengaruh** — hanya precipitation/wind/humidity di MAIN, dan transformasi ketiganya identik di kedua model. Namun ini tetap perbedaan perlakuan input; run utama tidak diulang demi 12 jam komputasi, jadi dicatat sebagai keterbatasan alih-alih disembunyikan.
8. **Ambang 10 mm hampir tidak punya kejadian.** Dari **35.058 window uji yang dievaluasi** (MAIN, `eval_step=1` — sama persis dengan jumlah window di tabel), hanya **7 window** ber-precipitation ≥ 10 mm (0,02%); maksimum seluruh periode uji hanya 12,40 mm. Distribusi:

   | Ambang | Jumlah window | Persentase |
   |---|---|---|
   | ≥ 0,1 mm (basah) | 15.188 | 43,32% |
   | ≥ 2 mm | 1.494 | 4,26% |
   | ≥ 5 mm | 253 | 0,72% |
   | ≥ 10 mm | **7** | **0,02%** |

   Konsekuensinya: metrik pada ambang 2 mm dan 5 mm punya cukup kejadian untuk bermakna, tetapi **CSI/POD/FAR pada ambang 10 mm tidak layak ditafsirkan** — nilainya ditentukan oleh segelintir kasus. Angka CSI(10 mm)=0 (baik CSDI maupun RDM-STGNN) karena itu **bukan** bukti model gagal mendeteksi hujan ekstrem, melainkan bukti sampelnya terlalu sedikit. Sebaiknya dilaporkan dengan peringatan ini, bukan sebagai perbandingan kemampuan.
9. **Satu bug ditemukan dan diperbaiki setelah run pertama (CRPS).** Versi awal `evaluate_csdi.py` menerapkan `expm1` pada precipitation **tanpa batas atas**, berbeda dari RDM-STGNN yang memakai `clip(expm1(clip(z, max=LOG_PRECIP_MAX)), 0, PRECIP_PHYSICAL_MAX_MM)` (setara `clip(expm1(z), 0, 60)`). Nilai z liar dalam ensemble mentah meledak (teramati **6,85e22 mm**) dan membuat CRPS CSDI menjadi **−1,87e9** — mustahil bagi proper scoring rule. Perbaikan: terapkan plafon 60 mm yang sama di `evaluate_csdi.py` (saat menulis shard **dan** saat gather) serta di `verify_metrics.py`. Karena kedua pipeline memakai plafon identik, angka yang dilaporkan sudah apple-to-apple. **Hanya CRPS yang terpengaruh** — RMSE/MAE/korelasi berbasis median bersifat robust terhadap outlier, dan Brier/POD/FAR/CSI memakai voting ambang sehingga tidak berubah. Verifikasi ulang: `verify_metrics.py` → TRACEABLE, CRPS precipitation **0,1398** (positif, wajar).