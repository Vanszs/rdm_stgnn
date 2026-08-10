# Arsip Tabel Bab 2

## Tabel 2.3 Perbandingan Keluaran Deterministik dan Probabilistik pada Nowcasting [4], [16], [27]

| Aspek | Pendekatan Deterministik | Pendekatan Probabilistik |
|---|---|---|
| Keluaran | Satu prediksi titik untuk setiap waktu dan lokasi. | Ensemble atau distribusi beberapa prediksi yang mungkin. |
| Ketidakpastian | Tidak dinyatakan secara eksplisit. | Direpresentasikan melalui sebaran antar anggota ensemble. |
| Kegunaan | Menilai nilai prakiraan tunggal. | Mendukung keputusan berbasis peluang dan tingkat risiko. |
| Metrik utama | MAE, RMSE, korelasi. | CRPS, Brier Score, reliability diagram, serta metrik deterministik. |
| Keterbatasan | Cenderung meratakan nilai pada kondisi tidak pasti. | Memerlukan evaluasi kalibrasi dan biaya sampling lebih tinggi. |

## Tabel 2.4 Definisi Node pada Representasi Graf Lima Node [11], [14], [35]

| Node | Posisi Relatif terhadap MAIN | Fungsi dalam Model | Koneksi Graf |
|---|---|---|---|
| MAIN | Titik prediksi utama. | Menyediakan target curah hujan, kecepatan angin, dan kelembapan relatif pada node `MAIN`. | Terhubung dua arah dengan UP, DOWN, LEFT, RIGHT. |
| UP | Utara dari MAIN. | Menyediakan konteks kondisi atmosfer dari arah utara. | Terhubung dua arah dengan MAIN |
| DOWN | Selatan dari MAIN. | Menyediakan konteks kondisi atmosfer dari arah selatan. | Terhubung dua arah dengan MAIN |
| LEFT | Barat dari MAIN. | Menyediakan konteks kondisi atmosfer dari arah barat. | Terhubung dua arah dengan MAIN |
| RIGHT | Timur dari MAIN. | Menyediakan konteks kondisi atmosfer dari arah timur. | Terhubung dua arah dengan MAIN |
