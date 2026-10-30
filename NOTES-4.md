# NOTES-4 — Kamus lengkap

Sesi 4 selesai mengikuti **SESSION-4.md**: seluruh konten subtree Kamus, yaitu **52 halaman** (beranda + 48 istilah + 3 sektor), CSS Kamus, pencarian klien, pemilih kedalaman, serta indeks pencarian untuk Kamus dan ChatWidget. Cakupan khusus ini menjadi acuan meskipun peta ringkas BRIEF.md menempatkan API pada Sesi 4.

Tidak mengerjakan riset/jalur/tentang/kalkulator/referensi/glosarium, `/api/ask`, sitemap, atau robots. Tidak mengubah berkas sesi 1–3, dependensi, konfigurasi, lockfile, maupun `_old/`. Tidak menjalankan `npm install`, `npm run build`, perintah instalasi/build pengganti, atau generator lama.

## Berkas dan struktur

- `src/app/kamus/layout.js`: mengimpor hanya `./kamus.css` dan menambahkan link font Kamus persis dari head lama: Plus Jakarta Sans 600/700/800 + Noto Sans 400/600/700. Link stylesheet memakai `precedence="default"` agar React menempatkannya di head. Header, Footer, ChatWidget, font global, dan script tema tetap diwarisi dari root tanpa perubahan.
- `src/app/kamus/kamus.css`: salinan byte-identik `_old/kamus/assets/kamus.css`, termasuk override tema gelap. Tidak ada CSS tambahan atau penyuntingan selector. File ini hanya diimpor oleh layout Kamus.
- `src/app/kamus/page.js`: seluruh beranda dengan hero, pencarian, tiga kartu sektor, enam chip fondasi, istilah populer, katalog gabungan A–Z 48 istilah, dan enam bagian fondasi.
- `src/app/kamus/istilah/[slug]/page.js`: 48 slug dari data melalui `generateStaticParams()`, `dynamicParams = false`, `dynamic = "force-static"`. Kedua jenis entri dirender server.
- `src/app/kamus/sektor/[slug]/page.js`: tiga slug, konfigurasi statis yang sama; alur proses, simpul tertaut/tanpa tautan, bahan/produk, dan daftar istilah sesuai urutan sumber.
- `src/components/KamusShell.jsx`: pembungkus `.wrap` dan footer khusus `.foot` dari generator. Tidak menambahkan `<main>`. Footer khusus ini tetap di dalam `.wrap`; Footer root tetap hadir sesuai SESSION-4, tanpa menggandakan Header atau ChatWidget.
- `src/components/KamusTermCard.jsx`: kartu `.sresult` dalam/dasar, potongan definisi, dan label fondasi/status sesuai sumber.
- `src/components/KamusTerm.jsx`: renderer entri dasar dan entri dalam.
- `src/components/KamusSearch.jsx`: komponen klien yang mengembalikan `null`, memasang perilaku pencarian pada markup server beranda Kamus.
- `src/components/KamusLevels.jsx`: komponen klien yang mengembalikan `null`, memasang perilaku tombol kedalaman pada entri dalam.
- `src/lib/kamus.js`: indeks data server, urutan A–Z, pemotongan teks mengikuti code point Python, dan pembentukan metadata.
- `src/data/kamus/`: `terms.json`, `sectors.json`, `basic-terms.json`, `page-metadata.json`.
- `public/kamus/search-index.json`: salinan VERBATIM dari `_old/kamus/search-index.json`, **satu-satunya berkas public baru**. Tidak menyalin biner maupun skrip lama.

## Peta halaman

| Route | Jumlah | Sumber |
| --- | ---: | --- |
| `/kamus` | 1 | `_old/kamus/index.html`, `build_index` |
| `/kamus/istilah/<slug>` — entri dalam | 20 | `terms.json`, `build_term` |
| `/kamus/istilah/<slug>` — entri dasar | 28 | hasil gabungan glosarium lama, `build_basic_term` |
| `/kamus/sektor/oleokimia` | 1 | `sectors.json`, 14 istilah |
| `/kamus/sektor/kilang-migas` | 1 | `sectors.json`, 14 istilah |
| `/kamus/sektor/petrokimia` | 1 | `sectors.json`, 15 istilah |

Seluruh 48 slug istilah (prefix `/kamus/istilah/`):

