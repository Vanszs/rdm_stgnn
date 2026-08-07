# BAB I
# PENDAHULUAN

## 1.1 Latar Belakang

Hipotermia merupakan kondisi darurat ketika suhu inti tubuh turun secara abnormal akibat kehilangan panas yang melebihi kemampuan tubuh untuk memproduksinya. Pada aktivitas pendakian, risiko hipotermia meningkat secara signifikan ketika pendaki terpapar suhu rendah, angin kencang, hujan, pakaian yang basah, serta kelelahan fisik dalam durasi yang panjang [1], [2]. Urgensi permasalahan ini ditunjukkan oleh data BASARNAS periode 2015–2018 yang dilaporkan oleh Aminullah et al. [2], di mana hipotermia menjadi penyebab utama kecelakaan dalam aktivitas pendakian gunung dengan kontribusi sebesar 47%. Bahkan pada tahun 2018, dilaporkan terdapat tiga pendaki yang meninggal dunia akibat kondisi ini di Gunung Tampomas. Fakta tersebut menegaskan bahwa keselamatan pendaki sangat bergantung pada kesediaan informasi kondisi cuaca yang cepat dan akurat agar mereka dapat mengambil tindakan pencegahan sebelum paparan risiko berkembang menjadi kondisi medis yang mengancam jiwa.

Untuk meminimalkan risiko kecelakaan tersebut, diperlukan informasi prakiraan cuaca jangka pendek (nowcasting) yang mampu memberikan deteksi dini sebelum kondisi berbahaya terjadi. Dalam konteks mitigasi keselamatan pendakian, informasi cuaca per jam jauh lebih krusial dibandingkan prakiraan harian karena kondisi atmosfer di pegunungan dapat berubah secara dinamis dalam hitungan jam. Informasi mengenai hujan probabilistik—yaitu peluang terjadinya hujan dalam rentang waktu tertentu—menjadi parameter kunci untuk memahami tingkat ketidakpastian cuaca di lapangan. Berbeda dengan prakiraan deterministik yang hanya memberikan nilai tunggal, prakiraan probabilistik menyajikan distribusi kemungkinan kejadian cuaca beserta tingkat keyakinannya. Hal ini memungkinkan pendaki memperoleh gambaran risiko yang lebih realistis, seperti kemungkinan terjadinya hujan lebat mendadak atau peningkatan kecepatan angin yang ekstrem.

Nowcasting cuaca pada rentang waktu sangat pendek (0–6 jam) berperan sebagai garda depan dalam sistem peringatan dini keselamatan aktivitas luar ruang [3], [4]. Pemanfaatan data radar, model prediksi numerik, dan kecerdasan buatan memungkinkan informasi cuaca diperbarui secara berkala dan cepat guna mendukung keputusan taktis di lapangan [4], [5]. Penerapan metode deep learning dalam nowcasting juga telah terbukti mampu menghasilkan prakiraan curah hujan dan angin dengan resolusi spasial dan temporal yang tinggi [6], [7], [8]. Kendati demikian, efektivitas model ini sangat bergantung pada karakteristik wilayah pengamatan, sehingga evaluasi metodologis yang mendalam pada area dengan kondisi geografis ekstrem sangat diperlukan sebelum model diterapkan secara praktis.

Kawasan Gunung Gede–Pangrango merupakan salah satu destinasi wisata alam dan pendakian dengan intensitas kunjungan yang sangat tinggi, sehingga memiliki paparan risiko keselamatan yang besar. Berdasarkan kajian daya dukung lingkungan di kawasan Curug Cibeureum [9], tingkat kunjungan harian pada akhir pekan dan musim liburan sering kali melampaui kapasitas tampung nyata (Real Carrying Capacity/RCC) dan kapasitas tampung efektif (Effective Carrying Capacity/ECC). Kajian tersebut mengidentifikasi curah hujan tinggi sebagai faktor pembatas utama yang secara signifikan menurunkan daya dukung kawasan, bahkan dalam kondisi tertentu memaksa penutupan jalur wisata demi keselamatan pengunjung. Oleh karena itu, ketersediaan informasi cuaca per jam di kawasan ini sangat vital untuk membantu pihak pengelola dan pendaki dalam mengambil keputusan operasional, seperti pembatasan jumlah pengunjung, penutupan jalur sementara, atau evakuasi dini.

Dinamika hujan di wilayah pegunungan seperti Gunung Gede–Pangrango sangat kompleks karena dipengaruhi oleh interaksi antara topografi elevasi, kelembapan udara, dan arah angin. Mekanisme pengangkatan udara oleh lereng pegunungan (orographic lifting) memicu kondensasi uap air dan pembentukan awan konvektif secara cepat di lereng atas, sementara siklus harian pemanasan daratan turut menentukan waktu puncak terjadinya hujan [11], [12], [13]. Dinamika lokal ini menciptakan variabilitas spasial yang ekstrem, di mana perbedaan curah hujan yang signifikan dapat terjadi dalam jarak horizontal yang sangat pendek [14], [15]. Ketergantungan spasial dan temporal yang erat antar-elevasi ini membuat prakiraan cuaca per jam di wilayah pegunungan menjadi sangat menantang dan tidak dapat didekati dengan asumsi stasioner.

Model prakiraan cuaca deterministik konvensional sering kali gagal mengantisipasi kejadian ekstrem di pegunungan karena cenderung mengalami bias terhadap nilai rata-rata (smoothing effect). Hambatan utama dalam pemodelan cuaca ini terletak pada karakteristik data hujan yang bersifat zero-inflated dan heavy-tailed. Karakteristik **zero-inflated** berarti sebagian besar rekaman data menunjukkan nilai nol (tidak ada hujan), sedangkan karakteristik **heavy-tailed** berarti sebagian kecil kejadian hujan memiliki intensitas yang sangat ekstrem. Model regresi deterministik yang dioptimalkan dengan fungsi loss rata-rata akan cenderung memprediksi hujan ringan saat terjadi hujan lebat, dan sebaliknya, memprediksi ada hujan ringan saat kondisi sebenarnya kering. Akibatnya, representasi kejadian ekstrem yang sangat penting untuk mitigasi keselamatan menjadi terabaikan [16], [17].

Untuk mengatasi keterbatasan tersebut, penelitian terdahulu mulai mengembangkan pendekatan **probabilistik generatif**, dengan *Retrieval-Augmented Diffusion Model* (RDM) sebagai salah satu contoh penerapannya, serta **pemodelan spasio-temporal**, yang salah satunya diwujudkan melalui *Spatio-Temporal Graph Neural Network* (STGNN). Namun, sebagian besar studi masih menerapkan kedua pendekatan tersebut secara terpisah. Beberapa penelitian hanya berfokus pada model generatif untuk ketidakpastian tanpa mempertimbangkan informasi topografi [6], [7], sedangkan sebagian lainnya menggunakan pemodelan spasio-temporal untuk representasi spasial namun menghasilkan keluaran deterministik tunggal [10], [18], [20], [21]. Terdapat celah penelitian yang signifikan untuk mengintegrasikan model generatif probabilistik dengan representasi spasial graf secara bersamaan guna menangani karakteristik data hujan pegunungan yang zero-inflated dan heavy-tailed.

Penelitian ini bertujuan untuk mengatasi celah tersebut dengan mengembangkan **Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network**. Dalam model ini, **Retrieval-Augmented Diffusion Model (RDM)** bertindak sebagai model generatif utama yang memodelkan distribusi probabilistik cuaca melalui fix per, sehingga mampu menghasilkan beberapa kemungkinan skenario cuaca. Sementara itu, **Spatio-Temporal Graph Neural Network (STGNN)** digunakan sebagai komponen pengkondisi (conditioning) yang memodelkan lima titik lokasi pengamatan sebagai graf untuk menangkap ketergantungan spasial dan evolusi temporal dari data elevasi pegunungan. Kombinasi kedua metode ini dirancang untuk menghasilkan ensemble prakiraan probabilistik yang realistis dan sensitif terhadap nilai ekstrem.

Fokus penelitian ini dibatasi pada evaluasi metodologis model dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif satu jam ke depan di kawasan Gunung Gede–Pangrango dengan menggunakan data ERA5. Dataset ERA5 merupakan kumpulan catatan cuaca global dari *European Centre for Medium-Range Weather Forecasts* (ECMWF) yang mengombinasikan hasil simulasi komputer dengan data pengukuran langsung di lapangan. Penelitian ini berorientasi pada mitigasi risiko dengan menganalisis hasil prediksi serta kepekaan model terhadap kejadian cuaca ekstrem [22], [23]. Selain itu, hasil prediksi dari model ini akan diintegrasikan ke dalam visualisasi berbasis web [24].

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, penelitian ini merumuskan permasalahan sebagai berikut:

1. Bagaimana kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kondisi hujan, angin, dan kelembapan pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5?
2. Bagaimana hasil prediksi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dapat ditampilkan melalui visualisasi berbasis web untuk mendukung pengambilan keputusan dalam aktivitas pendakian?
3. Seberapa baik Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kejadian cuaca ekstrem, khususnya hujan dengan intensitas tinggi?
4. Bagaimana kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dibandingkan dengan model deterministik dalam memprediksi kondisi cuaca dan kejadian ekstrem?

## 1.3 Tujuan Penelitian

Tujuan umum penelitian ini adalah mengevaluasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network untuk nowcasting kondisi cuaca per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.

Tujuan khusus penelitian ini adalah:

1. Mengevaluasi kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kondisi hujan, angin, dan kelembapan pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.
2. Mengembangkan visualisasi berbasis web untuk menampilkan hasil prediksi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network sebagai informasi pendukung pengambilan keputusan dalam aktivitas pendakian.
3. Mengevaluasi kemampuan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kejadian cuaca ekstrem, khususnya hujan dengan intensitas tinggi.
4. Membandingkan kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dengan model deterministik dalam memprediksi kondisi cuaca dan kejadian ekstrem.

## 1.4 Manfaat Penelitian

Penelitian ini diharapkan dapat memberikan kontribusi dalam pengembangan metode nowcasting cuaca serta penerapannya dalam mendukung mitigasi risiko aktivitas pendakian di wilayah pegunungan. Manfaat yang diharapkan dari penelitian ini adalah sebagai berikut:

1. Memberikan kontribusi dalam pengembangan dan evaluasi pendekatan nowcasting probabilistik berbasis probabilistic generative modeling untuk memodelkan dinamika hujan, angin, dan kelembapan pada skala waktu per jam di wilayah pegunungan.
2. Menyediakan pemahaman yang lebih komprehensif mengenai efektivitas integrasi retrieval-based historical analogs dan spatio-temporal graph representation dalam menangkap ketidakpastian serta hubungan spasial-temporal cuaca.
3. Menyediakan analisis empiris mengenai kemampuan model nowcasting probabilistik dalam merepresentasikan ketidakpastian hujan yang bersifat zero-inflated dan heavy-tailed, termasuk sensitivitas prediksi terhadap kejadian hujan pada berbagai ambang intensitas.
4. Menyediakan analisis terkait trade-off antara akurasi prediksi rata-rata dan sensitivitas terhadap kejadian ekstrem sebagai dasar dalam pengambilan keputusan berbasis risiko pada aktivitas pendakian di wilayah pegunungan.
5. Menyediakan keluaran prediksi probabilistik yang dapat digunakan sebagai dasar pengembangan sistem visualisasi berbasis web untuk penyampaian informasi cuaca jangka pendek.

## 1.5 Batasan Masalah

Untuk menjaga fokus penelitian dan memastikan ketercapaian tujuan dalam ruang lingkup skripsi, penelitian ini dibatasi oleh beberapa ketentuan sebagai berikut:

1. Penelitian difokuskan pada kawasan Gunung Gede–Pangrango yang direpresentasikan oleh 5 titik lokasi.
2. Penelitian menggunakan data reanalysis ERA5 melalui Open-Meteo API dengan input 6 jam terakhir untuk memprediksi kondisi cuaca 1 jam ke depan.
3. Target prediksi dibatasi pada curah hujan, kecepatan angin, dan kelembapan relatif.
4. Penelitian mengevaluasi probabilistic generative modeling yang terintegrasi dengan retrieval-based historical analogs dan spatio-temporal graph representation.
5. Hasil prediksi tidak merepresentasikan kondisi mikrocuaca secara presisi karena menggunakan data grid reanalysis ERA5.
6. Penelitian difokuskan pada pengembangan dan evaluasi metodologi nowcasting probabilistik, bukan implementasi sistem operasional.

---

# BAB II — TINJAUAN PUSTAKA

BAB II TINJAUAN PUSTAKA

## 2.1 Penelitian Terdahulu

Penelitian-penelitian yang telah dilakukan dan relevan dengan penelitian ini mencakup model generatif probabilistik, model graf spasio-temporal, mekanisme retrieval pada diffusion model, model recurrent berbasis attention, serta pendekatan ensemble untuk prakiraan cuaca. Sepuluh penelitian berikut digunakan sebagai landasan perbandingan konseptual. Penelitian yang diusulkan tidak dihitung sebagai penelitian terdahulu dan hanya ditampilkan sebagai baris keempat pada Tabel 2.1.

1. Penelitian “Precipitation Nowcasting with Generative Diffusion Models”

oleh Asperti et al. (2025) [25] Penelitian ini mengembangkan Generative Ensemble Diffusion (GED) berbasis DDIM dan denoiser U-Net untuk menghasilkan 15 sampel prediksi hujan berbasis ERA5. Ensemble dibentuk melalui proses sampling berulang dan dapat diproses menggunakan rata-rata atau post-processing U-Net. Penelitian tersebut relevan karena menunjukkan bahwa diffusion ensemble dapat merepresentasikan beberapa kemungkinan evolusi hujan. Perbedaannya terletak pada penggunaan grid Eropa, bukan lima node ERA5 dengan target `MAIN` di Gunung Gede–Pangrango.

2. Penelitian   “Spatio-temporal      graph    neural    networks     to   improve

precipitation forecasts from numerical models” oleh Yousaf et al. (2025) [26] Penelitian ini mengembangkan WRF-GNN untuk memperbaiki keluaran prakiraan WRF menggunakan informasi 22 rain gauge di Calabria, Italia. Relevansinya terletak pada penggunaan representasi graf untuk memodelkan ketergantungan spasio-temporal. Namun, penelitian ini memakai keluaran WRF, observasi rain gauge, resolusi 2 km, dan horizon satu hari sehingga tidak merupakan reproduksi model pada penelitian ini.

3. Penelitian “Retrieval-Augmented Diffusion Models for Time Series

Forecasting” oleh Liu et al. (2024) [27] Penelitian ini mengusulkan Retrieval-Augmented Time series Diffusion (RATD), yang mengambil urutan historis serupa melalui embedding retrieval dan memasukkannya ke proses denoising melalui Reference-Modulated Attention. Relevansinya adalah prinsip integrasi retrieval dan diffusion pada data deret waktu. RATD tidak menggunakan lima node, ERA5, target `MAIN`, atau STGNN, sehingga hasilnya tidak dapat dianggap sebagai bukti performa pada hujan lokal.

4. Penelitian “Skilful precipitation nowcasting using deep generative models

of radar” oleh Ravuri et al. (2021) [6] Penelitian ini mengembangkan DGMR berbasis conditional GAN untuk menghasilkan prakiraan hujan probabilistik dari empat frame radar dan memprediksi hingga 90 menit. Model menggunakan spatial discriminator, temporal discriminator, dan regularisasi grid-cell. Penelitian ini relevan sebagai rujukan model generatif probabilistik untuk nowcasting, tetapi data radar dan resolusi spasialnya berbeda dari data ERA5 titik-lokasi pada penelitian ini.

5. Penelitian “Skilful nowcasting of extreme precipitation with NowcastNet”

oleh Zhang et al. (2023) [7] NowcastNet menggabungkan evolution network berbasis adveksi dan persamaan kontinuitas dengan stochastic generative network untuk mempertahankan struktur hujan ekstrem. Penelitian ini relevan karena memadukan kendala evolusi dan pembangkitan stokastik. Ketergantungannya pada data radar resolusi tinggi dan evaluasi hingga tiga jam membatasi penerapan langsung pada lima node ERA5.

6. Penelitian “Exploring Geometric Deep Learning for Precipitation

Nowcasting” oleh Zhao et al. (2023) [28] Penelitian ini memandang grid radar sebagai graf dan menggunakan temporal Graph Convolutional Network untuk memodelkan hubungan antarlokasi. Relevansinya adalah dasar konseptual adaptasi representasi graf pada data hujan. Perbedaan unit node, sumber data radar, dan horizon prediksi menyebabkan hasilnya tidak dapat dipindahkan langsung ke penelitian ini.

7. Penelitian   “RSDF-AM-LSTM:          Regional    Scale    Division    Rainfall

Forecasting Using Attention and LSTM” oleh Li et al. (2021) [29] Penelitian ini menggabungkan beberapa LSTM paralel dengan mekanisme attention untuk menangkap dependensi temporal-spasial pada ribuan stasiun meteorologi. Relevansinya terletak pada pemanfaatan attention dan LSTM untuk data multi-lokasi. Baseline Multi-node LSTM + Attention pada penelitian ini hanya merupakan adaptasi gagasan tersebut ke lima node ERA5 dan target `MAIN`, bukan reproduksi penuh RSDF-AM-LSTM.

8. Penelitian “A Hybrid Approach to Physical and Deep Learning Models for

Radar-Based Precipitation Nowcasting” oleh Kim et al. (2025) [20] Penelitian ini memadukan PySTEPS, RainNet, dan LightGBM untuk menggabungkan keunggulan model adveksi dan deep learning. Relevansinya terletak pada strategi penggabungan beberapa sumber representasi untuk meningkatkan prediksi. Pipeline radar dan model fisik pada penelitian tersebut tidak direproduksi karena penelitian ini menggunakan ERA5 pada lima node.

9. Penelitian “FuXi-ENS: A machine learning model for efficient and accurate

ensemble weather prediction” oleh Zhong et al. (2025) [17] FuXi-ENS menggunakan variational autoencoder dan loss CRPS untuk menghasilkan prakiraan ensemble global dengan perturbasi yang bergantung pada kondisi atmosfer. Relevansinya adalah representasi ketidakpastian dan evaluasi probabilistik. Perbedaan resolusi, wilayah, interval enam jam, dan horizon hingga 15 hari membatasi perbandingan langsung dengan nowcasting satu jam pada penelitian ini.

10. Penelitian “Beyond the horizon: A comprehensive analysis of artificial

