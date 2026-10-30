# NOTES-5 — Halaman statis terakhir

Sesi 5 selesai mengikuti **SESSION-5.md**: **38 halaman**, yaitu 26 riset/paten, 8 jalur, tentang, kalkulator, referensi, dan glosarium. BRIEF.md serta NOTES-1 sampai NOTES-4 sudah dibaca. Tidak mengerjakan `/api/ask`, sitemap, atau robots; ketiganya tetap Sesi 6 sesuai cakupan khusus sesi ini.

**Koreksi inventaris:** SESSION-5.md menyebut 237 halaman lama. Inventaris aktual `_old/` berisi **185 `index.html`**: beranda 1 + artikel 61 + video 33 + kamus 52 + halaman sesi ini 38. Sitemap lama memiliki **184 URL**, karena stub `/glosarium` tidak tercantum. Gabungan inventaris route setelah sesi ini tepat mencakup seluruh 185 halaman tersebut, tanpa URL halaman tambahan. Tidak mengarang 52 halaman tambahan untuk memenuhi angka 237.

## Berkas dan route

- `src/app/riset/page.js`, `riset/[slug]/page.js`, `riset/paten/page.js`, dan `riset/paten/[slug]/page.js`: dua indeks, 19 bedah jurnal, 5 bedah paten.
- `src/app/jalur/page.js` dan `jalur/[slug]/page.js`: indeks dan 7 jalur, total 40 langkah.
- `src/app/tentang/page.js`, `kalkulator/page.js`, `referensi/page.js`, dan `glosarium/page.js`: empat halaman terakhir.
- `src/components/ResearchPost.jsx`, `ResearchIndex.jsx`, dan `LearningPath.jsx`: renderer server berbasis data, termasuk figur, sumber, kesimpulan, tautan terkait, navigasi sebelumnya/berikutnya, serta CTA lama.
- `src/components/ResearchIntro.jsx`, `PatentIntro.jsx`, `LearningIntro.jsx`, dan `ReferenceIntro.jsx`: copy pengantar literal HTML lama; jumlah jurnal/paten/jalur/langkah dihitung dari sumber data dengan aturan generator.
- `src/components/ResearchFilters.jsx`: port perilaku non-tema `main.js` pada indeks riset/paten. Komponen sesi ini berdiri sendiri; `HomeInteractions.jsx` sesi 2 tidak diubah.
- `src/components/CalculatorInteractions.jsx` dan `src/lib/calculators.js`: logika hitung, keluaran, listener, serta gambar canvas dari `calc.js`.
- `src/lib/staticPages.js`: pengurutan data, nama penulis singkat, resolver gambar/tautan, katalog gabungan Kamus, penggabungan perpustakaan referensi, dan metadata halaman.
- `src/data/static-pages/`: 26 salinan JSON sumber, indeks impor `sources.js`, `assets.json`, dan `page-metadata.json`.

Seluruh route baru menetapkan `dynamic = "force-static"`. Tiga route detail juga menetapkan `dynamicParams = false` dan `generateStaticParams()` untuk tepat 19/5/7 slug. Halaman dan metadata sama-sama memanggil `notFound()` untuk slug tidak dikenal, termasuk nama properti prototipe. Tidak ada akses request/cookie/header atau pembacaan `_old/` saat runtime aplikasi.

## Peta seluruh 38 halaman

Semua baris mengambil markup/teks/kelas/href dan metadata dari **`_old/<route>/index.html`**. Kolom sumber menjelaskan data isi; JSON riset/paten/jalur/glosarium disalin ke `src/data/static-pages/` dengan nama relatif yang sama.

