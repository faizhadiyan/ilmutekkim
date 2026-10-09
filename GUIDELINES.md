# Guidelines Website ilmutekkim

Situs: https://ilmutekkim.vercel.app · Generator: `tools/build.py` · Repo: faizhadiyan/ilmutekkim

## Halaman video = artikel versi baca

<!-- R:ILM-R63 -->

Halaman detail video motion graphics (`/video/<slug>/`) WAJIB berbentuk artikel versi baca untuk pembaca umum: judul, lead, video tertanam, isi prose per subtopik yang judulnya menyebut isi subtopik itu, fakta kunci, kesimpulan, kuis, dan link ke Reel aslinya.

DILARANG menampilkan bahasa dapur produksi ke pembaca, dalam bentuk apa pun: label struktur narasi (HOOK, TENSION, PAYOFF, TAKEAWAY, PROSES, dan sejenisnya), daftar bedah per scene, kutipan teks layar per scene, deskripsi visual, tujuan narasi, dan catatan apa yang perlu diperhatikan per scene. Semua itu artefak brief produksi, bukan isi untuk pembaca.

Navigasi waktu tetap wajib tersedia dalam bentuk yang masuk akal buat pembaca: tombol lompat (▶ m:ss) pada judul subtopik artikel yang membawa pemutar ke awal subtopik itu. Judul subtopik menyebut isi subtopiknya (mis. "Saprolit lewat jalur panas RKEF"), bukan peran naratifnya.

Berlaku untuk semua video yang digenerate `tools/build.py` tanpa kecuali, termasuk video yang ditambahkan belakangan: isi artikel per video (judul subtopik + prose penjelasan) wajib ditulis sebagai konten pembaca. Materi sumber boleh dari brief produksi, tapi wajib ditulis ulang sebagai prose penjelasan, bukan disalin dari field struktur produksi (role, on_screen, visual, purpose, watch).
