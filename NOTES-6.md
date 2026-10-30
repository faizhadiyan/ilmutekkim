# NOTES-6 — API, sitemap/robots, dan cache aset

Sesi 6 selesai mengikuti **SESSION-6.md**, setelah membaca BRIEF.md dan NOTES-1.md sampai NOTES-5.md. Cakupan: port `/api/ask`, sitemap/robots, header cache aset, contoh environment, pengujian lokal tanpa key asli, dan inventaris final. Tidak menjalankan `npm install`, `npm run build`, perintah instalasi/build pengganti, server preview, generator lama, atau panggilan AI sungguhan.

Ada satu ketidaksesuaian spesifikasi: **sumber `_old/api/ask.js` tidak memvalidasi Content-Type dan tidak memiliki cabang/status 415**. Port mempertahankan perilaku sumber, sebagaimana aturan logika identik dan adaptasi mekanis. Detail dan hasil uji ada di bawah; tidak mengarang error atau pesan 415 baru.

## Perubahan Sesi 6

| Berkas | Perubahan |
| --- | --- |
| `src/app/api/ask/route.js` | Route handler baru, port mekanis `_old/api/ask.js` |
| `public/sitemap.xml` | Salinan byte-identik `_old/sitemap.xml` |
| `public/robots.txt` | Salinan byte-identik `_old/robots.txt` |
| `.env.example` | Salinan byte-identik `_old/.env.example`, key tetap kosong |
| `next.config.mjs` | Menambahkan hanya `headers()` untuk cache `/assets/:path*` |
| `NOTES-6.md` | Catatan port, hasil verifikasi, inventaris final, dan risiko operator |

Lima berkas baru dan satu berkas konfigurasi diubah. **Satu-satunya berkas lama yang berubah ialah `next.config.mjs`**, sesuai deliverable eksplisit Sesi 6. `trailingSlash: false` tetap sama. Tidak membuat `vercel.json`; tidak menambahkan dependensi, skrip package, CSS, data, komponen UI, aset biner, atau route halaman. Seluruh berkas aplikasi Sesi 1–5 selain penambahan konfigurasi yang diminta tetap identik.

## Port `/api/ask`

Route menetapkan `runtime = "nodejs"` dan `dynamic = "force-dynamic"`. Fungsi handler diekspor sebagai `POST`; metode `GET`, `HEAD`, `PUT`, `PATCH`, `DELETE`, dan `OPTIONS` memakai handler yang sama untuk mempertahankan JSON 405 lama, termasuk `message: "Use POST {question, level}"`. Tidak mengandalkan respons 405/OPTIONS otomatis Next yang formatnya berbeda. Pada transport HTTP nyata, HEAD tidak mengirim body menurut semantik HTTP; harness membandingkan objek Response yang dikembalikan handler.

Adaptasi batas HTTP:

- `req.headers["x-forwarded-for"]` menjadi `request.headers.get("x-forwarded-for")`. IP tetap bagian pertama sebelum koma, di-trim, dengan fallback `unknown`. Tidak menambahkan sumber IP lain.
- `req.body` menjadi teks body dari `await request.text()`, lalu menjalankan `JSON.parse` seperti cabang string sumber. Kegagalan baca/parse menghasilkan pertanyaan kosong dan respons 400. Objek JSON yang sebelumnya sudah diparse platform dibandingkan dengan payload JSON wire yang setara pada port.
- `res.status(...).json(...)` menjadi `Response.json(..., { status: ... })`. Tidak mengekspor helper `classifyQuestion` dari file route karena ekspor route Next dibatasi; helper tetap fungsi internal yang sama.

Seluruh blok sumber dari `const WINDOW_MS` sampai sebelum handler **identik verbatim**, meliputi konstanta, Map rate limit, instruksi level, system prompt, regex satuan, tujuh kelompok sinyal, classifier, wrapper timeout, kedua penyedia, URL API, header autentikasi, serta payload upstream. Tidak ada pencarian glosarium di server dan tidak ada dependensi pada `_old/` saat runtime.

