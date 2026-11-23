# Sisipan Landasan Teori CSDI — Untuk Dimasukkan ke Skripsi

**Status:** bahan sisipan, bukan naskah final.
**Tujuan:** memberi AI lain instruksi dan teks siap tempel untuk menjelaskan mengapa CSDI memakai input 6 jam × 5 node × 10 variabel dan menargetkan 10 variabel per node, bukan 3.
**Prinsip:** tidak ada asumsi. Setiap klaim diberi sumber. Jika sumber hanya mendukung sebagian, batasnya ditulis.

---

## 0. Aturan untuk AI yang mengedit

1. Jangan mengubah angka hasil (RMSE, CRPS, POD, CSI).
2. Jangan mengarang sitasi. Gunakan referensi di §6.
3. Jangan menulis “CSDI hanya memprediksi 3 variabel”. Itu salah.
4. Jangan menulis “CSDI bisa input 50 kanal dan target 3 tanpa modifikasi”. Itu salah untuk forecasting.
5. Jangan menulis “CSDI NeurIPS 2021 Oral”. Status resminya **Poster**.
6. Jangan menulis “5 node × 10 variabel berasal dari paper CSDI”. Itu adaptasi data penelitian, bukan ketentuan paper.
7. Jangan mencampur 9 fitur dan 10 fitur. Gunakan **10 fitur per node** sesuai checkpoint dan adapter CSDI saat ini.
8. Jangan mengubah Tabel 4.13 atau klaim latency dalam tugas ini. Itu isu terpisah.

---

## 1. Inti yang harus dipahami

CSDI adalah model imputasi deret waktu multivariat. Ia menerima tensor:

```text
X ∈ R^{K × L}
K = jumlah fitur/kanal
L = panjang waktu
```

Pada penelitian ini:

```text
K = 5 node × 10 variabel = 50 kanal
L = 6 jam historis + 1 jam target = 7
```

Karena CSDI mendefinisikan forecasting sebagai imputasi **seluruh fitur** pada waktu mendatang, maka:

```text
Target diffusion = 50 kanal
```

Atau per node:

```text
Target diffusion = 10 variabel per node
```

Evaluasi kemudian hanya mengambil 3 kanal MAIN:

```text
precipitation, wind_speed, relative_humidity
```

Jadi:

> 50 kanal direkonstruksi, 3 kanal dinilai.

Bukan:

> 50 kanal input, 3 kanal target.

---

## 2. Kutipan sumber yang menjadi landasan

### 2.1 Definisi K fitur

Paper CSDI, §3.1:

> “We consider \(N\) multivariate time series with missing values. Let us denote the values of each time series as \(\mathbf{X}=\{x_{1:K,1:L}\}\in\mathbb{R}^{K\times L}\) where \(K\) is the number of features and \(L\) is the length of time series.”

Implikasi:
- CSDI memodelkan seluruh K fitur dalam satu tensor.
- Target dimension = K.
- Tidak ada pemisahan “K input, 3 target” di dalam diffusion.

### 2.2 Forecasting = imputasi semua fitur

Paper CSDI, §3.1:

> “This definition of imputation includes other related tasks, such as interpolation, which imputes all features at target time points, and forecasting, which imputes all features at future time points.”

Paper CSDI, §6.3:

> “We predict all features at future time steps using past time series.”

Implikasi:
- Forecasting CSDI bukan “prediksi sebagian fitur”.
- Seluruh fitur pada waktu mendatang dimask dan direkonstruksi.
- Karena itu targetnya 50 kanal, bukan 3.

### 2.3 2D attention memakai seluruh fitur

Paper CSDI, §3.2:

> “To capture temporal and feature dependencies of multivariate time series, we utilize a two dimensional attention mechanism … temporal Transformer layer … feature Transformer layer …”

Ablation paper (Table 7) menunjukkan:
- menghapus temporal attention → performa turun;
- menghapus feature attention → performa turun;
- 2D attention penuh → terbaik.

Implikasi:
- Memasukkan seluruh 10 variabel per node bukan pilihan sembarang.
- Feature attention memang dirancang untuk memanfaatkan hubungan antarfitur.
- Jika hanya 3 fitur yang dimasukkan, mekanisme feature attention kehilangan sebagian besar konteks.

### 2.4 Kode resmi CSDI

Kode resmi: https://github.com/ermongroup/CSDI

- `target_dim = K` → output diffusion memiliki K kanal.
- `observed_data` berbentuk `[batch, K, L]`.
- `impute()` mengembalikan seluruh K kanal.
- Forecasting memask nilai masa depan; model merekonstruksi seluruh kanal.

