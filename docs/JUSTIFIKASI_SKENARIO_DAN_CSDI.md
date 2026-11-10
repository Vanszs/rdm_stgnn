# Landasan Ilmiah Skenario Penalaan Hiperparameter dan Model Pembanding CSDI

Dokumen ini memuat landasan ilmiah komprehensif, berbasis bukti (*evidence-based*), dan bebas dari asumsi spekulatif mengenai:
1. Rasionalisasi metodologis pemilihan tepat 5 skenario penalaan hiperparameter RDM-STGNN.
2. Asal-usul teoritis penamaan skenario (*Operational Deployment Profiling*).
3. Landasan matematis dan literatur primer dari 6 parameter yang diuji serta justifikasi parameter yang dikunci.
4. Justifikasi pemilihan model CSDI (*Conditional Score-based Diffusion Models for Time Series*, NeurIPS 2021) sebagai pembanding eksternal 1:1 (*head-to-head*).
5. Rancangan tabel naskah Bab 3 dan panduan pembelaan sidang skripsi (*Defense Talking Points*).

Seluruh nomor referensi pada dokumen ini terikat secara konsisten dengan daftar pustaka naskah (`scratch/pdf_references.md`).

---

## 1. Rasional Metodologis: Mengapa Tepat 5 Skenario?

Penentuan 5 skenario penalaan hiperparameter memiliki landasan metodologis yang kokoh dalam riset *machine learning* dan meteorologi komputasional:

### A. Standar Sensitivitas Parameter dalam Literatur Terkemuka (Rentang 3–6 Konfigurasi)
Dalam literatur model difusi dan peramalan cuaca (*nowcasting*), pengujian sensitivitas parameter tidak dilakukan secara acak (*random grid search*), melainkan menggunakan rentang **3 hingga 6 titik konfigurasi bertingkat**:
1. **[27] Liu et al. (*RATD*, NeurIPS 2024, hal. 8–9, Tabel 3):** Melakukan studi ablasi terhadap parameter retrieval database dengan menguji **3 titik konfigurasi bertingkat** ($k \in \{1, 3, 5\}$).
2. **[25] Asperti et al. (*GED Diffusion*, 2024, hal. 10):** Menguji variasi langkah inferensi difusi presipitasi dalam **3 tingkatan diskret** (10, 15, dan 20 langkah).
3. **[16] Price et al. (*GenCast*, Nature, 2024, Extended Data):** Mengevaluasi skala anggota ensemble stokastik pada **4 tingkatan bertingkat** ($M \in \{10, 20, 42, 50\}$).
4. **[33] Rasp et al. (*WeatherBench*, 2020):** Standar pengujian benchmark data cuaca global merekomendasikan **3–5 rezim evaluasi** untuk mendemonstrasikan kestabilan model.

### B. Prinsip *5-Point Ordinal Sensitivity Scale* (Metodologi Eksperimen)
Secara metodologis, lima titik merupakan jumlah minimum yang optimal untuk memvalidasi kurva respons monotonik non-linear:
* **Titik 1 (Batas Bawah Ekstrem / Minimal Bound):** Menguji toleransi minimum parameter terhadap degradasi performa.
* **Titik 2 (Transisi Bawah / Lean Regime):** Menguji titik tolak peningkatan efisiensi sebelum mencapai konfigurasi standar.
* **Titik 3 (Median Kontrol / Baseline Control):** Titik tengah seimbang naskah skripsi (Tabel 3.16 & Sub-bab 3.7.4).
* **Titik 4 (Transisi Atas / Refined Regime):** Menguji peningkatan resolusi parameter dengan penalaan halus.
* **Titik 5 (Batas Atas Saturasi / Asymptotic Bound):** Menguji batas teoritis tertinggi (*theoretical ceiling*) untuk membuktikan ada/tidaknya fenomena *diminishing returns*.