| Halaman | Tipe | Sumber data isi |
| --- | --- | --- |
| `/glosarium` | Stub meta-refresh | `_old/glosarium/index.html` |
| `/jalur/distilasi-inti` | Detail jalur | `_old/jalur.json` → `distilasi-inti`, judul konten artikel/video/paten |
| `/jalur` | Indeks jalur | `_old/jalur.json`, judul konten artikel/video/paten |
| `/jalur/keselamatan-proses` | Detail jalur | `_old/jalur.json` → `keselamatan-proses`, judul konten artikel/video/paten |
| `/jalur/kilang-petrokimia` | Detail jalur | `_old/jalur.json` → `kilang-petrokimia`, judul konten artikel/video/paten |
| `/jalur/membaca-pabrik` | Detail jalur | `_old/jalur.json` → `membaca-pabrik`, judul konten artikel/video/paten |
| `/jalur/pabrik-indonesia` | Detail jalur | `_old/jalur.json` → `pabrik-indonesia`, judul konten artikel/video/paten |
| `/jalur/sawit-produk` | Detail jalur | `_old/jalur.json` → `sawit-produk`, judul konten artikel/video/paten |
| `/jalur/utilitas-energi` | Detail jalur | `_old/jalur.json` → `utilitas-energi`, judul konten artikel/video/paten |
| `/kalkulator` | Statis + interaksi klien | `_old/kalkulator/index.html` + `_old/assets/js/calc.js` |
| `/referensi` | Perpustakaan | Referensi artikel sesi 3, `_old/research/*.json`, `_old/paten/*.json` |
| `/riset/bedah-b100-mesin-diesel` | Bedah jurnal | `_old/research/bedah-b100-mesin-diesel.json` |
| `/riset/bedah-bentonit-sonikasi-katalis-asam` | Bedah jurnal | `_old/research/bedah-bentonit-sonikasi-katalis-asam.json` |
| `/riset/bedah-biodiesel-minyak-campuran` | Bedah jurnal | `_old/research/bedah-biodiesel-minyak-campuran.json` |
| `/riset/bedah-biogas-pome-listrik-tekno-ekonomi` | Bedah jurnal | `_old/research/bedah-biogas-pome-listrik-tekno-ekonomi.json` |
| `/riset/bedah-ccus-tekno-ekonomi` | Bedah jurnal | `_old/research/bedah-ccus-tekno-ekonomi.json` |
| `/riset/bedah-daur-ulang-plastik-kimia` | Bedah jurnal | `_old/research/bedah-daur-ulang-plastik-kimia.json` |
| `/riset/bedah-digital-twin-energi-industri` | Bedah jurnal | `_old/research/bedah-digital-twin-energi-industri.json` |
| `/riset/bedah-elektrolisis-hidrogen-hijau` | Bedah jurnal | `_old/research/bedah-elektrolisis-hidrogen-hijau.json` |
| `/riset/bedah-esterifikasi-pome-katalis-karbon-zeolit` | Bedah jurnal | `_old/research/bedah-esterifikasi-pome-katalis-karbon-zeolit.json` |
| `/riset/bedah-fotokatalis-tio2-air-terproduksi` | Bedah jurnal | `_old/research/bedah-fotokatalis-tio2-air-terproduksi.json` |
| `/riset/bedah-grading-sawit-yolov4` | Bedah jurnal | `_old/research/bedah-grading-sawit-yolov4.json` |
| `/riset/bedah-hidrogen-biru-smr-atr-ngd` | Bedah jurnal | `_old/research/bedah-hidrogen-biru-smr-atr-ngd.json` |
| `/riset/bedah-hydrocracking-minyak-jelantah-biogasoline` | Bedah jurnal | `_old/research/bedah-hydrocracking-minyak-jelantah-biogasoline.json` |
| `/riset/bedah-katalis-aaem-pirolisis-biomassa` | Bedah jurnal | `_old/research/bedah-katalis-aaem-pirolisis-biomassa.json` |
| `/riset/bedah-katalis-cao-indigofera-biodiesel` | Bedah jurnal | `_old/research/bedah-katalis-cao-indigofera-biodiesel.json` |
| `/riset/bedah-ko-pirolisis-batang-sawit-polipropilena` | Bedah jurnal | `_old/research/bedah-ko-pirolisis-batang-sawit-polipropilena.json` |
| `/riset/bedah-mikroalga-pome-biofuel` | Bedah jurnal | `_old/research/bedah-mikroalga-pome-biofuel.json` |
| `/riset/bedah-minyak-pirolisis-plastik-umpan-steam-cracker` | Bedah jurnal | `_old/research/bedah-minyak-pirolisis-plastik-umpan-steam-cracker.json` |
| `/riset/bedah-nanozirconia-tersulfat-hydrocracking` | Bedah jurnal | `_old/research/bedah-nanozirconia-tersulfat-hydrocracking.json` |
| `/riset` | Indeks jurnal | `_old/research/*.json` (19), jumlah paten dari `_old/paten/*.json` |
| `/riset/paten` | Indeks paten | `_old/paten/*.json` (5) |
| `/riset/paten/paten-distilasi-reaktif-eastman-1984` | Bedah paten | `_old/paten/paten-distilasi-reaktif-eastman-1984.json` |
| `/riset/paten/paten-dividing-wall-column-basf-2005` | Bedah paten | `_old/paten/paten-dividing-wall-column-basf-2005.json` |
| `/riset/paten/paten-membran-monsanto-1980` | Bedah paten | `_old/paten/paten-membran-monsanto-1980.json` |
| `/riset/paten/paten-mtg-mobil-1988` | Bedah paten | `_old/paten/paten-mtg-mobil-1988.json` |
| `/riset/paten/paten-psa-skarstrom-1960` | Bedah paten | `_old/paten/paten-psa-skarstrom-1960.json` |
| `/tentang` | Literal statis | `_old/tentang/index.html` |

