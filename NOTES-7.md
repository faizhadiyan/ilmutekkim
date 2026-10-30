# NOTES-7 — Perbaikan footer ganda Kamus

Perbaikan SESSION-7 selesai. Footer situs utama disembunyikan pada `/kamus` dan seluruh `/kamus/...`, mengikuti HTML lama. Semua halaman non-Kamus, termasuk stub `/glosarium`, tetap memiliki footer situs utama.

## Mekanisme dan berkas

- `src/components/FooterGate.jsx`: komponen `"use client"` kecil yang membaca `usePathname()` dari `next/navigation`. Mengembalikan `null` bila pathname tepat `/kamus` atau diawali `/kamus/`; selain itu mengembalikan `children` tanpa elemen pembungkus.
- `src/app/layout.js`: mengimpor FooterGate dan mengganti `<Footer />` menjadi `<FooterGate><Footer /></FooterGate>`. Footer tetap menjadi komponen server yang diteruskan sebagai children ke pembungkus klien. Root layout tetap komponen server.
- Tidak memakai efek, state pemasangan, pemeriksaan `window`, atau pemuatan dinamis. Keputusan tampil langsung memakai pathname dari konteks router pada render pertama, sehingga footer non-Kamus tetap ada dalam HTML server dan hasil awal server/klien sama untuk pathname yang sama.
- `Footer.jsx`, Header, ChatWidget, seluruh komponen Kamus, CSS, data, konfigurasi, dependensi, lockfile, `_old/`, dan dokumen sesi sebelumnya tidak diubah. Footer khusus `.foot` Kamus dipertahankan.

Pengecualian memakai batas segmen: `/kamus/` ikut disembunyikan, sedangkan `/kamus-lain`, `/kamusfoo`, dan `/artikel/kamus` tetap menampilkan footer utama. Tidak ada pengecualian untuk `/glosarium`.

## Bukti perbandingan

Menggunakan Babel bawaan Next dan ReactDOMServer yang sudah terpasang, tanpa instalasi atau build Next. Harness memuat komponen halaman dan layout aktual, mengembangkan seluruh `generateStaticParams()`, lalu merender dengan `PathnameContext` dan hook `usePathname()` asli dari Next.

| Route | Halaman | Footer utama pada HTML server setelah perbaikan |
| --- | ---: | --- |
| `/kamus` | 1 | Tidak ada |
| `/kamus/istilah/[slug]` | 48 | Tidak ada |
| `/kamus/sektor/[slug]` | 3 | Tidak ada |
| `/` | 1 | Tetap ada, persis markup Footer |
| `/artikel/[slug]` | 61 | Tetap ada, persis markup Footer |
| `/video`, `/video/[slug]` | 33 | Tetap ada, persis markup Footer |
| `/riset`, `/riset/[slug]` | 20 | Tetap ada, persis markup Footer |
| `/riset/paten`, `/riset/paten/[slug]` | 6 | Tetap ada, persis markup Footer |
| `/jalur`, `/jalur/[slug]` | 8 | Tetap ada, persis markup Footer |
| `/referensi`, `/kalkulator`, `/tentang` | 3 | Tetap ada, persis markup Footer |
| `/glosarium` | 1 | Tetap ada, persis markup Footer |

Hasil pemeriksaan:

- **185/185 halaman lulus**: 52 halaman Kamus tanpa footer utama, 133 halaman non-Kamus dengan tepat satu footer utama. Keberadaan `<footer>` juga dibandingkan dengan HTML lama masing-masing route: seluruhnya cocok.
- Layout sebelum perbaikan direkonstruksi dengan membalik hanya penambahan FooterGate. Pada seluruh 52 halaman Kamus, HTML sesudah perbaikan identik dengan HTML sebelumnya setelah menghapus tepat markup Footer. Pada 133 halaman lain, seluruh HTML sebelum/sesudah identik.
- **52/52 halaman Kamus** tetap memiliki tepat satu `.foot`. Markup Header dan ChatWidget tetap ada dan identik di seluruh 185 halaman.
- **185/185 perbandingan render awal server/klien lulus**: modul navigasi Next dan FooterGate dimuat ulang dengan cabang lingkungan browser, menggunakan pathname yang sama; hasil HTML identik dengan render server. Ini pemeriksaan kesamaan render awal, bukan pengujian hidrasi DOM di browser.
- **11 kasus batas lulus**: `/`, `/glosarium`, `/glosarium/`, `/kamus`, `/kamus/`, `/kamus/istilah/distilasi`, `/kamus/sektor/oleokimia/`, `/kamus-lain`, `/kamusfoo`, `/artikel/kamus`, dan konteks pathname `null`. Nilai `null` tidak menyebabkan error dan mempertahankan children; route App Router yang diuji memakai pathname aktual.
- Snapshot SHA-256 sebelum/sesudah memverifikasi hanya `src/app/layout.js` yang berubah dari berkas awal; hanya FooterGate dan catatan ini yang ditambahkan. Tidak ada berkas awal yang dihapus.

Artefak verifikasi sementara:

- `/tmp/ilmutekkim-session-7-check.cjs` — harness render/perbandingan.
- `/tmp/ilmutekkim-session-7-results.json` — jumlah dan hasil per kelompok route.
- `/tmp/ilmutekkim-session-7-rendered/` — HTML hasil render 185 halaman.
- `/tmp/ilmutekkim-session-7-before.json` — hash berkas sebelum perubahan.

## Batas verifikasi dan serah terima

Tidak menjalankan `npm install`, `npm run build`, instalasi/build pengganti, generator lama, atau layanan eksternal. HTML yang diperiksa berasal dari ReactDOMServer terhadap sumber saat ini, bukan artefak `.next` atau hasil build SSG Next baru. Operator tetap menjalankan build untuk memeriksa HTML statis keluaran Next serta hidrasi dan navigasi klien Kamus ↔ non-Kamus di browser. Tidak ada perubahan cakupan lain atau pertanyaan terbuka yang menghalangi perbaikan ini.