| Slug | Jenis |
| --- | --- |
| `distilasi` | Dalam |
| `reflux` | Dalam |
| `flooding` | Dalam |
| `heat-exchanger-dan-lmtd` | Dalam |
| `fouling` | Dalam |
| `pompa-kavitasi-npsh` | Dalam |
| `neraca-massa` | Dalam |
| `reaktor-konversi-selektivitas` | Dalam |
| `cooling-tower` | Dalam |
| `absorpsi-dan-stripping` | Dalam |
| `steam-dan-utilitas` | Dalam |
| `relief-valve` | Dalam |
| `splitting` | Dalam |
| `transesterifikasi` | Dalam |
| `ffa-dan-acid-value` | Dalam |
| `hidrogenasi` | Dalam |
| `distilasi-atmosferik-cdu` | Dalam |
| `fcc-fluid-catalytic-cracking` | Dalam |
| `steam-cracking` | Dalam |
| `polimerisasi` | Dalam |
| `azeotrop` | Dasar |
| `batch` | Dasar |
| `blowdown` | Dasar |
| `bottoms` | Dasar |
| `continuous` | Dasar |
| `dcs` | Dasar |
| `distilat` | Dasar |
| `flare` | Dasar |
| `hazop` | Dasar |
| `kondensor` | Dasar |
| `loop-kontrol` | Dasar |
| `p-id` | Dasar |
| `packing` | Dasar |
| `pengendali-pid` | Dasar |
| `permit-to-work` | Dasar |
| `pinch` | Dasar |
| `proses-kraft` | Dasar |
| `reboiler` | Dasar |
| `safety-instrumented-system` | Dasar |
| `seksi-rectifying` | Dasar |
| `seksi-stripping` | Dasar |
| `sil` | Dasar |
| `stoikiometri` | Dasar |
| `suhu-wet-bulb` | Dasar |
| `tahap-kesetimbangan` | Dasar |
| `tray` | Dasar |
| `utilitas` | Dasar |
| `volatilitas-relatif` | Dasar |

Daftar slug tepat sama dengan direktori HTML lama. Slug yang tidak dikenal menghasilkan `notFound()` pada halaman dan metadata, termasuk nama properti prototipe seperti `toString`, `constructor`, dan `__proto__`. Href sumber tetap memakai slash dan fragment aslinya; konfigurasi root `trailingSlash: false` tidak diubah.

## Skema data dan rendering

`terms.json` dan `sectors.json` disalin byte demi byte dari `_old/kamus-data/`. `terms.json` sebenarnya berisi **20 entri dalam**, bukan seluruh 48 istilah. Setiap entri mempertahankan `slug`, `term`, `aliases`, `fondasi`, `sectors`, `populer`, `definisi`, `analogi`, `mekanisme`, `prinsip`, `persamaan` (rumus/simbol/asumsi), `variabel` (nama/rentang/arah/efek), `kegagalan`, `plant` (biaya/checklist/contoh), `terkait`, `referensi`, dan `updated`. Alias dipertahankan di data pencarian; sumber HTML tidak menampilkan daftar alias terpisah, sehingga tidak ditambahkan UI alias baru.

`sectors.json` memuat tiga `sectors`, enam `fondasi`, serta `sector_terms` yang menetapkan urutan daftar setiap sektor. Urutan kartu populer/fondasi mengikuti urutan deklarasi entri dalam; katalog gabungan memakai sort lowercase berdasarkan code point, mengikuti Python, bukan sort locale browser.

`basic-terms.json` berisi **28 entri dasar** dengan `{ slug, term, definisi, terkait, kind }`. Data diekstrak dari indeks pencarian lama, yang sudah memuat hasil penggabungan glosarium dan resolusi judul bacaan terkait. `terkait` berisi `{ type, label, type_label, url }`; label dan path lama dipertahankan termasuk tautan paten dan judul panjangnya. Seluruh nilai kemudian diverifikasi terhadap pemanggilan fungsi asli `basic_terms()` dan `target_title()` dari generator pada glosarium/HTML lama. Tidak ada pembacaan `_old/`, glosarium mentah, atau file sumber lain pada runtime aplikasi.

`page-metadata.json` memuat **52 record** keyed per route, diekstrak dari head setiap HTML lama: title, description, canonical. Setiap title diekspor sebagai `{ absolute: ... }`. Semua canonical lama sengaja tetap **`https://ilmutekkim.site`** tanpa path atau slash tambahan. Head Kamus tidak memiliki tag OG; `openGraph: null` secara eksplisit meniadakan metadata OG beranda yang akan diwarisi dari root. Jangan menyeragamkan canonical atau menambahkan OG baru tanpa instruksi.

Entri dalam mempertahankan definisi/analogi, badge fondasi/sektor, pilihan level, mekanisme/prinsip, persamaan, tabel sensitivitas, batas/kegagalan, biaya/diagnosis/contoh plant, lapis pengantar, relasi, referensi, dan tanggal. Rumus merupakan HTML tepercaya dari JSON statis (entitas dan `<sub>`); hanya field `rumus` dirender lewat `dangerouslySetInnerHTML`, sebagaimana generator tidak meng-escape field itu. Field lain memakai escaping React. Entri dasar mempertahankan definisi, status kedalaman dan bacaan terkait, termasuk cabang daftar bacaan kosong.