### C. Pencegahan Ledakan Kombinatorik (*Combinatorial Explosion*)
Jika 6 parameter diuji dengan variasi penuh (*full factorial grid search* 5 level), total percobaan yang harus dilatih adalah:
$$\text{Total Model} = 5^6 = 15.625\text{ kombinasi}$$
Dengan waktu latih model spatio-temporal diffusion rata-rata 30–45 menit per model pada GPU lokal, pengujian kombinatorial penuh membutuhkan $>7.000$ jam komputasi (mustahil dalam batasan skripsi). Pendekatan 5 skenario bergradasi mengisolasi trajektori peningkatan kapasitas model secara efisien dan terarah.

---

## 2. Asal-Usul & Landasan Teori Penamaan Skenario 1–5

Penamaan skenario menggunakan prinsip **Operational Deployment Profiling** (Rezim Penempatan Operasional) yang berlandaskan pada teori perancangan Sistem Peringatan Dini Bencana (*Early Warning Systems* - EWS, merujuk **[3] Luciano et al., 2022**, **[4] Chavula et al., 2025**, dan **[5] Reichstein et al., Nature Reviews, 2025**):

| ID | Nama Profil | Landasan Teori Rezim Operasional | Karakteristik Komputasi & Mitigasi |
| :---: | :--- | :--- | :--- |
| **SKEN-1** | **Ultra-Lightweight** | **Edge / Resource-Constrained Regime:** Menguji batas terbawah kapabilitas model jika diimplementasikan pada perangkat pos pendakian (*edge device*) dengan daya listrik dan memori terbatas. | Latensi $<1$ detik; menguji apakah model tetap mampu mendeteksi hujan lebat orografis meski parameter ditekan ke ambang batas minimum. |
| **SKEN-2** | **Moderate-Fast** | **Fast-Response Transition Regime:** Menguji kompromi sampling langkah pendek berbasis akselerasi numerik DDIM (`[25]` Asperti et al.). | Latensi 1–2 detik; efisiensi tinggi untuk pembaharuan data berkala tanpa membebani GPU server web. |
| **SKEN-3** | **Default (Kontrol)** | **Balanced Operational Regime:** Nilai kontrol naskah skripsi (Tabel 3.16 & Sub-bab 3.7.4). Titik tengah teoritis antara biaya komputasi dan ketajaman representasi probabilitas. | Menjadi jangkar pembanding (*anchor baseline*) untuk mengukur deviasi akurasi dari skenario lainnya. |
| **SKEN-4** | **Fine-Tuned** | **High-Fidelity Server Regime:** Penalaan laju konvergensi halus pada manifold graf lereng gunung (`[26]` Yousaf et al.) dengan pengayaan konteks analog. | Peningkatan stabilitas loss; cocok untuk server analitik regional yang tidak membutuhkan respons sub-detik. |
| **SKEN-5** | **High-Capacity** | **Asymptotic / GenCast Benchmark Scale:** Menguji batas teoritis performa model generatif difusi merujuk pada standar benchmark cuaca global *Nature* (`[16]` Price et al., 2024). | Kapasitas stokastik penuh (50 ensemble, 50 step); membuktikan batas atas akurasi CRPS/CSI sebelum terjadi saturasi. |

---

## 3. Landasan Teori Kuat 6 Parameter yang Diuji

Keenam parameter ini dipilih karena merupakan **tuas pengendali fungsional (*active operational levers*)** dari 4 pilar arsitektur RDM-STGNN (Optimasi, Retrieval FAISS, Denoising Diffusion, dan Penanganan Data Kering):

### 1. Learning Rate ($\eta$)
* **Landasan Teori:** Teori Konvergensi Gradien pada Manifold Non-Euklidian (Lipschitz Smoothness).
* **Rasional Pengujian ($10^{-3} \to 5 \times 10^{-4} \to 10^{-4}$):**
  * Nilai $10^{-3}$ adalah default optimizer AdamW pada difusi deret waktu (**[27] Liu et al., RATD, 2024, hal. 14**).
  * Nilai $10^{-4}$ adalah nilai stabilisasi konvergensi Spatio-Temporal GNN pada peramalan presipitasi (**[26] Yousaf et al., WRF-GNN, 2025, hal. 5**).