## Data, transformasi, dan paritas

- **26 JSON disalin byte demi byte:** 19 research + 5 paten + `jalur.json` + `glosarium.json`. JSON Kamus `terms.json`/`sectors.json`, manifest/spec/deep artikel, dan data video menggunakan salinan sesi sebelumnya, tanpa penyuntingan atau duplikasi.
- Urutan riset/paten mengikuti `load_research`/`load_paten`: nama berkas naik terlebih dahulu, lalu sort tanggal `date_bedah` menurun secara stabil. Tanggal yang sama mempertahankan urutan nama berkas. Ini juga menentukan navigasi bedah dan urutan daftar paper/paten di referensi.
- `ResearchPost` mengikuti `render_bedah`/`render_paten`: coverage, lead, figur/kredit, kotak bibliografi, masalah, metode/temuan atau klaim/cara kerja, batas kritis, arti pabrik, kesimpulan, bacaan terkait, navigasi, CTA. Parafrase klaim dan status paten disalin dari data, tidak disunting. `authorsShort` mempertahankan tiga nama pertama + `, dkk.` bila lebih dari tiga.
- Resolusi gambar memakai hasil yang benar-benar teramati pada HTML lama, disimpan di `assets.json` per route. Path `/assets/img/<slug>/cover.jpg` dan seluruh kredit tetap sama; tidak memeriksa keberadaan file produksi untuk mengubah hasil rendering, tidak menyalin biner, dan tidak menjalankan resolver kompresi/generator.
- Jalur mempertahankan urutan JSON. Setiap langkah di-resolve ke judul penuh dan URL konten artikel/video/paten yang sama, termasuk prefix paten `/riset/paten/`. Link tidak dikenal menyebabkan galat, sama seperti gate generator. Seluruh **40 langkah** valid. `loadKamusCatalog()` mengikuti normalisasi ASCII nama/slug/alias dan deduplikasi glosarium yang sama, menghasilkan 20 entri dalam + 28 dasar + 3 sektor; tidak menambah UI baru pada jalur.
- Referensi dibentuk dari referensi final artikel sesi 3 dalam urutan artikel generator, termasuk fallback dua spec pilot yang telah didokumentasikan sesi 3. Key deduplikasi khusus perpustakaan ialah lowercase, hapus karakter selain ASCII `a-z0-9`, ambil **60 karakter** pertama; berbeda dari key `merge_refs` artikel. Record pertama mempertahankan teks aslinya, seluruh pemakaian ditambahkan, lalu sort teks lowercase menurut code point. Hasil **250 entri**; tampilkan maksimum tiga tautan pemakaian + `, dan N artikel lain`. Daftar berikutnya memuat 19 paper dan 5 paten. Seluruh DOM referensi cocok dengan HTML jadi lama.
- `page-metadata.json` menyimpan **38 head** lama. Judul absolut, description, canonical, dan seluruh OG dipertahankan, termasuk pemotongan description yang memang sudah terjadi pada generator lama. Canonical/OG memakai domain dan slash asli `https://ilmutekkim.vercel.app/.../`; tidak diseragamkan dengan canonical Kamus. Root layout menyediakan tema, font, favicon, Header, Footer, ChatWidget, dan Vercel Insights sebagaimana sesi 1.
- Tentang, markup kalkulator, dan stub glosarium ditranskripsikan sebagai JSX server literal. Entitas HTML boleh diserialisasi React berbeda, tetapi teks/DOM sama. Input kalkulator memakai `defaultValue` agar atribut/nilai awal sama dan tetap dapat diedit tanpa handler React tambahan.

## Perilaku kalkulator

Seluruh `_old/assets/js/calc.js` dibaca dan diport; bukan sekadar formulanya. Markup awal SSG mempertahankan empat kotak hasil yang kosong dan canvas **520 × 520**, lalu efek klien menghitung keempat kalkulator saat dipasang. Event tetap **`input`**, termasuk pada select, tanpa debounce atau tombol hitung baru.

