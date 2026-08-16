# BAB I
# PENDAHULUAN

## 1.1 Latar Belakang

Hipotermia merupakan kondisi darurat ketika suhu inti tubuh turun secara abnormal akibat kehilangan panas yang melebihi kemampuan tubuh untuk memproduksinya. Pada aktivitas pendakian, risiko hipotermia meningkat ketika pendaki terpapar suhu rendah, angin kencang, hujan, pakaian basah, serta kelelahan fisik dalam durasi yang panjang [1], [2]. Menurut Aminullah et al. [2], data BASARNAS periode 2015–2018 menunjukkan bahwa hipotermia merupakan penyebab kecelakaan pendakian yang paling dominan dengan persentase 47%. Sumber yang sama melaporkan tiga pendaki meninggal akibat hipotermia di Gunung Tampomas pada 2018. Studi eksperimental menunjukkan bahwa mempertahankan pakaian basah setelah paparan dingin dapat memperlambat pemulihan suhu kulit dibandingkan dengan mengganti pakaian basah [58]. Fakta tersebut menegaskan pentingnya ketersediaan informasi kondisi cuaca yang cepat dan akurat agar pendaki dapat mengambil tindakan pencegahan sebelum paparan risiko berkembang menjadi kondisi medis yang mengancam jiwa.

Untuk meminimalkan risiko kecelakaan tersebut, diperlukan informasi prakiraan cuaca jangka pendek (nowcasting) yang mampu memberikan deteksi dini sebelum kondisi berbahaya terjadi. Dalam konteks mitigasi keselamatan pendakian, informasi cuaca per jam lebih relevan untuk mendukung keputusan jangka pendek dibandingkan prakiraan harian karena kondisi atmosfer di pegunungan dapat berubah secara dinamis dalam hitungan jam. Informasi mengenai prakiraan probabilistik curah hujan—yaitu peluang atau sebaran kemungkinan curah hujan dalam rentang waktu tertentu—menjadi parameter penting untuk memahami tingkat ketidakpastian cuaca di lapangan. Berbeda dengan prakiraan deterministik yang hanya memberikan nilai tunggal, prakiraan probabilistik menyajikan distribusi kemungkinan kejadian cuaca beserta tingkat keyakinannya. Hal ini memungkinkan pendaki memperoleh gambaran risiko yang lebih realistis, seperti kemungkinan terjadinya hujan lebat mendadak atau peningkatan kecepatan angin yang ekstrem.

Nowcasting cuaca pada rentang waktu sangat pendek (0–6 jam) berperan penting dalam sistem peringatan dini untuk aktivitas luar ruang [3], [4]. Pemanfaatan data radar, model prediksi numerik, dan kecerdasan buatan memungkinkan informasi cuaca diperbarui secara berkala dan cepat guna mendukung keputusan taktis di lapangan [4], [5]. Penerapan metode deep learning dalam nowcasting juga telah terbukti mampu menghasilkan prakiraan curah hujan dan angin dengan resolusi spasial dan temporal yang tinggi [6], [7], [8]. Kendati demikian, efektivitas model ini sangat bergantung pada karakteristik wilayah pengamatan, sehingga evaluasi metodologis yang mendalam pada area dengan kondisi geografis ekstrem sangat diperlukan sebelum model diterapkan secara praktis.

Kawasan Gunung Gede–Pangrango merupakan salah satu destinasi wisata alam dan pendakian dengan intensitas kunjungan yang sangat tinggi, sehingga memiliki risiko keselamatan yang perlu diperhatikan. Berdasarkan kajian daya dukung lingkungan di kawasan Curug Cibeureum [9], curah hujan merupakan salah satu faktor yang perlu dipertimbangkan dalam pengelolaan kawasan wisata. Temuan tersebut menunjukkan bahwa kondisi cuaca dapat berkaitan dengan kapasitas dan keselamatan pengunjung. Oleh karena itu, ketersediaan informasi cuaca per jam di kawasan ini dapat menjadi bahan pertimbangan bagi pihak pengelola dan pendaki dalam menilai kondisi aktivitas di lapangan.

Dinamika hujan di wilayah pegunungan seperti Gunung Gede–Pangrango sangat kompleks karena dipengaruhi oleh interaksi antara topografi, perbedaan elevasi, kelembapan udara, dan arah angin. Mekanisme pengangkatan orografis (*orographic lifting*) memicu kondensasi uap air dan pembentukan awan konvektif secara cepat di lereng atas, sementara siklus harian pemanasan daratan turut menentukan waktu puncak terjadinya hujan [11], [12], [13]. Dinamika lokal ini menciptakan variabilitas spasial yang ekstrem, di mana perbedaan curah hujan yang signifikan dapat terjadi dalam jarak horizontal yang sangat pendek [14], [15]. Ketergantungan spasial dan temporal yang erat antar-elevasi ini membuat prakiraan cuaca per jam di wilayah pegunungan menjadi sangat menantang dan tidak dapat didekati dengan asumsi stasioner.

Model prakiraan cuaca deterministik konvensional dapat mengalami keterbatasan dalam merepresentasikan kejadian ekstrem di pegunungan karena prediksinya cenderung mendekati nilai rata-rata (*smoothing effect*) [16], [17]. Model deterministik merupakan pendekatan prediksi yang menghasilkan satu nilai untuk setiap waktu dan lokasi, tanpa menyertakan rentang ketidakpastian atau peluang kejadian lainnya. Sebaliknya, pendekatan probabilistik menghasilkan beberapa kemungkinan prediksi beserta peluang atau tingkat ketidakpastiannya, sehingga dapat menggambarkan berbagai kondisi cuaca yang mungkin terjadi. Hambatan utama dalam pemodelan cuaca ini berkaitan dengan kemungkinan karakteristik data hujan yang *zero-inflated* dan *heavy-tailed*. Karakteristik *zero-inflated* berarti sebagian besar rekaman data menunjukkan nilai nol (tidak ada hujan), sedangkan karakteristik *heavy-tailed* berarti sebagian kecil kejadian hujan memiliki intensitas yang sangat ekstrem. Karakteristik tersebut perlu dikonfirmasi melalui analisis statistik pada data penelitian. Model regresi deterministik yang dioptimalkan dengan fungsi loss rata-rata akan cenderung memprediksi hujan ringan saat terjadi hujan lebat, dan sebaliknya, memprediksi ada hujan ringan saat kondisi sebenarnya kering. Akibatnya, representasi kejadian ekstrem yang sangat penting untuk mitigasi keselamatan menjadi terabaikan [16], [17].

Untuk mengatasi keterbatasan tersebut, sejumlah penelitian mengembangkan pendekatan **probabilistik generatif**, termasuk *Retrieval-Augmented Diffusion Model*, serta **pemodelan spasio-temporal** melalui *Spatio-Temporal Graph Neural Network*. Namun, pada penelitian yang ditinjau, kedua pendekatan tersebut masih banyak diterapkan secara terpisah. Beberapa penelitian hanya berfokus pada model generatif untuk ketidakpastian tanpa mempertimbangkan informasi topografi [6], [7], sedangkan sebagian lainnya menggunakan pemodelan spasio-temporal untuk representasi spasial namun menghasilkan keluaran deterministik tunggal [10], [18], [20], [21]. Berdasarkan penelitian yang ditinjau, masih diperlukan kajian yang mengintegrasikan model generatif probabilistik dengan representasi spasial graf untuk menangani karakteristik data hujan pegunungan yang zero-inflated dan heavy-tailed.

Penelitian ini merespons kebutuhan tersebut dengan mengembangkan **Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network**. Dalam model ini, **Retrieval-Augmented Diffusion Model** bertindak sebagai model generatif utama yang memodelkan distribusi probabilistik cuaca melalui proses *diffusion*, sehingga mampu menghasilkan beberapa kemungkinan skenario cuaca. Sementara itu, **Spatio-Temporal Graph Neural Network** digunakan sebagai komponen pengondisi (*conditioning*) yang memodelkan lima titik lokasi pengamatan sebagai graf untuk menangkap ketergantungan spasial dan evolusi temporal kondisi cuaca di wilayah pegunungan. Kombinasi kedua metode ini dirancang untuk menghasilkan ensemble prakiraan probabilistik yang realistis dan sensitif terhadap nilai ekstrem.

Fokus penelitian ini dibatasi pada evaluasi metodologis model dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif satu jam ke depan di kawasan Gunung Gede–Pangrango dengan menggunakan data ERA5. Dataset ERA5 merupakan data reanalisis global dari *European Centre for Medium-Range Weather Forecasts* (ECMWF) yang menggabungkan hasil model numerik atmosfer dengan berbagai pengamatan melalui proses asimilasi data. Data ini disajikan pada grid dengan resolusi horizontal sekitar 25 kilometer. Oleh karena itu, nilai ERA5 merupakan estimasi kondisi atmosfer pada grid tersebut dan tidak secara langsung merepresentasikan kondisi cuaca mikro pada titik ketinggian tertentu di puncak gunung [57]. Dalam penelitian ini, ERA5 digunakan untuk menguji kinerja metodologis model pada skala grid yang tersedia, bukan untuk mengklaim representasi kondisi mikrocuaca secara presisi. Atas dasar tersebut, penelitian ini berorientasi pada mitigasi risiko dengan menganalisis hasil prediksi serta kemampuan model dalam mendeteksi kejadian cuaca ekstrem [23]. Selain itu, hasil prediksi dari model ini dirancang untuk diintegrasikan ke dalam visualisasi berbasis web.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, penelitian ini merumuskan permasalahan sebagai berikut:

1. Bagaimana kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5?
2. Bagaimana kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dibandingkan dengan model deterministik dalam memprediksi kondisi cuaca dan kejadian ekstrem?
3. Seberapa baik Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kejadian cuaca ekstrem, khususnya hujan dengan intensitas tinggi?
4. Bagaimana hasil prediksi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dapat ditampilkan melalui visualisasi berbasis web untuk menyajikan informasi cuaca pendukung bagi aktivitas pendakian?

## 1.3 Tujuan Penelitian

Tujuan umum penelitian ini adalah mengevaluasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network untuk nowcasting kondisi cuaca satu jam ke depan di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.

Tujuan khusus penelitian ini adalah:

1. Mengevaluasi kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.
2. Membandingkan kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dan model deterministik dalam memprediksi kondisi cuaca dan kejadian ekstrem.
3. Mengevaluasi kemampuan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi kejadian cuaca ekstrem, khususnya hujan dengan intensitas tinggi.
4. Mengembangkan visualisasi berbasis web untuk menampilkan hasil prediksi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network sebagai informasi pendukung pengambilan keputusan dalam aktivitas pendakian.

## 1.4 Manfaat Penelitian

Penelitian ini diharapkan dapat memberikan kontribusi dalam pengembangan metode *nowcasting* cuaca serta penerapannya dalam mendukung mitigasi risiko aktivitas pendakian di wilayah pegunungan. Manfaat yang diharapkan dari penelitian ini adalah sebagai berikut:

1. Memberikan kontribusi dalam pengembangan dan evaluasi model *nowcasting* probabilistik berbasis *Retrieval-Augmented Diffusion Model* dan *Spatio-Temporal Graph Neural Network* untuk memodelkan dinamika curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan.
2. Memberikan pemahaman ilmiah mengenai efektivitas penggabungan pencarian kondisi cuaca historis yang serupa pada *Retrieval-Augmented Diffusion Model* dan representasi graf spasio-temporal pada *Spatio-Temporal Graph Neural Network* dalam menangkap ketidakpastian serta hubungan spasial-temporal cuaca.
3. Menyajikan analisis empiris mengenai kemampuan model *Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network* dalam merepresentasikan ketidakpastian curah hujan yang sering kali bernilai nol (*zero-inflated*) dan memiliki nilai ekstrem (*heavy-tailed*), termasuk kepekaan prediksi terhadap kejadian hujan pada berbagai ambang intensitas.
4. Menyajikan analisis terkait perbandingan antara akurasi prediksi rata-rata dan kemampuan model *Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network* dalam mendeteksi kejadian ekstrem sebagai dasar dalam pengambilan keputusan berbasis risiko pada aktivitas pendakian di wilayah pegunungan.
5. Menghasilkan prediksi probabilistik dari model *Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network* yang dapat digunakan sebagai dasar pengembangan sistem visualisasi berbasis web untuk penyampaian informasi cuaca jangka pendek.

## 1.5 Batasan Masalah

Untuk menjaga fokus penelitian dan memastikan ketercapaian tujuan dalam ruang lingkup skripsi, penelitian ini dibatasi oleh beberapa ketentuan sebagai berikut:

1. Penelitian difokuskan pada kawasan Gunung Gede–Pangrango yang direpresentasikan oleh lima titik lokasi.
2. Penelitian menggunakan data *reanalysis* ERA5 melalui *Open-Meteo API* dengan menggunakan data masukan (*input*) enam jam terakhir untuk memprediksi kondisi cuaca satu jam ke depan.
3. Target prediksi dibatasi pada curah hujan, kecepatan angin, dan kelembapan relatif.
4. Penelitian mengevaluasi model *nowcasting* probabilistik berbasis *Retrieval-Augmented Diffusion Model* yang terintegrasi dengan representasi graf dari *Spatio-Temporal Graph Neural Network*.
5. Hasil prediksi tidak merepresentasikan kondisi cuaca mikro secara presisi karena menggunakan data berbasis grid dari *reanalysis* ERA5.
6. Penelitian difokuskan pada pengembangan dan evaluasi metodologi *nowcasting* probabilistik, bukan pada implementasi sistem operasional secara langsung.

---

# BAB II — TINJAUAN PUSTAKA

## 2.1 Penelitian Terdahulu

Penelitian-penelitian yang telah dilakukan dan relevan dengan penelitian ini mencakup model generatif probabilistik, model graf spasio-temporal, mekanisme retrieval pada diffusion model, model recurrent berbasis attention, serta pendekatan ensemble untuk prakiraan cuaca. Sepuluh penelitian berikut digunakan sebagai landasan perbandingan konseptual. Tiga penelitian yang paling dekat dengan fokus penelitian dirangkum dalam Tabel 2.1, sedangkan penelitian yang diusulkan ditampilkan sebagai baris pembanding keempat. Penelitian yang diusulkan tidak dihitung sebagai penelitian terdahulu.

1. Penelitian “Precipitation Nowcasting with Generative Diffusion Models”

oleh Asperti et al. (2024) [25] Penelitian ini mengembangkan Generative Ensemble Diffusion (GED) berbasis DDIM dan denoiser U-Net untuk menghasilkan 15 sampel prediksi hujan berbasis ERA5. Ensemble dibentuk melalui proses sampling berulang dan dapat diproses menggunakan rata-rata atau post-processing U-Net. Penelitian tersebut relevan karena menunjukkan bahwa diffusion ensemble dapat merepresentasikan beberapa kemungkinan evolusi hujan. Perbedaannya terletak pada penggunaan grid Eropa, bukan lima node ERA5 dengan target `MAIN` di Gunung Gede–Pangrango.

2. Penelitian   “Spatio-temporal      graph    neural    networks     to   improve

precipitation forecasts from numerical models” oleh Yousaf et al. (2025) [26] Penelitian ini mengembangkan WRF-GNN untuk memperbaiki keluaran prakiraan WRF menggunakan informasi 22 rain gauge di Calabria, Italia. Relevansinya terletak pada penggunaan representasi graf untuk memodelkan ketergantungan spasio-temporal. Namun, penelitian ini memakai keluaran WRF, observasi rain gauge, resolusi 2 km, dan horizon satu hari sehingga tidak merupakan reproduksi model pada penelitian ini.

3. Penelitian “Retrieval-Augmented Diffusion Models for Time Series

Forecasting” oleh Liu et al. (2024) [27] Penelitian ini mengusulkan Retrieval-Augmented Time series Diffusion (RATD), yang mengambil urutan historis serupa melalui embedding retrieval dan memasukkannya ke proses denoising melalui Reference-Modulated Attention. Relevansinya adalah prinsip integrasi retrieval dan diffusion pada data deret waktu. RATD tidak menggunakan lima node, ERA5, target `MAIN`, atau Spatio-Temporal Graph Neural Network, sehingga hasilnya tidak dapat dianggap sebagai bukti performa pada hujan lokal.

4. Penelitian “Skilful precipitation nowcasting using deep generative models

of radar” oleh Ravuri et al. (2021) [6] Penelitian ini mengembangkan DGMR berbasis conditional GAN untuk menghasilkan prakiraan hujan probabilistik dari empat frame radar dan memprediksi hingga 90 menit. Model menggunakan spatial discriminator, temporal discriminator, dan regularisasi grid-cell. Penelitian ini relevan sebagai rujukan model generatif probabilistik untuk nowcasting, tetapi data radar dan resolusi spasialnya berbeda dari data ERA5 titik-lokasi pada penelitian ini.

5. Penelitian “Skilful nowcasting of extreme precipitation with NowcastNet”

oleh Zhang et al. (2023) [7] NowcastNet menggabungkan evolution network berbasis adveksi dan persamaan kontinuitas dengan stochastic generative network untuk mempertahankan struktur hujan ekstrem. Penelitian ini relevan karena memadukan kendala evolusi dan pembangkitan stokastik. Ketergantungannya pada data radar resolusi tinggi dan evaluasi hingga tiga jam membatasi penerapan langsung pada lima node ERA5.

6. Penelitian “Exploring Geometric Deep Learning for Precipitation

Nowcasting” oleh Zhao et al. (2023) [28] Penelitian ini memandang grid radar sebagai graf dan menggunakan temporal Graph Convolutional Network untuk memodelkan hubungan antarlokasi. Relevansinya adalah dasar konseptual adaptasi representasi graf pada data hujan. Perbedaan unit node, sumber data radar, dan horizon prediksi menyebabkan hasilnya tidak dapat dipindahkan langsung ke penelitian ini.

7. Penelitian   “RSDF-AM-LSTM:          Regional    Scale    Division    Rainfall

Forecasting Using Attention and LSTM” oleh Li et al. (2022) [29] Penelitian ini menggabungkan beberapa LSTM paralel dengan mekanisme attention untuk menangkap dependensi temporal-spasial pada ribuan stasiun meteorologi. Relevansinya terletak pada pemanfaatan attention dan LSTM untuk data multi-lokasi. Baseline Multi-node LSTM + Attention pada penelitian ini hanya merupakan adaptasi gagasan tersebut ke lima node ERA5 dan target `MAIN`, bukan reproduksi penuh RSDF-AM-LSTM.

8. Penelitian “A Hybrid Approach to Physical and Deep Learning Models for

Radar-Based Precipitation Nowcasting” oleh Kim et al. (2025) [20] Penelitian ini memadukan PySTEPS, RainNet, dan LightGBM untuk menggabungkan keunggulan model adveksi dan deep learning. Relevansinya terletak pada strategi penggabungan beberapa sumber representasi untuk meningkatkan prediksi. Pipeline radar dan model fisik pada penelitian tersebut tidak direproduksi karena penelitian ini menggunakan ERA5 pada lima node.

9. Penelitian “FuXi-ENS: A machine learning model for efficient and accurate

ensemble weather prediction” oleh Zhong et al. (2025) [17] FuXi-ENS menggunakan variational autoencoder dan loss CRPS untuk menghasilkan prakiraan ensemble global dengan perturbasi yang bergantung pada kondisi atmosfer. Relevansinya adalah representasi ketidakpastian dan evaluasi probabilistik. Perbedaan resolusi, wilayah, interval enam jam, dan horizon hingga 15 hari membatasi perbandingan langsung dengan nowcasting satu jam pada penelitian ini.

10. Penelitian “Beyond the horizon: A comprehensive analysis of artificial

intelligence-based weather forecasting models” oleh Haji-Aghajany et al. (2025) [30] Penelitian ini merupakan tinjauan komprehensif terhadap model prakiraan cuaca berbasis AI, termasuk isu ketidakpastian, generalisasi, interpretabilitas, dan kendala fisik. Relevansinya adalah pemetaan konseptual posisi diffusion model, retrieval, graf, dan attention dalam perkembangan prakiraan cuaca berbasis AI. Artikel tinjauan ini bukan baseline dan tidak menyediakan eksperimen langsung pada lima node ERA5 atau Gunung Gede–Pangrango. Kesepuluh penelitian tersebut menunjukkan perkembangan pada diffusion ensemble, graf spasio-temporal, retrieval-augmented forecasting, attention-LSTM, dan ensemble weather prediction. Berdasarkan penelitian yang ditinjau dalam naskah ini, belum ditemukan penelitian yang menguji integrasi Retrieval-Augmented Diffusion Model dan Spatio-Temporal Graph Neural Network secara simultan pada lima node ERA5 dengan target `MAIN` dan horizon satu jam di kawasan Gunung Gede–Pangrango. Kebaruan penelitian ini dibatasi pada kombinasi metode, konfigurasi spasial, sumber data, horizon, dan wilayah studi; penelitian ini tidak mengklaim sebagai penelitian pertama di dunia. **Tabel 2.1 Penelitian Terdahulu**