* **Justifikasi Sidang:** *"Model RDM-STGNN menggabungkan dua dinamika: perambatan pesan graf lereng (GAT) dan rekonsiliasi derau difusi. Pengujian $10^{-3} \to 10^{-4}$ membuktikan apakah gradien pada layer graf lereng mengalami osilasi (overshooting) jika menggunakan laju standar $10^{-3}$."*

### 2. Epoch Maksimum & Early Stopping Patience
* **Landasan Teori:** Teori Generalization Bound dan Regularisasi Empiris.
* **Rasional Pengujian ($10(5) \to 20(12) \to 35(12) \to 50(15)$):**
  * `[25]` Asperti et al. (GED, 2024, hal. 10) menggunakan penalaan 10 epoch untuk menjaga generalisasi model nowcasting.
  * Naskah menetapkan default 20 epoch dengan patience 12 (`bab3.md:1001-1002`).
  * Nilai 50 epoch (patience 15) menguji batas saturasi kurva loss validasi.
* **Justifikasi Sidang:** *"Data hujan lereng gunung didominasi kondisi kering ($>70\%$). Epoch pendek (10–20) mencegah model menghafal sampel kering (overfitting), sementara 50 epoch membuktikan apakah model naskah mengalami underfitting atau sudah konvergen optimal."*

### 3. FAISS Neighbors ($k$)
* **Landasan Teori:** Teori Memory Density & Information Oversmoothing pada Representasi Riwayat.
* **Rasional Pengujian ($1 \to 2 \to 3 \to 4 \to 5$):**
  * Merujuk langsung pada studi ablasi basis data retrieval paper acuan utama **[27] Liu et al. (RATD, NeurIPS 2024, hal. 8–9, Tabel 3)** yang menguji $k \in \{1, 3, 5\}$.
* **Justifikasi Sidang:** *"Parameter $k$ mengatur bobot konteks analog masa lalu. Jika $k=1$, model rentan terhadap bias analog tunggal. Jika $k>5$, terjadi oversmoothing di mana rata-rata analog mengaburkan deviasi ekstrem hujan lokal. Variasi 1 hingga 5 mengisolasi titik densitas analog paling optimal."*

### 4. DDIM Sampling Steps ($T_{inf}$)
* **Landasan Teori:** Teori Diskretisasi Numerik Reverse Stochastic Differential Equations (SDE/ODE).
* **Rasional Pengujian ($10 \to 15 \to 20 \to 30 \to 50$):**
  * `[25]` Asperti et al. (2024, hal. 10) menetapkan sampling cepat pada 15 langkah.
  * Song et al. (*DDIM*, ICLR 2021) membuktikan trajektori non-Markovian DDIM mampu memangkas langkah dari 1000 ke rentang 10–50 langkah tanpa merusak distribusi sampel.
* **Justifikasi Sidang:** *"Langkah sampling mengendalikan galat diskretisasi lintasan pembersihan derau. Semakin tinggi step, semakin halus rekonstruksi intensitas hujan lebat, tetapi latensi meningkat secara linier $\mathcal{O}(T_{inf})$. Pengujian ini mencari titik potong terbaik antara latensi dashboard dan ketajaman sebaran."*

### 5. Ensemble Size ($M$)
* **Landasan Teori:** Teori Galat Sampling Monte Carlo yang menyusut sebesar $\mathcal{O}(1/\sqrt{M})$.
* **Rasional Pengujian ($10 \to 20 \to 30 \to 40 \to 50$):**
  * Naskah menetapkan default $M=30$ (`bab3.md:1016`) untuk membentuk rentang persentil ($P_{10}, P_{50}, P_{90}$).
  * Standar emas global **[16] Price et al. (GenCast, Nature, 2024, hal. 3)** menggunakan $M=50$ ensemble members.
* **Justifikasi Sidang:** *"Ketidakpastian prediksi kuantil stabil saat ukuran sampel mencukupi. Pengujian 10–50 sampel membuktikan apakah 30 anggota pada naskah sudah konvergen secara statistik pada metrik CRPS dan Spread-Skill Ratio, ataukah membutuhkan 50 anggota seperti GenCast."*

