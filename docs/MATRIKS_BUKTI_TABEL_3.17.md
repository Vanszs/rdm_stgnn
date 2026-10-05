# Matriks Bukti Literatur — Tabel 3.17 Skenario Pengujian Parameter Pelatihan RDM

Dokumen ini melaporkan **bukti literature per nilai sel** Tabel 3.17 naskah (`bepan Revisi (1).pdf`, hal. cetak 68–69).
Disusun tanpa asumsi: setiap klaim disertai rujukan halaman paper asli. **Selisih yang tidak punya sumber ditandai jujur sebagai `TIDAK ADA SUMBER`.**

Screenshot bukti per parameter tersimpan di `docs/bukti_highlight/`:
`learning_rate.png`, `epoch_patience.png`, `k_faiss.png`, `langkah_ddim.png`, `ensemble.png`, `bobot_auxiliary.png`.
File PDF referensi di `Refrensi Urut/` sudah diblok kuning pada baris bukti terkait.

---

## 1. Learning Rate (η) — Skenario 1–5: `1e-3`, `1e-3`, `1e-3`, `5e-4`, `1e-4`

| Nilai | Ada Sumber? | Bukti (halaman paper asli) |
| :---: | :---: | :--- |
| **1e-3** | **YA** | **[16] Liu et al., RATD (NeurIPS 2024) hal. 14** — *"with an initial learning rate of 10⁻³, betas = (0.95, 0.999)"*<br>**[21] Zhang et al. hal. 6** — *"The initial learning rate of the model was set to 0.001"*<br>**[2] Zhang et al., NowcastNet (Nature 2023) hal. 8** — *"initial learning rate of 1 × 10⁻³"* |
| **5e-4** | **TIDAK ADA SUMBER** | Tidak ada paper dalam Daftar Pustaka naskah yang memakai 5×10⁻⁴. Nilai terdekat: **[10] Zhong et al., FuXi-ENS hal. 11** — *"an initial learning rate of 2.5 × 10⁻⁴"*. Nilai 5e-4 adalah **interpolasi desain naskah** antara 1e-3 dan 1e-4. |
| **1e-4** | **YA** | **[11] Asperti et al., GED (2024) hal. 10** — *"a learning rate of 1e-04 and weight decay of 1e-05"*<br>**[12] Yousaf et al., WRF-GNN (2025) hal. 5** — *"a learning rate of 0.0001 for a total of 2000 epochs"*<br>**[13] Zhao et al. (2023) hal. 3** — *"the initial learning rate 1e-4 and weight decay 1e-5"* |

---

## 2. Epoch (Patience) — `10(5)`, `20(8)`, `20(12)`, `35(12)`, `50(15)`

| Nilai | Ada Sumber? | Bukti (halaman paper asli) |
| :---: | :---: | :--- |
| **Epoch 10** | **YA** | **[11] Asperti et al., GED (2024) hal. 10** — *"a fine-tuning phase of 10 epochs using a learning rate of 1e-05"* |
| **Epoch 15 & 20** | **YA** | **[13] Zhao et al. (2023) hal. 3** — *"The number of training epochs is 15 for GCN and 20 for ConvLSTM."* |
| **Patience (konsep)** | **YA (konsep)** | **[21] Zhang et al. hal. 6** — *"an early stopping strategy was applied... if the validation loss showed no improvement over the past 10 epochs"* dan *"reduced to 90%... if the validation loss did not decrease for 3 consecutive epochs"*<br>**[16] RATD hal. 14** — *"early stopping was applied for a maximum of 200 epochs"* |
| **Epoch 35 & 50** | **TIDAK ADA SUMBER** | Tidak ada paper yang memakai 35 atau 50 epoch pada tugas ini. **[21] Zhang hal. 7** memakai *"Maximum Iterations 100"*; **[16] RATD** memakai batas 200 epoch. |
| **Patience 5, 8, 12, 15** | **TIDAK ADA SUMBER** | Angka spesifik ini tidak muncul di paper mana pun. Paper hanya memberi praktik *early stopping* dengan nilai berbeda (3 dan 10 pada **[21]**; 200 pada **[16]**; 100 pada **[28] Veličković, GAT hal. 7**). |

