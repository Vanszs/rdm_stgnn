# Penyelarasan Fitur Temporal RDM-STGNN (Mode 10-Fitur: `both`)

Dokumen ini mencatat rasional teknis, perbaikan implementasi, dan bukti empiris dari penyelarasan fitur temporal presipitasi pada model RDM-STGNN.

---

## 1. Latar Belakang Masalah (Off-by-One Fitur Presipitasi)

Pada rancangan awal 9 fitur (`FINAL_FEATURE_COLS`), fitur presipitasi yang disertakan hanya `precipitation_lag1`, sedangkan variabel `precipitation` mentah tidak dimasukkan ke dalam daftar fitur karena kekhawatiran terjadinya kebocoran target (*target leakage*).

Namun, analisis aliran data (*data flow tracing*) membuktikan adanya defisit informasi 1 jam:
1. **Target Prediksi:** Horizon peramalan adalah $t$, yaitu nilai `precipitation`, `wind_speed`, dan `relative_humidity` pada jam $t$ di node MAIN.
2. **Jendela Konteks Observasi:** Model membaca jendela historis 6 jam, yaitu baris $t-6 \dots t-1$.
3. **Konsekuensi Kolom Lag:**
   - Di baris $t-1$, kolom cuaca standar (`temperature`, `wind_speed`, dll.) membawa kondisi mutakhir jam $t-1$.
   - Namun, kolom `precipitation_lag1` di baris $t-1$ berisi $\text{precipitation}(t-2)$ (karena definisi $\text{lag1}_i = \text{precipitation}_{i-1}$).
   - Akibatnya, model **tidak pernah menerima informasi curah hujan jam $t-1$**, melainkan hanya informasi curah hujan paling baru jam $t-2$.

Di sisi lain, model pembanding CSDI (`core/csdi_baseline/build_data.py`) menggunakan 50 kanal (5 node $\times$ 10 kanal: 9 fitur standar + 1 kanal `precipitation` mentah), sehingga CSDI menerima nilai presipitasi jam $t-1$. Hal ini menciptakan asimetri informasi di mana RDM-STGNN tertinggal 1 jam informasi autokorelasi hujan.

---

## 2. Resolusi: Konfigurasi 10 Fitur (`precip_mode="both"`)

Solusi yang diterapkan adalah menyertakan `precipitation` mentah ke dalam daftar fitur observasi bersama dengan `precipitation_lag1`:

$$\text{Fitur} = [\text{temperature}, \text{relative\_humidity}, \text{dewpoint}, \text{surface\_pressure}, \text{wind\_speed}, \text{wind\_direction}, \text{cloud\_cover}, \text{precipitation\_lag1}, \text{elevation}, \mathbf{precipitation}]$$

### Mengapa Tidak Bocor?
Jendela observasi berhenti tepat di baris $t-1$. Nilai `precipitation` pada baris $t-1$ adalah curah hujan masa lalu (1 jam sebelum target $t$). Target evaluasi di baris $t$ tetap tertutup dan tidak pernah tersentuh oleh jendela input.

### Mengapa Menyimpan Keduanya (`precipitation` dan `precipitation_lag1`)?
1. `precipitation` ($t-1$): Menyediakan kondisi intensitas hujan saat ini.
2. `precipitation_lag1` ($t-2$): Menyediakan dinamika/momentum perubahan intensitas ($t-2 \to t-1$).
3. **Kesetaraan 1:1 dengan CSDI:** CSDI mengalokasikan 10 kanal per node (9 fitur + `precipitation`), sehingga RDM-STGNN kini menerima jumlah dan jenis informasi yang identik (10 fitur per node pada ST-GNN, dan 10 fitur konteks pada node MAIN).

---

## 3. Hasil Pengujian Empiris (Test Set 35.058 Jendela, 2022–2025)

Pengujian dilakukan pada checkpoint terlatih 20 epoch dengan protokol penuh (35.058 jendela uji, ensemble $M=30$, langkah inferensi DDIM 20):

| Metrik | Model 9-Fitur Lama (t−2) | **Model 10-Fitur Baru (t−1 & t−2)** | Baseline CSDI | Perubahan vs Model Lama |
| :--- | :---:| :---:| :---:| :---:|
| **RMSE Presipitasi (mm/h)** | 0,7927 | **0,6252** | 0,5821 | **Turun 21,1%** |
| **MAE Presipitasi (mm/h)** | 0,3651 | **0,2568** | 0,1926 | **Turun 29,7%** |
| **Korelasi Pearson ($r$)** | 0,6278 | **0,7015** | 0,7212 | **Naik +11,7%** |
| **CRPS Presipitasi** | 0,2588 | **0,1843** | 0,1398 | **Turun 28,8%** |
| **CSI Ambang 2 mm** | 0,2758 | **0,3529** | 0,3295 | **Unggul (+28,0%)** |
| **FAR Ambang 5 mm** | 0,6901 | **0,2593** | 0,4394 | **Turun drastis (lebih baik)** |
| **RMSE Kecepatan Angin** | 0,9916 | **0,9857** | 0,8648 | Membaik |
| **RMSE Kelembapan Relatif** | 2,9287 | **2,8831** | 2,9865 | **Unggul dibanding CSDI** |

*Catatan:* Gap performa presipitasi antara RDM-STGNN dan CSDI yang semula 26,1% terpangkas menjadi hanya **6,3%**.

---

## 4. Lokasi Artefak

- Kode pelatihan: `core/src/train.py` (opsi CLI `--precip-mode both`, dijadikan default)
- Checkpoint model terlatih: `core/results/fix_lag1/model.pth`
- Evaluasi metrik lengkap: `core/results/fix_lag1/eval/comparison/comparison_summary.json`
- Laporan komparasi resmi: `docs/CSDI_COMPARISON.md` (Tabel 3.18)

> **Catatan kanonik:** angka pada tabel ini adalah hasil eksperimen historis (sebelum retrain 10-fitur final). Metrik kanonik: `core/results/eval_10feat_restore/`.