| No. | Judul dan Peneliti | Metode | Temuan Utama | Kedudukan terhadap Penelitian Ini |
|---:|---|---|---|---|
| 1 | Precipitation Nowcasting with Generative Diffusion Models — Asperti et al. (2024) [25] | Generative Ensemble Diffusion berbasis DDIM dan U-Net | Ensemble diffusion menghasilkan beberapa kemungkinan prediksi presipitasi berbasis ERA5. | Rujukan utama diffusion ensemble; berbeda pada grid, wilayah, dan konfigurasi spasial. |
| 2 | Spatio-temporal graph neural networks to improve precipitation forecasts from numerical models — Yousaf et al. (2025) [26] | WRF-GNN dengan keluaran WRF dan rain gauge | Graf spasio-temporal digunakan untuk memperbaiki prakiraan presipitasi numerik. | Rujukan utama representasi graf; penelitian ini tidak menggunakan WRF atau 22 rain gauge. |
| 3 | Retrieval-Augmented Diffusion Models for Time Series Forecasting — Liu et al. (2024) [27] | RATD dengan embedding retrieval dan Reference-Modulated Attention | Retrieval historis membantu diffusion model pada forecasting deret waktu. | Rujukan integrasi retrieval-diffusion; bukan penelitian cuaca lokal dan tidak memakai Spatio-Temporal Graph Neural Network. |
| 4 | Penelitian yang diusulkan | Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network; ERA5/Open-Meteo; lima node; target MAIN | Hasil penelitian belum tersedia. | Model utama penelitian ini. |

## 2.2 Landasan Teori

Landasan teori dalam penelitian ini disusun untuk memberikan dasar ilmiah bagi pengembangan model *nowcasting* probabilistik kondisi cuaca menggunakan *Retrieval-Augmented Diffusion Model* dengan *Spatio-Temporal Graph Neural Network*. Bab ini membahas konsep-konsep utama yang menjadi dasar penelitian, mulai dari prinsip *nowcasting* pada skala waktu per jam, dinamika hujan orografis di pegunungan tropis, hingga cara kerja *Retrieval-Augmented Diffusion Model* dalam menghasilkan beberapa kemungkinan prediksi cuaca. Selanjutnya, dibahas pula pencarian kondisi cuaca historis yang serupa serta penggunaan representasi graf spasio-temporal melalui lima node, yaitu `MAIN`, `UP`, `DOWN`, `LEFT`, dan `RIGHT`. Representasi tersebut digunakan untuk menangkap hubungan kondisi cuaca antar lokasi dan perubahan kondisi atmosfer dari waktu ke waktu, dengan node `MAIN` sebagai titik target prediksi. Pembahasan kemudian dilanjutkan dengan risiko hipotermia pada aktivitas pendakian di Gunung Gede–Pangrango serta relevansinya terhadap penyampaian informasi cuaca jangka pendek. Dengan landasan teori tersebut, penelitian ini mengevaluasi kemampuan model dalam menghasilkan prediksi cuaca yang mempertimbangkan kemungkinan ketidakpastian, hubungan antar lokasi, dan perubahan kondisi dari waktu ke waktu di wilayah pegunungan tropis.

### 2.2.1 Konsep Nowcasting dan Skala Waktu Prediksi Atmosfer

*Nowcasting* merupakan prakiraan cuaca jangka sangat pendek yang menggunakan kondisi atmosfer terkini untuk memprediksi perubahan cuaca hingga sekitar enam jam ke depan [6]. Berbeda dengan prakiraan cuaca harian atau mingguan, *nowcasting* berfokus pada perubahan cuaca lokal yang berlangsung cepat. Dalam penelitian ini, *nowcasting* digunakan untuk memprediksi kondisi cuaca satu jam ke depan pada satu titik pengamatan utama yang disebut node `MAIN` di kawasan Gunung Gede–Pangrango.

Target prediksi meliputi curah hujan, kecepatan angin, dan kelembapan relatif. Ketiga variabel tersebut digunakan untuk menggambarkan kondisi cuaca yang dapat memengaruhi paparan pendaki. Tabel 2.2 membandingkan *nowcasting* dengan prakiraan cuaca pada rentang waktu yang lebih panjang. Contoh keluaran pada tabel menggunakan curah hujan karena hujan merupakan salah satu fenomena cuaca yang dapat berubah dengan cepat. Keluaran model penelitian ini tetap mencakup tiga target, yaitu curah hujan, kecepatan angin, dan kelembapan relatif.

Konsep *nowcasting* ini menjadi dasar untuk membahas dinamika cuaca per jam, fitur temporal, keterbatasan pendekatan deterministik, dan pendekatan probabilistik pada subbab berikutnya.
**Tabel 2.2 Perbandingan Skala Prakiraan Atmosfer [7] [16]**

| Skala Prakiraan | Horizon | Karakteristik Utama | Contoh Keluaran |
|---|---|---|---|
| Nowcasting | 0–6 jam | Bergantung kuat pada kondisi awal dan observasi terkini; menargetkan fenomena lokal yang berubah cepat. | Prediksi curah hujan satu jam ke depan. |
| Short-range forecasting | 6–72 jam | Memadukan observasi dan prediksi numerik untuk evolusi cuaca jangka pendek. | Prakiraan hujan harian dan peringatan cuaca. |
| Medium-range forecasting | Lebih dari 72 jam hingga sekitar 15 hari | Menekankan dinamika atmosfer skala besar dan prediksi ensemble. | Prakiraan probabilistik regional atau global. |

#### 2.2.1.1 Definisi dan Ruang Lingkup Nowcasting

Dalam meteorologi operasional, *nowcasting* merupakan prakiraan cuaca jangka sangat pendek yang memberikan informasi mengenai kondisi saat ini hingga sekitar enam jam ke depan. Prakiraan ini berfokus pada kondisi lokal yang dapat berubah dengan cepat dan memanfaatkan informasi pengamatan terkini [6].

Dalam penelitian ini, *nowcasting* dibatasi pada prediksi kondisi cuaca satu jam ke depan berdasarkan data enam jam sebelumnya. Data tersebut digunakan untuk mengenali perubahan kondisi atmosfer terbaru sebelum model menghasilkan prediksi pada satu titik pengamatan utama, yaitu node `MAIN` [7]. Target prediksi meliputi curah hujan, kecepatan angin, dan kelembapan relatif.

*Nowcasting* berbeda dari prakiraan cuaca jangka pendek yang umumnya mencakup rentang waktu enam hingga 72 jam. Prakiraan jangka pendek dapat menggunakan model numerik dan informasi atmosfer berskala lebih luas, sedangkan *nowcasting* lebih menekankan kondisi terkini dan perubahan cuaca lokal. Oleh karena itu, pendekatan *nowcasting* sesuai digunakan untuk memantau perubahan cuaca per jam di kawasan pegunungan yang memiliki kondisi atmosfer dinamis [6], [7].

Pemahaman mengenai ruang lingkup *nowcasting* menjadi dasar untuk membahas karakteristik perubahan cuaca per jam di wilayah pegunungan pada subbab berikutnya.

#### 2.2.1.2 Karakteristik Dinamika pada Skala Waktu Per Jam di Wilayah Pegunungan

Rentang prediksi 0–6 jam pada *nowcasting* berkaitan erat dengan perubahan cuaca lokal dan pembentukan awan atau hujan yang dapat berlangsung cepat [7]. Dalam meteorologi, fenomena tersebut umumnya dibahas pada skala menengah (*mesoscale*) dan skala pembentukan awan atau hujan akibat naiknya udara lembap. Pada skala ini, proses awal pembentukan awan dan hujan di wilayah pegunungan, yang dalam meteorologi disebut **inisiasi pembentukan awan dan hujan (*convective initiation*)**, sangat dipengaruhi oleh naiknya udara lembap serta perubahan kecil pada kelembapan, suhu, dan kecepatan angin lokal [13].

Di wilayah pegunungan tropis seperti Gunung Gede–Pangrango, dinamika tersebut menjadi lebih kompleks karena dipengaruhi oleh pengangkatan udara akibat topografi (*orographic lifting*), siklus harian pembentukan awan, dan interaksi angin dengan lereng. Faktor-faktor tersebut menyebabkan kondisi cuaca berbeda antarlokasi dan berubah dari waktu ke waktu [11], [14].

Awan dan hujan yang terbentuk melalui proses tersebut dapat muncul dan berubah dalam waktu yang relatif singkat [11], [20]. Oleh karena itu, prediksi cuaca satu jam ke depan perlu mempertimbangkan kemungkinan terbentuknya awan baru, pergerakan hujan, serta perubahan intensitas curah hujan [4], [20].

Perubahan kecil pada kondisi awal atmosfer, seperti kelembapan, suhu, dan kecepatan angin, dapat menghasilkan perubahan cuaca yang berbeda dalam waktu singkat. Akibatnya, kesalahan prakiraan dapat membesar seiring bertambahnya waktu prediksi (*rapid error growth*) [32]. Di kawasan Gunung Gede–Pangrango, perbedaan elevasi yang cukup besar dapat menyebabkan kondisi meteorologis yang berbeda dalam jarak horizontal yang relatif pendek [11], [14]. Kondisi ini membuat prediksi per jam penting untuk menggambarkan perubahan curah hujan, kecepatan angin, dan kelembapan relatif di sepanjang wilayah pendakian. Oleh karena itu, model *nowcasting* perlu mempertimbangkan perubahan kondisi cuaca yang berlangsung cepat, baik menurut waktu maupun lokasi [1].

#### 2.2.1.3 Keterkaitan Waktu dalam Prediksi Curah Hujan

Curah hujan dapat berubah dalam waktu yang relatif singkat [11], [20]. Kondisi tersebut menunjukkan bahwa keadaan hujan pada waktu sebelumnya dapat memberikan informasi mengenai kemungkinan kondisi hujan pada waktu berikutnya [4], [20].

Dalam penelitian ini, keterkaitan waktu tersebut direpresentasikan melalui fitur curah hujan satu jam sebelumnya atau *lag-1*. Fitur ini digunakan sebagai salah satu fitur masukan pada setiap waktu pengamatan dan dirumuskan sebagai berikut:

$$
\operatorname{PrecipitationLag1}_t = \operatorname{Precipitation}_{t-1} \tag{2.1}
$$

dengan:

- `PrecipitationLag1_t` = nilai curah hujan satu jam sebelum waktu prediksi `t`;

- `Precipitation_{t-1}` = nilai curah hujan pada waktu `t-1`.

Formula 2.1 hanya menunjukkan penggunaan curah hujan satu jam sebelumnya sebagai salah satu fitur temporal. Sementara itu, jendela pengamatan enam jam mencakup rangkaian kondisi cuaca dari waktu `t-6` hingga `t-1` untuk memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada waktu `t`. Jendela tersebut diproses sebagai rangkaian snapshot graf, sedangkan perubahan kondisi antarwaktu dipelajari melalui mekanisme *temporal attention* pada *Spatio-Temporal Graph Neural Network*. Mekanisme tersebut dibahas lebih lanjut pada Subbab 2.2.6. (noted [pertanyaan ke dosen nantinya])

#### 2.2.1.4 Transformasi dan Standardisasi Data Curah Hujan