1. **Carothers:** `1/(1-p)` untuk stoikiometri sempurna; `(1+r)/(1+r-2rp)` untuk `0 < r < 1`. UI menolak p tidak finite atau p ≤ 0/p ≥ 1 dengan pesan lama. r tidak valid atau di luar rentang tersebut mengikuti fallback r = 1 lama. Hasil Xn memakai 2 desimal, tabel p = 0.9/0.95/0.99/0.995/0.999 memakai 1 desimal.
2. **LMTD:** susunan counter/co mempertahankan rumus kedua ΔT ujung. ΔT ≤ 0 menghasilkan pesan temperature cross lama; kedua ΔT berbeda kurang dari `1e-9` memakai limit ΔT pertama. ΔT tampil 1 desimal, LMTD 2 desimal. Masukan kosong/nonangka tetap mengikuti keluaran `n/a` lama; tidak menambah aturan validasi baru.
3. **McCabe–Thiele:** kurva kesetimbangan dengan volatilitas relatif konstan; q ≈ 1 menggunakan garis umpan vertikal, selain itu pinch dicari dengan biseksi **200 iterasi** dan fallback titik zF lama. Menghitung R minimum/operasi, N minimum Fenske, tangga tahap maksimum **500**, dan tahap umpan; reboiler termasuk dalam total. Validasi tetap alpha > 1 dan 0 < xB < zF < xD < 1, tanpa menambah validasi q/faktor reflux. Pesan, presisi, label, dan penjelasan jumlah tahap tetap sama. Seluruh perintah gambar, koordinat, warna, ketebalan garis, font, kurva, garis operasi, tangga, dan label canvas dipertahankan. Masukan tidak valid memperbarui pesan dan membiarkan gambar terakhir, sesuai sumber.
4. **Konversi:** °C/°F/K, Pa/kPa/bar/atm/psi, serta m³/s/m³/jam/L/s/gpm (US), dengan konstanta, urutan satuan, dan 4 desimal asli. Nilai kosong/nonangka memakai fallback nol seperti sumber. Tidak menambahkan pemisah ribuan atau mengubah label unit hasil.

Perbedaan implementasi hanya siklus hidup React: handler dibatasi pada `<main>` aktif, listener dilepas saat unmount, keluaran dipulihkan, dan canvas dibersihkan. Pemasangan ulang menghitung dari input saat itu dan tidak menggandakan listener. Script `calc.js`/`main.js`/`chat.js` lama tidak dimuat ulang; logika tema/widget tetap milik sesi 1.

## Filter riset/paten dan stub glosarium

Indeks riset/paten mempertahankan filter topik dan pencarian `main.js`: pencarian substring penuh pada `data-title` judul + topik + jurnal/nomor, lowercase dan trim, digabung dengan topik aktif. Default Semua; tidak memfilter otomatis pada pemasangan. Tanpa hasil, grid disembunyikan dan pesan asli muncul. Di mobile, chip setelah dua baris dilipat, dengan tombol **“Tampilkan semua topik (N) ▾”**, **“Tutup ▴”**, kelas dan `aria-expanded` asli. Posisi diukur saat pemasangan, tanpa listener resize, sesuai sumber. Listener/kelas/style/tombol tambahan dibersihkan saat komponen dilepas atau berpindah indeks.

`/glosarium` tetap **halaman statis yang menyajikan stub**, tanpa `redirect()` server. JSX menambahkan `<meta httpEquiv="refresh" content="0; url=/kamus" />`; React 19 menempatkannya di `<head>` saat SSR dokumen. Isi stub, title “Kamus Industri Kimia | ilmutekkim”, metadata lengkap, dan tautan cadangan `/kamus` sama dengan HTML lama. Perbedaan urutan serialisasi tag head tidak mengubah mekanisme refresh lama.

## Verifikasi

Memakai Babel/React/Next **yang sudah tersedia sebelum sesi ini**, serta parser HTML `lxml`, tanpa instalasi atau build. Harness dan hasil berada di `/tmp/ilmutekkim-session-5-*`; tidak menambah dependensi atau berkas pengujian ke proyek.