intelligence-based weather forecasting models” oleh Haji-Aghajany et al. (2025) [30] Penelitian ini merupakan tinjauan komprehensif terhadap model prakiraan cuaca berbasis AI, termasuk isu ketidakpastian, generalisasi, interpretabilitas, dan kendala fisik. Relevansinya adalah pemetaan konseptual posisi diffusion model, retrieval, graf, dan attention dalam perkembangan AI weather forecasting. Paper ini bukan baseline dan tidak menyediakan eksperimen langsung pada lima node ERA5 atau Gunung Gede–Pangrango. Kesepuluh penelitian tersebut menunjukkan perkembangan pada diffusion ensemble, graf spasio-temporal, retrieval-augmented forecasting, attention-LSTM, dan ensemble weather prediction. Namun, belum terdapat penelitian pada daftar ini yang menguji integrasi Retrieval-Augmented Diffusion Model dan Spatio- Temporal Graph Neural Network secara simultan pada lima node ERA5 dengan target `MAIN`, horizon satu jam, dan konteks mikrocuaca Gunung Gede– Pangrango. Kebaruan penelitian ini dibatasi pada kombinasi metode, konfigurasi spasial, sumber data, horizon, dan wilayah studi; penelitian ini tidak mengklaim sebagai penelitian pertama di dunia. Tabel 2.1 Tabel Penelitian Terdahulu Kedudukan Judul dan Temuan No. Metode terhadap Peneliti Utama Penelitian Ini 1 Precipitation Generative Ensemble Rujukan utama Nowcasting Ensemble diffusion diffusion with Generative Diffusion menghasilkan ensemble; Diffusion berbasis DDIM beberapa berbeda pada Models — dan U-Net kemungkinan grid, wilayah, Asperti et al. prediksi dan konfigurasi (2025) [25] hujan spasial. berbasis ERA5. 2 Spatio-temporal WRF-GNN Graf spasio- Rujukan utama graph neural dengan keluaran temporal representasi networks to WRF dan rain digunakan graf; penelitian improve gauge untuk ini tidak precipitation memperbaiki menggunakan forecasts from prakiraan WRF atau 22 numerical hujan rain gauge. models — numerik. Yousaf et al. (2025) [26] 3 Retrieval- RATD dengan Retrieval Rujukan Augmented embedding historis integrasi Diffusion retrieval dan membantu retrieval- Models for Time Reference- diffusion model diffusion; Series Modulated pada bukan Forecasting — Attention forecasting penelitian cuaca Liu et al. (2024) deret waktu. lokal dan tidak [27] memakai STGNN. 4 Penelitian yang Retrieval- Hasil penelitian Model utama diusulkan Augmented belum tersedia. penelitian ini. Diffusion Model dengan STGNN; ERA5/Open- Meteo; lima node; target MAIN

## 2.2 Landasan Teori

Landasan teori dalam penelitian ini disusun untuk memberikan fondasi ilmiah bagi pengembangan model nowcasting probabilistik hujan menggunakan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning. Bab ini membahas konsep-konsep utama yang menjadi dasar penelitian, mulai dari prinsip nowcasting pada skala waktu per-jam, dinamika hujan orografis di pegunungan tropis, hingga mekanisme model generatif probabilistik berbasis diffusion. Selanjutnya, dijelaskan pula pendekatan retrieval- based historical analogs dan Spatio-Temporal Graph Conditioning dengan representasi lima node yang dirancang untuk menangkap ketergantungan spasial multidirectional di sekitar titik prediksi utama. Pembahasan ditutup dengan analisis risiko hipotermia pada aktivitas pendakian di Gunung Gede–Pangrango serta relevansinya dengan sistem peringatan dini berbasis nowcasting probabilistik. Dengan landasan teori yang terfokus ini, penelitian diharapkan mampu menghasilkan model yang tidak hanya unggul secara teknis, tetapi juga memberikan kontribusi nyata dalam mitigasi risiko keselamatan pendaki di kawasan pegunungan tropis.

### 2.2.1 Konsep Nowcasting dan Skala Waktu Prediksi Atmosfer

Nowcasting merupakan salah satu bidang paling dinamis dalam ilmu prakiraan cuaca modern karena beroperasi pada batas prediktabilitas atmosfer yang paling sensitif terhadap kondisi awal [6]. Pada skala waktu sangat pendek, atmosfer tidak lagi sepenuhnya didominasi oleh dinamika sinoptik berskala besar, melainkan juga belum sepenuhnya stabil dalam rezim statistik jangka menengah. Posisi antara dua rezim ini menjadikan nowcasting sebagai

**domain yang memerlukan pendekatan khusus dibandingkan prakiraan harian**

```text
atau mingguan. Dalam konteks penelitian ini yang berfokus pada mitigasi
risiko pendakian di wilayah pegunungan tropis, pemahaman konseptual
mengenai nowcasting skala waktu per jam menjadi landasan teoritis yang
krusial [7].
Tabel 2.2 Perbandingan Skala Prakiraan Atmosfer [7] [16].
Skala                                                      Contoh
Horizon      Karakteristik Utama
Prakiraan                                                   Keluaran
Bergantung kuat pada
kondisi awal dan observasi    Prediksi
Nowcasting            0–6 jam     terkini; menargetkan          hujan satu
fenomena lokal yang           jam ke depan.
berubah cepat.
Memadukan observasi dan     Prakiraan hujan
Short-range                       prediksi numerik untuk      harian dan
6–72 jam
forecasting                       evolusi cuaca jangka        peringatan
pendek.                     cuaca.
Lebih dari
Prakiraan
Medium-          72 jam           Menekankan dinamika
```

probabilistik range hingga atmosfer skala besar dan regional atau forecasting sekitar 15 prediksi ensemble. global. hari

#### 2.2.1.2 Definisi dan Ruang Lingkup Nowcasting

Dalam meteorologi operasional, nowcasting memiliki pengertian yang relatif spesifik dan dibedakan dari prakiraan cuaca pada skala waktu lain. Organisasi Meteorologi Dunia (WMO) mendefinisikan nowcasting sebagai prakiraan cuaca dengan detail lokal pada skala mesoscale dan skala yang lebih kecil, mencakup kondisi saat ini hingga sekitar 6 jam ke depan. Definisi ini menekankan tiga aspek utama: fokus pada horizon waktu sangat pendek (0–6 jam), resolusi spasial tinggi dengan detail lokal yang relevan untuk kejadian berisiko tinggi, serta ketergantungan kuat pada informasi pengamatan terkini beresolusi tinggi [6]. Dalam penelitian ini, nowcasting difokuskan pada prediksi satu jam ke depan dengan menggunakan jendela observasi 6 jam terakhir sebagai input [7]. Pendekatan ini sesuai dengan definisi WMO sekaligus selaras dengan karakteristik dinamika cuaca di kawasan pegunungan, di mana ancaman utama seperti hujan orografis dan peningkatan kecepatan angin dapat berkembang dengan sangat cepat [11]. Horizon satu jam memberikan keseimbangan optimal antara kecepatan respons dan akurasi prediksi untuk mendukung mitigasi risiko pendakian [1]. Horizon nowcasting yang pendek ini secara konseptual berada pada rezim initial condition-dominated, di mana akurasi prediksi sangat bergantung pada kualitas data observasi terkini dan kemampuan model dalam menangkap pola evolusi cuaca jangka pendek [6], [7]. Berbeda dengan short-range forecasting (6– 72 jam) yang lebih bergantung pada model Numerical Weather Prediction (NWP), nowcasting lebih mengandalkan data-driven learning dan ekstrapolasi dari observasi resolusi tinggi [31]. Pemahaman ini menjadi dasar pemilihan pendekatan probabilistik generatif dalam penelitian ini.

#### 2.2.1.3 Karakteristik Dinamika pada Skala Waktu Per Jam di Wilayah

Pegunungan Skala waktu 0–6 jam erat kaitannya dengan dinamika atmosfer pada mesoscale dan convective scale [7]. Pada skala ini, proses konvektif seperti convective initiation sangat sensitif terhadap fluktuasi kecil dalam kelembapan, suhu, dan dinamika angin lokal [13]. Di wilayah orografis tropis seperti Gunung Gede–Pangrango, dinamika ini semakin kompleks karena adanya efek orografis lifting, siklus diurnal konveksi yang kuat, serta interaksi angin lereng yang menyebabkan variabilitas spasial dan temporal yang tinggi [11], [14]. Lifetime sistem konvektif umumnya berada pada orde puluhan menit hingga beberapa jam [5]. Sel konvektif tunggal dapat hidup sekitar 30–60 menit, sedangkan sistem konveksi mesoskal dapat bertahan 3–6 jam atau lebih. Oleh karena itu, prakiraan pada horizon satu jam harus mampu merepresentasikan pembentukan sel baru, pergerakan sel yang ada, serta perubahan intensitas hujan secara akurat dan cepat [4], [20]. Rapid error growth akibat sifat nonlinier dan kaotik atmosfer semakin membatasi prediktabilitas deterministik pada skala ini [32]. Di kawasan Gunung Gede–Pangrango, efek topografi memperkuat dinamika mesoskal [11]. Gradien elevasi yang curam menyebabkan perbedaan kondisi meteorologis yang signifikan dalam jarak horizontal yang relatif pendek [14]. Variabilitas spasial yang tinggi ini menjadikan prakiraan per jam sebagai skala paling relevan untuk mitigasi risiko pendakian, karena ancaman cuaca dapat berkembang dan berubah secara cepat sepanjang lintasan pendakian dari hilir menuju puncak [1].

#### 2.2.1.4 Fitur Temporal dan Transformasi Distribusi Data Meteorologi

Fitur lag digunakan untuk merepresentasikan ketergantungan temporal kondisi hujan:

$$
\operatorname{PrecipitationLag1}_t = \operatorname{Precipitation}_{t-1} \tag{2.1}
$$

dengan:

- 𝑃𝑟𝑒𝑐𝑖𝑝𝑖𝑡𝑎𝑡𝑖𝑜𝑛𝐿𝑎𝑔1 = nilai curah hujan satu jam sebelumnya pada waktu 𝑡

- 𝑃𝑟𝑒𝑐𝑖𝑝𝑖𝑡𝑎𝑡𝑖𝑜𝑛        = nilai curah hujan pada waktu sebelumnya (𝑡 − 1)

Transformasi log1p digunakan untuk mengurangi distribusi tidak seimbang hujan yang memiliki nilai zero-inflated dan heavy-tailed:

$$
y' = \log(1+y) \tag{2.2}
$$

dengan:

- 𝑦 = nilai curah hujan asli

- 𝑦 = nilai curah hujan setelah transformasi

Standardisasi Z-score digunakan agar fitur memiliki skala yang sebanding: 𝑦′ − 𝜇