Kode adaptasi penelitian:
- `core/csdi_baseline/build_data.py` → `CH_PER_NODE = 9 + 1 = 10`; `N_CH = 5 × 10 = 50`.
- `core/csdi_baseline/train_csdi.py` → `target_mask[-PRED_LENGTH:] = 0.0` untuk seluruh kanal.
- `core/csdi_baseline/main_model.py` → `cond_mask = gt_mask`; `target_mask = observed_mask - cond_mask`.
- `core/csdi_baseline/evaluate_csdi.py` → hanya 3 kanal MAIN yang dihitung metriknya.

---

## 3. Mengapa target 10 per node, bukan 3?

Karena kalau hanya 3 yang dijadikan target, ada dua kemungkinan:

### Kemungkinan A — 7 variabel lain diberikan nilainya pada t+1

```text
Target    : 3 kanal MAIN
Diketahui : 7 kanal lain pada t+1
```

Ini **leakage** untuk nowcasting. Saat memprediksi t+1, nilai t+1 untuk 7 variabel lain belum diketahui. Model tidak boleh diberi nilai masa depan.

### Kemungkinan B — 7 variabel lain tetap tidak diketahui

```text
Target : 50 kanal
```

Model harus merekonstruksi semuanya. Ini yang dilakukan CSDI.

### Kemungkinan C — 50 kanal hanya sebagai konteks, diffusion 3 target

```text
Input  : 6 jam × 5 node × 10 variabel
Target : 3 kanal MAIN
```

Ini **bukan CSDI standar**. CSDI tidak punya cabang encoder terpisah untuk 50 kanal konteks lalu diffusion 3 target. Ini desain RDM: STGNN mengolah konteks, diffusion hanya menebak 3 target.

Kesimpulan:

> Target 10 per node adalah konsekuensi dari definisi forecasting CSDI yang mengimputasi seluruh fitur. Target 3 hanya mungkin jika 7 fitur lain diketahui pada t+1 (leakage) atau jika arsitektur diubah menjadi RDM-like.

---

## 4. Teks siap tempel untuk BAB II

Letakkan setelah penjelasan CSDI di §2.2.3 atau §2.2.6.

> CSDI mendefinisikan deret waktu multivariat sebagai \(\mathbf{X}\in\mathbb{R}^{K\times L}\), dengan \(K\) sebagai jumlah fitur dan \(L\) sebagai panjang waktu [33]. Dalam paper aslinya, Tashiro et al. (2021) menyatakan bahwa forecasting termasuk imputasi seluruh fitur pada waktu mendatang: “forecasting, which imputes all features at future time points” [33]. Oleh karena itu, seluruh kanal pada timestep target direkonstruksi, bukan hanya sebagian fitur.
>
> Pada penelitian ini, data disusun sebagai lima node pengamatan dan sepuluh variabel per node, sehingga \(K=5\times10=50\) kanal. Sepuluh variabel tersebut terdiri atas sembilan fitur cuaca (\(temperature\), \(relative\_humidity\), \(dewpoint\), \(surface\_pressure\), \(wind\_speed\), \(wind\_direction\), \(cloud\_cover\), \(precipitation\_lag1\), \(elevation\)) dan satu kanal curah hujan (\(precipitation\)). Dengan demikian, target diffusion CSDI adalah 50 kanal, atau 10 variabel per node. Evaluasi kemudian mengambil tiga kanal pada node MAIN, yaitu curah hujan, kecepatan angin, dan kelembapan relatif.
>
> Pemilihan seluruh sepuluh variabel sebagai target bukan pilihan arbitrer. CSDI menggunakan mekanisme two-dimensional attention yang terdiri atas temporal attention dan feature attention [33]. Feature attention mempelajari ketergantungan antarfitur; ablasi pada paper asli menunjukkan bahwa menghapus feature attention menurunkan performa imputasi [33]. Dengan mempertahankan seluruh sepuluh variabel dalam tensor, mekanisme tersebut dapat memanfaatkan hubungan antarvariabel dan antarlokasi. Sebaliknya, jika hanya tiga variabel yang dijadikan target, tujuh variabel lainnya pada \(t+1\) harus diketahui terlebih dahulu; kondisi itu tidak tersedia pada nowcasting dan akan menimbulkan kebocoran informasi masa depan.

---

## 5. Teks siap tempel untuk BAB III

Letakkan di §3.7.2 atau bagian integrasi CSDI.