Data curah hujan memiliki karakteristik *zero-inflated*, yaitu sebagian besar nilainya berada pada angka nol karena tidak terjadi hujan, serta *heavy-tailed*, yaitu sebagian kecil datanya memiliki nilai curah hujan yang sangat tinggi. Karakteristik tersebut menyebabkan rentang nilai curah hujan menjadi tidak seimbang, sehingga perlu dilakukan transformasi agar pola data lebih mudah dipelajari oleh model. Oleh karena itu, digunakan transformasi logaritmik `log1p`, yaitu transformasi yang tetap dapat diterapkan pada nilai nol:

$$  
y' = \log(1+y) \tag{2.2}
$$

dengan:

- `y` = nilai curah hujan asli;

- `y'` = nilai curah hujan setelah transformasi.

Setelah transformasi, data diseragamkan menggunakan standardisasi Z-score agar variabel dengan rentang nilai berbeda dapat diproses pada skala yang sebanding:

$$
z = \frac{y' - \mu}{\sigma + \varepsilon} \tag{2.3}
$$

dengan:

- `z` = nilai setelah standardisasi;

- `y'` = nilai curah hujan setelah transformasi;

- `μ` = rata-rata data pelatihan;

- `σ` = simpangan baku data pelatihan;

- `ε` = konstanta kecil untuk mencegah pembagian dengan nol.

Rata-rata dan simpangan baku dihitung hanya berdasarkan data pelatihan untuk mencegah informasi dari data validasi dan data pengujian masuk ke dalam proses pembelajaran model. Data yang telah ditransformasi dan distandardisasi kemudian digunakan sebagai bagian dari masukan model.

### 2.2.2 Dinamika Hujan Orografis di Pegunungan Tropis

Hujan orografis merupakan hujan yang terbentuk ketika udara lembap bergerak menuju pegunungan dan terdorong naik oleh permukaan lereng. Udara yang naik mengalami penurunan suhu sehingga uap air mengembun dan membentuk awan serta hujan [11], [35]. Di wilayah tropis, proses ini dipengaruhi oleh kelembapan udara yang tinggi dan kondisi atmosfer yang tidak stabil. Akibatnya, curah hujan dapat berbeda antara satu lokasi dan lokasi lainnya dalam jarak yang relatif dekat [11], [14], [35].

Di kawasan Gunung Gede–Pangrango, perbedaan elevasi, bentuk lereng, dan arah angin menyebabkan kondisi cuaca berubah menurut lokasi. Lereng yang berhadapan dengan arah datangnya angin (*windward slope*) cenderung menerima lebih banyak udara lembap, sedangkan lereng yang terlindung dari arah angin (*leeward slope*) dapat mengalami kondisi yang lebih kering atau bayangan hujan (*rain shadow*) [11], [36]. Selain itu, pemanasan permukaan pada siang hari dan perubahan angin dapat memengaruhi waktu serta intensitas terjadinya hujan [37].

Dinamika tersebut menyebabkan hujan di wilayah pegunungan dapat berubah dalam waktu singkat dan memiliki perbedaan intensitas yang besar. Karakteristik ini membuat prediksi cuaca per jam menjadi penting, terutama untuk memprediksi curah hujan, kecepatan angin, dan kelembapan relatif. Oleh karena itu, pemodelan cuaca di wilayah Gunung Gede–Pangrango perlu mempertimbangkan perubahan kondisi atmosfer menurut lokasi dan waktu. Penjelasan mengenai mekanisme pembentukan hujan serta variasi hujan menurut lokasi dan waktu dibahas pada subbab berikutnya.

#### 2.2.2.1 Mekanisme Orographic Lifting dan Convective Initiation

Mekanisme utama hujan orografis terjadi ketika udara lembap terdorong naik oleh permukaan lereng pegunungan. Ketika udara tersebut naik, suhunya menurun sehingga uap air dapat mengembun dan membentuk awan [36]. Di wilayah tropis, proses awal pembentukan awan dan hujan ini disebut inisiasi konveksi (*convective initiation*). Proses tersebut dipengaruhi oleh kelembapan udara, suhu, kestabilan atmosfer, serta kecepatan dan arah angin [11].

Angin yang bergerak melintasi lereng (*cross-slope wind*) dapat memperkuat pengangkatan udara dan membawa uap air menuju lereng pegunungan. Namun, pengaruh angin terhadap pembentukan hujan tidak berdiri sendiri karena juga bergantung pada topografi, kelembapan, orientasi lereng, dan kondisi atmosfer [36]. Dengan demikian, peningkatan kecepatan angin dapat meningkatkan potensi pembentukan hujan pada kondisi tertentu, tetapi besarnya pengaruh tersebut dapat berbeda menurut wilayah dan keadaan atmosfer.

Hubungan konseptual antara intensitas hujan orografis dan faktor atmosfer serta topografi dapat dinyatakan sebagai berikut:

$$
P_{\mathrm{orografis}} = f(U_{\mathrm{cross}}, q, H, S, C) \tag{2.4}
$$

dengan:

- `P_orografis` = intensitas hujan orografis;

- `U_cross` = komponen kecepatan angin yang bergerak melintasi lereng;

- `q` = kelembapan udara;

- `H` = karakteristik elevasi atau topografi;

- `S` = orientasi dan kemiringan lereng;

- `C` = kondisi atmosfer yang mendukung pembentukan awan dan hujan.

Rumus tersebut merupakan representasi konseptual mengenai faktor-faktor yang berkaitan dengan pembentukan hujan orografis. Rumus ini bukan persamaan empiris untuk menghitung curah hujan di Gunung Gede–Pangrango dan tidak digunakan secara langsung dalam proses prediksi model. Hubungan antara angin, kelembapan, topografi, dan pembentukan hujan menjadi dasar teoritis untuk mempertimbangkan informasi dari beberapa titik pengamatan dalam penelitian ini [11], [12], [36].

Di kawasan Gunung Gede–Pangrango, interaksi antara faktor mekanis, seperti pengangkatan udara oleh lereng, dan faktor termal, seperti pemanasan permukaan, dapat menyebabkan hujan terbentuk secara tidak merata. Kondisi tersebut mendukung penggunaan representasi spasio-temporal untuk mempelajari hubungan kondisi cuaca antartitik pengamatan. Pembahasan mengenai variasi hujan menurut lokasi dan waktu dilanjutkan pada Subbab 2.2.2.2.

#### 2.2.2.2 Variabilitas Spasial dan Temporal Hujan Orografis

Hujan orografis di wilayah pegunungan memiliki variasi spasial karena dipengaruhi oleh elevasi, bentuk dan orientasi lereng, arah angin, serta kelembapan udara [14], [35]. Hubungan antara curah hujan dan elevasi tidak selalu seragam karena bergantung pada kondisi atmosfer dan karakteristik topografi setempat [11], [36]. Oleh karena itu, perbedaan curah hujan antarlokasi di kawasan Gunung Gede–Pangrango perlu dianalisis berdasarkan data penelitian dan tidak diasumsikan mengikuti satu pola tertentu.

Perbedaan kondisi cuaca juga dapat terjadi antara sisi lereng yang berhadapan dengan arah datangnya angin dan sisi lereng yang terlindung. Lereng yang berhadapan dengan angin dapat menerima lebih banyak udara lembap, sedangkan sisi yang terlindung dapat mengalami kondisi yang berbeda. Perbedaan tersebut berpotensi menghasilkan curah hujan, kecepatan angin, dan kelembapan relatif yang tidak sama pada setiap titik pengamatan [11], [36].

Dari sisi waktu atau secara temporal, curah hujan dapat menunjukkan pola harian. Namun, waktu puncaknya dapat berbeda menurut lokasi, musim, arah angin, dan kondisi atmosfer [37]. Pada kondisi tertentu, pengaruh topografi dan angin dapat mengubah pola harian sehingga waktu terjadinya hujan menjadi lebih sulit diprediksi [36]. Perubahan tersebut menjadi alasan pentingnya penggunaan data beberapa jam sebelumnya untuk memprediksi kondisi cuaca satu jam ke depan.

Selain berbeda menurut waktu dan lokasi, intensitas hujan juga tidak tersebar secara merata. Sebagian besar rekaman dapat menunjukkan curah hujan rendah atau tidak terjadi hujan, sedangkan sebagian kecil kejadian dapat memiliki intensitas yang sangat tinggi. Karakteristik ini disebut distribusi berekor berat (*heavy-tailed*), yaitu kondisi ketika terdapat sebagian kecil nilai ekstrem yang jauh lebih besar daripada nilai umumnya [6], [7]. Pada kondisi tertentu, hujan lebat dapat bertahan lebih lama di sekitar lereng apabila pergerakan sistem hujan terhambat oleh topografi atau terjadi pengangkatan udara secara berulang [34], [35]. Namun, pola tersebut bergantung pada kondisi atmosfer dan perlu dibuktikan melalui data penelitian.

Perbedaan curah hujan antarlokasi dan antarwaktu tersebut menjadi dasar penggunaan representasi spasio-temporal dalam penelitian ini. Informasi dari beberapa titik pengamatan digunakan untuk menggambarkan hubungan kondisi cuaca di sekitar titik utama. Dalam model yang dikembangkan, hubungan tersebut dipelajari menggunakan Spatio-Temporal Graph Neural Network, sedangkan pendekatan diffusion digunakan untuk menghasilkan beberapa kemungkinan prediksi. Detail mengenai peran kedua pendekatan tersebut dijelaskan pada subbab berikutnya.

#### 2.2.2.3 Relevansi dengan Nowcasting Probabilistik dan Mitigasi Risiko

Variasi hujan orografis yang kompleks dan cepat berubah menjadi tantangan bagi model deterministik dalam memprediksi kejadian ekstrem di wilayah pegunungan tropis [7], [32]. Model regresi deterministik cenderung menghasilkan prediksi yang mendekati nilai rata-rata. Akibatnya, model dapat memprediksi hujan berintensitas tinggi lebih rendah daripada kondisi sebenarnya karena mengalami efek perataan (*smoothing*). Pendekatan probabilistik digunakan untuk menghasilkan beberapa kemungkinan kondisi cuaca sehingga ketidakpastian prediksi dapat direpresentasikan [25].

Hal tersebut penting dalam nowcasting di Gunung Gede–Pangrango karena hujan orografis dapat mempercepat kehilangan panas tubuh pendaki. Variasi kondisi cuaca yang tinggi antarlokasi dan antarketinggian dapat direpresentasikan menggunakan graf untuk menangkap ketergantungan antar-*node* [7].

Spatio-Temporal Graph Neural Network digunakan untuk mempelajari hubungan kondisi cuaca antarlokasi melalui mekanisme *message passing*. Mekanisme ini menggabungkan informasi dari node yang saling terhubung. Dalam penelitian ini, informasi kondisi cuaca dari beberapa titik dapat digunakan secara bersama untuk membantu merepresentasikan kondisi di sekitar titik prediksi utama, termasuk perubahan yang berkaitan dengan kejadian hujan ekstrem [6], [7].

Informasi dari Spatio-Temporal Graph Neural Network kemudian digunakan sebagai informasi tambahan dalam Retrieval-Augmented Diffusion Model. Retrieval-Augmented Diffusion Model menghasilkan prediksi probabilistik berupa beberapa kemungkinan kondisi cuaca. Dengan demikian, integrasi kedua pendekatan tersebut menjadi landasan bagi pengembangan prediksi cuaca satu jam ke depan yang dapat mendukung mitigasi risiko hipotermia pendaki di kawasan Gunung Gede–Pangrango [1], [36].

### 2.2.3 Risiko Hipotermia pada Pendakian

Risiko hipotermia merupakan salah satu ancaman keselamatan dalam aktivitas pendakian, termasuk di kawasan pegunungan tropis seperti Gunung Gede–Pangrango [1]. Hipotermia terjadi ketika suhu inti tubuh turun di bawah 35°C karena kehilangan panas tubuh lebih besar daripada panas yang dihasilkan [1].

Di lingkungan pegunungan tropis, paparan hujan dapat membasahi pakaian dan kulit pendaki. Kondisi tersebut mengurangi kemampuan pakaian dalam mempertahankan panas tubuh. Angin juga dapat mempercepat kehilangan panas dari permukaan tubuh, sedangkan kelembapan relatif yang tinggi dapat mempertahankan kondisi basah pada pakaian dan lingkungan [1]. Oleh karena itu, risiko hipotermia tidak hanya berkaitan dengan suhu udara, tetapi juga dengan kombinasi curah hujan, kecepatan angin, kelembapan relatif, dan durasi paparan.

Kelelahan akibat aktivitas pendakian yang berlangsung lama juga dapat meningkatkan kerentanan pendaki terhadap hipotermia. Dalam kondisi lelah, kemampuan tubuh untuk menghasilkan dan mempertahankan panas dapat menurun. Gejala awal seperti menggigil, kelelahan, dan menurunnya koordinasi tubuh juga dapat dianggap sebagai kelelahan biasa sehingga berpotensi terlambat dikenali [1].

Ketiga variabel tersebut, yaitu curah hujan, kecepatan angin, dan kelembapan relatif, merupakan kondisi cuaca yang relevan untuk diprediksi dalam penelitian ini. Hubungan antara prediksi cuaca dan mitigasi risiko dibahas lebih lanjut pada Subbab 2.2.3.3.

#### 2.2.3.1 Mekanisme Hipotermia di Lingkungan Pegunungan Tropis

Hipotermia terjadi ketika tubuh kehilangan panas lebih cepat daripada kemampuan tubuh untuk menghasilkan panas. Di lingkungan pegunungan tropis, kondisi tersebut dapat dipicu oleh hujan, pakaian basah, angin, dan durasi paparan yang panjang, meskipun suhu udara tidak serendah wilayah pegunungan bersalju [1].

Kehilangan panas tubuh dapat terjadi melalui beberapa mekanisme. **Konduksi** merupakan perpindahan panas melalui kontak langsung antara tubuh dan permukaan yang lebih dingin, termasuk pakaian atau kulit yang basah. **Konveksi** merupakan kehilangan panas akibat pergerakan udara di sekitar tubuh dan dapat meningkat ketika pendaki terpapar angin. Sementara itu, **evaporasi** merupakan kehilangan panas ketika air menguap dari permukaan kulit atau pakaian yang basah [1].

Hujan dan pakaian basah dapat memperbesar kehilangan panas melalui konduksi dan evaporasi. Pakaian yang basah juga memiliki kemampuan perlindungan yang lebih rendah dibandingkan pakaian dalam kondisi kering. Selain itu, angin dapat mempercepat perpindahan udara di sekitar tubuh sehingga kehilangan panas melalui konveksi menjadi lebih besar [1].

Di kawasan Gunung Gede–Pangrango, perubahan kondisi cuaca dapat terjadi antarlokasi dan dalam waktu yang relatif singkat karena pengaruh topografi, elevasi, arah angin, dan pembentukan hujan orografis [11], [35]. Perubahan tersebut dapat menyebabkan pendaki mengalami paparan hujan, angin, dan kelembapan yang berbeda sepanjang jalur pendakian, mulai dari elevasi rendah hingga elevasi yang lebih tinggi.

Dengan demikian, prediksi curah hujan, kecepatan angin, dan kelembapan relatif dapat memberikan informasi mengenai kondisi meteorologis yang berpotensi meningkatkan paparan dingin. Prediksi tersebut bukan diagnosis hipotermia, tetapi dapat menjadi informasi pendukung dalam pemantauan kondisi cuaca selama aktivitas pendakian.

#### 2.2.3.2 Faktor Meteorologis yang Berkaitan dengan Risiko Hipotermia

Faktor meteorologis yang berkaitan dengan paparan dingin di wilayah pegunungan tropis meliputi curah hujan, kecepatan angin, dan kelembapan relatif [1]. Curah hujan yang tinggi dapat membasahi pakaian pendaki dan memperbesar kehilangan panas. Kecepatan angin dapat mempercepat perpindahan udara di sekitar tubuh. Kelembapan relatif digunakan sebagai informasi tambahan untuk menilai kondisi lingkungan yang berkaitan dengan kebasahan pakaian dan paparan dingin.

**Tabel 2.3 Faktor Meteorologis terkait Paparan Dingin Pendaki [1], [58]**

| Faktor | Dampak Potensial | Variabel Model | Peran Informasi Nowcasting |
|---|---|---|---|
| Curah hujan | Membasahi pakaian dan meningkatkan kehilangan panas melalui konduksi serta evaporasi. | Curah hujan. | Memberi peringatan peluang hujan pada satu jam berikutnya. |
| Kecepatan angin | Meningkatkan kehilangan panas melalui konveksi dan pergerakan udara di sekitar tubuh. | Kecepatan angin. | Mengidentifikasi kondisi angin yang berpotensi memperburuk paparan. |
| Kelembapan relatif | Memengaruhi kondisi basah pada pakaian dan lingkungan. | Kelembapan relatif. | Melengkapi interpretasi kondisi basah dan kenyamanan termal. |

Ketiga variabel tersebut merupakan indikator kondisi meteorologis yang dapat meningkatkan paparan pendaki terhadap dingin. Pada node utama (`MAIN`) sebagai titik prediksi, informasi dari node `UP`, `DOWN`, `LEFT`, dan `RIGHT` digunakan untuk menggambarkan kondisi cuaca di sekitar lokasi tersebut [7], [16]. Perbedaan kondisi antarlokasi dapat membantu model mempelajari variasi cuaca di sekitar `MAIN`, termasuk perubahan curah hujan dan angin yang berpotensi meningkatkan paparan dingin [1].

Pendekatan probabilistik digunakan untuk merepresentasikan beberapa kemungkinan kondisi cuaca, terutama karena intensitas hujan dapat berubah dan memiliki kejadian ekstrem yang jarang [6], [25]. Informasi tersebut tidak digunakan untuk menghitung risiko hipotermia secara langsung, tetapi dapat menjadi dasar untuk memahami kondisi meteorologis yang berkaitan dengan paparan dingin pendaki.

#### 2.2.3.3 Relevansi Nowcasting Probabilistik sebagai Mitigasi Risiko

Nowcasting probabilistik dengan horizon satu jam ke depan dapat menyediakan informasi mengenai kemungkinan perubahan curah hujan, kecepatan angin, dan kelembapan relatif. Informasi tersebut dapat menjadi bahan pertimbangan dalam menilai kondisi cuaca selama aktivitas pendakian [1], [46].

Hasil keluaran model berupa distribusi probabilitas pada node `MAIN` dapat menjadi masukan bagi pengembangan indeks risiko hipotermia multi-faktor pada penelitian lanjutan. Indeks tersebut tidak menjadi keluaran langsung dalam penelitian ini. Penelitian ini berfokus pada prediksi kondisi meteorologis yang berpotensi meningkatkan paparan dingin pendaki.

Integrasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network digunakan untuk menghasilkan prediksi probabilistik dengan memanfaatkan informasi historis dan hubungan kondisi cuaca antarlokasi [7], [25]. Pendekatan tersebut diharapkan dapat membantu model merepresentasikan ketidakpastian dan perubahan cuaca, termasuk kemungkinan terjadinya hujan berintensitas tinggi. Kemampuan model dalam mendeteksi kejadian ekstrem dan menghasilkan prediksi yang bermanfaat perlu dievaluasi berdasarkan hasil eksperimen.

Dalam penerapannya, hasil nowcasting dapat menjadi dasar pengembangan sistem pendukung keputusan bagi pengelola kawasan dan pendaki. Namun, penelitian ini tidak mengukur penurunan kejadian hipotermia, perubahan perilaku pendaki, atau efektivitas sistem peringatan dini secara operasional. Oleh karena itu, kontribusi model terhadap mitigasi risiko dipahami sebagai penyediaan informasi cuaca pendukung bagi keselamatan aktivitas pendakian [1], [22], [46].

### 2.2.4 Model Generatif Probabilistik dengan Diffusion Model

Model generatif probabilistik, seperti *diffusion model*, digunakan untuk menghasilkan beberapa kemungkinan kondisi cuaca masa depan, bukan hanya satu nilai prediksi. Pendekatan ini relevan dalam *nowcasting* karena kondisi atmosfer dapat berubah dan tidak selalu dapat diprakirakan secara pasti. Dengan menghasilkan beberapa kemungkinan prediksi, model dapat memberikan informasi mengenai ketidakpastian kondisi cuaca yang diprakirakan [6], [25].

Salah satu pendekatan generatif probabilistik yang digunakan dalam penelitian ini adalah *diffusion model*. Model ini bekerja melalui dua tahap utama. Pada tahap pertama, *noise* ditambahkan secara bertahap ke data asli. Pada tahap kedua, model mempelajari cara mengurangi *noise* tersebut secara bertahap untuk menghasilkan sampel prediksi. Proses pertama disebut *forward diffusion*, sedangkan proses kedua disebut *reverse denoising* [16], [25].

Dalam penelitian ini, *diffusion model* digunakan untuk menghasilkan prediksi probabilistik tiga variabel cuaca pada node `MAIN`, yaitu curah hujan, kecepatan angin, dan kelembapan relatif. Target prediksi berbentuk vektor, sedangkan informasi dari kondisi cuaca sebelumnya, representasi spasio-temporal, dan analog historis digunakan sebagai informasi tambahan selama proses pembentukan prediksi. Proses penambahan noise secara bertahap pada data dapat dinyatakan sebagai berikut [25], [39]:

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\left(x_t;\sqrt{1-\beta_t}\,x_{t-1},\beta_t I\right) \tag{2.5}
$$

Selanjutnya, fungsi loss untuk meminimalkan perbedaan antara noise aktual dan noise prediksi dapat dinyatakan sebagai berikut [25], [39]:

$$
L_{diff} = \mathbb{E}_{x_0,\epsilon,t}\left[\left\|\epsilon-\epsilon_\theta(x_t,t,c)\right\|_2^2\right] \tag{2.6}
$$

dengan:

- `x_0` = target asli;

- `x_t` = target bernoise pada timestep diffusion `t`;

- `β_t` = varians noise pada timestep `t`;

- `I` = matriks identitas;

- `ε` = noise Gaussian yang ditambahkan;

- `ε_θ` = noise yang diprediksi model; dan

- `c` = kondisi tambahan, berupa representasi historis, spasial, dan retrieval.

Pada tahap pelatihan, hasil jaringan `ε_θ` bukanlah hasil prediksi cuaca akhir, melainkan perkiraan noise yang terdapat pada target bernoise `x_t`. Perkiraan noise tersebut dibandingkan dengan noise aktual `ε` melalui fungsi loss pada Formula 2.6. Pada tahap pembentukan prediksi, model memulai proses *reverse diffusion* dari noise acak, kemudian menggunakan perkiraan noise secara berulang untuk mengurangi noise sedikit demi sedikit. Setelah proses tersebut selesai, hasilnya dikembalikan ke ruang data cuaca dan menjadi sampel prediksi berupa curah hujan, kecepatan angin, dan kelembapan relatif pada node `MAIN`. Beberapa sampel yang dihasilkan membentuk prediksi ensemble. Dengan demikian, hasil akhir diffusion model bukan nilai `ε_θ`, melainkan kondisi cuaca yang diperoleh setelah seluruh proses denoising selesai [25], [39].

Sejumlah penelitian melaporkan bahwa diffusion models memiliki kualitas sampel dan stabilitas pelatihan yang kompetitif dibandingkan sebagian pendekatan generatif sebelumnya, seperti Generative Adversarial Networks (GAN), pada konfigurasi eksperimen tertentu [25], [30]. Dalam penelitian ini, kualitas sampel, sensitivitas terhadap kejadian ekstrem, dan relevansinya terhadap prediksi cuaca di kawasan dengan dinamika orografis menjadi bagian dari evaluasi model [7], [31].

#### 2.2.4.1 Prinsip Kerja Diffusion Model untuk Nowcasting

Diffusion models terdiri dari dua proses utama, yaitu *forward diffusion process* dan *reverse denoising process*. *Forward diffusion process* adalah proses penambahan noise secara bertahap pada data. *Reverse denoising process* adalah proses pengurangan noise secara bertahap untuk membentuk kembali sampel prediksi berdasarkan informasi kondisi [6], [16], [25]. Pada penelitian ini, data yang diberi noise berbentuk vektor target cuaca ternormalisasi pada node `MAIN`, bukan citra radar. Proses *forward diffusion* dapat dituliskan sebagai berikut:

$$
x_t = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\varepsilon \tag{2.7}
$$

Estimasi noise dikondisikan pada target bernoise, timestep, representasi graf, dan retrieval:

$$
\hat{\varepsilon}=f_\theta(x_t,t,h_t^G,R_t) \tag{2.8}
$$

Embedding timestep dapat menggunakan fungsi GELU [38]:

$$
\operatorname{GELU}(x)=x\Phi(x) \tag{2.9}
$$

Denoising network mempelajari pemetaan dari target bernoise dan kondisi menuju estimasi noise. Setelah proses reverse diffusion selesai, satu kali proses sampling menghasilkan satu sampel prediksi pada ruang target. Jika proses sampling diulang dengan noise awal yang berbeda, kumpulan sampel tersebut membentuk ensemble dan digunakan untuk mendekati distribusi prediktif bersyarat:

$$
p\left(y_{t+1}^{\mathrm{MAIN}} \mid X_{\leq t},h_t^G,R_t\right) \tag{2.10}
$$

dengan `y_{t+1}^{MAIN}` sebagai vektor target cuaca satu jam ke depan, `X_{\leq t}` sebagai informasi historis hingga waktu pengamatan `t`, `h_t^G` sebagai representasi graf, dan `R_t` sebagai representasi analog historis.

Proses sampling bertahap memungkinkan *diffusion model* menghasilkan beberapa sampel dengan variasi yang berbeda. Dalam *nowcasting* hujan, *multiple plausible realizations* berarti beberapa sampel prediksi yang mungkin untuk merepresentasikan ketidakpastian kondisi cuaca. Keragaman sampel dan kualitas representasi ketidakpastian tersebut perlu dinilai melalui evaluasi probabilistik dan evaluasi berbasis kejadian [7], [25], [31].

Diffusion models dapat dikondisikan terhadap variabel tambahan melalui informasi yang dimasukkan ke dalam denoising network. Dalam penelitian ini, kondisi cuaca sebelumnya, angin, kelembapan, informasi spasial elevasi, dan hasil retrieval digunakan sebagai informasi tambahan [6], [25]. Informasi spasio-temporal dari beberapa node diringkas melalui Spatio-Temporal Graph Neural Network untuk membantu proses pembentukan prediksi pada node `MAIN` [7], [16].

#### 2.2.4.2 MLP sebagai Denoiser pada Diffusion Model

Denoiser penelitian ini menggunakan multilayer perceptron (MLP) pada diffusion model. MLP merupakan jaringan yang tersusun atas beberapa lapisan terhubung penuh dan digunakan untuk mempelajari hubungan nonlinier antara target bernoise dan informasi pengondisi. Target yang diberi noise, informasi cuaca, retrieval, representasi graf, dan timestep diproses sebagai representasi vektor. Penggunaan MLP sebagai denoiser pada data berbentuk tabel juga diterapkan dalam diffusion model untuk data noncitra [39], [48]. Pada proses ini, MLP memperkirakan noise dari target bernoise dan kondisi tambahan, bukan langsung menghasilkan nilai cuaca akhir. Dalam penelitian ini, hubungan antarnode telah diringkas lebih dahulu oleh Spatio-Temporal Graph Neural Network sehingga denoiser MLP memproses representasi vektor tersebut.

Lebar lapisan MLP dapat diperbesar atau diperkecil sesuai kebutuhan representasi. Pelebaran lapisan, misalnya dari 64 menjadi 128 unit, menyediakan ruang representasi yang lebih besar untuk mempelajari hubungan nonlinier yang lebih beragam. Penyempitan lapisan, misalnya dari 128 menjadi 64 unit, meringkas informasi ke representasi yang lebih ringkas sebelum diteruskan ke lapisan berikutnya atau ke lapisan hasil akhir. Pemilihan jumlah lapisan dan unit tersembunyi merupakan bagian dari desain arsitektur MLP dan dapat memengaruhi kinerja model serta risiko *overfitting* [52]. DiffImpute menunjukkan bahwa diffusion model untuk data tabular dapat menggunakan beberapa pilihan arsitektur denoiser, termasuk MLP, sehingga bentuk dan kapasitas denoiser merupakan bagian dari rancangan model [48].

Aktivasi SiLU digunakan sebagai fungsi nonlinier pada lapisan MLP. SiLU didefinisikan sebagai:

$$
\operatorname{SiLU}(x)=x\sigma(x) \tag{2.11}
$$

Penggunaan SiLU merupakan pilihan arsitektur pada jaringan generatif [40]. Pengaruhnya terhadap optimisasi dan performa bergantung pada data, konfigurasi, dan hasil eksperimen.

*Skip connection* adalah jalur yang menghubungkan representasi dari lapisan sebelumnya dengan lapisan berikutnya sehingga informasi dari tahap awal tetap dapat digunakan pada tahap pemrosesan selanjutnya. *Residual connection* merupakan salah satu bentuk *skip connection* yang menggabungkan representasi melalui penjumlahan. DenseNet merupakan contoh arsitektur yang menggabungkan fitur melalui konkatenasi [50], [51]. Pada penelitian ini, *skip connection* menggunakan konkatenasi. Jika `h_mid` dan `h_2` merupakan representasi dari dua lapisan, keduanya digabungkan pada dimensi fitur:

$$
h_{skip}=h_{mid}\,\|\,h_2 \tag{2.12}
$$

Hasil konkatenasi tersebut diteruskan ke lapisan berikutnya untuk menghasilkan estimasi noise. Dengan demikian, skip connection membantu mempertahankan informasi dari representasi sebelumnya selama proses pemetaan noise, sedangkan hasil prediksi cuaca diperoleh setelah proses reverse diffusion selesai.

#### 2.2.4.3 Peran Diffusion Model pada Arsitektur Penelitian

Pendekatan deterministik berbasis regresi atau Numerical Weather Prediction (NWP) dapat memiliki keterbatasan pada *lead time* pendek, yaitu rentang waktu antara saat prakiraan dibuat dan waktu prediksi berlaku, terutama ketika prediksi terlalu dekat dengan nilai rata-rata dan kurang merepresentasikan kejadian ekstrem [32], [34]. Model prakiraan berbasis machine learning juga menghadapi tantangan dalam merepresentasikan ketidakpastian dan *rapid error growth*, yaitu pertumbuhan kesalahan prakiraan dalam waktu singkat, pada skala per jam [16], [32].

Diffusion model dipilih karena termasuk pendekatan probabilistik generatif yang dapat memodelkan beberapa kemungkinan kondisi cuaca, bukan hanya satu nilai prediksi [6], [25]. Dalam penelitian ini, diffusion model digunakan untuk mempelajari pola cuaca yang berubah menurut lokasi dan waktu serta menghasilkan ensemble prediksi. Retrieval-Augmented Diffusion Model memanfaatkan analog historis sebagai informasi pengondisi tambahan selama proses denoising. Retrieval membantu model menggunakan informasi dari kejadian historis yang serupa, sedangkan pengaruhnya terhadap akurasi, kalibrasi, deteksi kejadian ekstrem, dan kualitas ensemble dinilai melalui metrik evaluasi [1], [7], [16], [25], [31]. Kalibrasi adalah kesesuaian antara probabilitas yang diperkirakan model dan frekuensi kejadian aktual.

Pemilihan diffusion model dalam penelitian ini berkaitan dengan kebutuhan nowcasting cuaca pegunungan yang memiliki perubahan kondisi menurut lokasi dan waktu serta ketidakpastian prediksi. Kesesuaian pendekatan tersebut terhadap data penelitian, kualitas prediksi, dan kemampuan merepresentasikan kejadian ekstrem menjadi bagian dari evaluasi model [7], [11].

### 2.2.5 Retrieval-Based Historical Analogs

*Retrieval-Based Historical Analogs* merupakan mekanisme untuk mencari kondisi historis yang memiliki kemiripan dengan kondisi cuaca saat ini. Kondisi historis tersebut digunakan sebagai informasi tambahan bagi model, bukan sebagai pengganti proses *reverse diffusion*. Dalam penelitian ini, kondisi cuaca pada periode pengamatan digunakan sebagai *query*, yaitu masukan pencarian, untuk menemukan analog historis yang serupa pada basis data pelatihan [27].

Kondisi historis yang serupa dapat memberikan gambaran mengenai pola perubahan cuaca yang pernah terjadi. Hasil retrieval kemudian digunakan sebagai informasi pengondisi tambahan selama proses *denoising* pada *Retrieval-Augmented Diffusion Model*. Pengaruh informasi analog historis terhadap akurasi, kalibrasi, deteksi kejadian ekstrem, dan kualitas ensemble dinilai melalui metrik evaluasi [16], [27], [31].

Secara konseptual, penggunaan informasi retrieval tidak mengubah proses *diffusion*. Analog historis dimasukkan ke dalam kondisi tambahan `c` bersama informasi historis dan spasial. Dengan demikian, *diffusion model* tetap melakukan penambahan *noise*, estimasi *noise*, dan proses *denoising* seperti dirumuskan pada Formula 2.5–2.6. Retrieval berperan menyediakan informasi dari analog historis, bukan menggantikan proses *diffusion* [25], [27].

### 2.2.6 Spatio-Temporal Graph Neural Network untuk Pemodelan Cuaca

Kondisi cuaca memiliki hubungan spasial karena dapat berbeda antarlokasi dan memiliki hubungan temporal karena berubah dari waktu ke waktu [11], [14]. Spatio-Temporal Graph Neural Network digunakan untuk mempelajari kedua jenis hubungan tersebut secara bersamaan. Spatio-Temporal Graph Neural Network tersusun atas tiga gagasan yang saling berhubungan: Graph Neural Network (GNN) untuk memproses hubungan antar-node, Graph Attention Network (GAT) sebagai lapisan spasial untuk mempelajari kontribusi relatif informasi dari node tetangga, dan pemodelan temporal untuk mempelajari perubahan representasi dari waktu ke waktu.

Pada GAT, *attention mechanism* adalah mekanisme yang memberikan bobot berbeda pada informasi dari setiap node tetangga. Bobot tersebut menunjukkan seberapa besar kontribusi informasi suatu node dalam membentuk representasi node lain yang terhubung. GNN membentuk representasi awal data cuaca, GAT menggabungkan informasi antarnode berdasarkan bobot tersebut, dan pemodelan temporal mengolah hasilnya dari waktu ke waktu. Representasi akhir *Spatio-Temporal Graph Neural Network* digunakan sebagai informasi pengondisi tambahan bagi *diffusion model* [7], [16].

#### 2.2.6.1 Graph Neural Network untuk Representasi Data Cuaca

Graph Neural Network (GNN) merepresentasikan data multi-lokasi sebagai graf yang terdiri atas node, edge, dan fitur node. Node merepresentasikan lokasi pengamatan, edge merepresentasikan hubungan yang digunakan untuk pertukaran informasi, sedangkan fitur node berisi variabel cuaca pada waktu tertentu. Satu graf pada satu waktu disebut *graph snapshot* (snapshot graf). GNN mengolah fitur node dengan menggabungkan informasi dari node yang terhubung melalui *message passing* (pertukaran informasi antarnode) [7], [16].

Hasil pemrosesan tersebut merupakan representasi spasial pada satu waktu. Beberapa snapshot graf kemudian disusun menjadi urutan untuk mempelajari perubahan kondisi cuaca dari waktu ke waktu. Dengan `t` sebagai waktu target, urutan snapshot historis ditulis sebagai:


$$
X_t=\left(x_{t-6},x_{t-5},\ldots,x_{t-1}\right) \tag{2.13}
$$

Dengan:

- `X_t` = urutan enam matriks fitur node sebelum waktu target `t`;

- `x_τ` = matriks fitur node pada satu waktu `τ`;

Urutan graf spasio-temporal dinyatakan sebagai:

$$
\mathcal{G}=\left(G_{t-6},G_{t-5},\ldots,G_{t-1}\right) \tag{2.14}
$$

dengan:

- `G_τ` = graf pada waktu `τ`;

- `\mathcal{G}` = urutan graf yang menjadi input model;

Secara umum, node merepresentasikan lokasi pengamatan, sedangkan edge menyatakan hubungan yang digunakan untuk pertukaran informasi. Pada implementasi, pemrosesan graf dilakukan pada setiap snapshot secara berurutan. Setelah representasi setiap node dibentuk melalui pengodean spasial, representasi tersebut dapat diringkas dengan *global mean pooling*, yaitu perataan representasi seluruh node:

$$
g_\tau=\frac{1}{|V|}\sum_{i\in V}H_{\tau,i} \tag{2.15}
$$

Dengan `g_τ` sebagai representasi graf pada waktu `τ`, `V` sebagai himpunan node, dan `H_{τ,i}` sebagai representasi node ke-`i` setelah pengodean spasial. *Global mean pooling* mengubah representasi seluruh node menjadi satu *graph-level embedding* (representasi tingkat graf). Pada implementasi, pengodean spasial dilakukan oleh GAT pada setiap *graph snapshot*, kemudian hasilnya diringkas melalui *global mean pooling*. Operasi *global mean pooling* pada representasi graf multi-lokasi sejalan dengan alur pemrosesan *Spatio-Temporal Graph Neural Network* pada penelitian terdahulu [43]. Enam representasi graf kemudian disusun sebagai urutan waktu untuk diproses oleh *temporal attention* (mekanisme pemberian bobot pada waktu pengamatan).


#### 2.2.6.2 Graph Attention Network untuk Hubungan Antar-Node

Graph Attention Network (GAT) merupakan pengembangan GNN yang menggunakan *attention mechanism*. Dalam GAT, *attention mechanism* memberikan bobot berbeda pada informasi dari node tetangga untuk menentukan kontribusi relatifnya dalam membentuk representasi node. Mekanisme ini menghasilkan bobot berdasarkan pola statistik pada data dan tidak dimaknai sebagai bukti hubungan sebab-akibat antarnode [44]. Pada setiap pasangan node yang saling terhubung, GAT menghitung skor attention berdasarkan fitur kedua node. Skor tersebut dihitung menggunakan transformasi linear dan fungsi aktivasi *LeakyReLU* [44]:

$$
e_{ij}=\operatorname{LeakyReLU}\left(\mathbf{a}^{\mathsf{T}}[W\mathbf{h}_i\mathbin{\|}W\mathbf{h}_j]\right)
$$

dengan `e_{ij}` sebagai skor attention dari node `j` terhadap node `i`, `W` sebagai matriks transformasi fitur, `h_i` dan `h_j` sebagai fitur node `i` dan `j`, `a` sebagai vektor parameter attention, dan `\|` sebagai operator konkatenasi. *LeakyReLU* mempertahankan sebagian kecil nilai negatif sehingga skor attention tetap dapat diproses ketika hasil transformasi bernilai negatif. Secara matematis, fungsi tersebut dapat ditulis sebagai [44]:

$$
\operatorname{LeakyReLU}(x)=\begin{cases}x, & x\geq 0,\\\lambda x, & x<0,\end{cases}
$$

dengan `x` sebagai nilai masukan dan `λ` sebagai kemiringan pada bagian negatif. Fungsi ini digunakan dalam perhitungan skor attention pada `GATConv` yang digunakan oleh model [44].

Skor attention kemudian dinormalisasi terhadap seluruh node tetangga agar menjadi bobot yang dapat dibandingkan:

$$
\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_{k\in\mathcal{N}_i}\exp(e_{ik})}
$$

