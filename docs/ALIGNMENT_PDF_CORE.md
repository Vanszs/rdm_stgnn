# ALIGNMENT REPORT — PDF `bepan Revisi (2).pdf` vs `core/`

Sumber PDF: `/home/vanszs/Downloads/bepan Revisi (2).pdf` (93 halaman, diekstrak ke `/tmp/pdfalign/`).
Metode: 6 subagent read-only (model Gemini), split per subbab; **setiap temuan diverifikasi ulang oleh auditor utama** terhadap teks PDF dan baris kode nyata. Tidak ada asumsi; tidak ada file diubah.

Status dokumen ini: **LAPORAN SAJA — belum ada perubahan kode.** Menunggu keputusan.

---

## 0. RINGKASAN

| Kategori | Jumlah |
|---|---|
| MATCH (sesuai) | ~100 klaim |
| **MISMATCH nyata (terverifikasi)** | **8 kelompok** |
| Hanya di PDF, tidak ada di kode | 3 |
| Hanya di kode, tidak ada di PDF | 2 |
| **PDF kontradiksi dengan dirinya sendiri** | 1 (kritis) + 3 (penomoran gambar/tabel) |

---

## 1. TEMUAN KRITIS — KONTRADIKSI INTERNAL PDF

### 1.1 PDF bertentangan soal nama variabel target/fitur

Ini yang membuat "align 1:1" tidak bisa dijalankan tanpa keputusan Anda.

**PDF p059 §3.4.2 (halaman 45), verbatim:**
> "Harmonisasi ini menghilangkan keterangan ketinggian pengukuran seperti `_2m` dan `_10m` pada nama untuk analisis"

**PDF Tabel 3.5 (p059–p060), verbatim:**

| field API | nama untuk analisis |
|---|---|
| `temperature_2m` | `temperature` |
| `relative_humidity_2m` | `relative_humidity` |
| `dew_point_2m` | `dewpoint` |
| `wind_speed_10m` | `wind_speed` |
| `wind_direction_10m` | `wind_direction` |

**PDF p068 §3.6.1 (halaman 54), Tabel 3.13 — sembilan fitur, verbatim:** `temperature`, `relative_humidity`, `dewpoint`, `surface_pressure`, `wind_speed`, `wind_direction`, `cloud_cover`, `precipitation_lag1`, `elevation`.
**Target (p068), verbatim:** "yaitu precipitation, wind_speed, dan relative_humidity."

**Kode `core/src/config.py:86-90, 114-124`:** target = `precipitation`, `wind_speed_10m`, `relative_humidity_2m`; fitur = `temperature_2m`, `relative_humidity_2m`, `dewpoint_2m`, `surface_pressure`, `wind_speed_10m`, `wind_direction_10m`, `cloud_cover`, `precipitation_lag1`, `elevation`.

**Kontradiksi internal PDF:** di tempat lain PDF memakai nama bersufiks —
- **p054 (Gambar 3.2, field API)** dan **p055 (Tabel 3.4)** memakai `temperature_2m` / `relative_humidity_2m` / `wind_speed_10m` / `wind_direction_10m`.

Ketiganya masih bisa dirujuk balik sebagai "field sumber", jadi tidak fatal. **Tapi Tabel 3.5 + §3.4.2 + Tabel 3.13 eksplisit menyatakan nama analisis TANPA sufiks**, sedangkan data tersimpan dan checkpoint memakai sufiks. **Ini MISMATCH nyata.**

**Blocker teknis yang terverifikasi** (hasil load checkpoint nyata):
```
checkpoint['config']['target_cols']  = ['precipitation','wind_speed_10m','relative_humidity_2m']
checkpoint['config']['feature_cols'] = ['temperature_2m',...,'wind_direction_10m',...]
parquet columns (data/raw/*.parquet) = [...,'temperature_2m','relative_humidity_2m','dewpoint_2m',
                                         'wind_speed_10m','wind_direction_10m',...]
```
Renaming kolom di kode **tanpa** regenerate parquet + retrain model akan memutus `validate_feature_schema` (`config.py:142`) dan membuat `diffusion_chkpt.pth` tidak bisa dipakai. **Butuh keputusan Anda.**

### 1.2 Penomoran Gambar & Tabel di PDF salah (bukan masalah kode)

