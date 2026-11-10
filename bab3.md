# BAB III
# METODE PENELITIAN

## 3.1 Studi Literatur

Studi literatur dilakukan untuk membangun dasar metodologis penelitian dan menentukan metode yang sesuai dengan tujuan *nowcasting* probabilistik cuaca. Literatur yang dikaji meliputi konsep *nowcasting*, dinamika hujan orografis, model generatif berbasis *diffusion*, pencarian analog historis, representasi graf spasio-temporal, serta metrik evaluasi prediksi cuaca.

Proses studi literatur meliputi identifikasi sumber, seleksi berdasarkan kesesuaian topik, pembacaan metode dan hasil, serta sintesis kelebihan dan keterbatasan penelitian terdahulu. Hasil kajian digunakan untuk menyusun rancangan model, menentukan variabel prediksi, memilih bentuk representasi data, dan menetapkan metode evaluasi.

Sintesis literatur tersebut menjadi landasan perancangan alur penelitian terpadu yang dirangkum pada Gambar 3.1, dengan rincian tahapan yang dijabarkan pada subbab-subbab berikutnya.

![Gambar 3.1 — Alur tahapan penelitian](bab3_media/gambar-3-1-alur-penelitian.jpeg)

**Gambar 3.1 Alur Tahapan Penelitian**
*Sumber: rancangan penelitian.*

Gambar 3.1 menunjukkan urutan penelitian dari studi literatur, pengambilan data, preprocessing, pembagian dataset, pembentukan fitur dan graf, perancangan arsitektur model, pelatihan, evaluasi, hingga rancangan visualisasi web. Seluruh tahapan penelitian dijalankan secara sistematis dan terintegrasi.

## 3.2 Pengambilan Data

Penelitian ini menggunakan data sekunder berupa deret waktu meteorologis yang diperoleh melalui Open-Meteo Archive API berbasis reanalisis ERA5. Data ERA5 digunakan untuk pelatihan dan evaluasi metodologis, bukan sebagai pengamatan lapangan atau sumber data real-time.

Lima titik grid ERA5 digunakan untuk merepresentasikan kawasan penelitian. Kelima node tersebut adalah `MAIN`, `UP`, `DOWN`, `LEFT`, dan `RIGHT`. Node `MAIN` menjadi sumber target prediksi, sedangkan empat node lainnya menyediakan konteks spasial.

Alur pengambilan data ditunjukkan pada Gambar 3.2. Gambar ini menjadi gambaran umum proses, sedangkan setiap langkahnya dijelaskan secara berurutan pada Subbab 3.2.1 sampai 3.2.6.

![Gambar 3.2 — Alur pengambilan data reanalisis ERA5](bab3_media/gambar-3-2-pengambilan-data.png)

**Gambar 3.2 Alur Pengambilan Data Reanalisis ERA5 melalui Open-Meteo API**
*Sumber: rancangan penelitian.*

Gambar 3.2 dibaca dari kiri ke kanan pada baris pertama, kemudian dilanjutkan ke bawah dan ke kiri pada baris kedua. Alurnya dimulai dari penentuan koordinat node, dilanjutkan dengan permintaan data melalui Open-Meteo API, penerimaan data ERA5, validasi grid, penggabungan lima node, dan pembentukan dataset penelitian. Transformasi fitur, pembagian dataset, serta pembentukan model tidak termasuk dalam gambar ini.

### 3.2.1 Penentuan Node dan Koordinat

Koordinat node ditentukan sebelum permintaan data dikirimkan ke Open-Meteo API. Susunan node mengikuti urutan tetap `[MAIN, UP, DOWN, LEFT, RIGHT]`. Koordinat yang digunakan ditunjukkan pada Tabel 3.1.

**Tabel 3.1 Koordinat dan Peran Node**

| Node | Latitude | Longitude | Peran |
|---|---:|---:|---|
| `MAIN` | -6.75 | 107.00 | Target prediksi |
| `UP` | -6.50 | 107.00 | Konteks spasial |
| `DOWN` | -7.00 | 107.00 | Konteks spasial |
| `LEFT` | -6.75 | 106.75 | Konteks spasial |
| `RIGHT` | -6.75 | 107.25 | Konteks spasial |

Tabel 3.1 menyajikan koordinat geografis dan peran fungsional setiap node. Koordinat node `MAIN` berfungsi sebagai lokus target prediksi utama, sedangkan empat node sekitarnya (`UP`, `DOWN`, `LEFT`, `RIGHT`) berperan sebagai penyedia konteks spasial dinamika cuaca orografis. Urutan baris pada tabel dipertahankan saat data disusun menjadi masukan model.

Sebagai contoh, koordinat `MAIN` digunakan untuk mengambil data yang menjadi target prediksi. Koordinat `UP`, `DOWN`, `LEFT`, dan `RIGHT` digunakan untuk mengambil data pendukung dari lokasi di sekitar `MAIN`. Dengan demikian, satu waktu pengamatan menghasilkan satu kondisi cuaca pada lima lokasi, bukan hanya satu nilai dari `MAIN`.

Node tersebut merupakan titik grid (*grid point*) ERA5, bukan stasiun pengamatan. Node `DOWN` dipertahankan sebagai bagian dari struktur lima node yang ditetapkan, meskipun grid yang diperoleh memiliki elevasi sangat rendah dan karakter maritim. Kondisi ini menjadi keterbatasan representasi spasial yang perlu diperhatikan ketika menafsirkan hasil model [57].

### 3.2.2 Pengambilan Data melalui Open-Meteo API

Pengambilan data dilakukan melalui endpoint `https://archive-api.open-meteo.com/v1/archive` menggunakan protokol HTTPS dengan metode HTTP `GET`. Endpoint tersebut dipilih karena menyediakan data historis per jam dari model reanalisis ERA5. Permintaan dikirim menggunakan koordinat lima node, periode 1 Januari 2005 sampai 31 Desember 2025, zona waktu `Asia/Jakarta`, model `era5`, dan daftar variabel meteorologis yang diperlukan.

Parameter `latitude` dan `longitude` berisi koordinat lima node, sedangkan `start_date` dan `end_date` menentukan rentang data. Parameter `hourly` meminta field sumber `precipitation`, `temperature_2m`, `relative_humidity_2m`, `dew_point_2m`, `surface_pressure`, `wind_speed_10m`, `wind_direction_10m`, dan `cloud_cover`. Parameter `timezone=Asia/Jakarta` mengatur acuan waktu respons API, sedangkan data kemudian dikonversi dan disimpan dalam UTC. Parameter `models=era5` menetapkan sumber model reanalisis yang digunakan. Nama field tersebut merupakan nama mentah sebelum harmonisasi variabel karena berasal langsung dari API.

Contoh bentuk permintaan untuk lima node dapat ditulis sebagai berikut:

```text
GET https://archive-api.open-meteo.com/v1/archive
    ?latitude=-6.75,-6.50,-7.00,-6.75,-6.75
    &longitude=107.00,107.00,107.00,106.75,107.25
    &start_date=2005-01-01
    &end_date=2025-12-31
    &hourly=precipitation,temperature_2m,relative_humidity_2m,dew_point_2m,
            surface_pressure,wind_speed_10m,wind_direction_10m,cloud_cover
    &timezone=Asia/Jakarta
    &models=era5
```

Respons API berisi data per jam untuk setiap koordinat. Program memeriksa jumlah respons agar sama dengan jumlah node, kemudian membaca waktu, nilai variabel, koordinat grid aktual, dan elevasi. Permintaan menggunakan sesi dengan cache dan mekanisme percobaan ulang agar kegagalan jaringan sementara tidak langsung menghentikan proses.

### 3.2.3 Data Mentah ERA5

Data yang diterima dari Open-Meteo Archive API bersumber dari reanalisis ERA5 milik ECMWF (*European Centre for Medium-Range Weather Forecasts*). Model ERA5 menyediakan catatan cuaca historis global berbasis reanalisis atmosfer dengan resolusi spasial $0{,}25^\circ \times 0{,}25^\circ$ (sekitar $25\text{ km} \times 25\text{ km}$) pada skala waktu per jam. Secara keseluruhan, endpoint reanalisis ERA5 pada Open-Meteo menyediakan puluhan variabel permukaan (*surface variables*) yang mencakup parameter suhu, kelembapan, tekanan udara, presipitasi, radiasi matahari, tutupan awan, dan vektor angin.

Untuk kebutuhan penelitian *nowcasting* dan mitigasi risiko cuaca buruk di kawasan pegunungan, penelitian ini secara selektif meminta 8 variabel cuaca dinamis melalui parameter `hourly`:
1. `precipitation`: laju curah hujan per jam (mm/jam);
2. `temperature_2m`: suhu udara pada ketinggian 2 meter di atas permukaan tanah (°C);
3. `relative_humidity_2m`: kelembapan relatif udara pada ketinggian 2 meter (%);
4. `dew_point_2m`: suhu titik embun pada ketinggian 2 meter (°C);
5. `surface_pressure`: tekanan atmosfer di permukaan tanah (hPa);
6. `wind_speed_10m`: kecepatan hembusan angin pada ketinggian 10 meter (m/s);
7. `wind_direction_10m`: arah angin pada ketinggian 10 meter (derajat kompas $0^\circ–360^\circ$);
8. `cloud_cover`: persentase total tutupan awan (%).

Variabel radiasi matahari, salju, dan angin pada elevasi tinggi ($80\text{ m}$) tidak diambil karena tidak relevan secara langsung dengan dinamika mikroklimat permukaan dan risiko hipotermia pada ketinggian jalur pendakian.

Selain delapan variabel cuaca di atas, respons API memuat metadata lokasi, zona waktu, elevasi grid model, dan deret waktu `hourly.time`. Struktur data mentah yang diterima untuk satu koordinat dirangkum pada Tabel 3.2.

**Tabel 3.2 Contoh Struktur Data Respons Mentah ERA5 pada Satu Koordinat**

| Bagian respons | Field Open-Meteo | Contoh isi | Keterangan |
|---|---|---|---|
| Metadata lokasi | `latitude` | `-6.75` | Lintang pusat grid |
| Metadata lokasi | `longitude` | `107.00` | Bujur pusat grid |
| Metadata waktu | `utc_offset_seconds` | `25200` | Selisih detik terhadap UTC |
| Metadata waktu | `timezone` | `Asia/Jakarta` | Zona waktu respons |
| Metadata model | `elevation` | `1529` m | Ketinggian permukaan model |
| Deret waktu | `hourly.time` | `2004-12-31T17:00` | Timestamp ISO 8601 |
| Deret waktu | `hourly.precipitation` | `0.000` mm | Curah hujan 1 jam |
| Deret waktu | `hourly.temperature_2m` | `15.195` °C | Suhu udara 2 meter |
| Deret waktu | `hourly.relative_humidity_2m` | `95.591` % | Kelembapan relatif 2 meter |
| Deret waktu | `hourly.dew_point_2m` | `12.100` °C | Titik embun 2 meter |
| Deret waktu | `hourly.surface_pressure` | `850.000` hPa | Tekanan udara permukaan |
| Deret waktu | `hourly.wind_speed_10m` | `5.589` m/s | Kecepatan angin 10 meter |
| Deret waktu | `hourly.wind_direction_10m` | `180`° | Arah angin 10 meter |
| Deret waktu | `hourly.cloud_cover` | `73` % | Tutupan awan total |
| Satuan | `hourly_units` | Satuan masing-masing field | Metadata satuan variabel |

Elevasi yang digunakan sebagai fitur model diperoleh melalui Open-Meteo Elevation API secara terpisah untuk memastikan ketinggian aktual setiap koordinat terpetakan presisi, lalu dipasangkan kembali ke masing-masing node. Dalam arsitektur model, `elevation` berperan sebagai fitur statis lokasi (topografi), bukan fitur dinamis cuaca dan bukan target prediksi.

Respons mentah dari kelima koordinat tersebut mencakup periode 1 Januari 2005 hingga 31 Desember 2025 (21 tahun atau 184.080 timestamp per koordinat), sehingga menghasilkan total $184.080 \times 5 = 920.400$ baris data observasi koordinat-waktu sebelum masuk ke tahap penggabungan node.

### 3.2.4 Validasi Koordinat dan Pembentukan Lima Node

Validasi dilakukan setelah respons API diterima dan sebelum koordinat diberi label node. Tahap ini memeriksa pusat grid aktual (*grid center*) dan memastikan bahwa dua koordinat tidak memperoleh grid ERA5 yang sama. Benturan grid (*grid collision*) berarti dua koordinat berbeda dipetakan ke grid yang sama, sehingga keduanya tidak lagi memberikan informasi spasial yang berbeda.

Pemeriksaan koordinat secara ketat terhadap koordinat yang diminta diterapkan pada koordinat `MAIN`. Empat koordinat lainnya diperiksa melalui identitas grid dan pemeriksaan benturan grid. Setelah seluruh koordinat lolos pemeriksaan, program memasangkan koordinat dengan label node berdasarkan urutan yang telah ditentukan, yaitu `[MAIN, UP, DOWN, LEFT, RIGHT]`. Dengan demikian, data respons API berubah dari kumpulan respons berdasarkan urutan koordinat menjadi dataset dengan lima node yang memiliki identitas lokasi konsisten.

Kelengkapan data kemudian diperiksa pada setiap timestamp. Setiap timestamp harus memiliki tepat lima node dengan urutan yang sama. Sebagai contoh, respons lima koordinat tanpa benturan grid (*grid collision*) dapat dipetakan menjadi `MAIN`, `UP`, `DOWN`, `LEFT`, dan `RIGHT`. Jika satu koordinat tidak memiliki respons, atau dua koordinat memiliki grid yang sama, proses dihentikan. Validasi ini tidak mengubah nilai cuaca; tahap ini hanya memastikan koordinat benar, label node konsisten, dan struktur lima node siap digabungkan.

### 3.2.5 Gabung Lima Node

Setelah validasi berhasil dan label lima node terbentuk, data dari kelima node digabungkan berdasarkan timestamp UTC. Penggabungan dilakukan dengan mempertahankan ID node, peran node, koordinat grid, elevasi, dan seluruh variabel cuaca. Data kemudian diurutkan menggunakan urutan node `[MAIN, UP, DOWN, LEFT, RIGHT]` agar setiap timestamp selalu memiliki susunan baris yang sama.

Pada tahap penggabungan, tidak ada nilai cuaca yang dirata-ratakan atau dijumlahkan. Setiap node tetap menjadi satu baris tersendiri. Dengan demikian, informasi spasial tidak hilang ketika data disusun menjadi masukan graf. Fitur historis dari kelima node digunakan saat sampel pelatihan dan evaluasi dibentuk. Target prediksi hanya diambil dari node `MAIN`, sedangkan nilai target pada node konteks tidak digunakan sebagai keluaran supervisi maupun dalam perhitungan *loss* model.

Contoh hasil penggabungan lima node pada satu timestamp ditunjukkan pada Tabel 3.3. Visualisasi posisi node hasil pemetaan ditunjukkan pada Gambar 3.3.

**Tabel 3.3 Contoh Data Hasil Penggabungan Lima Node**