Perilaku yang dipertahankan:

- Maksimum **20 request per 10 menit per IP per instance**, Map in-memory. Metode selain POST ditolak sebelum menghitung rate; POST dihitung sebelum validasi body dan pemeriksaan key, termasuk request invalid. Request ke-21 menghasilkan 429 `rate_limited`; umur timestamp tepat 600.000 ms sudah keluar dari jendela. Tidak menambah header rate limit, pembersihan Map global, atau penyimpanan bersama.
- Pertanyaan wajib string nonkosong sesudah trim; maksimum **500 unit panjang string JavaScript**. Error 400 `question_required` atau `{ error: "question_too_long", max: 500 }` tetap sama. Pemilihan level/fallback `awam` menggunakan ekspresi sumber yang sama, tanpa validasi level tambahan.
- Skor **< 4** memilih Gemini **`gemini-3.5-flash-lite`**, key `GEMINI_API_KEY`; override `GEMINI_MODEL` tetap dibaca saat modul diinisialisasi. Skor **≥ 4** memilih DeepSeek **`deepseek-flash`**, key `DEEPSEEK_API_KEY`. Skor, urutan reasons, bobot level, ambang panjang/kata, dan perilaku sinonim satu kelompok tidak berubah.
- Key utama hilang, HTTP upstream gagal, jaringan/timeout, JSON upstream invalid, dan jawaban kosong mencoba penyedia kedua. Timeout tetap **20.000 ms** dan timer dibersihkan. Kedua key kosong langsung 503 `{ error: "ai_not_configured" }`.
- Respons sukses mempertahankan **seluruh 11 field**: `answer`, `source`, `verified`, `model`, `level`, `route`, `router`, `score`, `reasons`, `fallback`. Termasuk `source: "ai"`, `verified: false`, `router: "heuristic"`, label route awal, model penyedia yang benar-benar menjawab, dan flag fallback berdasarkan model seperti sumber.
- Jika kedua upaya gagal, error mengikuti **upaya terakhir**, persis sumber: 503 `ai_not_configured` bila error terakhir `_not_configured`; selain itu 502 `ai_upstream_error`. Respons akhir ini memuat `route` dan `score`. Karena itu kegagalan upstream utama yang diikuti key sekunder kosong dapat tetap menghasilkan 503; tidak diubah menjadi aturan error baru.

### Content-Type dan penyebutan 415 di SESSION-6

Tidak ada pembacaan `content-type`, error `unsupported_media_type`, atau kode 415 pada `_old/api/ask.js`. Harness menjalankan file lama secara langsung dan route baru pada kasus yang setara: body JSON valid tanpa Content-Type eksplisit atau dengan `text/plain`, `application/xml`, `application/octet-stream`, dan `application/json; charset=utf-8` tetap diparse sebagai string JSON dan berhasil; body `question=distilasi` menghasilkan 400 `question_required`. Seluruh **10 perbandingan** ini cocok, tanpa respons 415.

Ini membuktikan paritas **handler sumber**, bukan meniru seluruh body parser otomatis/penolakan request milik hosting Vercel lama. Penolakan pada lapisan platform, body parser form/biner otomatis, batas ukuran request, dan perilaku HTTP server nyata tetap perlu diperiksa operator pada preview. Menambahkan validasi 415 sendiri akan mengubah perilaku yang benar-benar ada di file sumber, sehingga tidak dilakukan.

## Sitemap, robots, dan cache

Ketiga salinan sitemap/robots/environment dibandingkan sebagai byte, termasuk newline dan komentar: **3/3 identik**. Sitemap tetap memuat **184 URL** dan domain, slash, urutan, serta metadata XML yang sama. Robots tetap mengizinkan semua crawler dan menunjuk `https://ilmutekkim.vercel.app/sitemap.xml`. Tidak menambahkan generator metadata `sitemap.js` atau `robots.js` yang berpotensi mengganti isinya.