PDF merujuk nomor yang tidak cocok dengan caption-nya sendiri:
- p056 menyebut "Gambar 3.3" untuk posisi node; caption Gambar 3.3 (p058) = "Flowchart Preprocessing Data".
- p058 menyebut "Gambar 3.4"; caption p058 = "Gambar 3.3".
- p063 menyebut "Gambar 3.5"; caption = "Gambar 3.4".
- p060 menyebut "Tabel 3.5 dan Tabel 3.6"; caption = "Tabel 3.6".
- p081/p082 menyebut "Tabel 3.16"; caption = "Tabel 3.17".
- Dua "Gambar 3.6" berbeda (p070 arsitektur STGNN, p088 mockup dashboard).

Ini cacat penulisan dokumen, bukan `core/`.

---

## 2. MISMATCH NYATA (kode perlu diubah, atau PDF perlu dikoreksi)

### 2.1 `hidden_dim` diffusion: PDF P79=128, tapi ada bagian lain PDF bilang 64

- **PDF p079 (Tabel 3.15, halaman 63)**, verbatim: `Time MLP: SinusoidalPosEmb(64) + Linear(64,128) + Linear(128,64)`, `Context MLP: Linear(9,64)`, `Graph MLP: Linear(64,64)`, `Down2: Linear(64,128)`, `Mid: Linear(128,128)`, `Up MLP: Linear(256,64)`.
- **PDF p071–p072 §3.7.1**, verbatim: `d₁ = 64 per head`, `K₂=1 untuk memetakan ... menjadi representasi spasial lokal berdimensi 64`, `graph embedding h_graph ∈ R⁶⁴`.
- **Kode** (`train.py:263` default `hidden_dim=128`; `train.py:483` STGNN pakai `hidden_dim//2 = 64`; `train.py:496` diffusion pakai `hidden_dim = 128`; checkpoint `hidden_dim=128`, `graph_dim=64`): **semua cocok dengan PDF.**

**Kesimpulan: MATCH.** (Dua subagent sempat melaporkan MISMATCH pada `graph_mlp`/`retrieval_mlp` — itu **salah**; mereka membaca default `ConditionalDiffusionModel.__init__` (`graph_dim=64, retrieval_dim=32, hidden_dim=64`) padahal model nyata dibangun lewat `train.py` dengan `hidden_dim=128`, `retrieval_dim=num_targets*k=9`.) Sudah diverifikasi manual dan ditolak.

### 2.2 `wet_probability_threshold`: PDF=0,6; kode default=0,5; checkpoint=0,6

- **PDF p084 §3.8.4**, verbatim: "Jika probabilitas hujan pada suatu jendela berada di bawah ambang **0,6**, komponen curah hujan ... diatur menjadi 0".
- **Kode `core/src/inference.py:116, 297`:** default fallback `0.5`.
- **Checkpoint nyata:** `'wet_probability_threshold': 0.6000000238418579`.
- **Kode `core/src/train.py:243, 697, 784, 852`:** threshold **dikalibrasi** saat training (bukan konstanta), dan hasilnya tersimpan di checkpoint = 0,6.

**Kesimpulan: MATCH pada perilaku** (saat runtime pakai 0,6 dari checkpoint). Default `0.5` hanya terpakai jika checkpoint tidak punya `rain_specialization` — jalur yang tidak terjadi. Bukan mismatch perilaku, tapi **nilai default di kode tidak sesuai angka PDF**. Kandidat koreksi bila ingin literal.

### 2.3 Skema pembagian dataset: PDF Tabel 3.10 angkanya TIDAK cocok dengan data

**PDF p064 Tabel 3.10, verbatim:** Training `2005–2018` = **613.560** baris; Validation `2019–2021` = **131.520**; Test `2022–2025` = **175.320**; total 920.400. Teks p064: train `122.712` timestamp, val `26.304`, test `35.064`.

**Hasil hitung ulang dari parquet nyata (`data/raw/pangrango_era5_5node_2005_2025.parquet`) memakai aturan kode (`train.py:52` `train_end=2018-12-31`, `val_end=2021-12-31`):**

| himpunan | PDF (Tabel 3.10) | PDF (teks p064) | kode/data nyata | selisih |
|---|---|---|---|---|
| train | 613.560 | 122.712 ts | **613.480** | PDF +80 baris |
| val | 131.520 | 26.304 ts | **131.520** | cocok |
| test | 175.320 | 35.064 ts | **175.400** | PDF −80 baris |
| total | 920.400 | 184.080 ts | 920.400 | cocok |
| train ts | — | 122.712 | **122.696** | PDF +16 |
| test ts | — | 35.064 | **35.080** | PDF −16 |