### 6. Bobot Auxiliary Loss ($\lambda_{aux}$)
* **Landasan Teori:** Multi-Task Gradient Balancing pada Data Presipitasi *Zero-Inflated*.
* **Rasional Pengujian ($0{,}3 \to 0{,}5 \to 0{,}7 \to 1{,}0$):**
  * Presipitasi pegunungan memiliki sifat *zero-inflated* di mana mayoritas jam bernilai $0\text{ mm/jam}$. Naskah menetapkan $\lambda_{aux} = 0{,}7$ (`bab3.md:1008`).
* **Justifikasi Sidang:** *"Tanpa bobot klasifikasi hujan yang tepat, gradien loss difusi didominasi oleh rekonstruksi kondisi tanpa hujan sehingga model enggan memprediksi hujan lebat. Rentang $0{,}3 \to 1{,}0$ menguji trade-off penekanan False Alarm Ratio (FAR) dan peningkatan Probability of Detection (POD)."*

---

## 4. Parameter yang Dikunci (Terkendali) dan Justifikasi Fisisnya

Untuk menjaga validitas komparasi (*controlled experiment*), parameter berikut **wajib dikunci** dan tidak diubah antarskenario:

1. **Lookback Window ($6$ jam):** Dikunci oleh dinamika fisis siklus diurnal konveksi lereng Gunung Gede (`bab3.md:1003`). Mengubah panjang riwayat akan merusak format tensor input antarmodel.
2. **Batch Size ($512$):** Dikunci oleh batasan saturasi memori VRAM GPU yang digunakan.
3. **Weight Decay ($10^{-4}$) & Gradient Clipping ($1{,}0$):** Konstanta regularisasi baku AdamW untuk mencegah ledakan gradien pada graf spatio-temporal.
4. **Conditioning Dropout ($0{,}15$):** Menjaga kapabilitas *classifier-free guidance* agar model difusi tidak runtuh menjadi model tanpa kondisi (*unconditional*).
5. **Seed ($1$):** Menjamin determinisme dan keterulangan (*reproducibility*) komparasi data (`bab3.md:1012`).

---

## 5. Matriks 5 Skenario Penalaan Hiperparameter RDM-STGNN

| ID Skenario | Profil Operasional | Learning Rate ($\eta$) | Epoch (Patience) | FAISS ($k$) | DDIM Steps | Ensemble ($M$) | Loss Aux ($\lambda_{aux}$) | Landasan Rujukan Utama | Target Pembuktian Ilmiah |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **SKEN-1** | Ultra-Lightweight | $1 \times 10^{-3}$ | 10 (5) | 1 | 10 | 10 | 0,3 | Asperti et al. [25], Liu et al. [27] | Batas bawah latensi inferensi realtime dashboard ($<1$ detik). |
| **SKEN-2** | Moderate-Fast | $1 \times 10^{-3}$ | 20 (8) | 2 | 15 | 20 | 0,5 | Asperti et al. [25] (GED Diffusion) | Efisiensi sampling langkah pendek (15 DDIM steps). |
| **SKEN-3** | **Default (Kontrol)** | **$1 \times 10^{-3}$** | **20 (12)** | **3** | **20** | **30** | **0,7** | **Naskah Skripsi Bevantyo (Tabel 3.16 & 3.7.4)** | **Baseline kontrol naskah; titik tengah akurasi vs biaya komputasi.** |
| **SKEN-4** | Fine-Tuned | $5 \times 10^{-4}$ | 35 (12) | 4 | 30 | 40 | 0,7 | Yousaf et al. [26], Liu et al. [27] | Stabilitas konvergensi dengan LR lebih halus dan retrieval analog menengah. |
| **SKEN-5** | High-Capacity | $1 \times 10^{-4}$ | 50 (15) | 5 | 50 | 50 | 1,0 | Price et al. [16] (*Nature*), Yousaf [26] | Batas atas akurasi stokastik maksimum (*GenCast scale* 50 ensemble). |

---

## 6. Landasan Pemilihan Model Pembanding CSDI (NeurIPS 2021)

