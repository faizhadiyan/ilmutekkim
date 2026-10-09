# Guidelines Website ilmutekkim

Situs: https://ilmutekkim.vercel.app · Generator: `tools/build.py` · Repo: faizhadiyan/ilmutekkim

## Halaman video = artikel versi baca

<!-- R:ILM-R63 -->

Halaman detail video motion graphics (`/video/<slug>/`) WAJIB berbentuk artikel versi baca untuk pembaca umum: judul, lead, video tertanam, isi prose per subtopik yang judulnya menyebut isi subtopik itu, fakta kunci, kesimpulan, kuis, dan link ke Reel aslinya.

DILARANG menampilkan bahasa dapur produksi ke pembaca, dalam bentuk apa pun: label struktur narasi (HOOK, TENSION, PAYOFF, TAKEAWAY, PROSES, dan sejenisnya), daftar bedah per scene, kutipan teks layar per scene, deskripsi visual, tujuan narasi, dan catatan apa yang perlu diperhatikan per scene. Semua itu artefak brief produksi, bukan isi untuk pembaca.

Navigasi waktu tetap wajib tersedia dalam bentuk yang masuk akal buat pembaca: tombol lompat (▶ m:ss) pada judul subtopik artikel yang membawa pemutar ke awal subtopik itu. Judul subtopik menyebut isi subtopiknya (mis. "Saprolit lewat jalur panas RKEF"), bukan peran naratifnya.

Berlaku untuk semua video yang digenerate `tools/build.py` tanpa kecuali, termasuk video yang ditambahkan belakangan: isi artikel per video (judul subtopik + prose penjelasan) wajib ditulis sebagai konten pembaca. Materi sumber boleh dari brief produksi, tapi wajib ditulis ulang sebagai prose penjelasan, bukan disalin dari field struktur produksi (role, on_screen, visual, purpose, watch).

## Standar artikel: mendalam, kitab suci, dengan sitasi

<!-- R:ILM-R64 -->

Semua halaman artikel di website (dari carousel maupun video) WAJIB memenuhi standar ini:

1. DILARANG membahas teknologi atau cara produksi konten di halaman pembaca (nama tool, format render, jumlah scene, ada tidaknya voice-over, dan sejenisnya). Pembaca datang untuk teknik kimianya, bukan dapur produksinya.
2. Pembuka adalah hook tertulis mengikuti kitab suci konten (HTPC sebagai craft: hook yang menahan jawaban, tegangan, payoff dermawan, penutup beralasan). Label strukturnya DILARANG ditampilkan; yang tampil hanya tulisan yang bekerja.
3. Isi membedah sangat mendalam dan akademis: prinsip dasar, mekanisme, persamaan yang relevan, angka terverifikasi, alasan pilihan desain, kesalahan umum, dan konteks industri.
4. Klaim kunci dirujuk dengan sitasi bernomor [n] ke daftar Referensi di akhir artikel. Referensi wajib literatur nyata (buku teks, standar, ensiklopedia industri). DILARANG mengarang nomor halaman, DOI, atau volume.
5. Angka hanya dari sumber terverifikasi (spec carousel, brief video, artikel yang sudah lolos QC). DILARANG mengarang angka, kapasitas, atau kejadian baru saat memperdalam artikel.

## Standar bedah riset (page research)

<!-- R:ILM-R65 -->

Halaman riset berisi bedah paper jurnal dengan standar QC tertinggi di situs ini (perintah Hadi 2026-10-09):

1. CAKUPAN JUJUR: bedah ditulis hanya dari abstrak yang terverifikasi dari sumber bibliografis (OpenAlex/Crossref) dan WAJIB dilabeli "Berdasarkan abstrak". Dilarang mengklaim membaca full text bila belum dibaca.
2. ANGKA: setiap angka di badan bedah WAJIB persis tertulis di abstrak sumbernya. Angka hasil hitungan sendiri DILARANG, kecuali ditandai eksplisit sebagai hitungan turunan beserta dasarnya.
3. PARAFRASE: abstrak DILARANG disalin utuh atau nyaris utuh; bedah ditulis dengan kata sendiri. Sitasi lengkap (penulis, tahun, jurnal) dan tautan DOI wajib ada.
4. APRESIASI KRITIS: setiap bedah wajib memuat batas/catatan kritis (skala penelitian, keterbatasan klaim abstrak) dan kesimpulan akhir eksplisit yang berbunyi persis "Baca full paper-nya" atau "Cukup baca abstraknya". Kesimpulan tanpa dasar yang dinyatakan di teks dilarang.
5. GATE MEKANIS: `tools/qc_research.py` memeriksa setiap bedah sebelum build (angka subset dari abstrak, kemiripan teks dengan abstrak, kelengkapan field, format DOI). Build GAGAL bila satu bedah pun tidak lolos; tidak ada bedah yang tayang tanpa lolos gate. Sumber wajib campuran jurnal internasional dan jurnal Indonesia.

