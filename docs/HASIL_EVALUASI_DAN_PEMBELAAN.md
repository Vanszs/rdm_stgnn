# Hasil Evaluasi & Panduan Pembelaan (Tabel 3.18 Baru)

Dokumen ini merangkum hasil evaluasi terbaru setelah perbaikan protokol, alasan di balik hasil, bukti tidak ada kebocoran data, dan kemungkinan pertanyaan sidang beserta jawabannya.

## 1. Ringkasan eksekusi

- Waktu: 3 November 2026.
- Perangkat: RTX 3050 Laptop 4 GB, CUDA.
- RDM-STGNN: 4 skenario ablasi, 35.058 window, M=30, DDIM 20, `eval_step=1`, output `core/results/eval_final_fixed/`.
- CSDI: 1.096 shard (35.058 window), M=30, DDIM 20, checkpoint epoch 25.
- Validasi: `verify_metrics.py` → **TRACEABLE** (setiap angka tabel dihitung ulang dari shard mentah).
- Perbandingan: `compare.py` menolak tabel bila jumlah window tidak sama; kedua model 35.058.

## 2. Protokol 1:1

| Aspek | RDM-STGNN | CSDI |
|---|---|---|
| Data | ERA5 5 node, 10 kanal/node | sama |
| Split | train 2005–2018, val 2019–2021, test 2022–2025 | sama |
| Jendela | 6 jam → t+1 | sama |
| Normalisasi | statistik train | sama |
| Ensemble | 30 | 30 |
| Sampling | DDIM 20 | DDIM 20 |
| Metrik | `probabilistic_metrics.py` | fungsi yang sama |
| Window uji | 35.058 | 35.058 |

Perbedaan yang tersisa adalah **arsitektur**, bukan protokol. Itu memang objek penelitian.

## 3. Tabel 3.18 baru

### Presipitasi

| Metrik | CSDI | RDM-STGNN | Menang |
|---|---:|---:|---|
| RMSE | 0,5821 | 0,6641 | CSDI |
| MAE | 0,1920 | 0,2730 | CSDI |
| Korelasi | 0,7252 | 0,6997 | CSDI |
| CRPS | 0,1393 | 0,1953 | CSDI |
| Brier 2 mm | 0,0257 | 0,0367 | CSDI |
| POD 2 mm | 0,4157 | 0,7282 | RDM |
| FAR 2 mm | 0,3759 | 0,5723 | CSDI |
| CSI 2 mm | 0,3324 | 0,3688 | RDM |
| Brier 5 mm | 0,0060 | 0,0074 | CSDI |
| POD 5 mm | 0,1621 | 0,0870 | CSDI |
| FAR 5 mm | 0,4058 | 0,7215 | CSDI |
| CSI 5 mm | 0,1459 | 0,0710 | CSDI |
| Brier 10 mm | 0,0002 | 0,0003 | CSDI* |
| POD 10 mm | 0,1429 | 0,0000 | CSDI* |
| FAR 10 mm | 0,0000 | 1,0000 | CSDI* |
| CSI 10 mm | 0,1429 | 0,0000 | CSDI* |

\*Hanya 7 kejadian ≥10 mm (0,02%). Tidak layak ditafsirkan sebagai kemampuan.

### Angin

| Metrik | CSDI | RDM |
|---|---:|---:|
| RMSE | 0,8648 | 0,9946 |
| MAE | 0,6594 | 0,7575 |
| Korelasi | 0,9018 | 0,8784 |
| CRPS | 0,4691 | 0,5284 |

### Kelembapan

| Metrik | CSDI | RDM |
|---|---:|---:|
| RMSE | 2,9937 | 3,1002 |
| MAE | 2,0347 | 2,1882 |
| Korelasi | 0,9754 | 0,9701 |
| CRPS | 1,4537 | 1,5244 |

**Rekap: CSDI menang 22 baris, RDM 2 baris (POD 2 mm dan CSI 2 mm).**

## 4. Alasan logis CSDI menang

1. **Akses informasi.** Denoiser CSDI melihat seluruh tensor 50 kanal × 7 langkah di setiap langkah denoising. RDM hanya menerima 10 angka jam terakhir + 64 angka ringkasan graf + 9 angka retrieval.
2. **Supervisi lebih kaya.** CSDI men-denoise 50 kanal sekaligus; RDM hanya 3 target. Kanal lain menjadi tugas bantu yang memperkaya representasi.
3. **Kapasitas denoiser.** CSDI memakai transformer 4 blok (attention waktu + fitur); RDM memakai MLP.
4. **Graf kehilangan identitas target.** `global_mean_pool` merata-ratakan 5 node; titik puncak hanya 1/5. Ablasi: GNN-only CRPS 0,1974 vs tanpa GNN 0,1981 — pengaruh graf kecil.
5. **Retrieval tidak konsisten.** Saat training memakai tetangga deret yang sama; saat eval memakai DB train-only. Ablasi: retrieval memperburuk (CRPS 0,1988 vs 0,1981; CSI 5 mm 0,0345 vs 0,0642).
6. **Metrik dioptimalkan untuk CSI.** Ambang gate dikalibrasi memaksimalkan CSI. Akibatnya POD 2 mm tinggi tetapi FAR buruk; kalibrasi (Brier/CRPS) kalah.

## 5. Kontribusi RDM-STGNN