| Timestamp UTC | Node | `precipitation` | `temperature_2m` | `relative_humidity_2m` | `⋯` | `cloud_cover` | `elevation` |
|---|---|---:|---:|---:|---:|---:|---:|
| 2004-12-31 17:00 | `MAIN` | 0.000 | 15.195 | 95.591 | `⋯` | 73 | 1529 |
| 2004-12-31 17:00 | `UP` | 0.000 | 23.688 | 94.708 | `⋯` | 97 | 162 |
| 2004-12-31 17:00 | `DOWN` | 0.000 | 25.344 | 96.776 | `⋯` | 74 | 0 |
| 2004-12-31 17:00 | `LEFT` | 0.000 | 19.629 | 97.240 | `⋯` | 99 | 823 |
| 2004-12-31 17:00 | `RIGHT` | 0.000 | 23.570 | 96.149 | `⋯` | 67 | 288 |

Tabel 3.3 menunjukkan bahwa satu timestamp menghasilkan lima baris, yaitu satu baris untuk setiap node. Nilai tidak dirata-ratakan; setiap baris tetap mewakili kondisi node masing-masing. Pada tahap berikutnya, lima baris tersebut dibaca sebagai satu snapshot graf dengan lima node. Target pelatihan tetap hanya diambil dari `MAIN`, sedangkan empat node lain menyediakan konteks spasial.

![Gambar 3.3 — Posisi lima titik grid ERA5](bab3_media/gambar-3-3-posisi-node.jpeg)

**Gambar 3.3 Posisi Lima Titik Grid ERA5 di Sekitar Kawasan Gunung Gede–Pangrango**
*Sumber: rancangan penelitian berdasarkan koordinat node.*

Gambar 3.3 menunjukkan lima titik grid yang digunakan dalam penelitian. Unsur pada gambar dibaca sebagai berikut.

1. **`MAIN`** adalah titik grid pusat yang menjadi sumber target prediksi curah hujan, kecepatan angin, dan kelembapan relatif.
2. **`UP`** menyediakan fitur cuaca dari titik grid yang terletak di sisi utara relatif terhadap `MAIN`.
3. **`DOWN`** menyediakan fitur cuaca dari titik grid yang terletak di sisi selatan relatif terhadap `MAIN`.
4. **`LEFT`** menyediakan fitur cuaca dari titik grid yang terletak di sisi barat relatif terhadap `MAIN`.
5. **`RIGHT`** menyediakan fitur cuaca dari titik grid yang terletak di sisi timur relatif terhadap `MAIN`.

Posisi `UP`, `DOWN`, `LEFT`, dan `RIGHT` menunjukkan lokasi relatif node, bukan arah angin. Susunan ini kemudian digunakan untuk membentuk topologi graf.

### 3.2.6 Dataset Penelitian

Dataset penelitian merupakan keluaran akhir alur pengambilan data dan menjadi masukan untuk preprocessing pada Subbab 3.3. Dataset memiliki satu baris untuk setiap kombinasi timestamp dan node. Dataset lengkap terdiri atas 184.080 timestamp, lima node, dan 920.400 baris data. Dataset ini memuat delapan variabel cuaca dinamis dari API, satu fitur statis `elevation`, serta metadata dan fitur turunan yang diperlukan oleh pipeline. Ringkasannya ditunjukkan pada Tabel 3.4.

**Tabel 3.4 Karakteristik Dataset Penelitian**

| Karakteristik | Nilai |
|---|---|
| Sumber data | Open-Meteo Archive API berbasis ERA5 |
| Resolusi temporal | 1 jam |
| Periode data | 2005–2025 |
| Timestamp penyimpanan | UTC |
| Jumlah node | 5 |
| Jumlah timestamp | 184.080 |
| Total baris | 920.400 |
| Target | Curah hujan, kecepatan angin, kelembapan relatif pada `MAIN` |

Tabel 3.4 merangkum ukuran dan cakupan dataset setelah lima node digabungkan. Resolusi satu jam menunjukkan jarak waktu antarobservasi, lima node menunjukkan jumlah lokasi pada setiap timestamp, dan total baris merupakan hasil perkalian jumlah timestamp dengan jumlah node. Perhitungannya adalah:

$$
\text{Total baris}=184.080\times5=920.400
$$

Artinya, satu timestamp menghasilkan lima baris data, sedangkan 184.080 timestamp menghasilkan 920.400 baris. Target hanya berasal dari `MAIN`, sedangkan empat node lain dipakai sebagai konteks spasial.

## 3.3 Preprocessing Data

Preprocessing mengubah dataset penelitian menjadi data yang siap dibagi secara kronologis. Tahap ini dimulai dari dataset lima node yang telah diperoleh pada Subbab 3.2. Urutan tahap mengikuti Gambar 3.4: dataset penelitian, harmonisasi nama variabel, pengurutan kronologis, pembentukan fitur lag temporal, dan transformasi curah hujan. Pembagian dataset serta normalisasi dijelaskan pada Subbab 3.4.

Alur preprocessing ditunjukkan pada Gambar 3.4.

![Gambar 3.4 — Alur preprocessing data](bab3_media/gambar-3-4-alur-preprocessing.png)

**Gambar 3.4 Alur Preprocessing Data**
*Sumber: rancangan penelitian.*

Gambar 3.4 dibaca dari kiri ke kanan pada baris pertama, kemudian dilanjutkan ke bawah dan ke kiri pada baris kedua. Setiap tahap memiliki keluaran yang menjadi masukan tahap berikutnya. Penjelasan rinci setiap tahap diberikan pada Subbab 3.3.1 sampai 3.3.5. Tahap pembagian data kronologis dan normalisasi pada bagian akhir alur dijelaskan pada Subbab 3.4 agar urutannya tetap berhubungan dengan penjelasan statistik pembagian data.

### 3.3.1 Pemeriksaan Integritas Data Awal

Dataset penelitian pada awal preprocessing merupakan data hasil ekstraksi lima node dari Subbab 3.2.6. Sebelum dilakukan harmonisasi nama dan transformasi, catatan masih menggunakan nama field asli dari API Open-Meteo sebagaimana dirangkum pada contoh data gabungan (Tabel 3.3 pada Subbab 3.2.5).

Sebagai ilustrasi sebelum tahap preprocessing dilakukan, cuaca pada timestamp awal di node `MAIN` memiliki nilai asli:
- `precipitation`: $0{,}000\text{ mm/jam}$;
- `temperature_2m`: $15{,}195^\circ\text{C}$;
- `relative_humidity_2m`: $95{,}591\%$;
- `wind_speed_10m`: $5{,}589\text{ m/s}$;
- `elevation`: $1529\text{ m}$.

Setelah seluruh rangkaian tahap preprocessing (harmonisasi nama variabel, pengurutan kronologis, pembentukan lag, dan transformasi curah hujan) selesai dijalankan, catatan tersebut disiapkan menjadi data masukan terstruktur yang siap dibagi ke dalam partisi temporal. Pada akhir Subbab 3.3, nama variabel telah diharmonisasi (`temperature`, `wind_speed`, dsb.), fitur `precipitation_lag1` telah terisi nilai satu jam sebelumnya, dan nilai target curah hujan telah diubah ke skala $\log(1+y)$. Pembagian dataset ke partisi temporal dan proses normalisasi Z-score dijelaskan pada Subbab 3.4.

Sebelum diproses, setiap catatan harus memiliki timestamp UTC, ID node, variabel meteorologis, elevasi, dan curah hujan. Urutan node tetap digunakan, yaitu `[MAIN, UP, DOWN, LEFT, RIGHT]`. Dataset yang tidak memiliki kolom wajib atau tidak memiliki nilai yang dapat digunakan pada kolom fitur yang diperlukan tidak diteruskan ke tahap berikutnya. Sebagai contoh, catatan yang memiliki timestamp, ID node, sepuluh fitur masukan (9 meteorologis + precipitation), elevasi, dan curah hujan dapat diteruskan, sedangkan catatan tanpa timestamp atau ID node dihentikan pada tahap pemeriksaan. Dengan demikian, keluaran Subbab 3.3.1 adalah dataset penelitian dengan struktur yang siap diharmonisasi namanya.

### 3.3.2 Harmonisasi Nama Variabel

Harmonisasi nama variabel (sesuai tahap harmonisasi kolom pada Gambar 3.4) dilakukan agar nama field lebih mudah dibaca dan konsisten dengan penulisan ilmiah, tetapi tetap menggunakan format `snake_case`. Harmonisasi ini menghilangkan keterangan ketinggian pengukuran seperti `_2m` dan `_10m` pada nama untuk analisis; satuan dan makna variabel tidak berubah. Tabel 3.5 menampilkan field sumber/API dan nama variabel yang digunakan dalam analisis setelah tahap ini.

**Tabel 3.5 Harmonisasi Nama Variabel**

| No. | Nama field sumber/API | Nama variabel untuk analisis | Peran dan keterangan |
|---:|---|---|---|
| 1 | `precipitation` | `precipitation` | Target curah hujan dan dasar pembentukan `precipitation_lag1` |
| 2 | `temperature_2m` | `temperature` | Fitur dinamis suhu udara |
| 3 | `relative_humidity_2m` | `relative_humidity` | Fitur dinamis dan target kelembapan relatif |
| 4 | `dew_point_2m` | `dewpoint` | Fitur dinamis titik embun |
| 5 | `surface_pressure` | `surface_pressure` | Fitur dinamis tekanan permukaan |
| 6 | `wind_speed_10m` | `wind_speed` | Fitur dinamis dan target kecepatan angin |
| 7 | `wind_direction_10m` | `wind_direction` | Fitur dinamis arah angin |
| 8 | `cloud_cover` | `cloud_cover` | Fitur dinamis tutupan awan |
| 9 | — | `precipitation_lag1` | Fitur turunan curah hujan satu jam sebelumnya |
| 10 | — | `elevation` | Fitur statis elevasi node |

Tabel tersebut menunjukkan harmonisasi nama variabel untuk analisis, bukan penerjemahan ke bahasa Indonesia. Sebagai contoh, field `temperature_2m` ditulis sebagai `temperature`, bukan sebagai `suhu`. Fitur `precipitation_lag1` dibentuk setelah data diurutkan secara kronologis, sedangkan `elevation` diperoleh sebagai informasi lokasi dan tetap digunakan sebagai fitur statis.

Pada uraian setelah Subbab 3.3.2, nama variabel hasil harmonisasi digunakan secara konsisten. Nama field sumber/API hanya digunakan ketika menjelaskan respons Open-Meteo atau pemetaan pada Tabel 3.5. Harmonisasi nama tidak mengubah nilai, satuan, urutan fitur, atau jumlah node. Perlu diperhatikan bahwa `relative_humidity` dan `wind_speed` digunakan sebagai fitur pada waktu historis sekaligus sebagai target prediksi pada waktu satu jam berikutnya; penggunaannya pada dua posisi tersebut tidak berarti datanya berasal dari waktu yang sama.

### 3.3.3 Pengurutan Kronologis

Setelah struktur data diperiksa, seluruh catatan diurutkan berdasarkan timestamp UTC secara menaik. Pada timestamp yang sama, urutan node dipertahankan sebagai `[MAIN, UP, DOWN, LEFT, RIGHT]`. Pengurutan ini dilakukan sebelum pembentukan fitur temporal agar nilai satu jam sebelumnya benar-benar berasal dari timestamp sebelumnya, bukan dari baris yang hanya berdekatan secara posisi.

Sebagai contoh, catatan pada pukul 17.00 UTC ditempatkan sebelum catatan pada pukul 18.00 UTC untuk node yang sama. Jika urutan waktu tidak benar, fitur curah hujan sebelumnya dapat mengambil nilai dari waktu yang lebih baru dan menyebabkan kebocoran informasi. Keluaran tahap ini adalah dataset yang tersusun secara kronologis dan siap digunakan untuk pembentukan lag.

Contoh perubahan urutan data sebelum dan sesudah proses pengurutan kronologis disajikan pada Tabel 3.6. Contoh hanya menampilkan `MAIN` dan `UP` agar mudah dibaca; pada dataset penelitian, aturan yang sama diterapkan pada kelima node.

**Tabel 3.6 Contoh Pengurutan Data Berdasarkan Timestamp UTC**

| Tahap | Urutan | Timestamp UTC | Node | Curah hujan (`precipitation`) |
|---|---:|---|---|---:|
| Sebelum pengurutan | 1 | 2025-01-01 18:00 | `UP` | 0,400 mm |
| Sebelum pengurutan | 2 | 2025-01-01 17:00 | `MAIN` | 0,000 mm |
| Sebelum pengurutan | 3 | 2025-01-01 18:00 | `MAIN` | 0,500 mm |
| Sebelum pengurutan | 4 | 2025-01-01 17:00 | `UP` | 0,200 mm |
| Sesudah pengurutan | 1 | 2025-01-01 17:00 | `MAIN` | 0,000 mm |
| Sesudah pengurutan | 2 | 2025-01-01 17:00 | `UP` | 0,200 mm |
| Sesudah pengurutan | 3 | 2025-01-01 18:00 | `MAIN` | 0,500 mm |
| Sesudah pengurutan | 4 | 2025-01-01 18:00 | `UP` | 0,400 mm |

Pada bagian sebelum pengurutan, timestamp dan node masih bercampur. Setelah pengurutan, timestamp tersusun menaik dan node pada timestamp yang sama mengikuti urutan kanonik. Nilai cuaca tidak berubah; hanya posisi baris yang diperbaiki. Jika data divisualisasikan sebagai grafik deret waktu, sumbu horizontal menunjukkan timestamp UTC dan sumbu vertikal menunjukkan nilai `precipitation`; titik atau garis akan dibaca dari waktu paling awal ke waktu paling akhir. Contoh ini menjadi dasar pembentukan fitur `precipitation_lag1` pada subbab berikutnya.

### 3.3.4 Fitur Lag Temporal

Fitur lag temporal menyimpan curah hujan satu jam sebelumnya sebagai salah satu fitur masukan. Untuk setiap node, fitur tersebut dirumuskan sebagai:

$$
\mathrm{precipitation\_lag1}_t=\mathrm{precipitation}_{t-1}
\tag{3.1}
$$

Jika curah hujan pada `t−1` sebesar `2 mm`, maka `precipitation_lag1` pada `t` bernilai `2 mm`. Pada timestamp pertama setiap node, nilai lag diisi `0,0` karena belum tersedia catatan satu jam sebelumnya. Fitur lag merupakan informasi masa lalu dan berbeda dari target curah hujan pada waktu prediksi. Dalam implementasi, fitur ini dibentuk saat penyiapan dataset setelah data diurutkan; pada naskah, tahap tersebut dijelaskan sebagai bagian dari preprocessing.

Contoh perubahan satu deret data `MAIN` ditunjukkan pada Tabel 3.7. Kolom `precipitation` menunjukkan curah hujan pada timestamp target, sedangkan kolom `precipitation_lag1` menunjukkan curah hujan satu jam sebelumnya.

**Tabel 3.7 Contoh Deret Data `MAIN` dan Sumber Nilai Fitur Lag**

| Timestamp target UTC | Node | `precipitation` pada waktu target (mm) | Sumber nilai lag | `precipitation_lag1` (mm) |
|---|---|---:|---|---:|
| 2025-01-01 17:00 | `MAIN` | 0,000 | Belum tersedia | 0,000* |
| 2025-01-01 18:00 | `MAIN` | 2,000 | `precipitation` pukul 17.00 | 0,000 |
| 2025-01-01 19:00 | `MAIN` | 0,500 | `precipitation` pukul 18.00 | 2,000 |