## Perilaku pencarian

Port membaca seluruh `_old/kamus/assets/search.js`, terpisah dari pencarian lokal ChatWidget yang tidak diubah.

- Mengambil `/kamus/search-index.json` hanya ketika kueri minimal **dua karakter**. Kueri kosong/satu karakter mengosongkan hasil tanpa fetch. Tidak ada pencarian otomatis saat pemasangan.
- Normalisasi: trim kueri, lowercase, NFD, hapus combining marks U+0300–U+036F. Pencocokan memakai substring kueri utuh, tanpa tokenisasi.
- Skor nama identik **100**, awalan nama **80**, substring nama **60**; alias identik **90**, substring alias **55**, memakai nilai tertinggi. Jika belum ada skor, substring `search_text` bernilai **25**.
- Kandidat dengan skor > 0 diurutkan menurun secara stabil dan dibatasi **12 istilah**. Sektor dicocokkan pada gabungan nama + tagline, tanpa batas 12, lalu ditampilkan dalam grup terpisah setelah Istilah.
- Hasil istilah mempertahankan nama, label `Entri dasar` bila berlaku, potongan definisi `.slice(0, 150)` JavaScript + elipsis, dan href `/kamus/istilah/<slug>/`. Sektor memakai nama, tagline, dan href `/kamus/sektor/<slug>/`. Escaping HTML persis sumber: `&` dan `<`.
- Tidak ada hasil: copy `.zero` lama tetap utuh, mengarahkan pembaca menggunakan tombol Tanya Tekkim yang sudah ada. Tidak menambahkan tombol/pemanggilan API chatbot atau membuka panel otomatis.
- Event input memakai debounce **140 ms**; submit mencegah navigasi dan mencari langsung. Shortcut `/` memfokuskan pencarian kecuali fokus sudah di input tersebut atau elemen INPUT/TEXTAREA lain. Perilaku submit terhadap timer input yang tertunda tetap mengikuti sumber.
- Hasil fetch/JSON disimpan dalam cache selama pemasangan. Kegagalan fetch/JSON dicache sebagai `{ terms: [], sectors: [] }` dan menghasilkan pesan nol hasil. Urutan penyelesaian permintaan yang bersamaan tetap seperti sumber; tidak menambahkan pembatalan kueri lama selama halaman aktif.
- Saat komponen dilepas, timer/listener dibersihkan, isi hasil dipulihkan, dan respons tertunda tidak menulis ke halaman yang sudah dilepas. Pemasangan ulang tidak menggandakan listener. Perubahan ini diperlukan untuk siklus hidup React dan tidak mengganti hasil pencarian saat aktif.

`public/kamus/search-index.json` memiliki 48 `terms` dan tiga `sectors`. Entri dalam tetap memiliki semua field jawaban Awam/Tekkim/Plant yang diperlukan ChatWidget; entri dasar tetap memiliki status dan bacaan terkait. Widget sesi 1 kini dapat mem-fetch path aktual ini dan seluruh tautan istilahnya telah mempunyai route. Fallback `/api/ask` tetap menunggu sesi API.

## Pemilih kedalaman

Port script inline `SEG_JS`: tombol Awam/Tekkim/Plant/Semua mengganti kelas `on` dan `style.display` setiap `[data-layer]`. Setelah efek terpasang, tombol **Tekkim diklik sebagai keadaan awal**, persis sumber. Definisi, analogi, relasi, dan referensi tetap terlihat. Semua menampilkan ketiga lapisan; entri dasar tidak memiliki pemilih level. HTML server tetap berisi seluruh lapisan, sama seperti HTML lama sebelum script berjalan.

Selektor dibatasi pada `.wrap` entri aktif; listener dan keadaan DOM dipulihkan saat dilepas, dependensi slug menangani navigasi antaristilah. Tidak memuat `main.js`, `search.js`, atau `chat.js` lagi sehingga handler tema/widget tidak digandakan.

## Verifikasi

Menggunakan dependensi yang sudah tersedia: Babel bawaan Next memeriksa JSX/impor, `react-dom/server` menghasilkan HTML sementara, parser `lxml` membandingkan hasil. Ini **bukan build Next** dan tidak memakai hasil `.next` lama.