`headers()` menghasilkan satu rule untuk `/assets/:path*` dengan `Cache-Control: public, max-age=31536000, immutable`, sama dengan nilai `_old/vercel.json`. Matcher Next terpasang diuji pada sembilan path: `/assets`, `/assets/`, gambar bertingkat, video, CSS cocok; prefix `/assets-other`, indeks pencarian Kamus, API, dan root tidak cocok. Tidak mengubah konfigurasi lain dan tidak memasang cache tersebut pada respons API atau JSON Kamus.

## Verifikasi lokal

Harness sementara menggunakan Node yang sudah tersedia, `vm.SourceTextModule` untuk memuat file ESM route **utuh tanpa mengubah source**, `vm` untuk menjalankan CommonJS lama, serta Web `Request`/`Response` Node. Setiap pasangan memakai environment terisolasi berisi key dummy, jam/timer terkontrol, dan mock fetch; tidak membaca key deployment atau memakai jaringan. Timer abort disimulasikan langsung tanpa menunggu 20 detik. Peringatan eksperimental Node untuk VM Modules tidak menyebabkan kegagalan.

**421/421 perbandingan perilaku lulus.** Setiap perbandingan mencocokkan kode status dan seluruh isi JSON, serta urutan, URL, metode, header, dan body semua panggilan upstream. Signal abort dan pembersihan timer turut diperiksa. Kasus utama juga memiliki assertion eksplisit untuk hasil yang diminta, tidak hanya saling membandingkan implementasi.

| Kelompok pengujian | Perbandingan lulus |
| --- | ---: |
| Simple tanpa key Gemini → DeepSeek fallback; kompleks langsung DeepSeek; kompleks tanpa key DeepSeek → Gemini fallback | 3 |
| Override model Gemini dan string override kosong | 2 |
| Body kosong/JSON rusak/null/nonobjek/pertanyaan hilang atau bukan string | 11 |
| Body objek legacy versus JSON request baru yang setara | 5 |
| Batas 499/500/501 dan trim sebelum batas | 4 |
| Tiga level, fallback, dan nilai level lainnya yang diterima sumber | 13 |
| 405 dan pesan lama pada enam metode selain POST | 6 |
| Perilaku Content-Type sumber; tidak ada 415 | 10 |
| Tanpa key, urutan validasi/key, kegagalan saat salah satu key kosong | 6 |
| HTTP 401/429/500, jaringan, timeout, JSON invalid, struktur hilang, jawaban kosong, dua arah | 32 |
| Seluruh 58 frasa sinyal × tiga level | 174 |
| Seluruh satuan regex dan angka tanpa satuan | 22 |
| Batas panjang/kata, multi-pertanyaan, sinonim tidak menumpuk | 16 |
| Skor 3/4/5 di sekitar ambang | 3 |
| Request ke-21, IP terpisah, IP pertama dalam rantai, kedaluwarsa sebelum/tepat batas | 25 |
| POST invalid tetap menghabiskan kuota, dengan/tanpa key | 42 |
| Header IP tidak ada/kosong berbagi bucket unknown | 21 |
| Penolakan metode tidak menghabiskan kuota POST | 26 |

Pemeriksaan tambahan:

- Inventaris route aktual dihitung dari `page.js` dan hasil `generateStaticParams()` kode proyek, lalu dibandingkan dengan seluruh direktori HTML lama: **185/185 halaman**, tanpa tambahan/hilang. Tujuh route parameter menghasilkan 61 artikel, 32 video, 48 istilah, 3 sektor, 19 riset, 5 paten, dan 7 jalur; `dynamicParams = false` dan `force-static` tetap ada.
- Seluruh **184/184 URL sitemap** unik dan mempunyai route. Selisih satu halaman ialah stub `/glosarium`, yang memang tidak masuk sitemap lama. Angka 237 dalam dokumen sesi sebelumnya tetap bukan inventaris aktual; tidak menambahkan halaman buatan.
- Hanya ada satu file route API, `/api/ask`, dengan ekspor metode/runtime/dynamic yang benar. Tidak memeriksa ulang DOM seluruh halaman karena berkasnya tidak berubah; hasil paritas konten sebelumnya tetap ada di NOTES-1 sampai NOTES-5.
- Snapshot SHA-256 sebelum/sesudah: **677/678 berkas yang telah ada tetap identik**; satu perubahan yang diizinkan adalah `next.config.mjs`. Ini mencakup **296/296 `_old/`**, seluruh input `_sources/`, src/public lama, catatan sesi lama, package/lockfile, dan konfigurasi lain. Tidak menggunakan metadata Git yang tidak tersedia sebagai repository kerja sesi ini.

Berkas pengujian/hasil sementara (bukan file proyek/dependensi):

```text
/tmp/ilmutekkim-session-6-before.json
/tmp/ilmutekkim-session-6-api.cjs
/tmp/ilmutekkim-session-6-api-results.json
/tmp/ilmutekkim-session-6-final.cjs
/tmp/ilmutekkim-session-6-final-results.json
/tmp/ilmutekkim-session-6-notes.py
/tmp/ilmutekkim-session-6-integrity.json
```

Perintah uji yang dijalankan: `node --experimental-vm-modules /tmp/ilmutekkim-session-6-api.cjs`, `node /tmp/ilmutekkim-session-6-final.cjs`, dan pemeriksaan byte/hash menggunakan Python. Validator inventaris memanfaatkan loader Babel/React sementara Sesi 4 yang sudah tersedia untuk membaca modul halaman dan static params; tidak menjalankan bundler, build Next, atau server. `node_modules`, `package-lock.json`, dan `.next` telah ada sebelum Sesi 6.

## Inventaris lengkap proyek final

Daftar berikut memuat **238 berkas** aplikasi, konfigurasi, lockfile, serta dokumen kerja di root; termasuk **219 berkas `src/` dan `public/`**. Setiap berkas disebut eksplisit, tanpa wildcard. Direktori `_old/` dan `_sources/` adalah arsip input yang dipertahankan, bukan file aplikasi deployment, sehingga tidak diduplikasi dalam daftar ini. `node_modules/`, `.next/`, direktori metadata/mount lingkungan `.git/`, `.agents/`, `.codex/`, `.aws/`, dan harness `/tmp/` juga bukan source proyek final. Aset biner operator belum tersedia di `public/assets/` dan tidak dikarang sebagai entri inventaris.