**Catatan kejujuran:** gradasi patience `5 → 8 → 12 → 15` adalah **rancangan naskah sendiri**, bukan kutipan.

---

## 3. k (FAISS Neighbors) — `1`, `2`, `3`, `4`, `5`

| Nilai | Ada Sumber? | Bukti (halaman paper asli) |
| :---: | :---: | :--- |
| **k = 1, 3, 5** | **YA** | **[16] Liu et al., RATD (NeurIPS 2024) hal. 8** — *"We conducted an ablation study on two variables, n and k, to investigate the influence of the retrieval database Dᴿ in RATD"*<br>**[16] hal. 9, Tabel 3** — baris ablasi `k=1`, `k=3`, `k=5`; **Gambar 5** legenda `k=1 / k=3 / k=5`<br>**[16] hal. 9** — *"the settings of n and k are 256 and 3, respectively"* |
| **k = 2, 4** | **TIDAK ADA SUMBER** | Paper RATD hanya menguji `{1, 3, 5}`. Nilai 2 dan 4 adalah **interpolasi desain naskah**, bukan titik yang pernah diuji literatur. |

---

## 4. Langkah DDIM — `10`, `15`, `20`, `30`, `50`

| Nilai | Ada Sumber? | Bukti (halaman paper asli) |
| :---: | :---: | :--- |
| **15** | **YA** | **[11] Asperti et al., GED (2024) hal. 10** — *"The number of diffusion steps was fixed at 15"* |
| **100 (langkah latih T)** | **YA** | **[16] Liu et al., RATD hal. 14** — *"The diffusion steps T were set to 100."* |
| **10, 20, 30, 50 (langkah inferensi)** | **TIDAK ADA SUMBER** | Tidak ada paper dalam Daftar Pustaka yang menyapu langkah DDIM inferensi pada nilai-nilai ini. **[24] Ho et al., DDPM hal. 15** menyapu *training steps* (1000→875→750...), bukan langkah DDIM inferensi. |

**Catatan:** nilai `20` pada Skenario 3 memang dipakai naskah sebagai protokol evaluasi (Tabel 3.16/3.8.3), tetapi **bukan kutipan literatur**.

---

## 5. Ensemble (M) — `10`, `20`, `30`, `40`, `50`

| Nilai | Ada Sumber? | Bukti (halaman paper asli) |
| :---: | :---: | :--- |
| **20** | **YA** | **[1] Ravuri et al., DGMR (Nature 2021) hal. 4** — *"We use 20 member ensembles and show three accumulation levels used for weather warnings"* |
| **50** | **YA** | **[8] Price et al., GenCast (Nature 2025) hal. 3** — *"ENS contains 50 perturbed ensemble members, so we used 50-member GenCast ensembles to perform all evaluations"* |
| **10, 30, 40** | **TIDAK ADA SUMBER** | Tidak ada paper yang memakai 10/30/40 anggota ensemble untuk tugas ini. **Nilai 30 adalah protokol evaluasi naskah sendiri** (Sub-bab 3.8.3), bukan kutipan. |

---

## 6. Bobot Auxiliary (λaux) — `0,3`, `0,5`, `0,7`, `0,7`, `1,0`

**Hasil pencarian menyeluruh atas 49 PDF referensi:** pola `pos_weight`, `class weight`, `weighted loss`, `focal loss`, `BCEWithLogits`, `binary cross`, dan `weighted noise loss` → **0 hit. Tidak ada satu pun.**

