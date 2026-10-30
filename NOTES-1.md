# NOTES-1 — Scaffold dan kerangka

Sesi 1 selesai sesuai `BRIEF.md` dan `SESSION-1.md`. Beranda penuh, artikel, video, kamus, halaman statis lain, API, sitemap, dan robots belum dikerjakan.

## Struktur proyek

Memakai App Router dengan direktori `src/`, JavaScript/JSX, dan alias `@/*` → `./src/*` di `jsconfig.json`.

```text
package.json
next.config.mjs
jsconfig.json
.gitignore
public/
  .gitkeep
src/
  app/
    layout.js
    globals.css
    chat.css
    page.js
    not-found.js
  components/
    Header.jsx
    Footer.jsx
    ChatWidget.jsx
```

- Nama paket `ilmutekkim-web`; skrip `dev`, `build`, dan `start` memakai perintah Next standar. Dependensi hanya `next`, `react`, dan `react-dom`.
- Next dipatok ke `15.5.28`, rilis stabil terbaru seri 15 yang ditemukan saat sesi ini. Sumber: [pengumuman resmi Next.js, 14 Oktober 2026](https://nextjs.org/blog/nextjs-security-update-october-14-2026). React dan React DOM memakai rentang `^19.0.0` yang sama.
- `next.config.mjs` menetapkan `trailingSlash: false`. Belum ada konfigurasi static export; halaman menggunakan SSG bawaan App Router tanpa API dinamis di server.
- `public/` hanya berisi `.gitkeep`. Tidak ada aset biner atau JSON yang disalin. Seluruh path aset lama tetap menjadi acuan untuk sesi berikutnya dan operator.
- `globals.css` identik byte demi byte dengan `_old/assets/css/style.css`, termasuk komentar. `chat.css` identik byte demi byte dengan `_old/kamus/assets/chat.css`. Keduanya diimpor dari layout; tidak ada CSS tambahan.

## Layout, header, footer, dan halaman sementara

Layout **tidak menambahkan `<main>`**. Keputusan berdasarkan pemeriksaan beranda, artikel, tentang, riset, dan kamus: beranda memakai `<main>` dengan section, artikel/tentang/riset memakai `<main>` dengan artikel `.post` yang lebarnya berbeda, sedangkan kamus memakai `<div class="wrap">` tanpa `<main>`. Tiap halaman berikutnya harus mempertahankan pembungkusnya sendiri.

Urutan body: `Header`, konten halaman, `Footer`, lalu `ChatWidget`. Beranda sementara hanya memakai struktur lama `main > section.hero > div.hero-grid` dan judul asli “Teknik kimia, ditelaah dari prosesnya.” Halaman 404 memakai kelas `.post.narrow`, angka `404`, dan tautan berlabel lama “Beranda”; header/footer/chat diwarisi dari layout.

Script inisialisasi tema disalin persis sebagai string dan dikeluarkan lewat `<script dangerouslySetInnerHTML>` sinkron di awal `<head>`, sebelum font dan konten body. Script membaca `ilm-theme`, mengikuti preferensi sistem jika belum ada pilihan, dan memakai tema terang jika penyimpanan gagal. `<html lang="id" suppressHydrationWarning>` mengakomodasi perubahan atribut `data-theme` sebelum hidrasi.

Link Google Fonts (Archivo dan Plus Jakarta Sans), preconnect, favicon data URI, serta dua script Vercel Insights mengikuti head beranda lama tanpa paket tambahan. Metadata default mempertahankan judul, description, OG type/title/description/url, dan canonical `https://ilmutekkim.vercel.app/` dari `_old/index.html`. Template judul: `%s | ilmutekkim`. Untuk menyalin judul lengkap halaman lama pada sesi berikutnya, gunakan `title: { absolute: judulLama }` agar suffix tidak ditambahkan dua kali; salin canonical dan OG masing-masing halaman juga.

Header dan footer mempertahankan urutan elemen, nama kelas, teks, atribut, serta href dari `_old/index.html`. Href lama seperti `/riset/`, `/jalur/`, dan tautan footer berakhiran slash dipertahankan; konfigurasi Next tetap `trailingSlash: false` sesuai brief. Tombol tema berada setelah `</nav>` dan memakai logika toggle dari `main.js`, termasuk penanganan kegagalan localStorage. Burger tetap menggunakan pasangan checkbox `#nav-toggle` dan label `.burger` beserta selector CSS lama; sumber lama tidak memiliki handler burger JavaScript tersendiri.

## Port ChatWidget

Seluruh `_old/kamus/assets/chat.js` dibaca sebelum port. Komponen klien React mempertahankan:

- Tombol `#tt-btn`, panel dialog `#tt-panel`, header/tombol tutup, pemilih level, daftar pesan, chip saran, dan form dalam urutan DOM lama. ID, kelas, label, placeholder, tiga pertanyaan saran, serta batas input 500 karakter tetap sama. Panel, riwayat pesan, dan level bertahan ketika ditutup/dibuka.
- Level awal `awam`; pilihan lain `tekkim` dan `plant`. Pesan sambutan baru ditambahkan ketika panel pertama kali dibuka. `window.TanyaTekkim.open()` tetap tersedia untuk pintu masuk dari keadaan nol hasil pada beranda sesi 2. API global dibersihkan saat komponen dilepas.
- Pencarian lokal lebih dahulu dengan `GET /kamus/search-index.json`, memakai objek `{ terms: [...] }`. Hasil JSON dicache selama komponen aktif. Fetch/JSON gagal dicache sebagai `{ terms: [] }`, sesuai sumber, lalu pertanyaan diteruskan ke AI.
- Normalisasi huruf kecil, NFD, dan penghapusan diakritik. Skor persis: nama identik **100**, nama terkandung dalam pertanyaan atau potongan pertanyaan minimal 4 karakter dalam nama **85**, alias minimal 3 karakter terkandung dalam pertanyaan **88**, seluruh kata judul dengan panjang minimal 5 karakter ditemukan **70**. Ambang kecocokan **70**; skor tertinggi dipilih, dan kandidat pertama menang saat skor sama.
- Jawaban entri dasar berisi definisi, pemberitahuan pendalaman menyusul, label `Sumber: Glosarium terverifikasi · Entri dasar`, dan tautan `/kamus/istilah/<slug>/`. Entri dalam memakai definisi/analogi pada Awam, mekanisme/prinsip pada Tekkim, serta biaya/checklist diagnosis pada Plant, dengan label `Sumber: Glosarium terverifikasi` dan tautan yang sama.
- Jika tidak cocok, `POST /api/ask` dengan header `Content-Type: application/json` dan payload `{ question: q, level: level }`, tanpa riwayat percakapan. Respons sukses memakai `answer` dan opsional `model`; label persis `AI — belum terverifikasi · <model>` atau tanpa suffix jika model tidak tersedia. Baris baru jawaban menjadi `<br>`, dengan escaping teks yang sama seperti sumber.
- Pesan tunggu, tombol Kirim nonaktif selama proses, cabang `ai_not_configured`, `rate_limited`, kegagalan umum, serta kegagalan koneksi/JSON memakai teks lama. Pengguliran mengikuti penambahan pesan dan penyelesaian permintaan AI. Perubahan level saat indeks masih dimuat dibaca melalui ref sehingga level yang dipakai mengikuti perilaku variabel sumber lama.

State React mengelola panel, input, level, riwayat, dan pembaruan pesan tunggu. HTML jawaban memakai formatter lama yang melakukan escaping sebelum dimasukkan ke pesan; tidak ada wrapper tambahan di dalam pesan. Script `main.js` dan `chat.js` lama tidak dimuat lagi, sehingga tidak ada handler atau widget ganda.

## Pemeriksaan yang sudah dijalankan

- Perbandingan byte kedua CSS: identik. SHA-256 seluruh **296 file** di `_old/` dibandingkan sebelum/sesudah pekerjaan: tidak berubah.
- Perbandingan struktur HTML header/footer dengan sumber (mengabaikan whitespace): elemen, atribut, teks, kelas, serta semua href cocok. Urutan ID chat, impor lokal, cakupan route/CSS, dependensi, alias, dan isi `public/` diperiksa.
- Impor `next.config.mjs` dengan Node berhasil; `trailingSlash` terverifikasi `false`.
- Metadata default dan favicon dibandingkan langsung dengan head lama. Script tema diuji pada lima skenario pilihan tersimpan/preferensi sistem/penyimpanan gagal; toggle tema diuji pada empat skenario, termasuk penyimpanan gagal.
- Harness Node sementara membandingkan formatter, pencarian, state, dan alur async komponen dengan eksekusi `chat.js` lama melalui simulasi DOM/hooks: **48 istilah × 3 level**, **177 kueri data nyata**, **7 kasus batas pencocokan**, **9 skenario AI/galat**, cache indeks termasuk fallback kegagalan, pertanyaan kosong, escaping, pesan sambutan, status Kirim, dan perubahan level saat loading. Hasil cocok. Harness ada di `/tmp/ilmutekkim-session-1-check.cjs`, bukan dependensi atau berkas proyek.
- **Tidak menjalankan `npm install`, `npm run build`, atau perintah instalasi/build pengganti.** Tidak ada `node_modules`, `.next`, maupun lockfile yang dibuat. Pemeriksaan ini belum mencakup kompilasi JSX oleh Next, hidrasi React nyata, screenshot, atau uji browser.

## Catatan untuk sesi berikutnya/operator

1. Sesi 2 mengisi beranda penuh beserta filter/pencarian/kartu, halaman artikel, dan video. Pertahankan struktur `<main>` per halaman dan seluruh copy, kelas, metadata, serta URL sumber. Port perilaku beranda dari `main.js` pada sesi itu; jangan memuat ulang bagian toggle tema lama.
2. `public/kamus/search-index.json` belum tersedia karena sesi ini mensyaratkan `public/` hanya placeholder. Sesi kamus perlu menyediakan JSON lama secara utuh di path tersebut, termasuk 48 entri. Sampai tersedia, widget mengikuti cabang indeks gagal dan mencoba API. Tautan sitasi juga menunggu halaman kamus sesi 3.
3. `/api/ask` sengaja belum dibuat; router model, fallback dua arah, dan rate limit server menunggu sesi 4. Uji sesi ini memakai respons simulasi, bukan layanan AI asli.
4. Operator menempatkan aset biner ke `public/assets/`, memasang dependensi, dan memverifikasi build/SSG serta browser. Periksa tema sebelum tampilan pertama/hidrasi, burger pada lebar mobile, chat pada desktop/mobile, dan label model setelah API tersedia. Periksa pula perilaku redirect slash yang dihasilkan konfigurasi Next terhadap href sumber yang tetap dipertahankan.
5. Domain canonical homepage sengaja tetap `ilmutekkim.vercel.app` sesuai sumber dan instruksi, meskipun brief menyebut `ilmutekkim.site`. Jangan menyeragamkan canonical halaman lama tanpa instruksi; salin per halaman pada sesi berikutnya.

Tidak ada pertanyaan yang menghalangi penyelesaian Sesi 1. Verifikasi runtime dan ketergantungan lintas sesi di atas masih menunggu tahap/operator yang telah ditentukan.