dengan `α_{ij}` sebagai bobot attention dari node `j` terhadap node `i` dan `\mathcal{N}_i` sebagai himpunan node tetangga dari node `i`. Pengodean spasial oleh GAT dirumuskan secara umum sebagai:

$$
H_\tau=GAT(G_\tau,X_\tau) \tag{2.16}
$$

dengan `G_τ` sebagai graf pada waktu `τ`, `X_τ` sebagai fitur node pada waktu tersebut, dan `H_τ` sebagai kumpulan representasi seluruh node setelah pengodean spasial. Representasi tingkat graf pada Formula 2.15 diperoleh dengan merata-ratakan representasi node `H_τ`. Pada mekanisme *multi-head attention*, beberapa hasil attention dapat digabungkan melalui konkatenasi [44].

#### 2.2.6.3 Pemodelan Temporal dalam Spatio-Temporal Graph Neural Network

*Spatio-Temporal Graph Neural Network* menyusun representasi spasial dari beberapa *graph snapshot* untuk mempelajari perubahan kondisi cuaca dari waktu ke waktu. Pada penelitian ini, enam representasi graf historis diringkas menggunakan *temporal attention* (mekanisme pemberian bobot pada beberapa waktu pengamatan) [7], [16]:

$$
h_{t-1}^G=\mathrm{TemporalAttention}\left(g_{t-L},\ldots,g_{t-1}\right),\quad L=6 \tag{2.17}
$$