| Aspek | Ada Sumber? | Bukti (halaman paper asli) |
| :--- | :---: | :--- |
| **Nilai λaux (0,3 / 0,5 / 0,7 / 1,0)** | **TIDAK ADA SUMBER** | **0 dari 49 paper.** Seluruh kolom λaux pada Tabel 3.17 berasal dari arsitektur naskah sendiri (Bab 3.7.2 komponen no. 24: `L_total = L_noise + 0,7 L_wet`). Gradasi 0,3→1,0 adalah rancangan hyperparameter naskah. |
| **Mekanisme classifier di dalam diffusion** | **YA (mekanisme berbeda)** | **[11] Asperti et al., GED (2024) hal. 5** — *"one based on an auxiliary classifier (similar, in spirit, to AC-GANs), and a second one that is classifier-free"*. **Perhatian:** ini adalah **classifier guidance** (classifier memandu proses sampling), **bukan** penjumlahan bobot loss. Mekanismenya berbeda dari λaux naskah. |
| **Rasional data hujan tidak seimbang** | **YA (alasan, bukan nilai)** | **[1] Ravuri et al., DGMR (Nature 2021) hal. 7** — *"approximately 89% of grid cells contain no rain... Medium to heavy precipitation comprises fewer than 0.4% of grid cells in the dataset. To account for this imbalanced distribution, the dataset is rebalanced"*. **Perhatian:** angka **0,4%** di sini adalah **persentase sel grid berhujan lebat** (statistik ketidakseimbangan data), **bukan** nilai λaux = 0,4. DGMR menangani ketidakseimbangan dengan **rebalancing dataset**, bukan dengan bobot auxiliary loss. |

### Klarifikasi penting (mencegah salah kutip)
* Angka **`0,4%`** pada DGMR **bukan** bobot λaux. Itu proporsi grid berhujan lebat → dipakai sebagai **alasan mengapa** penanganan data tidak seimbang diperlukan.
* **`auxiliary classifier`** pada GED **bukan** λaux. Itu teknik *classifier guidance* untuk sampling difusi, bukan pembobotan loss.
* Karena itu, **tidak ada satu pun sel λaux pada Tabel 3.17 yang dapat dikutip dari Daftar Pustaka naskah saat ini.**

---

## 6b. Hasil Pencarian Internet: Apakah Ada Paper yang Benar-benar Memakainya?

Pencarian dilakukan di **arXiv API** (bukan ringkasan AI) dan diverifikasi dengan membaca teks lengkap paper.

### TEMUAN UTAMA — MZ-Rain (paling cocok, 1:1 dengan desain naskah)

**Y. Zhang, S. Xiong, H. Wang, dkk., "MZ-Rain: Moisture-Budget-Guided Zero-Inflated Model for Station-Level Precipitation Nowcasting," arXiv:2609.04864, 4 Sep 2026.**
<https://arxiv.org/abs/2609.04864>

Paper ini **hampir identik** dengan desain λaux naskah — station-level (bukan grid), zero-inflated, memakai **auxiliary task klasifikasi hujan/tidak hujan**:

| Aspek | MZ-Rain (arXiv:2609.04864) | Naskah Bevantyo |
| :--- | :--- | :--- |
| Domain | Station-level precipitation nowcasting | Node MAIN (station-level) |
| Masalah | Severe zero inflation | Zero-inflated precipitation |
| Mekanisme | Auxiliary rainfall-occurrence task + BCE | Auxiliary wet head + `BCEWithLogitsLoss` |
| Ambang kering/basah | **δ = 0,1 mm/jam** | **0,1 mm/jam** (sama persis) |
| Persamaan loss | `L = L_MSE + β·L_MAE + α·L_Tw + α·L_BCE` | `L_total = L_noise + 0,7·L_wet` |
| Bobot auxiliary | **α = 0,1** dan **β = 0,3** | λaux = 0,3 … 1,0 |

**Kutipan verbatim (hal. Section IV-E Training Objective):**
> *"We jointly optimize wet-dry occurrence discrimination, Tweedie-inspired quantitative precipitation modeling, and point-wise regression... the overall objective is defined as ℒ = ℒ_MSE + βℒ_MAE + αℒ_Tw + αℒ_BCE (29)... Here, δ = 0.1 mm/h defines the dry-wet threshold, ϵ = 10⁻⁶ ensures numerical stability, and **α = 0.1 and β = 0.3 are loss balancing coefficients**."*

