# BRIEF MASTER — Migrasi ilmutekkim.site ke Next.js

## Tujuan
Migrasi PENUH situs ilmutekkim.site dari HTML statis (generator Python) ke **Next.js (App Router, JavaScript, SSG)** dengan paritas tampilan & isi 100%. BUKAN redesign. TIDAK ADA perubahan teks/copy sama sekali.

## Sumber kebenaran
Folder `_old/` di workspace ini = salinan lengkap situs lama (HTML, CSS, JS, JSON data, api, tools). Semua markup, kelas CSS, teks, dan perilaku diambil dari sana persis. `tools/build.py` dan `tools/build_kamus.py` adalah spesifikasi rendering lama — baca kalau struktur halaman tidak jelas dari HTML jadinya.

## Aturan keras
1. **URL identik** dengan situs lama (daftar di `_old/sitemap.xml`). `trailingSlash: false`. Tidak ada URL baru/berubah/hilang.
2. **CSS global = port verbatim** `_old/assets/css/style.css`. Nama kelas TIDAK diganti. DILARANG Tailwind / CSS Modules / styled-components. Satu-satunya CSS: globals.css (dari style.css), chat.css (dari `_old/kamus/assets/chat.css`), kamus.css (dari `_old/kamus/assets/kamus.css`, sesi kamus).
3. **Tema**: atribut `data-theme` di `<html>`, localStorage key `ilm-theme`, script init inline yang sama persis seperti di head `_old/index.html` (jalan sebelum CSS, anti kedip).
4. **Font**: link Google Fonts yang sama (Archivo + Plus Jakarta Sans).
5. **Aset**: semua path `/assets/...` TIDAK berubah. File binernya ditempatkan operator di `public/assets/`. Jangan menyalin biner, jangan mengubah path.
6. **Chatbot "Tanya Tekkim"**: port setia `_old/kamus/assets/chat.js` + `chat.css`: perilaku, urutan DOM, kelas, label sumber, alur data (pencarian glosarium di klien dulu, lalu POST `/api/ask`) semua sama. Muncul di SEMUA halaman.
7. **API `/api/ask`**: logika identik `_old/api/ask.js` (router heuristik Gemini/DeepSeek + fallback dua arah + rate limit). Diport apa adanya di sesi 4.
8. **Bahasa**: JavaScript saja (BUKAN TypeScript). Dependensi HANYA: next, react, react-dom.
9. **Semua halaman SSG** (static generation). Metadata tiap halaman (title, description, OG, canonical) disalin persis dari HTML lama.
10. **DILARANG**: mengubah teks/copy, mengganti nama kelas, menambah library, menyentuh `_old/`.
11. Setiap sesi menulis `NOTES-<n>.md`: yang dibangun, keputusan, pertanyaan terbuka/risiko untuk sesi berikut.
12. JANGAN menjalankan `npm install` / `npm run build` — operator yang menjalankan dan memverifikasi.

## Sumber data (di `_old/`)
- `deep/*.json` — artikel pendalaman (lead, sections, facts, refs, closing)
- `glosarium.json`, `jalur.json` — data jalur & glosarium/kamus
- `kamus-data/terms.json` + `sectors.json` — katalog kamus (48 istilah, 3 sektor)
- `research/`, `paten/` — data riset & paten (dirender build.py jadi halaman /riset)
- `artikel/<slug>/`, `video/` — halaman jadi; model kontennya di `tools/build.py`
- `kamus/` — halaman kamus jadi; modelnya di `tools/build_kamus.py`

## Peta sesi
- Sesi 1: scaffold + layout + Header/Footer + globals.css + ChatWidget
- Sesi 2: beranda (search/filter/cards) + halaman artikel & video
- Sesi 3: kamus + halaman statis (riset, jalur, tentang, kalkulator, referensi, redirect glosarium)
- Sesi 4: route /api/ask + wiring final + sitemap/robots