dengan `h_{t-1}^G` sebagai representasi spasio-temporal akhir dari jendela historis, `g_τ` sebagai representasi graf pada waktu `τ`, dan `L` sebagai panjang jendela historis. *Temporal attention* menggunakan *scaled dot-product attention* (perhitungan bobot perhatian berdasarkan kesamaan representasi) dengan *causal mask*:

$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_K}}+M\right)V \tag{2.18}
$$

Pada Formula 2.18, `Q` (*query*) digunakan untuk mencari informasi yang relevan, `K` (*key*) digunakan sebagai pembanding, dan `V` (*value*) berisi informasi yang diringkas. Simbol `d_K` menyatakan dimensi *key*, sedangkan `M` merupakan *causal mask*. Dalam implementasi, `M` membatasi setiap langkah waktu agar hanya menggunakan representasi pada waktu yang sama atau lebih awal dalam urutan historis. Karena seluruh masukan berasal dari waktu `t-6` hingga `t-1`, pembatasan ini menjaga urutan temporal tetap kausal dan tidak menggunakan informasi dari waktu yang lebih baru dalam jendela tersebut. Representasi pada waktu terakhir digunakan sebagai ringkasan urutan graf historis. Secara keseluruhan, GNN membentuk representasi spasial, GAT mengatur penggabungan informasi antarnode, dan *temporal attention* mengolah perubahan representasi tersebut dari waktu ke waktu. Dengan demikian, *Spatio-Temporal Graph Neural Network* menggabungkan informasi antarlokasi dan antarwaktu menjadi representasi spasio-temporal `h_{t-1}^G`, kemudian menggunakannya sebagai informasi pengondisi bagi *diffusion model* untuk menghasilkan prediksi cuaca pada waktu target [43], [44].

