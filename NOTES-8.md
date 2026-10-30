# NOTES-8 — Footer kamus melalui route group

Perbaikan sumber selesai sesuai `SESSION-8.md`, menggantikan mekanisme Sesi 7. Footer situs utama kini dimiliki layout server `(site)`, bukan root dan bukan komponen klien yang membaca pathname. Tidak menjalankan `npm install`, `npm run build`, build pengganti, atau harness render manual.

## Perubahan

- `src/app/layout.js`: menghapus impor `Footer`, impor `FooterGate`, dan pemanggilan `<FooterGate><Footer /></FooterGate>`. Script tema, font, metadata, CSS, Header, dan ChatWidget tetap identik. Urutan body root: Header, children, ChatWidget.
- `src/app/(site)/layout.js`: layout server baru, mengimpor Footer melalui `@/components/Footer` dan mengembalikan fragment berisi children lalu `<Footer />`. Tidak menambahkan elemen pembungkus DOM, hook pathname, atau direktif `use client`.
- `src/components/FooterGate.jsx`: dihapus; tidak ada referensinya lagi di `src/`.
- Seluruh halaman non-kamus dipindah tanpa perubahan isi. Tidak diperlukan perbaikan impor karena seluruh impor halaman tersebut memakai alias `@/` atau modul paket.

Daftar lengkap file yang dipindah:

| Lokasi semula | Lokasi akhir |
| --- | --- |
| `src/app/page.js` | `src/app/(site)/page.js` |
| `src/app/artikel/[slug]/page.js` | `src/app/(site)/artikel/[slug]/page.js` |
| `src/app/video/page.js` | `src/app/(site)/video/page.js` |
| `src/app/video/[slug]/page.js` | `src/app/(site)/video/[slug]/page.js` |
| `src/app/riset/page.js` | `src/app/(site)/riset/page.js` |
| `src/app/riset/[slug]/page.js` | `src/app/(site)/riset/[slug]/page.js` |
| `src/app/riset/paten/page.js` | `src/app/(site)/riset/paten/page.js` |
| `src/app/riset/paten/[slug]/page.js` | `src/app/(site)/riset/paten/[slug]/page.js` |
| `src/app/jalur/page.js` | `src/app/(site)/jalur/page.js` |
| `src/app/jalur/[slug]/page.js` | `src/app/(site)/jalur/[slug]/page.js` |
| `src/app/tentang/page.js` | `src/app/(site)/tentang/page.js` |
| `src/app/kalkulator/page.js` | `src/app/(site)/kalkulator/page.js` |
| `src/app/referensi/page.js` | `src/app/(site)/referensi/page.js` |
| `src/app/glosarium/page.js` | `src/app/(site)/glosarium/page.js` |

## Struktur akhir dan pewarisan layout

```text
src/app/
├── layout.js                   # Header → children → ChatWidget
├── globals.css
├── chat.css
├── not-found.js                # Tetap di root, tidak dipindah/diubah
├── api/
│   └── ask/route.js             # Tetap di root, tidak dipindah/diubah
├── (site)/
│   ├── layout.js               # children → Footer (server)
│   ├── page.js
│   ├── artikel/[slug]/page.js
│   ├── video/{page.js,[slug]/page.js}
│   ├── riset/{page.js,[slug]/page.js,paten/{page.js,[slug]/page.js}}
│   ├── jalur/{page.js,[slug]/page.js}
│   ├── tentang/page.js
│   ├── kalkulator/page.js
│   ├── referensi/page.js
│   └── glosarium/page.js
└── kamus/                      # Seluruh subtree identik dengan sebelum sesi
    ├── layout.js
    ├── kamus.css
    ├── page.js
    ├── istilah/[slug]/page.js
    └── sektor/[slug]/page.js
```

Route group `(site)` tidak menjadi segmen URL. Halaman situs memiliki urutan DOM Header → konten → Footer → ChatWidget. Halaman `/kamus`, `/kamus/istilah/<slug>`, dan `/kamus/sektor/<slug>` berada di luar grup, sehingga tidak mewarisi Footer situs; footer `.foot` bawaan Kamus tetap berada di kontennya. `/glosarium` masuk `(site)` dan tetap memperoleh Footer situs. `not-found.js` tetap di root sesuai instruksi; fallback root tidak mewarisi layout `(site)`.