| Pemeriksaan | Hasil |
| --- | --- |
| DOM seluruh beranda Kamus | **1/1 cocok** |
| DOM entri dalam, termasuk rumus/tabel/relasi/referensi | **20/20 cocok** |
| DOM entri dasar, termasuk bacaan artikel/video/paten | **28/28 cocok** |
| DOM sektor, termasuk simpul alur dan daftar istilah | **3/3 cocok** |
| Metadata versus head HTML asli | **52/52 cocok** |
| Penggabungan metadata root → Kamus oleh resolver Next terpasang | **52/52 lulus**, OG root terhapus, title absolut dan canonical sesuai |
| Slug statis dan penanganan 404 halaman/metadata | **48 + 3 slug unik**, cocok direktori lama; slug tidak dikenal/properti prototipe → 404 |
| Pencarian asli versus port React | **748 perbandingan lulus**, termasuk **725 kueri** |
| Pemilih level asli versus port React | **160 perbandingan lulus** pada seluruh 20 entri dalam |
| Gate kedalaman generator asli | **20/20 lulus** |
| Entri dasar versus hasil generator asli | **28/28 cocok seluruh nilai** |
| Salinan CSS/terms/sectors/search-index | **4/4 identik byte demi byte** |
| Hash berkas yang ada sebelum sesi | **459/459 tidak berubah**, termasuk **296/296 berkas `_old/`** |

Perbandingan DOM mencakup `.wrap` lengkap beserta `.foot`, hierarki/urutan elemen, atribut, kelas, href, style, dan teks. Whitespace pemformatan, urutan atribut, serta titik koma style dinormalisasi; teks gabungan pada elemen inline turut diperiksa agar spasi di sekitar tautan/simbol tidak hilang. Tidak membandingkan ulang Header/Footer root/ChatWidget yang tidak berubah. Font Kamus terverifikasi memakai URL tepat dan stylesheet dipindahkan React ke `<head>`.

Perbandingan pencarian mencakup nama/alias, prefix/substring, potongan isi, kapitalisasi, spasi, diakritik, sektor, kueri kosong/pendek, nol hasil, escaping, debounce, shortcut, cache sukses/gagal, kegagalan JSON, urutan respons async, pelepasan saat respons tertunda, dan pemasangan ulang. Pemilih level diuji pada keadaan awal, semua tombol berulang, pelepasan, dan pemasangan ulang. DOM, timer, fetch, dan hook disimulasikan; ini bukan interaksi browser nyata.

Harness/hasil ada di `/tmp/ilmutekkim-session-4-*` (loader, render, parity, behavior, data, metadata dan direktori rendered), tanpa dependensi atau berkas pengujian baru di proyek. Pemeriksaan metadata memakai `accumulateMetadata` dari Next yang sudah terpasang dengan marker `server-only` disimulasikan oleh harness; tidak menjalankan server/build Next.

## Risiko dan serah terima

1. Operator tetap perlu menjalankan build/SSG Next serta memeriksa hidrasi, tampilan desktop/mobile, tema, pencarian, shortcut, pergantian level, dan navigasi antarhalaman. Pemeriksaan JSX/SSR/parser dan simulasi perilaku tidak menggantikan runtime/browser nyata.
2. CSS Kamus sengaja dipertahankan verbatim, termasuk selector global (`:root`, `body`, `.hero`, `.grid`, `.card`, `.chips`). Import dibatasi ke layout Kamus sesuai instruksi. Operator perlu memeriksa urutan stylesheet dan perpindahan klien Kamus ↔ halaman utama karena stylesheet global App Router dapat bertahan setelah navigasi; jangan mengubah CSS/root atau menambahkan sistem styling baru untuk menanganinya tanpa cakupan terpisah.
3. Root layout tetap memuat font situs dan Footer umum, sementara Kamus menambahkan font serta `.foot` miliknya; ini mengikuti instruksi eksplisit untuk mewarisi komponen root dan mempertahankan DOM konten lama. Duplikasi fungsi footer dan link font global tidak dihilangkan karena berkas sesi 1–3 dilarang disentuh.
4. Tautan sumber ke `/artikel/` dari `.foot`, riset/paten, jalur, dan halaman statis lain tetap dipertahankan. Beberapa tujuan di luar Kamus belum mempunyai route pada tahap ini; pengerjaannya tetap di sesi terkait. Tidak ditemukan bug sesi 1–3 yang menghalangi Kamus.
5. API belum tersedia: pencocokan lokal ChatWidget kini mempunyai indeks dan halaman sitasi, tetapi pertanyaan di luar katalog tetap memerlukan sesi `/api/ask`. Tidak menguji layanan AI eksternal.
6. Seluruh aset biner tetap tanggung jawab operator di `public/assets/`. Sesi ini tidak memerlukan biner baru; satu-satunya tambahan public adalah indeks JSON. Canonical dan href slash sumber sengaja dipertahankan; redirect slash perlu diperiksa operator.

Tidak ada halaman atau perilaku dalam cakupan SESSION-4 yang tertinggal dan tidak ada pertanyaan yang menghalangi serah terima.