Pada mekanisme GAT, penggabungan informasi dari beberapa *attention head* dapat dituliskan sebagai:

$$
h_i'=\mathbin{\|}_{k=1}^{4}\sum_{j\in\mathcal{N}_i}\alpha_{ij}^{k}W^{k}h_j \tag{2.19}
$$

dengan `\mathcal{N}_i` sebagai himpunan node tetangga dari node `i`, `\alpha_{ij}^{k}` sebagai bobot perhatian dari node `j` ke node `i` pada *attention head* ke-`k`, `W^k` sebagai matriks transformasi pada *attention head* ke-`k`, `h_j` sebagai representasi node `j`, dan `\|` sebagai operator konkatenasi. Batas `k=1` hingga `4` menunjukkan penggunaan empat *attention head*.

### 2.2.7 Metrik Evaluasi Prediksi Cuaca

Evaluasi prediksi perlu menilai lebih dari satu aspek. Prediksi titik dinilai berdasarkan kedekatannya dengan observasi, sedangkan prediksi probabilistik dinilai berdasarkan kualitas distribusi kemungkinan yang dihasilkan. Untuk kejadian hujan pada ambang tertentu, evaluasi juga perlu menilai kemampuan model dalam mendeteksi kejadian, menghindari alarm palsu, dan memberikan probabilitas yang sesuai dengan frekuensi kejadian aktual [53], [54].