### A. Alasan Menolak Pembanding Model Radar 2D (DGMR / NowcastNet / DiffCast):
Model generatif radar seperti **DGMR [6]** (*Nature 2021*) dan **NowcastNet [7]** (*Nature 2023*) dirancang khusus untuk memproses domain citra grid piksel 2D beresolusi tinggi ($256 \times 256$ piksel) menggunakan operasi konvolusi dan persamaan kontinuitas fluida. Data penelitian ini berbasis 5 stasiun sel diskret ERA5 pada lereng gunung. Memaksakan DGMR/NowcastNet mengharuskan interpolasi koordinat buatan menjadi citra semu, yang memunculkan artefak buatan dan merusak dinamika mikroklimat orografis lokal.

### B. Bukti CSDI Adalah 100% *Apple-to-Apple* (Head-to-Head):
Model **CSDI** (*Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation/Forecasting*, Yusuke Tashiro et al., **NeurIPS 2021**) merupakan standar emas pemodelan difusi deret waktu multivariat:
1. **Format Input Identik:** Mengolah tensor multivariat $[B, L, K]$ dengan panjang riwayat $L=6$ jam dan fitur multivariat $K = 5\text{ node} \times 9\text{ variabel} = 45\text{ kanal}$, tanpa interpolasi buatan.
2. **Paradigma Identik:** Sama-sama berbasis *Conditional Denoising Diffusion Probabilistic Models* (DDPM/DDIM) dengan estimasi skor derau bertingkat.
3. **Protokol Inferensi Identik:** Menghasilkan 30 anggota ensemble stokastik ke horizon $t+1$ jam di node target `MAIN`.
4. **Metrik Seragam:** Keduanya dapat diukur langsung menggunakan metrik CRPS, Brier Score, CSI, RMSE, dan Spread-Skill Ratio pada data uji yang sama persis.
5. **Kaitan Literatur Langsung:** Paper acuan utama skripsi ini, yaitu **[27] Liu et al. (RATD, NeurIPS 2024)**, secara eksplisit menggunakan CSDI sebagai baseline difusi utama di seluruh tabel evaluasinya (Tabel 1, 2, dan 4).

### C. Isolasi Kontribusi Ilmiah RDM-STGNN vs CSDI:
* **Keunggulan Graf Fisik vs Atensi Acak:** CSDI menggunakan *2D Dense Attention* (menganggap semua hubungan antarfitur bebas konteks spasial), sedangkan RDM-STGNN menggunakan *Star-Graph GAT* yang membatasi perambatan informasi sesuai hukum topografi lereng (Utara, Selatan, Barat, Timur menuju Puncak/MAIN).
* **Keunggulan Retrieval vs Gaussian Murni:** CSDI memulai proses sampling dari prior Gaussian baku $\mathcal{N}(0, \mathbf{I})$ sehingga rentan runtuh ke rata-rata pada kasus ekstrem (*regression to the mean*), sedangkan RDM-STGNN memanfaatkan analog cuaca ekstrem dari basis data FAISS untuk menjaga deviasi hujan lebat.

---

## 7. Rekomendasi Format Tabel Revisi Bab 3 (Tabel 3.18)

Bila penguji meminta model pembanding generatif sepadan di naskah, susun matriks pembanding pada Sub-bab 3.8.6 menjadi:

| Skenario | Model Pembanding | Paradigma Model | Representasi Spasial | Karakteristik Output | Sumber Acuan |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | Multi-Node LSTM | Recurrent Deep Learning | Concatenation (Tanpa Graf) | Deterministik (Titik) | Li et al. [29] |
| **2** | STGNN Deterministik | Spatio-Temporal Graph | Star-Graph GAT | Deterministik (Titik) | Yousaf et al. [26], Zhao et al. [28] |
| **3** | **CSDI (NeurIPS 2021)** | **Multivariate Diffusion Model** | **Dense Feature Attention** | **Probabilistik (30 Ensambel)** | **Tashiro et al. (2021) / Liu et al. [27]** |
| **4** | **RDM-STGNN (Diusulkan)** | **Retrieval-Augmented Diffusion** | **Star-Graph GAT + Top-3 Retrieval** | **Probabilistik (30 Ensambel)** | **Model Penelitian Ini** |
