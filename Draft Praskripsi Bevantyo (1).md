![Logo Universitas Padjadjaran](media_sp2/image1.jpeg)

PRA-SKRIPSI

NOWCASTING CUACA UNTUK MITIGASI RISIKO PENDAKI DI GUNUNG GEDE-PANGRANGO MENGGUNAKAN RETRIEVAL-AUGMENTED DIFFUSION MODEL DENGAN SPATIO-TEMPORAL GRAPH NEURAL NETWORK

BEVANTYO SATRIA PINANDHITA

NPM 22081010153

DOSEN PEMBIMBING

Dr. Faisal Muttaqin, S.Kom, M.T

Andreas Nugroho Sihananto, S.Kom., M.Kom.

KEMENTERIAN PENDIDIKAN, KEBUDAYAAN, RISET, DAN TEKNOLOGI UNIVERSITAS PEMBANGUNAN NASIONAL VETERAN JAWA TIMUR FAKULTAS ILMU KOMPUTER

PROGRAM STUDI INFORMATIKA SURABAYA

2026

# ABSTRAK

Nama Mahasiswa / NPM: Bevantyo Satria Pinandhita / 22081010153

Judul Skripsi:Nowcasting Cuaca Untuk Mitigasi Risiko Pendaki di Gunung Gede–Pangrango Menggunakan Retrieval-Augmented Diffusion Model Dengan Spatio-Temporal Graph Neural Network

Dosen Pembimbing: 1. Dr. Faisal Muttaqin, S.Kom, M.T

2. Andreas Nugroho Sihananto, S.Kom., M.Kom.

[DRAFT]

Nowcasting cuaca jangka pendek pada skala waktu 0–6 jam memiliki peran penting dalam mitigasi risiko bencana dan keselamatan aktivitas luar ruang, terutama pada wilayah pegunungan dengan dinamika atmosfer yang cepat berubah. Kawasan Gunung Gede–Pangrango merupakan salah satu lokasi pendakian dengan intensitas kunjungan tinggi dan kondisi cuaca yang kompleks, sehingga perubahan presipitasi, angin, dan kelembapan dapat menimbulkan risiko keselamatan bagi pendaki. Namun, pendekatan prakiraan cuaca deterministik konvensional sering kali kurang mampu merepresentasikan ketidakpastian atmosfer serta cenderung mengalami bias terhadap nilai rata-rata, yang menyebabkan keterbatasan dalam mendeteksi kejadian presipitasi ekstrem. Penelitian ini bertujuan mengembangkan model nowcasting presipitasi probabilistik untuk mendukung mitigasi risiko pendakian di kawasan Gunung Gede–Pangrango. Model yang diusulkan menggunakan pendekatan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning untuk memodelkan hubungan spasial dan temporal antar lokasi pengamatan. Data cuaca diperoleh dari dataset reanalysis ERA5 melalui Open-Meteo API dengan resolusi waktu per jam. Model dilatih untuk menghasilkan distribusi probabilistik kondisi presipitasi satu jam ke depan ( $t+1$ ), yang berada dalam rentang nowcasting 0–6 jam menurut WMO. Kinerja model dievaluasi menggunakan metrik statistik dan probabilistik serta dibandingkan dengan pendekatan regresi deterministik berbasis machine learning. Hasil penelitian diharapkan dapat memberikan pendekatan nowcasting yang lebih adaptif dalam merepresentasikan ketidakpastian cuaca serta meningkatkan sensitivitas deteksi terhadap kejadian presipitasi yang berpotensi membahayakan aktivitas pendakian.

Kata kunci: Diffusion model, Mitigasi risiko pendakian, Nowcasting cuaca, Presipitasi probabilistik, Spatio-temporal graph

# ABSTRACT

Nama Mahasiswa / NPM: Bevantyo Satria Pinandhita / 22081010153

Judul Skripsi:Nowcasting Cuaca Untuk Mitigasi Risiko Pendaki di Gunung Gede–Pangrango Menggunakan Retrieval-Augmented Diffusion Model Dengan Spatio-Temporal Graph Neural Network

Dosen Pembimbing: 1. Dr. Faisal Muttaqin, S.Kom, M.T

2. Andreas Nugroho Sihananto, S.Kom., M.Kom.

[DRAFT]

Short-term weather nowcasting within a 0–6 hour horizon plays a crucial role in disaster risk mitigation and outdoor activity safety, particularly in mountainous regions where atmospheric conditions can change rapidly. The Gunung Gede–Pangrango area is one of the most popular hiking destinations in Indonesia and exhibits complex climate dynamics, where variations in precipitation, wind, and humidity may pose significant risks to hikers. Conventional deterministic weather forecasting approaches often fail to adequately represent atmospheric uncertainty and tend to exhibit bias toward mean values, limiting their capability to detect extreme precipitation events. This study aims to develop a probabilistic precipitation nowcasting model to support risk mitigation for hiking activities in the Gunung Gede–Pangrango region. The proposed approach employs a Retrieval-Augmented Diffusion Model combined with Spatio-Temporal Graph Conditioning to capture spatial and temporal dependencies among observation locations. Weather data are obtained from the ERA5 reanalysis dataset through the Open-Meteo API with hourly temporal resolution. The model is trained to generate probabilistic distributions of precipitation conditions one hour ahead (t+1), within the WMO nowcasting range of 0–6 hours. Model performance is evaluated using statistical and probabilistic metrics and compared with deterministic machine learning regression approaches. The expected outcome of this research is a more adaptive nowcasting framework capable of representing atmospheric uncertainty while improving sensitivity to precipitation events that may pose hazards for mountain hiking activities.

Keywords: Diffusion model, hiking risk mitigation, probabilistic precipitation, spatio-temporal graph, weather nowcasting

# DAFTAR ISI

# DAFTAR GAMBAR

# DAFTAR TABEL

# DAFTAR ISTILAH

Domain Meteorologi & Mitigasi Bencana

Nowcasting: Prakiraan cuaca resolusi temporal tinggi untuk rentang 0–6 jam ke depan berbasis kondisi atmosfer terkini.

Hujan Orografis (Orographic Precipitation): Hujan yang terbentuk akibat naiknya massa udara lembap saat melewati lereng pegunungan.

Pengangkatan Orografis (Orographic Lifting): Proses terangkatnya parsel udara secara mekanis oleh rintangan topografi hingga mengalami pendinginan dan kondensasi.

Inisiasi Konvektif (Convective Initiation): Tahap awal pembentukan arus udara vertikal naik (updraft) pemicu awan hujan badai lokal.

Lereng Menghadap Angin (Windward Slope): Sisi lereng yang berhadapan langsung dengan arah datangnya angin lembap sehingga menerima curah hujan lebih tinggi.

Lereng Membelakangi Angin (Leeward Slope): Sisi lereng yang terlindung dari angin dan cenderung lebih kering akibat efek bayangan hujan (rain shadow).

Hipotermia: Kondisi penurunan suhu inti tubuh di bawah 35°C saat laju pelepasan panas melebihi produksi panas internal tubuh.

Kehilangan Panas Konvektif (Convective Heat Loss): Pelepasan panas tubuh akibat tiupan aliran udara dingin di sekitar permukaan kulit (wind chill).

Kehilangan Panas Konduktif (Conductive Heat Loss): Pelepasan panas tubuh melalui kontak fisik langsung dengan media yang lebih dingin, seperti pakaian basah kuyup.

Sumber Data & Prapemrosesan (Preprocessing)

ERA5: Data reanalisis iklim global generasi kelima ECMWF dengan resolusi spasial $∼ 25 km$ ( $0,25^{∘}$ ) dan resolusi waktu per jam.

Reanalisis Atmosfer: Rekonstruksi data cuaca historis global tanpa kekosongan (gap-free) berbasis kombinasi model numerik dan observasi riil.

Open-Meteo API: Antarmuka pemrograman aplikasi terbuka untuk mengakses data reanalisis dan prakiraan cuaca tanpa autentikasi kunci API.

Node MAIN: Titik grid observasi target prediksi utama di area puncak/kawah Gunung Gede–Pangrango (lintang $-6,75^{∘}$ , bujur $107,00^{∘}$ $).

Node Konteks Spasial (UP, DOWN, LEFT, RIGHT): Empat titik grid lereng di sisi utara, selatan, barat, dan timur penyedia informasi cuaca regional di sekitar titik utama.

Kebocoran Data (Data Leakage): Masuknya informasi dari data validasi atau uji ke dalam proses pelatihan model secara tidak sengaja.

Lag Temporal ( $t-1$ ): Nilai observasi satu jam sebelumnya yang digunakan sebagai fitur masukan model.

Distribusi Berekor Berat (Heavy-Tailed Distribution): Karakteristik sebaran data dengan kemunculan nilai ekstrem yang jauh lebih tinggi daripada distribusi normal.

Inflasi Nol (Zero-Inflation): Kondisi data deret waktu yang didominasi oleh nilai nol (jam tanpa hujan).

Transformasi log1p: Transformasi logaritma natural untuk meredam kemiringan sebaran data bernilai nol tanpa menghasilkan nilai tak hingga.

Standardisasi Z-Score: Penyetaraan skala data menjadi rata-rata $\mu =0$ dan simpangan baku $\sigma =1$ .

Arsitektur Model (RADM-STGNN)

Graf Spasio-Temporal ( $G$ ): Struktur data graf yang memodelkan keterhubungan ruang (node) dan perubahan waktu (snapshot temporal).

Snapshot Graf ( $G_{\tau}$ ): Struktur graf statis yang memuat fitur seluruh node pada satu langkah waktu $\tau$.

Topologi Bintang (Star Topology): Konfigurasi graf saat node pusat (MAIN) terhubung dua arah dengan node lereng lainnya tanpa interkoneksi antarnode lereng.

Graph Attention Network (GAT): Varian graf konvolusional yang menghitung bobot pengaruh dinamis antar-node menggunakan mekanisme atensi.

Penyampaian Pesan (Message Passing): Proses agregasi dan pertukaran informasi fitur antar-node yang saling terhubung pada graf.

Perataan Global Graf (Global Mean Pooling): Operasi perataan seluruh fitur node untuk menghasilkan satu vektor ringkasan graf tunggal.

Atensi Temporal Kausal (Causal Temporal Attention): Mekanisme pembobotan waktu historis dengan pembatas (causal mask) guna mencegah kebocoran informasi masa depan.

Model Difusi (Diffusion Model): Kelas model generatif yang memodelkan sebaran probabilitas data melalui proses penambahan dan pengurangan derau acak.

Difusi Maju (Forward Diffusion): Proses penambahan derau Gaussian bertahap hingga data target berubah menjadi derau murni $N\left(0,I\right)$ .

Denoising Mundur (Reverse Denoising): Rekonstruksi bertahap data target bersih dari derau acak menggunakan estimasi jaringan saraf.

DDPM (Denoising Diffusion Probabilistic Models): Formulasi difusi berbasis rantai Markov diskret dengan proses pemulihan bertahap.

DDIM (Denoising Diffusion Implicit Models): Metode inferensi difusi non-Markovian untuk mempercepat proses sampling dengan jumlah iterasi yang lebih sedikit.

MLP Denoiser: Jaringan Multilayer Perceptron yang bertugas memperkirakan nilai derau $ϵ_{\theta}$ berdasarkan target berderau dan vektor pengondisi.

Skip Connection: Jalur pintas yang menghubungkan representasi lapisan awal ke lapisan akhir untuk mempertahankan sinyal fitur dan menstabilkan gradien.

Sinusoidal Time Embedding: Pemetaan langkah difusi skalar diskret $s$ ke dalam representasi vektor kontinu menggunakan gelombang sinus dan kosinus.

Analog Historis (Historical Analogs): Kejadian cuaca masa lalu yang memiliki kemiripan pola atmosfer dengan kondisi cuaca saat ini.

K-Nearest Neighbors (KNN): Algoritma nonparametrik untuk mencari sejumlah $k$ data terdekat pada ruang fitur.

FAISS (Facebook AI Similarity Search): Pustaka komputasi efisien untuk operasi pencarian kemiripan vektor berdimensi tinggi.

Pembelajaran Multi-Tugas (Multi-Task Learning): Pelatihan model dengan dua tugas berbeda secara simultan (prediksi derau difusi dan klasifikasi biner presipitasi).

Auxiliary Wet Head: Cabang keluaran jaringan yang menghasilkan nilai logit klasifikasi kejadian hujan atau tidak hujan.

Rain Gate: Mekanisme pengondisian pascapemrosesan yang memaksa nilai prediksi curah hujan menjadi nol jika probabilitas klasifikasi biner berada di bawah ambang batas.

Pelatihan, Optimasi & Inferensi

Weighted Denoising Loss: Fungsi kerugian kuadratik dengan bobot penalti ekstra untuk sampel bernilai ekstrem guna mencegah luaran bias ke nilai rata-rata.

Binary Cross-Entropy (BCE): Fungsi kerugian untuk mengukur galat prediksi probabilitas pada tugas klasifikasi biner.

Pos Weight ( $w_{pos}$ ): Bobot pengali penyeimbang kelas minoritas (kejadian hujan) pada fungsi kerugian klasifikasi biner.

Pemotongan Gradien (Gradient Clipping): Pembatasan panjang norma gradien agar tidak melebihi batas $C_{clip}$ guna mencegah ledakan gradien (exploding gradients).

AdamW: Varian algoritma optimasi berbasis gradien adaptif dengan pemisahan mekanisme peluruhan bobot (weight decay).

Ensemble Sampling: Pembangkitan sekumpulan skenario prediksi masa depan secara probabilistik untuk mengukur tingkat ketidakpastian luaran.

Evaluasi & Verifikasi Meteorologis

Mean Absolute Error (MAE): Rata-rata selisih absolut antara nilai prediksi titik dan nilai observasi aktual.

Root Mean Square Error (RMSE): Akar kuadrat dari rata-rata selisih kuadrat antara prediksi dan observasi, sensitif terhadap galat bernilai besar.

Koefisien Korelasi Pearson (r): Ukuran statistik untuk mengevaluasi derajat kelinearan hubungan antara kurva hasil prediksi dan kurva observasi.

Continuous Ranked Probability Score (CRPS): Metrik verifikasi probabilistik pengukur jarak fungsi distribusi kumulatif prediksi ensemble terhadap nilai observasi aktual.

Brier Score (BS): Rata-rata galat kuadratik antara probabilitas prediksi suatu kejadian terhadap kejadian biner aktual (0 atau 1).

Probability of Detection (POD): Rasio keberhasilan model dalam memprediksi kejadian dibandingkan dengan total seluruh kejadian aktual yang berlangsung (hit rate).

False Alarm Ratio (FAR): Rasio alarm palsu terhadap seluruh prediksi kejadian yang diterbitkan oleh model.

Critical Success Index (CSI): Ukuran keberhasilan deteksi gabungan yang memperhitungkan prediksi tepat (hit), luput (miss), dan alarm palsu (false alarm).

Diagram Keandalan (Reliability Diagram): Grafik evaluasi kalibrasi yang membandingkan probabilitas prediksi model terhadap frekuensi kemunculan aktualnya.

# BAB I
# PENDAHULUAN

## 1.1 Latar Belakang

Hipotermia merupakan kondisi darurat ketika suhu inti tubuh turun secara abnormal akibat kehilangan panas yang melebihi kemampuan tubuh untuk memproduksinya. Pada aktivitas pendakian, risiko hipotermia meningkat ketika pendaki terpapar suhu rendah, angin kencang, hujan, pakaian basah, serta kelelahan fisik dalam durasi yang panjang [1], [2]. Menurut Aminullah et al. [2], data BASARNAS periode 2015–2018 menunjukkan bahwa hipotermia merupakan penyebab kecelakaan pendakian yang paling dominan dengan persentase 47%. Sumber yang sama melaporkan tiga pendaki meninggal akibat hipotermia di Gunung Tampomas pada 2018. Studi eksperimental menunjukkan bahwa mempertahankan pakaian basah setelah paparan dingin dapat memperlambat pemulihan suhu kulit dibandingkan dengan mengganti pakaian basah [58]. Fakta tersebut menegaskan pentingnya ketersediaan informasi kondisi cuaca yang cepat dan akurat agar pendaki dapat mengambil tindakan pencegahan sebelum paparan risiko berkembang menjadi kondisi medis yang mengancam jiwa.

Untuk meminimalkan risiko kecelakaan tersebut, diperlukan informasi prakiraan cuaca jangka pendek (nowcasting) yang mampu memberikan deteksi dini sebelum kondisi berbahaya terjadi. Dalam konteks mitigasi keselamatan pendakian, informasi cuaca per jam lebih relevan untuk mendukung keputusan jangka pendek dibandingkan prakiraan harian karena kondisi atmosfer di pegunungan dapat berubah secara dinamis dalam hitungan jam. Informasi mengenai prakiraan probabilistik curah hujan, yaitu peluang atau sebaran kemungkinan curah hujan dalam rentang waktu tertentu menjadi parameter penting untuk memahami tingkat ketidakpastian cuaca di lapangan. Berbeda dengan prakiraan deterministik yang hanya memberikan nilai tunggal, prakiraan probabilistik menyajikan distribusi kemungkinan kejadian cuaca beserta tingkat keyakinannya. Hal ini memungkinkan pendaki memperoleh gambaran risiko yang lebih realistis, seperti kemungkinan terjadinya hujan lebat mendadak atau peningkatan kecepatan angin yang ekstrem.

Nowcasting cuaca pada rentang waktu sangat pendek (0–6 jam) berperan penting dalam sistem peringatan dini untuk aktivitas luar ruang [3], [4]. Pemanfaatan data radar, model prediksi numerik, dan kecerdasan buatan memungkinkan informasi cuaca diperbarui secara berkala dan cepat guna mendukung keputusan taktis di lapangan [4], [5]. Penerapan metode deep learning dalam nowcasting juga telah terbukti mampu menghasilkan prakiraan curah hujan dan angin dengan resolusi spasial dan temporal yang tinggi [6], [7], [8]. Kendati demikian, efektivitas model ini sangat bergantung pada karakteristik wilayah pengamatan, sehingga evaluasi metodologis yang mendalam pada area dengan kondisi geografis ekstrem sangat diperlukan sebelum model diterapkan secara praktis.

Kawasan Gunung Gede–Pangrango merupakan salah satu destinasi wisata alam dan pendakian dengan intensitas kunjungan yang sangat tinggi, sehingga memiliki risiko keselamatan yang perlu diperhatikan. Berdasarkan kajian daya dukung lingkungan di kawasan Curug Cibeureum [9], curah hujan merupakan salah satu faktor yang perlu dipertimbangkan dalam pengelolaan kawasan wisata. Temuan tersebut menunjukkan bahwa kondisi cuaca dapat berkaitan dengan kapasitas dan keselamatan pengunjung. Oleh karena itu, ketersediaan informasi cuaca per jam di kawasan ini dapat menjadi bahan pertimbangan bagi pihak pengelola dan pendaki dalam menilai kondisi aktivitas di lapangan.

Dinamika hujan di wilayah pegunungan seperti Gunung Gede–Pangrango sangat kompleks karena dipengaruhi oleh interaksi antara topografi, perbedaan elevasi, kelembapan udara, dan arah angin yang disebut dengan mekanisme pengangkatan orografis (orographic lifting). Hal inimemicu kondensasi uap air dan pembentukan awan konvektif secara cepat di lereng atas, sementara siklus harian pemanasan daratan turut menentukan waktu puncak terjadinya hujan [11], [12], [13]. Dinamika lokal ini menciptakan variabilitas spasial yang ekstrem, di mana perbedaan curah hujan yang signifikan dapat terjadi dalam jarak horizontal yang sangat pendek [14], [15]. Ketergantungan spasial dan temporal yang erat antar-elevasi ini membuat prakiraan cuaca per jam di wilayah pegunungan menjadi sangat menantang dan tidak dapat didekati dengan asumsi stasioner.

Model prakiraan cuaca deterministik konvensional dapat mengalami keterbatasan dalam merepresentasikan kejadian ekstrem di pegunungan karena prediksinya cenderung mendekati nilai rata-rata (smoothing effect) [16], [17]. Model deterministik merupakan pendekatan prediksi yang menghasilkan satu nilai untuk setiap waktu dan lokasi, tanpa menyertakan rentang ketidakpastian atau peluang kejadian lainnya. Sebaliknya, pendekatan probabilistik menghasilkan beberapa kemungkinan prediksi beserta peluang atau tingkat ketidakpastiannya, sehingga dapat menggambarkan berbagai kondisi cuaca yang mungkin terjadi. Hambatan utama dalam pemodelan cuaca ini berkaitan dengan kemungkinan karakteristik data hujan yang sebagian besar rekaman data menunjukkan nilai nol atau tidak hujan (zero-inflated) dan sebagian kecil kejadian hujan memiliki intensitas yang sangat ekstrem (heavy-tailed). Karakteristik tersebut perlu dikonfirmasi melalui analisis statistik pada data penelitian. Model regresi deterministik yang dioptimalkan dengan fungsi loss rata-rata akan cenderung memprediksi hujan ringan saat terjadi hujan lebat, dan sebaliknya, memprediksi ada hujan ringan saat kondisi sebenarnya kering. Akibatnya, representasi kejadian ekstrem yang sangat penting untuk mitigasi keselamatan menjadi terabaikan [16], [17].

Untuk mengatasi keterbatasan tersebut, sejumlah penelitian mengembangkan pendekatan probabilistik generatif, termasuk Retrieval-Augmented Diffusion Model (RDM), serta pemodelan spasio-temporal melalui Spatio-Temporal Graph Neural Network (STGNN). Namun, pada penelitian yang ditinjau, kedua pendekatan tersebut masih banyak diterapkan secara terpisah. Beberapa penelitian hanya berfokus pada model generatif untuk ketidakpastian tanpa mempertimbangkan informasi topografi [6], [7], sedangkan sebagian lainnya menggunakan pemodelan spasio-temporal untuk representasi spasial namun menghasilkan keluaran deterministik tunggal [10], [18], [20], [21]. Berdasarkan penelitian yang ditinjau, masih diperlukan kajian yang mengintegrasikan model generatif probabilistik dengan representasi spasial graf untuk menangani karakteristik data hujan pegunungan yang zero-inflated dan heavy-tailed.

Penelitian ini merespons kebutuhan tersebut dengan mengembangkan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network. Dalam model ini, Retrieval-Augmented Diffusion Model bertindak sebagai model generatif utama yang memodelkan distribusi probabilistik cuaca melalui proses diffusion, sehingga mampu menghasilkan beberapa kemungkinan skenario cuaca. Sementara itu, Spatio-Temporal Graph Neural Network digunakan sebagai komponen pengondisi (conditioning) yang memodelkan lima titik lokasi pengamatan sebagai graf untuk menangkap ketergantungan spasial dan evolusi temporal kondisi cuaca di wilayah pegunungan. Kombinasi kedua metode ini dirancang untuk menghasilkan ensemble prakiraan probabilistik yang realistis dan sensitif terhadap nilai ekstrem.

Fokus penelitian ini dibatasi pada evaluasi metodologis model dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif satu jam ke depan di kawasan Gunung Gede–Pangrango dengan menggunakan data ERA5. Dataset ERA5 merupakan data reanalisis global dari European Centre for Medium-Range Weather Forecasts (ECMWF) yang menggabungkan hasil model numerik atmosfer dengan berbagai pengamatan melalui proses asimilasi data. Data ini disajikan pada grid dengan resolusi horizontal sekitar 25 kilometer. Oleh karena itu, nilai ERA5 merupakan estimasi kondisi atmosfer pada grid tersebut dan tidak secara langsung merepresentasikan kondisi cuaca mikro pada titik ketinggian tertentu di puncak gunung [57]. Dalam penelitian ini, ERA5 digunakan untuk menguji kinerja metodologis model pada skala grid yang tersedia, bukan untuk mengklaim representasi kondisi mikrocuaca secara presisi. Atas dasar tersebut, penelitian ini berorientasi pada mitigasi risiko dengan menganalisis hasil prediksi serta kemampuan model dalam mendeteksi kejadian cuaca ekstrem [23]. Selain itu, hasil prediksi dari model ini dirancang untuk diintegrasikan ke dalam visualisasi berbasis web.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, permasalahan penelitian ini dapat dirumuskan sebagai berikut:

Bagaimana kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5?

Bagaimana pengaruh penggabungan mekanisme pencarian kondisi cuaca historis (retrieval) dan representasi graf spasio-temporal terhadap kemampuan model dalam menangkap dinamika spasial-temporal cuaca?

Seberapa baik kemampuan model tersebut dalam merepresentasikan distribusi data curah hujan yang bersifat zero-inflated dan heavy-tailed, serta dalam memprediksi kejadian hujan dengan intensitas tinggi?

Bagaimana perbandingan kinerja antara model probabilistik Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network melawan model deterministik, khususnya dalam hal akurasi prediksi dan deteksi kejadian ekstrem?

Bagaimana hasil prediksi probabilistik dari model tersebut dapat diintegrasikan dan ditampilkan melalui sistem visualisasi berbasis web untuk menyediakan informasi cuaca yang mendukung aktivitas pendakian?

## 1.3 Tujuan Penelitian

Tujuan umum penelitian ini adalah mengevaluasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network untuk nowcasting kondisi cuaca satu jam ke depan di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.

Untuk mencapai tujuan umum tersebut, penelitian ini memiliki tujuan khusus sebagai berikut:

Mengevaluasi kinerja Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan Gunung Gede–Pangrango menggunakan data ERA5.

Menganalisis efektivitas penggabungan mekanisme pencarian kondisi cuaca historis (retrieval) dan representasi graf spasio-temporal dalam menangkap ketidakpastian serta dinamika spasial-temporal cuaca.

Mengevaluasi kemampuan model dalam merepresentasikan distribusi data curah hujan yang bersifat zero-inflated dan heavy-tailed, serta mengukur akurasinya dalam memprediksi kejadian hujan dengan intensitas tinggi.

Membandingkan kinerja model probabilistik yang diusulkan melawan model deterministik dalam hal akurasi prediksi rata-rata dan kemampuan mendeteksi kejadian ekstrem.

Mengembangkan sistem visualisasi berbasis web untuk menampilkan hasil prediksi probabilistik dari model sebagai informasi pendukung pengambilan keputusan dalam aktivitas pendakian.

## 1.4 Manfaat Penelitian

Penelitian ini diharapkan dapat memberikan kontribusi dalam pengembangan metode nowcasting cuaca serta penerapannya dalam mendukung mitigasi risiko aktivitas pendakian di wilayah pegunungan. Manfaat yang diharapkan dari penelitian ini adalah sebagai berikut:

Memberikan kontribusi dalam pengembangan dan evaluasi model nowcasting probabilistik berbasis Retrieval-Augmented Diffusion Model dan Spatio-Temporal Graph Neural Network untuk memodelkan dinamika curah hujan, kecepatan angin, dan kelembapan relatif pada skala waktu per jam di wilayah pegunungan.

Memberikan pemahaman ilmiah mengenai efektivitas penggabungan pencarian kondisi cuaca historis yang serupa pada Retrieval-Augmented Diffusion Model dan representasi graf spasio-temporal pada Spatio-Temporal Graph Neural Network dalam menangkap ketidakpastian serta hubungan spasial-temporal cuaca.

Menyajikan analisis empiris mengenai kemampuan model Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam merepresentasikan ketidakpastian curah hujan yang sering kali bernilai nol (zero-inflated) dan memiliki nilai ekstrem (heavy-tailed), termasuk kepekaan prediksi terhadap kejadian hujan pada berbagai ambang intensitas.

Menyajikan analisis terkait perbandingan antara akurasi prediksi rata-rata dan kemampuan model Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network dalam mendeteksi kejadian ekstrem sebagai dasar dalam pengambilan keputusan berbasis risiko pada aktivitas pendakian di wilayah pegunungan.

Menghasilkan prediksi probabilistik dari model Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network yang dapat digunakan sebagai dasar pengembangan sistem visualisasi berbasis web untuk penyampaian informasi cuaca jangka pendek.

## 1.5 Batasan Masalah

Untuk menjaga fokus penelitian dan memastikan ketercapaian tujuan dalam ruang lingkup skripsi, penelitian ini dibatasi oleh beberapa ketentuan sebagai berikut:

Penelitian difokuskan pada kawasan Gunung Gede–Pangrango yang direpresentasikan oleh 5 titik lokasi.

Penelitian menggunakan data reanalysis ERA5 melalui Open-Meteo API dengan input 6 jam terakhir untuk memprediksi kondisi cuaca 1 jam ke depan.

Target prediksi dibatasi pada curah hujan, kecepatan angin, dan kelembapan relatif.

Penelitian mengevaluasi probabilistic generative modeling yang terintegrasi dengan retrieval-based historical analogs dan spatio-temporal graph representation.

Hasil prediksi tidak merepresentasikan kondisi mikrocuaca secara presisi karena menggunakan data grid reanalysis ERA5.

Penelitian difokuskan pada pengembangan dan evaluasi metodologi nowcasting probabilistik, bukan implementasi sistem operasional.

# BAB II
# TINJAUAN PUSTAKA

## 2.1 Penelitian Terdahulu

Penelitian-penelitian yang telah dilakukan dan relevan dengan penelitian ini mencakup model generatif probabilistik, model graf spasio-temporal, mekanisme retrieval pada diffusion model, model recurrent berbasis attention, serta pendekatan ensemble untuk prakiraan cuaca. Sepuluh penelitian berikut digunakan sebagai landasan perbandingan konseptual. Tiga penelitian yang paling dekat dengan fokus penelitian dirangkum dalam Tabel 2.1, sedangkan penelitian yang diusulkan ditampilkan sebagai baris pembanding keempat. Penelitian yang diusulkan tidak dihitung sebagai penelitian terdahulu.

Penelitian “Precipitation Nowcasting with Generative Diffusion Models” oleh Asperti et al. (2025) [25]

Penelitian ini mengembangkan Generative Ensemble Diffusion (GED) berbasis DDIM dan denoiser U-Net untuk menghasilkan 15 sampel prediksi presipitasi berbasis ERA5. Ensemble dibentuk melalui proses sampling berulang dan dapat diproses menggunakan rata-rata atau post-processing U-Net. Penelitian tersebut relevan karena menunjukkan bahwa diffusion ensemble dapat merepresentasikan beberapa kemungkinan evolusi presipitasi. Perbedaannya terletak pada penggunaan grid Eropa, bukan lima node ERA5 dengan target `MAIN` di Gunung Gede–Pangrango.

Penelitian “Spatio-temporal graph neural networks to improve precipitation forecasts from numerical models” oleh Yousaf et al. (2025) [26]

Penelitian ini mengembangkan WRF-GNN untuk memperbaiki keluaran prakiraan WRF menggunakan informasi 22 rain gauge di Calabria, Italia. Relevansinya terletak pada penggunaan representasi graf untuk memodelkan ketergantungan spasio-temporal. Namun, penelitian ini memakai keluaran WRF, observasi rain gauge, resolusi 2 km, dan horizon satu hari sehingga tidak merupakan reproduksi model pada penelitian ini.

Penelitian “Retrieval-Augmented Diffusion Models for Time Series Forecasting” oleh Liu et al. (2024) [27]

Penelitian ini mengusulkan Retrieval-Augmented Time series Diffusion (RATD), yang mengambil urutan historis serupa melalui embedding retrieval dan memasukkannya ke proses denoising melalui Reference-Modulated Attention. Relevansinya adalah prinsip integrasi retrieval dan diffusion pada data deret waktu. RATD tidak menggunakan lima node, ERA5, target `MAIN`, atau STGNN, sehingga hasilnya tidak dapat dianggap sebagai bukti performa pada presipitasi lokal.

Penelitian “Skilful precipitation nowcasting using deep generative models of radar” oleh Ravuri et al. (2021) [6]

Penelitian ini mengembangkan DGMR berbasis conditional GAN untuk menghasilkan prakiraan presipitasi probabilistik dari empat frame radar dan memprediksi hingga 90 menit. Model menggunakan spatial discriminator, temporal discriminator, dan regularisasi grid-cell. Penelitian ini relevan sebagai rujukan model generatif probabilistik untuk nowcasting, tetapi data radar dan resolusi spasialnya berbeda dari data ERA5 titik-lokasi pada penelitian ini.

Penelitian “Skilful nowcasting of extreme precipitation with NowcastNet” oleh Zhang et al. (2023) [7]

NowcastNet menggabungkan evolution network berbasis adveksi dan persamaan kontinuitas dengan stochastic generative network untuk mempertahankan struktur presipitasi ekstrem. Penelitian ini relevan karena memadukan kendala evolusi dan pembangkitan stokastik. Ketergantungannya pada data radar resolusi tinggi dan evaluasi hingga tiga jam membatasi penerapan langsung pada lima node ERA5.

Penelitian “Exploring Geometric Deep Learning for Precipitation Nowcasting” oleh Zhao et al. (2023) [28]

Penelitian ini memandang grid radar sebagai graf dan menggunakan temporal Graph Convolutional Network untuk memodelkan hubungan antarlokasi. Relevansinya adalah dasar konseptual adaptasi representasi graf pada data presipitasi. Perbedaan unit node, sumber data radar, dan horizon prediksi menyebabkan hasilnya tidak dapat dipindahkan langsung ke penelitian ini.

Penelitian “RSDF-AM-LSTM: Regional Scale Division Rainfall Forecasting Using Attention and LSTM” oleh Li et al. (2021) [29]

Penelitian ini menggabungkan beberapa LSTM paralel dengan mekanisme attention untuk menangkap dependensi temporal-spasial pada ribuan stasiun meteorologi. Relevansinya terletak pada pemanfaatan attention dan LSTM untuk data multi-lokasi. Baseline Multi-node LSTM + Attention pada penelitian ini hanya merupakan adaptasi gagasan tersebut ke lima node ERA5 dan target `MAIN`, bukan reproduksi penuh RSDF-AM-LSTM.

Penelitian “A Hybrid Approach to Physical and Deep Learning Models for Radar-Based Precipitation Nowcasting” oleh Kim et al. (2025) [20]

Penelitian ini memadukan PySTEPS, RainNet, dan LightGBM untuk menggabungkan keunggulan model adveksi dan deep learning. Relevansinya terletak pada strategi penggabungan beberapa sumber representasi untuk meningkatkan prediksi. Pipeline radar dan model fisik pada penelitian tersebut tidak direproduksi karena penelitian ini menggunakan ERA5 pada lima node.

Penelitian “FuXi-ENS: A machine learning model for efficient and accurate ensemble weather prediction” oleh Zhong et al. (2025) [17]

FuXi-ENS menggunakan variational autoencoder dan loss CRPS untuk menghasilkan prakiraan ensemble global dengan perturbasi yang bergantung pada kondisi atmosfer. Relevansinya adalah representasi ketidakpastian dan evaluasi probabilistik. Perbedaan resolusi, wilayah, interval enam jam, dan horizon hingga 15 hari membatasi perbandingan langsung dengan nowcasting satu jam pada penelitian ini.

Penelitian “Beyond the horizon: A comprehensive analysis of artificial intelligence-based weather forecasting models” oleh Haji-Aghajany et al. (2025) [30]

Penelitian ini merupakan tinjauan komprehensif terhadap model prakiraan cuaca berbasis AI, termasuk isu ketidakpastian, generalisasi, interpretabilitas, dan kendala fisik. Relevansinya adalah pemetaan konseptual posisi diffusion model, retrieval, graf, dan attention dalam perkembangan AI weather forecasting. Paper ini bukan baseline dan tidak menyediakan eksperimen langsung pada lima node ERA5 atau Gunung Gede–Pangrango.

**Tabel Penelitian Terdahulu**

| No. | Judul dan Peneliti | Metode | Temuan Utama | Kedudukan terhadap Penelitian Ini |
| --- | --- | --- | --- | --- |
| 1 | Precipitation Nowcasting with Generative Diffusion Models — Asperti et al. (2025) [25] | Generative Ensemble Diffusion berbasis DDIM dan U-Net | Ensemble diffusion menghasilkan beberapa kemungkinan prediksi presipitasi berbasis ERA5. | Rujukan utama diffusion ensemble; berbeda pada grid, wilayah, dan konfigurasi spasial. |
| 2 | Spatio-temporal graph neural networks to improve precipitation forecasts from numerical models — Yousaf et al. (2025) [26] | WRF-GNN dengan keluaran WRF dan rain gauge | Graf spasio-temporal digunakan untuk memperbaiki prakiraan presipitasi numerik. | Rujukan utama representasi graf; penelitian ini tidak menggunakan WRF atau 22 rain gauge. |
| 3 | Retrieval-Augmented Diffusion Models for Time Series Forecasting — Liu et al. (2024) [27] | RATD dengan embedding retrieval dan Reference-Modulated Attention | Retrieval historis membantu diffusion model pada forecasting deret waktu. | Rujukan integrasi retrieval-diffusion; bukan penelitian cuaca lokal dan tidak memakai STGNN. |
| 4 | Penelitian yang diusulkan | Retrieval-Augmented Diffusion Model dengan STGNN; ERA5/Open-Meteo; lima node; target MAIN | Hasil penelitian belum tersedia. | Model utama penelitian ini. |

## 2.2 Landasan Teori

Landasan teori dalam penelitian ini disusun untuk memberikan dasar ilmiah bagi pengembangan model nowcasting probabilistik kondisi cuaca menggunakan Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network. Bab ini membahas konsep-konsep utama yang menjadi dasar penelitian, mulai dari prinsip nowcasting pada skala waktu per jam, dinamika hujan orografis di pegunungan tropis, hingga cara kerja Retrieval-Augmented Diffusion Model dalam menghasilkan beberapa kemungkinan prediksi cuaca. Selanjutnya, dibahas pula pencarian kondisi cuaca historis yang serupa serta penggunaan representasi graf spasio-temporal melalui lima node, yaitu MAIN, UP, DOWN, LEFT, dan RIGHT. Representasi tersebut digunakan untuk menangkap hubungan kondisi cuaca antar lokasi dan perubahan kondisi atmosfer dari waktu ke waktu, dengan node MAIN sebagai titik target prediksi. Pembahasan kemudian dilanjutkan dengan risiko hipotermia pada aktivitas pendakian di Gunung Gede–Pangrango serta relevansinya terhadap penyampaian informasi cuaca jangka pendek. Dengan landasan teori tersebut, penelitian ini mengevaluasi kemampuan model dalam menghasilkan prediksi cuaca yang mempertimbangkan kemungkinan ketidakpastian, hubungan antar lokasi, dan perubahan kondisi dari waktu ke waktu di wilayah pegunungan tropis.

### 2.2.1 Definisi dan Konsep Nowcasting

Nowcasting merupakan prakiraan cuaca jangka sangat pendek yang memanfaatkan kondisi atmosfer terkini untuk memprediksi perubahan cuaca hingga sekitar enam jam ke depan [6]. Pada meteorologi operasional, prakiraan ini berfokus pada fenomena lokal yang dapat berubah cepat dengan mengandalkan data pengamatan paling baru [6]. Berbeda dengan prakiraan harian atau mingguan, nowcasting menitikberatkan pengamatan pada kondisi mutakhir dan dinamika lokal. Karakteristik ini membuat nowcasting cocok digunakan untuk memantau perubahan cuaca per jam di kawasan pegunungan yang dinamis [6], [7].

Pada penelitian ini, cakupan nowcasting dibatasi pada prediksi kondisi cuaca satu jam ke depan berdasarkan data historis enam jam sebelumnya di titik pengamatan utama, yaitu node MAIN di kawasan Gunung Gede–Pangrango. Data historis tersebut digunakan agar model dapat mengenali pola perubahan atmosfer terkini sebelum menghasilkan estimasi [7]. Target prediksi mencakup tiga variabel: curah hujan, kecepatan angin, dan kelembapan relatif. Ketiga variabel ini dipilih karena langsung memengaruhi tingkat risiko dan paparan fisik bagi para pendaki.

Nowcasting berbeda secara mendasar dari prakiraan cuaca jangka pendek (short-range forecasting) yang mencakup rentang 6–72 jam. Prakiraan jangka pendek umumnya mengandalkan simulasi model numerik berskala luas, sedangkan nowcasting mengutamakan data observasi langsung berskala mikro dan lokal. Tabel 2.2 merangkum perbandingan antara nowcasting dan skala prakiraan cuaca lainnya. Curah hujan digunakan sebagai contoh pada tabel karena memiliki sifat perubahan yang paling dinamis. Meskipun demikian, keluaran model pada penelitian ini tetap menghasilkan tiga variabel target sekaligus.

**Perbandingan Skala Prakiraan Atmosfer.**

| Skala Prakiraan | Horizon | Karakteristik Utama | Contoh Keluaran |
| --- | --- | --- | --- |
| Nowcasting | 0–6 jam | Bergantung kuat pada observasi terkini; menargetkan fenomena lokal yang berubah cepat. | Prediksi curah hujan satu jam ke depan. |
| Short-range forecasting | 6–72 jam | Memadukan observasi lapangan dan model numerik untuk memantau perubahan jangka pendek. | Prakiraan hujan harian dan sistem peringatan dini. |
| Medium-range forecasting | >72 jam s.d. 15 hari | Menitikberatkan dinamika sirkulasi atmosfer skala besar dan prediksi ensambel (ensemble). | Prakiraan cuaca probabilistik regional atau global. |

Batasan dan konsep dasar nowcasting ini menjadi landasan untuk membedah dinamika cuaca per jam, penyusunan fitur temporal, keterbatasan model deterministik, serta penerapan model probabilistik pada subbab berikutnya.

#### 2.2.1.1 Karakteristik Dinamika pada Skala Waktu Per Jam di Wilayah Pegunungan

Horizon prediksi 0–6 jam pada nowcasting berkaitan erat dengan proses pembentukan awan dan hujan lokal yang terjadi cepat [7]. Secara meteorologis, proses ini bekerja pada skala menengah (mesoscale). Pada kawasan pegunungan, tahap awal pembentukan awan dan hujan konvektif (convective initiation) dipicu oleh naiknya massa udara lembap serta perubahan kecil pada parameter kelembapan, suhu, dan kecepatan angin setempat [13].

Di wilayah pegunungan tropis seperti Gunung Gede–Pangrango, proses atmosferik tersebut menjadi lebih kompleks akibat tiga faktor utama: pengangkatan udara oleh lereng gunung (orographic lifting), siklus pemanasan harian permukaan tanah, dan pola gesekan angin lokal dengan kontur lereng. Interaksi ketiga faktor ini menyebabkan kondisi cuaca dapat berbeda jauh antartitik lereng serta berubah secara mendadak dari jam ke jam [11], [14].

Awan konvektif dan presipitasi yang terbentuk dari proses fisik tersebut memiliki masa hidup yang singkat [11], [20]. Oleh karena itu, tugas prediksi satu jam ke depan harus memperhitungkan tiga fenomena sekaligus: kemunculan awan baru, pergerakan sel hujan di atas lereng, dan fluktuasi intensitas curah hujan secara cepat [4], [20].

Perubahan kecil pada data awal atmosfer (seperti penurunan suhu atau pergeseran arah angin) dapat memicu hasil cuaca yang berbeda drastis dalam tempo singkat. Kondisi ini menyebabkan galat prediksi membesar sangat cepat seiring bertambahnya horizon waktu (rapid error growth) [32]. Selain itu, kontur curam Gunung Gede–Pangrango menciptakan variasi elevasi ekstrem dalam jarak horizontal yang pendek [11], [14]. Akibatnya, stasiun pengamatan yang berdekatan sekalipun dapat merekam mikroklimat yang berbeda. Karakteristik spasial dan temporal yang dinamis inilah yang mendasari pentingnya model nowcasting berbasis graf dan deret waktu per jam di sepanjang jalur pendakian [1].

Skala waktu 0–6 jam erat kaitannya dengan dinamika atmosfer pada mesoscale dan convective scale [7]. Pada skala ini, proses konvektif seperti convective initiation sangat sensitif terhadap fluktuasi kecil dalam kelembapan, suhu, dan dinamika angin lokal [13]. Di wilayah orografis tropis seperti Gunung Gede–Pangrango, dinamika ini semakin kompleks karena adanya efek orografis lifting, siklus diurnal konveksi yang kuat, serta interaksi angin lereng yang menyebabkan variabilitas spasial dan temporal yang tinggi [11], [14].

Lifetime sistem konvektif umumnya berada pada orde puluhan menit hingga beberapa jam [5]. Sel konvektif tunggal dapat hidup sekitar 30–60 menit, sedangkan sistem konveksi mesoskal dapat bertahan 3–6 jam atau lebih. Oleh karena itu, prakiraan pada horizon satu jam harus mampu merepresentasikan pembentukan sel baru, pergerakan sel yang ada, serta perubahan intensitas presipitasi secara akurat dan cepat [4], [20]. Rapid error growth akibat sifat nonlinier dan kaotik atmosfer semakin membatasi prediktabilitas deterministik pada skala ini [32].

Di kawasan Gunung Gede–Pangrango, efek topografi memperkuat dinamika mesoskal [11]. Gradien elevasi yang curam menyebabkan perbedaan kondisi meteorologis yang signifikan dalam jarak horizontal yang relatif pendek [14]. Variabilitas spasial yang tinggi ini menjadikan prakiraan per jam sebagai skala paling relevan untuk mitigasi risiko pendakian, karena ancaman cuaca dapat berkembang dan berubah secara cepat sepanjang lintasan pendakian dari hilir menuju puncak [1].

#### 2.2.1.2 Keterkaitan Temporal dalam Prediksi Curah Hujan

Kondisi atmosfer pada waktu terkini memiliki hubungan erat dengan kondisi beberapa saat sebelumnya [11], [20]. Informasi hujan pada satu jam sebelumnya dapat menjadi petunjuk kuat mengenai potensi hujan pada satu jam berikutnya [4], [20].

Untuk memanfaatkan keterkaitan waktu tersebut secara langsung, model menggunakan fitur curah hujan satu jam sebelumnya (lag-1). Secara sederhana, nilai fitur ini pada jam ke- $t$ diambil langsung dari nilai curah hujan aktual pada jam ke- $t-1$ :

$$
PrecipitationLag1_{t}=Precipitation_{t-1} \tag{(2.1)}
$$

dengan:

$PrecipitationLag1_{t}=$ nilai curah hujan satu jam sebelumnya pada waktu $t$

$Precipitation_{t-1}=$ nilai curah hujan pada waktu sebelumnya $\left(t-1\right)$

Persamaan (2.1) mewakili fitur riwayat satu langkah ke belakang. Di samping fitur lag-1, model juga memanfaatkan deret waktu historis sepanjang enam jam $(t-6$ hingga $t-1$ ) untuk memprediksi curah hujan, kecepatan angin, dan kelembapan relatif pada waktu $t$ . Deret enam jam tersebut diproses sebagai rangkaian snapshot graf, lalu dinamika perubahannya dipelajari menggunakan mekanisme temporal attention pada arsitektur Spatio-Temporal Graph Neural Network (dibahas pada Subbab 2.2.6).

#### 2.2.1.3 Transformasi dan Standardisasi Data Curah Hujan

Data curah hujan memiliki sebaran nilai yang sangat timpang. Sebagian besar data bernilai nol karena cuaca dominan cerah atau tidak hujan (zero-inflated), sedangkan saat hujan lebat nilainya dapat melonjak sangat tinggi secara drastis (heavy-tailed). Rentang nilai yang sangat jomplang ini menyulitkan model dalam proses optimasi gradien. Oleh karena itu, data curah hujan perlu dimampatkan skalanya menggunakan fungsi transformasi logaritma natural log1p. Fungsi ini menambahkan angka satu sebelum proses logaritma agar data bernilai nol tetap terdefinisi dan tidak menghasilkan nilai minus tak hingga ( $log(0) = -∞$ ):