```text
.env.example
.gitignore
BRIEF.md
NOTES-1.md
NOTES-2.md
NOTES-3.md
NOTES-4.md
NOTES-5.md
NOTES-6.md
SESSION-1.md
SESSION-2.md
SESSION-3.md
SESSION-4.md
SESSION-5.md
SESSION-6.md
jsconfig.json
next.config.mjs
package-lock.json
package.json
public/.gitkeep
public/kamus/search-index.json
public/robots.txt
public/sitemap.xml
src/app/api/ask/route.js
src/app/artikel/[slug]/page.js
src/app/chat.css
src/app/globals.css
src/app/glosarium/page.js
src/app/jalur/[slug]/page.js
src/app/jalur/page.js
src/app/kalkulator/page.js
src/app/kamus/istilah/[slug]/page.js
src/app/kamus/kamus.css
src/app/kamus/layout.js
src/app/kamus/page.js
src/app/kamus/sektor/[slug]/page.js
src/app/layout.js
src/app/not-found.js
src/app/page.js
src/app/referensi/page.js
src/app/riset/[slug]/page.js
src/app/riset/page.js
src/app/riset/paten/[slug]/page.js
src/app/riset/paten/page.js
src/app/tentang/page.js
src/app/video/[slug]/page.js
src/app/video/page.js
src/components/ArticleBody.jsx
src/components/ArticleParts.jsx
src/components/ArticlePost.jsx
src/components/CalculatorInteractions.jsx
src/components/ChatWidget.jsx
src/components/Footer.jsx
src/components/Header.jsx
src/components/HomeCard.jsx
src/components/HomeInteractions.jsx
src/components/KamusLevels.jsx
src/components/KamusSearch.jsx
src/components/KamusShell.jsx
src/components/KamusTerm.jsx
src/components/KamusTermCard.jsx
src/components/LearningIntro.jsx
src/components/LearningPath.jsx
src/components/PatentIntro.jsx
src/components/ReferenceIntro.jsx
src/components/ResearchFilters.jsx
src/components/ResearchIndex.jsx
src/components/ResearchIntro.jsx
src/components/ResearchPost.jsx
src/components/VideoInteractions.jsx
src/components/VideoPost.jsx
src/data/articles/deep/b40-biodiesel-sawit-transesterifikasi.json
src/data/articles/deep/baca-pid-lima-simbol-pabrik.json
src/data/articles/deep/batch-vs-continuous-pabrik.json
src/data/articles/deep/batu-kapur-ke-semen-kiln.json
src/data/articles/deep/bbm-dari-sampah-plastik-pirolisis.json
src/data/articles/deep/bhopal-1984-lapisan-pengaman-yang-mati.json
src/data/articles/deep/boiler-meledak-lahirnya-katup-pengaman.json
src/data/articles/deep/coffey-still-1830-distilasi-kontinu.json
src/data/articles/deep/control-room-dcs-loop-kontrol.json
src/data/articles/deep/cooling-tower-cara-kerja.json
src/data/articles/deep/cooling-tower-wet-bulb-range-approach.json
src/data/articles/deep/cs01-step-growth-carothers-dp-runtuh.json
src/data/articles/deep/cs02-mccabe-thiele-garis-operasi.json
src/data/articles/deep/cs03-reflux-minimum-jebakan-mahal.json
src/data/articles/deep/cs04-fouling-lmtd-meleset.json
src/data/articles/deep/cs05-azeotrop-etanol-956.json
src/data/articles/deep/cs06-purge-recycle-gas-inert.json
src/data/articles/deep/cs07-pompa-kompresor-versi-ujian.json
src/data/articles/deep/cs08-cooling-tower-wet-bulb-ujian.json
src/data/articles/deep/cs09-batch-vs-cstr-volume.json
src/data/articles/deep/cs10-pid-sepuluh-simbol-ujian.json
src/data/articles/deep/cs11-relief-set-pressure-mawp.json
src/data/articles/deep/cs12-gliserol-satu-ton-cpo.json
src/data/articles/deep/cs13-raoult-kesetimbangan-uap-cair.json
src/data/articles/deep/cs14-absorpsi-vs-stripping-kremser.json
src/data/articles/deep/desuperheater-uap-disemprot-air.json
src/data/articles/deep/distilasi-bertingkat-minyak-mentah.json
src/data/articles/deep/flame-arrestor-lampu-davy-1815.json
src/data/articles/deep/flixborough-sketsa-kapur-manajemen-perubahan.json
src/data/articles/deep/gas-alam-ke-urea-haber-bosch.json
src/data/articles/deep/heat-exchanger-bikin-shutdown.json
src/data/articles/deep/ipal-tujuh-tahap-air-limbah.json
src/data/articles/deep/kavitasi-pompa-gelembung-mengeruk-baja.json
src/data/articles/deep/level-apd-kelas-cedera.json
src/data/articles/deep/molecular-sieve-mengeringkan-gas.json
src/data/articles/deep/naphtha-ke-plastik-petrokimia.json
src/data/articles/deep/near-miss-hampir-celaka-wajib-lapor.json
src/data/articles/deep/neraca-massa-data-pabrik-bocor.json
src/data/articles/deep/oleokimia-sawit-sabun-deterjen.json
src/data/articles/deep/pabrik-kelapa-sawit-tandan-ke-cpo.json
src/data/articles/deep/permit-to-work-kerja-panas.json
src/data/articles/deep/pigging-membersihkan-pipa-dari-dalam.json
src/data/articles/deep/polimerisasi-konversi-carothers.json
src/data/articles/deep/pompa-vs-kompresor.json
src/data/articles/deep/preventive-maintenance-bongkar-terjadwal.json
src/data/articles/deep/pulp-kertas-proses-kraft.json
src/data/articles/deep/refinery-sawit-cpo-ke-minyak-goreng.json
src/data/articles/deep/reflux-optimum-kolom-distilasi.json
src/data/articles/deep/roadmap-enam-mata-kuliah-pabrik.json
src/data/articles/deep/safety-instrumented-system-lapisan-pengaman.json
src/data/articles/deep/satu-barel-minyak-jadi-apa.json
src/data/articles/deep/satuan-tekanan-torricelli-titik-nol.json
src/data/articles/deep/seligman-1923-plate-heat-exchanger.json
src/data/articles/deep/tebu-ke-gula-pabrik-gula.json
src/data/articles/deep/tekanan-relief-valve-rupture-disk.json
src/data/articles/deep/texas-city-2005-informasi-yang-hilang.json
src/data/articles/deep/thermocouple-seebeck-1821.json
src/data/articles/deep/toolbox-meeting-lima-menit-menyelamatkan-nyawa.json
src/data/articles/deep/utilitas-pabrik-steam-air-nitrogen.json
src/data/articles/deep/warna-pipa-bahasa-peringatan.json
src/data/articles/deep/water-hammer-palu-air-pipa.json
src/data/articles/drafts/2026-10-03-cooling-tower-buku.json
src/data/articles/drafts/spec-real.json
src/data/articles/manifest.json
src/data/articles/sources.js
src/data/articles/specs/2026-09-30-carousel-1.json
src/data/articles/specs/2026-09-30-carousel-2-rev4.json
src/data/articles/specs/2026-09-30-carousel-3.json
src/data/articles/specs/2026-10-01-bbm-plastik.json
src/data/articles/specs/2026-10-01-carousel-1.json
src/data/articles/specs/2026-10-01-carousel-2.json
src/data/articles/specs/2026-10-01-carousel-3-rev2.json
src/data/articles/specs/2026-10-02-carousel-1.json
src/data/articles/specs/2026-10-02-carousel-2-rev.json
src/data/articles/specs/2026-10-02-carousel-3.json
src/data/articles/specs/2026-10-03-advanced-polimerisasi.json
src/data/articles/specs/2026-10-03-carousel-1.json
src/data/articles/specs/2026-10-03-carousel-2.json
src/data/articles/specs/2026-10-03-carousel-3.json
src/data/articles/specs/2026-10-04-carousel-1.json
src/data/articles/specs/2026-10-04-carousel-2.json
src/data/articles/specs/2026-10-04-carousel-3.json
src/data/articles/specs/2026-10-05-carousel-1.json
src/data/articles/specs/2026-10-05-carousel-2.json
src/data/articles/specs/2026-10-05-carousel-3.json
src/data/articles/specs/2026-10-06-carousel-1.json
src/data/articles/specs/2026-10-06-carousel-2-rev.json
src/data/articles/specs/2026-10-06-carousel-3.json
src/data/articles/specs/2026-10-07-roadmap-1.json
src/data/articles/specs/2026-10-08-carousel-1.json
src/data/articles/specs/2026-10-08-carousel-2.json
src/data/articles/specs/2026-10-09-carousel-1.json
src/data/articles/specs/2026-10-09-carousel-2.json
src/data/articles/specs/2026-10-10-carousel-1.json
src/data/articles/specs/2026-10-10-carousel-2.json
src/data/articles/specs/2026-10-11-carousel-1.json
src/data/articles/specs/2026-10-11-carousel-2.json
src/data/articles/specs/2026-10-12-carousel-1.json
src/data/articles/specs/2026-10-12-carousel-2.json
src/data/articles/specs/2026-10-13-carousel-1.json
src/data/articles/specs/2026-10-13-carousel-2.json
src/data/articles/specs/2026-10-14-carousel-1.json
src/data/articles/specs/2026-10-14-carousel-2.json
src/data/articles/specs/2026-10-15-carousel-1-rev2.json
src/data/articles/specs/2026-10-15-carousel-2.json
src/data/articles/specs/2026-10-16-carousel-1-repost-tex2.json
src/data/articles/specs/2026-10-16-carousel-2.json
src/data/articles/specs/2026-10-17-carousel-1.json
src/data/articles/specs/2026-10-17-carousel-2.json
src/data/articles/specs/2026-10-18-carousel-1.json
src/data/articles/specs/2026-10-18-carousel-2.json
src/data/articles/specs/2026-10-19-carousel-1.json
src/data/articles/specs/2026-10-19-carousel-2.json
src/data/articles/specs/2026-10-20-carousel-1.json
src/data/articles/specs/2026-10-20-carousel-2.json
src/data/articles/specs/2026-10-21-carousel-1.json
src/data/articles/specs/2026-10-21-carousel-2.json
src/data/articles/specs/2026-10-22-carousel-2.json
src/data/articles/specs/2026-10-23-carousel-1.json
src/data/articles/specs/2026-10-23-carousel-2.json
src/data/articles/specs/2026-10-24-carousel-1.json
src/data/articles/specs/2026-10-24-carousel-2.json
src/data/home.json
src/data/kamus/basic-terms.json
src/data/kamus/page-metadata.json
src/data/kamus/sectors.json
src/data/kamus/terms.json
src/data/page-metadata.json
src/data/static-pages/assets.json
src/data/static-pages/glosarium.json
src/data/static-pages/jalur.json
src/data/static-pages/page-metadata.json
src/data/static-pages/paten/paten-distilasi-reaktif-eastman-1984.json
src/data/static-pages/paten/paten-dividing-wall-column-basf-2005.json
src/data/static-pages/paten/paten-membran-monsanto-1980.json
src/data/static-pages/paten/paten-mtg-mobil-1988.json
src/data/static-pages/paten/paten-psa-skarstrom-1960.json
src/data/static-pages/research/bedah-b100-mesin-diesel.json
src/data/static-pages/research/bedah-bentonit-sonikasi-katalis-asam.json
src/data/static-pages/research/bedah-biodiesel-minyak-campuran.json
src/data/static-pages/research/bedah-biogas-pome-listrik-tekno-ekonomi.json
src/data/static-pages/research/bedah-ccus-tekno-ekonomi.json
src/data/static-pages/research/bedah-daur-ulang-plastik-kimia.json
src/data/static-pages/research/bedah-digital-twin-energi-industri.json
src/data/static-pages/research/bedah-elektrolisis-hidrogen-hijau.json
src/data/static-pages/research/bedah-esterifikasi-pome-katalis-karbon-zeolit.json
src/data/static-pages/research/bedah-fotokatalis-tio2-air-terproduksi.json
src/data/static-pages/research/bedah-grading-sawit-yolov4.json
src/data/static-pages/research/bedah-hidrogen-biru-smr-atr-ngd.json
src/data/static-pages/research/bedah-hydrocracking-minyak-jelantah-biogasoline.json
src/data/static-pages/research/bedah-katalis-aaem-pirolisis-biomassa.json
src/data/static-pages/research/bedah-katalis-cao-indigofera-biodiesel.json
src/data/static-pages/research/bedah-ko-pirolisis-batang-sawit-polipropilena.json
src/data/static-pages/research/bedah-mikroalga-pome-biofuel.json
src/data/static-pages/research/bedah-minyak-pirolisis-plastik-umpan-steam-cracker.json
src/data/static-pages/research/bedah-nanozirconia-tersulfat-hydrocracking.json
src/data/static-pages/sources.js
src/data/video-articles.json
src/data/video-assets.json
src/data/videos.json
src/lib/articles.js
src/lib/calculators.js
src/lib/content.js
src/lib/kamus.js
src/lib/pageMetadata.js
src/lib/staticPages.js
src/lib/videos.js
```

