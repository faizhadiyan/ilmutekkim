# NOTES-9 — Perbaikan mikro spasi Kamus

Sesi 9 selesai sesuai `SESSION-9.md`, dengan acuan `BRIEF.md`, `NOTES-4.md`, dan HTML padanan di `_old/kamus/`. Perubahan kode hanya tiga baris pada tiga berkas Kamus berikut.

## Pola yang diperbaiki

| Berkas | Pola dan hasil |
| --- | --- |
| `src/components/KamusTermCard.jsx` | Awalan fondasi, cuplikan definisi, dan elipsis `…` digabung dalam satu template literal. Elipsis melekat pada hasil pemotongan, misalnya `cairan yan…`. Berlaku bersama untuk kartu populer, katalog A–Z, bagian fondasi, dan ketiga sektor; mencakup entri dalam maupun dasar. |
| `src/app/kamus/page.js` | Seluruh judul hitungan dirangkai dalam satu template literal: `Semua Istilah A–Z (48)`. Tidak ada batas ekspresi JSX di antara kurung dan angka. |
| `src/app/kamus/sektor/[slug]/page.js` | Seluruh judul hitungan sektor dirangkai dalam satu template literal: `Istilah pada Sektor Ini (14)` untuk oleokimia/kilang-migas dan `(15)` untuk petrokimia. |

Panjang pemotongan tetap 130 code point untuk entri dalam dan 150 untuk entri dasar, melalui fungsi `excerpt` yang tidak diubah. Spasi asli dalam definisi, termasuk bila pemotongan tepat mengenai spasi, tetap mengikuti HTML lama; tidak memakai `trim()` atau penghapusan spasi menyeluruh.

## Pola yang diperiksa dan sudah benar

Audit mencakup seluruh enam `src/components/Kamus*.jsx` dan seluruh berkas JavaScript di `src/app/kamus/**`. Layout dan CSS hanya dibaca, tidak diubah.

- `KamusSearch.jsx`: hasil pencarian sudah memakai konkatenasi string untuk cuplikan + `…`, sesuai `_old/kamus/assets/search.js`. Spasi sebelum label `Entri dasar` juga sesuai sumber. Tidak perlu perubahan.
- `src/app/kamus/page.js`: hitungan lead `48 istilah tersedia: 20 entri dalam dan 28 entri dasar.`, label sektor `N istilah terkait`, dan spasi antara nama fondasi dengan angka dalam `<b>` sesuai HTML lama. Placeholder pencarian mempertahankan elipsis, koma, titik dua, dan dua spasi asli sebelum `(tekan / untuk fokus)`.
- `KamusTerm.jsx`: `Analogi:`, `Asumsi:`, `Contoh hitungan (angka textbook):`, serta `Terakhir diperbarui: <tanggal> · Sumber entri: ...` sudah memiliki spasi tepat. Kurung dan koma pada teks status/kedalaman juga sesuai sumber.
- `src/app/kamus/sektor/[slug]/page.js`: `Bahan baku:` dan `Produk:` masing-masing diikuti satu spasi sebelum isi, sesuai HTML lama.
- `KamusShell.jsx`: pemisah navigasi ` · ` dan titik setelah tautan `ilmutekkim.site` sudah tepat, termasuk jeda baris paragraf sumber.
- Koma, persen, kurung, titik dua, dan elipsis yang berasal dari nilai data, tabel, rumus, definisi, referensi, dan bacaan terkait tetap sesuai HTML lama. Tidak ada pola JSX tambahan yang perlu diperbaiki untuk tanda baca tersebut.
- `KamusLevels.jsx` dan route istilah tidak memiliki penyusunan teks bertanda baca lain yang memerlukan perubahan.

## Verifikasi

Menggunakan Babel bawaan Next serta `react-dom/server` yang sudah tersedia, tanpa instalasi, server Next, atau build. Harness dan hasil hanya ditulis di `/tmp/ilmutekkim-session-9-*`.

| Pemeriksaan | Hasil |
| --- | --- |
| Render beranda, 48 halaman istilah, dan tiga sektor | 52 halaman, masing-masing dengan `renderToString` dan `renderToStaticMarkup` |
| Struktur DOM dan atribut `.wrap` terhadap HTML lama | 52/52 cocok pada kedua jenis render; urutan atribut dan format style dinormalisasi |
| Teks terhadap HTML lama | 52/52 cocok pada kedua jenis render; whitespace pemformatan dinormalisasi, teks inline digabung tanpa menyisipkan separator |
| Cuplikan `.snip`, termasuk bacaan terkait | 154/154 cocok persis tanpa normalisasi spasi pada kedua jenis render |
| Cuplikan kartu katalog pada SSR | 123/123 berupa satu node teks, tanpa komentar pemisah React |
| Judul hitungan beranda dan sektor pada SSR | 4/4 cocok persis dan berupa satu node teks |
| Markup statis sebelum/sesudah perbaikan | 52/52 identik byte demi byte; isi tidak berubah |
| SSR sebelum/sesudah perbaikan | Perubahan hanya menghilangkan 226 komentar pemisah teks React pada beranda dan tiga sektor; 52/52 identik setelah komentar pemisah diabaikan |

Catatan pemeriksaan: SSR awal menulis hitungan sebagai `(<!-- -->48<!-- -->)` dan akhir cuplikan sebagai `yan<!-- -->…`. Harness tidak menemukan spasi literal tambahan pada markup statis awal. Penggabungan menjadi satu string menghilangkan batas node tersebut, sehingga cuplikan dan hitungan tidak lagi bergantung pada cara alat pembanding menyatukan node teks. Spasi yang sah menurut HTML lama tetap dipertahankan.

Tidak mengubah komponen non-Kamus, layout, CSS, data, dependensi, konfigurasi, lockfile, atau `_old/`. Tidak menjalankan `npm install`, `npm run build`, ataupun perintah instalasi/build pengganti. Pemeriksaan browser/hidrasi dan build Next tetap dilakukan operator; tidak ada perbaikan dalam cakupan Sesi 9 yang tertinggal.