**Kesimpulan: MISMATCH.** Selisih 80 baris (16 timestamp × 5 node) — PDF lebih banyak di train, kode lebih banyak di test. Artinya batas potong PDF berbeda tipis dari aturan `<=`/`>` di kode. **Ini perlu diputuskan: perbaiki PDF, atau ubah `train_end`.**

### 2.4 Model pembanding **CSDI** tidak ada di kode sama sekali

- **PDF p086 §3.9.6**, verbatim: "membandingkan performa model RDM-STGNN yang diusulkan secara langsung terhadap model pembanding utama **CSDI** ... pada data pengujian (test set) periode 2022–2025".
- **PDF p082–p083 Tabel 3.18**: hanya berkolom `CSDI` dan `RDM-STGNN`.
- **Kode:** `grep -rn -i "csdi" core api web/src` → **nol**. Tidak ada implementasi, bobot, runner, maupun skrip evaluasi CSDI.

**Kesimpulan: NOT_FOUND_IN_CODE.** PDF menjanjikan pembanding yang tidak pernah ada di repo. (Catatan: sebelum konsolidasi, repo ini punya pembanding MLP + persistence — bukan CSDI, dan keduanya baru dihapus atas keputusan 1A Anda.)

### 2.5 Skenario pengujian: PDF (CSDI) vs kode (ablasi internal) — tidak sama

- **PDF Tabel 3.18:** baris = `CSDI`, `RDM-STGNN`.
- **Kode `run_eval_final.py:414-435`:** `diff_only`, `diff_retrieval`, `diff_gnn`, `full_model` (4 skenario ablasi internal).

**Kesimpulan: MISMATCH.** PDF tidak menyebut ablasi; kode tidak menyebut CSDI. Dua skema pengujian yang berbeda.

### 2.6 Tabel 3.17 (5 skenario hyperparameter) tidak ada runner-nya

- **PDF p082 Tabel 3.17**, verbatim: 5 skenario kombinasi `Learning Rate` / `Epoch (Patience)` / `k (FAISS)` dll.
- **Kode `core/src/train.py`:** hanya punya argparse argumen tunggal (`--lr`, `--epochs`, `--patience`, `--k-neighbors`); **tidak ada** skrip/loop yang menjalankan 5 skenario tersebut otomatis, dan tidak ada artefak hasil per skenario.

**Kesimpulan: NOT_FOUND_IN_CODE.** 5 skenario itu harus dijalankan manual.

### 2.7 Prosedur pelatihan: PDF menyebut "dua tahap (decoupled)" tapi juga "satu optimizer"

- **PDF p081 §3.8**, verbatim: "pelatihan dirancang terpisah menjadi dua tahap (**decoupled training**) ... STGNN dilatih terlebih dahulu ... sebelum model difusi (RDM) dilatih".
- **PDF p081 §3.8.1** (halaman yang sama), verbatim: "STGNN tidak memiliki fungsi loss mandiri ... bobotnya diperbarui **bersama** denoiser MLP melalui **satu** optimizer AdamW berdasarkan sinyal gradien dari L_total".
- **Kode `train.py:497-501`:** `trainable_params = list(st_gnn.parameters()) + list(diff_model.parameters())` → satu optimizer.

**Kesimpulan: AMBIGUOUS_IN_PDF.** Kalimat pertama bilang terpisah, kalimat kedua bilang bersama; kode mengikuti yang kedua (bersama). PDF perlu diperjelas.

### 2.8 Cakupan evaluasi: kode mampu, tapi beberapa skenario hanya dijalankan di kode

- **PDF p085 §3.9.2–3.9.5** menyebut: MAE, RMSE, korelasi Pearson, CRPS, Brier, POD, FAR, CSI, reliability diagram; ambang kejadian **2, 5, 10 mm/jam**; probabilitas **0,5**; reliability **10 bin pada ambang 2 mm/jam**.
- **Kode:** semua ada dan **cocok** — `THRESHOLDS_PRECIP = [2.0, 5.0, 10.0]` (`run_eval_final.py:57`), `PROB_EVENT_THRESHOLD = 0.5` (`config.py:112`), `plot_reliability` (`run_eval_final.py:320`), `compute_reliability_data` (`probabilistic_metrics.py:284`).

**Kesimpulan: MATCH.** (Satu subagent melaporkan "CSDI basis evaluasi" sebagai mismatch; itu benar untuk CSDI, sudah dicatat di §2.4.)