$$
z = \frac{y' - \mu}{\sigma + \varepsilon} \tag{2.3}
$$

𝜎+𝜀 dengan:

- 𝑧 = nilai hasil normalisasi Z-score

- 𝑦 = nilai curah hujan setelah transformasi

- 𝜇 = rata-rata (mean) dari data pelatihan

- 𝜎 = simpangan baku (standard deviation) dari data pelatihan

- 𝜀 = konstanta kecil untuk menghindari pembagian dengan nol

Parameter dihitung hanya dari data pelatihan. Pendekatan ini sejalan dengan standardisasi variabel meteorologis pada WeatherBench [33].

#### 2.2.1.5 Keterbatasan Pendekatan Deterministik dan Relevansi Pendekatan

Probabilistik Model Numerical Weather Prediction (NWP) dan pendekatan deterministik berbasis machine learning sering mengalami keterbatasan signifikan pada lead time pendek untuk fenomena konvektif [32]. Siklus pembaruan model yang relatif lambat, resolusi grid yang terbatas, serta kecenderungan menghasilkan prediksi yang terlalu halus (over-smoothing) menyebabkan under-prediction pada kejadian hujan ekstrem [31], [34]. Model regresi yang dioptimalkan dengan fungsi kerugian berbasis mean squared error cenderung bias ke nilai rata-rata distribusi, sehingga kurang sensitif terhadap distribusi heavy-tailed hujan yang menjadi ciri khas hujan orografis di pegunungan [6], [25]. Selain itu, pendekatan deterministik sulit merepresentasikan ketidakpastian intrinsik atmosfer pada skala per jam [7], [32]. Ketidakpastian ini berasal dari initial condition uncertainty, model structural error, observation error, dan chaotic error growth yang tumbuh secara nonlinier [16], [30]. Akibatnya, model deterministik sering gagal memberikan informasi yang cukup bagi pengambilan keputusan berbasis risiko, terutama dalam konteks keselamatan pendaki di lingkungan pegunungan yang dinamis [1]. Pendekatan probabilistik, seperti generative diffusion models, menawarkan solusi yang lebih sesuai karena mampu memodelkan distribusi kemungkinan kondisi atmosfer masa depan daripada hanya menghasilkan satu trajektori deterministik [25]. Pendekatan ini selaras dengan sifat stokastik atmosfer pada skala per jam dan mendukung pengambilan keputusan berbasis risiko, khususnya dalam mitigasi hipotermia pendaki [1]. Oleh karena itu, pemilihan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning dalam penelitian ini memiliki justifikasi teoritis yang kuat [7].

**Tabel 2.3 Perbandingan Keluaran Deterministik dan Probabilistik pada**

```text
Nowcasting [4], [16], [27].
Pendekatan
Aspek                                       Pendekatan Probabilistik
Deterministik
Ensemble atau distribusi
Satu prediksi titik untuk
Keluaran                                        beberapa prediksi yang
setiap waktu dan lokasi.
mungkin.
Tidak dinyatakan secara     Direpresentasikan melalui
Ketidakpastian
eksplisit.                  sebaran antar anggota ensemble.
Menilai nilai prakiraan     Mendukung keputusan berbasis
Kegunaan
```

tunggal. peluang dan tingkat risiko. CRPS, Brier Score, reliability Metrik utama MAE, RMSE, korelasi. diagram, serta metrik deterministik. Cenderung meratakan Memerlukan evaluasi kalibrasi Keterbatasan nilai pada kondisi tidak dan biaya sampling lebih tinggi. pasti.

### 2.2.2 Dinamika Hujan Orografis di Pegunungan Tropis

Hujan orografis merupakan fenomena utama yang membentuk pola curah hujan di wilayah pegunungan, terutama di daerah tropis seperti Gunung Gede– Pangrango [11], [35]. Interaksi antara aliran angin lembab dengan topografi menghasilkan angkat paksa (orographic lifting) yang memicu pembentukan awan dan hujan intens [36]. Di kawasan tropis, proses ini sering diperkuat oleh kelembapan tinggi dan ketidakstabilan atmosfer, sehingga menghasilkan distribusi hujan yang sangat heterogen dalam skala spasial dan temporal yang kecil [11], [25]. Pemahaman dinamika ini menjadi krusial dalam penelitian nowcasting probabilistik karena hujan orografis cenderung berkembang cepat dan sulit diprediksi dengan model deterministik. Di Gunung Gede–Pangrango, variabilitas elevasi yang tajam dari dataran rendah hingga puncak menciptakan gradien meteorologis yang signifikan [35]. Efek orografis tidak hanya meningkatkan intensitas hujan di lereng angin (windward slope), tetapi juga menghasilkan bayangan hujan (rain shadow) di sisi lereng lindung (leeward) [11], [36]. Fenomena ini menyebabkan perbedaan kondisi cuaca yang ekstrem dalam jarak horizontal relatif pendek, sehingga sangat relevan dengan risiko hipotermia pendaki yang melintasi berbagai elevasi dalam waktu singkat [28]. Dinamika hujan orografis di pegunungan tropis juga dipengaruhi oleh siklus diurnal dan interaksi dengan monsun, yang mempercepat convective initiation pada skala per jam [37]. Proses ini menghasilkan hujan dengan distribusi heavy-tailed, di mana kejadian ekstrem lebih sering terjadi dibandingkan distribusi normal [6], [7]. Oleh karena itu, model nowcasting yang digunakan dalam penelitian ini harus mampu menangkap ketergantungan spasial-temporal antar elevasi (hilir, lereng, dan puncak) melalui pendekatan Spatio-Temporal Graph Conditioning.

#### 2.2.2.1 Mekanisme Orographic Lifting dan Convective Initiation

Mekanisme utama hujan orografis adalah angkat paksa udara lembab oleh topografi, yang menyebabkan pendinginan adiabatik dan kondensasi [36]. Di wilayah tropis, angkat orografis ini sering memicu convective initiation ketika udara mencapai tingkat kebebasan konveksi (Level of Free Convection) [11]. Kecepatan angin lintang lereng (cross-slope wind) memainkan peran penting; semakin kuat angin, semakin dalam penetrasi gangguan gravitasi orografis yang mendinginkan dan melembabkan troposfer bawah, sehingga meningkatkan curah hujan hingga 20–30% per m/s peningkatan kecepatan angin [25], [36]. Berdasarkan sintesis mekanisme orographic lifting oleh Nicolas dan Boos [32], hubungan konseptual antara intensitas hujan orografis dan faktor atmosfer serta topografi dapat dinyatakan sebagai berikut:

$$
P_{\mathrm{orographic}} = f(U_{\perp}, q, H, S, C) \tag{2.4}
$$

dengan:

- 𝑃             = intensitas hujan orografis;

- 𝑈        = komponen kecepatan angin yang tegak lurus terhadap lereng;

- 𝑞 = kelembapan udara;

- 𝐻 = karakteristik elevasi/topografi;

- 𝑆 = orientasi dan kemiringan lereng;

- 𝐶 = kondisi konvektif atmosfer.

Rumus ini merupakan representasi konseptual, bukan persamaan empiris untuk menghitung curah hujan di Gunung Gede-Pangrango. Sumber: disusun dari Nicolas dan Boos [32]. Di Gunung Gede–Pangrango, gradien elevasi yang curam memperkuat proses lifting ini, terutama pada lereng selatan dan barat yang sering menjadi windward terhadap aliran monsun [35]. Interaksi antara angin lembab dengan topografi menghasilkan konvergensi lokal yang memicu sel konvektif baru dalam waktu singkat. Proses ini sangat dinamis pada skala per jam, sehingga memerlukan pendekatan probabilistik untuk merepresentasikan ketidakpastian convective initiation [6], [7]. Selain mekanis, faktor termal seperti pemanasan radiasi lereng pada siang hari juga berkontribusi terhadap convective initiation di pegunungan tropis [37]. Kombinasi forcing mekanis dan termal ini menghasilkan variabilitas spasial yang tinggi, di mana hujan lebat dapat terkonsentrasi di lereng tertentu sementara area berdekatan tetap relatif kering [11]. Pemahaman mekanisme ganda ini mendukung penggunaan graph neural network untuk memodelkan ketergantungan antar titik elevasi yang berbeda dalam arsitektur model penelitian ini.

#### 2.2.2.2 Variabilitas Spasial dan Temporal Hujan Orografis

Hujan orografis di pegunungan tropis menunjukkan variabilitas spasial yang sangat tinggi akibat perbedaan elevasi, orientasi lereng, dan interaksi angin [14], [35]. Di Gunung Gede–Pangrango, curah hujan cenderung meningkat seiring kenaikan elevasi pada lereng angin hingga mencapai maksimum di zona tengah lereng, kemudian menurun di puncak atau sisi lindung [11], [36]. Variabilitas ini menciptakan cuaca yang berbeda antar elevasi, yang berdampak langsung pada kondisi termal dan kelembapan yang dialami pendaki. Secara temporal, hujan orografis di wilayah tropis sering mengikuti siklus diurnal yang kuat, dengan puncak hujan pada sore hingga malam hari akibat pemanasan siang dan pelepasan ketidakstabilan [37]. Namun, pada kondisi angin lintas lereng yang kuat, siklus diurnal dapat tergantikan oleh forcing mekanis yang lebih dominan, sehingga hujan dapat terjadi kapan saja dalam skala per jam [36]. Karakteristik ini menjadikan nowcasting satu jam ke depan sangat relevan untuk mendeteksi perubahan mendadak yang berbahaya bagi keselamatan pendakian. Distribusi temporal hujan orografis juga cenderung heavy-tailed, dengan kejadian ekstrem yang jarang namun berdampak besar [6], [7]. Kejadian hujan lebat yang dipicu orografi sering bersifat quasi-stationary, di mana sistem hujan bertahan lama di lereng tertentu akibat blocking dan lifting berulang [34], [35]. Variabilitas ini menekankan pentingnya pendekatan retrieval-augmented untuk menangkap analog historis kejadian ekstrem dalam model diffusion yang dikembangkan.

#### 2.2.2.3 Relevansi dengan Nowcasting Probabilistik dan Mitigasi Risiko

Dinamika hujan orografis yang kompleks dan cepat berubah membatasi kemampuan model deterministik dalam memprediksi kejadian ekstrem di pegunungan tropis [7], [32]. Model regresi cenderung under-predict hujan berintensitas tinggi karena smoothing efek, sementara pendekatan probabilistik mampu menghasilkan distribusi kemungkinan yang lebih realistis [25]. Hal ini sangat penting untuk nowcasting di Gunung Gede–Pangrango, di mana hujan orografis dapat mempercepat kehilangan panas tubuh pendaki. Spatio-temporal variability yang tinggi antar elevasi memerlukan representasi graph-based untuk menangkap ketergantungan antar node [7]. Pendekatan Spatio- Temporal Graph Conditioning memungkinkan model mempelajari bagaimana hujan di satu elevasi memengaruhi elevasi lain melalui message passing, sehingga meningkatkan sensitivitas terhadap kejadian ekstrem [6], [7]. Dengan demikian, pemahaman mendalam tentang dinamika hujan orografis memberikan landasan teoritis yang kuat bagi Retrieval-Augmented Diffusion Model dalam menghasilkan prediksi probabilistik yang dapat mendukung sistem peringatan dini mitigasi risiko hipotermia pendaki di kawasan pegunungan tropis seperti Gunung Gede–Pangrango [1], [36].

### 2.2.3 Model Generatif Probabilistik dengan Diffusion Models

Model generatif probabilistik semakin menjadi pilihan utama dalam nowcasting hujan karena kemampuannya menangani ketidakpastian intrinsik atmosfer pada skala per jam [6], [25]. Berbeda dengan model deterministik yang cenderung menghasilkan prediksi rata-rata dan over-smoothing, model generatif mampu menghasilkan distribusi kemungkinan skenario cuaca masa depan yang lebih realistis [16], [30]. Dalam konteks penelitian ini, pendekatan diffusion models dipilih karena keunggulannya dalam memodelkan distribusi heavy-tailed hujan orografis di pegunungan tropis seperti Gunung Gede–Pangrango [7], [25]. Diffusion models bekerja berdasarkan proses forward yang secara bertahap menambahkan noise Gaussian ke data hingga menjadi noise murni, diikuti proses reverse (denoising) yang mempelajari cara mengembalikan noise menjadi data asli secara probabilistik [16], [25]. Proses ini memungkinkan model menghasilkan sampel yang beragam, sehingga sangat sesuai untuk menghasilkan ensemble prediksi nowcasting yang mencerminkan ketidakpastian alamiah atmosfer [6], [7]. Kemampuan ini menjadi landasan penting bagi pengembangan Retrieval- Augmented Diffusion Model dalam penelitian ini. Mengacu pada formulasi forward diffusion yang digunakan oleh Asperti et al. [25], proses penambahan noise Gaussian secara bertahap pada data dapat dinyatakan sebagai berikut:

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\left(x_t;\sqrt{1-\beta_t}\,x_{t-1},\beta_t I\right) \tag{2.5}
$$

Selanjutnya, sesuai objektif pelatihan diffusion model yang dijelaskan oleh Asperti et al. [25], fungsi kerugian untuk meminimalkan perbedaan antara noise aktual dan noise prediksi dapat dinyatakan sebagai berikut:

$$
L_{diff} = \mathbb{E}_{x_0,\epsilon,t}\left[\left\|\epsilon-\epsilon_\theta(x_t,t,c)\right\|_2^2\right] \tag{2.6}
$$

𝐿 =𝐸 , , 𝜖 −𝜖 ( , , ) dengan:

- 𝑥 = data target asli;

- 𝑥 = data pada diffusion timestep 𝑡;

- 𝛽 = varians noise pada timestep 𝑡;

- 𝐼 = matriks identitas;

- 𝜖 = noise Gaussian yang ditambahkan;

- 𝜖 = noise yang diprediksi model dengan parameter theta; dan

- 𝑐 = kondisi tambahan, berupa representasi historis, spasial, dan retrieval.

Penerapan diffusion models pada nowcasting hujan telah menunjukkan peningkatan performa signifikan dibandingkan pendekatan generatif sebelumnya seperti Generative Adversarial Networks (GAN), terutama dalam hal kualitas sampel dan stabilitas pelatihan [25], [30]. Model ini mampu menghasilkan prediksi yang lebih tajam dan lebih sensitif terhadap kejadian ekstrem, yang sangat dibutuhkan untuk mitigasi risiko hipotermia pendaki di kawasan dengan dinamika orografis yang kompleks [7], [31].

#### 2.2.3.1 Prinsip Kerja dan Keunggulan Diffusion Models untuk Nowcasting

Diffusion models terdiri dari dua proses utama yaitu forward diffusion process dan reverse denoising process [25]. Pada proses forward, data input seperti citra radar atau field hujan secara bertahap ditambahkan noise hingga menjadi distribusi Gaussian murni. Proses reverse kemudian mempelajari langkah demi langkah untuk menghilangkan noise tersebut dan merekonstruksi data asli yang kondisional terhadap observasi terkini [6], [16]. Forward diffusion secara bertahap menambahkan noise Gaussian:

$$
x_t = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\varepsilon \tag{2.7}
$$

Estimasi noise dikondisikan pada target bernoise, timestep, representasi graf, dan retrieval:

$$
\hat{\varepsilon}=f_\theta(x_t,t,h_g,R) \tag{2.8}
$$

Embedding timestep dapat menggunakan fungsi GELU [38]:

$$
\operatorname{GELU}(x)=x\Phi(x) \tag{2.9}
$$

Denoising network mempelajari pemetaan dari target bernoise dan kondisi menuju estimasi noise. Keluaran probabilistik dirumuskan sebagai distribusi bersyarat:

$$
p\left(y_{t+1}^{\mathrm{MAIN}} \mid X_t\right) \tag{2.10}
$$

Keunggulan utama diffusion models dibandingkan model generatif lain adalah kemampuannya menghindari mode collapse dan menghasilkan sampel dengan kualitas tinggi serta variasi yang realistis [25], [30]. Dalam nowcasting hujan, kemampuan ini sangat penting karena hujan pada skala per jam bersifat sangat stokastik dan memiliki distribusi heavy-tailed [7], [31]. Model ini mampu menghasilkan multiple plausible realizations yang lebih baik merepresentasikan ketidakpastian prediksi. Selain itu, diffusion models dapat dengan mudah dikondisikan terhadap variabel tambahan seperti kondisi atmosfer sebelumnya, angin, kelembapan, dan informasi spasial elevasi [6], [25]. Kondisional ini memungkinkan integrasi dengan Spatio-Temporal Graph Conditioning, sehingga model dapat mempelajari ketergantungan antar titik observasi di Gunung Gede–Pangrango [7], [16].

#### 2.2.3.2 Justifikasi Denoiser MLP dan Pemilihan Dimensi

Denoiser penelitian ini menggunakan multilayer perceptron (MLP) karena objek yang didenoising berbentuk vektor target ternormalisasi berdimensi tiga, sedangkan konteks cuaca, retrieval, graph embedding, dan timestep telah diproyeksikan menjadi embedding vektor. MLP sesuai untuk mempelajari pemetaan nonlinier dari target bernoise dan embedding kondisional menuju estimasi noise. Formulasi denoiser yang memprediksi noise dari data bernoise dan kondisi merupakan bagian utama DDPM [39] serta digunakan pada penerapan diffusion untuk keluaran meteorologis [25]. Arsitektur ini tidak memerlukan operasi konvolusi spasial seperti pada citra radar karena struktur spasial telah diringkas lebih dahulu oleh STGNN. Aktivasi SiLU digunakan pada lapisan MLP sebagai fungsi nonlinier yang halus. SiLU didefinisikan sebagai:

$$
\operatorname{SiLU}(x)=x\sigma(x) \tag{2.11}
$$

Penggunaan SiLU merupakan praktik arsitektural pada jaringan generatif [40] dan bukan jaminan bahwa model selalu lebih stabil. Dampaknya terhadap optimisasi dan performa tetap bergantung pada data, konfigurasi, dan hasil eksperimen. Denoiser menggunakan struktur dimensi 128 → 256 → 256 → 512 → 128 → 3. Dimensi 128 pertama merupakan ruang embedding hasil penggabungan kondisi. Ekspansi ke 256 dan 512 menyediakan ruang representasi yang lebih lebar untuk memodelkan interaksi nonlinier antara target bernoise dan kondisi. Representasi kemudian diproyeksikan kembali ke 128 sebelum keluaran akhir berdimensi tiga. Pola ekspansi dan kompresi tersebut merupakan rancangan hourglass-style yang memberikan kapasitas tersembunyi tanpa menggunakan lebar ribuan unit. Pada implementasi, keluaran lapisan tengah dan lapisan kedua digabungkan melalui concatenation:

$$
h_{skip}=h_{mid}\,\|\,h_2 \tag{2.12}
$$

Dengan demikian, koneksi ini bukan penjumlahan residual. Skip connection mempertahankan informasi dari representasi tahap sebelumnya dan menyediakan jalur tambahan bagi propagasi gradien. Literatur MLP residual dan diffusion mendukung penggunaan hidden width pada kisaran ratusan unit [41], [42], tetapi tidak membuktikan bahwa konfigurasi tertentu adalah optimal untuk penelitian ini.log1 Pemilihan 128, 256, dan 512 juga menggunakan ukuran yang merupakan kelipatan 32 dan umum pada operasi matriks perangkat keras modern. Pertimbangan tersebut hanya mendukung efisiensi implementasi, keunggulan akurasi, efisiensi, atau generalisasi harus dibuktikan melalui perbandingan konfigurasi dan eksperimen ablation. Dimensi keluaran tiga mengikuti jumlah target diffusion, yaitu hujan, kecepatan angin, dan kelembapan relatif pada node MAIN.

#### 2.2.3.3 Keterbatasan Model Deterministik dan Relevansi Pendekatan

Generatif Pendekatan deterministik berbasis regresi atau Numerical Weather Prediction (NWP) sering mengalami keterbatasan pada lead time pendek karena kecenderungan menghasilkan prediksi yang terlalu halus dan kurang sensitif terhadap kejadian ekstrem [32], [34]. Model ini bias terhadap nilai rata-rata distribusi, sehingga under-predict intensitas hujan tinggi yang sering memicu risiko hipotermia pada pendaki [30], [31]. Machine learning weather prediction models saat ini juga masih menghadapi tantangan dalam merepresentasikan ketidakpastian dan rapid error growth pada skala per jam [16], [32]. Pendekatan probabilistik generatif menjadi solusi karena mampu memodelkan distribusi penuh kemungkinan daripada hanya satu nilai prediksi tunggal [6], [25]. Dalam konteks pegunungan tropis, di mana hujan orografis bersifat sangat lokal dan cepat berubah, pendekatan generatif seperti diffusion models menawarkan fleksibilitas yang lebih tinggi untuk menangkap pola kompleks yang sulit dimodelkan secara fisika murni [7], [11]. Hal ini menjadikan diffusion models sebagai pilihan yang sesuai untuk mendukung sistem peringatan dini berbasis risiko.

#### 2.2.3.4 Relevansi dengan Retrieval-Augmented Diffusion Model

Retrieval-Augmented Diffusion Model menggabungkan diffusion model dengan mekanisme retrieval historis. Analog historis digunakan sebagai informasi pengondisian tambahan pada proses denoising. Pengaruhnya terhadap akurasi, kalibrasi, dan deteksi kejadian ekstrem pada data penelitian ini harus dibuktikan melalui eksperimen, bukan diasumsikan dari sitasi. Integrasi retrieval mechanism membantu mengatasi keterbatasan data pelatihan pada kejadian langka (rare events) yang sangat berbahaya bagi pendaki [16], [31]. Kombinasi ini memungkinkan model menghasilkan ensemble prediksi yang lebih terkalibrasi dan sensitif terhadap kondisi ekstrem di Gunung Gede– Pangrango. Dengan demikian, Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning digunakan untuk mengevaluasi kemampuan diffusion model dalam menghasilkan prediksi probabilistik yang beragam pada lingkungan pegunungan tropis yang dinamis [1], [7], [25].

### 2.2.4 Retrieval-Based Historical Analogs

Model generatif probabilistik semakin menjadi pilihan utama dalam nowcasting hujan karena kemampuannya menangani ketidakpastian intrinsik atmosfer pada skala per jam [6], [25]. Berbeda dengan model deterministik yang cenderung menghasilkan prediksi rata-rata dan over-smoothing, model generatif mampu menghasilkan distribusi kemungkinan skenario cuaca masa depan yang lebih realistis [16], [30]. Dalam konteks penelitian ini, pendekatan diffusion models dipilih karena keunggulannya dalam memodelkan distribusi heavy-tailed hujan orografis di pegunungan tropis seperti Gunung Gede–Pangrango [7], [25]. Diffusion models bekerja berdasarkan proses forward yang secara bertahap menambahkan noise Gaussian ke data hingga menjadi noise murni, diikuti proses reverse (denoising) yang mempelajari cara mengembalikan noise menjadi data asli secara probabilistik [16], [25]. Proses ini memungkinkan model menghasilkan sampel yang beragam, sehingga sangat sesuai untuk menghasilkan ensemble prediksi nowcasting yang mencerminkan ketidakpastian alamiah atmosfer [6], [7]. Kemampuan ini menjadi landasan penting bagi pengembangan Retrieval- Augmented Diffusion Model dalam penelitian ini. Mengacu pada formulasi forward diffusion yang digunakan oleh Asperti et al. [25], proses penambahan noise Gaussian secara bertahap pada data dapat dinyatakan sebagai berikut:

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\left(x_t;\sqrt{1-\beta_t}\,x_{t-1},\beta_t I\right) \tag{2.13}
$$

Selanjutnya, sesuai objektif pelatihan diffusion model yang dijelaskan oleh Asperti et al. [25], fungsi kerugian untuk meminimalkan perbedaan antara noise aktual dan noise prediksi dapat dinyatakan sebagai berikut:

$$
L_{diff} = \mathbb{E}_{x_0,\epsilon,t}\left[\left\|\epsilon-\epsilon_\theta(x_t,t,c)\right\|_2^2\right] \tag{2.14}
$$

𝐿 =𝐸 , , 𝜖 −𝜖 ( , , ) dengan:

- 𝑥 = data target asli;

- 𝑥 = data pada diffusion timestep 𝑡;

- 𝛽 = varians noise pada timestep 𝑡;

- 𝐼 = matriks identitas;

- 𝜖 = noise Gaussian yang ditambahkan;

- 𝜖 = noise yang diprediksi model dengan parameter theta; dan

- 𝑐 = kondisi tambahan, berupa representasi historis, spasial, dan retrieval.

Penerapan diffusion models pada nowcasting hujan telah menunjukkan peningkatan performa signifikan dibandingkan pendekatan generatif sebelumnya seperti Generative Adversarial Networks (GAN), terutama dalam hal kualitas sampel dan stabilitas pelatihan [25], [30]. Model ini mampu menghasilkan prediksi yang lebih tajam dan lebih sensitif terhadap kejadian ekstrem, yang sangat dibutuhkan untuk mitigasi risiko hipotermia pendaki di kawasan dengan dinamika orografis yang kompleks [7], [31].

### 2.2.5 Spatio-Temporal Graph Conditioning pada Representasi Data Elevasi

Representasi data spatio-temporal menjadi sangat penting dalam nowcasting hujan di wilayah pegunungan karena adanya ketergantungan kuat antar lokasi yang berbeda posisi relatif terhadap titik observasi utama [11], [14]. Dalam penelitian ini, lima titik observasi direpresentasikan sebagai node dalam graph, yaitu MAIN, UP, DOWN, LEFT, dan RIGHT, dengan node MAIN sebagai target prediksi utama [7], [35]. Pendekatan Spatio-Temporal Graph Conditioning memungkinkan model mempelajari hubungan spasial dan temporal antar kelima node ini secara simultan, sehingga lebih mampu menangkap dinamika lokal hujan orografis di sekitar lokasi pendakian Gunung Gede–Pangrango [16], [30]. Graph Neural Network (GNN), khususnya Graph Attention Network (GAT), merepresentasikan kelima titik observasi sebagai node dalam graf. Secara umum, graf dinyatakan sebagai 𝐺 = (𝑉, 𝐸), dengan 𝑉 sebagai himpunan node dan 𝐸 sebagai himpunan edge berarah. Pada penelitian ini, 𝑉= {𝑀𝐴𝐼𝑁, 𝑈𝑃, 𝐷𝑂𝑊𝑁, 𝐿𝐸𝐹𝑇, 𝑅𝐼𝐺𝐻𝑇} dan 𝐸 terdiri atas delapan edge eksplisit dua arah pada topologi star. Topologi tersebut merupakan abstraksi relasi spasial penelitian, bukan representasi bahwa atmosfer hanya memiliki delapan hubungan fisik. Integrasi Spatio-Temporal Graph Conditioning ke dalam arsitektur Retrieval- Augmented Diffusion Model meningkatkan kemampuan model dalam menangani variabilitas spasial tinggi yang menjadi ciri khas hujan orografis [11], [35]. Pendekatan ini sangat relevan untuk mitigasi risiko hipotermia karena memungkinkan prediksi yang lebih akurat pada titik MAIN, yang dapat mewakili posisi pendaki atau lokasi krusial di sepanjang jalur pendakian [1], [34].

#### 2.2.5.1 Representasi Graph untuk Data Elevasi dengan Lima Node

Dalam model ini, lima titik observasi direpresentasikan sebagai node dalam graph spatio-temporal, yaitu node MAIN sebagai target utama, serta node UP, DOWN, LEFT, dan RIGHT yang merepresentasikan posisi relatif di sekitarnya [14], [35]. Setiap node dilengkapi dengan fitur meteorologis seperti hujan lag, suhu udara, kelembapan relatif, kecepatan angin, dan variabel atmosfer lainnya pada beberapa waktu observasi sebelumnya [7], [16]. Node MAIN menjadi pusat perhatian karena menjadi lokasi utama yang diprediksi. Graph Attention Network (GAT) digunakan untuk memproses graph ini karena kemampuannya memberikan bobot perhatian yang adaptif terhadap node tetangga [30], [32]. Melalui mekanisme attention, model dapat mempelajari seberapa besar pengaruh node UP, DOWN, LEFT, dan RIGHT terhadap evolusi kondisi cuaca di node MAIN pada horizon satu jam ke depan [7], [16]. Struktur graph menggunakan topologi star: node MAIN terhubung dua arah dengan UP, DOWN, LEFT, dan RIGHT, sedangkan node tetangga tidak saling terhubung. Jendela waktu (sliding window) menyusun enam snapshot graf historis sebelum waktu target. Dengan 𝑡 sebagai waktu target, jendela aktual adalah:

$$
X_t=\left\{x_{t-6},x_{t-5},\ldots,x_{t-1}\right\} \tag{2.15}
$$

Dengan:

- 𝑋 = matriks fitur node pada snapshot waktu 𝑡

- 𝑥 = enam snapshot graf historis sebelum waktu target 𝑡

Urutan graf spasio-temporal dinyatakan sebagai:

$$
g=\left\{G_{t-6},G_{t-5},\ldots,G_{t-1}\right\} \tag{2.16}
$$

dengan:

- 𝐺 = graf pada waktu 𝑡

- 𝑔 = urutan graf yang menjadi input model

Secara umum, node merepresentasikan lokasi atau unit pengamatan, sedangkan edge menyatakan hubungan spasial yang digunakan untuk pertukaran informasi. Pada implementasi, graph processing dilakukan pada setiap snapshot secara berurutan. Hasil node-level kemudian diproses dengan global mean pooling:

$$
g_b=\frac{1}{|V_b|}\sum_{i\in V_b}h_{b,i} \tag{2.17}
$$

|𝑉 | ∈ Pooling tersebut mengubah representasi seluruh node menjadi satu embedding graph-level. Operasi pooling pada representasi graf multi-lokasi sejalan dengan alur pemrosesan STGNN pada penelitian terdahulu [43]. Embedding enam snapshot kemudian ditumpuk sebagai sequence untuk diproses oleh temporal attention.

**Tabel 2.4 Definisi Node pada Representasi Graph Lima Node [11], [14], [35]**

```text
Posisi Relatif
Node                        Fungsi dalam Model        Koneksi Graph
terhadap MAIN
Menyediakan target
Terhubung dua arah
Titik prediksi    curah hujan, kecepatan
MAIN                                                     dengan UP, DOWN,
utama.        angin, dan kelembapan
LEFT, RIGHT.
```

relatif pada 𝑡 + 1. Menyediakan konteks Terhubung dua arah UP Utara dari MAIN. kondisi atmosfer dari dengan MAIN arah utara. Menyediakan konteks Selatan dari Terhubung dua arah DOWN kondisi atmosfer dari MAIN. dengan MAIN arah selatan. Menyediakan konteks Terhubung dua arah LEFT Barat dari MAIN. kondisi atmosfer dari dengan MAIN arah barat. Menyediakan konteks Timur dari Terhubung dua arah RIGHT kondisi atmosfer dari MAIN. dengan MAIN arah timur.

#### 2.2.5.2 Keunggulan Spatio-Temporal Graph dibandingkan Pendekatan

Konvensional Pendekatan sequence-based atau grid-based konvensional sering kali kurang efektif dalam menangkap ketergantungan spasial non-Euclidean yang kompleks di wilayah pegunungan [32], [34]. Model berbasis CNN atau LSTM umumnya mengasumsikan hubungan spasial tetap atau hanya lokal, sehingga sulit memodelkan interaksi multidirectional dari berbagai arah terhadap satu titik utama [30], [31]. Spatio-Temporal Graph Conditioning mampu mengatasi keterbatasan tersebut dengan secara eksplisit memodelkan hubungan antar node melalui message passing dan attention mechanism [7], [16]. Pendekatan ini memungkinkan model mempelajari pola propagasi hujan orografis dan pengaruh angin dari berbagai arah secara lebih akurat pada skala per jam [11], [35]. Integrasi graph conditioning dengan diffusion model memungkinkan proses denoising dilakukan secara kondisional terhadap struktur graph lima node, sehingga menghasilkan prediksi ensemble yang lebih konsisten secara spasial dan lebih sensitif terhadap kondisi lokal di sekitar node MAIN [7], [25]. Keunggulan ini sangat penting untuk meningkatkan akurasi prediksi pada titik krusial yang digunakan untuk mitigasi risiko. Encoding spasial oleh GAT dirumuskan sebagai:

$$
h_t=GAT(G_t) \tag{2.18}
$$

dengan:

- 𝐺 = graf pada waktu 𝑡

- ℎ = representasi spasial hasil encoding

Representasi seluruh waktu diagregasi menggunakan temporal attention:

$$
h_t^G=\mathrm{TemporalAttention}\left(h_{t-L+1},\ldots,h_t\right) \tag{2.19}
$$

dengan:

- ℎ = representasi spasio-temporal akhir pada waktu 𝑡

- 𝐿 = panjang jendela observasi historis

Pada multi-head attention, keluaran kepala atensi digabungkan melalui concatenation sesuai mekanisme GAT [44]. Penggunaan representasi graph untuk ketergantungan spasio-temporal multi-lokasi juga didukung oleh penelitian STGNN [43]. Temporal attention menggunakan scaled dot-product attention dengan causal mask: 𝑄𝐾

$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_K}}+M\right)V \tag{2.20}
$$