- Unggul **CSI 2 mm** (0,3688 vs 0,3324) dan POD 2 mm (0,7282 vs 0,4157).
- Namun FAR 2 mm lebih buruk (0,5723 vs 0,3759) — lebih banyak alarm palsu, bukan deteksi lebih baik.
- Inferensi jauh lebih ringan (orde milidetik per sampel vs detik).
- Memberi bukti kuantitatif bahwa retrieval dan graf belum memberi nilai tambah pada konfigurasi ini — temuan yang berguna, bukan kegagalan.

## 6. Bukti tidak ada kebocoran

- Target (t+1) di-mask untuk semua 50 kanal; sampler hanya menerima `mask × observed`.
- Uji perturbasi: nilai target diubah +123,456 → `max|Δsample| = 0,0`.
- Statistik normalisasi hanya dari train (selisih 0,0 terhadap hitungan ulang).
- Window train/val/test tidak menyeberang batas (setelah perbaikan).
- `verify_metrics.py` menyatakan TRACEABLE.

## 7. Mengapa memilih CSDI sebagai pembanding meski lebih kuat

- Baseline harus sekuat mungkin; paper acuan (RATD, NeurIPS 2024) memakai CSDI.
- Tujuan perbandingan adalah mengukur posisi, bukan mencari lawan yang mudah.
- Kalah dari baseline kuat tetap temuan ilmiah; menang dari baseline lemah tidak bernilai.
- CSDI dipakai apa adanya (tanpa melemahkan arsitekturnya); yang disamakan adalah protokol.

## 8. Batasan

1. Ambang 10 mm hanya 7 kejadian.
2. GPU 4 GB membatasi batch CSDI (32), bukan hasil.
3. CSDI berjalan fp32; RDM memakai autocast.
4. Hasil RDM bergantung pada checkpoint 10 fitur; naskah harus menyebut 10 fitur (bukan 9).
5. Angka lama Tabel 3.18 tidak berlaku; gunakan dokumen ini.

## 9. Reproduksi

```bash
cd core/csdi_baseline
python build_data.py
python evaluate_csdi.py --nsample 30 --sampler ddim --ddim-steps 20 --batch-size 32
python verify_metrics.py

cd ../..
python core/scripts/run_eval_final.py --scenarios all --eval-step 1 --num-ensemble 30 \
  --sample-batch-size 256 --out-dir results/eval_final_fixed

cd core/csdi_baseline
python make_rdm_metrics.py --summary ../results/eval_final_fixed/comparison/comparison_summary.json
python compare.py
```

## 10. Kemungkinan pertanyaan dosen dan jawaban

**Q1. Kenapa memilih CSDI kalau akhirnya kalah?**
Baseline harus kuat. CSDI adalah standar difusi deret waktu dan dipakai paper acuan. Tujuannya mengukur posisi metode, bukan memastikan menang.

**Q2. Kenapa CSDI menang?**
Karena melihat seluruh data mentah di setiap langkah denoising dan dilatih menebak 50 kanal sekaligus. RDM hanya menerima ringkasan dan menebak 3 angka.

**Q3. Apakah perbandingan adil?**
Ya. Data, split, 35.058 window, M=30, DDIM=20, dan fungsi metrik sama. Yang berbeda arsitektur — itu objek penelitian.

**Q4. Bagaimana membuktikan tidak ada kebocoran?**
Target di-mask untuk semua kanal; perturbasi target menghasilkan Δ=0; statistik hanya dari train; `verify_metrics` TRACEABLE.

**Q5. Kenapa POD 2 mm RDM lebih tinggi?**
Karena RDM lebih agresif memicu hujan. FAR-nya 0,5723 vs 0,3759, jadi peningkatan POD datang bersama alarm palsu.

**Q6. Kenapa CSI 2 mm RDM lebih tinggi tetapi CSI 5 mm kalah?**
Ambang gate dikalibrasi untuk CSI 2 mm. Pada kejadian lebih lebat, model cenderung melemahkan intensitas.

**Q7. Kenapa tidak memakai baseline yang lebih lemah agar menang?**
Itu tidak ilmiah. Baseline yang dilemahkan membuat kesimpulan tidak bisa dipercaya.

**Q8. Kalau kalah, apa kontribusi penelitian?**
Negative result yang terukur: retrieval dan graf belum memberi nilai tambah, plus arah perbaikan yang jelas (akses informasi penuh, pooling titik puncak, retrieval satu aturan).

**Q9. Kenapa 10 mm tidak dibahas?**
Hanya 7 kejadian. CSI/POD/FAR di ambang itu ditentukan segelintir kasus, bukan kemampuan model.

**Q10. Apakah hasil ini bisa direproduksi?**
Ya. Seed per skenario, determinisme diaktifkan, shard terikat hash checkpoint, dan `verify_metrics` menghitung ulang dari shard.

**Q11. Kenapa RDM lebih cepat?**
Outputnya 3 angka dengan MLP kecil; CSDI mengolah 50 kanal × 7 langkah dengan transformer.

**Q12. Apa langkah berikutnya agar RDM menyusul?**
Beri denoiser akses jendela penuh, ambil embedding titik puncak (bukan rata-rata), samakan perlakuan retrieval, dan kalibrasi untuk CRPS/Brier.

## 11. Kalimat siap pakai untuk naskah

> "Pada protokol 1:1 dengan 35.058 window uji, M=30, dan DDIM 20 langkah, CSDI unggul pada seluruh metrik akurasi dan kalibrasi serta pada ambang 5 mm. RDM-STGNN hanya unggul pada CSI 2 mm (0,3688 vs 0,3324), dengan FAR yang lebih tinggi. Tidak ditemukan kebocoran data; perbedaan hasil disebabkan oleh akses informasi dan supervisi arsitektur, bukan oleh perbedaan protokol."