## Standar bedah paten (rak paten page research)

<!-- R:ILM-R66 -->

Bedah paten di halaman riset mengikuti integritas yang sama dengan bedah jurnal, disesuaikan sifat dokumennya:

1. SUMBER PRIMER: nomor paten, judul, inventor, pemilik, tanggal pengajuan, dan tanggal terbit WAJIB diverifikasi dari dokumen paten publik (Google Patents atau PDF paten), bukan dari ingatan atau artikel sekunder. Tautan sumber wajib tampil di halaman.
2. KLAIM DIPARAFRASE: klaim paten adalah teks hukum; bedah WAJIB memparafrase klaim inti dengan kata sendiri. Dilarang menyalin klaim verbatim melebihi frasa teknis pendek.
3. STATUS HUKUM HATI-HATI: status ditulis sebagai fakta dokumen (mis. "Expired - Fee Related per Google Patents, diakses <tanggal>") dengan sumber dan tanggal aksesnya. Dilarang menyimpulkan kebebasan pakai sebagai nasihat hukum; paten kedaluwarsa disebut dokumen publik yang dapat dipelajari.
4. ANGKA: setiap angka di badan bedah WAJIB ada di teks sumber terverifikasi yang disimpan (src_text). Gate mekanis `tools/qc_patent.py` wajib lolos sebelum build; build GAGAL bila satu bedah paten pun tidak lolos.

## Standar jalur belajar, glosarium, dan referensi gabungan

<!-- R:ILM-R67 -->

1. RESOLVE ATAU GAGAL: setiap langkah jalur, istilah glosarium, dan entri referensi yang menautkan konten situs WAJIB menunjuk slug artikel/video/bedah yang benar-benar ada; generator memeriksa ini dan build GAGAL bila ada slug tidak dikenal.
2. GLOSARIUM: definisi ditulis redaksi dalam bahasa polos dan tepat secara teknis; dilarang memuat angka yang tidak ada di artikel terkaitnya. Setiap istilah menautkan minimal satu bacaan lanjutan di situs.
3. REFERENSI GABUNGAN: halaman ini adalah AGREGASI sitasi yang sudah tampil di artikel dan bedah situs; dilarang menambah sitasi baru di halaman ini.
4. JALUR BELAJAR: urutan langkah adalah keputusan editorial yang dinyatakan eksplisit di data (bukan urutan tanggal); setiap langkah punya catatan satu kalimat tentang posisinya di jalur.

## Standar kalkulator interaktif

<!-- R:ILM-R68 -->

1. RUMUS STANDAR: kalkulator hanya menghitung persamaan standar teknik kimia yang juga dipakai artikel situs (Carothers, LMTD, McCabe-Thiele biner volatilitas relatif konstan, konversi satuan). Dilarang menambah konstanta atau korelasi karangan.
2. ASUMSI EKSPLISIT: setiap kalkulator menulis asumsinya di halaman (mis. volatilitas relatif konstan, kondensor total); hasil di luar asumsi harus dinyatakan sebagai pendekatan.
3. TAUTAN BALIK: setiap kalkulator menautkan artikel penjelas konsepnya di situs.
4. UJI OTOMATIS: fungsi hitung murni di aset JS WAJIB lolos uji kasus acuan yang dapat diverifikasi tangan (node test) sebelum build; build tidak perlu gagal, tetapi uji adalah gate rilis halaman ini.

## Standar editorial: diksi akademis dan profesional

<!-- R:ILM-R69 -->

Seluruh teks yang dibaca pengunjung situs ilmutekkim WAJIB memakai diksi akademis dan profesional: bahasa Indonesia baku (EYD/KBBI), kalimat lengkap, istilah teknis yang tepat, dan nada penulis ahli yang menulis untuk sejawat profesional dan peneliti. Dilarang: kata jalanan atau percakapan (mis. "kok", "gimana", "banget", "asik", "ngerti", "bakal", "nggak", "deh", "sih", "dong", "nih", "tuh", "biar"), pertanyaan retoris bernada jalanan, sapaan orang kedua informal, serta seruan promosi. Pembuka artikel tetap wajib mengait perhatian (prinsip kitab suci diterapkan sebagai kerajinan tulisan), tetapi kaitannya berbentuk pertanyaan analitis, ketegangan konsep, atau jurang antara praktik dan teori yang dirumuskan secara formal. Angka, satuan, sitasi bernomor, dan daftar referensi dalam artikel tidak boleh diubah saat penulisan ulang editorial; untuk bedah riset dan paten berlaku tambahan aturan ILM-R65/ILM-R66 (angka tetap subset dari sumber dan kesimpulan akhir tetap persis seperti yang ditetapkan). Aturan ini berlaku untuk seluruh badan artikel, bedah, glosarium, jalur, dan teks antarmuka (judul seksi, tombol, footer, meta).