## Sisa risiko dan serah terima operator

1. **Build dan SSG:** operator masih perlu menjalankan instalasi/build di lingkungan yang ditentukan dan memeriksa output route. Pengujian source/Request/Response/static params ini tidak membuktikan kompilasi Next, hidrasi, atau perilaku hosting. Halaman tetap memakai SSG; hanya `/api/ask` yang sengaja dinamis dan runtime Node. Tidak memakai static export yang akan meniadakan API.
2. **Preview/browser:** periksa tema awal, mobile/menu/filter, video/kuis, canvas kalkulator, Kamus/pemilih level/pencarian, dan chat pada desktop/mobile. Uji alur indeks lokal terlebih dahulu, lalu AI fallback, label model, error tanpa key, dan rate limit melalui HTTP nyata. Isi environment deployment di luar `.env.example`; key tidak pernah diisi di repository. Ketersediaan/otorisasi model default dan respons provider nyata belum diuji, karena sesi ini tanpa key asli dan konstanta harus dipertahankan.
3. **Crawl paritas:** crawl seluruh 184 URL sitemap + `/glosarium`, bandingkan status, redirect slash, metadata/canonical/OG, internal link, serta file gambar/video. Sitemap/robots/domain canonical yang bercampur `ilmutekkim.vercel.app` dan `ilmutekkim.site` dipertahankan sesuai sumber. Tautan lama menuju `/artikel/` masih ada meski tidak terdapat halaman indeks tersebut pada HTML/sitemap lama; tidak menambah URL atau memperbaiki copy/href Sesi 1–5.
4. **Aset dan cache:** operator menempatkan biner asli pada `public/assets/`, kemudian memeriksa header HTTP cache sesungguhnya di preview/deployment dan integrasi CDN. Dua source video kosong, lima placeholder kartu beranda, dan dua spec pilot tidak tersedia tetap sesuai sumber/NOTES-2 dan NOTES-3. Sesi ini tidak mengisi media yang hilang atau mengubah resolver.
5. **Navigasi dan styling:** risiko CSS global Kamus yang dapat bertahan sesudah navigasi klien, tambahan font/footer Kamus, dan urutan stylesheet tetap seperti NOTES-4. Periksa Kamus ↔ halaman utama di browser. Larangan mengubah berkas Sesi 1–5 dipatuhi.
6. **API/hosting:** rate limit tetap per instance, dapat reset saat cold start, dan tidak menyatukan kuota lintas instance. Identitas IP bergantung pada `x-forwarded-for` hosting; header kosong memakai bucket bersama `unknown`. Perilaku parser/request limits platform lama, respons HEAD di jaringan, dan ketiadaan 415 perlu diverifikasi di preview bila diperlukan. Ini batas paritas handler yang dipertahankan, bukan perubahan infrastruktur yang dikerjakan sesi ini.

Tidak ada pekerjaan implementasi dalam cakupan Sesi 6 yang tertinggal. Selisih spesifikasi 415 dicatat berdasarkan sumber dan dibuktikan dengan perbandingan; build, preview, layanan AI nyata, penempatan aset, dan crawl deployment tetap tugas operator.
