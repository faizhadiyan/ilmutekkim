# NOTES-2 — Beranda penuh

Sesi 2 selesai mengikuti **cakupan khusus `SESSION-2.md`**: beranda saja. Ringkasan peta sesi di `BRIEF.md` menyebut artikel/video, tetapi instruksi sesi secara eksplisit melarang pengerjaan halaman tersebut. Tidak ada route artikel, video, kamus, halaman statis, atau API yang dibuat pada sesi ini.

## Berkas yang dikerjakan

- `src/app/page.js`: mengganti beranda sementara dengan seluruh `<main>` lama: hero dan enam tautan strip fitur, pengantar dan CTA, chip seri dan pencarian, section video, grid artikel, serta pesan tanpa hasil, dalam urutan sumber.
- `src/data/home.json`: seluruh data kartu dan urutan chip dari beranda lama.
- `src/components/HomeCard.jsx`: komponen server untuk markup kartu artikel/video, tanpa wrapper tambahan.
- `src/components/HomeInteractions.jsx`: komponen klien yang mengembalikan `null`; memasang perilaku non-tema dari `main.js` pada DOM beranda yang dirender server.
- `NOTES-2.md`: catatan sesi ini.

`Header`, `Footer`, `ChatWidget`, layout, kedua CSS, konfigurasi, dependensi, dan `public/` tidak diubah. Tidak ditemukan bug sesi 1 yang menghalangi beranda. Seluruh 296 berkas `_old/` tetap identik menurut SHA-256 sebelum/sesudah pekerjaan.

## Sumber dan skema data

Sumber data aktual adalah markup `_old/index.html`. Aturan pembentukan kartu dan urutannya diperiksa terhadap bagian beranda `_old/tools/build.py` (sekitar baris 1961–2034); generator tersebut **tidak dijalankan**. `_old/assets/js/main.js` dibaca seluruhnya, termasuk filter, strip sentuh, dan pelipatan chip. Script inline beranda hanya berisi inisialisasi tema dan Vercel Insights; keduanya sudah ditangani layout sesi 1.

`home.json` memiliki tiga properti:

- `series`: 29 label filter dalam urutan lama, yaitu `Video` dan 28 seri artikel. Tombol `Semua` tetap menjadi markup statis, sehingga total ada 30 chip sebelum peningkatan mobile.
- `videos`: 32 objek dalam urutan tampil lama.
- `articles`: 61 objek dalam urutan tampil lama.

Field bersama kartu: `slug` (key React), `href` (tautan lama lengkap, termasuk slash), `series` (`data-series`), `searchTitle` (`data-title` persis dari HTML lama), `title`, `image` (path sumber atau `null`), `label` (eyebrow), `excerpt`, dan `date` (tanggal tampilan lama). Video menambahkan `duration` dan `extra`; artikel menambahkan `badge` (`Arsip` atau `null`). `searchTitle` disimpan langsung agar tidak terjadi perubahan hasil normalisasi dari generator Python ke JavaScript.

Judul juga menjadi alt gambar, sesuai sumber. `image: null` menghasilkan `<div class="no-img">ilmutekkim</div>` yang sama. Ada **dua video** dan **tiga artikel** tanpa gambar, serta **dua artikel** berlabel `Arsip`. Kutipan yang terpotong pada 170 karakter dan spasi akhirnya sengaja dipertahankan tanpa penyuntingan. Meta video tetap menambahkan ` · tonton + baca artikelnya`; play badge tetap `▶ <durasi>`.

## Jumlah kartu

Total **93 kartu**: **61 artikel dalam 28 seri** dan **32 video** dalam kelompok filter `Video`. Semua ada di HTML awal. Empat video pertama terlihat; 28 video berikutnya tetap memiliki `v-extra` dan `display:none` seperti sumber. Dengan filter awal `Semua` dan pencarian kosong, ada **65 kartu terlihat**.