---

## 3. HANYA DI PDF (tidak ada padanan di kode)

| # | Klaim PDF | Bukti |
|---|---|---|
| 3.1 | Pembanding **CSDI** (§3.9.6 Tabel 3.18) | grep `csdi` = 0 |
| 3.2 | **5 skenario** hyperparameter Tabel 3.17 | tidak ada runner di `train.py` |
| 3.3 | Nama file dataset mentah & file validasi grid **tidak disebut** di PDF | kode punya `CANONICAL_DATA_PATH` / `GRID_VALIDATION_PATH` (`ingest.py:26-27`) |

## 4. HANYA DI KODE (tidak ada di PDF)

| # | Item kode | Bukti |
|---|---|---|
| 4.1 | Skrip ablasi `diff_only` / `diff_retrieval` / `diff_gnn` | `run_eval_final.py:414-435`; Tabel 3.18 tidak memuatnya |
| 4.2 | `core/scripts/eval_rain_robust.py` (crosscheck mingguan) | tidak dirujuk PDF |

---

## 5. YANG SUDAH MATCH (terverifikasi, tidak perlu diubah)

- **Node & koordinat**: MAIN(-6.75,107.00), UP(-6.50,107.00), DOWN(-7.00,107.00), LEFT(-6.75,106.75), RIGHT(-6.75,107.25) — `config.py:22-63`. PDF p053.
- **Elevasi**: 1529 / 162 / 0 / 823 / 288 — `config.py:29-61`. PDF p057 Tabel 3.3.
- **Topologi star, 8 edge berarah** — `config.py:74-84`. PDF p069.
- **API**: `models=era5`, endpoint archive, `timezone=Asia/Jakarta`, field hourly, cache+retry — `ingest.py:22-23,161-178`. PDF p054.
- **Rentang data 2005–2025**, 920.400 baris, 184.080 timestamp — terverifikasi dari parquet. PDF p055/p057.
- **Split cutoff**: `train_end=2018-12-31`, `val_end=2021-12-31` — `train.py:52`. PDF p064 (rentang tahun cocok; *jumlah baris* lihat §2.3).
- **Z-score epsilon 0,00001** — `config.py:98` `ZSCORE_EPSILON = 1e-5`. PDF p066.
- **log1p hanya untuk precipitation** — `temporal_loader.py:164`. PDF p062.
- **Statistik target dari MAIN; fitur dari MAIN dengan fallback all-node untuk fitur degenerat** — `train.py:63-108`. PDF p065.
- **9 fitur, 3 target, seq_len 6, konteks MAIN t−1** — `config.py` + `temporal_loader.py:39,204`. PDF p068.
- **Arsitektur STGNN**: 2 lapis GATConv, K₁=4 heads concat, K₂=1, ReLU, global_mean_pool; TemporalAttention 4 heads, pos_embedding learnable, residual+dropout(0,1)+LayerNorm, causal mask, slice `x[:,-1,:]`, output_proj Linear(64,64) — `gnn.py:23-134`. PDF p070-p073.
- **Arsitektur diffusion**: time_mlp SinusoidalPosEmb(64)→Linear(64,128)→GELU→Linear(128,64); cond/graph/retrieval MLP; down1 Linear(3,64)+SiLU+cond; down2 Linear(64,128); mid Linear(128,128); cat→Linear(256,64)→SiLU→Linear(64,3); wet_head Linear(64,64)→SiLU→Linear(64,1); `weighted_noise_loss` — `diffusion.py:57-101,180`. PDF p079-p080.
- **diffusion T=1000**, `torch.randint(0,1000)` — `config.py:103`. PDF p076/p082.
- **FAISS**: `IndexFlatL2`, k=3, retrieval embedding = 9 (3×3) — `retrieval/base.py:12,28` + checkpoint `k_neighbors=3`, `retrieval_dim=9`. PDF p075/p079.
- **Conditioning aditif** (`cond_emb + r_emb + g_emb`, `t_emb + cond_emb`) — `diffusion.py:117,121,147`. PDF p075/p079.
- **Ensemble 30 & DDIM 20 langkah** — `run_eval_final.py:385` `num_ensemble=30`, `config.py:99`. PDF p083/p086.
- **Optimizer AdamW lr 1e-3, epochs 20, patience 12, k=3** — `train.py:263-283`. PDF p082 Tabel 3.17 skenario 3.
- **Loss gabungan**: weighted noise loss + `wet_loss_weight=0.7` × wet loss — `train.py:280,581`. PDF p082.
- **Ambang kejadian hujan 0,1 mm/jam untuk label** — `train.py:279`. PDF p085/p082.
- **Batas fisik pasca-proses**: precip 0–60 mm/jam, wind ≥0, RH 0–100% — `config.py:95`, `inference.py:289-294`. PDF p084.
- **Rain gate + guard anti-degenerat** — `run_eval_final.py:222-225`. PDF p084.
- **Protokol**: eval_step=1, median ensemble untuk prediksi titik, CRPS fair/unbiased, single-member→MAE — `run_eval_final.py:210,546`, `probabilistic_metrics.py:108`. PDF p084/p085.