$$
y^{'}=log\left(1+y\right) \tag{(2.2)}
$$

dengan:

$y=$ nilai curah hujan asli

$y^{'}=$ nilai curah hujan setelah transformasi

Setelah model selesai melakukan inferensi, nilai prediksi yang masih berada pada skala logaritmik harus dikembalikan ke satuan fisik aslinya (mm/jam). Pembalikan nilai ini dilakukan pada tahap pascapemrosesan (post-processing) menggunakan fungsi inversi eksponensial:

$$
y=exp(y')-1 \tag{(2.3)}
$$

dengan:

$y^{'}=$ nilai keluaran model dalam skala logaritmik

$y=$ nilai curah hujan yang telah kembali ke skala fisik asli

Selain pemampatan skala curah hujan, variabel-variabel cuaca lainnya memiliki rentang satuan yang berbeda-beda, misalnya suhu dalam belasan derajat Celcius, sedangkan tekanan udara mencapai ratusan hektopaskal. Perbedaan skala ini dapat membuat model bias terhadap variabel bernilai besar. Untuk menyetarakan kontribusi seluruh variabel, diterapkan standardisasi Z-score sehingga setiap fitur memiliki rata-rata nol dan simpangan baku satu:

$$
z=\frac{y'- \mu}{\sigma + \epsilon} \tag{(2.4)}
$$

dengan:

$z=$ nilai hasil normalisasi Z-score

$y^{'}=$ nilai curah hujan setelah transformasi

$\mu =$ rata-rata (mean) dari data pelatihan

$\sigma =$ simpangan baku (standard deviation) dari data pelatihan

$\epsilon =$ konstanta kecil untuk menghindari pembagian dengan nol

Nilai rata-rata ( $\mu$ ) dan simpangan baku ( $\sigma$ ) dihitung hanya dari data pelatihan. Pembatasan ini wajib diterapkan untuk mencegah kebocoran informasi (data leakage) dari data validasi maupun data pengujian ke dalam proses pelatihan model. Pada tahap pengujian, keluaran prediksi yang masih berupa nilai terstandardisasi $z$ dikembalikan ke skala aslinya melalui proses denormalisasi:

$$
v=z( \sigma + \epsilon ) + \mu \tag{(2.5)}
$$

Data yang telah melewati proses transformasi dan standardisasi ini siap digunakan sebagai masukan terstruktur bagi model deep learning.

### 2.2.2 Dinamika Hujan Orografis di Pegunungan Tropis

Hujan orografis terbentuk ketika massa udara lembap tertiup menuju lereng pegunungan dan dipaksa bergerak naik. Udara yang naik tersebut mendingin secara perlahan hingga uap air di dalamnya mengembun, membentuk awan, dan akhirnya jatuh sebagai hujan [11], [35]. Pada kawasan tropis, proses ini diperkuat oleh tingkat kelembapan udara yang tinggi serta kondisi atmosfer yang labil. Akibatnya, intensitas hujan dapat sangat berbeda antar-lokasi meskipun jaraknya berdekatan [11], [14], [35].

Di kawasan Gunung Gede–Pangrango, perbedaan ketinggian (elevasi), kemiringan lereng, dan arah angin menghasilkan variasi cuaca lokal yang tajam. Sisi lereng yang berhadapan langsung dengan arah datangnya angin (windward slope) menerima suplai uap air paling melimpah sehingga curah hujannya lebih tinggi. Sebaliknya, sisi lereng yang membelakangi arah angin (leeward slope) menerima udara yang sudah kering, memicu kondisi bayangan hujan (rain shadow) [11], [36]. Selain itu, pemanasan sinar matahari pada siang hari dan dinamika sirkulasi angin lokal turut memengaruhi waktu kemunculan serta intensitas hujan lebat [37].

Dinamika ini menyebabkan cuaca di wilayah pegunungan dapat berubah drastis dalam hitungan menit hingga jam. Karakteristik tersebut menegaskan pentingnya sistem nowcasting berbasis per jam, khususnya untuk memprediksi curah hujan, kecepatan angin, dan kelembapan relatif. Oleh sebab itu, pemodelan cuaca di Gunung Gede–Pangrango wajib memperhitungkan keterkaitan spasial dan temporal dari kondisi atmosfer di sekitarnya.

Presipitasi orografis merupakan fenomena utama yang membentuk pola curah hujan di wilayah pegunungan, terutama di daerah tropis seperti Gunung Gede–Pangrango [11], [35]. Interaksi antara aliran angin lembab dengan topografi menghasilkan angkat paksa (orographic lifting) yang memicu pembentukan awan dan hujan intens [36]. Di kawasan tropis, proses ini sering diperkuat oleh kelembapan tinggi dan ketidakstabilan atmosfer, sehingga menghasilkan distribusi presipitasi yang sangat heterogen dalam skala spasial dan temporal yang kecil [11], [25]. Pemahaman dinamika ini menjadi krusial dalam penelitian nowcasting probabilistik karena presipitasi orografis cenderung berkembang cepat dan sulit diprediksi dengan model deterministik.

Di Gunung Gede–Pangrango, variabilitas elevasi yang tajam dari dataran rendah hingga puncak menciptakan gradien meteorologis yang signifikan [35]. Efek orografis tidak hanya meningkatkan intensitas hujan di lereng angin (windward slope), tetapi juga menghasilkan bayangan hujan (rain shadow) di sisi lereng lindung (leeward) [11], [36]. Fenomena ini menyebabkan perbedaan kondisi cuaca yang ekstrem dalam jarak horizontal relatif pendek, sehingga sangat relevan dengan risiko hipotermia pendaki yang melintasi berbagai elevasi dalam waktu singkat [28].

Dinamika presipitasi orografis di pegunungan tropis juga dipengaruhi oleh siklus diurnal dan interaksi dengan monsun, yang mempercepat convective initiation pada skala per jam [37]. Proses ini menghasilkan presipitasi dengan distribusi heavy-tailed, di mana kejadian ekstrem lebih sering terjadi dibandingkan distribusi normal [6], [7]. Oleh karena itu, model nowcasting yang digunakan dalam penelitian ini harus mampu menangkap ketergantungan spasial-temporal antar elevasi (hilir, lereng, dan puncak) melalui pendekatan Spatio-Temporal Graph Conditioning.

#### 2.2.2.1 Mekanisme Orographic Lifting dan Convective Initiation

Mekanisme utama terbentuknya hujan orografis diawali oleh dorongan fisik lereng yang memaksa udara lembap naik (orographic lifting). Di daerah tropis, udara yang terangkat ini memicu proses awal pembentukan awan hujan konvektif (convective initiation). Keberhasilan proses konveksi ini ditentukan oleh pasokan kelembapan, suhu udara, kestabilan lapisan atmosfer, serta kekuatan angin permukaan [11], [36].

Angin yang bertiup melintasi lereng (cross-slope wind) berfungsi mengalirkan uap air menuju dataran tinggi. Pengaruh angin ini bekerja bersamaan dengan profil topografi lokal. Jika angin bertiup kencang membawa uap air yang jenuh menabrak lereng curam, potensi pembentukan awan tebal akan meningkat secara cepat. Sebaliknya, jika massa udaranya kering, kenaikan angin tersebut tidak serta-merta menghasilkan hujan lebat [36].

Secara logika fisik, besar kecilnya hujan orografis merupakan fungsi gabungan dari seberapa kencang angin membawa uap air menabrak lereng, seberapa basah udara tersebut, serta bagaimana bentuk dan orientasi dinding lerengnya. Ketergantungan faktor-faktor ini dapat diringkas melalui hubungan fungsi konseptual berikut:

$$
P_{orografis}= f\left(U_{cross}, q, H, S, C\right) \tag{(2.6)}
$$

dengan:

$P_{orografis}=$ intensitas presipitasi orografis;

$U_{cross}=$ komponen kecepatan angin yang tegak lurus terhadap lereng;

$q =$ kelembapan udara;

$H =$ karakteristik elevasi/topografi;

$S =$ orientasi dan kemiringan lereng;

$C =$ kondisi konvektif atmosfer.

Persamaan (2.6) merupakan formulasi konseptual untuk merangkum faktor-faktor penentu hujan di wilayah pegunungan, bukan rumus empiris perhitungan numerik langsung. Konsep ini menjadi landasan mengapa model deep learning dalam penelitian ini tidak bisa hanya membaca satu titik stasiun pengamatan saja. Model memerlukan data masukan dari beberapa titik lereng (multi-node) di sekeliling kawasan puncak untuk menangkap interaksi antara angin, kelembapan, dan topografi secara menyeluruh [11], [12], [36]. Variasi hujan menurut lokasi dan waktu dibahas lebih lanjut pada Subbab 2.2.2.2.

#### 2.2.2.2 Variabilitas Spasial dan Temporal Presipitasi Orografis

Hujan orografis di wilayah pegunungan memiliki variasi spasial yang tinggi karena dipengaruhi oleh elevasi, orientasi lereng, arah angin, dan kelembapan udara [14], [35]. Hubungan antara curah hujan dan ketinggian tempat tidak selalu berbanding lurus, melainkan sangat bergantung pada kondisi atmosfer lokal [11], [36]. Oleh karena itu, variasi cuaca di kawasan Gunung Gede–Pangrango tidak dapat disederhanakan menjadi satu pola tunggal, melainkan harus dianalisis langsung berdasarkan data observasi.

Variasi spasial ini tampak jelas pada perbedaan kondisi antara lereng yang menghadap arah datangnya angin (windward) dan lereng yang membelakangi angin (leeward). Lereng yang menghadap angin menerima pasokan uap air yang lebih banyak, sedangkan lereng yang terlindung cenderung lebih kering. Akibatnya, nilai curah hujan, kecepatan angin, dan kelembapan relatif dapat berbeda nyata antar-titik pengamatan meskipun jarak geografisnya relatif dekat [11], [36].

Secara temporal, kejadian hujan umumnya mengikuti pola siklus harian. Namun, waktu puncak hujan dapat bergeser bergantung pada musim, dinamika angin, dan kestabilan atmosfer [37]. Interaksi antara angin lokal dan dinding lereng sering kali mempercepat atau menunda waktu turunnya hujan sehingga kondisi cuaca menjadi lebih sulit diprediksi [36]. Dinamika yang cepat ini mendasari perlunya penggunaan data pengamatan beberapa jam sebelumnya untuk memprediksi kondisi cuaca pada satu jam ke depan.

Selain bervariasi menurut ruang dan waktu, intensitas curah hujan memiliki sebaran statistik yang tidak merata. Sebagian besar waktu pengamatan didominasi oleh kondisi kering atau hujan ringan, sementara kejadian hujan lebat terjadi dalam frekuensi yang sangat kecil. Karakteristik sebaran data seperti ini disebut distribusi berekor berat (heavy-tailed) [6], [7]. Pada situasi tertentu, topografi lereng dapat menahan pergerakan awan hujan sehingga presipitasi berintensitas tinggi terkonsentrasi di area lereng dalam durasi yang lebih lama [34], [35].

Tingginya variasi kondisi cuaca secara spasial dan temporal ini menjadi alasan utama penerapan representasi spasio-temporal pada penelitian ini. Data dari beberapa titik pengamatan lereng digunakan untuk menangkap dinamika atmosfer di sekitar titik utama. Model yang dibangun memanfaatkan Spatio-Temporal Graph Neural Network untuk memodelkan interaksi antar-lokasi dan waktu, serta model diffusion untuk menghasilkan prediksi cuaca probabilistik. Penjelasan mendalam mengenai kedua arsitektur tersebut dibahas pada subbab berikutnya.

### 2.2.3 Risiko Hipotermia pada Pendakian

Risiko hipotermia merupakan salah satu ancaman keselamatan utama dalam aktivitas pendakian, termasuk di kawasan pegunungan tropis seperti Gunung Gede–Pangrango [1]. Hipotermia terjadi ketika suhu inti tubuh merosot di bawah 35°C akibat laju pelepasan panas tubuh lebih cepat daripada kemampuan tubuh menghasilkannya [1].

Di kawasan tropis, hipotermia sering kali dipicu oleh pakaian yang basah kuyup akibat hujan. Air yang membasahi pakaian menghilangkan sifat isolasi kain, sehingga panas tubuh terbuang dengan cepat. Terpaan angin kencang makin mempercepat pelepasan panas tersebut, sedangkan kelembapan udara yang tinggi membuat pakaian sulit kering [1]. Oleh sebab itu, risiko hipotermia tidak semata-mata dipicu oleh suhu udara rendah, melainkan oleh kombinasi curah hujan, kecepatan angin, kelembapan relatif, dan durasi paparan di lapangan.

Kelelahan fisik akibat durasi pendakian yang panjang turut memperparah kerentanan pendaki. Ketika stamina terkuras, metabolisme tubuh melambat dan produksi panas internal menurun. Gejala awal seperti menggigil, badan lemas, dan penurunan koordinasi gerak sering disalahartikan sebagai lelah biasa, sehingga penanganannya kerap terlambat [1].

Kondisi tersebut menjadikan curah hujan, kecepatan angin, dan kelembapan relatif sebagai tiga variabel krusial yang diprediksi dalam penelitian ini. Hubungan antara hasil prediksi cuaca dan strategi mitigasi risiko diuraikan lebih lanjut pada Subbab 2.2.3.3.

#### 2.2.3.1 Mekanisme Hipotermia di Lingkungan Pegunungan Tropis

Hipotermia terjadi saat tubuh mengalami defisit energi termal secara berkelanjutan. Di pegunungan tropis, proses ini tidak membutuhkan suhu beku ekstrem; kombinasi terpaan hujan, pakaian basah, angin kencang, dan durasi paparan yang lama sudah cukup untuk memicu penurunan suhu tubuh secara kritis [1]. Pelepasan panas tubuh ke lingkungan terjadi melalui tiga mekanisme fisik utama:

Konduksi, yaitu perpindahan panas secara langsung dari kulit ke benda yang lebih dingin, terutama pakaian basah yang menempel pada tubuh. Konduktivitas termal air yang jauh lebih tinggi daripada udara membuat panas tubuh terserap puluhan kali lebih cepat saat basah.

Konveksi, yaitu pelepasan panas akibat aliran udara di sekitar tubuh. Terpaan angin yang bertiup kencang secara terus-menerus menyapu lapisan udara hangat tipis di permukaan kulit.

Evaporasi, yaitu pelepasan panas melalui penguapan butiran air dari permukaan pakaian dan kulit yang basah [1].

Di kawasan Gunung Gede–Pangrango, variasi cuaca lokal berlangsung sangat dinamis karena pengaruh topografi, lereng terjal, dan mekanisme hujan orografis [11], [35]. Dinamika ini membuat pendaki dapat terpapar kondisi kering pada awal perjalanan, namun mendadak diterpa hujan lebat dan angin kencang saat melintasi punggungan atau pos pendakian di elevasi yang lebih tinggi.

#### 2.2.3.2 Faktor Meteorologis yang Berkaitan dengan Risiko Hipotermia

Parameter meteorologis utama yang menentukan tingkat keparahan paparan dingin di pegunungan tropis adalah curah hujan, kecepatan angin, dan kelembapan relatif [1]. Rangkuman peran setiap parameter disajikan pada Tabel 2.3.

**Faktor Meteorologis Terkait Paparan Dingin Pendaki**

| Faktor | Dampak Fisik | Variabel Model | Peran Informasi Nowcasting |
| --- | --- | --- | --- |
| Hujan | Membasahi pakaian pendaki dan melipatgandakan kehilangan panas lewat konduksi dan evaporasi. | precipitation | Memberikan estimasi probabilitas dan intensitas hujan satu jam ke depan. |
| Kecepatan angin | Menyapu lapisan udara hangat di sekitar tubuh dan mempercepat pelepasan panas lewat konveksi. | wind_speed | Mengidentifikasi potensi hembusan angin kencang yang memperburuk paparan dingin. |
| Kelembapan relatif | Menghambat pengeringan pakaian basah dan memengaruhi kenyamanan termal pendaki. | relative_humidity | Melengkapi analisis tingkat kebasahan udara di sekitar jalur pendakian. |

### 2.2.4 Model Generatif Probabilistik dengan Diffusion Models

Diffusion model awalnya populer untuk membangkitkan data citra, tetapi prinsip dasarnya dapat diterapkan pada berbagai tipe data lain, termasuk data tabel dan deret waktu (time-series) [39], [48]. Model ini bekerja dengan cara merusak data secara bertahap menggunakan derau (noise), lalu melatih jaringan saraf tiruan untuk memulihkan kembali data asli tersebut. Pada penelitian ini, data yang diproses bukan citra radar, melainkan vektor numerik berdimensi tiga yang memuat variabel curah hujan, kecepatan angin, dan kelembapan relatif pada node MAIN.

Model generatif probabilistik seperti diffusion model menghasilkan sekelompok kemungkinan nilai prediksi di masa depan, bukan hanya satu nilai tunggal (deterministik). Pendekatan ini sangat sesuai untuk persoalan nowcasting cuaca pegunungan yang dinamis dan sulit dipastikan. Dengan menghasilkan banyak sampel luaran (ensemble), model dapat memberikan gambaran tingkat ketidakpastian kondisi cuaca kepada pengguna [6], [25]. Secara umum, diffusion model beroperasi melalui dua tahapan utama:

Forward diffusion, yaitu proses penambahan derau Gaussian ke data asli secara perlahan dan bertahap hingga data berubah menjadi derau acak murni.

Reverse denoising, yaitu proses ketika model belajar memprediksi dan membuang derau tersebut sedikit demi sedikit untuk mengonstruksi kembali data fisik yang bermakna [16], [25].

Pada tahap forward diffusion, data target cuaca pada langkah waktu $t$ dibubuhi derau acak berdasarkan distribusi normal dengan jadwal varians $\beta _{t}$ :

$$
q\left(x_{t}\right|x_{t-1})= N\left(x_{t}; \sqrt \left(1- \beta _{t}\right) x_{t-1}, \beta _{t}I\right) \tag{(2.7)}
$$

dengan:

$x_{t} =$ data target berderau pada langkah difusi $t$

$x_{t-1}=$ data target pada langkah difusi sebelumnya

$\beta _{t}=$ varians noise pada timestep $t$

$I =$ matriks identitas

Jaringan saraf tiruan dilatih bukan untuk langsung menebak nilai cuaca akhir, melainkan untuk memperkirakan seberapa besar derau $ϵ$ yang sebelumnya ditambahkan ke dalam data. Selisih antara derau acak yang disuntikkan dan derau yang ditebak oleh model dihitung menggunakan fungsi kerugian (loss function) berbasis galat kuadrat terkecil (mean squared error):

$$
L_{diff}=E_{x_{0}, ϵ, t} \left[\left|\left|ϵ -ϵ_{\theta \left(x_{t}, t, c\right)}\right|\right|_{2}^{2}\right] \tag{(2.8)}
$$

dengan:

$x_{0} =$ data target asli

$ϵ=$ noise Gaussian yang ditambahkan

$ϵ_{\theta}=$ noise yang diprediksi model dengan parameter theta

$c=$ kondisi tambahan, berupa representasi historis, spasial, dan retrieval

Saat proses inferensi atau pembentukan prediksi berlangsung, alur dibalik (reverse diffusion). Model memulai iterasi dari vektor derau acak murni, kemudian membuang derau secara bertahap menggunakan estimasi $ϵ_ \theta$ . Setelah seluruh iterasi selesai, luaran diubah kembali ke satuan fisik aslinya sehingga menghasilkan sampel prediksi curah hujan, kecepatan angin, dan kelembapan relatif. Proses pengambilan sampel ini diulang sebanyak 30 kali dengan titik awal derau acak yang berbeda guna membentuk satu kelompok prediksi probabilistik (ensemble) [25], [39].

#### 2.2.4.1 Prinsip Kerja Diffusion Model untuk Nowcasting

Dalam perancangan sistem nowcasting, target luaran bersih yang ingin diprediksi pada langkah waktu ke depan didefinisikan sebagai vektor multivariat $y_{0}$ :

$$
y_{0}=[y_{precip}, y_{wind}, y_{humid}]^T \tag{(2.9)}
$$

dengan:

$y_{precip} =$ target laju curah hujan ternormalisasi

$y_{wind}=$ target kecepatan angin ternormalisasi

$y_{humid}=$ target kelembapan relatif ternormalisasi

![Gambar 2.1 Ilustrasi Forward Diffusion dan Reverse Diffusion pada Data Citra](media_sp2/image2.png)

Ilustrasi Forward Diffusion dan Reverse Diffusion pada Data Citra

**Gambar 2.1 memperlihatkan analogi visual proses difusi pada citra. Pada tahap forward diffusion, data perlahan dirusak oleh derau hingga menjadi pola acak. Pada tahap reverse diffusion, model membuang derau tersebut langkah demi langkah untuk merekonstruksi objek. Pada penelitian ini, prinsip yang sama diterapkan pada data vektor tiga variabel cuaca di node MAIN.**

Agar proses pelatihan berjalan cepat tanpa harus menghitung langkah penambahan derau satu per satu dari awal, nilai data berderau pada sembarang langkah difusi $s$ dapat dihitung secara langsung menggunakan formulasi analitis:

$$
x_{t}=\sqrt{\alpha _{s}x_{0}}+\sqrt{1- \alpha _{s}ϵ} \tag{(2.10)}
$$

dengan:

$x_{t} =$ data target berderau pada langkah difusi ke- $s$

$x_{0}=$ data cuaca bersih

$ϵ=$ derau acak dari distribusi normal standar $N\left(0, I\right)$

$\alpha _{s}=i=1s\left(1 - \beta _{i}\right)=$ koefisien skala kumulatif yang menentukan sisa sinyal data asli dan porsi derau yang masuk.

Jaringan denoiser kemudian bertugas menebak nilai $\epsilon$ dengan memanfaatkan seluruh konteks pengondisi yang tersedia:

$$
ϵ=f_{\theta}\left(x_{s},s,h_{t}^{G},R_{t}\right) \tag{(2.11)}
$$

dengan:

$ϵ =$ derau yang diprediksi oleh jaringan

$s=$ nomor langkah difusi aktif

$h_{t}^{G}=$ representasi fitur lingkungan dari graf spasio-temporal

$R_{t}=$ fitur pola cuaca masa lalu dari pencarian analog (retrieval)

Langkah waktu difusi $s$ awalnya berupa bilangan bulat biasa ( $0, 1, 2, \dots , 999$ ). Agar jaringan saraf tiruan dapat membedakan posisi langkah awal dan langkah akhir secara halus, nilai skalar $s$ dipetakan ke dalam deret gelombang sinus dan kosinus pada berbagai frekuensi (sinusoidal positional embedding):

$$
e_{s}=\left[sin\left(\frac{s}{10000^{\frac{2k}{d}}}\right),cos\left(\frac{s}{10000^{\frac{2k}{d}}}\right)\right]_{k=0}^{\frac{d}{2}-1} \tag{(2.12)}
$$

dengan:

$e_{s}=$ vektor posisi langkah difusi berdimensi $d$

$k=$ indeks dimensi fitur

$d=$ dimensi ruang embedding (bernilai 64)

Vektor posisi $e_{s}$ kemudian disalurkan ke modul Time MLP untuk diekspansikan kapasitas fiturnya melalui fungsi aktivasi nonlinier GELU:

$$
h_{s}^{time}=W_{T2}⋅GELU \left(W_{T1}e_{s}+b_{T1}\right)+b_{T2} \tag{(2.13)}
$$

Fungsi aktivasi GELU (Gaussian Error Linear Unit) meloloskan masukan secara proporsional berdasarkan fungsi distribusi kumulatif normal:

$$
GELU\left(x\right)=xϕ\left(x\right) \tag{(2.14)}
$$

dengan $xϕ$ sebagai fungsi distribusi kumulatif dari distribusi normal standar. Setelah jaringan denoiser berhasil dilatih memprediksi derau, proses pengambilan sampel reverse diffusion berulang dapat memetakan distribusi probabilitas cuaca bersyarat secara menyeluruh:

$$
p\left(y_{t+1}^{MAIN}, X_{\le t},h_{t}^{G},R_{t}\right) \tag{(2.15)}
$$

dengan:

$y_{t+1}^{MAIN} =$ distribusi prediksi tiga target cuaca untuk satu jam ke depan

$X_{\le t}=$ riwayat pengamatan cuaca hingga langkah waktu $t$

$h_{t}^{G}=$ ringkasan kondisi spasio-temporal regional

$R_{t}=$ referensi pola historis serupa dari basis data

#### 2.2.4.2 MLP sebagai Denoiser pada Diffusion Model

Penelitian ini menggunakan Multilayer Perceptron (MLP) sebagai arsitektur jaringan denoiser. MLP tersusun atas beberapa lapisan terhubung penuh (fully-connected layers) yang bertugas memetakan hubungan nonlinier antara data target berderau dan seluruh variabel pengondisi atmosfer. Struktur vektor tabular pada target cuaca membuat MLP lebih efisien dan ringan secara komputasi dibandingkan arsitektur konvolusi citra seperti U-Net [39], [48].

![Gambar 2.2 Arsitektur Dasar Multilayer Perceptron](media_sp2/image3.png)

Arsitektur Dasar Multilayer Perceptron

**Gambar 2.2 memperlihatkan struktur dasar MLP yang terdiri atas lapisan masukan, lapisan tersembunyi, dan lapisan keluaran. Kapasitas representasi jaringan diatur melalui variasi lebar lapisan tersembunyi. Pelebaran dimensi (misalnya dari 64 menjadi 128 unit) memberi keleluasaan bagi model untuk mempelajari interaksi fitur yang rumit, sedangkan penyempitan dimensi (dari 128 kembali ke 64 unit) memadatkan representasi sebelum menghasilkan keluaran akhir. Sebagai fungsi aktivasi nonlinier antar-lapisan MLP, digunakan SiLU (Sigmoid Linear Unit). Fungsi ini menghaluskan gradien dengan mengalikan masukan terhadap fungsi sigmoidnya:**

$$
SiLU\left(x\right)=x \sigma \left(x\right) \tag{(2.16)}
$$

dengan:

$\sigma \left(x\right) =\frac{1}{1+e^{-x}}=$ distribusi prediksi tiga target cuaca untuk satu jam ke depan

Untuk mencegah hilangnya informasi sinyal awal pada lapisan-lapisan yang lebih dalam, model menerapkan jalur pintas (skip connection). Berbeda dengan penjumlahan biasa, fitur lapisan tengah $h_{mid}$ dan fitur lapisan perantara $h_{2}$ digabungkan secara berdampingan melalui operasi konkatenasi:

$$
h_{skip}=\left[h_{mid} \| h_{2}\right] \tag{(2.17)}
$$

dengan:

$h_{skip}=$ vektor gabungan hasil konkatenasi

$\| =$ simbol operasi konkatenasi fitur

Karakteristik data cuaca yang didominasi nilai nol (zero-inflated) dan kemunculan hujan lebat yang bernilai ekstrem (heavy-tailed) dapat menyebabkan model malas memprediksi nilai ekstrem. Agar model memberi perhatian lebih pada kejadian ekstrem, galat prediksi derau diberi bobot penalti ekstra bertingkat ( $w_{i}$ ) berdasarkan seberapa jauh nilai data aktual menyimpang dari rata-rata:

$$
w_{i}= \left{w_{extreme}, |y_{0,i}|> \gamma _{extreme}w_{moderate}, & \gamma _{base}<\left|y_{0,i}\right| \le \gamma _{extreme} 1,0, & \left|y_{0,i}\right| \le \gamma _{base}\right) \tag{(2.18)}
$$

dengan:

$y_{0,i} =$ nilai absolut target aktual variabel ke- $i$

$\gamma _{base} dan \gamma _{extreme}=$ batas ambang kondisi sedang dan ekstrem

$w_{moderate} dan w_{extreme}=$ bobot penalti untuk kejadian ekstrem dan sedang

Fungsi kerugian prediksi derau terbobot kemudian dirumuskan sebagai rata-rata galat kuadrat yang telah dikalikan faktor penalti masing-masing variabel:

$$
L_{noise}=\frac{1}{D} i=1Dw_{i}\left(ϵ_{\theta ,i}-ϵ_{i}\right)^{2} \tag{(2.19)}
$$

dengan:

$D =$ jumlah variabel target

$ϵ_{\theta ,i}=$ nilai derau yang diprediksi untuk variabel ke- $i$

$ϵ_{i}=$ nilai derau acak sebenarnya untuk variabel ke- $i$

$w_{i}=$ bobot penalti variabel ke- $i$

Selain memprediksi derau, model dilengkapi cabang pembantu (auxiliary wet head) untuk menebak probabilitas biner apakah hujan terjadi atau tidak. Nilai logit peluang hujan dihitung dari ringkasan vektor cuaca $c_{t}$ :

$$
z_{wet}=w_{w2}^{T}⋅ SiLU \left(W_{w1}c_{t}+b_{w1}\right)+b_{w2} \tag{(2.20)}
$$

dengan:

$z_{wet} =$ nilai logit klasifikasi hujan

$c_{t}=$ vektor kondisi lingkungan atmosfer

$W,b=$ matriks bobot dan vektor bias lapisan klasifikasi

Karena jam kejadian tidak hujan jauh lebih banyak daripada jam hujan, fungsi kerugian klasifikasi biner diberi bobot penyeimbang kelas $w_{pos}$ agar model tidak bias ke kondisi kering:

$$
L_{wet}=-\left[ w_{pos}⋅y_{wet}log\left( \sigma \left(z_{wet}\right)\right)+\left(1 - y_{wet}\right)log\left(1- \sigma \left(z_{wet}\right)\right)\right] \tag{(2.21)}
$$

dengan:

$y_{wet} \in \left{0,1\right}=$ label biner kejadian hujan aktual (bernilai 1 jika presipitasi $\ge 0,1$ mm/jam)

$w_{pos}=$ rasio jumlah sampel kering terhadap sampel basah pada data latih

$\sigma \left(z_{wet}\right)=$ probabilitas terjadinya hujan

Kedua fungsi kerugian tersebut digabungkan menjadi satu fungsi objektif terpadu menggunakan hiperparameter penyeimbang $\lambda _{wet}$ :

$$
L_{total}=L_{noise}+ \lambda _{wet}L_{wet} \tag{(2.22)}
$$

dengan:

$L_{total}=$ fungsi kerugian total pelatihan

$\lambda _{wet}=$ koefisien pengali bobot tugas klasifikasi hujan

Selama proses perambatan balik (backpropagation), lonjakan nilai gradien dapat merusak stabilitas bobot model. Untuk mencegah hal tersebut, norma gradien dipotong (gradient clipping) agar tidak melampaui ambang batas $C_{clip}$ :

$$
g= \nabla _{\theta} L_{total} \tag{(2.23)}
$$

$$
g=g⋅min\left(1,\frac{C_{clip}}{\left‖g\right‖_{2}}\right) \tag{(2.24)}
$$

$$
\theta \leftarrow \theta - \eta ⋅AdamW(g) \tag{(2.25)}
$$

dengan:

$g=$ vektor gradien turunan fungsi kerugian terhadap parameter $\theta$

$\left‖g\right‖_{2}=$ orma Euclidean ( $L_{2}$ ) dari vektor gradien

$C_{clip}=$ batas maksimum panjang vektor gradien

$g=$ gradien aman hasil pemotongan

$\eta =$ laju pembelajaran (learning rate)

$AdamW=$ algoritma optimasi pembaruan bobot dengan peluruhan bobot (weight decay)

#### 2.2.4.3 Peran Diffusion Model pada Arsitektur Penelitian

Model prediksi cuaca numerik konvensional (Numerical Weather Prediction) maupun model regresi deterministik standar kerap kali menghasilkan keluaran yang terlalu halus atau mendekati nilai rata-rata (mean-blurring). Akibatnya, model-model tersebut kesulitan memprediksi kejadian ekstrem mendadak pada rentang waktu pendek [32], [34]. Selain itu, prediksi satu nilai tunggal tidak mampu menyajikan tingkat ketidakpastian atmosfer di lapangan [16], [32].

Penerapan diffusion model pada penelitian ini menjawab keterbatasan tersebut dengan menghasilkan luaran berupa sebaran distribusi probabilitas. Melalui integrasi pencarian analog historis (Retrieval-Augmented Diffusion), model dapat merujuk pola cuaca nyata di masa lalu saat menghadapi kondisi atmosfer serupa. Kombinasi antara modul spasio-temporal STGNN dan mekanisme pembangkitan probabilistik ini memungkinkan sistem nowcasting menghasilkan prakiraan cuaca lokal per jam yang lebih tanggap terhadap potensi hujan lebat dan angin kencang di kawasan pegunungan [6], [25].

### 2.2.5 Retrieval-Based Historical Analogs

Retrieval-Based Historical Analogs merupakan mekanisme pencarian pola cuaca masa lalu yang memiliki kemiripan dinamika dengan kondisi cuaca saat ini. Data analog historis ini dimanfaatkan sebagai informasi pelengkap bagi model, bukan sebagai pengganti proses reverse diffusion. Pada penelitian ini, vektor kondisi cuaca terkini digunakan sebagai kueri (query) untuk mencari kejadian-kejadian serupa di dalam basis data historis masa lampau [27].

Kondisi historis yang serupa memberikan gambaran awal mengenai bagaimana pola atmosfer serupa berkembang pada waktu-waktu sebelumnya. Hasil pencarian (retrieval) tersebut kemudian diproyeksikan dan diinjeksikan sebagai salah satu fitur pengondisi tambahan (conditioning features) saat model diffusion melakukan proses pembuangan derau (denoising) [16], [27], [31].

Penggunaan mekanisme retrieval tidak mengubah alur kerja utama dari diffusion model. Informasi analog historis digabungkan ke dalam vektor kondisi atmosfer $c$ bersama dengan fitur riwayat waktu lokal dan representasi graf spasial. Dengan demikian, diffusion model tetap menjalankan proses penambahan derau, estimasi derau, serta pemulihan data asli secara bertahap sebagaimana dirumuskan pada Persamaan (2.7) dan (2.8). Peran utama modul retrieval adalah menyediakan acuan pola historis yang relevan agar proses estimasi cuaca menjadi lebih terarah [25], [27].

### 2.2.6 Spatio-Temporal Graph Neural Network untuk Pemodelan Cuaca

Kondisi cuaca di kawasan pegunungan memiliki keterkaitan spasial karena kondisinya berbeda antarlokasi lereng, sekaligus memiliki keterkaitan temporal karena kondisinya berubah seiring berjalannya waktu [11], [14]. Spatio-Temporal Graph Neural Network (STGNN) digunakan untuk mempelajari kedua pola hubungan tersebut secara serentak. Arsitektur ini menggabungkan tiga komponen utama: Graph Neural Network (GNN) untuk memetakan keterhubungan antarlokasi, Graph Attention Network (GAT) untuk menimbang seberapa penting informasi dari lokasi tetangga, dan mekanisme pemodelan temporal untuk menangkap dinamika perubahan cuaca dari jam ke jam.

GAT memanfaatkan mekanisme atensi (attention mechanism) untuk memberikan bobot pengaruh yang berbeda pada setiap tetangga. Bobot ini menentukan seberapa besar informasi dari lereng sekitar memengaruhi titik pengamatan utama. Hasil agregasi spasial ini kemudian diproses sepanjang deret waktu historis untuk menghasilkan representasi utuh. Vektor representasi akhir STGNN selanjutnya diinjeksikan sebagai kondisi tambahan (conditioning vector) bagi diffusion model [7], [16].

#### 2.2.6.1 Graph Neural Network untuk Representasi Data Cuaca

Graph Neural Network (GNN) memodelkan jaringan lokasi pengamatan cuaca dalam bentuk graf. Titik lokasi pengamatan direpresentasikan sebagai node, jalur pertukaran informasinya dinyatakan sebagai edge, dan parameter cuaca pada setiap jam disimpan sebagai fitur node. Satu kondisi graf utuh pada satu langkah waktu disebut graph snapshot. GNN memproses data ini dengan mengalirkan pesan fitur antar-node yang terhubung (message passing) [7], [16].

Graph Attention Network (GAT) digunakan untuk memproses graph ini karena kemampuannya memberikan bobot perhatian yang adaptif terhadap node tetangga [30], [32]. Melalui mekanisme attention, model dapat mempelajari seberapa besar pengaruh node UP, DOWN, LEFT, dan RIGHT terhadap evolusi kondisi cuaca di node MAIN pada horizon satu jam ke depan [7], [16]. Struktur graph menggunakan topologi star, node MAIN terhubung dua arah dengan UP, DOWN, LEFT, dan RIGHT, sedangkan node tetangga tidak saling terhubung.

![Gambar 2.3 Topologi Star sebagai representasi graf](media_sp2/image5.png)

Topologi Star sebagai representasi graf

Pada satu langkah waktu $\tau$ , data cuaca seluruh lokasi disusun menjadi sebuah matriks fitur $X_{\tau}$ berukuran jumlah node dikalikan jumlah variabel cuaca:

$$
X_{\tau}=\left[ x_{1, \tau}^{T}x_{2, \tau}^{T} ⋮x_{\left|v\right|, \tau}^{T}\right] \in R^{\left|V\right| \times F} \tag{(2.26)}
$$

dengan:

$V=$ himpunan seluruh titik lokasi pengamatan (node)

$\left|V\right|=$ jumlah node pengamatan

$F=$ jumlah variabel cuaca per node (berjumlah sembilan fitur)

$x_{i, \tau}=$ vektor fitur cuaca node ke- $i$ pada waktu $\tau$

Untuk memprediksi cuaca pada jam ke- $t$ , model mengambil deret waktu dari enam jam sebelumnya ( $t-6$ sampai $t-1$ ). Kumpulan matriks fitur historis ini dituliskan sebagai:

$$
X_{t}=\left{x_{t-6},x_{t-5}, \dots ,x_{t-1}\right} \tag{(2.27)}
$$

Dengan mendefinisikan graf pada setiap langkah waktu sebagai $G_{\tau}=( V,E,X_{\tau},E)$ , urutan snapshot graf historis yang menjadi masukan model dinyatakan sebagai:

$$
G=\left{G_{t-61},G_{t-5}, \dots ,G_{t-1}\right} \tag{(2.28)}
$$

dengan:

$E=$ himpunan sisi berarah (directed edges) penghubung antar-node

$E=$ atribut statis sisi (jarak spasial antar-grid)

$G=$ urutan masukan graf enam jam historis

Setelah hubungan spasial antar-node diproses oleh lapisan konvolusi graf, representasi seluruh node pada waktu $\tau$ dirata-ratakan (global mean pooling) untuk menghasilkan satu vektor ringkasan graf tunggal:

$$
g_{\tau}=\frac{1}{\left|V\right|}i \in V_h_{i, \tau}^{\left(2\right)} \tag{(2.29)}
$$

dengan:

$g_{\tau}=$ vektor ringkasan graf pada jam ke- $\tau$

$h_{i, \tau}^{\left(2\right)}=$ representasi fitur node ke- $i$ setelah melewati lapisan graf kedua

Vektor ringkasan dari keenam jam historis ($L = 6$) kemudian disusun berurutan membentuk matriks deret waktu graf:

$$
G=\left[ g_{t-6}g_{t-5} ⋮g_{t-1}\right] \in R^{L \times d_{g}} \tag{(2.30)}
$$

dengan:

$L=$ panjang jendela waktu historis

$d_{g}=$ dimensi fitur ringkasan graf

#### 2.2.6.2 Graph Attention Network untuk Hubungan Antar-Node

Tidak semua stasiun lereng memberikan pengaruh cuaca yang sama besar terhadap titik utama. Graph Attention Network (GAT) secara otomatis menghitung tingkat kepentingan relatif antar-node melalui koefisien atensi spasial. Nilai kecocokan awal antara node $i$ dan tetangganya $j$ dihitung lewat perkalian matriks bobot yang dilanjutkan dengan fungsi aktivasi LeakyReLU [44]:

$$
e_{ij}=LeakyReLU (a^{T}\left[Wh_{i}\left‖Wh_{j}\right]\right) \tag{(2.31)}
$$

dengan:

$e_{ij}=$ skor kecocokan hubungan antara node $i$ dan node $j$

$W=$ matriks proyeksi linear fitur

$h_{i},h_{j}=$ representasi fitur node $i$ dan node $j$

$a=$ vektor parameter pembelajaran atensi

$\| =$ operasi penggabungan (concatenation)

Fungsi LeakyReLU digunakan agar sinyal gradien tetap mengalir meskipun hasil perkalian bernilai negatif, dengan mempertahankan kemiringan kecil $\lambda$ :

$$
LeakyReLU\left(x\right)=\left{x, x \ge 0 \lambda x, x<0\right) \tag{(2.32)}
$$

Agar skor kecocokan dari semua tetangga dapat diperbandingkan secara adil, nilai $e_{ij}$ dinormalisasi menggunakan fungsi softmax sehingga total bobotnya bernilai satu:

$$
\alpha _{ij} =\frac{exp\left(e_{ij}\right)}{k \in N_{i}∪\left{i\right}exp\left(e_{ik}\right)} \tag{(2.33)}
$$

dengan:

$\alpha _{ij}=$ bobot atensi ternormalisasi dari node $j$ ke node $i$

$N_{i}=$ himpunan node tetangga dari node $i$

Untuk meningkatkan kestabilan pembelajaran, model menggunakan mekanisme banyak kepala atensi (multi-head attention). Sebanyak empat kepala independen ( $K=4$ ) menghitung atensinya masing-masing, lalu hasilnya digabungkan secara berdampingan:

$$
h_{i}^{(1)} =ReLU\left( k=1Kj\inN_{i}∪\left{i\right} \alpha _{ij}^{k}W^{k}h_{j} \right) \tag{(2.34)}
$$

dengan:

$h_{i}^{(1)}=$ representasi node $i$ keluaran lapisan GAT pertama

$K=$ jumlah kepala atensi

$⨁=$ operasi perangkaian (concatenation) vektor antar-kepala

Pada lapisan graf kedua (GAT2), dimensi fitur dirapatkan kembali dari 256 menjadi 64 unit menggunakan satu kepala atensi tunggal:

$$
h_{i, \tau}^{\left(2\right)}=j \in N_{i}∪\left{i\right} \alpha _{ij, \tau}^{\left(2\right)} W_{2} h_{j, \tau}^{\left(1\right)} \in R^{64}
$$

dengan:

$h_{i, \tau}^{\left(2\right)}=$ representasi fitur akhir node $i$ pada jam ke- $\tau$

$W_{2}=$ matriks reduksi dimensi linear berukuran $64 \times 256$

#### 2.2.6.3 Keunggulan Spatio-Temporal Graph dibandingkan Pendekatan Konvensional

Pendekatan sequence-based atau grid-based konvensional sering kali kurang efektif dalam menangkap ketergantungan spasial non-Euclidean yang kompleks di wilayah pegunungan [32], [34]. Model berbasis CNN atau LSTM umumnya mengasumsikan hubungan spasial tetap atau hanya lokal, sehingga sulit memodelkan interaksi multidirectional dari berbagai arah terhadap satu titik utama [30], [31].

Spatio-Temporal Graph Conditioning mampu mengatasi keterbatasan tersebut dengan secara eksplisit memodelkan hubungan antar node melalui message passing dan attention mechanism [7], [16]. Pendekatan ini memungkinkan model mempelajari pola propagasi presipitasi orografis dan pengaruh angin dari berbagai arah secara lebih akurat pada skala per jam [11], [35].

Integrasi graph conditioning dengan diffusion model memungkinkan proses denoising dilakukan secara kondisional terhadap struktur graph lima node, sehingga menghasilkan prediksi ensemble yang lebih konsisten secara spasial dan lebih sensitif terhadap kondisi lokal di sekitar node MAIN [7], [25]. Keunggulan ini sangat penting untuk meningkatkan akurasi prediksi pada titik krusial yang digunakan untuk mitigasi risiko.

Encoding spasial oleh GAT dirumuskan sebagai:

$$
h_{t}=GAT G_{t} \tag{(2.35)}
$$

dengan:

$G_{t}=$ graf pada waktu $t$

$h_{t}=$ representasi spasial hasil encoding

Representasi seluruh waktu diagregasi menggunakan temporal attention:

$$
h_{t}^{G}=TemporalAttention\left(h_{t-L+1}, \dots ,h_{t}\right) \tag{(2.36)}
$$

dengan:

$h_{t}^{G}=$ representasi spasio-temporal akhir pada waktu $t$

$L=$ panjang jendela observasi historis

Pada multi-head attention, keluaran kepala atensi digabungkan melalui concatenation sesuai mekanisme GAT [44]. Penggunaan representasi graph untuk ketergantungan spasio-temporal multi-lokasi juga didukung oleh penelitian STGNN [43]. Temporal attention menggunakan scaled dot-product attention dengan causal mask:

$$
Attention \left(Q,K,V\right)=softmax \left(\frac{QK^{T}}{\sqrt{d_{K}}}+M\right) V \tag{(2.37)}
$$

Mask $M$ mencegah representasi pada suatu timestep mengakses timestep masa depan. Embedding posisi trainable, residual connection, dropout, dan LayerNorm digunakan pada tahap temporal. Representasi pada timestep terakhir dipilih sebagai embedding graph sequence; mekanisme ini bukan penjumlahan berbobot satu skalar untuk setiap jam.

Pada multi-head attention, keluaran kepala atensi digabungkan melalui concatenation [44]:

$$
h_{i}^{'}=\left(​\right‖_{k=1}^{4} j \in N_{i} \alpha _{ij}^{k} W^{k} h_{j} \tag{(2.38)}
$$

Aktivasi SiLU digunakan untuk membentuk transformasi nonlinier yang halus. Dimensi kepala, jumlah kepala, dan dimensi embedding ditetapkan secara eksperimental pada metodologi.

### 2.2.7 Risiko Hipotermia dan Mitigasi Pendakian

Risiko hipotermia merupakan ancaman serius bagi keselamatan pendaki di pegunungan, termasuk di kawasan tropis seperti Gunung Gede–Pangrango [1]. Hipotermia terjadi ketika suhu inti tubuh manusia turun di bawah 35°C akibat kehilangan panas yang melebihi produksi panas tubuh [1], [45]. Di pegunungan tropis, hipotermia sering disebabkan oleh kombinasi hujan deras, angin kencang, dan kelembapan tinggi yang mempercepat kehilangan panas melalui konduksi, konveksi, dan evaporasi, meskipun suhu udara tidak ekstrem seperti di pegunungan tinggi bersalju [1], [22].

Kondisi cuaca di Gunung Gede–Pangrango yang dinamis, terutama presipitasi orografis disertai angin, dapat menyebabkan hipotermia “wet-cold” (hipotermia basah-dingin) dengan cepat [1]. Pakaian yang basah kehilangan kemampuan isolasi hingga 90%, sementara angin memperbesar efek wind chill, sehingga mempercepat penurunan suhu tubuh pendaki meskipun berada di elevasi sedang hingga tinggi [1], [45]. Kejadian ini semakin berbahaya karena pendaki sering berada dalam kondisi kelelahan setelah berjalan jauh, sehingga kemampuan tubuh untuk menghasilkan panas menurun secara signifikan [22].

Nowcasting probabilistik presipitasi, kecepatan angin, dan kelembapan relatif menjadi sangat relevan sebagai sistem peringatan dini. Prediksi satu jam ke depan dengan pendekatan probabilistik memungkinkan pendeteksian dini kombinasi faktor berisiko tinggi sebelum kondisi hipotermia berkembang [6], [7]. Penelitian ini menghubungkan output model Retrieval-Augmented Diffusion dengan Spatio-Temporal Graph Conditioning secara langsung dengan mitigasi risiko keselamatan pendaki.

### 2.2.8 Visualisasi Web Berbasis Vue.js dan FastAPI

Visualisasi berbasis web berperan sebagai lapisan penyajian yang menghubungkan keluaran model nowcasting dengan pengguna akhir. Lapisan ini memungkinkan informasi berupa prediksi titik, distribusi ensemble, probabilitas kejadian hujan, dan indikator risiko disajikan secara terstruktur serta mudah diinterpretasikan tanpa mengubah proses pelatihan maupun inferensi model. Dalam pengembangan dashboard, penggunaan framework front-end mendukung konsistensi antarmuka, pemisahan komponen tampilan, dan pembaruan data secara responsif [47].

Vue.js digunakan sebagai landasan front-end untuk merancang dashboard yang memuat kartu indikator kondisi node MAIN, grafik deret waktu, visualisasi probabilitas, dan tabel ringkasan prediksi. Pendekatan berbasis komponen memungkinkan setiap elemen antarmuka dikembangkan secara modular, sehingga perubahan pada satu komponen tidak memengaruhi keseluruhan halaman. Vue memiliki kinerja rendering yang kompetitif, struktur pengembangan sederhana, serta efisiensi penggunaan sumber daya yang memadai untuk aplikasi web responsif. Karakteristik tersebut relevan bagi penyajian hasil nowcasting yang perlu diperbarui secara periodik dan dipahami oleh pengguna nonteknis[47].

FastAPI digunakan sebagai lapisan backend untuk menyediakan antarmuka pemrograman aplikasi yang menyalurkan artefak hasil inferensi kepada dashboard. Framework ini mendukung validasi data berbasis Python type hints, dokumentasi API otomatis, dan pemrosesan asinkron, sehingga sesuai untuk penyediaan layanan data yang terstruktur [48]. Integrasi FastAPI sebagai backend Python dan Vue sebagai antarmuka memungkinkan pemisahan yang jelas antara modul algoritme, layanan data, dan visualisasi hasil pada sistem model atmosfer. Dalam arah pengembangan penelitian ini, FastAPI dapat menyediakan endpoint untuk hasil prediksi probabilistik, sedangkan Vue.js menyajikannya sebagai grafik dan indikator risiko. Implementasi dashboard tidak termasuk ruang lingkup evaluasi model; subbab ini menjadi landasan konseptual bagi pengembangan sistem penyampaian informasi pada tahap lanjutan [48].

## 2.3 Analisis Gap Penelitian

Penelitian nowcasting cuaca telah banyak mengembangkan model generatif probabilistik, seperti diffusion models, untuk menghasilkan variasi skenario prediksi dan memetakan tingkat ketidakpastian atmosfer [6], [25], [56]. Meskipun berpotensi tinggi, kualitas luaran model generatif sangat bergantung pada karakteristik data, metode evaluasi, serta kemampuannya dalam memprediksi kejadian cuaca ekstrem [7], [16]. Penerapan model generatif secara mandiri belum memadai untuk memodelkan interaksi cuaca antarlokasi lereng dan dinamika perubahannya dari waktu ke waktu di wilayah pegunungan.

Gap penelitian berikutnya terletak pada integrasi informasi spasial, temporal, dan riwayat historis dalam satu arsitektur terpadu. Pendekatan konvensional berbasis grid reguler maupun deret waktu murni belum mampu memetakan keterkaitan antartitik pengamatan secara eksplisit, terutama pada kawasan dengan variasi elevasi yang curam dan perubahan mikroklimat yang cepat [14], [32]. Di sisi lain, pemanfaatan pola cuaca masa lampau yang serupa (retrieval-based historical analogs) berpeluang memandu proses estimasi model. Namun, integrasi analog historis ke dalam proses denoising pada diffusion model untuk nowcasting berbasis data reanalisis per jam masih sangat terbatas [27], [30]. Sepanjang penelusuran literatur, belum ditemukan penelitian yang memadukan model generatif probabilistik, pencarian analog historis, dan representasi graf spasio-temporal secara simultan pada data ERA5 multi-titik di kawasan Gunung Gede–Pangrango.

Penelitian ini mengisi gap tersebut dengan mengusulkan arsitektur Retrieval-Augmented Diffusion Model yang terintegrasi dengan Spatio-Temporal Graph Neural Network (STGNN). Model ini memadukan referensi analog historis dengan pemodelan interaksi cuaca antarlereng dan dinamika waktu, lalu menghasilkan luaran probabilistik tiga parameter cuaca (curah hujan, kecepatan angin, dan kelembapan relatif) pada node MAIN. Kinerja model dievaluasi secara komprehensif melalui metrik akurasi prediksi titik, ketajaman sebaran distribusi probabilistik, serta keandalan deteksi kejadian hujan. Model ini tidak menghitung indeks medis hipotermia secara langsung, melainkan menyajikan data prakiraan meteorologis ekstrem sebagai sistem pendukung keputusan untuk keselamatan aktivitas pendakian [46].

# BAB III
# METODE PENELITIAN

## 3.1 Tahapan Penelitian

Tahapan penelitian disusun secara berurutan untuk mengembangkan dan mengevaluasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Conditioning dalam nowcasting probabilistik presipitasi satu jam ke depan. Tahapan tersebut mencakup studi literatur, pengambilan data, preprocessing, pembagian dataset temporal, pembentukan fitur dan representasi graf, perancangan arsitektur model, pelatihan, inferensi, evaluasi, serta skenario eksperimen. Alur keseluruhan tahapan penelitian ditunjukkan pada Gambar 3.1.

![Gambar 3.1 Alur Tahapan Penelitian](media_sp2/image6.jpeg)

Alur Tahapan Penelitian

Tahap awal penelitian adalah studi literatur untuk mengidentifikasi, menganalisis, dan mensintesis kajian terdahulu yang relevan dengan pengembangan model nowcasting probabilistik presipitasi berbasis deep learning. Fokus kajian mencakup: (1) teknik nowcasting presipitasi pada skala per-jam, (2) penerapan model generatif probabilistik khususnya diffusion models, serta (3) pendekatan spatio-temporal graph dan retrieval-augmented mechanism dalam pemodelan cuaca.

Tahap selanjutnya adalah Pengambilan Data, yaitu pengumpulan data meteorologi per jam dari Open-Meteo Archive API berbasis ERA5 reanalysis pada lima titik observasi spasial (MAIN, UP, DOWN, LEFT, RIGHT). Tahap ini menjadi fondasi utama karena kualitas dan kelengkapan data sangat menentukan keberhasilan tahapan berikutnya.

Selanjutnya dilakukan Preprocessing Data yang meliputi validasi struktur, pembersihan, pembentukan fitur lag, transformasi logaritmik pada presipitasi, serta normalisasi data menggunakan Standard Scaling untuk memastikan data siap digunakan dalam pelatihan model.

Kemudian dilakukan Pembagian Dataset secara temporal (time-based split) untuk memisahkan data menjadi training, validation, dan testing set. Pembagian ini penting untuk menjaga aspek temporal order dan mencegah data leakage pada evaluasi model.

Tahap Pembentukan Fitur dan Graf melibatkan rekayasa fitur serta pembuatan struktur graph spatio-temporal dengan lima node di mana node MAIN menjadi target prediksi utama. Graf ini merepresentasikan ketergantungan spasial multidirectional antar node.

Selanjutnya adalah Perancangan Arsitektur Model yang mendefinisikan keseluruhan komponen Retrieval-Augmented Diffusion Model, termasuk mekanisme retrieval historical analogs dan Spatio-Temporal Graph Conditioning menggunakan Graph Attention Network (GAT).

Proses Proses Pelatihan Model dilakukan dengan menggunakan weighted denoising loss untuk meningkatkan sensitivitas model terhadap kejadian presipitasi ekstrem serta teknik conditional diffusion berdasarkan observasi historis dan struktur graph.

Tahap Evaluasi Model kemudian dilakukan menggunakan metrik deterministik (MAE, RMSE), metrik probabilistik (CRPS), serta metrik berbasis threshold (POD, FAR, CSI) untuk menilai performa model secara komprehensif.

Tahap terakhir, merancang web visualisasi hasil prediksi dirancang sebagai sarana penyampaian informasi nowcasting yang dapat mendukung interpretasi keluaran model oleh pengguna.

Dengan alur tahapan yang terstruktur seperti yang ditunjukkan pada Gambar 3.1, penelitian ini memastikan bahwa setiap komponen model dikembangkan secara bertahap dan dapat dievaluasi secara ilmiah.

## 3.2 Studi Literatur

Studi literatur merupakan tahap awal untuk membangun dasar metodologis penelitian dan menentukan komponen model yang sesuai dengan tujuan nowcasting probabilistik presipitasi. Kajian dilakukan secara terarah terhadap penelitian terdahulu, teori nowcasting, dinamika presipitasi orografis, model generatif berbasis diffusion, retrieval-based historical analogs, serta representasi graph spasio-temporal.

Proses studi literatur meliputi identifikasi sumber yang relevan, seleksi berdasarkan kesesuaian topik dan tahun publikasi, pembacaan metode serta hasil penelitian, kemudian sintesis kelebihan, keterbatasan, dan peluang pengembangan. Literatur tentang diffusion digunakan untuk merumuskan mekanisme pembangkitan ensemble dan denoising. Literatur tentang GNN, GAT, dan temporal attention digunakan untuk merancang representasi hubungan antar-node dan urutan snapshot historis. Literatur retrieval digunakan untuk merumuskan penggunaan analog historis sebagai kondisi tambahan pada diffusion model.

Hasil studi literatur digunakan untuk menetapkan: (1) penggunaan data ERA5 pada lima node spasial, (2) node MAIN sebagai target prediksi, (3) jendela historis enam snapshot, (4) integrasi STGNN, retrieval, dan conditional diffusion, serta (5) metrik evaluasi deterministik, probabilistik, dan berbasis kejadian. Selain itu, studi literatur digunakan untuk menentukan model pembanding yang diuji pada skenario eksperimen.

Studi literatur tidak digunakan untuk mengklaim bahwa model penelitian ini pasti lebih baik daripada penelitian terdahulu. Klaim kinerja ditentukan berdasarkan hasil eksperimen pada dataset dan protokol evaluasi penelitian ini. Dengan demikian, keluaran tahap studi literatur berupa kerangka teori, spesifikasi metodologis, daftar referensi, dan rumusan celah penelitian yang menjadi dasar tahap pengambilan data.

## 3.3 Pengambilan Data

Pengambilan data merupakan tahap awal yang sangat krusial dalam penelitian ini karena menjadi fondasi bagi seluruh proses pengembangan model. Penelitian ini menggunakan data sekunder berupa deret waktu multivariat dengan referensi spasial tetap yang diperoleh melalui layanan Open-Meteo Archive API berbasis reanalisis ERA5. Pemilihan ERA5 didasarkan pada konsistensi historis jangka panjang, kelengkapan variabel meteorologis, serta resolusi spasial dan temporal yang seragam. ERA5 adalah reanalysis historis, bukan sumber observasi real-time; karena itu penggunaannya dibatasi untuk pelatihan dan evaluasi metodologis, bukan operasi nowcasting langsung. Proses pengambilan data melalui Open-Meteo Archive API dapat dilihat pada Gambar 3.2 berikut.

![Gambar 3.2 Alur Pengambilan Data Reanalisis ERA5 melalui Open-Meteo API](media_sp2/image7.jpeg)

Alur Pengambilan Data Reanalisis ERA5 melalui Open-Meteo API

**Gambar 3.2 mengilustrasikan alur pengambilan data yang dimulai dari penentuan Koordinat Node, permintaan data melalui Open-Meteo API, perolehan ERA5 Dataset, dilanjutkan dengan Validasi Data Grid, Penggabungan Data Semua Node, hingga menghasilkan Dataset Penelitian yang siap digunakan. Diagram ini menekankan mekanisme validasi grid center untuk mencegah duplikasi spasial serta konsistensi penggabungan data dari kelima node.**

### 3.3.1 Penentuan Node dan Koordinat

Koordinat node ditetapkan sebelum permintaan data dikirimkan ke Open-Meteo API. Lima node digunakan, yaitu MAIN sebagai node target serta UP, DOWN, LEFT, dan RIGHT sebagai node konteks. Koordinat setiap node dirangkum pada Tabel 3.1.

**Koordinat Node**

| Node | Latitude | Longitude |
| --- | --- | --- |
| MAIN | -6.75 | 107.00 |
| UP | -6.50 | 107.00 |
| DOWN | -7.00 | 107.00 |
| LEFT | -6.75 | 106.75 |
| RIGHT | -6.75 | 107.25 |

### 3.3.2 Open-Meteo API

Pengambilan data dilakukan melalui endpoint (https://archive-api.open-meteo.com/v1/archive) menggunakan protokol HTTPS dengan metode HTTP GET. Endpoint tersebut dipilih karena menyediakan data historis per jam dari model reanalisis ERA5. Permintaan dikirim menggunakan koordinat lima node, periode 1 Januari 2005 sampai 31 Desember 2025, zona waktu Asia/Jakarta, model ERA5, dan daftar variabel meteorologis yang diperlukan.

Parameter latitude dan longitude berisi koordinat lima node, sedangkan start_date dan end_date menentukan rentang data. Parameter hourly meminta field sumber precipitation, temperature_2m, relative_humidity_2m, dew_point_2m, surface_pressure, wind_speed_10m, wind_direction_10m, dan cloud_cover. Parameter timezone=Asia/Jakarta mengatur acuan waktu respons API, sedangkan data kemudian dikonversi dan disimpan dalam UTC. Parameter models=era5 menetapkan sumber model reanalisis yang digunakan. Nama field tersebut merupakan nama mentah sebelum harmonisasi variabel karena berasal langsung dari API.

Respons API berisi data per jam untuk setiap koordinat. Program memeriksa jumlah respons agar sama dengan jumlah node, kemudian membaca waktu, nilai variabel, koordinat grid aktual, dan elevasi. Permintaan menggunakan sesi dengan cache dan mekanisme percobaan ulang agar kegagalan jaringan sementara tidak langsung menghentikan proses.

### 3.3.3 ERA5 Dataset

Data yang diterima dari Open-Meteo Archive API bersumber dari reanalisis ERA5 milik ECMWF (European Centre for Medium-Range Weather Forecasts). Secara keseluruhan, endpoint reanalisis ERA5 pada Open-Meteo menyediakan puluhan variabel permukaan (surface variables) yang mencakup parameter suhu, kelembapan, tekanan udara, presipitasi, radiasi matahari, tutupan awan, dan vektor angin.

Untuk kebutuhan penelitian nowcasting dan mitigasi risiko cuaca buruk di kawasan pegunungan, penelitian ini secara selektif meminta delapan variabel cuaca dinamis melalui parameter hourly, serta memuat metadata lokasi, zona waktu, elevasi grid model, dan deret waktu hourly.time. Struktur data mentah yang diterima untuk satu koordinat dirangkum pada Tabel 3.2.

**Contoh Struktur Data Respons Mentah ERA5 pada Satu Koordinat**

| Bagian respons | Field Open-Meteo | Contoh data | Keterangan |
| --- | --- | --- | --- |
| Metadata lokasi | latitude | -6.75 | Lintang pusat grid |
| Metadata lokasi | longitude | 107.00 | Bujur pusat grid |
| Metadata waktu | utc_offset_seconds | 25200 | Selisih detik terhadap UTC |
| Metadata waktu | timezone | Asia/Jakarta | Zona waktu respons |
| Metadata model | elevation | 1529 m | Ketinggian permukaan model |
| Deret waktu | hourly.time | 2004-12-31T17:00 | Timestamp ISO 8601 |
| Deret waktu | hourly.precipitation | 0.000 mm | Curah hujan 1 jam |
| Deret waktu | hourly.temperature_2m | 15.195 °C | Suhu udara 2 meter |
| Deret waktu | hourly.relative_humidity_2m | 95.591 % | Kelembapan relatif 2 meter |
| Deret waktu | hourly.dew_point_2m | 12.100 °C | Titik embun 2 meter |
| Deret waktu | hourly.surface_pressure | 850.000 hPa | Tekanan udara permukaan |
| Deret waktu | hourly.wind_speed_10m | 5.589 m/s | Kecepatan angin 10 meter |
| Deret waktu | hourly.wind_direction_10m | 180° | Arah angin 10 meter |
| Deret waktu | hourly.cloud_cover | 73 % | Tutupan awan total |
| Satuan | hourly_units | Satuan masing-masing field | Metadata satuan variabel |

Elevasi yang digunakan sebagai fitur model diperoleh melalui Open-Meteo Elevation API secara terpisah untuk memastikan ketinggian aktual setiap koordinat terpetakan presisi, lalu dipasangkan kembali ke masing-masing node. Dalam arsitektur model, elevation berperan sebagai fitur statis lokasi (topografi), bukan fitur dinamis cuaca dan bukan target prediksi.

Respons mentah dari kelima koordinat tersebut mencakup periode 1 Januari 2005 hingga 31 Desember 2025 (21 tahun atau 184.080 timestamp per koordinat), sehingga menghasilkan total $184.080 \times 5=920.400$ baris data observasi koordinat waktu sebelum masuk ke tahap penggabungan node.

### 3.3.4 Validasi Data Grid

Validasi dilakukan setelah respons API diterima dan sebelum koordinat diberi label node. Tahap ini memeriksa pusat grid aktual (grid center) dan memastikan bahwa dua koordinat tidak memperoleh grid ERA5 yang sama. Benturan grid (grid collision) berarti dua koordinat berbeda dipetakan ke grid yang sama, sehingga keduanya tidak lagi memberikan informasi spasial yang berbeda.

Pemeriksaan koordinat secara ketat terhadap koordinat yang diminta diterapkan pada koordinat MAIN. Empat koordinat lainnya diperiksa melalui identitas grid dan pemeriksaan benturan grid. Setelah seluruh koordinat lolos pemeriksaan, program memasangkan koordinat dengan label node berdasarkan urutan yang telah ditentukan, yaitu [MAIN, UP, DOWN, LEFT, RIGHT]. Dengan demikian, data respons API berubah dari kumpulan respons berdasarkan urutan koordinat menjadi dataset dengan lima node yang memiliki identitas lokasi konsisten.

Kelengkapan data kemudian diperiksa pada setiap timestamp. Setiap timestamp harus memiliki tepat lima node dengan urutan yang sama. Sebagai contoh, respons lima koordinat tanpa benturan grid (grid collision) dapat dipetakan menjadi MAIN, UP, DOWN, LEFT, dan RIGHT. Jika satu koordinat tidak memiliki respons, atau dua koordinat memiliki grid yang sama, proses dihentikan. Validasi ini tidak mengubah nilai cuaca; tahap ini hanya memastikan koordinat benar, label node konsisten, dan struktur lima node siap digabungkan.

### 3.3.5 Penggabungan Semua Node

Setelah validasi berhasil dan label lima node terbentuk, data dari kelima node digabungkan berdasarkan timestamp UTC. Penggabungan dilakukan dengan mempertahankan ID node, peran node, koordinat grid, elevasi, dan seluruh variabel cuaca. Data kemudian diurutkan menggunakan urutan node [MAIN, UP, DOWN, LEFT, RIGHT] agar setiap timestamp selalu memiliki susunan baris yang sama.

Pada tahap penggabungan, tidak ada nilai cuaca yang dirata-ratakan atau dijumlahkan. Setiap node tetap menjadi satu baris tersendiri. Dengan demikian, informasi spasial tidak hilang ketika data disusun menjadi masukan graf. Fitur historis dari kelima node digunakan saat sampel pelatihan dan evaluasi dibentuk. Target prediksi hanya diambil dari node MAIN, sedangkan nilai target pada node konteks tidak digunakan sebagai keluaran supervisi maupun dalam perhitungan loss model. Contoh hasil penggabungan lima node pada satu timestamp ditunjukkan pada Tabel 3.3. Visualisasi posisi node hasil pemetaan ditunjukkan pada Gambar 3.3.

**Contoh Data Hasil Penggabungan Lima Node**

| Timestamp UTC | Node | precipitation | temperature_2m | relative_humidity_2m | ⋯ | cloud_cover | elevation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2004-12-31 17:00 | MAIN | 0.000 | 15.195 | 95.591 | ⋯ | 73 | 1529 |
| 2004-12-31 17:00 | UP | 0.000 | 23.688 | 94.708 | ⋯ | 97 | 162 |
| 2004-12-31 17:00 | DOWN | 0.000 | 25.344 | 96.776 | ⋯ | 74 | 0 |
| 2004-12-31 17:00 | LEFT | 0.000 | 19.629 | 97.240 | ⋯ | 99 | 823 |
| 2004-12-31 17:00 | RIGHT | 0.000 | 23.570 | 96.149 | ⋯ | 67 | 288 |

**Tabel 3.3 menunjukkan bahwa satu timestamp menghasilkan lima baris, yaitu satu baris untuk setiap node. Nilai tidak dirata-ratakan; setiap baris tetap mewakili kondisi node masing-masing. Pada tahap berikutnya, lima baris tersebut dibaca sebagai satu snapshot graf dengan lima node. Target pelatihan tetap hanya diambil dari MAIN, sedangkan empat node lain menyediakan konteks spasial.**

### 3.3.6 Dataset Penelitian

Dataset penelitian merupakan keluaran akhir alur pengambilan data dan menjadi masukan untuk preprocessing pada Subbab 3.4. Dataset memiliki satu baris untuk setiap kombinasi timestamp dan node. Dataset lengkap terdiri atas 184.080 timestamp, lima node, dan 920.400 baris data. Dataset ini memuat delapan variabel cuaca dinamis dari API, satu fitur statis elevation, serta metadata dan fitur turunan yang diperlukan oleh pipeline. Ringkasannya ditunjukkan pada Tabel 3.4.

**Karakteristik Dataset Penelitian**

| Karakteristik | Nilai |
| --- | --- |
| Sumber data | Open-Meteo Archive API berbasis ERA5 |
| Resolusi temporal | 1 jam |
| Periode data | 2005–2025 |
| Timestamp penyimpanan | UTC |
| Jumlah node | 5 |
| Jumlah timestamp | 184.080 |
| Total baris | 920.400 |
| Target | Curah hujan, kecepatan angin, kelembapan relatif pada MAIN |

**Tabel 3.4 merangkum ukuran dan cakupan dataset setelah lima node digabungkan. Resolusi satu jam menunjukkan jarak waktu antarobservasi, lima node menunjukkan jumlah lokasi pada setiap timestamp, dan total baris merupakan hasil perkalian jumlah timestamp dengan jumlah node. Perhitungannya adalah:**

$$
Total baris=184.080 \times 5=920.400
$$

Artinya, satu timestamp menghasilkan lima baris data, sedangkan 184.080 timestamp menghasilkan 920.400 baris. Target hanya berasal dari MAIN, sedangkan empat node lain dipakai sebagai konteks spasial.

## 3.4 Preprocessing Data

Preprocessing mengubah dataset penelitian menjadi data yang siap dibagi secara kronologis. Tahap ini dimulai dari dataset lima node yang telah diperoleh pada Subbab 3.2. Urutan tahap mengikuti Gambar 3.4.

![Gambar 3.3 Flowchart Preprocessing Data](media_sp2/image8.jpeg)

Flowchart Preprocessing Data

**Gambar 3.3 menunjukan alur preprocessing data secara keseluruhan, mulai dari dataset penelitian, harmonisasi nama variabel, pengurutan kronologis, pembentukan fitur lag temporal, dan transformasi curah hujan.**

### 3.4.1 Pemeriksaan Integritas Data Awal

Dataset penelitian pada awal preprocessing merupakan data hasil ekstraksi lima node dari Subbab 3.2.6. Sebelum dilakukan harmonisasi nama dan transformasi, catatan masih menggunakan nama field asli dari API Open-Meteo sebagaimana dirangkum pada contoh data gabungan pada Tabel 3.3

Sebelum diproses, setiap catatan harus memiliki timestamp UTC, ID node, variabel meteorologis, elevasi, dan curah hujan. Urutan node tetap digunakan, yaitu [MAIN, UP, DOWN, LEFT, RIGHT]. Dataset yang tidak memiliki kolom wajib atau tidak memiliki nilai yang dapat digunakan pada kolom fitur yang diperlukan tidak diteruskan ke tahap berikutnya. Sebagai contoh, catatan yang memiliki timestamp, ID node, sembilan fitur, elevasi, dan curah hujan dapat diteruskan, sedangkan catatan tanpa timestamp atau ID node dihentikan pada tahap pemeriksaan. Dengan demikian, keluaran Subbab ini adalah dataset penelitian dengan struktur yang siap diharmonisasi namanya.

### 3.4.2 Harmonisasi Nama Variabel

Harmonisasi nama variabel dilakukan agar nama field lebih mudah dibaca dan konsisten dengan penulisan ilmiah, tetapi tetap menggunakan format snake_case. Harmonisasi ini menghilangkan keterangan ketinggian pengukuran seperti _2m dan _10m pada nama untuk analisis, namun untuk satuan dan makna variabel tidak berubah. Tabel 3.5 menampilkan field sumber/API dan nama variabel yang digunakan dalam analisis setelah tahap ini.

| No. | Nama field sumber/API | Nama variabel untuk analisis | Peran variabel |
| --- | --- | --- | --- |
| 1 | precipitation | precipitation | Target curah hujan |
| 2 | temperature_2m | temperature | Fitur dinamis suhu udara |
| 3 | relative_humidity_2m | relative_humidity | Fitur dinamis dan target kelembapan relatif |
| 4 | dew_point_2m | dewpoint | Fitur dinamis titik embun |
| 5 | surface_pressure | surface_pressure | Fitur dinamis tekanan permukaan |
| 6 | wind_speed_10m | wind_speed | Fitur dinamis dan target kecepatan angin |
| 7 | wind_direction_10m | wind_direction | Fitur dinamis arah angin |
| 8 | cloud_cover | cloud_cover | Fitur dinamis tutupan awan |

### 3.4.3 Pegurutan Kronologis

Setelah struktur data diperiksa, seluruh catatan diurutkan berdasarkan timestamp UTC secara menaik. Pada timestamp yang sama, urutan node dipertahankan sebagai [MAIN, UP, DOWN, LEFT, RIGHT]. Pengurutan ini dilakukan sebelum pembentukan fitur temporal agar nilai satu jam sebelumnya benar-benar berasal dari timestamp sebelumnya, bukan dari baris yang hanya berdekatan secara posisi.

Sebagai contoh, catatan pada pukul 17.00 UTC ditempatkan sebelum catatan pada pukul 18.00 UTC untuk node yang sama. Jika urutan waktu tidak benar, fitur curah hujan sebelumnya dapat mengambil nilai dari waktu yang lebih baru dan menyebabkan data leakage. Keluaran tahap ini adalah dataset yang tersusun secara kronologis dan siap digunakan untuk pembentukan lag.

Contoh perubahan urutan data sebelum dan sesudah proses pengurutan kronologis disajikan pada Tabel 3.5 dan Tabel 3.6. Contoh menampilkan node MAIN dan UP pada dataset penelitian.

**Contoh Data Sebelum Pengurutan Kronologis**

| Urutan | Timestamp UTC | Node | Curah hujan (precipitation) |
| --- | --- | --- | --- |
| 1 | 2025-01-01 18:00 | UP | 0,400 mm |
| 2 | 2025-01-01 17:00 | MAIN | 0,000 mm |
| 3 | 2025-01-01 18:00 | MAIN | 0,500 mm |
| 4 | 2025-01-01 17:00 | UP | 0,200 mm |

**Contoh Data Sebelum Pengurutan Kronologis**

| Urutan | Timestamp UTC | Node | Curah hujan (precipitation) |
| --- | --- | --- | --- |
| 1 | 2025-01-01 17:00 | MAIN | 0,000 mm |
| 2 | 2025-01-01 17:00 | UP | 0,200 mm |
| 3 | 2025-01-01 18:00 | MAIN | 0,500 mm |
| 4 | 2025-01-01 18:00 | UP | 0,400 mm |

Pada Tabel 3.5 (sebelum pengurutan), timestamp dan node masih bercampur. Setelah pengurutan pada Tabel 3.6, timestamp tersusun menaik dan node pada timestamp yang sama mengikuti urutan kanonik. Nilai cuaca tidak berubah; hanya posisi baris yang diperbaiki. Jika data divisualisasikan sebagai grafik deret waktu, sumbu horizontal menunjukkan timestamp UTC dan sumbu vertikal menunjukkan nilai precipitation; titik atau garis akan dibaca dari waktu paling awal ke waktu paling akhir. Contoh ini menjadi dasar pembentukan fitur precipitation_lag1 pada subbab berikutnya.

### 3.4.4 Fitur Lag Temporal

Fitur lag temporal menyimpan curah hujan satu jam sebelumnya sebagai salah satu fitur masukan. Untuk setiap node jika curah hujan pada $t-1$ sebesar 2 mm, maka precipitation_lag1 pada $t$ bernilai 2 mm. Pada timestamp pertama setiap node, nilai lag diisi 0,0 karena belum tersedia catatan satu jam sebelumnya. Fitur lag merupakan informasi masa lalu dan berbeda dari target curah hujan pada waktu prediksi. Dalam implementasi, fitur ini dibentuk saat penyiapan dataset setelah data diurutkan; pada naskah, tahap tersebut dijelaskan sebagai bagian dari preprocessing.

Contoh perubahan satu deret data MAIN ditunjukkan pada Tabel 3.7. Kolom precipitation menunjukkan curah hujan pada timestamp target, sedangkan kolom precipitation_lag1 menunjukkan curah hujan satu jam sebelumnya.

**Contoh Deret Data MAIN dan Sumber Nilai Fitur Lag**

| Timestamp target UTC | Node | precipitation pada waktu target (mm) | Sumber nilai lag | precipitation_lag1 (mm) |
| --- | --- | --- | --- | --- |
| 2025-01-01 17:00 | MAIN | 0,000 | Belum tersedia | 0,000* |
| 2025-01-01 18:00 | MAIN | 2,000 | precipitation pukul 17.00 | 0,000 |
| 2025-01-01 19:00 | MAIN | 0,500 | precipitation pukul 18.00 | 2,000 |

Nilai 0,000* pada timestamp pertama merupakan nilai awal karena belum ada data satu jam sebelumnya. Nilai lag pada pukul 19.00 berasal dari curah hujan pukul 18.00, bukan dari nilai pada pukul 19.00. Dengan demikian, fitur lag hanya menggunakan informasi masa lalu.

### 3.4.5 Transformasi Curah Hujan

Transformasi log1p diterapkan khusus pada variabel target curah hujan (precipitation) karena sebagian besar nilainya bernilai nol (zero-inflated), sedangkan sebagian kecilnya memiliki intensitas sangat tinggi (heavy-tailed). Transformasi ini berfungsi meredam kemiringan (skewness) distribusi data sebelum dihitung statistik normalisasinya dan diproses oleh model diffusion. Fitur masukan precipitation_lag1, wind_speed, dan relative_humidity tidak menggunakan transformasi log1p, melainkan langsung dinormalisasi menggunakan statistik Z-score standar. Kebalikan dari transformasi ini digunakan pada tahap post-processing untuk mengembalikan prediksi curah hujan ke skala aslinya melalui fungsi inversi eksponensia. Contoh perhitungannya adalah:

$$
log1p\left(0\right)=log\left(1+0\right)= 0
$$

$$
log1p\left(4\right)=log\left(1+4\right)=log(5) \approx 1,609
$$

$$
exp\left(1,609\right) - 1 \approx 4 mm
$$

Contoh nilai dataset sebelum dan sesudah transformasi ditunjukkan pada Tabel 3.8. Nilai pada kolom precipitation masih menggunakan satuan asli, sedangkan nilai hasil log1p merupakan nilai sementara yang diteruskan ke tahap normalisasi; nilai tersebut tidak disimpan sebagai kolom baru pada dataset mentah. Nilai variabel lain, seperti wind_speed dan relative_humidity, tidak berubah pada tahap ini.

**Contoh Curah Hujan Sebelum dan Sesudah Transformasi log1p**

| Timestamp UTC | Node | precipitation sebelum transformasi (mm) | Nilai sementara setelah log1p |
| --- | --- | --- | --- |
| 2025-01-01 17:00 | MAIN | 0,000 | 0,000 |
| 2025-01-01 18:00 | MAIN | 0,500 | 0,405 |
| 2025-01-01 19:00 | MAIN | 4,000 | 1,609 |

**Tabel 3.8 memperlihatkan bahwa curah hujan nol tetap bernilai nol setelah transformasi, sedangkan nilai positif dikompresi ke skala yang lebih kecil. Transformasi ini tidak menghapus kejadian hujan; transformasi hanya mengubah skala numeriknya. Kecepatan angin dan kelembapan relatif tidak menggunakan transformasi log1p. Pada akhir Subbab 3.3, dataset telah memiliki nama variabel penyajian yang lebih ringkas, urutan kronologis, fitur lag, dan curah hujan yang telah ditransformasi secara sementara. Dataset tersebut belum dinormalisasi. Jika divisualisasikan, distribusi curah hujan setelah log1p menjadi lebih terpusat dan tidak terlalu dipengaruhi oleh nilai ekstrem, tetapi urutan waktu dan hubungan antar catatan tetap sama.**

## 3.5 Pembagian Dataset Temporal

Dataset dibagi secara kronologis berdasarkan timestamp UTC agar model hanya belajar dari periode yang lebih awal dan dievaluasi pada periode yang lebih baru. Skema pembagian ditunjukkan pada Gambar 3.5.

![Gambar 3.4 Ilustrasi Pembagian Dataset Temporal](media_sp2/image9.png)

Ilustrasi Pembagian Dataset Temporal

**Gambar 3.4 menunjukkan tiga bagian data yang dipisahkan berdasarkan waktu.**

Data training berisi periode paling awal. Data ini digunakan untuk menghitung statistik normalisasi, membangun basis analog historis, dan memperbarui parameter model.

Data validation berisi periode setelah training. Data ini digunakan untuk memantau proses pelatihan dan memilih checkpoint tanpa memperbarui statistik atau basis retrieval.

Data test berisi periode paling akhir. Data ini disimpan untuk evaluasi akhir dan tidak digunakan dalam pelatihan maupun pemilihan checkpoint.

Batas pembagian diterapkan pada timestamp UTC yang tersimpan dalam dataset. Periode lokal digunakan sebagai keterangan cakupan waktu, bukan sebagai acuan operasional pembagian. Tidak ada pengacakan, sehingga urutan waktu tetap terjaga.

### 3.5.1 Skema Pembagian Dataset

Rincian rentang waktu dan fungsi partisi temporal dataset disajikan pada Tabel 3.9.

**Skema Pembagian Dataset Temporal**

| Himpunan | Rentang tahun berdasarkan timestamp UTC | Jumlah baris data | Fungsi |
| --- | --- | --- | --- |
| Training | 2005–2018 | 613.560 | Menghitung statistik dan melatih model |
| Validation | 2019–2021 | 131.520 | Memantau pelatihan dan memilih checkpoint |
| Test | 2022–2025 | 175.320 | Evaluasi akhir |

**Tabel 3.9 menunjukkan batas waktu, volume baris data untuk kelima node, dan fungsi setiap himpunan data. Data training berada pada periode paling awal (613.560 baris atau 122.712 timestamp), data validation digunakan setelah proses pelatihan untuk pemantauan (131.520 baris atau 26.304 timestamp), dan data test berada pada periode paling akhir untuk evaluasi (175.320 baris atau 35.064 timestamp). Total keseluruhan mencakup 920.400 baris data (184.080 timestamp). Rentang tabel mengacu pada timestamp UTC dan pembagian dilakukan tanpa pengacakan.**

### 3.5.2 Pencegahan Data Leakage

Pencegahan kebocoran data (data leakage) dilakukan melalui beberapa aturan. Statistik normalisasi dihitung hanya dari data training. Basis analog historis dibangun dari data training. Data validation dan test tidak digunakan untuk memperbarui parameter model atau memilih parameter pelatihan. Setiap sampel prediksi menggunakan enam timestamp sebelum waktu target (rancangan jendela waktu historis $t-6$ sampai $t-1$ dirinci pada Subbab 3.6.2). Karena setiap himpunan diproses sebagai dataset terpisah, enam timestamp pertama pada data validation dan test tidak digunakan sebagai sampel karena belum memiliki jendela historis lengkap di dalam himpunan tersebut. Retrieval menggunakan basis data training agar kondisi pada atau setelah waktu target tidak digunakan sebagai referensi.

### 3.5.3 Normalisasi Data

Setelah pembagian dataset, fitur dan target dinormalisasi menggunakan statistik data training. Statistik target dihitung dari node MAIN. Statistik fitur juga dihitung dari MAIN, kecuali fitur statis atau fitur lain yang memiliki simpangan baku degenerat; fitur tersebut menggunakan statistik seluruh node untuk mencegah pembagian dengan simpangan baku yang mendekati nol. Aturan ini menjaga agar fitur statis seperti elevation tetap memiliki skala yang dapat dibandingkan antarnode.

Perubahan data sebelum dan sesudah normalisasi dapat dilihat pada contoh MAIN berikut. Nilai sebelum normalisasi masih menggunakan satuan meteorologis atau hasil log1p, sedangkan nilai sesudah normalisasi berada pada skala Z-score dan digunakan oleh model.

**Contoh Transformasi dan Normalisasi Target MAIN**

| Variabel target | Nilai asli | Operasi sebelum Z-score | Nilai setelah transformasi | Nilai setelah normalisasi |
| --- | --- | --- | --- | --- |
| precipitation | 0,000 mm | log1p | 0,000 | -0,479 |
| wind_speed | 5,589 m/s | Tidak ada | 5,589 | 0,857 |
| relative_humidity | 95,591% | Tidak ada | 95,591 | 0,986 |

**Tabel 3.10 mengilustrasikan perubahan nilai numerik target pada node MAIN setelah penerapan transformasi log1p dan normalisasi Z-score. Tabel dibaca dari kiri ke kanan: nilai asli, operasi sebelum Z-score, nilai setelah operasi tersebut, kemudian nilai setelah normalisasi.**

Pada baris precipitation, nilai asli 0,000 mm terlebih dahulu menjadi 0 melalui log1p, kemudian menjadi -0,479 setelah Z-score. Kecepatan angin dan kelembapan relatif tidak menggunakan log1p, sehingga nilai setelah transformasi masih sama dengan nilai asli sebelum normalisasi. Nilai tersebut kemudian diubah ke skala Z-score menggunakan rata-rata dan simpangan baku training.

Contoh perhitungan sederhana untuk target curah hujan pada MAIN adalah sebagai berikut. Misalkan curah hujan asli sebesar 0,000 mm. Karena nilai tersebut diproses dengan log1p, nilai setelah transformasi menjadi:

$$
y^{'}=log\left(1+0\right) = 0
$$

Berdasarkan statistik data training, rata-rata curah hujan setelah log1p adalah $\mu = 0,176636$ dan simpangan bakunya $\sigma = 0,368494$ . Nilai Z-score kemudian dihitung sebagai:

$$
z =\frac{0 - 0,176636}{0,368494 + 0,00001} \approx -0,479
$$

Artinya, nilai -0,479 bukan curah hujan sebesar -0,479 mm. Nilai tersebut adalah nilai curah hujan yang telah diubah ke skala standar agar dapat diproses bersama fitur lain. Contoh perhitungan log1p sebelum normalisasi telah ditunjukkan pada Subbab 3.3.5.

Untuk target kecepatan angin, prosesnya lebih singkat karena tidak menggunakan log1p. Misalnya nilai angin 5,589 m/s, rata-rata training 3,873071, dan simpangan baku 2,002620, maka:

$$
z =\frac{5,589 - 3,873071}{2,002620 + 0,00001} \approx 0,857
$$

Jadi, angka pada Tabel 3.10 merupakan nilai yang telah diubah skalanya, bukan satuan asli yang dihapus dari data. Tabel 3.10 merangkum target MAIN, sedangkan susunan lima node sebagai masukan graf dirangkum terpisah pada Tabel 3.11.

Pada contoh timestamp awal, target MAIN memiliki curah hujan 0,000 mm, kecepatan angin 5,589 m/s, dan kelembapan relatif 95,591%. Setelah menggunakan statistik training, nilainya menjadi sekitar -0,479, 0,857, dan 0,986 secara berturut-turut. Contoh ini menunjukkan perubahan skala, bukan hasil prediksi model. Nilai target tersebut berasal dari timestamp target setelah jendela historis enam jam, bukan dari nilai fitur pada timestamp terakhir di dalam jendela.

Nilai fitur pada lima node juga dinormalisasi sebelum masuk ke graf. Untuk contoh timestamp yang sama, beberapa fitur setelah normalisasi ditunjukkan secara ringkas pada Tabel 3.11. Nama variabel tetap mengikuti nama hasil harmonisasi agar makna setiap kolom dapat dibaca langsung.

**Contoh Fitur Lima Node Setelah Normalisasi**

| Node | temperature | relative_humidity | dewpoint | ⋯ | elevation |
| --- | --- | --- | --- | --- | --- |
| MAIN | -0,996 | 0,986 | -0,034 | ⋯ | 1,737 |
| UP | 2,121 | 0,922 | 5,860 | ⋯ | -0,715 |
| DOWN | 2,728 | 1,073 | 7,285 | ⋯ | -1,005 |
| LEFT | 0,632 | 1,106 | 3,296 | ⋯ | 0,471 |
| RIGHT | 2,078 | 1,027 | 5,954 | ⋯ | -0,489 |

**Tabel 3.11 menunjukkan bahwa satu timestamp menghasilkan lima baris fitur yang kemudian disusun menjadi matriks lima node. Kolom yang ditampilkan merupakan contoh dari fitur input. Nilai tersebut digunakan sebagai masukan graf, sedangkan target tetap hanya diambil dari MAIN pada waktu prediksi.**

## 3.6 Pembentukan Fitur dan Representasi Graf

Setelah dataset melalui tahap preprocessing dan pembagian temporal, langkah selanjutnya adalah membentuk representasi data yang sesuai dengan arsitektur model Retrieval-Augmented Diffusion dengan Spatio-Temporal Graph Neural Network.

### 3.6.1 Fitur Masukan Model

Fitur masukan model diringkas berdasarkan nama variabel hasil harmonisasi pada Tabel 3.12. Penamaan tersebut lebih informatif daripada label umum karena pembaca dapat langsung mengetahui makna setiap masukan.

**Fitur Masukan Model Setelah Harmonisasi Nama Variabel**

| No. | Nama variabel setelah harmonisasi | Keterangan | Status |
| --- | --- | --- | --- |
| 1 | temperature | Suhu udara | Dinamis |
| 2 | relative_humidity | Kelembapan relatif | Dinamis |
| 3 | dewpoint | Titik embun | Dinamis |
| 4 | surface_pressure | Tekanan permukaan | Dinamis |
| 5 | wind_speed | Kecepatan angin | Dinamis |
| 6 | wind_direction | Arah angin | Dinamis |
| 7 | cloud_cover | Tutupan awan | Dinamis |
| 8 | precipitation_lag1 | Curah hujan satu jam sebelumnya | Dinamis |
| 9 | elevation | Elevasi node | Statis |

Sembilan fitur tersebut digunakan pada waktu historis dari $t-6$ sampai $t-1$ untuk seluruh node. Tiga target pada waktu $t$ tetap diambil dari MAIN, yaitu precipitation, wind_speed, dan relative_humidity. Dengan demikian, relative_humidity dan wind_speed dapat muncul sebagai fitur historis sekaligus target pada waktu berikutnya, sedangkan precipitation_lag1 hanya berfungsi sebagai fitur masukan. Keempat node selain MAIN berfungsi sebagai konteks spasial.

### 3.6.2 Pembentukan Jendela Waktu Historis

Untuk target meteorologis pada waktu t, masukan graf hanya menggunakan enam timestamp sebelumnya, setiap timestamp memiliki lima node dan sembilan fitur per node. Konteks tambahan diambil dari fitur MAIN pada $t-1$ . Contoh jendela historis untuk target pukul 18.00 UTC ditunjukkan pada Tabel 3.13.

| Posisi waktu | Timestamp UTC | Isi data | Peran |
| --- | --- | --- | --- |
|  | 12.00 |  | Snapshot graf |
|  | 13.00 |  | Snapshot graf |
|  | 14.00 |  | Snapshot graf |
|  | 15.00 |  | Snapshot graf |
|  | 16.00 |  | Snapshot graf |
|  | 17.00 |  | Snapshot graf dan konteks MAIN |
|  | 18.00 | 3 target dari MAIN | Target prediksi, bukan masukan |

Enam baris pertama pada Tabel 3.13 digunakan sebagai masukan model. Baris pada waktu $t$ tidak dimasukkan ke dalam urutan graf karena berisi nilai yang ingin diprediksi. Setiap snapshot memiliki lima node dan sembilan fitur, sedangkan konteks tambahan hanya mengambil fitur MAIN pada $t-1$ . Dengan demikian, urutan waktu, bentuk data, dan posisi target dapat dibaca secara langsung.

### 3.6.3 Topologi Graf Lima Node

Hubungan antarnode direpresentasikan dengan topologi bintang (star). MAIN terhubung secara dua arah dengan UP, DOWN, LEFT, dan RIGHT. Node tetangga tidak memiliki edge graf langsung satu sama lain. Topologi tersebut menghasilkan delapan edge graf berarah. Topologi keterhubungan spasial dan arah pertukaran pesan antarnode disajikan pada Gambar 3.6.

![Gambar 3.5 Topologi Graf Star Lima Node](media_sp2/image10.jpeg)

Topologi Graf Star Lima Node

**Gambar 3.5 menunjukkan susunan topologi graf yang digunakan.**

MAIN berada di tengah dan menjadi node yang terhubung dengan seluruh node konteks.

UP, DOWN, LEFT, dan RIGHT menjadi node tetangga yang mengirimkan dan menerima informasi dari MAIN.

Panah menunjukkan arah pertukaran pesan graf, bukan arah angin.

Delapan edge graf berarah berasal dari empat pasangan hubungan dua arah antara MAIN dan setiap node tetangga.

Self-loop atau sisi yang menghubungkan node dengan dirinya sendiri tidak ditampilkan sebagai bagian dari delapan edge graf berarah. Penambahan self-loop oleh lapisan graf dijelaskan pada Subbab 3.7.1.

Pada tahap pembentukan graf, informasi spasial utama berasal dari topologi bintang dan perbedaan fitur antarnode pada setiap timestamp. Detail atribut edge graf dan pemrosesan pesan internal lapisan graf dijelaskan pada Subbab 3.7.1. Representasi urutan graf enam timestamp ini kemudian menjadi masukan bagi Spatio-Temporal Graph Neural Network untuk memodelkan ketergantungan ruang-waktu secara simultan.

## 3.7 Perancangan Arsitektur Model

Arsitektur model yang dikembangkan dalam penelitian ini merupakan integrasi antara dua komponen utama, yaitu Spatio-Temporal Graph Neural Network (STGNN) dan Retrieval-Augmented Diffusion Model. Desain ini dirancang khusus untuk menangani karakteristik presipitasi orografis di pegunungan tropis serta menghasilkan prediksi probabilistik satu jam ke depan yang akurat dan sensitif terhadap kejadian ekstrem.

### 3.7.1 Spatio-Temporal Graph Neural Network (STGNN)

Komponen pertama adalah Spatio-Temporal Graph Neural Network yang dirancang untuk memodelkan interaksi spasial antarlokasi lereng Gunung Gede–Pangrango sekaligus dinamika ketergantungan temporal cuaca dari enam snapshot graf historis menjadi satu vektor representasi graf padat (graph embedding). Arsitektur ini terdiri atas pemrosesan spasial menggunakan dua lapis Graph Attention Network (GAT) dan pemrosesan temporal menggunakan Causal Multi-Head Self-Attention. Alur pemrosesan STGNN ditunjukkan pada Gambar 3.7.

![Gambar 3.6 Arsitektur Spatio-Temporal Graph Neural Network](media_sp2/image11.jpeg)

Arsitektur Spatio-Temporal Graph Neural Network

**Gambar 3.6 menunjukkan alur arsitektur STGNN yang menerima urutan graf sebagai masukan. Alur pemrosesan dibagi menjadi lima tahap, yaitu input graph sequence, encoding spasial dengan GAT, global mean pooling, temporal attention, dan pembentukan graph embedding. Embedding yang dihasilkan digunakan sebagai kondisi tambahan pada Conditional Diffusion Model.**

Input Sequence

Input STGNN berupa enam snapshot graf historis. Setiap snapshot memiliki lima node dengan sembilan fitur yang telah melalui preprocessing dan normalisasi. Struktur edge dipertahankan sama pada seluruh snapshot, sedangkan nilai fitur node berubah mengikuti timestamp. Dengan demikian, input STGNN memuat dimensi node, fitur, dan urutan waktu tanpa mengubah struktur spasial pada setiap langkah.

Secara operasional, urutan snapshot yang digunakan adalah $G_{t-6},G_{t-5}, \dots , G_{t-1}$ . Setiap snapshot graf pada langkah waktu $\tau \in {t-6, \dots ,t-1}$ didefinisikan sebagai $G_{\tau}=( V,E,X_{\tau},E)$ di mana $V= \left{MAIN, UP, DOWN, LEFT, RIGHT\right}$ merupakan himpunan lima node pemantauan ( $\left|V\right|=5$ ), $E$ adalah himpunan delapan directed edges berarah dua arah antara MAIN dan empat node lereng bertopologi bintang (star topology), $E \in R^{8 \times 1}$ adalah atribut jarak spasial statis antar-grid ( $0,25^{∘}$ ), dan $X_{\tau} \in$ merupakan matriks sembilan fitur cuaca ternormalisasi untuk kelima node. Matriks fitur pada waktu $\tau$ dirumuskan sebagai:

$$
X_{\tau}=\left[ x_{MAIN, \tau}^{T}x_{UP, \tau}^{T}x_{DOWN, \tau}^{T}x_{LEFT, \tau}^{T}x_{RIGHT, \tau}^{T}\right] \in R^{5 \times 9}
$$

Node MAIN pada $t-1$ juga digunakan sebagai context tambahan, sedangkan target diffusion berada pada node MAIN waktu target dan tidak menjadi bagian dari graph sequence yang diberi noise.

GAT 1(Graph Attention Network 1)

Lapisan konvolusi graf pertama menerapkan mekanisme multi-head spatial attention dengan $K_{1}=4$ heads independen dan dimensi tersembunyi $d_{1}=64$ per head. Lapisan ini menghitung koefisien atensi spasial antara node target dan node tetangga dengan mempertimbangkan fitur node serta atribut jarak edge, kemudian menggabungkan (concatenate) keluaran keempat head dan menerapkan fungsi aktivasi ReLU

GAT 2 (Graph Attention Network 2)

Lapisan konvolusi graf kedua menggunakan satu head atensi tunggal ( $K_{2}=1$ ) untuk memetakan kembali representasi 256 dimensi hasil GAT1 menjadi representasi spasial lokal berdimensi 64 yang lebih padat dan terintegrasi. Agregasi dilakukan secara linier tanpa fungsi aktivasi non-linier tambahan sebelum proses pooling.

Global Mean Pooling

Operasi global mean pooling merata-ratakan representasi fitur dari seluruh node pada masing-masing snapshot graf untuk menghasilkan satu vektor ringkasan tingkat graf (graph-level embedding) $g_{\tau} \in R^{64}$ pada setiap langkah waktu $\tau$ . Enam vektor ringkasan dari $\tau =t-6$ hingga $t-1$ kemudian disusun secara sekuensial membentuk matriks deret temporal:

$$
G=\left[g_{t-6}g_{t-5}⋮g_{t-1}\right] \in R^{6 \times 64}
$$

Temporal Attention

Blok pemodelan waktu menerapkan Causal Multi-Head Self-Attention ( $K_{t} = 4 heads, dimensi per head d_{k}=64/4 =16$ ) yang diperkaya dengan learnable positional embedding $E_{pos} \in R^{6 \times 64}$ untuk mengenali urutan kronologis antar-jam. Struktur ini dilengkapi koneksi residual (residual connection), regularisasi dropout ( $p=0,1$ ), dan Layer Normalization

Setiap langkah waktu menghitung korelasi temporal masa lalunya melalui empat head, melewati dropout dan normalisasi lapisan, menghasilkan representasi temporal $Z \in R^{6 \times 64}$ .

Causal Slicing Timestep

Penerapan matriks causal mask $M_{causal} \in R^{6 \times 6}$ (bernilai $-∞$ pada elemen segitiga atas di mana kolom $>$ baris, dan bernilai 0 pada elemen lainnya) menjamin prinsip kausalitas temporal terpenuhi secara ketat, yaitu langkah waktu $\tau$ tidak dapat mengakses informasi waktu di masa depan ( $> \tau$ ). Representasi fitur pada langkah waktu paling akhir ( $t-1$ ) kemudian diiris (sliced) sebagai ringkasan kondisi cuaca historis paling mutakhir

Output Projection

Tahap akhir STGNN menggunakan lapisan transformasi linier (nn.Linear(64, 64)) untuk memproyeksikan vektor temporal terakhir ke dalam ruang embedding representasi graf akhir

Hasil akhirnya adalah embedding graf berdimensi 64 yang memuat ringkasan keterkaitan spasial antarlokasi dan dinamika temporal cuaca sepanjang jendela historis enam jam. Rincian alur transformasi tensor pada setiap tahapan STGNN dirangkum pada Tabel 3.13.

**Rincian Alur Transformasi Tensor pada Komponen STGNN**

| No | Nama Komponen | Modul / Operasi PyTorch | Dimensi Masukan | Dimensi Keluaran | Keterangan Pemrosesan |
| --- | --- | --- | --- | --- | --- |
| 1 | Input Sequence | torch_geometric.data.Data |  |  | Enam snapshot graf historis ($t-6 \dots t-1$) |
| 2 | GAT1 | GATConv(9, 64, heads=4) + ReLU | [5, 9] per snapshot | [5, 256] per snapshot | Multi-head spatial attention terkonkatenasi |
| 3 | GAT2 | GATConv(256, 64, heads=1) | [5, 256] per snapshot | [5, 64] per snapshot | Reduksi representasi spasial node |
| 4 | Global Mean Pool | global_mean_pool | [5, 64] per snapshot | [1, 64] per snapshot | Agregasi rata-rata lima node ke level graf |
| 5 | Temporal Attention | MultiheadAttention(64, heads=4) | [6, 64] | [6, 64] | Causal self-attention temporal + Positional Embedding |
| 6 | Causal Slicing | x[:, -1, :] (tensor slicing) | [6, 64] | [1, 64] | Pengambilan representasi waktu terakhir ($t-1$) |
| 7 | Output Projection | nn.Linear(64, 64) | [1, 64] | [1, 64] | Proyeksi linier menuju Graph Embedding |

### 3.7.2 Integrasi Retrieval-Augmented Diffusion Model

Integrasi arsitektur Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network (STGNN) dirancang untuk memprediksi distribusi probabilitas multivariat tiga parameter cuaca target (curah hujan [mm/jam], kecepatan angin [m/s], dan kelembapan relatif [%]) pada node MAIN untuk horizon waktu $t$ . Arsitektur ini menggabungkan empat pilar representasi utama: (1) konteks dinamika spasio-temporal regional melalui graf lereng pegunungan, (2) konteks meteorologis lokal mutakhir node target, (3) analog historis pola cuaca serupa dari basis data k-NN masa lalu (historical analogs), dan (4) pemodelan noise stokastik berbasis reverse diffusion.

Alur rancangan integrasi model, komponen pemrosesan kondisi (conditioning), perambatan maju denoiser, serta mekanisme perhitungan fungsi loss disajikan secara menyeluruh pada Gambar 3.8.

![Gambar 3.7 Integrasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network](media_sp2/image12.jpeg)

Integrasi Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network

**Gambar 3.7 menunjukan 25 tahapan dari Retrieval-Augmented Diffusion Model dengan Spatio-Temporal Graph Neural Network untuk rincian tahapan dijelaskan sebagaimana berikut ini:**

Output STGNN (1) berfungsi mengekstraksi keterkaitan spasial regional dan dinamika temporal dari urutan graf cuaca historis. Komponen ini menerima masukan berupa enam snapshot graf historis $G_{t} \in R^{6 \times 5 \times 9}$ dari rentang waktu $t-6$ hingga $t-1$ , lalu menghasilkan keluaran berupa vektor representasi graf (graph embedding) $h_{graph} \in R^{64}$

Graph MLP (2) berfungsi memproyeksikan vektor keluaran STGNN ke dalam ruang representasi pengondisian laten (conditioning space). Lapisan ini memproses masukan berupa vektor $h_{graph} \in R^{64}$ dan menghasilkan keluaran berupa vektor kondisi graf $h_{t}^{G} \in R^{64}$ .

Context Input (3) berfungsi menyediakan kondisi meteorologis permukaan mutakhir yang diamati secara lokal pada node MAIN. Tahap ini mengambil masukan berupa nilai observasi lokal pada langkah waktu $t-1$ dan menghasilkan keluaran berupa vektor sembilan fitur ternormalisasi $x_{MAIN, t-1} \in R^{9}$ .

Context MLP (4) berfungsi memetakan sembilan fitur cuaca lokal MAIN ke ruang representasi kondisi tersembunyi. Modul ini menerima masukan berupa vektor $x_{MAIN, t-1} \in R^{9}$ untuk menghasilkan keluaran berupa vektor kondisi lokal $hₜ^{MAIN} \in R^{64}$ .

Retrieval Input (5) berfungsi menyediakan nilai target historis satu jam ke depan dari tiga kejadian masa lalu yang paling mirip (Top-3 Analogs melalui FAISS k-NN). Masukan yang diterima berupa matriks berdimensi $3 tetangga \times 3 target \left(v_{\tau _{1}},v_{\tau _{2}},v_{\tau _{3}}\right)$ , yang kemudian diratakan untuk menghasilkan keluaran berupa vektor hasil perataan (flattened vector) $r_{flat} \in R^{9}$ .

Retrieval MLP (6) berfungsi memetakan representasi sembilan dimensi analog historis ke dalam ruang embedding kondisi. Lapisan ini memproses masukan berupa vektor $r_{flat} \in R^{9}$ dan menghasilkan keluaran berupa vektor kondisi retrieval $h_{t}^{R} \in R^{64}$ .

Condition Embedding (7) berfungsi menggabungkan seluruh informasi lingkungan atmosfer yang mencakup graf, konteks lokal, dan retrieval secara aditif. Komponen ini menerima masukan berupa tiga vektor kondisi $h_{t}^{G}, h_{t}^{MAIN},h_{t}^{R} \in R^{64}$ dan menghasilkan keluaran berupa satu vektor kondisi total atmosfer $c_{t} \in R^{64}$ .

Diffusion Timestep (8) berfungsi menentukan tingkat intensitas noise stokastik pada iterasi pelatihan diffusion. Tahap ini mengambil masukan dari hasil pembangkitan acak seragam $s∼U\left(\left{0, 1, \dots , T_{train}-1\right}\right)$ dengan $T_{train}=1000$ , lalu menghasilkan keluaran berupa nilai skalar integer $s \in \left[0, 999\right]$ .

Time MLP (9) berfungsi mengonversi langkah waktu diffusion diskret $s$ menjadi representasi kontinu berdimensi 64. Modul ini menerima masukan berupa skalar langkah waktu diffusion $s \in R^{1}$ dan menghasilkan keluaran berupa vektor penyematan waktu (time embedding) $h_{s}^{time} \in R^{64}$ .

Total Embedding (10) berfungsi menyatukan representasi atmosferik dan time embedding langkah diffusion sebagai vektor conditioning total. Masukan yang diproses terdiri atas vektor $c_{t} \in R^{64}$ dan $h_{s}^{time} \in R^{64}$ , menghasilkan keluaran berupa vektor total conditioning $c_{t}^{total} \in R^{64}$ .

Denoiser Input / Noisy Target (11) berfungsi membentuk masukan target berderau (noisy target) pada timestep $s$ melalui proses forward diffusion. Komponen ini menerima masukan berupa target bersih $y_{0} \in R^{3}$ , Gaussian noise $ϵ \in R^{3}$ , dan jadwal varians (noise variance schedule)   $\alpha _{s}$ , sehingga menghasilkan keluaran berupa vektor noisy target $y_{s} \in R^{3}$ .

Down1 (12) berfungsi mereduksi target tiga dimensi ke dimensi tersembunyi 64 sekaligus menginjeksikan vektor kondisi total $c_{t}^{total}$ . Lapisan ini memproses masukan berupa noisy target $y_{s} \in R^{3}$ bersama vektor pengondisian $c_{t}^{total} \in R^{64}$ , dan menghasilkan keluaran berupa vektor representasi tersembunyi $h_{1} \in R^{64}$ .

Down2 (13) berfungsi memperluas kapasitas representasi fitur tersembunyi denoiser ke dimensi yang lebih tinggi. Masukan yang diterima berupa vektor $h_{1} \in R^{64}$ , dan keluaran yang dihasilkan adalah vektor representasi $h_{2} \in R^{128}$ .

Skip Connection (14) berfungsi menyalurkan salinan fitur $h_{2}$ secara langsung ke tahap penggabungan akhir demi mempertahankan informasi representasi perantara. Komponen ini menerima masukan berupa vektor $h_{2} \in R^{128}$ dan menghasilkan keluaran berupa salinan identitas tensor $h_{2} \in R^{128}$ .

Mid Layer (15) berfungsi sebagai lapisan pemrosesan laten tingkat tinggi pada bagian bottleneck. Lapisan ini menerima masukan berupa vektor $h_{2} \in R^{128}$ dan menghasilkan keluaran berupa vektor representasi tengah $h_{mid} \in R^{128}$ .

Concatenate (16) berfungsi menggabungkan representasi fitur lapisan bottleneck (mid layer) dengan fitur dari jalur skip connection. Masukan yang diterima terdiri atas vektor $h_{mid} \in R^{128}$ dan $h_{2} \in R^{128}$ , yang menghasilkan keluaran berupa vektor terkonkatenasi $h_{up} \in R^{256}$ .

Up MLP (17) berfungsi merekonstruksi dan memproyeksikan fitur gabungan kembali ke dimensi fisik tiga variabel target. Modul ini menerima masukan berupa vektor gabungan $h_{up} \in R^{256}$ dan menghasilkan keluaran berupa vektor estimasi noise (predicted noise)   $ϵ_{\theta} \in R^{3}$ .

Predicted Noise (18) berfungsi merepresentasikan estimasi Gaussian noise yang diprediksi oleh jaringan denoiser. Komponen ini menerima masukan dari keluaran rekonstruksi Up MLP dan menghasilkan keluaran berupa vektor estimasi noise $ϵ_{\theta}=\left[ϵ_{1}, ϵ_{2}, ϵ_{3}\right]^{T} \in R^{3}$ .

Target Ground Truth (19) berfungsi menyediakan data observasi aktual tiga variabel cuaca ternormalisasi sebagai acuan pembobotan penalti ekstrem. Tahap ini mengambil masukan dari nilai observasi aktual target MAIN pada waktu $t$ dan menghasilkan keluaran berupa vektor target bersih $y_{0} \in R^{3}$ .

Gaussian Noise (20) berfungsi menyediakan derau acak standar yang dibangkitkan sebagai target acuan perbandingan (ground truth noise). Komponen ini menerima masukan berupa sampel dari distribusi normal standar $N\left(0, I\right)$ dan menghasilkan keluaran berupa vektor Gaussian noise $ϵ \in R^{3}$ .

Weighted Noise Loss (21) berfungsi menghitung penalti fungsi loss kuadratik terbobot antara ground truth noise $ϵ$ dan prediksi noise   $ϵ_{\theta}$ dengan bobot ekstra untuk kejadian ekstrem. Masukan yang diproses mencakup prediksi noise   $ϵ_{\theta} \in R^{3}$ , ground truth noise $ϵ \in R^{3}$ , dan target acuan $y_{0} \in R^{3}$ , yang kemudian menghasilkan keluaran berupa nilai skalar $L_{noise} \in R^{+}$ .

Auxiliary Wet Head (22) berfungsi memprediksi logit biner ada atau tidaknya kejadian hujan berdasarkan representasi kondisi atmosfer $c_{t}$ . Lapisan ini menerima masukan berupa vektor kondisi $c_{t} \in R^{64}$ dan menghasilkan keluaran berupa nilai skalar logit $z_{wet} \in R^{1}$ serta nilai probabilitas hujan $p_{wet} \in \left[0, 1\right]$ .

Auxiliary Wet Loss (23) berfungsi menghitung penalti biner terbobot (pos_weight) guna menajamkan pemisahan antara kondisi kering dan basah (zero-inflated). Masukan yang diterima berupa logit $z_{wet}$ dan label biner hujan aktual $y_{wet} \in \left{0, 1\right}$ , sehingga menghasilkan keluaran berupa nilai skalar fungsi loss klasifikasi $L_{wet} \in R^{+}$ .

Total Training Loss (24) berfungsi menggabungkan fungsi loss diffusion dan fungsi loss klasifikasi kejadian hujan menjadi satu objektif optimasi tunggal. Komponen ini memproses masukan berupa nilai $L_{noise}$ dan $L_{wet}$ dengan pembobotan $\lambda _{wet}=0,7$ , lalu menghasilkan keluaran berupa nilai skalar objektif terpadu $L_{total} \in R^{+}$ .

Backpropagation (25) berfungsi menghitung gradien otomatis, memotong gradien ekstrem secara teratur ( $\le 1,0$ ), dan memperbarui seluruh bobot parameter model $\theta$ secara end-to-end. Masukan yang digunakan adalah nilai skalar $L_{total}$ beserta kumpulan parameter model $\theta =\left{\theta _{STGNN}, \theta _{diff}\right}$ , dengan keluaran berupa parameter jaringan $\theta$ yang telah diperbarui melalui algoritma optimasi AdamW.

Rincian alur transformasi tensor, ukuran dimensi, modul PyTorch terkait, dan fungsi komputasi pada integrasi model diffusion terangkum secara sistematis pada Tabel 3.14.

**Rincian Alur Transformasi Tensor pada Komponen Integrasi Diffusion**

| No. | Nama Komponen | Modul / Operasi PyTorch | Dimensi Masukan | Dimensi Keluaran | Keterangan Pemrosesan |
| --- | --- | --- | --- | --- | --- |
| 1 | Output STGNN | SpatioTemporalGNN |  | [B, 64] | Representasi graf spasio-temporal |
| 2 | Graph MLP | nn.Sequential(Linear(64,64), SiLU, Linear(64,64)) | [B, 64] | [B, 64] | Pemetaan kondisi graf ke ruang laten |
| 3 | Context Input | x_main[:, -1, :] | [B, 9] | [B, 9] | Fitur cuaca node MAIN pada $t-1$ |
| 4 | Context MLP | nn.Sequential(Linear(9,64), SiLU, Linear(64,64)) | [B, 9] | [B, 64] | Pemetaan kondisi cuaca lokal mutakhir |
| 5 | Retrieval Input | retrieval_values.reshape(B, -1) | [B, 3, 3] | [B, 9] | Target $t-1$ dari top-3 analog historis |
| 6 | Retrieval MLP | nn.Sequential(Linear(9,64), SiLU, Linear(64,64)) | [B, 9] | [B, 64] | Pemetaan prior pola analog masa lalu |
| 7 | Condition Embedding | Penjumlahan elemen ($h_{t}^{G}+h_{t}^{MAIN}+ h_{t}^{R}$) |  | [B, 64] | Penggabungan ketiga kondisi lingkungan |
| 8 | Diffusion Timestep | torch.randint(0, 1000, (B,)) | Skalar integer | [B] | Indeks langkah diffusion stokastik |
| 9 | Time MLP | SinusoidalPosEmb(64) + Linear(64,128) + Linear(128,64) | [B] | [B, 64] | Sinusoidal positional embedding waktu diffusion |
| 10 | Total Embedding | Penjumlahan elemen ($c_{t}+ h_{s}^{time}$) |  | [B, 64] | Vektor conditioning total atmosfer dan waktu |
| 11 | Denoiser Input | Forward Diffusion scheduler.add_noise | [B, 3] | [B, 3] | Target 3 variabel yang diinjeksi noise (noisy target) |
| 12 | Down1 | Linear(3, 64) + SiLU + $c_{t}^{total}$ | [B, 3] | [B, 64] | Reduksi pertama + injeksi conditioning total |
| 13 | Down2 | Linear(64, 128) + SiLU | [B, 64] | [B, 128] | Ekspansi representasi fitur laten |
| 14 | Skip Connection | Identity mapping | [B, 128] | [B, 128] | Skip connection resolusi fitur perantara |
| 15 | Mid Layer | Linear(128, 128) + SiLU | [B, 128] | [B, 128] | Transformasi representasi laten bottleneck |
| 16 | Concatenate | torch.cat([h_mid, h2], dim=-1) |  | [B, 256] | Penggabungan bottleneck dan skip connection |
| 17 | Up MLP | Linear(256, 64) + SiLU + Linear(64, 3) | [B, 256] | [B, 3] | Proyeksi balik ke dimensi target |
| 18 | Predicted Noise | Keluaran denoiser  $ϵ_{\theta}$ | [B, 256] | [B, 3] | Estimasi noise 3 variabel cuaca |
| 19 | Target GT | targets ($y_{0}$) | [B, 3] | [B, 3] | Target observasi aktual ternormalisasi |
| 20 | Gaussian Noise | torch.randn_like(targets) | [B, 3] | [B, 3] | Gaussian noise standar acuan |
| 21 | Weighted Noise Loss | RainForecaster.weighted_noise_loss |  | Skalar | MSE terbobot penalti ekstrem |
| 22 | Auxiliary Wet Head | Linear(64, 64) + SiLU + Linear(64, 1) | [B, 64] | [B, 1] | Logit klasifikasi kejadian hujan |
| 23 | Auxiliary Wet Loss | BCEWithLogitsLoss(pos_weight) | [B, 1] | Skalar | Klasifikasi penanganan zero-inflation |
| 24 | Total Loss |  | 2 Skalar | Skalar | Fungsi objektif pelatihan terpadu |
| 25 | Backpropagation | optimizer.step() via AdamW | Skalar | Parameter | Pembaruan parameter dengan gradient clipping ($\le 1,0$) |

### 3.7.3 Integrasi End-to-End Model

Secara keseluruhan, satu sampel prediksi dibentuk melalui urutan berikut:

mengambil enam snapshot graf dari $t-6$ hingga $t-1$ ;

mengambil konteks MAIN pada $t-1$ ;

membentuk embedding graf melalui STGNN;

mencari tiga analog historis;

membentuk embedding graf, konteks, retrieval, dan waktu;

menggabungkan embedding menjadi embedding total;

memberi noise pada target tiga variabel;

memperkirakan noise melalui MLP denoiser;

menjalankan reverse diffusion;

mengembalikan sampel ke skala asli dan menerapkan batas fisik.

## 3.8 Pelatihan dan Pembentukan Prediksi

Setelah arsitektur model dirancang, tahap pelatihan dilakukan untuk mengoptimalkan parameter model agar mampu mempelajari pola kompleks dari data spasio-temporal serta menghasilkan prediksi probabilistik yang akurat. Proses pelatihan menggunakan data pelatihan yang telah melalui preprocessing dan representasi graf, dengan tujuan utama meminimalkan kesalahan prediksi sekaligus meningkatkan sensitivitas terhadap kejadian ekstrem yang berpotensi memicu hipotermia pendaki.

### 3.8.1 Prosedur Pelatihan

Pelatihan menggunakan sampel dengan enam snapshot historis. Pada setiap sampel, urutan graf (graph sequence) berasal dari $t-6$ hingga $t-1$ , konteks berasal dari MAIN pada $t-1$ , dan target berasal dari MAIN pada $t$ . Hanya target yang diberi noise; fitur graf, konteks, dan retrieval tidak diberi noise. Bentuk satu sampel yang masuk ke proses pelatihan diringkas sebagai berikut:

Graph sequence: 6 timestamp × 5 node × 9 fitur

Konteks: 9 fitur MAIN pada $t-1$

Retrieval: 3 analog historis × 3 variabel target

Target: 3 variabel MAIN pada $t$

Dengan susunan tersebut, enam snapshot graf digunakan untuk menangkap kondisi spasial-temporal historis. Konteks MAIN dan tiga analog historis digunakan sebagai informasi tambahan, sedangkan target tiga variabel pada MAIN menjadi nilai yang dipelajari model. Sampel-sampel tersebut kemudian dikelompokkan ke dalam batch untuk memperbarui parameter model.

Noise Gaussian diambil dengan dimensi yang sama dengan target. Timestep diffusion $s$ dipilih pada rentang 0 hingga 999. Scheduler DDPM (Denoising Diffusion Probabilistic Model) kemudian membentuk noisy target. Denoiser dilatih untuk memperkirakan noise yang ditambahkan. Pada saat inferensi, DDIM (Denoising Diffusion Implicit Model) digunakan sebagai scheduler proses sampling dengan 20 langkah.

### 3.8.2 Fungsi Loss

Fungsi loss noise menggunakan bobot berdasarkan besar target ternormalisasi. Model juga memiliki cabang keluaran tambahan untuk klasifikasi hujan/tidak hujan (auxiliary wet/dry head) dengan loss $L_{wet}$ . Mekanisme gradient clipping digunakan untuk membatasi norma gradien sebelum pembaruan parameter. Optimizer AdamW memperbarui parameter berdasarkan fungsi loss total tersebut.

### 3.8.3 Konfigurasi Pelatihan

Parameter hiperparameter dan pengaturan komputasi pelatihan model dirangkum pada Tabel 3.15.

**Konfigurasi Pelatihan Model**

| Parameter | Nilai | Keterangan |
| --- | --- | --- |
| Optimizer | AdamW | Optimizer pembaruan parameter model |
| Weight decay |  | Regularisasi parameter optimizer |
| Learning rate awal | 0,001 | Laju pembelajaran awal |
| Batch size | 512 | Jumlah sampel per pembaruan parameter |
| Epoch maksimum | 20 | Jumlah maksimum putaran pelatihan |
| Early stopping patience | 12 | Batas epoch tanpa perbaikan validasi |
| Lookback window |  | Panjang konteks observasi historis |
| FAISS neighbors |  | Jumlah analog historis yang diambil |
| Diffusion train steps | 1000 | Jumlah langkah proses diffusion saat pelatihan |
| Diffusion inference steps | 20 | Jumlah langkah sampling saat inferensi |
| Ensemble size | 30 sampel | Jumlah sampel prediksi probabilistik |
| LR scheduler | ReduceLROnPlateau | Penyesuaian learning rate berdasarkan metrik validasi |
| Gradient clipping | 1,0 | Batas norma gradien untuk menjaga stabilitas pelatihan |
| Conditioning dropout | 0,15 | Peluang penghilangan kondisi saat pelatihan diffusion |
| Auxiliary wet/dry threshold | 0,1 mm/jam | Ambang klasifikasi kejadian hujan |
| Auxiliary wet/dry weight | 0,7 | Bobot loss auxiliary wet/dry |

**Tabel 3.15 merangkum parameter yang menjaga konsistensi proses pelatihan dan evaluasi. Jendela historis (lookback window) menetapkan enam jam masukan, jumlah tetangga FAISS menetapkan tiga analog historis, dan jumlah langkah diffusion saat pelatihan (diffusion train steps) ditetapkan sebanyak 1000. Ambang dan bobot fungsi loss klasifikasi hujan/tidak hujan mengatur kontribusi cabang tambahan terhadap fungsi loss total. Statistik normalisasi dan basis retrieval dihitung dari data training. Checkpoint dipilih berdasarkan perkembangan data validation. Satu seed digunakan dalam rancangan ini; karena itu, hasil perbandingan harus ditafsirkan sebagai hasil satu konfigurasi seed.**

### 3.8.4 Pembentukan Prediksi

Pada proses inferensi, model menghasilkan beberapa sampel menggunakan reverse diffusion. Protokol evaluasi menggunakan 30 sampel ensambel dan DDIM dengan 20 langkah. Saat inferensi aplikasi, jumlah sampel dapat diatur sesuai kebutuhan komputasi; hasil evaluasi utama dalam penelitian ini menggunakan 30 sampel agar setiap skenario dibandingkan dengan jumlah sampel yang sama. Setiap sampel memakai masukan enam jam historis untuk memprediksi kondisi MAIN satu jam berikutnya. Sampel-sampel tersebut digunakan untuk membentuk prediksi titik dan mengukur ketidakpastian prediksi.

### 3.8.5 Post-processing Prediksi

Setelah proses sampling selesai, prediksi dikembalikan ke skala asli menggunakan denormalisasi Z-score. Contoh pembalikan skala curah hujan ditunjukkan sebagai berikut. Jika nilai Z-score adalah -0,479, maka:

$$
v = \left(-0,479\right)\left(0,368494 + 0,00001\right)+ 0,176636 \approx 0
$$

Nilai tersebut kemudian dikembalikan dari transformasi log1p:

$$
y=exp\left(0\right)-1 = 0 mm
$$

Dengan demikian, nilai -0,479 adalah nilai standar untuk diproses model, bukan curah hujan -0,479 mm. Dalam implementasi, operasi terakhir dapat dilakukan menggunakan expm1. Setelah itu, batas fisik diterapkan: curah hujan dibatasi pada rentang 0–60 mm/jam, kecepatan angin tidak boleh negatif, dan kelembapan relatif dibatasi pada rentang 0–100%.

Mekanisme rain gate digunakan pada saat inferensi model utama. Gerbang (gate) ini dihitung dari probabilitas klasifikasi hujan/tidak hujan yang telah dikalibrasi pada data validation, kemudian diterapkan setelah seluruh lintasan sampel dibentuk. Jika probabilitas hujan pada suatu jendela berada di bawah ambang 0,6, komponen curah hujan pada jendela tersebut diatur menjadi 0; kecepatan angin dan kelembapan relatif tidak diubah. Jika seluruh jendela inferensi memiliki probabilitas di bawah ambang tersebut, rain gate tidak diterapkan untuk mencegah keluaran hujan selalu bernilai nol.

## 3.9 Metode Evaluasi Model

Evaluasi model dilakukan untuk mengukur kemampuan sistem dalam memprediksi kondisi meteorologis pada node utama (MAIN) secara akurat dan andal. Mengingat model menghasilkan prediksi dalam bentuk distribusi probabilistik, evaluasi tidak hanya mencakup akurasi titik (point forecast), tetapi juga kualitas distribusi probabilitas dan kemampuan deteksi kejadian ekstrem. Seluruh evaluasi dilakukan secara eksklusif menggunakan data pengujian (test set).

### 3.9.1 Protokol Evaluasi

Evaluasi menggunakan prediksi satu langkah ke depan (one-step-ahead forecast). Untuk setiap target pada waktu, model menggunakan enam jam historis dari $t-6$ sampai $t-1$ untuk memprediksi kondisi MAIN pada $t$ . Evaluasi utama dilakukan pada data test yang tidak digunakan dalam pelatihan atau pemilihan checkpoint. Pengambilan sampel evaluasi dilakukan setiap jam ( $eval_step=1$ ) sehingga tidak ada timestamp test yang dilewati karena subsampling. Horizon prediksi tetap satu jam; eval_step hanya mengatur jarak pengambilan sampel evaluasi.

### 3.9.2 Evaluasi Prediksi Titik

Prediksi titik dihitung dari median ensambel (ensemble). Metrik yang digunakan adalah MAE, RMSE, dan koefisien korelasi Pearson.

### 3.9.3 Evaluasi Prediksi Probabilistik

Evaluasi probabilistik menggunakan seluruh anggota ensambel. CRPS digunakan untuk menilai kedekatan distribusi prediksi terhadap target, sedangkan Brier Score digunakan untuk menilai probabilitas kejadian pada ambang tertentu. Probabilitas kejadian dihitung dari proporsi anggota ensambel yang melampaui ambang curah hujan. Untuk model yang hanya menghasilkan satu prediksi, ensambel diperlakukan sebagai satu anggota; kondisi ini tidak mengukur penyebaran probabilistik.

### 3.9.4 Evaluasi Berbasis Kejadian

Kejadian hujan dievaluasi pada ambang 2, 5, dan 10 mm/jam. Probabilitas kejadian dihitung dari proporsi anggota ensambel yang melebihi ambang tersebut. Suatu kejadian diprediksi terjadi apabila probabilitasnya sekurang-kurangnya 0,5; jika kurang dari 0,5, kejadian dianggap tidak diprediksi. POD, FAR, CSI, dan Brier Score kemudian dihitung dari hasil tersebut.

Ambang klasifikasi hujan/tidak hujan 0,1 mm/jam pada cabang keluaran tambahan digunakan untuk membentuk label pelatihan. Ambang probabilitas 0,5 digunakan khusus untuk mengubah probabilitas ensambel menjadi keputusan kejadian pada evaluasi. Keduanya berbeda dari ambang rain gate 0,6 yang dikalibrasi pada data validation dan digunakan setelah proses sampling model utama.

### 3.9.5 Evaluasi Reliabilitas Probabilitas

Reliability diagram dibuat untuk model utama pada ambang curah hujan 2 mm/jam menggunakan 10 bin probabilitas. Diagram membandingkan probabilitas kejadian hujan yang diperkirakan dengan frekuensi kejadian aktual pada data test ERA5. Hasilnya digunakan untuk menilai apakah probabilitas yang diberikan model sesuai dengan frekuensi kejadian yang diamati; diagram ini tidak mewakili ambang 5 dan 10 mm/jam.

### 3.9.6 Skenario Pengujian

Penelitian ini membandingkan tiga skenario model utama dengan data, target, jendela historis, horizon prediksi, dan protokol evaluasi yang sama untuk menganalisis kontribusi pemodelan sekuensial dan integrasi spasio-temporal probabilistik.

**Rancangan Skenario Pengujian Model**

| No. | Skenario Model | Fokus Perbandingan Metodologis |
| --- | --- | --- |
| 1 | LSTM Multi-Node | Model sekuensial berulang (recurrent baseline) yang menerima masukan multivariat dari seluruh node tanpa mekanisme pemodelan graf dan diffusion |
| 2 | STGNN Deterministik | Model graf spasio-temporal yang menggabungkan GAT dan temporal attention secara mandiri dengan keluaran prediksi titik deterministik |
| 3 | Model Lengkap (RDM-STGNN) | Arsitektur terpadu Retrieval-Augmented Diffusion Model dengan pengondisian graf STGNN dan pembangkitan ensambel probabilistik |

**Tabel 3.16 merangkum tiga konfigurasi model yang diuji. Skenario 1 (LSTM Multi-Node) menjadi representasi model deep learning sekuensial deret waktu konvensional. Skenario 2 (STGNN Deterministik) menguji efektivitas representasi graf spasio-temporal tanpa komponen diffusion dan retrieval. Skenario 3 (Model Lengkap RDM-STGNN) menguji arsitektur terintegrasi yang diusulkan dalam penelitian ini.**

Seluruh skenario dievaluasi pada node MAIN menggunakan tiga target, jendela historis enam jam, prediksi satu jam ke depan, 30 anggota ensambel untuk model probabilistik, dan pengambilan sampel evaluasi setiap jam. Dengan susunan ini, perbedaan hasil dapat diatribusikan secara langsung pada kontribusi arsitektur spasio-temporal dan pemodelan generatif diffusion.

## 3.10 Rancangan Visualisasi Hasil Prediksi Berbasis Web

Visualisasi hasil prediksi dirancang sebagai sarana penyampaian informasi nowcasting yang dapat mendukung interpretasi keluaran model oleh pengguna. Rancangan ini memisahkan proses pemodelan dari proses penyajian hasil: pipeline penelitian menghasilkan artefak prediksi probabilistik, sedangkan aplikasi web menampilkan ringkasan informasi tersebut dalam bentuk yang mudah dipahami. Pengembangan visualisasi berbasis web ditetapkan sebagai arah lanjutan penelitian dan tidak menjadi bagian dari evaluasi kinerja model pada subbab sebelumnya.

Arsitektur yang direncanakan menggunakan FastAPI sebagai backend dan Vue.js sebagai frontend. FastAPI menyediakan endpoint untuk mengakses hasil inferensi. Vue.js merender data tersebut menjadi kartu kondisi cuaca, grafik deret waktu, indikator risiko, dan tabel prediksi. Pemisahan backend dan frontend digunakan untuk menjaga modularitas aplikasi.

![Gambar 3.8 Mockup Dashboard Visualisasi Hasil Nowcasting](media_sp2/image13.png)

Mockup Dashboard Visualisasi Hasil Nowcasting

**Gambar 3.8 menunjukkan rancangan awal dashboard visualisasi hasil nowcasting. Halaman dirancang untuk menampilkan informasi lokasi dan waktu pembaruan, kondisi cuaca terkini, prediksi presipitasi, kecepatan angin, serta kelembapan relatif pada node MAIN. Grafik prediksi digunakan untuk membandingkan perubahan antarwaktu, sedangkan indikator risiko menyajikan interpretasi ringkas terhadap kondisi yang berpotensi membahayakan pendaki. Dengan rancangan tersebut, keluaran probabilistik model tidak hanya tersedia sebagai nilai numerik, tetapi dapat dikomunikasikan sebagai informasi pendukung pengambilan keputusan sebelum dan selama aktivitas pendakian.**

Pada tahap implementasi lanjutan, dashboard perlu memvalidasi respons API, menampilkan status data terakhir, dan membedakan secara jelas antara observasi dengan prediksi. Apabila sumber data near real-time tersedia, FastAPI dapat memperbarui data prediksi secara berkala dan Vue.js menampilkan perubahan tersebut pada antarmuka. Namun, karena penelitian ini menggunakan ERA5 sebagai data reanalysis historis, mockup yang ditampilkan berfungsi sebagai rancangan konseptual visualisasi dan bukan sistem peringatan dini operasional.

# BAB IV
# DAFTAR PUSTAKA

[1]E. Procter, H. Brugger, and M. Burtscher, “Accidental hypothermia in recreational activities in the mountains : A narrative review,” no. August, pp. 2464–2472, 2018, doi: 10.1111/sms.13294.

[2]Aminullah, A. Ayumar, A. Y. Kasma, and E. Samaliwu, “Overview Of Knowledge About First Aid For Hypothermia In Mountain Climbers In Makassar,” vol. XVI, pp. 180–190, 2025.

[3]D. Luciano and D. L. Giovanna, “Rainfall nowcasting model for early warning systems applied to a case over Central Italy,” Nat. Hazards, vol. 112, no. 1, pp. 501–520, 2022, doi: 10.1007/s11069-021-05191-w.

[4]P. Chavula, F. Kayusi, G. Lungu, and A. Uwimbabazi, “The Current Landscape of Early Warning Systems and Traditional Approaches to Disaster Detection,” 2025, doi: 10.62486/latia202577.

[5]M. Reichstein et al., “Early warning of complex climate risk with integrated artificial intelligence,” Nat. Commun., no. May 2024, 2025, doi: 10.1038/s41467-025-57640-w.

[6]S. Ravuri et al., “Skilful precipitation nowcasting using deep generative models of radar,” Nature, vol. 597, no. February, 2021, doi: 10.1038/s41586-021-03854-z.

[7]Y. Zhang, M. Long, K. Chen, L. Xing, and R. Jin, “Skilful nowcasting of extreme precipitation with NowcastNet,” vol. 619, no. September 2022, 2023, doi: 10.1038/s41586-023-06184-4.

[8]A. Mazza, A. Antonini, S. Melani, and A. Ortolani, “A Radar-Based Fast Code for Rainfall Nowcasting over the Tuscany Region,” pp. 1–24, 2025.

[9]A. P. Lakspriyanti, M. Ekayani, and A. Sunkar, “CARRYING CAPACITY ASSESSMENT OF CIBEUREUM WATERFALL TOURISM IN GUNUNG GEDE PANGRANGO NATIONAL PARK,” vol. 25, no. 3, pp. 203–211, 2020, doi: 10.29244/medkon.25.3.203-211.

[10]D. Sun, J. Wu, H. Huang, R. Wang, F. Liang, and H. Xinhua, “Prediction of Short-Time Rainfall Based on Deep Learning,” vol. 2021, 2021, doi: 10.1155/2021/6664413.

[11]Q. Nicolas and W. R. Boos, “Understanding the Spatiotemporal Variability of Tropical Orographic Rainfall Using Convective Plume Buoyancy,” pp. 1737–1757, 2024, doi: 10.1175/JCLI-D-23-0340.1.

[12]C. L. Tsai, G. Lee, K. Kim, H. Park, H. Park, and W. Bang, “Association Between Upstream Conditions and the Intensity of Orographic Precipitation in the Main Mountain Ranges of South Korea,” 2025, doi: 10.1029/2024EA003989.

[13]L. Silva, R. Célleri, and M. Córdova, “Diurnal to seasonal meteorological cycles along an equatorial Andean elevational gradient,” vol. 48, pp. 33–48, 2025.

[14]X. Zhang, M. Xu, S. Kang, H. Wu, and H. Han, “The spatiotemporal variability in precipitation gradients based on meteorological station observations in mountainous areas of Northwest China,” 2023.

[15]Y. Jiang et al., “Characterizing basin-scale precipitation gradients in the Third Pole region using a high-resolution atmospheric simulation-based dataset,” pp. 4587–4601, 2022.

[16]I. Price et al., “Probabilistic weather forecasting with machine learning,” Nature, vol. 637, no. April 2024, pp. 8–11, 2025, doi: 10.1038/s41586-024-08252-9.

[17]X. Zhong et al., “FuXi-ENS : A machine learning model for efficient and accurate ensemble weather prediction,” pp. 1–14, 2025, doi: 10.1126/sciadv.adu2854.

[18]O. A. Wani et al., “Predicting rainfall using machine learning , deep learning , and time series models across an altitudinal gradient in the North-Western Himalayas,” 2024.

[19]L. He et al., “Deep Learning-Based Feature Importance for Rainfall Nowcast Driven by GNSS,” IEEE J. Sel. Top. Appl. Earth Obs. Remote Sens., vol. 18, pp. 26688–26698, 2025, doi: 10.1109/JSTARS.2025.3621857.

[20]H. Kim, S. Yoon, Y. H. Gu, S. H. Kim, and Y. Choi, “A Hybrid Approach to Physical and Deep Learning Models for Radar-Based Precipitation Nowcasting,” IEEE Trans. Geosci. Remote Sens., vol. 63, pp. 1–16, 2025, doi: 10.1109/TGRS.2025.3560454.

[21]Z. Zhang, Q. Song, M. Duan, H. Liu, and J. Huo, “Deep Learning Model for Precipitation Nowcasting Based on Residual and Attention Mechanisms,” pp. 1–17, 2025.

[22]J. H. Meltzer and J. D. Forrester, “Human-Factor Risk Mitigation in Outdoor Climbing Areas : Survey of Existing Policies in Regulated Climbing Areas,” vol. 32, no. 4, 2021, doi: 10.1016/j.wem.2021.08.001.

[23]E. Rahmah, E. K. S. H. Muntasib, and S. B. Rushayati, “Tourism Hazard Mitigation in Mount Rinjani National Park ,” vol. 2, no. 2, pp. 5–19, 2021, doi: 10.22158/sshsr.v2n2p5.

[24]K. Hanly and G. Mcdowell, “The Evolution of ‘ Riskscapes ’: 100 years of climate change and mountaineering activity in the Lake Louise area of the Canadian Rockies,” pp. 1–25, 2023.

[25]A. Asperti, F. Merizzi, A. Paparella, and G. Pedrazzi, “Precipitation nowcasting with generative diffusion models,” Appl. Intell., 2024, doi: https://doi.org/10.1007/s10489-024-06048-y.

[26]U. Yousaf, A. De Rango, G. Mendicino, L. Furnari, D. D. Ambrosio, and A. Senatore, “Spatio-temporal graph neural networks to improve precipitation forecasts from numerical models,” Soft Comput., vol. 29, no. 9, pp. 4481–4494, 2025, doi: 10.1007/s00500-025-10635-7.

[27]J. Liu, L. Yang, H. Li, and S. Hong, “Retrieval-augmented diffusion models for time series forecasting,” no. NeurIPS, pp. 1–15, 2024.

[28]S. Zhao, S. Saha, Z. Xiong, N. Boers, and X. X. Zhu, “Exploring Geometric Deep Learning For Precipitation Nowcasting,” 2023.

[29]W. Li, P. Zhang, H. Dong, Y. Jia, and W. Cao, “RSDF-AM-LSTM : Regional Scale Division Rainfall Forecasting Using Attention and LSTM,” vol. 2, no. 4, 2022.

[30]S. Haji-aghajany, W. Rohm, P. Lipinski, and M. Kryza, “Beyond the horizon : A comprehensive analysis of artificial intelligence-based weather forecasting models,” Eng. Appl. Artif. Intell., vol. 162, no. PA, p. 112335, 2025, doi: 10.1016/j.engappai.2025.112335.

[31]S. P. Ashok and S. Pekkat, “A systematic quantitative review on the performance of some of the recent short-term rainfall forecasting techniques,” J. Water Clim. Chang., vol. 13, no. 8, 2022, doi: 10.2166/wcc.2022.302.

[32]M. Bonavita, “On Some Limitations of Current Machine Learning Weather Prediction Models,” 2024, doi: 10.1029/2023GL107377.

[33]S. Rasp, P. D. Dueben, S. Scher, J. A. Weyn, S. Mouatadid, and N. Thuerey, “WeatherBench: A Benchmark Data Set for Data-Driven Weather Forecasting Journal of Advances in Modeling Earth Systems,” 2020, doi: 10.1029/2020MS002203.

[34]Z. Ben Bouallègue et al., “The Rise of Data-Driven Weather Forecasting: A First Statistical Assessment of Machine Learning–Based Weather Forecasts in an Operational-Like Context,” pp. 864–883, 2024, doi: 10.1175/BAMS-D-23-0162.1.

[35]M. Dumont, M. Saadi, L. Oudin, P. Lachassagne, B. Nugraha, and A. Fadillah, “Assessing rainfall global products reliability for water resource management in a tropical volcanic mountainous catchment,” J. Hydrol. Reg. Stud., vol. 40, no. February, 2022, doi: 10.1016/j.ejrh.2022.101037.

[36]Q. Nicolas and W. R. Boos, “Sensitivity of tropical orographic precipitation to wind speed with implications for future projections,” pp. 231–244, 2025.

[37]E. Yulihastin, T. W. Hadi, N. S. Ningsih, and M. R. Syahputra, “Early morning peaks in the diurnal cycle of precipitation over the northern coast of West Java and possible influencing factors,” pp. 231–242, 2020.

[38]D. Hendrycks and K. Gimpel, “Gaussian Error Linear Units (GELUs),” pp. 1–10, 2016.

[39]J. Ho, A. Jain, and P. Abbeel, “Denoising Diffusion Probabilistic Models,” vol. 256, 2020.

[40]S. Elfwing, E. Uchibe, and K. Doya, “Sigmoid-weighted linear units for neural network function approximation in reinforcement learning,” Neural Networks, vol. 107, pp. 3–11, 2018, doi: 10.1016/j.neunet.2017.12.012.

[41]S. Wagner-carena, A. Akhmetzhanova, and S. Erickson, “A Data-Driven Prism : Multi-View Source Separation with Diffusion Model Priors,” no. NeurIPS, 2025.

[42]X. Li, Y. Dai, and Q. Qu, “Understanding Generalizability of Diffusion Models Requires Rethinking the Hidden Gaussian Structure,” no. NeurIPS, pp. 1–33, 2024.

[43]A. Verdone, S. Scardapane, and M. Panella, “Explainable Spatio-Temporal Graph Neural Networks for multi-site photovoltaic energy production,” Appl. Energy, vol. 353, no. PB, p. 122151, 2024, doi: 10.1016/j.apenergy.2023.122151.

[44]P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, and Y. Bengio, “Graph Attention Network,” pp. 1–12, 2018.

[45]M. Mukhaninga, C. Sigauke, and T. Ravele, “Comparative Performance of LSTM , ANN , and GAM in Predicting Precipitation and Temperature Anomalies Under Accelerated Warming : Evidence from Thohoyandou , South Africa (1990–2025),” 2026.

[46]G. Ayzel and M. Heistermann, “Brief communication : Training of AI-based nowcasting models for rainfall early warning should take into account user requirements,” pp. 41–47, 2025.

[47]F. A. F. Sofi’ie and A. Qoiriah, “Analisis Perbandingan Framework Front-End Javascript React dan Vue Pada Pengembangan Website Analisis Kebutuhan Pembuatan Sistem Pengumpulan Data Analisa Data,” vol. 05, pp. 157–164, 2023.

[48]J. Chen, “Application Technology of Atmospheric Dispersion Models Based on FastAPI + Vue,” vol. 6, no. 11, pp. 120–126, 2023, doi: 10.25236/AJETS.2023.061118.