**Bukti ablasi bahwa task auxiliary benar-benar membantu (Tabel X paper):**

| Varian | Brier ↓ | CSI ↑ | FAR ↓ | MAE ↓ |
| :--- | :---: | :---: | :---: | :---: |
| Full (`q` + BCE) | 0,086 | **0,3243** | **0,5895** | 0,2841 |
| Tanpa task occurrence | N/A | 0,3116 | 0,6052 | 0,2889 |

### Temuan pendukung lain

| Paper | Relevansi | Nilai bobot? |
| :--- | :--- | :--- |
| **Rahimi et al., "Global Precipitation Nowcasting of IMERG: A U-Net ConvLSTM Architecture," arXiv:2307.10843 (2023)** | Secara eksplisit mempelajari *"the impacts of different training loss functions, including the mean-squared error (regression) and the **focal-loss (classification)**"* untuk nowcasting presipitasi | Tidak menyebut λ numerik di abstrak |
| **MTLDM, "Extreme Precipitation Nowcasting using Multi-Task Latent Diffusion Models," arXiv:2410.14103 (2024)** | Multi-task + latent diffusion untuk presipitasi ekstrem; mengatasi *"imbalanced data distribution"* | Loss autoencoder `L = L_SSIM + L_KL + L_LPIPS + L_‖x−x′‖` — multi-task decoder, bukan bobot BCE |
| **ZIDF, "From Noise to Precision: A Diffusion-Driven Approach to Zero-Inflated Precipitation Prediction," arXiv:2509.10501 (2025)** | Difusi + zero-inflated precipitation (Tweedie + DDPM) | Loss DDPM standar (VLB), tanpa bobot aux klasifikasi |
| **PreDiff (Gao et al., NeurIPS 2023), arXiv:2307.10422** | Difusi laten untuk nowcasting presipitasi | `λ_𝓕` = *guidance scale* untuk knowledge alignment fisika — **bukan** bobot klasifikasi |

### Kesimpulan pencarian internet (jujur)

1. **YA — ada paper yang memakai bobot auxiliary klasifikasi hujan.** Yang paling langsung: **MZ-Rain (arXiv:2609.04864, 2026)** dengan **α = 0,1** dan ambang **δ = 0,1 mm/jam** — ambangnya **sama persis** dengan naskah.
2. **TETAPI:** nilai **λaux = 0,7 pada naskah TIDAK berasal dari paper mana pun.** MZ-Rain memakai α = 0,1 (dan β = 0,3 untuk MAE). Jadi λaux = 0,7 tetap **desain naskah sendiri**.
3. **Rekomendasi kuat:** tambahkan **MZ-Rain (arXiv:2609.04864)** ke Daftar Pustaka naskah sebagai landasan cabang auxiliary. Dengan begitu kolom λaux punya pijakan nyata: nilainya diuji pada rentang 0,1 (MZ-Rain) hingga 1,0, dan naskah menguji 0,3–1,0 termasuk titik 0,3.
4. **Catatan kejujuran yang harus diucapkan:** *"Bobot λaux kami uji pada rentang 0,3–1,0; literatur terdekat (MZ-Rain) memakai α = 0,1 dengan ambang δ = 0,1 mm/jam yang sama. Rentang ini kami pilih untuk menguji sensitivitas, bukan mengklaim nilai dari literatur."*

### Bukti visual untuk sidang

PDF MZ-Rain sudah disimpan di koleksi referensi (**sudah diblok kuning**) dan buktinya sudah masuk ke screenshot parameter:

| Berkas | Isi bukti MZ-Rain |
| :--- | :--- |
| `Refrensi Urut/[49] MZ-Rain ... (arXiv 2609.04864).pdf` | PDF asli; diblok kuning pada abstrak, persamaan loss (α=0,1; β=0,3; δ=0,1 mm/jam), dan Tabel X |
| `docs/bukti_highlight/bobot_auxiliary.png` | **4 bukti**: MZ-Rain hal. 8 (bobot α/β), MZ-Rain hal. 14 (Tabel X ablasi), GED hal. 5 (auxiliary classifier), DGMR hal. 7 (data tidak seimbang) |

---

## Ringkasan Kejujuran (siap dijawab ke penguji)

**Yang punya sumber langsung (bisa dikutip):**
1. Learning rate: `1e-3` ([16], [21], [2]) dan `1e-4` ([11], [12], [13]).
2. Epoch: `10` ([11]) dan `15/20` ([13]).
3. Praktik *early stopping* ([21], [16], [28]) — nilai patience berbeda-beda antarpaper.
4. `k ∈ {1, 3, 5}` dan setting optimal `k=3` ([16], Tabel 3 + Gambar 5).
5. Langkah difusi `15` ([11]) dan `T=100` ([16]).
6. Ensemble `20` ([1]) dan `50` ([8]).
7. **Alasan** data tidak seimbang: hujan lebat `< 0,4%` grid ([1]); konsep classifier di dalam difusi ([11]) — namun keduanya **bukan** nilai λaux.

**Yang TIDAK punya sumber langsung (harus dinyatakan sebagai desain naskah):**
1. Learning rate `5e-4` (interpolasi antara 1e-3 dan 1e-4).
2. Epoch `35` dan `50`; nilai patience `5`, `8`, `12`, `15`.
3. `k = 2` dan `k = 4` (RATD hanya menguji 1/3/5).
4. Langkah DDIM `10`, `20`, `30`, `50` untuk inferensi.
5. Ensemble `10`, `30`, `40`.
6. **Seluruh nilai λaux `0,3` / `0,5` / `0,7` / `1,0`** — 0 dari 49 paper referensi memakai bobot auxiliary/kalsifikasi (pencarian `pos_weight`, `class weight`, `focal loss`, `BCEWithLogits`, `weighted loss` = 0 hit).

**Rumusan jawaban sidang yang benar (tanpa asumsi):**
> *"Tabel 3.17 dirancang sebagai sapuan gradasi antara batas bawah dan batas atas yang berjangkar pada literatur. Jangkar yang dikutip adalah: LR 10⁻³ ([16],[21]) dan 10⁻⁴ ([11],[12],[13]); epoch 10 ([11]) dan 15–20 ([13]); k ∈ {1,3,5} dengan optimum k=3 ([16]); langkah difusi 15 ([11]); ensemble 20 ([1]) dan 50 ([8]). Nilai antara seperti 5×10⁻⁴, k=2, k=4, DDIM 10/30/50, dan gradasi λaux 0,3–1,0 adalah interpolasi yang kami rancang sendiri untuk menguji sensitivitas, bukan klaim kutipan. Jika penguji meminta seluruh sel harus bersumber, maka skenario perlu dipangkas menjadi nilai jangkar yang benar-benar terbit, atau ditambahkan referensi baru yang menguji nilai antara tersebut."*

---

## Berkas Terkait

| Berkas | Isi |
| :--- | :--- |
| `scratch/highlight_referensi.py` | Penanda kuning pada PDF referensi (idempoten, restore dari `.bak`) |
| `scratch/verify_highlight_referensi.py` | Verifikasi independen: baca ulang teks di bawah tiap highlight + penjaga cakupan (CSDI tidak boleh ter-highlight) |
| `scratch/compose_bukti_parameter.py` | Penyusun PNG bukti per parameter |
| `scratch/audit_tabel317_evidence.py`, `scratch/audit_tabel317_gaps.py` | Audit pencarian bukti di seluruh PDF referensi |
| `Refrensi Urut/*.pdf.bak` | Salinan bersih sebelum highlight (untuk rollback) |
