# Sampel Dataset Penelitian Gede–Pangrango

Berikut adalah 3 baris pertama data asli (raw data) dari dataset utama (`data/raw/pangrango_era5_5node_2005_2025.parquet`). Kolom koordinat, alias, dan metadata lainnya telah dihapus untuk menyederhanakan visualisasi.

### Tabel Data Mentah (Raw Data - 3 Baris Pertama)

| Tanggal & Waktu (UTC) | Node | Suhu (°C) | Kelembapan (%) | Titik Embun (°C) | ... | Ketinggian (m) | **[Target 1] Curah Hujan** | **[Target 2] Kecepatan Angin** | **[Target 3] Kelembapan** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2004-12-31 17:00:00 | **MAIN** | 15.20 | 95.59 | 14.49 | ... | 1529.0 | **0.00** | **5.59** | **95.59** |
| 2004-12-31 17:00:00 | **UP** | 23.69 | 94.71 | 22.79 | ... | 162.0 | *(diabaikan)* | *(diabaikan)* | *(diabaikan)* |
| 2004-12-31 17:00:00 | **RIGHT** | 23.57 | 96.15 | 22.92 | ... | 288.0 | *(diabaikan)* | *(diabaikan)* | *(diabaikan)* |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## TL;DR Penjelasan Struktur & Peran Data

### 1. Peran Node (Spasial)
- **`MAIN` (Node Utama)**: Berperan sebagai pusat prediksi (Puncak Gunung Gede-Pangrango). Hanya node `MAIN` yang memiliki nilai **Target** yang akan diprediksi oleh model.
- **Node Sekitar (`UP`, `DOWN`, `LEFT`, `RIGHT`)**: Hanya digunakan sebagai **Fitur Input Spasial** untuk memberikan konteks kondisi cuaca di sekeliling wilayah target. Nilai target pada node sekitar diabaikan selama pelatihan (*main-node-only policy*).

### 2. Fitur Input (9 Fitur Utama)
Sembilan fitur masukan ($X$) digunakan untuk menangkap kondisi atmosfer pada 6 jam sebelumnya ($t-6$ s.d. $t-1$):
- **Suhu (`temperature_2m`)**: Suhu udara pada ketinggian 2 meter (°C).
- **Kelembapan (`relative_humidity_2m`)**: Kelembapan relatif udara pada ketinggian 2 meter (%).
- **Titik Embun (`dewpoint_2m`)**: Suhu titik embun pada ketinggian 2 meter (°C).
- **Tekanan Permukaan (`surface_pressure`)**: Tekanan udara di permukaan tanah (hPa).
- **Kecepatan Angin (`wind_speed_10m`)**: Kecepatan angin pada ketinggian 10 meter (m/s).
- **Arah Angin (`wind_direction_10m`)**: Arah hembusan angin dalam derajat kompas (0-360°).
- **Tutupan Awan (`cloud_cover`)**: Persentase langit yang tertutup awan (%).
- **Lag Curah Hujan (`precipitation_lag1`)**: Nilai curah hujan 1 jam sebelumnya untuk mendeteksi autokorelasi hujan (mm/jam).
- **Ketinggian (`elevation`)**: Ketinggian geografis node di atas permukaan laut (meter).

### 3. Variabel Target (3 Output)
Target prediksi ($Y$) berada di ujung kanan tabel, hanya dihitung untuk node **`MAIN`** pada jam yang diprediksi ($t$):
- **[Target 1] Curah Hujan (`precipitation`)**: Intensitas hujan satu jam ke depan (mm/jam).
- **[Target 2] Kecepatan Angin (`wind_speed_10m`)**: Kecepatan angin satu jam ke depan (m/s).
- **[Target 3] Kelembapan (`relative_humidity_2m`)**: Kelembapan relatif udara satu jam ke depan (%).

*Catatan: Pembagian target 3-output ini dinormalisasi selama proses training agar model diffusion belajar memprediksi pada distribusi skala yang stabil, kemudian dikembalikan ke satuan aslinya saat pengujian menggunakan denormalisasi.*