𝑑 Mask 𝑀 mencegah representasi pada suatu timestep mengakses timestep masa depan. Embedding posisi trainable, residual connection, dropout, dan LayerNorm digunakan pada tahap temporal. Representasi pada timestep terakhir dipilih sebagai embedding graph sequence; mekanisme ini bukan penjumlahan berbobot satu skalar untuk setiap jam. Pada multi-head attention, keluaran kepala atensi digabungkan melalui concatenation [44]:

$$
h_i'=\mathbin{\|}_{k=1}^{4}\sum_{j\in\mathcal{N}_i}\alpha_{ij}^{k}W^{k}h_j \tag{2.21}
$$

∈𝒩 Aktivasi SiLU digunakan untuk membentuk transformasi nonlinier yang halus. Dimensi kepala, jumlah kepala, dan dimensi embedding ditetapkan secara eksperimental pada metodologi.

### 2.2.6 Risiko Hipotermia dan Mitigasi Pendakian

Risiko hipotermia merupakan ancaman serius bagi keselamatan pendaki di pegunungan, termasuk di kawasan tropis seperti Gunung Gede–Pangrango [1]. Hipotermia terjadi ketika suhu inti tubuh manusia turun di bawah 35°C akibat kehilangan panas yang melebihi produksi panas tubuh [1], [45]. Di pegunungan tropis, hipotermia sering disebabkan oleh kombinasi hujan deras, angin kencang, dan kelembapan tinggi yang mempercepat kehilangan panas melalui konduksi, konveksi, dan evaporasi, meskipun suhu udara tidak ekstrem seperti di pegunungan tinggi bersalju [1], [22]. Kondisi cuaca di Gunung Gede–Pangrango yang dinamis, terutama hujan orografis disertai angin, dapat menyebabkan hipotermia “wet-cold” (hipotermia basah-dingin) dengan cepat [1]. Pakaian yang basah kehilangan kemampuan isolasi hingga 90%, sementara angin memperbesar efek wind chill, sehingga mempercepat penurunan suhu tubuh pendaki meskipun berada di elevasi sedang hingga tinggi [1], [45]. Kejadian ini semakin berbahaya karena pendaki sering berada dalam kondisi kelelahan setelah berjalan jauh, sehingga kemampuan tubuh untuk menghasilkan panas menurun secara signifikan [22]. Nowcasting probabilistik hujan, kecepatan angin, dan kelembapan relatif menjadi sangat relevan sebagai sistem peringatan dini. Prediksi satu jam ke depan dengan pendekatan probabilistik memungkinkan pendeteksian dini kombinasi faktor berisiko tinggi sebelum kondisi hipotermia berkembang [6], [7]. Penelitian ini menghubungkan output model Retrieval-Augmented Diffusion dengan Spatio- Temporal Graph Conditioning secara langsung dengan mitigasi risiko keselamatan pendaki.

#### 2.2.6.1 Mekanisme Hipotermia di Lingkungan Pegunungan Tropis

Hipotermia di pegunungan tropis berbeda dengan kasus klasik di daerah dingin karena suhu udara relatif hangat, namun kelembapan tinggi dan hujan deras menjadi faktor dominan [1]. Mekanisme utama meliputi konduksi panas langsung ke pakaian dan kulit yang basah, konveksi yang dipercepat oleh angin, serta evaporasi yang terus berlangsung pada pakaian lembab [1], [45]. Kombinasi ketiga mekanisme ini menyebabkan kehilangan panas yang cepat bahkan pada suhu udara di atas 10–15°C. Di Gunung Gede–Pangrango, efek orografis sering menghasilkan hujan lebat secara tiba-tiba disertai peningkatan kecepatan angin seiring kenaikan elevasi [11], [35]. Kondisi ini sangat berbahaya bagi pendaki karena perubahan cuaca dapat terjadi dalam waktu singkat sepanjang jalur pendakian, dari zona hilir hingga menuju puncak [1]. Selain itu, kelelahan fisik dan penurunan kadar gula darah akibat aktivitas berkepanjangan semakin memperbesar kerentanan terhadap hipotermia [22], [45]. Gejala awal hipotermia seperti menggigil, kelelahan, dan penurunan koordinasi motorik sering diabaikan pendaki karena dianggap sebagai kelelahan biasa, padahal kondisi ini dapat berkembang cepat menjadi hipotermia sedang hingga berat yang mengancam nyawa [1]. Oleh karena itu, pemantauan dini melalui prediksi cuaca probabilistik menjadi krusial.

#### 2.2.6.2 Faktor Meteorologis Pemicu Risiko Hipotermia

Faktor meteorologis utama yang memicu hipotermia di pegunungan tropis adalah kombinasi curah hujan tinggi, kecepatan angin, dan kelembapan relatif yang tinggi [1], [7]. Hujan orografis yang intens membasahi pakaian secara cepat, sementara angin memperbesar efek convective heat loss [11], [35]. Kelembapan udara yang tinggi menghambat penguapan keringat dan memperburuk sensasi dingin pada tubuh.

**Tabel 2.5 Faktor Meteorologis terkait Paparan Dingin Pendaki [1], [22]**

```text
Variabel       Peran Informasi
Faktor      Dampak Potensial
Model           Nowcasting
Membasahi pakaian
dan meningkatkan                        Memberi peringatan
Hujan       kehilangan panas       Curah hujan.     peluang hujan pada
```

melalui konduksi serta satu jam berikutnya. evaporasi. Mengidentifikasi Meningkatkan kondisi angin yang Kecepatan kehilangan panas Kecepatan berpotensi angin melalui konveksi dan angin. memperburuk efek wind chill. paparan. Variabel Peran Informasi Faktor Dampak Potensial Model Nowcasting Melengkapi Memengaruhi Kelembapan Kelembapan interpretasi kondisi penguapan dan relatif relatif. basah dan kondisi pakaian basah. kenyamanan termal. Pada node utama (MAIN) yang menjadi fokus prediksi model ini, variabilitas dari node UP, DOWN, LEFT, dan RIGHT dapat memengaruhi kondisi lokal secara signifikan [7], [16]. Misalnya, angin dari arah tertentu dapat membawa hujan lebih deras ke titik MAIN, sehingga meningkatkan risiko hipotermia dalam waktu singkat [1]. Pendekatan lima node pada Spatio-Temporal Graph Conditioning memungkinkan model menangkap dinamika multidirectional ini dengan lebih baik. Kombinasi variabel tersebut sulit diprediksi secara akurat dengan model deterministik karena sifat stokastik dan heavy-tailed dari hujan orografis [6], [25]. Oleh karena itu, pendekatan probabilistik yang menghasilkan distribusi kemungkinan menjadi lebih sesuai untuk mendukung pengambilan keputusan keselamatan pendaki.

#### 2.2.6.3 Relevansi Nowcasting Probabilistik sebagai Mitigasi Risiko

Nowcasting probabilistik hujan dengan horizon satu jam ke depan dapat menyediakan informasi bagi tindakan preventif, seperti mencari tempat berteduh, mengganti pakaian basah, atau memutuskan untuk turun sebelum kondisi memburuk [1], [46]. Output model berupa distribusi probabilitas pada node MAIN dapat menjadi masukan bagi pengembangan indeks risiko hipotermia multi-faktor pada penelitian lanjutan; indeks tersebut bukan keluaran yang diimplementasikan dalam penelitian ini. Integrasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning memungkinkan prediksi yang lebih sensitif terhadap kejadian ekstrem yang berpotensi memicu hipotermia [7], [25]. Pendekatan ini tidak hanya meningkatkan akurasi teknis, tetapi juga memberikan nilai praktis langsung sebagai decision support system untuk pengelola taman nasional dan komunitas pendaki Gunung Gede–Pangrango. Dengan demikian, penelitian ini menghubungkan kemajuan teknologi nowcasting probabilistik dengan kebutuhan keselamatan manusia di lingkungan pegunungan tropis. Model yang dikembangkan diharapkan dapat berkontribusi pada pengurangan kejadian hipotermia dan peningkatan keselamatan aktivitas pendakian melalui sistem peringatan dini berbasis data yang akurat dan tepat waktu [1], [5], [46].

### 2.2.7 Visualisasi Web Berbasis Vue.js dan FastAPI

Visualisasi berbasis web berperan sebagai lapisan penyajian yang menghubungkan keluaran model nowcasting dengan pengguna akhir. Lapisan ini memungkinkan informasi berupa prediksi titik, distribusi ensemble, probabilitas kejadian hujan, dan indikator risiko disajikan secara terstruktur serta mudah diinterpretasikan tanpa mengubah proses pelatihan maupun inferensi model. Dalam pengembangan dashboard, penggunaan framework front-end mendukung konsistensi antarmuka, pemisahan komponen tampilan, dan pembaruan data secara responsif [47]. Vue.js digunakan sebagai landasan front-end untuk merancang dashboard yang memuat kartu indikator kondisi node MAIN, grafik deret waktu, visualisasi probabilitas, dan tabel ringkasan prediksi. Pendekatan berbasis komponen memungkinkan setiap elemen antarmuka dikembangkan secara modular, sehingga perubahan pada satu komponen tidak memengaruhi keseluruhan halaman. Vue memiliki kinerja rendering yang kompetitif, struktur pengembangan sederhana, serta efisiensi penggunaan sumber daya yang memadai untuk aplikasi web responsif. Karakteristik tersebut relevan bagi penyajian hasil nowcasting yang perlu diperbarui secara periodik dan dipahami oleh pengguna nonteknis[47]. FastAPI digunakan sebagai lapisan backend untuk menyediakan antarmuka pemrograman aplikasi yang menyalurkan artefak hasil inferensi kepada dashboard. Framework ini mendukung validasi data berbasis Python type hints, dokumentasi API otomatis, dan pemrosesan asinkron, sehingga sesuai untuk penyediaan layanan data yang terstruktur [48]. Integrasi FastAPI sebagai backend Python dan Vue sebagai antarmuka memungkinkan pemisahan yang jelas antara modul algoritme, layanan data, dan visualisasi hasil pada sistem model atmosfer. Dalam arah pengembangan penelitian ini, FastAPI dapat menyediakan endpoint untuk hasil prediksi probabilistik, sedangkan Vue.js menyajikannya sebagai grafik dan indikator risiko. Implementasi dashboard tidak termasuk ruang lingkup evaluasi model; subbab ini menjadi landasan konseptual bagi pengembangan sistem penyampaian informasi pada tahap lanjutan [48].

## 2.3 Analisis Celah Penelitian

Penelitian terkini dalam nowcasting hujan telah menunjukkan kemajuan melalui penerapan model generatif probabilistik, khususnya diffusion models [6], [25]. Model-model tersebut menyediakan prediksi ensemble, tetapi performanya tetap bergantung pada data, metrik, dan karakteristik kejadian ekstrem [7], [16]. Sebagian besar studi masih berfokus pada data radar resolusi tinggi di wilayah dataran atau lautan, dengan sedikit perhatian pada karakteristik hujan orografis di pegunungan tropis yang memiliki variabilitas spasial dan temporal yang sangat tinggi [11], [35]. Meskipun beberapa penelitian telah mengintegrasikan aspek fisika orografis ke dalam model nowcasting, pendekatan yang digunakan umumnya masih berbasis grid-based atau sequence modeling yang kurang efektif dalam menangkap ketergantungan multidirectional antar lokasi pada gradien elevasi yang curam [14], [32]. Selain itu, model diffusion yang ada sering kali mengalami kesulitan dalam memprediksi kejadian ekstrem karena keterbatasan data langka (rare events), sehingga cenderung under-predict intensitas hujan tinggi yang menjadi pemicu utama risiko hipotermia [25], [31]. Celah ini semakin terlihat pada konteks pegunungan tropis seperti Gunung Gede–Pangrango, di mana interaksi angin lintas lereng dan siklus diurnal memainkan peran penting. Penelitian sebelumnya juga jarang menggabungkan mekanisme retrieval historical analogs dengan diffusion models secara spesifik untuk nowcasting satu jam ke depan di lingkungan orografis [17], [30]. Kebanyakan studi hanya menggunakan pure generative approach atau retrieval sederhana tanpa integrasi yang mendalam dengan representasi graph untuk menangani variabilitas spasial dari berbagai arah. Selain itu, aplikasi model nowcasting probabilistik untuk mitigasi risiko keselamatan manusia, khususnya hipotermia pada aktivitas pendakian di pegunungan tropis, masih sangat terbatas [1], [46]. Mayoritas penelitian lebih berorientasi pada aspek teknis akurasi model daripada penerapan langsung sebagai sistem peringatan dini berbasis risiko.

### 2.3.1 Celah pada Representasi Spasial dan Temporal

Pendekatan konvensional seperti CNN, LSTM, atau transformer murni belum optimal dalam memodelkan ketergantungan spasial non-Euclidean yang kompleks di wilayah pegunungan [32], [34]. Representasi lima node (MAIN, UP, DOWN, LEFT, RIGHT) dengan node MAIN sebagai target utama belum banyak dieksplorasi dalam literatur nowcasting hujan orografis [5], [9]. Celah ini menyebabkan model sulit menangkap pengaruh multidirectional dari berbagai arah terhadap titik prediksi utama.

### 2.3.2 Celah pada Penanganan Kejadian Ekstrem dan Ketidakpastian

Banyak model diffusion saat ini masih kurang optimal dalam menangani distribusi heavy-tailed hujan ekstrem di lingkungan tropis tanpa bantuan informasi historis yang relevan [25], [31]. Penggunaan retrieval-based historical analogs yang dikombinasikan dengan proses denoising diffusion masih jarang diterapkan, terutama pada horizon nowcasting satu jam dengan data reanalysis atau stasiun permukaan [16], [30].

### 2.3.3 Celah pada Aplikasi Mitigasi Risiko Pendakian

Terdapat kesenjangan antara kemajuan teknologi nowcasting probabilistik dengan aplikasi mitigasi keselamatan pendakian di pegunungan tropis [1], [5]. Pengembangan indeks risiko hipotermia berbasis multi-faktor dari keluaran probabilistik merupakan peluang penelitian lanjutan, bukan komponen yang diimplementasikan dalam penelitian ini [22], [46]. Berdasarkan analisis celah tersebut, penelitian ini mengusulkan Retrieval- Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning menggunakan representasi lima node dengan MAIN sebagai target utama. Penelitian mengevaluasi retrieval historical analogs, diffusion probabilistik, dan representasi graph untuk dinamika orografis Gunung Gede–Pangrango; manfaatnya terhadap mitigasi keselamatan ditafsirkan dari hasil evaluasi, bukan diasumsikan sebelumnya.