> Pada implementasi CSDI, tensor masukan disusun dengan dimensi \(K=50\) dan \(L=7\). Dimensi \(K\) berasal dari lima node kali sepuluh variabel per node, sedangkan \(L\) terdiri atas enam jam historis \((t-6,\dots,t-1)\) dan satu jam target \((t+1)\). Nilai \(precipitation\) ditransformasi dengan \(\log(1+x)\) sebelum dinormalisasi, mengikuti perlakuan target pada RDM-STGNN. Pada tahap forecasting, seluruh kanal pada timestep target dimask, sehingga model merekonstruksi 50 kanal. Evaluasi metrik hanya dilakukan pada tiga kanal MAIN: \(precipitation\), \(wind\_speed\), dan \(relative\_humidity\). Dengan demikian, jumlah target diffusion adalah 50 kanal, bukan tiga kanal.

---

## 6. Tabel pembeda yang bisa dimasukkan

### Tabel A — Dimensi data CSDI dan RDM

| Aspek | CSDI | RDM-STGNN |
|---|---|---|
| Input | 6 jam × 5 node × 10 variabel | 6 jam × 5 node × 10 variabel |
| Representasi | 50 kanal datar `[K=50, L=7]` | Graf 5 node, 6 snapshot |
| Target diffusion | 50 kanal | 3 kanal MAIN |
| Kanal yang dinilai | 3 kanal MAIN | 3 kanal MAIN |
| Struktur topologi | Tidak ada; feature attention | Ada; Star-Graph GAT |
| Retrieval | Tidak ada | FAISS, k=3 |

### Tabel B — Jumlah target

| Model | Target diffusion | Target evaluasi |
|---|---:|---:|
| CSDI | 50 kanal (5 node × 10 variabel) | 3 kanal MAIN |
| RDM-STGNN | 3 kanal MAIN | 3 kanal MAIN |

Catatan tabel:
- “50 kanal” bukan berarti 50 metrik. Hanya 3 yang dinilai.
- “3 kanal” RDM adalah target diffusion; 5 node tetap menjadi konteks input.

---

## 7. Batas klaim yang harus ditulis

1. Paper CSDI **tidak** menetapkan “5 node × 10 variabel”. Itu desain data penelitian.
2. Paper CSDI hanya menetapkan bahwa forecasting mengimputasi seluruh \(K\) fitur.
3. Jika penelitian memakai \(K=50\), maka targetnya 50 kanal.
4. Jika ingin target 3 kanal tanpa leakage, itu bukan CSDI standar; itu RDM atau CSDI yang dimodifikasi.
5. Jangan menulis “CSDI lebih unggul karena menebak 50 kanal”. Itu hipotesis, bukan temuan paper.
6. Jangan menulis “CSDI NeurIPS 2021 Oral”. Status resminya **Poster**.

---

## 8. Referensi

1. **Tashiro, Y., Song, J., Song, Y., & Ermon, S. (2021).** *CSDI: Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation.* NeurIPS 2021.
   - arXiv: https://arxiv.org/abs/2107.03502
   - Prosiding: https://proceedings.neurips.cc/paper_files/paper/2021/hash/cfe8504bda37b575c70ee1a8276f3486-Abstract.html
   - Kutipan kunci: §3.1 (definisi \(K\) fitur; forecasting mengimputasi seluruh fitur), §6.3 (“We predict all features at future time steps using past time series”), §3.2 dan Table 7 (2D attention dan ablation).

2. **Kode resmi CSDI.** https://github.com/ermongroup/CSDI
   - `target_dim = K`; `observed_data` `[B, K, L]`; `impute()` mengembalikan seluruh K kanal.

3. **Kode adaptasi penelitian.**
   - `core/csdi_baseline/build_data.py`
   - `core/csdi_baseline/train_csdi.py`
   - `core/csdi_baseline/main_model.py`
   - `core/csdi_baseline/evaluate_csdi.py`

---

## 9. Checklist setelah sisipan

- [ ] Tabel 2.3 memakai 10 variabel per node, bukan 9.
- [ ] §3.6.1 menyebut 10 fitur, termasuk `precipitation`.
- [ ] §3.7.2 menyebut \(K=50\), \(L=7\).
- [ ] §4.4.2 menyebut target diffusion 50 kanal.
- [ ] §4.6 menyebut evaluasi hanya 3 kanal MAIN.
- [ ] Tidak ada kalimat “CSDI hanya menebak 3 variabel”.
- [ ] Tidak ada kalimat “50 kanal input, 3 kanal target” tanpa penjelasan leakage.
- [ ] Tidak ada klaim “NeurIPS Oral”.
- [ ] Sitasi [33] dan URL paper tercantum.