#### 2.2.7.1 MAE, RMSE, dan Pearson Correlation

Mean Absolute Error (MAE), Root Mean Square Error (RMSE), dan Pearson Correlation Coefficient (`r`) merupakan metrik evaluasi *deterministic forecast* atau prediksi titik [53], [55]. Pada penelitian ini, prediksi titik diringkas menggunakan median ensemble. MAE mengukur rata-rata nilai absolut selisih antara prediksi dan observasi:

$$
\mathrm{MAE}=\frac{1}{N}\sum_{i=1}^{N}|\hat{y}_i-y_i| \tag{2.20}
$$

dengan `\hat{y}_i` sebagai prediksi, `y_i` sebagai observasi, dan `N` sebagai jumlah waktu evaluasi. Nilai MAE yang lebih kecil menunjukkan kesalahan absolut rata-rata yang lebih kecil.

Root Mean Square Error (RMSE) memberikan bobot lebih besar pada kesalahan yang besar:

$$
\mathrm{RMSE}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(\hat{y}_i-y_i)^2} \tag{2.21}
$$

Pearson Correlation Coefficient (`r`) mengukur keeratan hubungan linear antara prediksi dan observasi:

$$
r=\frac{\sum_{i=1}^{N}(\hat{y}_i-\bar{\hat{y}})(y_i-\bar{y})}{\sqrt{\sum_{i=1}^{N}(\hat{y}_i-\bar{\hat{y}})^2}\sqrt{\sum_{i=1}^{N}(y_i-\bar{y})^2}} \tag{2.22}
$$

dengan `\bar{\hat{y}}` dan `\bar{y}` sebagai rata-rata prediksi dan observasi. MAE menilai rata-rata besar kesalahan tanpa membedakan arahnya, sedangkan RMSE memberikan pengaruh lebih besar pada kesalahan yang besar. Pearson Correlation Coefficient (`r`) menilai kesesuaian pola perubahan prediksi terhadap observasi, bukan jarak absolut antara keduanya [53], [55].

#### 2.2.7.2 CRPS dan Brier Score

Continuous Ranked Probability Score (CRPS) dan Brier Score merupakan metrik evaluasi probabilistik. CRPS menilai kualitas distribusi prediksi kontinu, sedangkan Brier Score menilai ketepatan probabilitas untuk kejadian biner [53], [54]. Continuous Ranked Probability Score (CRPS) menilai jarak antara distribusi prediksi dan nilai observasi. Untuk sampel ensemble `x_1,\ldots,x_M`, bentuk estimator ensemble yang digunakan dalam implementasi adalah:

$$
\mathrm{CRPS}=\frac{1}{M}\sum_{m=1}^{M}|x_m-y|-\frac{1}{2M(M-1)}\sum_{m=1}^{M}\sum_{n=1,\,n\neq m}^{M}|x_m-x_n| \tag{2.23}
$$

dengan `M` sebagai jumlah anggota ensemble, `x_m` sebagai sampel prediksi, dan `y` sebagai observasi. CRPS mempertimbangkan kedekatan sampel terhadap observasi serta penyebaran antarsampel. Formula tersebut berlaku untuk `M>1`. Untuk ensemble satu anggota, CRPS dihitung sebagai `|x_1-y|`, sehingga sama dengan kesalahan absolut. CRPS yang lebih kecil menunjukkan distribusi prediksi yang lebih baik [54].

Brier Score digunakan untuk menilai probabilitas suatu kejadian biner, misalnya curah hujan yang melampaui ambang `u`. Nilai ini menghukum perbedaan kuadrat antara probabilitas yang diprediksi dan hasil kejadian aktual:

$$
\mathrm{BS}=\frac{1}{N}\sum_{i=1}^{N}(p_i-o_i)^2 \tag{2.24}
$$

dengan `p_i` sebagai probabilitas prediksi kejadian, yang dihitung dari proporsi anggota ensemble dengan nilai di atas `u`, dan `o_i` sebagai indikator observasi. Nilai `o_i` adalah `1` jika `y_i>u` dan `0` jika `y_i\leq u`. Nilai Brier Score yang lebih kecil menunjukkan probabilitas yang lebih dekat dengan kejadian aktual [53].

#### 2.2.7.3 POD, FAR, dan CSI

Probability of Detection (POD), False Alarm Ratio (FAR), dan Critical Success Index (CSI) merupakan metrik *event-based verification* atau evaluasi berbasis kejadian. Ketiganya digunakan untuk menilai deteksi hujan setelah kejadian ditentukan berdasarkan ambang curah hujan dan ambang probabilitas prediksi [55]. Untuk mengevaluasi deteksi kejadian, probabilitas ensemble dibandingkan dengan ambang probabilitas `p_0`. Hasilnya diringkas dalam empat jumlah: `H` (*hit*), `M` (*miss*), `F` (*false alarm*), dan `C` (*correct negative*). Metrik yang digunakan adalah:

$$
\mathrm{POD}=\frac{H}{H+M} \tag{2.25}
$$

$$
\mathrm{FAR}=\frac{F}{H+F} \tag{2.26}
$$

$$
\mathrm{CSI}=\frac{H}{H+M+F} \tag{2.27}
$$

POD menunjukkan proporsi kejadian aktual yang berhasil terdeteksi. FAR menunjukkan proporsi prediksi kejadian yang ternyata tidak terjadi. CSI menggabungkan hit, miss, dan false alarm untuk menilai keberhasilan deteksi secara keseluruhan. POD dan CSI yang lebih besar lebih baik, sedangkan FAR yang lebih kecil lebih baik. Jika penyebut suatu metrik bernilai nol, nilai metrik tidak didefinisikan dan dikeluarkan dari agregasi sesuai penanganan pada implementasi evaluasi [55].

#### 2.2.7.4 Reliability Diagram

Reliability Diagram merupakan alat evaluasi kalibrasi probabilitas. Diagram ini membandingkan probabilitas kejadian yang diprediksi dengan frekuensi kejadian aktual pada kelompok prediksi yang memiliki rentang probabilitas serupa. Prediksi dikatakan reliabel apabila probabilitas yang diperkirakan mendekati frekuensi kejadian aktual. Diagram ini digunakan untuk menilai kesesuaian probabilitas, bukan sebagai satu nilai kesalahan tunggal [53], [55].

### 2.2.8 Visualisasi Web Berbasis Vue.js dan FastAPI

Visualisasi berbasis web digunakan untuk menyajikan hasil prediksi cuaca kepada pengguna. Hasil yang ditampilkan dapat berupa prediksi titik, distribusi ensemble, probabilitas kejadian hujan, dan informasi pendukung risiko. Visualisasi ini tidak mengubah proses pelatihan maupun proses prediksi model [47]. FastAPI digunakan sebagai backend untuk menyediakan data hasil prediksi melalui endpoint API. Vue.js digunakan sebagai frontend untuk menampilkan data tersebut dalam bentuk kartu informasi, grafik deret waktu, grafik probabilitas, dan tabel ringkasan. Pemisahan backend dan frontend membantu menjaga fungsi model prediksi tetap terpisah dari tampilan web [47], [49].

Dalam rancangan penelitian ini, FastAPI menyalurkan hasil prediksi dari model, sedangkan Vue.js menyajikan hasil tersebut kepada pengguna. Visualisasi berbasis web berfungsi sebagai media penyampaian informasi, bukan sebagai bagian dari evaluasi kinerja model.

## 2.3 Analisis Celah Penelitian

Penelitian *nowcasting* hujan telah mengembangkan model generatif probabilistik, termasuk *diffusion models*, untuk menghasilkan beberapa kemungkinan prediksi dan merepresentasikan ketidakpastian prakiraan [6], [25], [56]. Hasil penelitian tersebut menunjukkan potensi pendekatan probabilistik, tetapi kualitas prediksi tetap dipengaruhi oleh karakteristik data, metode evaluasi, dan kemampuan model dalam merepresentasikan kejadian ekstrem [7], [16]. Dengan demikian, penggunaan model generatif saja belum menjelaskan bagaimana hubungan kondisi cuaca antarlokasi dan antarwaktu pada wilayah pegunungan direpresentasikan.

Celah penelitian berikutnya terletak pada integrasi informasi spasial, temporal, dan historis dalam *nowcasting* cuaca pegunungan. Representasi berbasis grid atau urutan data belum tentu menggambarkan hubungan antarlokasi secara eksplisit, terutama pada wilayah dengan perbedaan elevasi dan perubahan cuaca yang cepat [14], [32]. Selain itu, informasi kondisi historis yang serupa berpotensi membantu proses prediksi, tetapi integrasi *retrieval-based historical analogs* dengan proses *denoising* pada *diffusion model* untuk *nowcasting* satu jam berbasis data *reanalysis* masih terbatas dalam penelitian yang ditinjau [27], [30]. Berdasarkan tinjauan tersebut, belum ditemukan penelitian yang secara bersamaan mengintegrasikan model generatif probabilistik, pencarian analog historis, dan representasi graf spasio-temporal pada lima node ERA5 untuk prediksi cuaca di kawasan Gunung Gede–Pangrango.

Penelitian ini menempatkan *Retrieval-Augmented Diffusion Model* dengan *Spatio-Temporal Graph Neural Network* sebagai pendekatan untuk mengisi celah tersebut. Model menggabungkan analog historis dengan representasi hubungan cuaca antarlokasi dan antarwaktu, kemudian menghasilkan prediksi probabilistik pada node `MAIN` untuk curah hujan, kecepatan angin, dan kelembapan relatif. Posisi penelitian dinilai melalui akurasi prediksi titik, kualitas distribusi probabilistik, dan kemampuan mendeteksi kejadian hujan. Model tidak memprediksi indeks hipotermia; hasil prediksi hanya digunakan sebagai informasi pendukung keselamatan pendakian, sedangkan manfaatnya ditafsirkan berdasarkan hasil evaluasi [46].

---