---

# BAB III
# METODE PENELITIAN

## 3.1 Tahapan Penelitian

Tahapan penelitian disusun secara berurutan untuk mengembangkan dan mengevaluasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning dalam nowcasting probabilistik hujan satu jam ke depan. Tahapan tersebut mencakup studi literatur, pengambilan data, preprocessing, pembagian dataset temporal, pembentukan fitur dan representasi graf, perancangan arsitektur model, pelatihan, inferensi, evaluasi, serta skenario eksperimen. Alur keseluruhan tahapan penelitian ditunjukkan pada Gambar 3.1.

![Gambar 3.1 — placeholder gambar: Alur Tahapan Penelitian](gambar-3-1-placeholder)

**Gambar 3.1 Alur Tahapan Penelitian**

Tahap awal penelitian adalah studi literatur untuk mengidentifikasi, menganalisis, dan mensintesis kajian terdahulu yang relevan dengan pengembangan model nowcasting probabilistik hujan berbasis deep learning. Fokus kajian mencakup: (1) teknik nowcasting hujan pada skala per-jam, (2) penerapan model generatif probabilistik khususnya diffusion models, serta (3) pendekatan spatio-temporal graph dan retrieval-augmented mechanism dalam pemodelan cuaca.

Tahap selanjutnya adalah Pengambilan Data, yaitu pengumpulan data meteorologi per jam dari Open-Meteo Archive API berbasis ERA5 reanalysis pada lima titik observasi spasial (MAIN, UP, DOWN, LEFT, RIGHT). Tahap ini menjadi fondasi utama karena kualitas dan kelengkapan data sangat menentukan keberhasilan tahapan berikutnya.

Selanjutnya dilakukan Preprocessing Data yang meliputi validasi struktur, pembersihan, pembentukan fitur lag, transformasi logaritmik pada hujan, serta normalisasi data menggunakan Standard Scaling untuk memastikan data siap digunakan dalam pelatihan model.

Kemudian dilakukan Pembagian Dataset secara temporal (time-based split) untuk memisahkan data menjadi training, validation, dan testing set. Pembagian ini penting untuk menjaga aspek temporal order dan mencegah data leakage pada evaluasi model.

Tahap Pembentukan Fitur dan Graf melibatkan rekayasa fitur serta pembuatan struktur graph spatio-temporal dengan lima node di mana node MAIN menjadi target prediksi utama. Graf ini merepresentasikan ketergantungan spasial multidirectional antar node.

Selanjutnya adalah Perancangan Arsitektur Model yang mendefinisikan keseluruhan komponen Retrieval-Augmented Diffusion Model, termasuk mekanisme retrieval historical analogs dan Spatio-Temporal Graph Conditioning menggunakan Graph Attention Network (GAT).

Proses Proses Pelatihan Model dilakukan dengan menggunakan weighted denoising loss untuk meningkatkan sensitivitas model terhadap kejadian hujan ekstrem serta teknik conditional diffusion berdasarkan observasi historis dan struktur graph.

Tahap Evaluasi Model kemudian dilakukan menggunakan metrik deterministik (MAE, RMSE), metrik probabilistik (CRPS), serta metrik berbasis threshold (POD, FAR, CSI) untuk menilai performa model secara komprehensif.

Tahap terakhir, merancang web visualisasi hasil prediksi dirancang sebagai sarana penyampaian informasi nowcasting yang dapat mendukung interpretasi keluaran model oleh pengguna.

Dengan alur tahapan yang terstruktur seperti yang ditunjukkan pada Gambar 3.1, penelitian ini memastikan bahwa setiap komponen model dikembangkan secara bertahap dan dapat dievaluasi secara ilmiah.

## 3.2 Studi Literatur

Studi literatur merupakan tahap awal untuk membangun dasar metodologis penelitian dan menentukan komponen model yang sesuai dengan tujuan nowcasting probabilistik hujan. Kajian dilakukan secara terarah terhadap penelitian terdahulu, teori nowcasting, dinamika hujan orografis, model generatif berbasis diffusion, retrieval-based historical analogs, serta representasi graph spasio-temporal.

Proses studi literatur meliputi identifikasi sumber yang relevan, seleksi berdasarkan kesesuaian topik dan tahun publikasi, pembacaan metode serta hasil penelitian, kemudian sintesis kelebihan, keterbatasan, dan peluang pengembangan. Literatur tentang diffusion digunakan untuk merumuskan mekanisme pembangkitan ensemble dan denoising. Literatur tentang GNN, GAT, dan temporal attention digunakan untuk merancang representasi hubungan antar-node dan urutan snapshot historis. Literatur retrieval digunakan untuk merumuskan penggunaan analog historis sebagai kondisi tambahan pada diffusion model.

Hasil studi literatur digunakan untuk menetapkan: (1) penggunaan data ERA5 pada lima node spasial, (2) node MAIN sebagai target prediksi, (3) jendela historis enam snapshot, (4) integrasi STGNN, retrieval, dan conditional diffusion, serta (5) metrik evaluasi deterministik, probabilistik, dan berbasis kejadian. Selain itu, studi literatur digunakan untuk menentukan model pembanding yang diuji pada skenario eksperimen.

Studi literatur tidak digunakan untuk mengklaim bahwa model penelitian ini pasti lebih baik daripada penelitian terdahulu. Klaim kinerja ditentukan berdasarkan hasil eksperimen pada dataset dan protokol evaluasi penelitian ini. Dengan demikian, keluaran tahap studi literatur berupa kerangka teori, spesifikasi metodologis, daftar referensi, dan rumusan celah penelitian yang menjadi dasar tahap pengambilan data.

## 3.3 Pengambilan Data

Pengambilan data merupakan tahap awal yang sangat krusial dalam penelitian ini karena menjadi fondasi bagi seluruh proses pengembangan model. Penelitian ini menggunakan data sekunder berupa deret waktu multivariat dengan referensi spasial tetap yang diperoleh melalui layanan Open-Meteo Archive API berbasis reanalisis ERA5. Pemilihan ERA5 didasarkan pada konsistensi historis jangka panjang, kelengkapan variabel meteorologis, serta resolusi spasial dan temporal yang seragam. ERA5 adalah reanalysis historis, bukan sumber observasi real-time; karena itu penggunaannya dibatasi untuk pelatihan dan evaluasi metodologis, bukan operasi nowcasting langsung. Proses pengambilan data melalui Open-Meteo Archive API dapat dilihat pada Gambar 3.2 berikut.

![Gambar 3.2 — placeholder gambar: Diagram Proses Pengambilan Data ERA5 melalui Open-Meteo API](gambar-3-2-placeholder)

**Gambar 3.2 Diagram Proses Pengambilan Data ERA5 melalui Open-Meteo API**

Gambar 3.2 mengilustrasikan alur pengambilan data yang dimulai dari penentuan Koordinat Node, permintaan data melalui Open-Meteo API, perolehan ERA5 Dataset, dilanjutkan dengan Validasi Data Grid, Penggabungan Data Semua Node, hingga menghasilkan Dataset Penelitian yang siap digunakan. Diagram ini menekankan mekanisme validasi grid center untuk mencegah duplikasi spasial serta konsistensi penggabungan data dari kelima node.

### 3.3.2 Koordinat Node

Koordinat node ditetapkan sebelum permintaan data dikirimkan ke Open-Meteo API. Lima node digunakan, yaitu MAIN sebagai node target serta UP, DOWN, LEFT, dan RIGHT sebagai node konteks. Koordinat setiap node dirangkum pada Tabel 3.1.

**Tabel 3.1 Koordinat Node**

| Node | Latitude | Longitude |
|---|---:|---:|
| MAIN | -6.75 | 107.00 |
| UP | -6.50 | 107.00 |
| DOWN | -7.00 | 107.00 |
| LEFT | -6.75 | 106.75 |
| RIGHT | -6.75 | 107.25 |

### 3.3.3 Open-Meteo API

Koordinat setiap node dikirimkan ke Open-Meteo Archive API menggunakan parameter waktu mulai dan waktu akhir, zona waktu UTC, serta daftar variabel meteorologis yang diperlukan. Respons API diterima dalam format data deret waktu. Proses ini diulang untuk setiap node menggunakan rentang waktu dan daftar variabel yang sama.

### 3.3.4 ERA5 Dataset

Data yang diterima melalui Open-Meteo API bersumber dari ERA5 reanalysis. Data dikumpulkan pada resolusi satu jam untuk periode 1 Januari 2005 hingga 31 Desember 2025. Variabel meteorologis dan elevasi disimpan bersama timestamp UTC dan ID node. ERA5 digunakan sebagai sumber data historis untuk pelatihan dan evaluasi metodologis, bukan sebagai sumber observasi real-time.

### 3.3.5 Validasi Data Grid

Setelah respons API diterima, koordinat grid aktual grid center diperiksa dan dibandingkan dengan koordinat node yang diminta. Pemeriksaan ini dilakukan untuk memastikan setiap node dipetakan pada grid yang sesuai dan mencegah grid collision, yaitu dua node berbeda memperoleh grid ERA5 yang sama. Apabila ditemukan ketidaksesuaian atau duplikasi grid, proses dihentikan dan koordinat node ditinjau sebelum pengambilan dilanjutkan.

### 3.3.6 Penggabungan Semua Node

Data dari kelima node digabungkan berdasarkan timestamp UTC ke dalam satu dataset terpadu. ID node dipertahankan sebagai penanda lokasi, dengan urutan konsisten [MAIN, UP, DOWN, LEFT, RIGHT]. Pemeriksaan kelengkapan dilakukan setelah penggabungan untuk memastikan setiap timestamp memiliki struktur node yang diperlukan. Tiga variabel target hanya ditetapkan pada node MAIN; node lainnya berfungsi sebagai penyedia fitur konteks spasial.

Posisi spasial kelima node hasil penetapan koordinat ditampilkan pada Gambar 3.3. Visualisasi ini digunakan untuk memeriksa susunan node yang dipertahankan ketika data digabungkan dan direpresentasikan sebagai graph sequence.

![Gambar 3.3 — placeholder gambar: Posisi Lima Node Pengamatan pada Wilayah Studi Gunung Gede–Pangrango](gambar-3-3-placeholder)

**Gambar 3.3 Posisi Lima Node Pengamatan pada Wilayah Studi Gunung Gede–Pangrango**

Gambar 3.3 memperlihatkan distribusi spasial kelima node di sekitar kawasan Gunung Gede–Pangrango. Node MAIN berfungsi sebagai titik target, sedangkan node UP, DOWN, LEFT, dan RIGHT menjadi konteks spasial pada dataset gabungan.

### 3.3.7 Dataset Penelitian

Dataset penelitian memiliki satu baris untuk setiap kombinasi timestamp dan node. Karakteristik keseluruhan dataset yang berhasil diperoleh ditunjukkan pada Tabel 3.2.

**Tabel 3.2 Karakteristik Dataset Penelitian**

| Karakteristik | Nilai |
|---|---|
| Sumber Data | Open-Meteo (ERA5) |
| Resolusi Temporal | 1 Jam |
| Periode Data | 2005–2025 |
| Jumlah Node | 5 |
| Jumlah Timestamp | 184.080 |
| Total Observasi | 920.400 |

Dengan prosedur pengambilan data yang terstruktur, tervalidasi, dan didukung visualisasi spasial, dataset yang dihasilkan memiliki integritas spasial dan temporal yang tinggi, sehingga siap digunakan pada tahapan preprocessing dan pemodelan selanjutnya.

Tabel 3.3 menampilkan beberapa baris contoh hasil penggabungan data dari lima node. Data disimpan sebagai deret waktu multivariat dengan satu baris untuk setiap kombinasi timestamp dan node. Kolom masukan memuat variabel meteorologis dan elevasi, sedangkan tiga kolom target digunakan khusus untuk node MAIN. Nilai target pada node konteks tidak digunakan dalam pembentukan target pelatihan dan ditandai sebagai diabaikan.

**Tabel 3.3 Contoh data yang diambil**

[TEKS PDF TIDAK TERBACA: Tabel 3.3 berupa visual/data yang tidak tersimpan sebagai tabel DOCX yang dapat dibaca; isi baris dan nilai tidak dapat diverifikasi.]

Pada Tabel 3.3, Baris MAIN memuat target yang digunakan untuk pelatihan dan evaluasi, sedangkan baris node konteks hanya menyediakan fitur masukan spasial. Tanda elipsis menunjukkan fitur meteorologis lain yang tidak ditampilkan dalam tabel ringkas.

## 3.4 Preprocessing Data

Tahap preprocessing data mengubah dataset hasil pengambilan menjadi data yang siap digunakan dalam pelatihan, validasi, pengujian, dan pembentukan graph sequence. Alur preprocessing dibagi menjadi tiga bagian, yaitu koleksi data, preprocessing dan validasi, serta normalisasi dan split.

![Gambar 3.4 — placeholder gambar: Flowchart Preprocessing Data](gambar-3-4-placeholder)

**Gambar 3.4 Flowchart Preprocessing Data**

Gambar 3.4 menunjukan alur preprocessing data secara keseluruhan, mulai dari dataset mentah hingga dataset siap pemodelan. Diagram ini menunjukkan urutan tahapan yang saling terkait untuk memastikan integritas data sepanjang pipeline.

### 3.4.1 Koleksi Data

Koleksi data pada tahap preprocessing menggunakan dataset terpadu hasil penggabungan lima node pada subbab Pengambilan Data. Dataset dibaca dengan mempertahankan timestamp UTC, ID node, urutan node [MAIN, UP, DOWN, LEFT, RIGHT], variabel masukan, target node MAIN, dan fitur elevasi.

Pemeriksaan awal dilakukan untuk memastikan berkas tersedia, kolom wajib terbaca, serta jumlah baris dapat diproses sebelum validasi dan transformasi dilaksanakan.

Data kemudian disusun berdasarkan timestamp dan ID node. Penyusunan ini menjadi masukan bagi pemeriksaan kelengkapan node pada setiap timestamp. Target tidak dibentuk ulang untuk node konteks; node MAIN tetap menjadi satu-satunya node target, sedangkan empat node lainnya digunakan sebagai sumber konteks spasial.

### 3.4.2 Preprocessing dan Validasi

Tahap selanjutnya adalah validasi struktur data. Pemeriksaan dilakukan terhadap kelengkapan lima node pada setiap timestamp, urutan node yang harus konsisten ([MAIN, UP, DOWN, LEFT, RIGHT]), kesesuaian nama kolom, serta keberadaan nilai tidak valid. Validasi ini bersifat fail-fast, yaitu proses dihentikan apabila ditemukan ketidaksesuaian untuk mencegah propagasi kesalahan ke tahap berikutnya.

Selanjutnya dilakukan pembentukan fitur temporal. Untuk menangkap ketergantungan waktu pada horizon nowcasting satu jam, dibuat fitur lag curah hujan satu jam sebelumnya (`precipitation_lag1`). Fitur ini dihitung menggunakan persamaan berikut:

$$\mathrm{PrecipitationLag1}=\mathrm{Precipitation}$$

$t-1$ (DOCX: `PrecipitationLag1_t = Precipitation_{t-1}`)

Pada timestamp pertama setiap node, nilai lag diinisialisasi dengan nol. Penambahan fitur lag ini penting karena curah hujan memiliki autokorelasi temporal yang kuat pada skala per-jam.

Tahap berikutnya adalah transformasi variabel curah hujan. Variabel ini memiliki distribusi yang sangat skewed dan didominasi oleh nilai nol dengan sedikit kejadian ekstrem. Untuk mengurangi skewness dan meningkatkan stabilitas pelatihan, dilakukan transformasi logaritmik menggunakan fungsi:

$$y'=\log(1+y)$$

Transformasi ini membantu model lebih baik dalam mempelajari pola hujan orografis yang bersifat heavy-tailed. Sebagai contoh untuk nilai curah hujan sebesar 2.40 mm maka $y=2.40\ \mathrm{mm}$, diperoleh nilai curah hujan setelah transformasi sebagai berikut $y'=\log(1+2.40)=1.2238$.

Setelah validasi, fitur lag dan transformasi logaritmik diterapkan pada kolom yang ditentukan. Tahap ini menghasilkan data yang konsisten secara struktur dan siap memasuki proses normalisasi. Nilai yang tidak memenuhi aturan validasi tidak diteruskan ke tahap berikutnya.

### 3.4.3 Normalisasi dan Split

Setelah transformasi, seluruh fitur dan variabel target dinormalisasi menggunakan parameter statistik yang dihitung dari data pelatihan. Statistik non-degenerate dihitung dari node MAIN pada data pelatihan dan digunakan pada validasi serta pengujian. Jika fitur tertentu memiliki statistik degenerate, fitur tersebut saja menggunakan fallback statistik seluruh node. Denominator tetap menggunakan epsilon $\varepsilon$ untuk mencegah pembagian dengan nol; DOCX mendefinisikan epsilon sebagai konstanta kecil, tetapi tidak memberikan nilai numerik.

Fitur dengan simpangan baku mendekati nol menggunakan fallback statistik seluruh node hanya untuk mengatasi kondisi degenerate. Fallback tersebut tidak berlaku otomatis untuk seluruh fitur. Seluruh fitur yang disalurkan ke DataLoader, termasuk fitur untuk GAT, telah berada pada skala Z-score. Proses normalisasi dilakukan dengan persamaan:

$$z=\frac{y'-\mu}{\sigma+\varepsilon}$$

Parameter $\mu$ dan $\sigma$ dihitung hanya dari data pelatihan untuk mencegah data leakage. Parameter yang sama kemudian diterapkan pada data validasi dan data uji. Dengan $y'=1.2238$, $\mu=0.60$, $\sigma=0.90$, $\epsilon=0.000001$, diperoleh nilai hasil normalisasi sebagai berikut $z=0.6931$.

Contoh perhitungan eksplisit tidak tersimpan sebagai struktur terpisah di DOCX; nilai hasil yang tercetak adalah $z=0.6931$.

Setelah normalisasi, dataset akan dibagi menjadi tiga himpunan secara kronologis. Detail rasio, rentang waktu, prosedur pencegahan data leakage, dan ilustrasi pembagian dijelaskan pada subbab selanjutnya.

## 3.5 Pembagian Dataset Temporal

Setelah melalui tahap preprocessing, dataset selanjutnya dibagi menjadi tiga himpunan yaitu data pelatihan (training set), data validasi (validation set), dan data pengujian (test set). Pembagian ini bertujuan untuk mendukung proses pelatihan model, pemilihan hyperparameter, serta evaluasi performa yang objektif dan tidak bias terhadap data yang belum pernah dilihat oleh model. Karena data meteorologis bersifat deret waktu dengan ketergantungan temporal yang kuat, penelitian ini menggunakan pembagian temporal (time-based split) daripada pembagian acak [6], [16].

Pendekatan temporal split dipilih untuk menjaga urutan kronologis data, sehingga model hanya mempelajari pola dari periode masa lalu dan dievaluasi pada periode masa depan. Skema pembagian dataset yang digunakan dalam penelitian ini ditunjukkan pada Gambar 3.5.

![Gambar 3.5 — placeholder gambar: Ilustrasi Pembagian Dataset Temporal](gambar-3-5-placeholder)

**Gambar 3.5 Ilustrasi Pembagian Dataset Temporal**

Gambar 3.5 menampilkan diagram garis waktu yang menggambarkan pembagian dataset secara kronologis menjadi tiga periode utama. Visualisasi ini memperjelas bahwa model dilatih hanya menggunakan data historis dan diuji pada data masa depan yang sepenuhnya tidak terlibat dalam proses pelatihan. Salah satu tujuan utama pembagian temporal adalah mencegah data leakage. Dalam penelitian ini, beberapa langkah pencegahan diterapkan, antara lain:

- Pembagian dilakukan secara kronologis tanpa pengacakan (shuffle).
- Statistik normalisasi dihitung hanya dari data pelatihan.
- Basis data retrieval hanya dibangun dari data pelatihan.
- Data validasi dan pengujian tidak digunakan dalam proses pelatihan maupun pemilihan hyperparameter.

Dengan skema pembagian temporal ini, model dilatih sesuai dengan kondisi operasional nowcasting yang sesungguhnya, di mana prediksi satu jam ke depan hanya dapat dibuat berdasarkan informasi observasi hingga waktu saat ini. Pendekatan ini meningkatkan reliabilitas evaluasi dan mendekatkan hasil penelitian dengan aplikasi nyata di lapangan untuk mitigasi risiko hipotermia pendaki di Gunung Gede–Pangrango.

## 3.6 Pembentukan Fitur dan Representasi Graf

Setelah dataset melalui tahap preprocessing dan pembagian temporal, langkah selanjutnya adalah membentuk representasi data yang sesuai dengan arsitektur model Retrieval-Augmented Diffusion dengan Spatio-Temporal Graph Neural Network. Pada tahap ini, data tidak lagi diperlakukan sebagai tabel konvensional, melainkan direpresentasikan sebagai urutan graf (graph sequence) yang mengintegrasikan informasi spasial dan temporal secara simultan. Proses ini mencakup pembentukan fitur input, pembuatan jendela waktu, serta konstruksi struktur graf yang merepresentasikan hubungan antar node observasi.

### 3.6.1 Pembentukan Fitur Input

Fitur input dipilih berdasarkan ketersediaan pada ERA5 dan relevansinya terhadap dinamika hujan orografis serta mitigasi risiko hipotermia. Fitur dibedakan menjadi dua kelompok: fitur dinamis (berubah terhadap waktu) dan fitur statis (nilai tetap). Elevasi berfungsi sebagai fitur statis yang memberikan informasi topografi pada setiap node. Fitur input ditunjukan pada Tabel 3.4.

**Tabel 3.4 Daftar Fitur Input Model**

| No | Variabel | Keterangan |
|---:|---|---|
| 1 | Temperature 2m | Suhu udara |
| 2 | Relative Humidity 2m | Kelembapan relatif |
| 3 | Dew Point 2m | Titik embun |
| 4 | Surface Pressure | Tekanan permukaan |
| 5 | Wind Speed 10m | Kecepatan angin |
| 6 | Wind Direction 10m | Arah angin |
| 7 | Cloud Cover | Tutupan awan |
| 8 | Precipitation Lag-1 | Curah hujan 1 jam sebelumnya |
| 9 | Elevation | Ketinggian node |

### 3.6.2 Pembentukan Jendela Waktu (Temporal Window)

Untuk menangkap ketergantungan temporal, data disusun menggunakan pendekatan sliding window. Setiap sampel input terdiri dari beberapa observasi historis sebagai konteks prediksi satu jam ke depan. Jendela observasi dapat dinyatakan sebagai:

$$X=\{x_{t-L+1},x_{t-L+2},\ldots,x_t\}$$

Formula pada DOCX tidak tersimpan sebagai OMML; bentuk di atas konsisten dengan keterangan DOCX bahwa jendela memuat enam snapshot historis.

Melalui pendekatan ini, model dapat mempelajari perubahan kondisi atmosfer yang terjadi dalam beberapa jam sebelumnya sebelum menghasilkan prediksi pada waktu berikutnya.

### 3.6.3 Representasi Graf Spasial

Hubungan spasial antar titik pengamatan direpresentasikan dalam bentuk graf. Penelitian ini menggunakan lima node dengan node MAIN sebagai target prediksi utama, sedangkan node UP, DOWN, LEFT, dan RIGHT berfungsi sebagai konteks spasial multidirectional. Struktur graf menggunakan topologi star dengan delapan edge terarah dan ditunjukkan pada Gambar 3.6.

![Gambar 3.6 — placeholder gambar: Topologi Star Graph pada Representasi Spasial](gambar-3-6-placeholder)

**Gambar 3.6 Topologi Star Graph pada Representasi Spasial**

Pada Gamabr 3.6 menunjukan Node MAIN terhubung secara dua arah dengan node UP, DOWN, LEFT, dan RIGHT, sedangkan node tetangga tidak memiliki edge langsung satu sama lain.

Koefisien atensi pada topologi tersebut bersifat terarah dan asimetris. Pada node MAIN, normalisasi softmax mendistribusikan atensi pada lima hubungan, yaitu self-loop MAIN serta empat hubungan dengan node tetangga. Sebaliknya, pada setiap node tetangga, atensi hanya didistribusikan pada dua hubungan, yaitu self-loop node tersebut dan hubungan langsung menuju MAIN. Pembatasan ini memastikan informasi antartetangga tidak dipertukarkan secara langsung, melainkan digunakan untuk memperkaya representasi spasial lokal node target.

### 3.6.4 Representasi Spasio-Temporal

Setelah struktur graf terbentuk, informasi spasial dan temporal digabungkan menjadi rangkaian graf (graph sequence). Pada setiap langkah waktu digunakan struktur graf yang sama, sedangkan nilai fitur pada masing-masing node diperbarui sesuai kondisi meteorologis aktual. Secara konseptual, rangkaian graf dapat dituliskan sebagai:

$$g=\{G_{t-L+1},G_{t-L+2},\ldots,G_t\}$$

Formula pada DOCX tidak tersimpan sebagai OMML; bentuk di atas konsisten dengan keterangan DOCX tentang urutan enam snapshot graf historis.

Melalui tahap pembentukan fitur dan representasi graf ini, data berhasil diubah menjadi format yang sesuai dengan kebutuhan Graph Neural Network dan conditional diffusion model.

## 3.7 Perancangan Arsitektur Model

Arsitektur model yang dikembangkan dalam penelitian ini merupakan integrasi antara tiga komponen utama, yaitu Spatio-Temporal Graph Neural Network (STGNN), Retrieval-Augmented Mechanism, dan Conditional Diffusion Model. Desain ini dirancang khusus untuk menangani karakteristik hujan orografis di pegunungan tropis serta menghasilkan prediksi probabilistik satu jam ke depan yang akurat dan sensitif terhadap kejadian ekstrem.

### 3.7.1 Spatio-Temporal Graph Neural Network (STGNN)

Komponen pertama adalah Spatio-Temporal Graph Neural Network yang bertugas mengekstraksi fitur spasial dan temporal dari kelima node observasi. Alur pemrosesan STGNN, mulai dari masukan graph sequence, encoding spasial menggunakan Graph Attention Network (GAT), agregasi temporal, hingga pembentukan embedding spasio-temporal, ditunjukkan pada Gambar 3.7.

![Gambar 3.7 — placeholder gambar: Arsitektur Spatio-Temporal Graph Neural Network](gambar-3-7-placeholder)

**Gambar 3.7 Arsitektur Spatio-Temporal Graph Neural Network**

Gambar 3.7 menunjukkan alur arsitektur STGNN yang menerima urutan graf sebagai masukan. Alur pemrosesan dibagi menjadi lima tahap, yaitu input graph sequence, encoding spasial dengan GAT, global mean pooling, temporal attention, dan pembentukan graph embedding. Embedding yang dihasilkan digunakan sebagai kondisi tambahan pada Conditional Diffusion Model.

#### a. Input Graph Sequence

Input STGNN berupa enam snapshot graf historis. Setiap snapshot memiliki lima node dengan sembilan fitur yang telah melalui preprocessing dan normalisasi. Struktur edge dipertahankan sama pada seluruh snapshot, sedangkan nilai fitur node berubah mengikuti timestamp. Dengan demikian, input STGNN memuat dimensi node, fitur, dan urutan waktu tanpa mengubah struktur spasial pada setiap langkah.

Secara operasional, urutan snapshot yang digunakan adalah $G_{t-6},G_{t-5},\ldots,G_{t-1}$. Node MAIN pada $t-1$ juga digunakan sebagai context tambahan, sedangkan target diffusion berada pada node MAIN waktu target dan tidak menjadi bagian dari graph sequence yang diberi noise.

#### b. Encoding Spasial dengan GAT 1

Pada setiap snapshot, GAT 1 menerima matriks fitur lima node dengan sembilan fitur per node. Lapisan ini mempelajari bobot hubungan antar-node secara adaptif menggunakan empat head atensi. Setiap head menghasilkan representasi berdimensi 64, kemudian seluruh keluaran head digabungkan melalui concatenation. Proses encoding GAT 1 dapat dinyatakan dengan:

$$H^{(1)}=\mathrm{GAT}_1(G)$$

DOCX hanya menyediakan keterangan operasional `GAT_1(G)` dan tidak menyimpan formula berindeks sebagai OMML; bentuk ringkas di atas dipertahankan sebagai representasi operator.

GAT 1 memproses seluruh lima node pada setiap snapshot. Hasil penggabungan empat head menghasilkan representasi node berdimensi 256, yaitu $4\times64$. Self-loop pada lapisan ini berasal dari perilaku default GATConv, bukan dari edge eksplisit topologi star.

#### c. Encoding Spasial dengan GAT 2

GAT 2 menerima keluaran GAT 1 berdimensi 256 pada setiap node. Lapisan ini menggunakan satu head atensi tanpa concatenation untuk memproyeksikan representasi setiap node menjadi 64 dimensi. Struktur edge dan self-loop yang digunakan tetap sama dengan GAT 1. Keluaran GAT 2 diteruskan ke tahap global mean pooling. Secara operasional, keluaran GAT 2 pada snapshot $\tau$ dapat ditulis sebagai:

DOCX tidak menyimpan formula keluaran GAT 2 sebagai OMML; hanya keterangan bahwa keluaran snapshot diteruskan ke global mean pooling.

#### d. Global Mean Pooling

Setelah dua lapisan GAT selesai, keluaran masih berupa representasi tingkat node. Global mean pooling digunakan untuk mengagregasi kelima node menjadi satu representasi tingkat graf berdimensi 64 pada setiap snapshot. Operasi ini mempertahankan informasi rata-rata seluruh node dan menghasilkan satu vektor graf untuk setiap waktu. Enam vektor hasil pooling kemudian disusun kembali sebagai urutan temporal.

#### e. Temporal Attention

Representasi dari seluruh snapshot historis kemudian diproses oleh temporal attention untuk menghasilkan representasi spasio-temporal akhir:

$$h=\mathrm{TemporalAttention}(h_{t-6},\ldots,h_{t-1})$$

Formula pada DOCX tidak tersimpan sebagai OMML; enam embedding snapshot historis dikonfirmasi oleh keterangan DOCX.

Temporal attention diimplementasikan menggunakan MultiheadAttention dengan empat head. Positional embedding trainable ditambahkan sebelum attention. Causal mask mencegah suatu timestep mengakses representasi timestep setelahnya. Residual connection, dropout, dan LayerNorm digunakan pada blok temporal.

#### f. Causal Slicing Last Timestep

Setelah temporal attention memproses enam embedding snapshot, hanya representasi pada timestep terakhir yang dipilih. Timestep tersebut mewakili snapshot paling baru dalam konteks historis, yaitu $t-1$, dan digunakan sebagai ringkasan seluruh urutan tanpa mengakses informasi pada waktu target $t$. Operasi pemilihan ini disebut causal slicing last timestep dan menjaga agar conditioning tidak menggunakan informasi masa depan.

Secara operasional, keluaran temporal attention berupa sequence embedding yang memuat representasi dari enam timestep historis. Model mengambil representasi pada timestep terakhir, yaitu timestep paling baru dalam jendela observasi, sebagai ringkasan konteks temporal. Pemilihan ini memastikan bahwa conditioning hanya menggunakan informasi hingga waktu observasi terakhir dan tidak mengakses informasi pada waktu target atau masa depan.

#### g. Output Projection

Representasi hasil causal slicing berdimensi 64 diproyeksikan menjadi 128 dimensi agar kompatibel dengan context MAIN, retrieval value, dan time embedding. Proyeksi ini merupakan transformasi linear yang menghasilkan graph conditioning embedding.

Lapisan output_projection menerima embedding timestep terakhir dan memetakannya dari dimensi representasi STGNN ke dimensi kondisi model. Hasil proyeksi tersebut menjadi graph embedding yang digunakan bersama context MAIN, retrieval value, dan time embedding pada tahap conditioning. Penyamaan dimensi memungkinkan seluruh representasi tersebut digabungkan secara elemen demi elemen sebelum diteruskan ke denoiser.

Dimensi 128 digunakan sebagai ruang bersama untuk operasi penjumlahan conditioning pada tahap berikutnya.

#### h. Graph Embedding dan Conditioning

Graph embedding hasil temporal attention diproyeksikan dari 64 menjadi 128 dimensi. Context MAIN pada $t-1$ dan retrieval value juga diproyeksikan ke 128 dimensi. Ketiga representasi tersebut dijumlahkan secara element-wise, kemudian time embedding dijumlahkan pada conditioning embedding. Conditioning embedding ini diteruskan ke denoiser bersama target MAIN yang telah diberi noise.

Formulasi multi-head attention pada lapisan GAT dituliskan sebagai berikut:

$$\mathbf{h}'_i=\mathbin{\|}_{k=1}^{K}\sigma\left(\sum_{j\in\mathcal{N}_i}\alpha_{ij}^{k}\mathbf{W}^{k}\mathbf{h}_j\right)$$

DOCX tidak menyimpan formula multi-head attention sebagai OMML; keterangan yang dapat diverifikasi: empat head, masing-masing berdimensi 64, digabungkan melalui concatenation menjadi 256 dimensi.

Operasi concatenation menghasilkan representasi 256 dimensi 64 × 4 sebelum diproyeksikan oleh lapisan GAT kedua menjadi 64 dimensi. Detail dimensi tersebut merupakan konfigurasi implementasi dan bukan klaim bahwa konfigurasi tersebut optimal tanpa pengujian pembanding.

### 3.7.2 Retrieval-Augmented Dan Conditional Diffusion Model

Untuk meningkatkan kemampuan model dalam menangani kejadian ekstrem, mekanisme retrieval historical analogs digunakan. Alur integrasi retrieval dengan representasi STGNN dan Conditional Diffusion Model ditunjukkan pada Gambar 3.8. Komponen ini mencari kondisi historis yang paling mirip dengan kondisi saat ini dari basis data pelatihan, kemudian menggunakan analog tersebut sebagai informasi pengondisian tambahan pada proses denoising.

![Gambar 3.8 — placeholder gambar: Arsitektur Retrieval-Augmented Diffusion Model](gambar-3-8-placeholder)

**Gambar 3.8 Arsitektur Retrieval-Augmented Diffusion Model**

Gambar 3.8 menunjukkan alur Retrieval-Augmented Diffusion Model. Alur pembahasan mengikuti urutan pembentukan graph embedding, context embedding, retrieval embedding, condition embedding, time embedding, total embedding, dan denoising. Detail pembentukan graph embedding mengacu pada subbab 3.7.1 Spatio-Temporal Graph Neural Network (STGNN); bagian ini menjelaskan pemanfaatannya dalam arsitektur diffusion.

#### 3.7.2.2 Pembentukan Graph Embedding Menggunakan ST-GNN

Input ST-GNN berupa enam snapshot graf historis dengan lima node dan sembilan fitur per node. Proses pembentukan graph sequence, GAT 1, GAT 2, global mean pooling, temporal attention, causal slicing, dan output projection telah dijelaskan pada subbab 3.7.1 Spatio-Temporal Graph Neural Network (STGNN). Pada subbab ini, keluaran proses tersebut digunakan sebagai graph embedding berdimensi 128 melalui Graph MLP. Target node MAIN tidak digunakan sebagai masukan graph embedding.

Graph MLP memproses keluaran graph dari STGNN agar berada pada ruang embedding yang sama dengan context dan retrieval. Hasilnya merupakan representasi informasi spasio-temporal yang digunakan pada tahap integrasi condition embedding.

#### 3.7.2.3 Pembentukan Context Embedding

Tahap ini menjelaskan pembentukan representasi embedding dari fitur cuaca terkini pada node MAIN. Prosesnya meliputi penentuan masukan context, pemetaan melalui Context MLP, dan pembentukan embedding yang digunakan pada tahap integrasi kondisi.

##### a. Context Input (Main Features)

Context input berupa sembilan fitur node MAIN pada timestep observasi terakhir, yaitu $t-1$. Context ini tidak memuat target waktu $t$ dan digunakan sebagai representasi kondisi cuaca terkini serta query untuk retrieval.

##### b. Context MLP

Context input diproses menggunakan Context MLP yang memproyeksikan vektor sembilan dimensi ke ruang embedding berdimensi 128. Transformasi ini menyamakan dimensi context dengan graph embedding dan retrieval embedding sebelum ketiganya digabungkan.

##### c. Transformasi Fitur Menjadi Embedding

Context MLP menghasilkan context embedding yang memuat kondisi meteorologis node MAIN pada waktu observasi terakhir. Embedding tersebut diteruskan ke tahap integrasi condition embedding dan tidak digunakan untuk menggantikan graph embedding.

#### 3.7.2.4 Pembentukan Retrieval Embedding

Tahap ini menjelaskan perubahan hasil retrieval historis menjadi embedding yang dapat digabungkan dengan graph embedding dan context embedding. Pembahasan dimulai dari bentuk input retrieval, dilanjutkan dengan pemetaan melalui Retrieval MLP dan pembentukan representasi retrieval.

##### a. Retrieval Input (Top-3 × 3 Targets)

Context node MAIN digunakan untuk mencari analog historis pada basis data training. Setiap hasil retrieval menyimpan tiga value target, yaitu hujan, kecepatan angin, dan kelembapan relatif. Dengan tiga tetangga terdekat, retrieval input memiliki bentuk Top-3 × 3 target. Proses pengambilan tetangga terdekat diformulasikan sebagai:

$$R=\mathrm{kNN}(c,D,k)$$

Formula DOCX yang dapat diverifikasi adalah $R=\mathrm{kNN}(c,D,k)$; dimensi input/output dijelaskan terpisah sebagai query 9 fitur, $k=3$, dan tiga target per tetangga.

Mekanisme ini menyediakan informasi keluaran historis yang memiliki kemiripan dengan kondisi saat ini. Pengaruh retrieval terhadap performa model tetap ditentukan melalui skenario pengujian.

Pencarian analog historis diimplementasikan menggunakan indeks FAISS IndexFlatL2, yang menghitung jarak kuadrat Euclidean antara vektor kondisi saat ini $\mathbf{q}\in\mathbb{R}^{9}$ dan setiap kunci historis data pelatihan $\mathbf{k}_i\in\mathbb{R}^{9}$:

$$d(\mathbf{q},\mathbf{k}_i)=\lVert\mathbf{q}-\mathbf{k}_i\rVert_2^2$$

Formula DOCX yang dapat diverifikasi adalah $d(\mathbf{q},\mathbf{k}_i)=\lVert\mathbf{q}-\mathbf{k}_i\rVert_2^2$ (jarak kuadrat Euclidean).

Basis indeks dibangun hanya dari data pelatihan. Key berupa fitur ternormalisasi node MAIN berdimensi sembilan pada waktu $t$ sedangkan value berupa target ternormalisasi node MAIN pada waktu $t+1$ berdimensi tiga. Exact search menggunakan squared L2 dengan IndexFlatL2 dan mengambil $K=3$ kandidat. Filter training menggunakan strict-past dan `exclude_self`. Tidak digunakan PCA, reduksi ruang retrieval, learned retrieval encoder, atau metric learning.

##### b. Retrieval MLP

Tiga value retrieval diratakan menjadi vektor berdimensi sembilan dan diproses oleh Retrieval MLP. Retrieval MLP memproyeksikan vektor tersebut ke embedding berdimensi 128.

##### c. Representasi Informasi Retrieval

Retrieval embedding merepresentasikan tiga keluaran target dari analog historis terdekat. Representasi ini digunakan sebagai kondisi tambahan dan tidak menggantikan context input atau graph embedding.

### 3.7.2.5 Integrasi Condition Embedding

Setelah graph embedding, context embedding, dan retrieval embedding tersedia pada ruang dimensi yang sama, ketiganya diintegrasikan menjadi satu condition embedding. Tahap berikut menjelaskan kontribusi masing-masing embedding dan proses penggabungannya.

#### a. Penggabungan Graph Embedding

Graph embedding hasil ST-GNN dimasukkan ke ruang integrasi berdimensi 128 melalui Graph MLP.

#### b. Penggabungan Context Embedding

Context embedding dari fitur MAIN di jam ke $t-1$ dipertahankan pada ruang berdimensi 128 dan disiapkan untuk dijumlahkan dengan embedding lainnya.

#### c. Penggabungan Retrieval Embedding

Retrieval embedding dari Top-3 × 3 target dipetakan ke ruang berdimensi 128 melalui Retrieval MLP.

#### d. Pembentukan Condition Embedding

Ketiga embedding tersebut dijumlahkan secara elemen demi elemen. Hasil penjumlahan menjadi condition embedding yang memuat informasi graph, kondisi MAIN, dan analog historis. Dimensi target diffusion tetap tiga dan tidak berubah pada tahap ini.

### 3.7.2.6 Pembentukan Time Embedding

Selain kondisi cuaca, retrieval, dan graf, denoiser memerlukan informasi mengenai posisi proses diffusion. Section ini menjelaskan pembentukan representasi timestep melalui sinusoidal embedding dan Time MLP.

#### a. Diffusion Timestep $t$

Pada setiap langkah pelatihan, timestep diffusion dipilih untuk menentukan tingkat noise pada target. Timestep tersebut menjadi masukan terpisah dari condition embedding.

#### b. Time MLP

Timestep diubah menjadi sinusoidal embedding, kemudian diproses oleh Time MLP yang memetakan embedding berdimensi 128 ke 256 dimensi dan kembali ke 128 dimensi menggunakan aktivasi GELU.

#### c. Representasi Timestep

Keluaran Time MLP menjadi time embedding berdimensi 128. Embedding ini merepresentasikan posisi proses diffusion yang sedang diproses oleh denoiser. Aktivasi GELU pada Time MLP dirumuskan sebagai:

$$\mathrm{GELU}(x)=x\Phi(x)$$

Formula DOCX yang dapat diverifikasi adalah $\mathrm{GELU}(x)=x\Phi(x)$; $\Phi$ dipertahankan sebagai fungsi distribusi normal baku.

Karakteristik ini relevan karena timestep diffusion merepresentasikan tingkat noise Gaussian yang ditambahkan pada data.

### 3.7.2.7 Pembentukan Total Embedding

Condition embedding yang telah terbentuk kemudian digabungkan dengan time embedding. Hasil penggabungan ini menjadi representasi kondisi akhir yang digunakan dalam proses denoising.

#### a. Integrasi Time Embedding

Time embedding dijumlahkan dengan condition embedding setelah keduanya berada pada dimensi 128.

#### b. Integrasi Condition Embedding

Condition embedding yang memuat graph, context, dan retrieval dipertahankan sebagai dasar pengondisian diffusion.

#### c. Total Embedding sebagai Conditioning Akhir

Hasil penjumlahan time embedding dan condition embedding disebut total embedding. Total embedding menjadi conditioning akhir yang digunakan oleh denoiser MLP dan tidak diberi noise.

### 3.7.2.8 Proses Denoising Menggunakan Denoiser MLP

Setelah total embedding tersedia, proses berikutnya adalah pemetaan noisy target menjadi estimasi noise. Section ini menguraikan aliran data melalui setiap bagian Denoiser MLP, mulai dari input hingga predicted noise.

#### a. Denoiser Input (Noisy Target)

Target ternormalisasi node MAIN berdimensi tiga diberi noise Gaussian pada timestep yang dipilih. Hasilnya menjadi noisy target yang diterima denoiser. Graph sequence, context, dan retrieval tidak diberi noise. Forward diffusion dituliskan sebagai:

$$x_s=\sqrt{\bar{\alpha}_s}\,x_0+\sqrt{1-\bar{\alpha}_s}\,\epsilon$$

Formula DOCX yang dapat diverifikasi adalah $x_s=\sqrt{\bar{\alpha}_s}\,x_0+\sqrt{1-\bar{\alpha}_s}\,\epsilon$; notasi DDPM dipertahankan.

#### b. Down1

Noisy target berdimensi tiga diproyeksikan melalui `down1` menjadi representasi berdimensi 128.

#### c. Integrasi Total Embedding (+)

Total embedding berdimensi 128 dijumlahkan secara elemen demi elemen dengan keluaran down1. Operasi ini memasukkan seluruh kondisi model ke representasi noisy target.

#### d. Down2

Hasil integrasi diproses oleh down2 dan diperluas dari 128 menjadi 256 dimensi.

#### e. Mid Layer

Representasi berdimensi 256 diproses oleh mid layer dengan dimensi yang sama untuk mempelajari transformasi nonlinier lanjutan.

#### f. Skip Connection

Keluaran mid layer dipertahankan untuk digabungkan dengan keluaran down2. Koneksi ini menyediakan jalur informasi tambahan pada proses pemetaan kembali menuju dimensi keluaran.

#### g. Concatenate

Keluaran mid layer dan down2 digabungkan menggunakan concatenation, bukan penjumlahan. Dua representasi berdimensi 256 menghasilkan vektor berdimensi 512.

#### h. Up1

Vektor berdimensi 512 diproyeksikan melalui up1 menjadi 128 dimensi.

#### i. Predicted Noise

Lapisan keluaran memetakan representasi 128 dimensi menjadi prediksi noise berdimensi tiga. Prediksi tersebut digunakan scheduler untuk memperbarui noisy target pada setiap langkah reverse diffusion.

### 3.7.2.9 Reverse Diffusion dan Pembentukan Ensemble

Pada inferensi, proses reverse diffusion dimulai dari noise random berdimensi tiga. Total embedding yang sama digunakan pada setiap anggota ensemble, sedangkan noise awal diacak secara berbeda. Denoiser memperkirakan noise pada setiap langkah reverse diffusion, kemudian scheduler memperbarui target bernoise hingga menghasilkan satu sampel prediksi. Proses tersebut diulang untuk seluruh anggota ensemble. Dengan demikian, median, P10, P90, CRPS, dan peluang kejadian dihitung dari kumpulan sampel, bukan dari satu keluaran deterministik.

## 3.7.3 Integrasi Antar Komponen Model

Ketiga komponen bekerja secara terintegrasi. Representasi dari STGNN dan hasil retrieval menjadi conditioning input bagi diffusion model, sehingga prediksi yang dihasilkan tidak hanya probabilistik tetapi juga kontekstual terhadap dinamika spasial dan historis di kawasan Gunung Gede–Pangrango. Pendekatan ini memungkinkan model mempelajari distribusi kondisional berikut:

$$p(y_t\mid X_t)$$

Formula DOCX yang dapat diverifikasi adalah $p(y_t\mid X_t)$; subskrip target dan input dipertahankan.

Dengan arsitektur yang terintegrasi ini, model menghasilkan sampel prediksi probabilistik untuk dievaluasi dari sisi akurasi titik, kualitas distribusi, dan deteksi kejadian hujan.

## 3.8 Prosedur Pelatihan Model

Setelah arsitektur model dirancang, tahap pelatihan dilakukan untuk mengoptimalkan parameter model agar mampu mempelajari pola kompleks dari data spasio-temporal serta menghasilkan prediksi probabilistik yang akurat. Proses pelatihan menggunakan data pelatihan yang telah melalui preprocessing dan representasi graf, dengan tujuan utama meminimalkan kesalahan prediksi sekaligus meningkatkan sensitivitas terhadap kejadian ekstrem yang berpotensi memicu hipotermia pendaki.

Proses pelatihan diawali dengan pembentukan sampel berupa graph sequence dari enam snapshot historis $t-6$ hingga $t-1$. Setiap snapshot memuat lima node dengan sembilan fitur. Context tambahan diambil dari node MAIN pada waktu $t-1$, sedangkan target yang diprediksi adalah tiga variabel node MAIN pada waktu target $t$. Model kemudian melakukan forward pass yang meliputi ekstraksi representasi oleh STGNN, pencarian analog historis, dan prediksi noise pada Conditional Diffusion Model.

Pada setiap batch, target cuaca terstandardisasi node MAIN pada waktu target, $\mathbf{y}\in\mathbb{R}^{3}$, diubah secara dinamis menjadi noisy target. Noise hanya ditambahkan pada target tersebut, bukan pada graf atau seluruh fitur input. Pertama, noise $\epsilon\sim\mathcal{N}(0,\mathbf{I})$ diundi dengan dimensi identik dengan target. Kedua, timestep diffusion $s$ diundi secara seragam pada rentang 0 hingga 999. Ketiga, scheduler DDPM membentuk masukan denoiser melalui:

$$\mathbf{x}_s=\sqrt{\bar{\alpha}_s}\,\mathbf{y}+\sqrt{1-\bar{\alpha}_s}\,\boldsymbol{\epsilon}$$

Formula DOCX yang dapat diverifikasi adalah $\mathbf{x}_s=\sqrt{\bar{\alpha}_s}\,\mathbf{y}+\sqrt{1-\bar{\alpha}_s}\,\boldsymbol{\epsilon}$; garis atas dan indeks dipertahankan sesuai notasi DDPM.

Tensor $\mathbf{x}$ selanjutnya digunakan untuk melatih denoiser dalam menaksir noise $\epsilon$.

Konfigurasi pelatihan model ditetapkan sebagaimana ditunjukkan pada Tabel 3.4. Parameter tersebut digunakan secara konsisten pada seluruh skenario yang melibatkan pelatihan model agar perbandingan kinerja dapat dilakukan secara adil dan dapat direplikasi.

**Tabel 3.5 Konfigurasi Pelatihan Model**

| Parameter | Nilai | Keterangan |
|---|---|---|
| Optimizer | AdamW | Optimizer pembaruan parameter model |
| Weight decay | $1\times10^{[\text{TEKS PDF TIDAK TERBACA: pangkat}] }$ | Regularisasi parameter optimizer |
| Learning rate | 0,001 | Laju pembelajaran awal |
| Batch size | 512 | Jumlah sampel per pembaruan parameter |
| Epoch | 20 | Jumlah maksimum putaran pelatihan |
| Early stopping patience | 12 | Batas epoch tanpa perbaikan validasi |
| Lookback window | $L=6$ jam | Panjang konteks observasi historis |
| FAISS neighbors | $k=3$ | Jumlah analog historis yang diambil |
| Diffusion train steps | 1000 | Jumlah langkah proses diffusion saat pelatihan |
| Diffusion inference steps | 20 | Jumlah langkah sampling saat inferensi |
| Ensemble size | 30 sampel | Jumlah sampel prediksi probabilistik |
| LR scheduler | ReduceLROnPlateau | Penyesuaian learning rate berdasarkan metrik validasi |
| Gradient clipping | 1,0 | Batas norma gradien untuk menjaga stabilitas pelatihan |
| Conditioning dropout | 0,15 | Peluang penghilangan kondisi saat pelatihan diffusion |
| Auxiliary wet/dry threshold | 0,1 mm/jam | Ambang klasifikasi kejadian hujan |
| Auxiliary wet/dry weight | 0,7 | Bobot loss auxiliary wet/dry |

Rujukan internal tidak konsisten: paragraf DOCX menyebut Tabel 3.4, sedangkan caption tabel DOCX menyebut Tabel 3.5; keduanya dipertahankan.

Parameter normalisasi dan basis retrieval hanya dihitung dari data pelatihan untuk mencegah data leakage. Pada akhir setiap epoch, model dievaluasi menggunakan data validasi. Mekanisme early stopping dan ReduceLROnPlateau menggunakan perkembangan metrik validasi untuk menghindari pelatihan berlebih dan menyesuaikan laju pembelajaran. Model dengan performa validasi terbaik disimpan untuk digunakan pada tahap inferensi.

Weighted denoising loss memberikan bobot 5 kali untuk target ternormalisasi dengan nilai absolut lebih dari 1,0 dan 10 kali untuk nilai absolut lebih dari 3,0. Pembobotan ini meningkatkan penekanan pada target besar, tetapi tidak mengatasi kelangkaan informasi kejadian ekstrem dalam data. Dengan auxiliary task wet/dry dan pemilihan model berdasarkan validasi, proses pelatihan ditujukan untuk meningkatkan sensitivitas terhadap kejadian berisiko tinggi.

## 3.9 Metode Evaluasi Model

Evaluasi model dilakukan untuk mengukur kemampuan sistem dalam memprediksi kondisi meteorologis pada node utama (MAIN) secara akurat dan andal. Mengingat model menghasilkan prediksi dalam bentuk distribusi probabilistik, evaluasi tidak hanya mencakup akurasi titik (point forecast), tetapi juga kualitas distribusi probabilitas dan kemampuan deteksi kejadian ekstrem. Seluruh evaluasi dilakukan secara eksklusif menggunakan data pengujian (test set) yang tidak pernah digunakan selama pelatihan maupun pemilihan model [6], [7], [25].

Evaluasi model dibagi menjadi tiga kelompok utama: evaluasi deterministik, evaluasi probabilistik, dan evaluasi berbasis kejadian. Selain itu, dilakukan pula analisis reliabilitas distribusi prediksi.

### a. Evaluasi Deterministik

Evaluasi deterministik mengukur kedekatan antara prediksi titik (median dari ensemble) dengan nilai observasi aktual. Metrik yang digunakan meliputi:

1. Mean Absolute Error (MAE)
2. Root Mean Square Error (RMSE)
3. Pearson Correlation Coefficient ($r$)

### b. Evaluasi Probabilistik

Evaluasi probabilistik menilai kualitas distribusi prediksi yang dihasilkan oleh diffusion model.

1. Continuous Ranked Probability Score (CRPS)
2. Brier Score

### c. Evaluasi Berbasis Kejadian Hujan

Evaluasi ini menilai kemampuan model mendeteksi kejadian hujan pada berbagai tingkat intensitas (ambang 2 mm, 5 mm, dan 10 mm). Metrik yang digunakan adalah:

1. **Probability of Detection (POD):** Proporsi kejadian hujan yang berhasil dideteksi.
2. **False Alarm Ratio (FAR):** Proporsi alarm palsu.
3. **Critical Success Index (CSI):** Ukuran keseluruhan keberhasilan deteksi.

### d. Evaluasi Reliabilitas Prediksi

Reliabilitas dinilai menggunakan Reliability Diagram yang membandingkan probabilitas prediksi dengan frekuensi kejadian aktual. Diagram ini menunjukkan sejauh mana probabilitas yang dihasilkan model sesuai dengan realisasi observasi di lapangan.

**Tabel 3.6 Ringkasan Metrik Evaluasi**

| Kelompok Evaluasi | Metrik Utama | Tujuan Utama |
|---|---|---|
| Deterministik | MAE, RMSE, Pearson Correlation | Akurasi prediksi titik |
| Probabilistik | CRPS, Brier Score | Kualitas distribusi probabilitas |
| Berbasis Kejadian | POD, FAR, CSI | Kemampuan deteksi kejadian hujan |
| Reliabilitas | Reliability Diagram | Kalibrasi probabilitas |

Evaluasi dilakukan dengan pendekatan one-step rolling forecast pada data pengujian. Model menggunakan enam jam observasi terakhir untuk memprediksi satu jam berikutnya ($t+1$). Untuk hasil utama, titik evaluasi diambil setiap 11 jam, parameter ini hanya mengatur jarak antar sampel evaluasi untuk mengurangi bias akibat autokorelasi, bukan horizon prediksi. Evaluasi penuh setiap jam tetap didukung melalui `eval_step=1`. Seluruh skenario menggunakan titik evaluasi yang sama. Dalam penggunaan operasional, apabila sumber data near real-time tersedia, model dapat dijalankan setiap jam dengan rolling window enam jam terakhir.

Dengan metode evaluasi yang komprehensif ini, penelitian dapat memberikan gambaran yang lengkap mengenai performa model, baik dari sisi akurasi, kalibrasi probabilitas, maupun kemampuan deteksi kejadian ekstrem yang relevan dengan mitigasi risiko hipotermia pendaki di Gunung Gede–Pangrango.

### 3.9.2 Skenario Eksperimen

Skenario pengujian dirancang untuk membandingkan model usulan dengan tiga arsitektur pembanding yang mewakili pemodelan dependensi temporal, pemodelan retrieval-probabilistik, dan pemodelan spasial-temporal. Keempat model menerima data penelitian, target prediksi, dan protokol evaluasi yang sama. Perbedaan antarmodel dibatasi pada komponen arsitektur yang diuji agar perbandingan kinerja dapat dilakukan secara adil.

Seluruh model menggunakan pembagian dataset temporal, normalisasi, jendela observasi enam jam, horizon prediksi satu jam, target node MAIN, dan tiga variabel keluaran yang sama. Model probabilistik menghasilkan ensemble prediksi dengan jumlah sampel serta prosedur sampling yang ditetapkan pada konfigurasi penelitian. Model yang tidak menghasilkan ensemble secara alami dikonversi ke keluaran probabilistik melalui prosedur yang ditetapkan dalam implementasi pengujian. Evaluasi dilakukan pada titik waktu yang sama menggunakan MAE, RMSE, Pearson Correlation, CRPS, Brier Score, POD, FAR, CSI, dan Reliability Diagram.

Tabel 3.6 menyajikan empat model yang dibandingkan. Kolom hasil dikosongkan untuk diisi setelah seluruh proses pelatihan, inferensi, dan evaluasi selesai.

**Tabel 3.7 Tabel Skenario Pengujian Model**

| Model Pengujian | Hasil Pengujian |
|---|---:|
| Multi-node Long Short-Term Memory + Attention | - |
| Retrieval-Augmented Diffusion Model | - |
| Spatio-Temporal Graph Neural Network | - |
| Retrieval-Augmented Diffusion dengan STGNN | - |

Multi-node Long Short-Term Memory + Attention digunakan untuk menguji kemampuan model dalam menangkap dependensi temporal dari beberapa node melalui mekanisme perhatian. Retrieval-Augmented Diffusion Model digunakan untuk mengukur kontribusi retrieval historical analog dan diffusion tanpa pengondisian graf. Spatio-Temporal Graph Neural Network digunakan untuk menilai kontribusi representasi hubungan spasial-temporal tanpa mekanisme retrieval dan diffusion. Retrieval-Augmented Diffusion dengan STGNN merupakan model usulan yang mengintegrasikan ketiga komponen tersebut.

Perbandingan hasil dilakukan berdasarkan dua kelompok keluaran. Median ensemble digunakan sebagai ringkasan point forecast untuk MAE, RMSE, dan Pearson Correlation. Seluruh anggota ensemble digunakan untuk menghitung CRPS, Brier Score, POD, FAR, CSI, serta Reliability Diagram. Dengan demikian, hasil pengujian tidak hanya menunjukkan kedekatan nilai prediksi terhadap observasi, tetapi juga kualitas distribusi probabilitas dan kemampuan deteksi kejadian hujan.

Hasil pengujian selanjutnya disajikan dalam tabel perbandingan metrik, grafik prediksi terhadap observasi, rentang P10–P90, dan reliability diagram. Analisis diarahkan untuk menentukan model yang paling mampu merepresentasikan dinamika temporal, hubungan spasial, serta ketidakpastian hujan pada wilayah penelitian.

## 3.10 Rancangan Visualisasi Hasil Prediksi Berbasis Web

Visualisasi hasil prediksi dirancang sebagai sarana penyampaian informasi nowcasting yang dapat mendukung interpretasi keluaran model. Rancangan ini memisahkan proses pemodelan dari proses penyajian hasil: pipeline penelitian menghasilkan artefak prediksi probabilistik, sedangkan aplikasi web menampilkan ringkasan informasi tersebut dalam bentuk yang mudah dipahami. Pengembangan visualisasi berbasis web ditetapkan sebagai arah lanjutan penelitian dan tidak menjadi bagian dari evaluasi kinerja model pada subbab sebelumnya.

Arsitektur yang direncanakan menggunakan FastAPI sebagai backend dan Vue.js sebagai frontend. FastAPI menyediakan endpoint untuk mengakses hasil inferensi. Vue.js merender data tersebut menjadi kartu kondisi cuaca, grafik deret waktu, indikator risiko, dan tabel prediksi. Pemisahan backend dan frontend digunakan untuk menjaga modularitas aplikasi.

![Gambar 3.6 — placeholder gambar: Mockup Dashboard Visualisasi Hasil Nowcasting](gambar-3-6-mockup-placeholder)

**Gambar 3.6 Mockup Dashboard Visualisasi Hasil Nowcasting**

Gambar 3.6 menunjukkan rancangan awal dashboard visualisasi hasil nowcasting. Halaman dirancang untuk menampilkan informasi lokasi dan waktu pembaruan, kondisi cuaca terkini, prediksi hujan, kecepatan angin, serta kelembapan relatif pada node MAIN. Grafik prediksi digunakan untuk membandingkan perubahan antarwaktu, sedangkan indikator risiko menyajikan interpretasi ringkas terhadap kondisi yang berpotensi membahayakan pendaki.

Dengan rancangan tersebut, keluaran probabilistik model tidak hanya tersedia sebagai nilai numerik, tetapi dapat dikomunikasikan sebagai informasi pendukung pengambilan keputusan sebelum dan selama aktivitas pendakian.

Pada tahap implementasi lanjutan, dashboard perlu memvalidasi respons API, menampilkan status data terakhir, dan membedakan secara jelas antara observasi dengan prediksi. Apabila sumber data near real-time tersedia, FastAPI dapat memperbarui data prediksi secara berkala dan Vue.js menampilkan perubahan tersebut pada antarmuka. Namun, karena penelitian ini menggunakan ERA5 sebagai data reanalysis historis, mockup yang ditampilkan berfungsi sebagai rancangan konseptual visualisasi dan bukan sistem peringatan dini operasional.

---

## Catatan verifikasi DOCX

Sebanyak 13 persamaan (2.5, 2.6, 2.10, 2.12–2.21) dan isi visual/data Tabel 3.3 tidak dapat diverifikasi karena elemen tersebut tidak tersimpan sebagai struktur OMML/tabel yang dapat dibaca dalam DOCX. Marker tetap dipertahankan. Rujukan konfigurasi Tabel 3.4/Tabel 3.5 tetap ambigu di sumber.


# Daftar Pustaka

[1] E. Procter, H. Brugger, and M. Burtscher, “Accidental hypothermia in recreational activities in the mountains : A narrative review,” no. August, pp. 2464–2472, 2018, doi: 10.1111/sms.13294.

[2] Aminullah, A. Ayumar, A. Y. Kasma, and E. Samaliwu, “Overview Of Knowledge About First Aid For Hypothermia In Mountain Climbers In Makassar,” vol. XVI, pp. 180–190, 2025.

[3] D. Luciano and D. L. Giovanna, “Rainfall nowcasting model for early warning systems applied to a case over Central Italy,” Nat. Hazards, vol. 112, no. 1, pp. 501–520, 2022, doi: 10.1007/s11069-021-05191-w.

[4] P. Chavula, F. Kayusi, G. Lungu, and A. Uwimbabazi, “The Current Landscape of Early Warning Systems and Traditional Approaches to Disaster Detection,” 2025, doi: 10.62486/latia202577.

[5] M. Reichstein et al., “Early warning of complex climate risk with integrated artificial intelligence,” Nat. Commun., no. May 2024, 2025, doi: 10.1038/s41467-025-57640-w.

[6] S. Ravuri et al., “Skilful precipitation nowcasting using deep generative models of radar,” Nature, vol. 597, no. February, 2021, doi: 10.1038/s41586-021-03854-z.

[7] Y. Zhang, M. Long, K. Chen, L. Xing, and R. Jin, “Skilful nowcasting of extreme precipitation with NowcastNet,” vol. 619, no. September 2022, 2023, doi: 10.1038/s41586-023-06184-4.

[8] A. Mazza, A. Antonini, S. Melani, and A. Ortolani, “A Radar-Based Fast Code for Rainfall Nowcasting over the Tuscany Region,” pp. 1–24, 2025.

[9] A. P. Lakspriyanti, M. Ekayani, and A. Sunkar, “CARRYING CAPACITY ASSESSMENT OF CIBEUREUM WATERFALL TOURISM IN GUNUNG GEDE PANGRANGO NATIONAL PARK,” vol. 25, no. 3, pp. 203–211, 2020, doi: 10.29244/medkon.25.3.203-211.

[10] D. Sun, J. Wu, H. Huang, R. Wang, F. Liang, and H. Xinhua, “Prediction of Short-Time Rainfall Based on Deep Learning,” vol. 2021, 2021, doi: 10.1155/2021/6664413.

[11] Q. Nicolas and W. R. Boos, “Understanding the Spatiotemporal Variability of Tropical Orographic Rainfall Using Convective Plume Buoyancy,” pp. 1737–1757, 2024, doi: 10.1175/JCLI-D-23-0340.1.

[12] C. L. Tsai, G. Lee, K. Kim, H. Park, H. Park, and W. Bang, “Association Between Upstream Conditions and the Intensity of Orographic Precipitation in the Main Mountain Ranges of South Korea,” 2025, doi: 10.1029/2024EA003989.

[13] L. Silva, R. Célleri, and M. Córdova, “Diurnal to seasonal meteorological cycles along an equatorial Andean elevational gradient,” vol. 48, pp. 33–48, 2025.

[14] X. Zhang, M. Xu, S. Kang, H. Wu, and H. Han, “The spatiotemporal variability in precipitation gradients based on meteorological station observations in mountainous areas of Northwest China,” 2023.

[15] Y. Jiang et al., “Characterizing basin-scale precipitation gradients in the Third Pole region using a high-resolution atmospheric simulation-based dataset,” pp. 4587–4601, 2022.

[16] I. Price et al., “Probabilistic weather forecasting with machine learning,” Nature, vol. 637, no. April 2024, pp. 8–11, 2025, doi: 10.1038/s41586-024-08252-9.

[17] X. Zhong et al., “FuXi-ENS : A machine learning model for efficient and accurate ensemble weather prediction,” pp. 1–14, 2025, doi: 10.1126/sciadv.adu2854.

[18] O. A. Wani et al., “Predicting rainfall using machine learning , deep learning , and time series models across an altitudinal gradient in the North-Western Himalayas,” 2024.

[19] L. He et al., “Deep Learning-Based Feature Importance for Rainfall Nowcast Driven by GNSS,” IEEE J. Sel. Top. Appl. Earth Obs. Remote Sens., vol. 18, pp. 26688–26698, 2025, doi: 10.1109/JSTARS.2025.3621857.

[20] H. Kim, S. Yoon, Y. H. Gu, S. H. Kim, and Y. Choi, “A Hybrid Approach to Physical and Deep Learning Models for Radar-Based Precipitation Nowcasting,” IEEE Trans. Geosci. Remote Sens., vol. 63, pp. 1–16, 2025, doi: 10.1109/TGRS.2025.3560454.

[21] Z. Zhang, Q. Song, M. Duan, H. Liu, and J. Huo, “Deep Learning Model for Precipitation Nowcasting Based on Residual and Attention Mechanisms,” pp. 1–17, 2025.

[22] J. H. Meltzer and J. D. Forrester, “Human-Factor Risk Mitigation in Outdoor Climbing Areas : Survey of Existing Policies in Regulated Climbing Areas,” vol. 32, no. 4, 2021, doi: 10.1016/j.wem.2021.08.001.

[23] E. Rahmah, E. K. S. H. Muntasib, and S. B. Rushayati, “Tourism Hazard Mitigation in Mount Rinjani National Park ,” vol. 2, no. 2, pp. 5–19, 2021, doi: 10.22158/sshsr.v2n2p5.

[24] K. Hanly and G. Mcdowell, “The Evolution of ‘ Riskscapes ’: 100 years of climate change and mountaineering activity in the Lake Louise area of the Canadian Rockies,” pp. 1–25, 2023.

[25] A. Asperti, F. Merizzi, A. Paparella, and G. Pedrazzi, “Precipitation nowcasting with generative diffusion models,” Appl. Intell., 2024, doi: https://doi.org/10.1007/s10489-024-06048-y.

[26] U. Yousaf, A. De Rango, G. Mendicino, L. Furnari, D. D. Ambrosio, and A. Senatore, “Spatio-temporal graph neural networks to improve precipitation forecasts from numerical models,” Soft Comput., vol. 29, no. 9, pp. 4481–4494, 2025, doi: 10.1007/s00500-025-10635-7.

[27] J. Liu, L. Yang, H. Li, and S. Hong, “Retrieval-augmented diffusion models for time series forecasting,” no. NeurIPS, pp. 1–15, 2024.

[28] S. Zhao, S. Saha, Z. Xiong, N. Boers, and X. X. Zhu, “Exploring Geometric Deep Learning For Precipitation Nowcasting,” 2023.

[29] W. Li, P. Zhang, H. Dong, Y. Jia, and W. Cao, “RSDF-AM-LSTM : Regional Scale Division Rainfall Forecasting Using Attention and LSTM,” vol. 2, no. 4, 2022.

[30] S. Haji-aghajany, W. Rohm, P. Lipinski, and M. Kryza, “Beyond the horizon : A comprehensive analysis of artificial intelligence-based weather forecasting models,” Eng. Appl. Artif. Intell., vol. 162, no. PA, p. 112335, 2025, doi: 10.1016/j.engappai.2025.112335.

[31] S. P. Ashok and S. Pekkat, “A systematic quantitative review on the performance of some of the recent short-term rainfall forecasting techniques,” J. Water Clim. Chang., vol. 13, no. 8, 2022, doi: 10.2166/wcc.2022.302.

[32] M. Bonavita, “On Some Limitations of Current Machine Learning Weather Prediction Models,” 2024, doi: 10.1029/2023GL107377.

[33] S. Rasp, P. D. Dueben, S. Scher, J. A. Weyn, J. Mouatadid, and N. Thuerey, “WeatherBench: A Benchmark Data Set for Data-Driven Weather Forecasting Journal of Advances in Modeling Earth Systems,” 2020, doi: 10.1029/2020MS002203.

[34] Z. Ben Bouallègue et al., “The Rise of Data-Driven Weather Forecasting: A First Statistical Assessment of Machine Learning–Based Weather Forecasts in an Operational-Like Context,” pp. 864–883, 2024, doi: 10.1175/BAMS-D-23-0162.1.

[35] M. Dumont, M. Saadi, L. Oudin, P. Lachassagne, B. Nugraha, and A. Fadillah, “Assessing rainfall global products reliability for water resource management in a tropical volcanic mountainous catchment,” J. Hydrol. Reg. Stud., vol. 40, no. February, 2022, doi: 10.1016/j.ejrh.2022.101037.

[36] Q. Nicolas and W. R. Boos, “Sensitivity of tropical orographic precipitation to wind speed with implications for future projections,” pp. 231–244, 2025.

[37] E. Yulihastin, T. W. Hadi, N. S. Ningsih, and M. R. Syahputra, “Early morning peaks in the diurnal cycle of precipitation over the northern coast of West Java and possible influencing factors,” pp. 231–242, 2020.

[38] D. Hendrycks and K. Gimpel, “Gaussian Error Linear Units (GELUs),” pp. 1–10, 2016.

[39] J. Ho, A. Jain, and P. Abbeel, “Denoising Diffusion Probabilistic Models,” vol. 256, 2020.

[40] S. Elfwing, E. Uchibe, and K. Doya, “Sigmoid-weighted linear units for neural network function approximation in reinforcement learning,” Neural Networks, vol. 107, pp. 3–11, 2018, doi: 10.1016/j.neunet.2017.12.012.

[41] S. Wagner-carena, A. Akhmetzhanova, and S. Erickson, “A Data-Driven Prism : Multi-View Source Separation with Diffusion Model Priors,” no. NeurIPS, 2025.

[42] X. Li, Y. Dai, and Q. Qu, “Understanding Generalizability of Diffusion Models Requires Rethinking the Hidden Gaussian Structure,” no. NeurIPS, pp. 1–33, 2024.

[43] A. Verdone, S. Scardapane, and M. Panella, “Explainable Spatio-Temporal Graph Neural Networks for multi-site photovoltaic energy production,” Appl. Energy, vol. 353, no. PB, p. 122151, 2024, doi: 10.1016/j.apenergy.2023.122151.

[44] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, and Y. Bengio, “Graph Attention Network,” pp. 1–12, 2018.

[45] M. Mukhaninga, C. Sigauke, and T. Ravele, “Comparative Performance of LSTM , ANN , and GAM in Predicting Precipitation and Temperature Anomalies Under Accelerated Warming : Evidence from Thohoyandou , South Africa (1990–2025),” 2026.

[46] G. Ayzel and M. Heistermann, “Brief communication : Training of AI-based nowcasting models for rainfall early warning should take into account user requirements,” pp. 41–47, 2025.

[47] F. A. F. Sofi’ie and A. Qoiriah, “Analisis Perbandingan Framework Front-End Javascript React dan Vue Pada Pengembangan Website Analisis Kebutuhan Pembuatan Sistem Pengumpulan Data Analisa Data,” vol. 05, pp. 157–164, 2023.

[48] J. Chen, “Application Technology of Atmospheric Dispersion Models Based on FastAPI + Vue,” vol. 6, no. 11, pp. 120–126, 2023, doi: 10.25236/AJETS.2023.061118.

## Ringkasan Konversi

- Jumlah entri: **48**.
- Urutan, penomoran, penulis, tahun, judul, DOI/URL, dan detail bibliografis dipertahankan sesuai sumber.
- Line-wrap di dalam entri digabungkan.
- Penanda halaman PDF (`70`, `71`, `72`, `73`, `74`) dan karakter form-feed tidak dimasukkan karena merupakan artefak pemisah halaman, bukan bagian daftar pustaka.

## Bagian Ambigu atau Tidak Lengkap pada Sumber

Berikut bagian yang tampak ambigu atau metadata-nya tidak lengkap pada hasil ekstraksi sumber. Isinya tidak ditebak atau dilengkapi:

- [1] `no. August` tanpa nama jurnal/terbitan yang lebih jelas.
- [2] `vol. XVI` tanpa nama jurnal/terbitan.
- [4] Tidak ada nama jurnal/prosiding atau volume/halaman.
- [5] `no. May 2024` dan tahun `2025` dipertahankan apa adanya.
- [6] `no. February` tanpa nomor edisi numerik.
- [7] `no. September 2022` dan tahun `2023` dipertahankan apa adanya.
- [8] Tidak ada nama jurnal/prosiding atau volume.
- [12] Tidak ada nama jurnal/prosiding atau volume/halaman.
- [13] Tidak ada nama jurnal/prosiding; hanya `vol. 48` dan halaman.
- [14] Tidak ada nama jurnal/prosiding, volume, atau halaman.
- [15] Tidak ada nama jurnal/prosiding atau volume.
- [17] Tidak ada nama jurnal/prosiding.
- [18] Tidak ada nama jurnal/prosiding atau volume/halaman.
- [21] Tidak ada nama jurnal/prosiding.
- [24] Tidak ada nama jurnal/prosiding atau volume.
- [27] `no. NeurIPS` dipertahankan sesuai sumber.
- [28] Tidak ada nama jurnal/prosiding atau detail volume/halaman.
- [29] Tidak ada nama jurnal/prosiding atau halaman.
- [32] Tidak ada nama jurnal/prosiding atau volume/halaman.
- [33] Judul memuat rangkaian `Forecasting Journal of Advances in Modeling Earth Systems` tanpa pemisah yang jelas; dipertahankan apa adanya.
- [34] Tidak ada nama jurnal/prosiding atau volume.
- [36] Tidak ada nama jurnal/prosiding atau volume.
- [37] Tidak ada nama jurnal/prosiding atau volume.
- [38] Tidak ada nama jurnal/prosiding atau volume.
- [39] Hanya tercantum `vol. 256` tanpa nama jurnal/prosiding.
- [41] `no. NeurIPS` dipertahankan sesuai sumber.
- [42] `no. NeurIPS` dipertahankan sesuai sumber.
- [44] Tidak ada nama jurnal/prosiding atau volume.
- [45] Tidak ada nama jurnal/prosiding atau volume/halaman.
- [46] Tidak ada nama jurnal/prosiding atau volume.
- [47] `vol. 05` tanpa nama jurnal yang jelas.

Tidak ada URL selain URL/DOI pada entri [25]; seluruh DOI/URL yang tersedia dipertahankan.