---

## 6. STATUS EKSEKUSI PENYELARASAN (arah: KODE menyesuaikan PDF)

Keputusan user: **sesuaikan kodenya, bukan PDF-nya.**

| # | Isu | Status | Bukti |
|---|---|---|---|
| **D1** | Nama variabel: harmonisasi menghapus `_2m`/`_10m` (PDF p059 §3.4.2, Tabel 3.5) | **SELESAI** | `config.py:86-90,114-124`; parquet 21 kolom di-rename; checkpoint `target_cols`/`feature_cols` diupdate. Bobot TIDAK berubah (state_dict nol nama kolom) — tidak perlu retrain. Grep produksi bersih. |
| **D2** | Batas split PDF Tabel 3.10 (p064): 613.560/131.520/175.320 | **SELESAI** | Batas tepat ditemukan: `2018-12-31 16:00` dan `2021-12-31 16:00` UTC (jendela utuh 14y/3y/4y dari awal data `2004-12-31 17:00`). `temporal_split` + checkpoint + semua fallback diupdate. Hitung ulang = **613.560 / 131.520 / 175.320** persis PDF. Sebelumnya 613.480/131.520/175.400 karena cutoff tanggal-saja memotong tengah hari. |
| **D3** | `wet_probability_threshold` default PDF=0,6 (p084 §3.8.4) | **SELESAI** | `inference.py` default fallback 0.5 → 0.6. Checkpoint memang sudah 0,6, jadi perubahan ini hanya menyelaraskan jalur tanpa metadata. |
| **D4** | Runner 5 skenario Tabel 3.17 | **TIDAK DIKERJAKAN** | Bukan bagian penyelarasan; dicatat sebagai gap. |
| **D5** | §3.8 PDF kontradiksi "decoupled" vs "satu optimizer" | **TIDAK DIUBAH (kode sudah benar)** | Kode `train.py:497-501` memakai satu optimizer AdamW untuk ST-GNN + denoiser, mengikuti kalimat kedua PDF ("bobotnya diperbarui bersama ... satu optimizer"). **PDF perlu dikoreksi penulis: kalimat "decoupled training ... dilatih terlebih dahulu" (p081) bertentangan dengan implementasi.** |

### 6.1 Item yang tetap tidak cocok (butuh keputusan lanjutan)

| # | Isu | Status |
|---|---|---|
| **CSDI** | PDF §3.9.6 + Tabel 3.18 menjadikan CSDI pembanding utama; kode nol implementasi | **GAP** — tidak diminta, tidak dikerjakan |
| **Skenario evaluasi** | PDF Tabel 3.18 = `CSDI` vs `RDM-STGNN`; kode = ablasi `diff_only`/`diff_retrieval`/`diff_gnn`/`full_model` | **GAP** — skema berbeda; kode memuat ablasi yang tidak ada di PDF |

### 6.2 Verifikasi akhir

- Test: **20/20 lulus** (`cd core && python -m pytest tests -q`).
  - Satu assertion test (`test_loader_contract.py`) memakai fixture dengan nama lama → diperbarui ke nama PDF. Itu test usang, bukan bug kode.
- E2E pada checkpoint nyata: mengembalikan kunci `precipitation`, `wind_speed`, `relative_humidity`; `raw (8,3)` finite; nama lama tidak ada.
- Grep nama bersufiks di produksi: hanya tersisa di (1) kamus pemetaan `OPTIONAL_LEGACY_RENAMES` dan (2) daftar parameter request API Open-Meteo — keduanya **harus** memakai nama field API, sesuai PDF §3.3.2.
- Backup sebelum perubahan: `/tmp/pdfalign/backup/` (2 parquet + checkpoint).