| Seri artikel | Jumlah |
| --- | ---: |
| Bedah Proses | 1 |
| Kisah Teknik Kimia | 12 |
| Seri Alat Pabrik | 2 |
| Seri Cheat Sheet Ujian | 14 |
| Seri Control Room | 1 |
| Seri Distilasi | 2 |
| Seri Energi Sawit | 1 |
| Seri Keselamatan Kerja | 1 |
| Seri Keselamatan Proses | 3 |
| Seri Kilang | 1 |
| Seri Mode Operasi | 1 |
| Seri Neraca Massa | 1 |
| Seri Oleokimia | 1 |
| Seri Pabrik Gula | 1 |
| Seri Perawatan Pabrik | 1 |
| Seri Petrokimia | 1 |
| Seri Pigging | 1 |
| Seri Polimer | 1 |
| Seri Proses Pabrik | 2 |
| Seri Pulp Dan Kertas | 1 |
| Seri Pupuk Dan Proses | 1 |
| Seri Refinery Sawit | 1 |
| Seri Roadmap Teknik Kimia | 1 |
| Seri Semen | 1 |
| Seri Steam | 1 |
| Seri Tekanan | 1 |
| Seri Utilitas Pabrik | 4 |
| Teknik Kimia | 2 |
| **Total artikel** | **61** |

## Perilaku yang diport

- Pencarian memakai event `input` langsung, **tanpa debounce**. Kueri hanya menjalani `.toLowerCase().trim()` dan dicocokkan sebagai substring utuh pada `data-title`; tidak ada pemisahan kata, normalisasi diakritik, atau pencarian di kutipan/tanggal/durasi/badge. `data-title` artikel berisi judul + seri; video berisi judul + tag + `video`.
- Seri aktif awal `all`. Klik chip menghapus `active` dari chip lain, mengaktifkan chip tersebut, dan menerapkan kondisi seri **dan** pencarian bersama. Kueri tetap dipertahankan ketika seri berubah.
- Video `v-extra` tersembunyi hanya ketika seri `all` dan kueri kosong. Memilih `Video` dengan kueri kosong menampilkan 32 video. Saat ada kueri, video lama ikut dicari. Menghapus kueri pada `Semua` mengembalikan empat video terbaru.
- Jumlah hasil mengatur `hidden` pesan `#no-result` dan `style.display` section `#video`/`#artikel`. Pesan lama dipertahankan persis: “Tidak ditemukan artikel yang sesuai. Silakan gunakan kata kunci lain.”
- **Tidak ada pemicu `window.TanyaTekkim.open()` dari keadaan nol hasil dalam sumber aktual.** `chat.js` lama hanya mengekspor API tersebut dengan komentar tentang pintu masuk beranda; tidak ada pemanggilan pada `index.html` atau `main.js`. Karena itu tidak ditambahkan tombol, tautan, teks, atau pembukaan chatbot otomatis. API global sesi 1 tetap tersedia.
- Pada perangkat `(hover: none)`, ketukan pertama pada tautan `.tool-strip` mencegah navigasi, menutup deskripsi terbuka lain, dan menambahkan kelas `open`. Ketukan kedua pada tautan yang sudah terbuka mengikuti href. Tidak ada handler tambahan untuk perangkat dengan hover.
- Pada `(max-width: 760px)`, posisi `offsetTop` chip diukur saat efek dipasang. Jika ada lebih dari dua baris, chip setelah baris kedua mendapat `chip-extra`, lalu tombol `.chip.chips-more` disisipkan tepat setelah `.chips`. Label beranda tetap **“Tampilkan semua seri (29) ▾”**; saat dibuka menjadi **“Tutup ▴”**. Kelas `expanded` dan `aria-expanded` mengikuti keadaan. Angka 29 mengecualikan `Semua` dan mencakup `Video`, sama seperti sumber. Jika sudah muat dalam satu/dua baris, tombol tidak dibuat. Pemeriksaan media hanya saat pemasangan, tanpa listener resize, mengikuti skrip lama.
- Filter tidak dijalankan otomatis saat pemasangan, sama seperti sumber. Markup awal sudah menentukan video yang disembunyikan. Pemfilteran hanya mengubah atribut keadaan yang juga diubah skrip lama, tanpa mengganti isi atau struktur kartu.

## Metadata dan perbedaan implementasi

Metadata beranda diwarisi langsung dari layout sesi 1. Tidak ada deklarasi metadata baru atau tag head tambahan. `title.default` layout menghasilkan judul lengkap beranda tanpa menerapkan suffix template terhadap judul itu sendiri. Title, description, OG type/title/description/url, dan canonical telah dibandingkan dengan head lama. Canonical tetap **`https://ilmutekkim.vercel.app/`**, sesuai sumber.

Perbedaan implementasi terbatas pada pemisahan data JSON, komponen server, dan pemasangan handler melalui `useEffect`. Selektor perilaku dibatasi ke `<main>` beranda. Listener, atribut keadaan, dan tombol mobile dibersihkan saat komponen dilepas agar pemasangan ulang efek pada development React tidak menggandakan handler atau tombol. Script `main.js` lama tidak dimuat ulang dan toggle tema tidak digandakan.