## Pemeriksaan yang dilakukan

Pemeriksaan ini memeriksa sumber, bukan hasil prerender Next:

- Hash SHA-256: **14/14 file yang dipindah identik byte demi byte**, termasuk seluruh ekspor konfigurasi statis, `generateStaticParams`, metadata, markup, dan teks halaman.
- **959/959 file yang tetap pada lokasinya tidak berubah** sebelum penulisan catatan ini. Ini mencakup seluruh subtree Kamus, komponen Header/Footer/ChatWidget, data, CSS, API, `not-found.js`, konfigurasi, dependensi/lockfile, public, `_old/`, dan berkas sesi sebelumnya.
- Perubahan root persis penghapusan dua impor dan satu pemanggilan FooterGate. Di luar pemindahan, hanya root layout yang berubah, FooterGate yang dihapus, dan layout `(site)` yang ditambah; catatan ini ditambahkan terakhir.
- **18/18 pola route sama** sebelum/sesudah pemindahan: 17 pola halaman dan satu API. Mengabaikan segmen grup menghasilkan URL yang sama tanpa benturan route.
- Parser Babel bawaan Next berhasil memeriksa **55 file JS/JSX**; **232 impor lokal** dapat diresolusikan. Tidak memasang dependensi tambahan.
- Pemeriksaan struktur layout memastikan Footer hanya dipasang di `(site)`, Header dan ChatWidget tetap di root, dan Kamus berada di luar grup.

Snapshot hash dan daftar pemindahan pemeriksaan sumber disimpan sementara di `/tmp/ilmutekkim-session-8/`. Tidak menghasilkan atau memperbarui artefak `.next` dalam sesi ini.

## Verifikasi SSG final oleh operator

**Verifikasi SSG final adalah pekerjaan operator lewat `npm run build`. Belum ada klaim build/SSG lulus dalam sesi ini; pemeriksaan sumber di atas tidak menggantikan hasil build Next asli.** Harness render manual Sesi 7 tidak dipakai sebagai bukti.

1. Jalankan `npm run build` dari workspace. Pastikan build sukses dan jumlah halaman yang ter-generate tetap **188 sesuai target SESSION-8.md**. Pastikan daftar route publik sama dengan sebelum restrukturisasi dan tidak mengandung segmen `(site)`.
2. Periksa HTML hasil build terbaru di `.next/server/app/`, termasuk kemungkinan direktori grup pada path artefak. Gunakan HTML nyata sebelum hidrasi, bukan hasil render komponen manual atau payload JavaScript/RSC. Untuk menemukan file HTML:

   ```sh
   rg --files --hidden --no-ignore .next/server/app -g '*.html'
   ```

3. Pada seluruh halaman `(site)`—beranda, artikel, video, riset/paten, jalur, tentang, kalkulator, referensi, dan stub `/glosarium`—pastikan tepat satu elemen `.foot-brand` milik Footer situs sudah ada di HTML statis. Pastikan Footer berada setelah konten dan sebelum ChatWidget.
4. Pada seluruh **52 halaman Kamus** (beranda, 48 istilah, tiga sektor), pastikan tidak ada elemen `.foot-brand` pada HTML statis dan footer `.foot` Kamus tetap ada. Sertakan `/kamus/istilah/azeotrop`, yaitu contoh kegagalan Sesi 7, serta `/kamus/sektor/oleokimia`.
5. Setelah itu, periksa muat langsung dan navigasi situs ↔ Kamus di browser: keberadaan footer sesuai route sejak HTML awal dan tetap sama setelah hidrasi, tanpa kedip atau hydration mismatch. Header serta ChatWidget tetap tampil.

Tidak ada perubahan data atau `generateStaticParams`; jumlah output SSG aktual dan perilaku browser masih menunggu verifikasi operator tersebut.