`*` Nilai `0,000` pada timestamp pertama merupakan nilai awal karena belum ada data satu jam sebelumnya. Nilai lag pada pukul 19.00 berasal dari curah hujan pukul 18.00, bukan dari nilai pada pukul 19.00. Dengan demikian, fitur lag hanya menggunakan informasi masa lalu.

### 3.3.5 Transformasi Curah Hujan (`log1p`)

Transformasi `log1p` diterapkan khusus pada variabel target curah hujan (`precipitation`) karena sebagian besar nilainya bernilai nol (*zero-inflated*), sedangkan sebagian kecilnya memiliki intensitas sangat tinggi (*heavy-tailed*). Transformasi ini berfungsi meredam kemiringan (*skewness*) distribusi data sebelum dihitung statistik normalisasinya dan diproses oleh model *diffusion*. Fitur masukan `precipitation_lag1`, `wind_speed`, dan `relative_humidity` tidak menggunakan transformasi `log1p`, melainkan langsung dinormalisasi menggunakan statistik Z-score standar.

Transformasi `log1p` dirumuskan sebagai:

$$
y'=\log(1+y)
\tag{3.2}
$$

dengan `y` sebagai curah hujan asli dan `y'` sebagai nilai setelah transformasi. Kebalikan dari transformasi ini digunakan pada tahap post-processing untuk mengembalikan prediksi curah hujan ke skala aslinya melalui fungsi inversi eksponensial:

$$
y=\exp(y')-1
$$

Contoh perhitungannya adalah:

$$
\log1p(0)=\log(1+0)=0
$$

$$
\log1p(4)=\log(1+4)=\log(5)\approx1{,}609
$$

$$
\exp(1{,}609)-1\approx4\text{ mm}
$$

Contoh nilai dataset sebelum dan sesudah transformasi ditunjukkan pada Tabel 3.8. Nilai pada kolom `precipitation` masih menggunakan satuan asli, sedangkan nilai hasil `log1p` merupakan nilai sementara yang diteruskan ke tahap normalisasi; nilai tersebut tidak disimpan sebagai kolom baru pada dataset mentah. Nilai variabel lain, seperti `wind_speed` dan `relative_humidity`, tidak berubah pada tahap ini.

**Tabel 3.8 Contoh Curah Hujan Sebelum dan Sesudah Transformasi `log1p`**

| Timestamp UTC | Node | `precipitation` sebelum transformasi (mm) | Nilai sementara setelah `log1p` |
|---|---|---:|---:|
| 2025-01-01 17:00 | `MAIN` | 0,000 | 0,000 |
| 2025-01-01 18:00 | `MAIN` | 0,500 | 0,405 |
| 2025-01-01 19:00 | `MAIN` | 4,000 | 1,609 |

Tabel 3.8 memperlihatkan bahwa curah hujan nol tetap bernilai nol setelah transformasi, sedangkan nilai positif dikompresi ke skala yang lebih kecil. Transformasi ini tidak menghapus kejadian hujan; transformasi hanya mengubah skala numeriknya. Kecepatan angin dan kelembapan relatif tidak menggunakan transformasi `log1p`. Pada akhir Subbab 3.3, dataset telah memiliki nama variabel penyajian yang lebih ringkas, urutan kronologis, fitur lag, dan curah hujan yang telah ditransformasi secara sementara. Dataset tersebut belum dinormalisasi. Jika divisualisasikan, distribusi curah hujan setelah `log1p` menjadi lebih terpusat dan tidak terlalu dipengaruhi oleh nilai ekstrem, tetapi urutan waktu dan hubungan antarcatatan tetap sama. Pembagian kronologis dan normalisasi Z-score dijelaskan pada Subbab 3.4.

## 3.4 Pembagian Dataset Temporal

Dataset dibagi secara kronologis berdasarkan timestamp UTC agar model hanya belajar dari periode yang lebih awal dan dievaluasi pada periode yang lebih baru. Skema pembagian ditunjukkan pada Gambar 3.5.

![Gambar 3.5 — Skema pembagian dataset temporal](bab3_media/gambar-3-5-skema-pembagian.png)

**Gambar 3.5 Skema Pembagian Dataset Temporal**
*Sumber: rancangan penelitian.*

Gambar 3.5 menunjukkan tiga bagian data yang dipisahkan berdasarkan waktu.

1. **Data training** berisi periode paling awal. Data ini digunakan untuk menghitung statistik normalisasi, membangun basis analog historis, dan memperbarui parameter model.
2. **Data validation** berisi periode setelah training. Data ini digunakan untuk memantau proses pelatihan dan memilih checkpoint tanpa memperbarui statistik atau basis retrieval.
3. **Data test** berisi periode paling akhir. Data ini disimpan untuk evaluasi akhir dan tidak digunakan dalam pelatihan maupun pemilihan checkpoint.

Batas pembagian diterapkan pada timestamp UTC yang tersimpan dalam dataset. Periode lokal digunakan sebagai keterangan cakupan waktu, bukan sebagai acuan operasional pembagian. Tidak ada pengacakan, sehingga urutan waktu tetap terjaga.

### 3.4.1 Skema Pembagian Dataset

Rincian rentang waktu dan fungsi partisi temporal dataset disajikan pada Tabel 3.9.

**Tabel 3.9 Skema Pembagian Dataset Temporal**

| Himpunan | Rentang tahun berdasarkan timestamp UTC | Fungsi |
|---|---|---|
| Training | 2005–2018 | Menghitung statistik dan melatih model |
| Validation | 2019–2021 | Memantau pelatihan dan memilih checkpoint |
| Test | 2022–2025 | Evaluasi akhir |

Tabel 3.9 menunjukkan batas waktu dan fungsi setiap himpunan data. Data training berada pada periode paling awal, data validation digunakan setelah proses pelatihan untuk pemantauan, dan data test berada pada periode paling akhir untuk evaluasi. Rentang tabel mengacu pada timestamp UTC dan pembagian dilakukan tanpa pengacakan.

### 3.4.2 Pencegahan Data Leakage

Pencegahan kebocoran data (*data leakage*) dilakukan melalui beberapa aturan. Statistik normalisasi dihitung hanya dari data training. Basis analog historis dibangun dari data training. Data validation dan test tidak digunakan untuk memperbarui parameter model atau memilih parameter pelatihan. Setiap sampel prediksi menggunakan enam timestamp sebelum waktu target (rancangan jendela waktu historis $t-6$ sampai $t-1$ dirinci pada Subbab 3.5.2). Karena setiap himpunan diproses sebagai dataset terpisah, enam timestamp pertama pada data validation dan test tidak digunakan sebagai sampel karena belum memiliki jendela historis lengkap di dalam himpunan tersebut. Retrieval menggunakan basis data training dan aturan hanya-masa-lalu agar kondisi pada atau setelah waktu target tidak digunakan sebagai referensi (mekanisme retrieval dirinci pada Subbab 3.6.2).

### 3.4.3 Normalisasi Data

Setelah pembagian dataset, fitur dan target dinormalisasi menggunakan statistik data training. Statistik target dihitung dari node `MAIN`. Statistik fitur juga dihitung dari `MAIN`, kecuali fitur statis atau fitur lain yang memiliki simpangan baku degenerat; fitur tersebut menggunakan statistik seluruh node untuk mencegah pembagian dengan simpangan baku yang mendekati nol. Aturan ini menjaga agar fitur statis seperti `elevation` tetap memiliki skala yang dapat dibandingkan antarnode.

Normalisasi Z-score dilakukan dengan:

$$
z=\frac{v-\mu}{\sigma+10^{-5}}
\tag{3.3}
$$

dengan `v` sebagai nilai setelah transformasi, `μ` sebagai rata-rata data training, dan `σ` sebagai simpangan baku data training. Statistik yang sama digunakan pada data validation dan test. Dengan demikian, informasi dari validation dan test tidak masuk ke dalam perhitungan statistik training.

Perubahan data sebelum dan sesudah normalisasi dapat dilihat pada contoh `MAIN` berikut. Nilai sebelum normalisasi masih menggunakan satuan meteorologis atau hasil `log1p`, sedangkan nilai sesudah normalisasi berada pada skala Z-score dan digunakan oleh model.

**Tabel 3.10 Contoh Transformasi dan Normalisasi Target `MAIN`**

Tabel 3.10 mengilustrasikan perubahan nilai numerik target pada node `MAIN` setelah penerapan transformasi `log1p` dan normalisasi Z-score. Tabel dibaca dari kiri ke kanan: nilai asli, operasi sebelum Z-score, nilai setelah operasi tersebut, kemudian nilai setelah normalisasi.

| Variabel target | Nilai asli | Operasi sebelum Z-score | Nilai setelah transformasi | Nilai setelah normalisasi |
|---|---:|---|---:|---:|
| `precipitation` | 0,000 mm | `log1p` | 0,000 | -0,479 |
| `wind_speed` | 5,589 m/s | Tidak ada | 5,589 | 0,857 |
| `relative_humidity` | 95,591% | Tidak ada | 95,591 | 0,986 |

Pada baris `precipitation`, nilai asli `0,000 mm` terlebih dahulu menjadi `0` melalui `log1p`, kemudian menjadi `-0,479` setelah Z-score. Kecepatan angin dan kelembapan relatif tidak menggunakan `log1p`, sehingga nilai setelah transformasi masih sama dengan nilai asli sebelum normalisasi. Nilai tersebut kemudian diubah ke skala Z-score menggunakan rata-rata dan simpangan baku training.

Contoh perhitungan sederhana untuk target curah hujan pada `MAIN` adalah sebagai berikut. Misalkan curah hujan asli sebesar `0,000 mm`. Karena nilai tersebut diproses dengan `log1p`, nilai setelah transformasi menjadi:

$$
y'=\log(1+0)=0
$$

Berdasarkan statistik data training, rata-rata curah hujan setelah `log1p` adalah `μ=0,176636` dan simpangan bakunya `σ=0,368494`. Nilai Z-score kemudian dihitung sebagai:

$$
z=\frac{0-0,176636}{0,368494+0,00001}\approx-0,479
$$

Artinya, nilai `-0,479` bukan curah hujan sebesar `-0,479 mm`. Nilai tersebut adalah nilai curah hujan yang telah diubah ke skala standar agar dapat diproses bersama fitur lain. Contoh perhitungan `log1p` sebelum normalisasi telah ditunjukkan pada Subbab 3.3.5.

Untuk target kecepatan angin, prosesnya lebih singkat karena tidak menggunakan `log1p`. Misalnya nilai angin `5,589 m/s`, rata-rata training `3,873071`, dan simpangan baku `2,002620`, maka:

$$
z=\frac{5,589-3,873071}{2,002620+0,00001}\approx0,857
$$

Jadi, angka pada Tabel 3.10 merupakan nilai yang telah diubah skalanya, bukan satuan asli yang dihapus dari data. Tabel 3.10 merangkum target `MAIN`, sedangkan susunan lima node sebagai masukan graf dirangkum terpisah pada Tabel 3.11.

Untuk target curah hujan, urutan preprocessing adalah:

```text
curah hujan asli → log1p → Z-score → target model
```

Pada contoh timestamp awal, target `MAIN` memiliki curah hujan `0.000 mm`, kecepatan angin `5.589 m/s`, dan kelembapan relatif `95.591%`. Setelah menggunakan statistik training, nilainya menjadi sekitar `-0.479`, `0.857`, dan `0.986` secara berturut-turut. Contoh ini menunjukkan perubahan skala, bukan hasil prediksi model. Nilai target tersebut berasal dari timestamp target setelah jendela historis enam jam, bukan dari nilai fitur pada timestamp terakhir di dalam jendela.

Nilai fitur pada lima node juga dinormalisasi sebelum masuk ke graf. Untuk contoh timestamp yang sama, beberapa fitur setelah normalisasi ditunjukkan secara ringkas pada Tabel 3.11. Nama variabel tetap mengikuti nama hasil harmonisasi agar makna setiap kolom dapat dibaca langsung.

**Tabel 3.11 Contoh Fitur Lima Node Setelah Normalisasi**

| Node | `temperature` | `relative_humidity` | `dewpoint` | `⋯` | `elevation` |
|---|---:|---:|---:|---:|---:|
| `MAIN` | -0,996 | 0,986 | -0,034 | `⋯` | 1,737 |
| `UP` | 2,121 | 0,922 | 5,860 | `⋯` | -0,715 |
| `DOWN` | 2,728 | 1,073 | 7,285 | `⋯` | -1,005 |
| `LEFT` | 0,632 | 1,106 | 3,296 | `⋯` | 0,471 |
| `RIGHT` | 2,078 | 1,027 | 5,954 | `⋯` | -0,489 |

Tabel 3.11 menunjukkan bahwa satu timestamp menghasilkan lima baris fitur yang kemudian disusun menjadi matriks lima node. Kolom yang ditampilkan merupakan contoh dari sepuluh fitur masukan input; tanda `⋯` menunjukkan fitur lain yang tidak ditampilkan pada tabel. Nilai tersebut digunakan sebagai masukan graf, sedangkan target tetap hanya diambil dari `MAIN` pada waktu prediksi.

## 3.5 Pembentukan Fitur dan Representasi Graf

Setelah preprocessing, pembagian temporal, dan normalisasi, data disusun sebagai masukan yang sesuai dengan arsitektur model. Pada tahap ini, sepuluh fitur masukan dari lima node dibentuk menjadi enam timestamp historis. Contoh susunan fitur setelah normalisasi telah ditunjukkan pada Tabel 3.11.

### 3.5.1 Fitur Masukan Model

Fitur masukan model diringkas berdasarkan nama variabel hasil harmonisasi pada Tabel 3.12. Penamaan tersebut lebih informatif daripada label umum karena pembaca dapat langsung mengetahui makna setiap masukan.

**Tabel 3.12 Fitur Masukan Model Setelah Harmonisasi Nama Variabel**

Tabel 3.12 memisahkan fitur dinamis dan fitur statis. Fitur dinamis berubah setiap jam dan menggambarkan kondisi atmosfer pada waktu historis, sedangkan `elevation` diperlakukan sebagai informasi statis lokasi. Seluruh fitur tersedia pada lima node; tabel ini tidak berarti bahwa hanya `MAIN` yang memiliki fitur.

| No. | Nama variabel setelah harmonisasi | Keterangan | Status |
|---:|---|---|---|
| 1 | `temperature` | Suhu udara | Dinamis |
| 2 | `relative_humidity` | Kelembapan relatif | Dinamis |
| 3 | `dewpoint` | Titik embun | Dinamis |
| 4 | `surface_pressure` | Tekanan permukaan | Dinamis |
| 5 | `wind_speed` | Kecepatan angin | Dinamis |
| 6 | `wind_direction` | Arah angin | Dinamis |
| 7 | `cloud_cover` | Tutupan awan | Dinamis |
| 8 | `precipitation_lag1` | Curah hujan satu jam sebelumnya | Dinamis |
| 9 | `elevation` | Elevasi node | Statis |

Sembilan fitur tersebut digunakan pada waktu historis dari `t-6` sampai `t-1` untuk seluruh node. Tiga target pada waktu `t` tetap diambil dari `MAIN`, yaitu `precipitation`, `wind_speed`, dan `relative_humidity`. Dengan demikian, `relative_humidity` dan `wind_speed` dapat muncul sebagai fitur historis sekaligus target pada waktu berikutnya, sedangkan `precipitation_lag1` hanya berfungsi sebagai fitur masukan. Keempat node selain `MAIN` berfungsi sebagai konteks spasial.

### 3.5.2 Pembentukan Jendela Waktu Historis

Untuk target meteorologis pada waktu `t`, masukan graf hanya menggunakan enam timestamp sebelumnya. Jendela graf ditulis sebagai:

$$
\mathcal{G}_t=\left(G_{t-6},G_{t-5},G_{t-4},G_{t-3},G_{t-2},G_{t-1}\right)
\tag{3.4}
$$

Setiap `G` memiliki lima node dan sepuluh fitur per node (9 meteorologis + precipitation). Konteks tambahan diambil dari fitur `MAIN` pada `t-1`, sedangkan target adalah:

$$
y_t^{MAIN}=\left(\mathrm{precipitation}_t,\mathrm{wind\_speed}_t,\mathrm{relative\_humidity}_t\right)
\tag{3.5}
$$

Contoh jendela historis untuk target pukul 18.00 UTC ditunjukkan pada Tabel 3.13.

**Tabel 3.13 Contoh Jendela Historis untuk Prediksi Pukul 18.00 UTC**

| Posisi waktu | Timestamp UTC | Isi data | Peran |
|---|---|---|---|
| `t−6` | 12.00 | `G_{t-6}`: 5 node × 10 fitur | Snapshot graf |
| `t−5` | 13.00 | `G_{t-5}`: 5 node × 10 fitur | Snapshot graf |
| `t−4` | 14.00 | `G_{t-4}`: 5 node × 10 fitur | Snapshot graf |
| `t−3` | 15.00 | `G_{t-3}`: 5 node × 10 fitur | Snapshot graf |
| `t−2` | 16.00 | `G_{t-2}`: 5 node × 10 fitur | Snapshot graf |
| `t−1` | 17.00 | `G_{t-1}`: 5 node × 10 fitur | Snapshot graf dan konteks `MAIN` |
| `t` | 18.00 | 3 target dari `MAIN` | Target prediksi, bukan masukan |

Enam baris pertama pada Tabel 3.13 digunakan sebagai masukan model. Baris pada waktu `t` tidak dimasukkan ke dalam urutan graf karena berisi nilai yang ingin diprediksi. Setiap snapshot memiliki lima node dan sepuluh fitur masukan, sedangkan konteks tambahan hanya mengambil fitur `MAIN` pada `t−1`. Dengan demikian, urutan waktu, bentuk data, dan posisi target dapat dibaca secara langsung.

### 3.5.3 Topologi Graf Lima Node

Hubungan antarnode direpresentasikan dengan topologi bintang (*star*). `MAIN` terhubung secara dua arah dengan `UP`, `DOWN`, `LEFT`, dan `RIGHT`. Node tetangga tidak memiliki edge graf langsung satu sama lain. Topologi tersebut menghasilkan delapan edge graf berarah.

Topologi keterhubungan spasial dan arah pertukaran pesan antar-node disajikan pada Gambar 3.6.

![Gambar 3.6 — Topologi graf star lima node](bab3_media/gambar-3-6-topologi-graf.jpeg)

**Gambar 3.6 Topologi Graf Star Lima Node**
*Sumber: rancangan penelitian.*

Gambar 3.6 menunjukkan susunan topologi graf yang digunakan.

1. **`MAIN`** berada di tengah dan menjadi node yang terhubung dengan seluruh node konteks.
2. **`UP`, `DOWN`, `LEFT`, dan `RIGHT`** menjadi node tetangga yang mengirimkan dan menerima informasi dari `MAIN`.
3. **Panah** menunjukkan arah pertukaran pesan graf, bukan arah angin.
4. **Delapan edge graf berarah** berasal dari empat pasangan hubungan dua arah antara `MAIN` dan setiap node tetangga.
5. **Self-loop** atau sisi yang menghubungkan node dengan dirinya sendiri tidak ditampilkan sebagai bagian dari delapan edge graf berarah. Penambahan self-loop oleh lapisan graf dijelaskan pada Subbab 3.6.1.

Pada tahap pembentukan graf, informasi spasial utama berasal dari topologi bintang dan perbedaan fitur antarnode pada setiap timestamp. Detail atribut edge graf dan pemrosesan pesan internal lapisan graf dijelaskan pada Subbab 3.6.1. Representasi urutan graf enam timestamp ini kemudian menjadi masukan bagi *Spatio-Temporal Graph Neural Network* untuk memodelkan ketergantungan ruang-waktu secara simultan.

## 3.6 Perancangan Arsitektur Model

*Embedding* adalah vektor numerik yang merangkum informasi representasi laten agar dapat diproses oleh *neural network*. Model penelitian dirancang sebagai integrasi beberapa komponen. Urutan pemrosesannya meliputi: pembentukan *graph embedding*, pembentukan *context embedding*, pencarian analog historis (*analog retrieval*), penggabungan *conditioning*, pembentukan *time embedding*, prediksi *noise* oleh MLP *denoiser*, dan pembangkitan sampel (*sampling*) melalui *reverse diffusion*. Istilah teknis dipertahankan pada nama komponen atau kode program, sedangkan penjelasan alur proses disajikan secara sistematis dalam bahasa Indonesia akademis.

### 3.6.1 Spatio-Temporal Graph Neural Network

*Spatio-Temporal Graph Neural Network* (STGNN) dirancang untuk memodelkan interaksi spasial antarlokasi lereng Gunung Gede-Pangrango sekaligus dinamika ketergantungan temporal cuaca dari enam *snapshot* graf historis menjadi satu vektor representasi graf padat (*graph embedding*). Arsitektur ini terdiri atas pemrosesan spasial menggunakan dua lapis *Graph Attention Network* (GAT) dan pemrosesan temporal menggunakan *Causal Multi-Head Self-Attention*. Alur pemrosesan STGNN ditunjukkan pada Gambar 3.7.

![Gambar 3.7 — Alur Spatio-Temporal Graph Neural Network](bab3_media/gambar-3-7-arsitektur-stgnn.png)

**Gambar 3.7 Alur Spatio-Temporal Graph Neural Network**
*Sumber: rancangan arsitektur model.*

Gambar 3.7 dibaca dari kiri ke kanan dengan rincian tujuh tahapan pemrosesan sebagai berikut:

1. **Input Sequence**
   Lapisan masukan menerima urutan enam *snapshot* graf historis $\mathcal{G}_t = (G_{t-6}, G_{t-5}, \dots, G_{t-1})$ sepanjang jendela waktu $t-6$ hingga $t-1$. Setiap *snapshot* graf pada langkah waktu $\tau \in \{t-6, \dots, t-1\}$ didefinisikan sebagai $G_\tau = (\mathcal{V}, \mathcal{E}, \mathbf{X}_\tau, \mathbf{E})$, di mana $\mathcal{V} = \{\text{MAIN, UP, DOWN, LEFT, RIGHT}\}$ merupakan himpunan lima node pemantauan ($|\mathcal{V}| = 5$), $\mathcal{E}$ adalah himpunan 8 *directed edges* berarah dua arah antara `MAIN` dan empat node lereng bertopologi bintang (*star topology*), $\mathbf{E} \in \mathbb{R}^{8 \times 1}$ adalah atribut jarak spasial statis antar-grid ($0{,}25^\circ$), dan $\mathbf{X}_\tau \in \mathbb{R}^{5 \times 9}$ merupakan matriks sepuluh fitur masukan cuaca ternormalisasi untuk kelima node. Matriks fitur pada waktu $\tau$ dirumuskan sebagai:
   $$
   \mathbf{X}_\tau = \begin{bmatrix} \mathbf{x}_{\text{MAIN},\tau}^T \\ \mathbf{x}_{\text{UP},\tau}^T \\ \mathbf{x}_{\text{DOWN},\tau}^T \\ \mathbf{x}_{\text{LEFT},\tau}^T \\ \mathbf{x}_{\text{RIGHT},\tau}^T \end{bmatrix} \in \mathbb{R}^{5 \times 9}
   \tag{3.6}
   $$
   *Contoh pemakaian data:* Pada langkah waktu $t-1$, node `MAIN` memiliki vektor fitur masukan ternormalisasi $\mathbf{x}_{\text{MAIN},t-1} = [-0{,}996, 0{,}986, -0{,}034, 0{,}120, 0{,}857, -0{,}420, 0{,}310, 0{,}000, 1{,}737]^T \in \mathbb{R}^9$ yang memuat variabel suhu, kelembapan, titik embun, tekanan, angin, tutupan awan, lag hujan, dan elevasi. Bersama empat node lainnya, terbentuk matriks masukan berdimensi $5 \times 9$ per *snapshot*.

2. **GAT1 (*Graph Attention Network 1*)**
   Lapisan konvolusi graf pertama menerapkan mekanisme *multi-head spatial attention* dengan $K_1 = 4$ *heads* independen dan dimensi tersembunyi $d_1 = 64$ per *head*. Lapisan ini menghitung koefisien atensi spasial $\alpha_{ij,\tau}^{k}$ antara node target $i$ dan node tetangga $j \in \mathcal{N}(i) \cup \{i\}$ dengan mempertimbangkan fitur node serta atribut jarak *edge* $\mathbf{e}_{ij}$, kemudian menggabungkan (*concatenate*) keluaran keempat *head* dan menerapkan fungsi aktivasi ReLU:
   $$
   \mathbf{h}_{i,\tau}^{(1)} = \text{ReLU}\left( \bigoplus_{k=1}^{4} \sum_{j \in \mathcal{N}(i) \cup \{i\}} \alpha_{ij,\tau}^{k} \mathbf{W}_1^k \mathbf{x}_{j,\tau} \right) \in \mathbb{R}^{256}
   \tag{3.7}
   $$
   di mana $\mathbf{W}_1^k \in \mathbb{R}^{64 \times 9}$ adalah matriks bobot proyeksi linier *head* ke-$k$, $\bigoplus$ melambangkan operasi konkatenasi vektor, dan $\alpha_{ij,\tau}^k$ adalah bobot atensi bernilai non-negatif dengan $\sum_{j} \alpha_{ij,\tau}^k = 1$.
   *Contoh pemakaian rumus:* Masukan node `MAIN` $\mathbf{x}_{\text{MAIN},\tau} \in \mathbb{R}^9$ diagregasikan bersama empat node tetangganya (`UP, DOWN, LEFT, RIGHT`) dan *self-loop*. Setiap *head* menghasilkan vektor representasi berdimensi 64. Hasil konkatenasi 4 *head* menghasilkan vektor fitur spasial tingkat pertama $\mathbf{h}_{\text{MAIN},\tau}^{(1)} \in \mathbb{R}^{256}$, sehingga seluruh graf pada waktu $\tau$ menghasilkan tensor berdimensi $5 \times 256$.

3. **GAT2 (*Graph Attention Network 2*)**
   Lapisan konvolusi graf kedua menggunakan satu *head* atensi tunggal ($K_2 = 1$) untuk memetakan kembali representasi 256 dimensi hasil GAT1 menjadi representasi spasial lokal berdimensi 64 yang lebih padat dan terintegrasi. Agregasi dilakukan secara linier tanpa fungsi aktivasi non-linier tambahan sebelum proses pooling:
   $$
   \mathbf{h}_{i,\tau}^{(2)} = \sum_{j \in \mathcal{N}(i) \cup \{i\}} \alpha_{ij,\tau}^{(2)} \mathbf{W}_2 \mathbf{h}_{j,\tau}^{(1)} \in \mathbb{R}^{64}
   \tag{3.8}
   $$
   di mana $\mathbf{W}_2 \in \mathbb{R}^{64 \times 256}$ merupakan matriks transformasi linier dan $\alpha_{ij,\tau}^{(2)}$ adalah koefisien atensi spasial lapisan kedua.
   *Contoh pemakaian rumus:* Vektor representasi node $\mathbf{h}_{i,\tau}^{(1)} \in \mathbb{R}^{256}$ dari kelima node ditransformasikan melalui perkalian dengan $\mathbf{W}_2$ dan dibobotkan oleh atensi spasial lapis kedua, menghasilkan matriks representasi node akhir $\mathbf{H}_\tau^{(2)} = [\mathbf{h}_{\text{MAIN},\tau}^{(2)}, \mathbf{h}_{\text{UP},\tau}^{(2)}, \mathbf{h}_{\text{DOWN},\tau}^{(2)}, \mathbf{h}_{\text{LEFT},\tau}^{(2)}, \mathbf{h}_{\text{RIGHT},\tau}^{(2)}]^T \in \mathbb{R}^{5 \times 64}$.

4. **Global Mean Pool**
   Operasi *global mean pooling* merata-ratakan representasi fitur dari seluruh node pada masing-masing *snapshot* graf untuk menghasilkan satu vektor ringkasan tingkat graf (*graph-level embedding*) $\mathbf{g}_\tau \in \mathbb{R}^{64}$ pada setiap langkah waktu $\tau$. Enam vektor ringkasan dari $\tau = t-6$ hingga $t-1$ kemudian disusun secara sekuensial membentuk matriks deret temporal:
   $$
   \mathbf{g}_\tau = \frac{1}{|\mathcal{V}|} \sum_{i=1}^{5} \mathbf{h}_{i,\tau}^{(2)} = \frac{\mathbf{h}_{\text{MAIN},\tau}^{(2)} + \mathbf{h}_{\text{UP},\tau}^{(2)} + \mathbf{h}_{\text{DOWN},\tau}^{(2)} + \mathbf{h}_{\text{LEFT},\tau}^{(2)} + \mathbf{h}_{\text{RIGHT},\tau}^{(2)}}{5} \in \mathbb{R}^{64}
   \tag{3.9}
   $$
   $$
   \mathbf{G} = \begin{bmatrix} \mathbf{g}_{t-6} \\ \mathbf{g}_{t-5} \\ \vdots \\ \mathbf{g}_{t-1} \end{bmatrix} \in \mathbb{R}^{6 \times 64}
   $$
   *Contoh pemakaian rumus:* Pada langkah waktu $t-1$, agregasi rata-rata per elemen (*element-wise mean*) terhadap lima vektor node berdimensi 64 menghasilkan satu vektor graf $\mathbf{g}_{t-1} \in \mathbb{R}^{64}$. Pengulangan operasi pada enam *timestamp* menghasilkan matriks urutan temporal graf $\mathbf{G} \in \mathbb{R}^{6 \times 64}$ (atau tensor berdimensi $[B \times 6 \times 64]$ untuk *batch* berukuran $B$).

5. **Temporal Attention**
   Blok pemodelan waktu menerapkan *Causal Multi-Head Self-Attention* ($K_t = 4$ *heads*, dimensi per *head* $d_k = 64/4 = 16$) yang diperkaya dengan *learnable positional embedding* $\mathbf{E}_{pos} \in \mathbb{R}^{6 \times 64}$ untuk mengenali urutan kronologis antar-jam. Struktur ini dilengkapi koneksi residual (*residual connection*), regularisasi *dropout* ($p = 0{,}1$), dan *Layer Normalization*:
   $$
   \tilde{\mathbf{G}} = \mathbf{G} + \mathbf{E}_{pos} \in \mathbb{R}^{6 \times 64}
   \tag{3.10}
   $$
   $$
   \text{head}_m = \text{softmax}\left( \frac{\mathbf{Q}_m \mathbf{K}_m^T}{\sqrt{d_k}} + \mathbf{M}_{causal} \right) \mathbf{V}_m \in \mathbb{R}^{6 \times 16}, \quad m \in \{1, 2, 3, 4\}
   $$
   $$
   \mathbf{Z} = \text{LayerNorm}\left( \tilde{\mathbf{G}} + \text{Dropout}\left( \bigoplus_{m=1}^{4} \text{head}_m \mathbf{W}_O \right) \right) \in \mathbb{R}^{6 \times 64}
   $$
   di mana $\mathbf{Q}_m = \tilde{\mathbf{G}}\mathbf{W}_Q^m$, $\mathbf{K}_m = \tilde{\mathbf{G}}\mathbf{W}_K^m$, dan $\mathbf{V}_m = \tilde{\mathbf{G}}\mathbf{W}_V^m$ dengan matriks proyeksi $\mathbf{W}_Q^m, \mathbf{W}_K^m, \mathbf{W}_V^m \in \mathbb{R}^{64 \times 16}$, $\mathbf{W}_O \in \mathbb{R}^{64 \times 64}$, serta skala normalisasi $\sqrt{d_k} = \sqrt{16} = 4$.
   *Contoh pemakaian rumus:* Matriks $\mathbf{G} \in \mathbb{R}^{6 \times 64}$ dijumlahkan dengan matriks posisi $\mathbf{E}_{pos} \in \mathbb{R}^{6 \times 64}$. Setiap langkah waktu menghitung korelasi temporal masa lalunya melalui 4 *head*, melewati *dropout* dan normalisasi lapisan, menghasilkan representasi temporal $\mathbf{Z} \in \mathbb{R}^{6 \times 64}$.

6. **Causal Slicing Last Timestep**
   Penerapan matriks *causal mask* $\mathbf{M}_{causal} \in \mathbb{R}^{6 \times 6}$ (bernilai $-\infty$ pada elemen segitiga atas di mana kolom $>$ baris, dan bernilai $0$ pada elemen lainnya) menjamin prinsip kausalitas temporal terpenuhi secara ketat, yaitu langkah waktu $\tau$ tidak dapat mengakses informasi waktu di masa depan ($> \tau$). Representasi fitur pada langkah waktu paling akhir ($t-1$) kemudian diiris (*sliced*) sebagai ringkasan kondisi cuaca historis paling mutakhir:
   $$
   \mathbf{h}_{last} = \mathbf{Z}[-1, :] = \mathbf{z}_{t-1} \in \mathbb{R}^{64}
   \tag{3.11}
   $$
   *Contoh pemakaian rumus:* Dari matriks sekuens temporal $\mathbf{Z} \in \mathbb{R}^{6 \times 64}$ yang memuat urutan $[\mathbf{z}_{t-6}, \mathbf{z}_{t-5}, \mathbf{z}_{t-4}, \mathbf{z}_{t-3}, \mathbf{z}_{t-2}, \mathbf{z}_{t-1}]^T$, operasi *slicing* mengambil baris ke-6 ($\mathbf{z}_{t-1}$), menghasilkan vektor representasi tunggal $\mathbf{h}_{last} \in \mathbb{R}^{64}$ yang telah mengagregasikan konteks dinamika atmosfer dari lima jam sebelumnya secara autoregresif tanpa kebocoran data masa depan.

7. **Output Projection**
   Tahap akhir STGNN menggunakan lapisan transformasi linier (`nn.Linear(64, 64)`) untuk memproyeksikan vektor temporal terakhir ke dalam ruang *embedding* representasi graf akhir:
   $$
   \mathbf{h}_{graph} = \mathbf{W}_{out}\mathbf{h}_{last} + \mathbf{b}_{out} \in \mathbb{R}^{64}
   \tag{3.12}
   $$
   di mana $\mathbf{W}_{out} \in \mathbb{R}^{64 \times 64}$ adalah matriks bobot proyeksi dan $\mathbf{b}_{out} \in \mathbb{R}^{64}$ adalah vektor bias.
   *Contoh pemakaian rumus:* Vektor $\mathbf{h}_{last} \in \mathbb{R}^{64}$ dikalikan dengan bobot $\mathbf{W}_{out}$ dan ditambahkan bias $\mathbf{b}_{out}$ menghasilkan vektor **Output STGNN (*Graph Embedding*)** $\mathbf{h}_{graph} \in \mathbb{R}^{64}$. Vektor ini siap diteruskan ke modul *Graph MLP* pada arsitektur *diffusion* (Subbab 3.6.2 butir 2).

Hasil akhirnya adalah embedding graf berdimensi 64 yang memuat ringkasan keterkaitan spasial antarlokasi dan dinamika temporal cuaca sepanjang jendela historis enam jam. Rincian alur transformasi tensor pada setiap tahapan STGNN dirangkum pada Tabel 3.14.

**Tabel 3.14 Rincian Alur Transformasi Tensor pada Komponen STGNN**

| No. | Nama Komponen | Modul / Operasi PyTorch | Dimensi Masukan | Dimensi Keluaran | Keterangan Pemrosesan |
|---:|---|---|---|---|---|
| 1 | Input Sequence | `torch_geometric.data.Data` | $6 \times [5, 9]$ | $6 \times [5, 9]$ | Enam snapshot graf historis ($t-6 \dots t-1$) |
| 2 | GAT1 | `GATConv(9, 64, heads=4)` + `ReLU` | $[5, 9]$ per snapshot | $[5, 256]$ per snapshot | Multi-head spatial attention terkonkatenasi |
| 3 | GAT2 | `GATConv(256, 64, heads=1)` | $[5, 256]$ per snapshot | $[5, 64]$ per snapshot | Reduksi representasi spasial node |
| 4 | Global Mean Pool | `global_mean_pool` | $[5, 64]$ per snapshot | $[1, 64]$ per snapshot | Agregasi rata-rata 5 node ke level graf |
| 5 | Temporal Attention | `MultiheadAttention(64, heads=4)` | $[6, 64]$ | $[6, 64]$ | Causal self-attention temporal + Positional Embedding |
| 6 | Causal Slicing | `x[:, -1, :]` (*tensor slicing*) | $[6, 64]$ | $[1, 64]$ | Pengambilan representasi waktu terakhir ($t-1$) |
| 7 | Output Projection | `nn.Linear(64, 64)` | $[1, 64]$ | $[1, 64]$ | Proyeksi linier menuju *Graph Embedding* |

### 3.6.2 Integrasi Retrieval-Augmented Diffusion Model

Integrasi arsitektur *Retrieval-Augmented Diffusion Model* dengan *Spatio-Temporal Graph Neural Network* (STGNN) dirancang untuk memprediksi distribusi probabilitas multivariat tiga parameter cuaca target ($\text{curah hujan } [\text{mm/jam}]$, $\text{kecepatan angin } [\text{m/s}]$, dan $\text{kelembapan relatif } [\%]$) pada node `MAIN` untuk horizon waktu $t$. Arsitektur ini menggabungkan empat pilar representasi utama: (1) konteks dinamika spasio-temporal regional melalui graf lereng pegunungan, (2) konteks meteorologis lokal mutakhir node target, (3) analog historis pola cuaca serupa dari basis data k-NN masa lalu (*historical analogs*), dan (4) pemodelan *noise* stokastik berbasis *reverse diffusion*.

Alur rancangan integrasi model, komponen pemrosesan kondisi (*conditioning*), perambatan maju *denoiser*, serta mekanisme perhitungan fungsi *loss* disajikan secara menyeluruh pada Gambar 3.8.

![Gambar 3.8 — Integrasi retrieval, STGNN, dan diffusion model](bab3_media/gambar-3-8-arsitektur-diffusion.png)

**Gambar 3.8 Integrasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network**
*Sumber: rancangan arsitektur model.*

Gambar 3.8 dibaca mengikuti 25 tahapan penomoran komponen terpadu dengan rincian formulasi matematis, operasi komputasi, dan contoh pemakaian tensor konkret sebagai berikut:

1. **Output STGNN (1)**
   - **Fungsi**: Mengekstraksi keterkaitan spasial regional dan dinamika temporal dari urutan graf cuaca historis.
   - **Masukan**: Enam *snapshot* graf historis $\mathcal{G}_t \in \mathbb{R}^{6 \times 5 \times 9}$ ($t-6 \dots t-1$).
   - **Keluaran**: Vektor representasi graf (*graph embedding*) $\mathbf{h}_{graph} \in \mathbb{R}^{64}$.
   - *Contoh data konkret:* Vektor keluaran STGNN untuk satu sampel masukan dinyatakan sebagai vektor $\mathbf{h}_{graph} = [0{,}214, -0{,}582, \dots, 0{,}109]^T \in \mathbb{R}^{64}$ (atau tensor berdimensi $[B, 64]$ untuk ukuran *batch* $B$).

2. **Graph MLP (2)**
   - **Fungsi**: Memproyeksikan vektor keluaran STGNN ke dalam ruang representasi *conditioning* laten (*conditioning space*).
   - **Masukan**: Vektor $\mathbf{h}_{graph} \in \mathbb{R}^{64}$.
   - **Keluaran**: Vektor kondisi graf $\mathbf{h}_t^G \in \mathbb{R}^{64}$.
   - **Rumus**:
     $$
     \mathbf{h}_t^G = \mathbf{W}_{G2} \cdot \text{SiLU}(\mathbf{W}_{G1}\mathbf{h}_{graph} + \mathbf{b}_{G1}) + \mathbf{b}_{G2} \in \mathbb{R}^{64}
     \tag{3.13}
     $$
     di mana $\mathbf{W}_{G1}, \mathbf{W}_{G2} \in \mathbb{R}^{64 \times 64}$ dan $\mathbf{b}_{G1}, \mathbf{b}_{G2} \in \mathbb{R}^{64}$.
   - *Contoh pemakaian rumus:* Vektor $\mathbf{h}_{graph} \in \mathbb{R}^{64}$ melewati transformasi linier pertama menjadi vektor 64 dimensi, diaktivasi dengan $\text{SiLU}(x) = x \cdot \sigma(x)$, lalu diproyeksikan kembali oleh lapisan kedua menghasilkan $\mathbf{h}_t^G = [0{,}145, -0{,}312, \dots, 0{,}088]^T \in \mathbb{R}^{64}$.

3. **Context Input (3)**
   - **Fungsi**: Menyediakan kondisi meteorologis permukaan mutakhir yang diamati secara lokal di node `MAIN`.
   - **Masukan**: Nilai observasi lokal pada $t-1$.
   - **Keluaran**: Vektor sepuluh fitur masukan ternormalisasi $\mathbf{x}_{\text{MAIN}, t-1} \in \mathbb{R}^9$.
   - **Rumus**:
     $$
     \mathbf{x}_{\text{MAIN}, t-1} = [T, RH, DP, SP, WS, WD, CC, P_{lag1}, Elev]^T \in \mathbb{R}^9
     \tag{3.14}
     $$
   - *Contoh pemakaian data:* Vektor fitur ternormalisasi Z-score pada waktu $t-1$ bernilai $\mathbf{x}_{\text{MAIN}, t-1} = [-0{,}996, 0{,}986, -0{,}034, 0{,}120, 0{,}857, -0{,}420, 0{,}310, 0{,}000, 1{,}737]^T \in \mathbb{R}^9$.

4. **Context MLP (4)**
   - **Fungsi**: Memetakan vektor sepuluh fitur masukan lokal `MAIN` ke ruang representasi kondisi tersembunyi.
   - **Masukan**: Vektor $\mathbf{x}_{\text{MAIN}, t-1} \in \mathbb{R}^9$.
   - **Keluaran**: Vektor kondisi lokal $\mathbf{h}_t^{\text{MAIN}} \in \mathbb{R}^{64}$.
   - **Rumus**:
     $$
     \mathbf{h}_t^{\text{MAIN}} = \mathbf{W}_{C2} \cdot \text{SiLU}(\mathbf{W}_{C1}\mathbf{x}_{\text{MAIN}, t-1} + \mathbf{b}_{C1}) + \mathbf{b}_{C2} \in \mathbb{R}^{64}
     \tag{3.15}
     $$
     di mana $\mathbf{W}_{C1} \in \mathbb{R}^{64 \times 9}$, $\mathbf{b}_{C1} \in \mathbb{R}^{64}$, $\mathbf{W}_{C2} \in \mathbb{R}^{64 \times 64}$, dan $\mathbf{b}_{C2} \in \mathbb{R}^{64}$.
   - *Contoh pemakaian rumus:* Vektor masukan $\mathbf{x}_{\text{MAIN}, t-1} \in \mathbb{R}^9$ ditransformasikan oleh matriks $\mathbf{W}_{C1}$, diaktivasi oleh SiLU, dan diproyeksikan oleh $\mathbf{W}_{C2}$ menghasilkan vektor kondisi lokal $\mathbf{h}_t^{\text{MAIN}} = [-0{,}421, 0{,}203, \dots, -0{,}115]^T \in \mathbb{R}^{64}$.

5. **Retrieval Input (5)**
   - **Fungsi**: Menyediakan target historis satu jam ke depan dari tiga kejadian masa lalu yang paling mirip (*Top-3 Analogs* via FAISS k-NN).
   - **Masukan**: Matriks $3 \text{ tetangga} \times 3 \text{ target}$ ($\mathbf{v}_{\tau_1}, \mathbf{v}_{\tau_2}, \mathbf{v}_{\tau_3}$).
   - **Keluaran**: Vektor hasil *flattening* (*flattened vector*) $\mathbf{r}_{flat} \in \mathbb{R}^9$.
   - **Rumus**:
     $$
     \mathbf{r}_{flat} = \text{vec}([\mathbf{v}_{\tau_1}, \mathbf{v}_{\tau_2}, \mathbf{v}_{\tau_3}]^T) \in \mathbb{R}^9
     \tag{3.16}
     $$
   - *Contoh pemakaian data:* Tiga analog historis terdekat memberikan target satu jam ke depan ternormalisasi $\mathbf{v}_{\tau_1} = [0{,}00, -0{,}35, 0{,}82]$, $\mathbf{v}_{\tau_2} = [0{,}45, -0{,}10, 0{,}65]$, dan $\mathbf{v}_{\tau_3} = [0{,}00, -0{,}22, 0{,}78]$. Penggabungan ketiganya menghasilkan $\mathbf{r}_{flat} = [0{,}00, -0{,}35, 0{,}82, 0{,}45, -0{,}10, 0{,}65, 0{,}00, -0{,}22, 0{,}78]^T \in \mathbb{R}^9$.

6. **Retrieval MLP (6)**
   - **Fungsi**: Memetakan representasi sembilan dimensi analog historis ke dalam ruang *embedding* kondisi.
   - **Masukan**: Vektor $\mathbf{r}_{flat} \in \mathbb{R}^9$.
   - **Keluaran**: Vektor kondisi retrieval $\mathbf{h}_t^R \in \mathbb{R}^{64}$.
   - **Rumus**:
     $$
     \mathbf{h}_t^R = \mathbf{W}_{R2} \cdot \text{SiLU}(\mathbf{W}_{R1}\mathbf{r}_{flat} + \mathbf{b}_{R1}) + \mathbf{b}_{R2} \in \mathbb{R}^{64}
     \tag{3.17}
     $$
     di mana $\mathbf{W}_{R1} \in \mathbb{R}^{64 \times 9}$, $\mathbf{b}_{R1} \in \mathbb{R}^{64}$, $\mathbf{W}_{R2} \in \mathbb{R}^{64 \times 64}$, dan $\mathbf{b}_{R2} \in \mathbb{R}^{64}$.
   - *Contoh pemakaian rumus:* Vektor $\mathbf{r}_{flat} \in \mathbb{R}^9$ dipetakan oleh $\mathbf{W}_{R1}$, dikenakan fungsi SiLU, lalu diproyeksikan oleh $\mathbf{W}_{R2}$ menghasilkan vektor kondisi retrieval $\mathbf{h}_t^R = [0{,}310, 0{,}092, \dots, -0{,}241]^T \in \mathbb{R}^{64}$.

7. **Condition Embedding (7)**
   - **Fungsi**: Menggabungkan seluruh informasi lingkungan atmosfer (graf, konteks lokal, dan retrieval) secara aditif.
   - **Masukan**: Tiga vektor kondisi $\mathbf{h}_t^G, \mathbf{h}_t^{\text{MAIN}}, \mathbf{h}_t^R \in \mathbb{R}^{64}$.
   - **Keluaran**: Vektor kondisi total atmosfer $\mathbf{c}_t \in \mathbb{R}^{64}$.
   - **Rumus**:
     $$
     \mathbf{c}_t = \mathbf{h}_t^G + \mathbf{h}_t^{\text{MAIN}} + \mathbf{h}_t^R \in \mathbb{R}^{64}
     \tag{3.18}
     $$
   - *Contoh perhitungan:* Penjumlahan elemen pertama dari ketiga vektor kondisi: $c_{t, 1} = 0{,}145 + (-0{,}421) + 0{,}310 = 0{,}034$. Dilakukan pada seluruh 64 dimensi, menghasilkan vektor kondisi lengkap $\mathbf{c}_t \in \mathbb{R}^{64}$.

8. **Diffusion Timestep (8)**
   - **Fungsi**: Menentukan tingkat intensitas *noise* stokastik pada iterasi pelatihan *diffusion*.
   - **Masukan**: Pembangkitan acak seragam $s \sim \mathcal{U}(\{0, 1, \dots, T_{train}-1\})$ dengan $T_{train} = 1000$.
   - **Keluaran**: Skalar integer $s \in [0, 999]$.
   - *Contoh data konkret:* Nilai langkah *diffusion* terpilih $s = 400$ (atau tensor indeks $[B]$ bernilai integer antara 0 dan 999).

9. **Time MLP (9)**
   - **Fungsi**: Mengonversi langkah waktu *diffusion* integer $s$ menjadi representasi kontinu berdimensi 64.
   - **Masukan**: Langkah waktu *diffusion* $s \in \mathbb{R}^1$.
   - **Keluaran**: Vektor *time embedding* $\mathbf{h}_s^{time} \in \mathbb{R}^{64}$.
   - **Rumus**:
     $$
     \mathbf{e}_s = \left[ \sin\left(\frac{s}{10000^{2k/64}}\right), \cos\left(\frac{s}{10000^{2k/64}}\right) \right]_{k=0}^{31} \in \mathbb{R}^{64}
     \tag{3.19}
     $$
     $$
     \mathbf{h}_s^{time} = \mathbf{W}_{T2} \cdot \text{GELU}(\mathbf{W}_{T1}\mathbf{e}_s + \mathbf{b}_{T1}) + \mathbf{b}_{T2} \in \mathbb{R}^{64}
     \tag{3.20}
     $$
     di mana $\mathbf{W}_{T1} \in \mathbb{R}^{128 \times 64}$, $\mathbf{b}_{T1} \in \mathbb{R}^{128}$, $\mathbf{W}_{T2} \in \mathbb{R}^{64 \times 128}$, dan $\mathbf{b}_{T2} \in \mathbb{R}^{64}$.
   - *Contoh perhitungan:* Untuk $s = 400$, perhitungan fungsi sinus dan kosinus pada 32 frekuensi geometris menghasilkan $\mathbf{e}_{400} \in \mathbb{R}^{64}$. Proyeksi ke 128 dimensi dengan aktivasi GELU dan proyeksi balik ke 64 dimensi menghasilkan $\mathbf{h}_{400}^{time} = [0{,}512, -0{,}188, \dots, 0{,}401]^T \in \mathbb{R}^{64}$.

10. **Total Embedding (10)**
    - **Fungsi**: Menyatukan representasi atmosferik dan *time embedding* langkah *diffusion* sebagai vektor *conditioning* total.
    - **Masukan**: $\mathbf{c}_t \in \mathbb{R}^{64}$ dan $\mathbf{h}_s^{time} \in \mathbb{R}^{64}$.
    - **Keluaran**: Vektor *total conditioning* $\mathbf{c}_t^{total} \in \mathbb{R}^{64}$.
    - **Rumus**:
      $$
      \mathbf{c}_t^{total} = \mathbf{c}_t + \mathbf{h}_s^{time} \in \mathbb{R}^{64}
      \tag{3.21}
      $$
    - *Contoh perhitungan:* Penjumlahan elemen pertama: $c_{t, 1}^{total} = 0{,}034 + 0{,}512 = 0{,}546$, menghasilkan $\mathbf{c}_t^{total} \in \mathbb{R}^{64}$.

11. **Denoiser Input / Noisy Target (11)**
    - **Fungsi**: Membentuk masukan target *noisy* (*noisy target*) pada *timestep* $s$ melalui proses *forward diffusion*.
    - **Masukan**: Target bersih $\mathbf{y}_0 \in \mathbb{R}^3$, *Gaussian noise* $\boldsymbol{\epsilon} \in \mathbb{R}^3$, dan jadwal varians (*noise variance schedule*) $\bar{\alpha}_s$.
    - **Keluaran**: Vektor *noisy target* $\mathbf{y}_s \in \mathbb{R}^3$.
    - **Rumus**:
      $$
      \mathbf{y}_s = \sqrt{\bar{\alpha}_s}\mathbf{y}_0 + \sqrt{1 - \bar{\alpha}_s}\boldsymbol{\epsilon} \in \mathbb{R}^3
      \tag{3.22}
      $$
      di mana $\mathbf{y}_0 = [y_{\text{precip}}, y_{\text{wind}}, y_{\text{humid}}]^T \in \mathbb{R}^3$ adalah target cuaca bersih ternormalisasi pada waktu $t$, dan $\bar{\alpha}_s = \prod_{i=1}^s (1 - \beta_i)$ merupakan koefisien kumulatif *noise schedule* DDPM.
    - *Contoh perhitungan:* Untuk $\mathbf{y}_0 = [1{,}20, -0{,}50, 0{,}80]^T$, vektor *noise* $\boldsymbol{\epsilon} = [-0{,}30, 1{,}10, -0{,}40]^T$, dan koefisien $\bar{\alpha}_{400} = 0{,}64$ ($\sqrt{\bar{\alpha}_{400}} = 0{,}80$, $\sqrt{1-\bar{\alpha}_{400}} = 0{,}60$):
      $$
      \mathbf{y}_{400} = 0{,}80 \begin{bmatrix} 1{,}20 \\ -0{,}50 \\ 0{,}80 \end{bmatrix} + 0{,}60 \begin{bmatrix} -0{,}30 \\ 1{,}10 \\ -0{,}40 \end{bmatrix} = \begin{bmatrix} 0{,}78 \\ 0{,}26 \\ 0{,}40 \end{bmatrix} \in \mathbb{R}^3
      $$

12. **Down1 (12)**
    - **Fungsi**: Mereduksi target 3 dimensi ke dimensi tersembunyi 64 dan menginjeksikan vektor kondisi total $\mathbf{c}_t^{total}$.
    - **Masukan**: *Noisy target* $\mathbf{y}_s \in \mathbb{R}^3$ dan vektor *conditioning* $\mathbf{c}_t^{total} \in \mathbb{R}^{64}$.
    - **Keluaran**: Vektor representasi $\mathbf{h}_1 \in \mathbb{R}^{64}$.
    - **Rumus**:
      $$
      \mathbf{h}_1 = \text{SiLU}(\mathbf{W}_{d1}\mathbf{y}_s + \mathbf{b}_{d1}) + \mathbf{c}_t^{total} \in \mathbb{R}^{64}
      \tag{3.23}
      $$
      di mana $\mathbf{W}_{d1} \in \mathbb{R}^{64 \times 3}$ dan $\mathbf{b}_{d1} \in \mathbb{R}^{64}$.
    - *Contoh perhitungan:* Vektor $\mathbf{y}_{400} \in \mathbb{R}^3$ ditransformasikan oleh $\mathbf{W}_{d1}$ menghasilkan representasi 64 dimensi, dikenakan SiLU, lalu dijumlahkan dengan $\mathbf{c}_t^{total} \in \mathbb{R}^{64}$ menghasilkan $\mathbf{h}_1 \in \mathbb{R}^{64}$.

13. **Down2 (13)**
    - **Fungsi**: Memperluas kapasitas representasi fitur tersembunyi denoiser ke dimensi yang lebih tinggi.
    - **Masukan**: Vektor $\mathbf{h}_1 \in \mathbb{R}^{64}$.
    - **Keluaran**: Vektor representasi $\mathbf{h}_2 \in \mathbb{R}^{128}$.
    - **Rumus**:
      $$
      \mathbf{h}_2 = \text{SiLU}(\mathbf{W}_{d2}\mathbf{h}_1 + \mathbf{b}_{d2}) \in \mathbb{R}^{128}
      \tag{3.24}
      $$
      di mana $\mathbf{W}_{d2} \in \mathbb{R}^{128 \times 64}$ dan $\mathbf{b}_{d2} \in \mathbb{R}^{128}$.
    - *Contoh perhitungan:* Lapisan linier $\mathbb{R}^{64 \to 128}$ dengan aktivasi SiLU menghasilkan $\mathbf{h}_2 = [0{,}812, -0{,}114, \dots, 0{,}455]^T \in \mathbb{R}^{128}$.

14. **Skip Connection (14)**
    - **Fungsi**: Menyalurkan salinan fitur $\mathbf{h}_2$ secara langsung ke tahap penggabungan akhir untuk menjaga informasi spasial/resolusi.
    - **Masukan**: Vektor $\mathbf{h}_2 \in \mathbb{R}^{128}$.
    - **Keluaran**: Salinan identitas tensor $\mathbf{h}_2 \in \mathbb{R}^{128}$.
    - *Contoh pemakaian tensor:* Tensor $\mathbf{h}_2$ ditahan pada memori untuk dihubungkan ke blok *Concatenate*.

15. **Mid Layer (15)**
    - **Fungsi**: Lapisan pemrosesan laten tingkat tinggi (*bottleneck layer*).
    - **Masukan**: Vektor $\mathbf{h}_2 \in \mathbb{R}^{128}$.
    - **Keluaran**: Vektor representasi tengah $\mathbf{h}_{mid} \in \mathbb{R}^{128}$.
    - **Rumus**:
      $$
      \mathbf{h}_{mid} = \text{SiLU}(\mathbf{W}_{mid}\mathbf{h}_2 + \mathbf{b}_{mid}) \in \mathbb{R}^{128}
      \tag{3.25}
      $$
      di mana $\mathbf{W}_{mid} \in \mathbb{R}^{128 \times 128}$ dan $\mathbf{b}_{mid} \in \mathbb{R}^{128}$.
    - *Contoh perhitungan:* Pemrosesan menghasilkan $\mathbf{h}_{mid} = [-0{,}215, 0{,}670, \dots, 0{,}102]^T \in \mathbb{R}^{128}$.

16. **Concatenate (16)**
    - **Fungsi**: Menggabungkan representasi lapisan *bottleneck* (*mid layer*) dengan fitur *skip connection*.
    - **Masukan**: $\mathbf{h}_{mid} \in \mathbb{R}^{128}$ dan $\mathbf{h}_2 \in \mathbb{R}^{128}$.
    - **Keluaran**: Vektor gabungan $\mathbf{h}_{up} \in \mathbb{R}^{256}$.
    - **Rumus**:
      $$
      \mathbf{h}_{up} = [\mathbf{h}_{mid} \,\|\, \mathbf{h}_2] \in \mathbb{R}^{256}
      \tag{3.26}
      $$
    - *Contoh perhitungan:* Dua vektor 128 dimensi digabungkan menghasilkan satu vektor $\mathbf{h}_{up} \in \mathbb{R}^{256}$.

17. **Up MLP (17)**
    - **Fungsi**: Merekonstruksi dan memproyeksikan fitur gabungan kembali ke dimensi target fisik 3 variabel.
    - **Masukan**: Vektor gabungan $\mathbf{h}_{up} \in \mathbb{R}^{256}$.
    - **Keluaran**: Vektor estimasi *noise* (*predicted noise*) $\hat{\boldsymbol{\epsilon}}_\theta \in \mathbb{R}^3$.
    - **Rumus**:
      $$
      \hat{\boldsymbol{\epsilon}}_\theta = \mathbf{W}_{u2} \cdot \text{SiLU}(\mathbf{W}_{u1}\mathbf{h}_{up} + \mathbf{b}_{u1}) + \mathbf{b}_{u2} \in \mathbb{R}^3
      \tag{3.27}
      $$
      di mana $\mathbf{W}_{u1} \in \mathbb{R}^{64 \times 256}$, $\mathbf{b}_{u1} \in \mathbb{R}^{64}$, $\mathbf{W}_{u2} \in \mathbb{R}^{3 \times 64}$, dan $\mathbf{b}_{u2} \in \mathbb{R}^3$.
    - *Contoh perhitungan:* Vektor 256 dimensi diproyeksikan ke 64 dimensi lalu ke 3 dimensi menghasilkan $\hat{\boldsymbol{\epsilon}}_\theta \in \mathbb{R}^3$.

18. **Predicted Noise (18)**
    - **Fungsi**: Estimasi *Gaussian noise* yang diprediksi oleh jaringan *denoiser*.
    - **Masukan**: Keluaran (*output*) rekonstruksi dari *Up MLP*.
    - **Keluaran**: Vektor estimasi *noise* $\hat{\boldsymbol{\epsilon}}_\theta = [\hat{\epsilon}_1, \hat{\epsilon}_2, \hat{\epsilon}_3]^T \in \mathbb{R}^3$.
    - *Contoh data konkret:* $\hat{\boldsymbol{\epsilon}}_\theta = [-0{,}284, 1{,}052, -0{,}391]^T \in \mathbb{R}^3$.

19. **Target Ground Truth (19)**
    - **Fungsi**: Menyediakan data observasi aktual 3 variabel cuaca ternormalisasi sebagai acuan pembobotan penalti ekstrem.
    - **Masukan**: Nilai observasi aktual target `MAIN` pada waktu $t$.
    - **Keluaran**: Vektor target bersih $\mathbf{y}_0 \in \mathbb{R}^3$.
    - *Contoh data konkret:* Target aktual $\mathbf{y}_0 = [1{,}20, -0{,}50, 0{,}80]^T \in \mathbb{R}^3$.

20. **Gaussian Noise (20)**
    - **Fungsi**: *Gaussian noise* baku yang dibangkitkan sebagai target acuan (*ground truth noise*).
    - **Masukan**: Sampel dari distribusi normal standar $\mathcal{N}(\mathbf{0}, \mathbf{I})$.
    - **Keluaran**: Vektor *Gaussian noise* $\boldsymbol{\epsilon} \in \mathbb{R}^3$.
    - *Contoh data konkret:* $\boldsymbol{\epsilon} = [-0{,}300, 1{,}100, -0{,}400]^T \in \mathbb{R}^3$.

21. **Weighted Noise Loss (21)**
    - **Fungsi**: Menghitung penalti *loss* kuadratik terbobot (*weighted noise loss*) antara *ground truth noise* $\boldsymbol{\epsilon}$ dan prediksi *noise* $\hat{\boldsymbol{\epsilon}}_\theta$ dengan bobot ekstra untuk kejadian ekstrem.
    - **Masukan**: Prediksi *noise* $\hat{\boldsymbol{\epsilon}}_\theta \in \mathbb{R}^3$, *ground truth noise* $\boldsymbol{\epsilon} \in \mathbb{R}^3$, dan target acuan $\mathbf{y}_0 \in \mathbb{R}^3$.
    - **Keluaran**: Nilai skalar $L_{noise} \in \mathbb{R}^+$.
    - **Rumus**:
      $$
      w_i = \begin{cases}
      10{,}0, & |y_{0,i}| > 3{,}0 \\
      5{,}0, & 1{,}0 < |y_{0,i}| \le 3{,}0 \\
      1{,}0, & |y_{0,i}| \le 1{,}0
      \end{cases}
      \tag{3.28}
      $$
      $$
      L_{noise} = \frac{1}{3} \sum_{i=1}^3 w_i (\hat{\epsilon}_{\theta, i} - \epsilon_i)^2
      \tag{3.29}
      $$
    - *Contoh perhitungan:* Untuk target $[1{,}20, -0{,}50, 0{,}80]^T$, bobot $\mathbf{w} = [5{,}0, 1{,}0, 1{,}0]^T$. Galat kuadrat per elemen: $(\hat{\epsilon}_1 - \epsilon_1)^2 = (-0{,}284 - (-0{,}300))^2 = 0{,}016^2 = 0{,}000256$; $(\hat{\epsilon}_2 - \epsilon_2)^2 = (1{,}052 - 1{,}100)^2 = (-0{,}048)^2 = 0{,}002304$; $(\hat{\epsilon}_3 - \epsilon_3)^2 = (-0{,}391 - (-0{,}400))^2 = 0{,}009^2 = 0{,}000081$. Perhitungan *loss*:
      $$
      L_{noise} = \frac{1}{3} [ 5{,}0(0{,}000256) + 1{,}0(0{,}002304) + 1{,}0(0{,}000081) ] = \frac{0{,}001280 + 0{,}002304 + 0{,}000081}{3} \approx 0{,}001222
      $$

22. **Auxiliary Wet Head (22)**
    - **Fungsi**: Memprediksi *logit* biner ada/tidaknya hujan dari representasi kondisi atmosfer $\mathbf{c}_t$.
    - **Masukan**: Vektor $\mathbf{c}_t \in \mathbb{R}^{64}$.
    - **Keluaran**: Skalar logit $z_{wet} \in \mathbb{R}^1$ dan peluang hujan $p_{wet} = \sigma(z_{wet}) \in [0, 1]$.
    - **Rumus**:
      $$
      z_{wet} = \mathbf{w}_{w2}^T \cdot \text{SiLU}(\mathbf{W}_{w1}\mathbf{c}_t + \mathbf{b}_{w1}) + b_{w2} \in \mathbb{R}^1
      \tag{3.30}
      $$
      di mana $\mathbf{W}_{w1} \in \mathbb{R}^{64 \times 64}$, $\mathbf{b}_{w1} \in \mathbb{R}^{64}$, $\mathbf{w}_{w2} \in \mathbb{R}^{64}$, dan $b_{w2} \in \mathbb{R}$.
    - *Contoh perhitungan:* Vektor $\mathbf{c}_t$ menghasilkan logit $z_{wet} = 1{,}85$. Peluang hujan terprediksi adalah $p_{wet} = \sigma(1{,}85) = \frac{1}{1 + e^{-1{,}85}} \approx 0{,}864$ ($86{,}4\%$).

23. **Auxiliary Wet Loss (23)**
    - **Fungsi**: Menghitung penalti biner terbobot (*pos_weight*) untuk menajamkan pemisahan kondisi kering vs basah (*zero-inflated*).
    - **Masukan**: Logit $z_{wet}$ dan label biner hujan aktual $y_{wet} = \mathbb{I}(\text{curah hujan} \ge 0{,}1\text{ mm/jam}) \in \{0, 1\}$.
    - **Keluaran**: Nilai skalar $L_{wet} \in \mathbb{R}^+$.
    - **Rumus**:
      $$
      L_{wet} = - \left[ w_{pos} \cdot y_{wet} \log(\sigma(z_{wet})) + (1 - y_{wet}) \log(1 - \sigma(z_{wet})) \right]
      \tag{3.31}
      $$
      di mana $y_{wet} = \mathbb{I}(\text{curah hujan aktual} \ge 0{,}1\text{ mm/jam}) \in \{0, 1\}$, dan $w_{pos} = \frac{N_{kering}}{N_{hujan}}$ yang dihitung dari data latih ($w_{pos} \approx 3{,}2$).
    - *Contoh perhitungan:* Jika target aktual adalah hujan ($y_{wet} = 1$) dan $p_{wet} = 0{,}864$:
      $$
      L_{wet} = - [ 3{,}2 \cdot 1 \cdot \log(0{,}864) ] = - [ 3{,}2 \cdot (-0{,}146) ] \approx 0{,}467
      $$

24. **Total Training Loss (24)**
    - **Fungsi**: Menggabungkan fungsi *loss* *diffusion* dan fungsi *loss* klasifikasi presipitasi menjadi objektif optimasi tunggal.
    - **Masukan**: $L_{noise}$ dan $L_{wet}$ dengan bobot $\lambda_{wet} = 0{,}7$.
    - **Keluaran**: Nilai skalar $L_{total} \in \mathbb{R}^+$.
    - **Rumus**:
      $$
      L_{total} = L_{noise} + \lambda_{wet} L_{wet}
      \tag{3.32}
      $$
    - *Contoh perhitungan:* Untuk nilai $L_{noise} = 0{,}001222$ dan $L_{wet} = 0{,}467$:
      $$
      L_{total} = 0{,}001222 + (0{,}7 \times 0{,}467) = 0{,}001222 + 0{,}326900 = 0{,}328122
      $$

25. **Backpropagation (25)**
    - **Fungsi**: Menghitung gradien otomatis, memotong gradien ekstrem ($\le 1{,}0$), dan memperbarui seluruh bobot model $\theta$ secara *end-to-end*.
    - **Masukan**: Nilai skalar $L_{total}$ dan parameter jaringan $\theta = \{\theta_{\text{STGNN}}, \theta_{\text{diff}}\}$.
    - **Keluaran**: Parameter jaringan $\theta$ yang diperbarui.
    - **Rumus**:
      $$
      \mathbf{g} = \nabla_\theta L_{total}
      \tag{3.33}
      $$
      $$
      \tilde{\mathbf{g}} = \mathbf{g} \cdot \min\left(1, \frac{1{,}0}{\|\mathbf{g}\|_2}\right)
      \tag{3.34}
      $$
      $$
      \theta \leftarrow \theta - \eta \cdot \text{AdamW}(\tilde{\mathbf{g}})
      \tag{3.35}
      $$
    - *Contoh perhitungan:* Jika norma gradien $\|\mathbf{g}\|_2 = 2{,}5$, faktor pemotongan adalah $\frac{1{,}0}{2{,}5} = 0{,}4$, sehingga vektor gradien diskalakan menjadi $\tilde{\mathbf{g}} = 0{,}4\mathbf{g}$ sebelum parameter $\theta$ diperbarui menggunakan *optimizer* AdamW ($\eta = 10^{-3}$, *weight decay* $10^{-4}$).

---

Rincian alur transformasi tensor, ukuran dimensi, modul PyTorch terkait, dan fungsi komputasi pada integrasi model *diffusion* terangkum secara sistematis pada Tabel 3.15.

**Tabel 3.15 Rincian Alur Transformasi Tensor pada Komponen Integrasi Diffusion**

| No. | Nama Komponen | Modul / Operasi PyTorch | Dimensi Masukan | Dimensi Keluaran | Keterangan Pemrosesan |
|---:|---|---|---|---|---|
| 1 | Output STGNN | `SpatioTemporalGNN` | $6 \times [5, 9]$ | $[B, 64]$ | Representasi graf spasio-temporal |
| 2 | Graph MLP | `nn.Sequential(Linear(64,64), SiLU, Linear(64,64))` | $[B, 64]$ | $[B, 64]$ | Pemetaan kondisi graf ke ruang laten |
| 3 | Context Input | `x_main[:, -1, :]` | $[B, 9]$ | $[B, 9]$ | Fitur cuaca node `MAIN` pada $t-1$ |
| 4 | Context MLP | `nn.Sequential(Linear(9,64), SiLU, Linear(64,64))` | $[B, 9]$ | $[B, 64]$ | Pemetaan kondisi cuaca lokal mutakhir |
| 5 | Retrieval Input | `retrieval_values.reshape(B, -1)` | $[B, 3, 3]$ | $[B, 9]$ | Target $t+1$ dari top-3 analog historis |
| 6 | Retrieval MLP | `nn.Sequential(Linear(9,64), SiLU, Linear(64,64))` | $[B, 9]$ | $[B, 64]$ | Pemetaan prior pola analog masa lalu |
| 7 | Condition Embedding | Penjumlahan elemen ($\mathbf{h}_t^G + \mathbf{h}_t^{\text{MAIN}} + \mathbf{h}_t^R$) | $3 \times [B, 64]$ | $[B, 64]$ | Penggabungan ketiga kondisi lingkungan |
| 8 | Diffusion Timestep | `torch.randint(0, 1000, (B,))` | Skalar integer | $[B]$ | Indeks langkah *diffusion* stokastik |
| 9 | Time MLP | `SinusoidalPosEmb(64)` + `Linear(64,128)` + `Linear(128,64)` | $[B]$ | $[B, 64]$ | *Sinusoidal positional embedding* waktu *diffusion* |
| 10 | Total Embedding | Penjumlahan elemen ($\mathbf{c}_t + \mathbf{h}_s^{time}$) | $2 \times [B, 64]$ | $[B, 64]$ | Vektor *conditioning* total atmosfer dan waktu |
| 11 | Denoiser Input | Forward Diffusion `scheduler.add_noise` | $[B, 3]$ | $[B, 3]$ | Target 3 variabel yang diinjeksi *noise* (*noisy target*) |
| 12 | Down1 | `Linear(3, 64)` + `SiLU` + $\mathbf{c}_t^{total}$ | $[B, 3]$ | $[B, 64]$ | Reduksi pertama + injeksi *conditioning* total |
| 13 | Down2 | `Linear(64, 128)` + `SiLU` | $[B, 64]$ | $[B, 128]$ | Ekspansi representasi fitur laten |
| 14 | Skip Connection | *Identity mapping* | $[B, 128]$ | $[B, 128]$ | *Skip connection* resolusi fitur perantara |
| 15 | Mid Layer | `Linear(128, 128)` + `SiLU` | $[B, 128]$ | $[B, 128]$ | Transformasi representasi laten *bottleneck* |
| 16 | Concatenate | `torch.cat([h_mid, h2], dim=-1)` | $2 \times [B, 128]$ | $[B, 256]$ | Penggabungan *bottleneck* dan *skip connection* |
| 17 | Up MLP | `Linear(256, 64)` + `SiLU` + `Linear(64, 3)` | $[B, 256]$ | $[B, 3]$ | Proyeksi balik ke dimensi target |
| 18 | Predicted Noise | Keluaran *denoiser* $\hat{\boldsymbol{\epsilon}}_\theta$ | $[B, 256]$ | $[B, 3]$ | Estimasi *noise* 3 variabel cuaca |
| 19 | Target GT | `targets` ($\mathbf{y}_0$) | $[B, 3]$ | $[B, 3]$ | Target observasi aktual ternormalisasi |
| 20 | Gaussian Noise | `torch.randn_like(targets)` | $[B, 3]$ | $[B, 3]$ | *Gaussian noise* standar acuan |
| 21 | Weighted Noise Loss | `RainForecaster.weighted_noise_loss` | $2 \times [B, 3]$ | Skalar | MSE terbobot penalti ekstrem |
| 22 | Auxiliary Wet Head | `Linear(64, 64)` + `SiLU` + `Linear(64, 1)` | $[B, 64]$ | $[B, 1]$ | Logit klasifikasi kejadian hujan |
| 23 | Auxiliary Wet Loss | `BCEWithLogitsLoss(pos_weight)` | $[B, 1]$ | Skalar | Klasifikasi penanganan *zero-inflation* |
| 24 | Total Loss | $L_{noise} + 0{,}7 L_{wet}$ | 2 Skalar | Skalar | Fungsi objektif pelatihan terpadu |
| 25 | Backpropagation | `optimizer.step()` via AdamW | Skalar | Parameter | Pembaruan parameter dengan *gradient clipping* ($\le 1{,}0$) |

### 3.6.3 Integrasi End-to-End Model

Secara keseluruhan, satu sampel prediksi dibentuk melalui urutan berikut:

1. mengambil enam snapshot graf dari `t-6` hingga `t-1`;
2. mengambil konteks `MAIN` pada `t-1`;
3. membentuk embedding graf melalui STGNN;
4. mencari tiga analog historis;
5. membentuk embedding graf, konteks, retrieval, dan waktu;
6. menggabungkan embedding menjadi embedding total;
7. memberi noise pada target tiga variabel;
8. memperkirakan noise melalui MLP denoiser;
9. menjalankan reverse diffusion;
10. mengembalikan sampel ke skala asli dan menerapkan batas fisik.

## 3.7 Pelatihan dan Pembentukan Prediksi

### 3.7.1 Prosedur Pelatihan

Pelatihan menggunakan sampel dengan enam snapshot historis. Pada setiap sampel, urutan graf (*graph sequence*) berasal dari `t-6` hingga `t-1`, konteks berasal dari `MAIN` pada `t-1`, dan target berasal dari `MAIN` pada `t`. Hanya target yang diberi noise; fitur graf, konteks, dan retrieval tidak diberi noise.

Bentuk satu sampel yang masuk ke proses pelatihan diringkas sebagai berikut:

```text
Graph sequence : 6 timestamp × 5 node × 10 fitur
Konteks        : 9 fitur MAIN pada t−1
Retrieval      : 3 analog historis × 3 variabel target
Target         : 3 variabel MAIN pada t
```

Dengan susunan tersebut, enam snapshot graf digunakan untuk menangkap kondisi spasial-temporal historis. Konteks `MAIN` dan tiga analog historis digunakan sebagai informasi tambahan, sedangkan target tiga variabel pada `MAIN` menjadi nilai yang dipelajari model. Sampel-sampel tersebut kemudian dikelompokkan ke dalam *batch* untuk memperbarui parameter model.

Noise Gaussian diambil dengan dimensi yang sama dengan target. Timestep diffusion `s` dipilih pada rentang 0 hingga 999. Scheduler DDPM (*Denoising Diffusion Probabilistic Model*) kemudian membentuk *noisy target* menggunakan Persamaan 3.22. Denoiser dilatih untuk memperkirakan *noise* yang ditambahkan. Pada saat inferensi, DDIM (*Denoising Diffusion Implicit Model*) digunakan sebagai *scheduler* proses *sampling* dengan 20 langkah.

### 3.7.2 Fungsi Loss

Fungsi *loss noise* menggunakan bobot berdasarkan besar target ternormalisasi sebagaimana dirumuskan pada Persamaan 3.28 dan 3.29. Model juga memiliki cabang keluaran tambahan untuk klasifikasi hujan/tidak hujan (*auxiliary wet/dry head*) dengan *loss* $L_{wet}$ pada Persamaan 3.31. Fungsi *loss* total yang dioptimalkan dirumuskan kembali sebagai:

$$
L_{total}=L_{noise}+0,7L_{wet}
\tag{3.36}
$$

Nilai `0,7` merupakan bobot fungsi *loss* klasifikasi hujan/tidak hujan dalam konfigurasi penelitian. Mekanisme *gradient clipping* digunakan untuk membatasi norma gradien sebelum pembaruan parameter (Persamaan 3.34). Optimizer AdamW memperbarui parameter berdasarkan fungsi *loss* total tersebut.

### 3.7.3 Konfigurasi Pelatihan

Parameter hiperparameter dan pengaturan komputasi pelatihan model dirangkum pada Tabel 3.16.

**Tabel 3.16 Konfigurasi Pelatihan Model**

| Parameter | Nilai |
|---|---:|
| Optimizer | AdamW |
| Weight decay | `1e-4` |
| Learning rate awal | `0,001` |
| Batch size | `512` |
| Epoch maksimum | `20` |
| Early stopping patience | `12` |
| Lookback window | `6` jam |
| FAISS neighbors | `3` |
| Diffusion train steps | `1000` |
| Conditioning dropout | `0,15` |
| Ambang klasifikasi hujan/tidak hujan | `0,1 mm/jam` |
| Bobot fungsi loss klasifikasi hujan/tidak hujan | `0,7` |
| Gradient clipping | `1,0` |
| Seed | `1` |

Tabel 3.16 merangkum parameter yang menjaga konsistensi proses pelatihan dan evaluasi. Jendela historis (*lookback window*) menetapkan enam jam masukan, jumlah tetangga FAISS menetapkan tiga analog historis, dan jumlah langkah *diffusion* saat pelatihan (*diffusion train steps*) ditetapkan sebanyak 1000. Ambang dan bobot fungsi loss klasifikasi hujan/tidak hujan mengatur kontribusi cabang tambahan terhadap fungsi loss total. Statistik normalisasi dan basis retrieval dihitung dari data training. Checkpoint dipilih berdasarkan perkembangan data validation. Satu *seed* digunakan dalam rancangan ini; karena itu, hasil perbandingan harus ditafsirkan sebagai hasil satu konfigurasi *seed*.

### 3.7.4 Pembentukan Prediksi

Pada proses inferensi, model menghasilkan beberapa sampel menggunakan reverse diffusion. Protokol evaluasi menggunakan 30 sampel ensemble dan DDIM dengan 20 langkah. Saat inferensi aplikasi, jumlah sampel dapat diatur sesuai kebutuhan komputasi; hasil evaluasi utama dalam penelitian ini menggunakan 30 sampel agar setiap skenario dibandingkan dengan jumlah sampel yang sama. Setiap sampel memakai masukan enam jam historis untuk memprediksi kondisi `MAIN` satu jam berikutnya. Sampel-sampel tersebut digunakan untuk membentuk prediksi titik dan mengukur ketidakpastian prediksi.

### 3.7.5 Post-processing Prediksi

Setelah proses *sampling* selesai, prediksi dikembalikan ke skala asli menggunakan denormalisasi Z-score. Pembalikan Z-score dilakukan dengan:

$$
v=z(\sigma+10^{-5})+\mu
\tag{3.37}
$$

Untuk curah hujan, pembalikan `log1p` dilakukan dengan:

$$
y=\exp(v)-1
\tag{3.38}
$$

Contoh pembalikan skala curah hujan ditunjukkan sebagai berikut. Jika nilai Z-score adalah `-0,479`, maka:

$$
v=(-0,479)(0,368494+0,00001)+0,176636\approx0
$$

Nilai tersebut kemudian dikembalikan dari transformasi `log1p`:

$$
y=\exp(0)-1=0\text{ mm}
$$

Dengan demikian, nilai `-0,479` adalah nilai standar untuk diproses model, bukan curah hujan `-0,479 mm`. Dalam implementasi, operasi terakhir dapat dilakukan menggunakan `expm1`. Setelah itu, batas fisik diterapkan: curah hujan dibatasi pada rentang `0–60 mm/jam`, kecepatan angin tidak boleh negatif, dan kelembapan relatif dibatasi pada rentang `0–100%`.

Mekanisme *rain gate* digunakan pada saat inferensi model utama. Gerbang (*gate*) ini dihitung dari probabilitas klasifikasi hujan/tidak hujan yang telah dikalibrasi pada data validation, kemudian diterapkan setelah seluruh lintasan sampel dibentuk. Jika probabilitas hujan pada suatu jendela berada di bawah ambang `0,6`, komponen curah hujan pada jendela tersebut diatur menjadi `0`; kecepatan angin dan kelembapan relatif tidak diubah. Jika seluruh jendela inferensi memiliki probabilitas di bawah ambang tersebut, *rain gate* tidak diterapkan untuk mencegah keluaran hujan selalu bernilai nol.

## 3.8 Evaluasi Model

### 3.8.1 Protokol Evaluasi

Evaluasi menggunakan prediksi satu langkah ke depan (*one-step-ahead forecast*). Untuk setiap target pada waktu `t`, model menggunakan enam jam historis dari `t-6` sampai `t-1` untuk memprediksi kondisi `MAIN` pada `t`. Evaluasi utama dilakukan pada data test yang tidak digunakan dalam pelatihan atau pemilihan checkpoint. Pengambilan sampel evaluasi dilakukan setiap jam (`eval_step=1`) sehingga tidak ada timestamp test yang dilewati karena subsampling. Horizon prediksi tetap satu jam; `eval_step` hanya mengatur jarak pengambilan sampel evaluasi.

### 3.8.2 Evaluasi Prediksi Titik

Prediksi titik dihitung dari median ensemble. Metrik yang digunakan adalah MAE, RMSE, dan koefisien korelasi Pearson. Rumus telah dijelaskan pada Bab II dan diterapkan setelah prediksi dikembalikan ke skala asli [53], [55].

### 3.8.3 Evaluasi Prediksi Probabilistik

Evaluasi probabilistik menggunakan seluruh anggota ensemble. CRPS digunakan untuk menilai kedekatan distribusi prediksi terhadap target, sedangkan Brier Score digunakan untuk menilai probabilitas kejadian pada ambang tertentu. Probabilitas kejadian dihitung dari proporsi anggota ensemble yang melampaui ambang curah hujan. Untuk model yang hanya menghasilkan satu prediksi, ensemble diperlakukan sebagai satu anggota; kondisi ini tidak mengukur penyebaran probabilistik [53], [54].

### 3.8.4 Evaluasi Berbasis Kejadian

Kejadian hujan dievaluasi pada ambang `2`, `5`, dan `10 mm/jam`. Probabilitas kejadian dihitung dari proporsi anggota ensemble yang melebihi ambang tersebut. Suatu kejadian diprediksi terjadi apabila probabilitasnya sekurang-kurangnya `0,5`; jika kurang dari `0,5`, kejadian dianggap tidak diprediksi. POD, FAR, CSI, dan Brier Score kemudian dihitung dari hasil tersebut [53]–[55].

Ambang klasifikasi hujan/tidak hujan `0,1 mm/jam` pada cabang keluaran tambahan digunakan untuk membentuk label pelatihan. Ambang probabilitas `0,5` digunakan khusus untuk mengubah probabilitas ensemble menjadi keputusan kejadian pada evaluasi. Keduanya berbeda dari ambang *rain gate* `0,6` yang dikalibrasi pada data validation dan digunakan setelah proses *sampling* model utama.

### 3.8.5 Evaluasi Reliabilitas Probabilitas

*Reliability diagram* dibuat untuk model utama pada ambang curah hujan `2 mm/jam` menggunakan 10 bin probabilitas. Diagram membandingkan probabilitas kejadian hujan yang diperkirakan dengan frekuensi kejadian aktual pada data test ERA5. Hasilnya digunakan untuk menilai apakah probabilitas yang diberikan model sesuai dengan frekuensi kejadian yang diamati; diagram ini tidak mewakili ambang `5` dan `10 mm/jam` [53], [55].

### 3.8.6 Skenario Pengujian

Penelitian ini membandingkan tiga skenario model utama dengan data, target, jendela historis, horizon prediksi, dan protokol evaluasi yang sama untuk menganalisis kontribusi pemodelan sekuensial dan integrasi spatio-temporal probabilistik.

**Tabel 3.17 Rancangan Skenario Pengujian Model**

| No. | Skenario Model | Fokus Perbandingan Metodologis |
|---:|---|---|
| 1 | LSTM Multi-Node | Model sekuensial berulang (*recurrent baseline*) yang menerima masukan multivariat dari seluruh node tanpa mekanisme pemodelan graf dan *diffusion* |
| 2 | STGNN Deterministik | Model graf spasio-temporal yang menggabungkan GAT dan *temporal attention* secara mandiri dengan keluaran prediksi titik deterministik |
| 3 | Model Lengkap (RDM-STGNN) | Arsitektur terpadu *Retrieval-Augmented Diffusion Model* dengan pengkondisian graf STGNN dan pembangkitan ensemble probabilistik |

Tabel 3.17 merangkum tiga konfigurasi model yang diuji. Skenario 1 (LSTM Multi-Node) menjadi representasi model *deep learning* sekuensial deret waktu konvensional. Skenario 2 (STGNN Deterministik) menguji efektivitas representasi graf spasio-temporal tanpa komponen *diffusion* dan retrieval. Skenario 3 (Model Lengkap RDM-STGNN) menguji arsitektur terintegrasi yang diusulkan dalam penelitian ini.

Seluruh skenario dievaluasi pada node `MAIN` menggunakan tiga target, jendela historis enam jam, prediksi satu jam ke depan, 30 anggota ensemble untuk model probabilistik, dan pengambilan sampel evaluasi setiap jam. Dengan susunan ini, perbedaan hasil dapat diatribusikan secara langsung pada kontribusi arsitektur spasio-temporal dan pemodelan generatif *diffusion*.

## 3.9 Rancangan Visualisasi Hasil Prediksi Berbasis Web

Rancangan visualisasi web merupakan tahap akhir pada alur penelitian. Tahap ini menyajikan hasil prediksi yang telah dihasilkan model dan tidak mengubah proses pelatihan atau evaluasi.

### 3.9.1 Alur Penyajian Hasil

Hasil model disiapkan sebagai data keluaran, kemudian direncanakan untuk disalurkan melalui FastAPI dan ditampilkan menggunakan Vue.js. FastAPI berfungsi sebagai lapisan penyedia data, sedangkan Vue.js berfungsi sebagai lapisan antarmuka. Pada proposal ini, keduanya diposisikan sebagai rancangan visualisasi dan bukan bagian dari evaluasi model [47], [49]. Mockup rancangan ditunjukkan pada Gambar 3.9.

![Gambar 3.9 — Mockup visualisasi hasil nowcasting](bab3_media/gambar-3-9-mockup-web.png)

**Gambar 3.9 Mockup Visualisasi Hasil Nowcasting**
*Sumber: rancangan visualisasi penelitian.*

Gambar 3.9 menunjukkan empat kelompok informasi utama pada antarmuka *Pangrango Weather Desk*:

1. **Peta Grid Spasial dan Topologi Graf (Panel Kiri Atas)**: Menampilkan visualisasi lima titik sel *grid* ERA5 di kawasan Gunung Gede–Pangrango (node `MAIN`, `UP`, `DOWN`, `LEFT`, dan `RIGHT`) untuk memetakan distribusi spasial cuaca lereng gunung.
2. **Nowcasting Probabilistik dan Metrik Evaluasi (Panel Kanan Atas)**: Menampilkan sebaran 30 sampel prediksi *diffusion* untuk satu jam ke depan ($t+1$) berupa rentang persentil ($P_{10}–P_{90}$) dan median ($P_{50}$) untuk curah hujan, kecepatan angin, dan kelembapan relatif, dilengkapi panel metrik akurasi presipitasi (MAE, RMSE, CRPS, *Brier Score*, dan CSI).
3. **Peringatan Mitigasi Risiko Pendakian (Panel Kiri Bawah)**: Menyajikan indikator kesiapsiagaan aktivitas pendakian, seperti risiko suhu dingin ekstrem pada elevasi tinggi (>2500 mdpl), terpaan angin kencang (*wind chill*), dan potensi jalur basah/licin akibat hujan.
4. **Analisis Kejadian Historis Serupa / FAISS Retrieval (Panel Kanan Bawah)**: Menampilkan kartu analog cuaca masa lalu dengan tingkat kemiripan tertinggi (*Top-3 Historical Analogs*) beserta rekaman kondisi cuaca historis aslinya sebagai dasar interpretasi berbasis analog.

Pembacaan mockup dimulai dari lokasi, dilanjutkan dengan ringkasan prediksi dan probabilitas, kemudian informasi pendukung untuk interpretasi pengguna. Mockup ini menjelaskan susunan antarmuka, bukan hasil evaluasi model atau sistem peringatan dini operasional.

### 3.9.2 Informasi yang Ditampilkan

Visualisasi dirancang untuk menampilkan curah hujan, kecepatan angin, kelembapan relatif, nilai ringkasan ensemble, peluang kejadian hujan, grafik perubahan waktu, dan tabel ringkasan. Nilai target ditampilkan dari node `MAIN`, sedangkan empat node lainnya ditampilkan sebagai konteks spasial untuk membantu perbandingan kondisi antarlokasi. Setiap tampilan perlu menyertakan satuan, timestamp, dan keterangan bahwa data berasal dari reanalisis ERA5.

### 3.9.3 Batasan Rancangan Web

Visualisasi web pada tahap ini merupakan rancangan konseptual. Rancangan tersebut bukan sistem peringatan dini operasional dan belum mengukur perubahan perilaku pendaki atau penurunan kasus hipotermia. Jika dikembangkan lebih lanjut, sistem perlu membedakan data historis ERA5 dari data real-time, memvalidasi respons API, serta menampilkan waktu pembaruan dan status prediksi secara jelas.