Tidak ada perubahan copy, nama kelas, tautan, path aset, atau struktur elemen `<main>`. Serialisasi React dapat berbeda pada whitespace pemformatan, entitas HTML, penutup elemen void, atribut boolean, dan titik koma style; DOM dan teks tampilannya sama. Tidak ada CSS atau aset biner baru.

## Pemeriksaan

- Menggunakan dependensi yang **sudah tersedia sebelum sesi ini**, Babel bawaan Next memeriksa JSX/impor lokal, lalu `react-dom/server` merender beranda ke HTML sementara. Ini bukan build Next dan tidak memakai hasil `.next` lama.
- Seluruh DOM `<main>` hasil render dibandingkan dengan sumber menggunakan parser HTML: elemen, hierarki, urutan, atribut, kelas, href, gambar, dan teks cocok setelah normalisasi whitespace pemformatan. Teks seluruh **93 kartu**, termasuk spasi akhir kutipan, juga dibandingkan persis tanpa normalisasi.
- Metadata layout dibandingkan langsung dengan title, description, OG, dan canonical lama; tidak ada override metadata beranda.
- Harness menjalankan `main.js` lama dan efek React baru terhadap simulasi DOM yang sama: **34.650 perbandingan keadaan lulus**, meliputi **190 kueri × 30 filter × 6 skenario perangkat/layout** (desktop, mobile sentuh dengan >2 baris, mobile satu baris, mobile dua baris, sentuh pada lebar desktop, dan tanpa `matchMedia`). Termasuk setiap judul kartu, kata kunci nyata, kapitalisasi/spasi, pencarian kosong/tanpa hasil, semua kombinasi seri, empat/32 video, section kosong, nol pemanggilan chatbot, ketukan pertama/kedua, buka/tutup chip, pembersihan listener/atribut/tombol, dan pemasangan ulang efek. Posisi chip disimulasikan; ini bukan pengukuran layout browser nyata.
- SHA-256 membuktikan seluruh **296 berkas** `_old/` tidak berubah. Dari berkas yang sudah ada sebelum sesi, hanya `src/app/page.js` berubah; empat berkas lain dalam daftar pekerjaan adalah tambahan sesi ini.
- Harness sementara berada di `/tmp/ilmutekkim-session-2-*`, tidak menambah dependensi atau berkas pengujian proyek.
- **Tidak menjalankan `npm install`, `npm run build`, atau perintah instalasi/build pengganti.** `node_modules`, `package-lock.json`, dan `.next` sudah ada ketika sesi dimulai; keberadaannya bukan hasil pekerjaan sesi ini.

## Risiko dan serah terima sesi berikutnya

1. Operator masih perlu memverifikasi build/SSG Next, hidrasi nyata, dan tampilan browser desktop/mobile. Pemeriksaan DOM dan simulasi media/posisi chip tidak menggantikan screenshot atau pengukuran layout browser dengan font asli. Periksa khusus dua baris chip, tombol pembuka, ketukan strip fitur, kombinasi pencarian/seri, dan perubahan tema sebelum hidrasi.
2. Aset biner tetap menjadi tanggung jawab operator di `public/assets/`. Lima placeholder tanpa gambar adalah keadaan sumber yang sengaja dipertahankan. `public/` pada akhir sesi tetap hanya `.gitkeep`.
3. Halaman artikel dan video **belum dibuat**, sesuai larangan sesi ini. Tautan tetap menunjuk URL lama dan menunggu sesi yang dialokasikan untuk port halaman tersebut. Ada ketidaksesuaian dengan peta master yang mencantumkan artikel/video pada Sesi 2; cakupan eksplisit `SESSION-2.md` menjadi acuan pekerjaan ini. Jangan menganggap halaman tujuan kartu sudah tersedia.
4. Sesi 3 tetap perlu membuat kamus dan halaman statis yang dijadwalkan. `public/kamus/search-index.json` serta tautan istilah menunggu sesi kamus. Jangan menimpa CSS global atau memuat ulang `main.js` untuk mengaktifkan beranda; perilakunya kini hanya terpasang pada beranda.
5. `/api/ask`, sitemap, dan robots menunggu sesi 4. Hero, strip fitur, dan kartu tetap memuat jumlah, teks, dan URL sumber, meskipun beberapa tujuan belum diport. Href berakhiran slash dipertahankan sementara konfigurasi `trailingSlash: false` tetap berlaku.

Tidak ada pertanyaan yang menghalangi penyelesaian cakupan beranda Sesi 2.