| Pemeriksaan | Hasil |
| --- | --- |
| DOM `<main>` indeks jurnal + seluruh bedah jurnal | **20/20 cocok** |
| DOM indeks paten + seluruh bedah paten | **6/6 cocok** |
| DOM indeks jalur + seluruh detail jalur | **8/8 cocok** |
| DOM tentang, kalkulator awal, referensi, glosarium | **4/4 cocok** |
| Title absolut, description, OG, canonical versus HTML lama | **38/38 cocok** |
| Penggabungan metadata root → halaman memakai resolver Next terpasang | **38/38 lulus**, tidak mewarisi isi OG beranda |
| Slug SSG dan 404 halaman/metadata | **19 + 5 + 7 unik**, sama dengan direktori lama; slug asing/prototipe → 404 |
| Meta-refresh dalam SSR dokumen | **Berada di head**, konten persis `0; url=/kamus` |
| Fungsi kalkulator versus eksekusi `calc.js` asli | **488 perbandingan lulus** |
| Keluaran UI dan seluruh perintah canvas versus `calc.js` asli | **250 perbandingan lulus**, cleanup/remount lulus |
| Filter/pencarian/mobile versus `main.js` asli | **15.648 perbandingan keadaan lulus** |
| JSON sumber, byte demi byte | **26/26 identik** |
| Load/sort riset-paten-jalur, penulis, katalog versus fungsi Python asli | **Seluruh nilai cocok** |
| Resolusi langkah jalur versus judul/href HTML tujuan | **40/40 cocok** |
| Inventaris route gabungan versus HTML lama/sitemap | **185/185 halaman**, seluruh **184 URL sitemap** + stub glosarium |
| SHA-256 berkas sebelum sesi | **626/626 tetap identik**, termasuk **296/296 `_old/`** |

Perbandingan DOM mencakup hierarki, urutan elemen, atribut, kelas, seluruh teks, href, path gambar/kredit, input/select/canvas, navigasi bedah, serta 250 entri referensi. Whitespace pemformatan dan serialisasi atribut boolean dinormalisasi. Teks gabungan elemen inline dibandingkan untuk menjaga spasi di sekitar tautan. Script kalkulator lama dikeluarkan dari perbandingan DOM karena perilakunya kini ditangani komponen klien.

Uji kalkulator mencakup masukan standar, kosong/nonangka, batas fraksi, rasio stoikiometri, suhu sama/bersilangan, semua satuan, q cair jenuh/nonjenuh, faktor reflux, dan batas tahap. Canvas memakai pencatatan perintah, bukan screenshot. Uji filter mencakup kedua indeks, semua topik, token judul nyata, kapitalisasi/spasi, nol hasil/pemulihan, enam skenario perangkat/layout, tombol mobile, dan pembersihan listener. Pengukuran offset chip disimulasikan.

**Tidak menjalankan `npm install`, `npm run build`, generator lama, atau perintah instalasi/build pengganti.** Pemanggilan fungsi Python sumber dibatasi lewat AST untuk perbandingan data baca-saja, tanpa menjalankan `main()` generator. `node_modules`, lockfile, dan `.next` sudah ada sebelum sesi. Semua perubahan aplikasi berupa **50 berkas baru**, ditambah catatan ini; berkas Sesi 1–4, konfigurasi, CSS, dependensi, `public/`, dan `_old/` tidak diubah. Metadata Git tidak tersedia sebagai repository yang dapat dipakai sesi ini, sehingga integritas berkas dibuktikan melalui snapshot SHA-256.

## Risiko dan serah terima

1. Operator masih perlu memverifikasi build/SSG Next serta hidrasi dan tampilan browser desktop/mobile. SSR React/parser, metadata resolver, simulasi DOM/input, dan perintah canvas tidak menggantikan build, screenshot, atau interaksi browser nyata. Periksa filter/topik mobile, canvas setelah mengubah input, navigasi riset ↔ paten, meta-refresh glosarium, dan tema.
2. Aset biner tetap dipasang operator di `public/assets/`. Sesi ini tidak menyalin atau menghasilkan aset biner. Seluruh href slash dan canonical dipertahankan; konfigurasi tetap `trailingSlash: false`, sehingga redirect slash perlu diperiksa operator pada runtime.
3. Risiko CSS global Kamus yang dapat bertahan sesudah navigasi klien tetap seperti NOTES-4. Tidak mengubah CSS/layout sesi sebelumnya untuk menanganinya di sesi ini.
4. Tautan lama ke `/artikel/` dari konten Kamus masih mengikuti keadaan sumber yang telah dicatat NOTES-4; tidak ada indeks `/artikel/` dalam inventaris HTML/sitemap lama. Tidak menambah URL baru atau mengubah href sesi sebelumnya.
5. Selisih angka **237 versus 185 halaman aktual** perlu dijadikan acuan perencanaan operator. Seluruh 38 halaman yang disebut satu per satu dalam SESSION-5 sudah selesai. Tidak ditemukan bug berkas Sesi 1–4 yang menghalangi pekerjaan ini.
6. `/api/ask`, sitemap, dan robots tetap belum dikerjakan, sesuai larangan Sesi 5. Fallback AI ChatWidget di luar indeks lokal menunggu Sesi 6. Tidak menguji layanan AI eksternal.

Tidak ada halaman atau perilaku dalam cakupan Sesi 5 yang tertinggal.
