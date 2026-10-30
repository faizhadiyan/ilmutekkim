# BUILD REPORT — Kamus Industri Kimia IlmuTekkim (MVP)

Tanggal build: 2026-10-29 · Status: **selesai secara lokal, TIDAK di-push, TIDAK di-deploy** (sesuai instruksi).
`tools/build.py` dan halaman artikel/video/glosarium yang ada **tidak diubah**.

## Cara menjalankan ulang

```bash
python3 tools/build_kamus.py     # gate kedalaman berjalan di dalam build; gagal = build berhenti
python3 -m http.server           # pratinjau lokal dari root repo
```

## Berkas yang dibuat

| Berkas | Fungsi |
|---|---|
| `kamus-data/terms.json` | 20 entri kamus dalam (sumber kebenaran konten) |
| `kamus-data/sectors.json` | 3 sektor + 6 kategori fondasi + peta sektor-istilah |
| `tools/build_kamus.py` | Generator mandiri (Python, tanpa dependensi) + gate kedalaman mekanis |
| `kamus/index.html` | Beranda search-first: pencarian besar, kartu sektor + hitungan, chip fondasi, istilah populer, daftar per fondasi |
| `kamus/sektor/{oleokimia,kilang-migas,petrokimia}/index.html` | Halaman sektor: diagram alur proses horizontal yang simpulnya tertaut ke halaman istilah, bahan/produk, daftar istilah sektor |
| `kamus/istilah/<slug>/index.html` (20 halaman) | Halaman istilah: breadcrumb, lapis 0, kontrol segmen Awam \| Tekkim \| Plant \| Semua (JS), tabel sensitivitas berpanah ↑/↓, badge "Glosarium terverifikasi", terkait, referensi + tanggal pembaruan |
| `kamus/search-index.json` | Indeks pencarian klien + data jawaban glosarium chatbot (20 istilah, 3 sektor) |
| `kamus/assets/kamus.css` | Gaya kamus: navy `#0B1B3F`, cyan `#00B4D8`, amber `#F59E0B`, Plus Jakarta Sans + Noto Sans, mobile-first |
| `kamus/assets/search.js` | Pencarian instan tergrup (Istilah/Sektor), cuplikan per hasil, peringkat judul persis > alias > isi, keadaan nol hasil yang menawarkan chatbot, pintasan `/` |
| `kamus/assets/chat.css` + `chat.js` | Pop-up **Tanya Tekkim**: tombol melayang berlabel kanan bawah, panel (HP: bottom sheet), chip level Awam/Tekkim/Plant, pertanyaan contoh, sitasi ke halaman istilah |
| `api/ask.js` | Fungsi serverless Vercel (Node, tanpa dependensi): POST `{question, level}`, model `deepseek-flash`, batas laju memori 20 req/10 menit per IP, panjang pertanyaan maks 500 |
| `.env.example` | Hanya `DEEPSEEK_API_KEY=` kosong. `.gitignore` yang ada sudah mengabaikan `.env`/`.env.*` dengan pengecualian `!.env.example` (tidak diubah). Tidak ada kunci asli di mana pun. |

## Jumlah entri per sektor dan fondasi

Sektor (istilah yang relevan; satu entri dapat melayani beberapa sektor):
- **Oleokimia: 14** · **Kilang & Migas: 14** · **Petrokimia: 15** (dari 20 entri unik)

Fondasi (rumah kanonis, tepat satu per entri):
- Unit Operasi & Separasi: 12 — distilasi, reflux, flooding, absorpsi/stripping, reaktor-konversi-selektivitas, splitting, transesterifikasi, hidrogenasi, CDU, FCC, steam cracking, polimerisasi
- Equipment: 3 — heat exchanger/LMTD, fouling, pompa-kavitasi-NPSH
- Utilitas & Energi: 2 — cooling tower, steam dan utilitas
- Lab & QC: 1 — FFA dan acid value
- Safety: 1 — relief valve
- Ekonomi Proses: 1 — neraca massa

## Checklist gate kedalaman per entri

Gate ditegakkan secara mekanis di `tools/build_kamus.py` (`depth_gate()`): build gagal apabila
satu entri pun kehilangan (1) mekanisme, (2) prinsip + persamaan ber-simbol dan ber-asumsi,
(3) variabel dengan rentang berlabel "rentang umum textbook, bukan data plant" + arah sensitivitas
dan efeknya, (4) kegagalan/batas operasi; ditambah lapis 0 (definisi + analogi), lapis plant
(biaya, checklist sebab-akibat, contoh hitungan), terkait yang ter-resolve, dan referensi.
Hasil build 2026-10-29: **20/20 entri LOLOS seluruh gate.**

| Entri | Mekanisme | Persamaan | Variabel + sensitivitas | Kegagalan | Plant + contoh hitungan |
|---|---|---|---|---|---|
| Distilasi | ✓ VLE per tray | ✓ K, volatilitas relatif | ✓ 3 | ✓ 4 | ✓ perbandingan alfa |
| Reflux | ✓ | ✓ R = L/D, R operasi vs Rmin | ✓ 2 | ✓ 3 | ✓ kenaikan beban vs R |
| Flooding | ✓ jet + downcomer | ✓ korelasi Fair | ✓ 3 | ✓ 3 | ✓ margin 80% banjir |
| Heat Exchanger dan LMTD | ✓ | ✓ Q = UA·ΔTlm, LMTD | ✓ 3 | ✓ 3 | ✓ A = 100 m², efek fouling |
| Fouling | ✓ 5 mekanisme | ✓ 1/U + Rf | ✓ 3 | ✓ 3 | ✓ U turun ±19% |
| Pompa, Kavitasi, dan NPSH | ✓ | ✓ NPSHa, margin | ✓ 3 | ✓ 3 | ✓ NPSHa ±10,6 m |
| Neraca Massa | ✓ | ✓ akumulasi, F = D + B | ✓ 3 | ✓ 3 | ✓ kehilangan 2 ton/hari |
| Reaktor, Konversi, Selektivitas | ✓ | ✓ X, Y = X·S | ✓ 3 | ✓ 3 | ✓ yield 72% vs 67,5% |
| Cooling Tower | ✓ evaporatif | ✓ range/approach, Q | ✓ 3 | ✓ 3 | ✓ beban ±5,8 MW |
| Absorpsi dan Stripping | ✓ | ✓ faktor A, Henry | ✓ 3 | ✓ 3 | ✓ Kremser ±97% |
| Steam dan Sistem Utilitas | ✓ | ✓ Q = m·hfg, nilai tabel uap | ✓ 3 | ✓ 3 | ✓ 7,2 ton/jam steam |
| Relief Valve | ✓ | ✓ p setel ≤ MAWP, akumulasi 110%/121% | ✓ 3 | ✓ 3 | ✓ MAWP 10 bar g |
| Splitting | ✓ 3 tahap | ✓ stoikiometri, derajat splitting | ✓ 3 | ✓ 3 | ✓ gliserin per 100 kg minyak |
| Transesterifikasi | ✓ | ✓ stoikiometri, rasio 6:1 | ✓ 3 | ✓ 3 | ✓ metanol per 1.000 kg minyak |
| FFA dan Acid Value | ✓ lipase/hidrolisis | ✓ AV titrasi, faktor 0,503 | ✓ 3 | ✓ 3 | ✓ AV 4,04 → FFA 2,03% |
| Hidrogenasi | ✓ | ✓ stoikiometri H₂ per ikatan rangkap | ✓ 3 | ✓ 3 | ✓ kebutuhan H₂ per 1.000 kg |
| Distilasi Atmosferik (CDU) | ✓ | ✓ gap/overlap fraksi | ✓ 3 | ✓ 3 | ✓ potongan rentang didih |
| FCC | ✓ riser-regenerator | ✓ definisi konversi, C/O | ✓ 3 | ✓ 3 | ✓ pola hasil tipikal |
| Steam Cracking | ✓ radikal bebas | ✓ skema pirolisis | ✓ 3 | ✓ 3 | ✓ pola perolehan olefin |
| Polimerisasi | ✓ chain vs step growth | ✓ Carothers + bentuk r | ✓ 3 | ✓ 3 | ✓ DP pada p = 0,90/0,99/0,999 |

Seluruh angka adalah rentang umum textbook (Perry's, Coulson & Richardson, Geankoplis,
Bailey's, Gunstone, Kister, API RP 520/521, literatur penyulingan dan polimer) dan dilabeli
demikian pada setiap variabel. Tidak ada data perusahaan/plant spesifik.

## Hasil verifikasi (2026-10-29, server statis lokal)

| Pemeriksaan | Hasil |
|---|---|
| `python3 tools/build_kamus.py` | OK — 25 berkas ter-generate, gate kedalaman lolos 20/20 |
| GET `/kamus/` | 200 (15.179 B) |
| GET `/kamus/sektor/oleokimia/` | 200 (7.093 B) |
| GET `/kamus/istilah/distilasi/` | 200 (9.495 B) — persamaan `<sub>` tampil, badge dan label textbook ditemukan |
| GET `/kamus/istilah/ffa-dan-acid-value/` | 200 (9.344 B) |
| GET `/kamus/search-index.json` | 200 — 20 istilah, 3 sektor, field chatbot lengkap |
| Diagram alur sektor kilang | 7 simpul, 14 tautan istilah unik ter-resolve |
| `node --check` chat.js, search.js, api/ask.js | sintaks OK |
| Harness Node `api/ask.js` tanpa kunci | GET → 405; POST valid → **503 `ai_not_configured`** ✓; pertanyaan kosong → 400; >500 karakter → 400; ledakan 21+ req/IP → **429 `rate_limited`** ✓ |

## Perilaku chatbot (sesuai rancangan)

1. Klien memuat `/kamus/search-index.json` lokal terlebih dahulu.
2. Kecocokan kuat (judul/alias/frasa judul di dalam pertanyaan, skor ≥ 70) dijawab dari entri
   glosarium pada lapis level terpilih, dengan chip sitasi "Baca entri lengkap" dan label
   "Sumber: Glosarium terverifikasi".
3. Tanpa kecocokan kuat, klien POST ke `/api/ask`; jawaban dilabeli **"AI — belum terverifikasi"**.
   Apabila server mengembalikan 503 `ai_not_configured`, panel menampilkan pesan penurunan
   layanan yang anggun dan mengarahkan ke pencarian kamus.

## Yang belum lengkap / catatan

- **Kunci DeepSeek belum terpasang** (disengaja): jalur AI langsung belum teruji terhadap API
  DeepSeek sesungguhnya. Parameter `thinking: {type: "disabled"}` disertakan sebagai upaya
  menonaktifkan mode berpikir; apabila penyedia menolak parameter tak dikenal (uji pertama
  dengan kunci asli), hapus blok tersebut dari `api/ask.js`.
- **Batas laju bersifat dalam memori per instans** serverless: memadai untuk MVP, bukan
  perlindungan produksi. Untuk produksi, ganti dengan penyimpanan bersama (mis. Vercel KV).
- **Belum di-push dan belum di-deploy** sesuai instruksi. Konsekuensi deploy yang perlu
  diketahui: Vercel akan mengambil `api/ask.js` sebagai fungsi `/api/ask` secara otomatis;
  halaman kamus ter-generate bersifat statis biasa.
- Navbar situs utama **tidak diubah** (tidak ada tautan "Kamus" baru), sesuai batas tugas.
  Kamus dapat ditemukan melalui URL langsung `/kamus/`.
- Sektor lain (Pupuk & Gas, Semen, Pulp & Kertas, Gula & Fermentasi, Air & Limbah) belum
  dibuka karena belum memiliki konten nyata, sesuai prinsip rancangan yang disetujui.
- Kata "Semua" pada kontrol segmen adalah pilihan keempat di samping Awam | Tekkim | Plant,
  untuk menampilkan seluruh lapis sekaligus; keadaan awal adalah Tekkim.

## Koreksi owner 2026-10-29 (site-wide)

Status: **selesai dan terverifikasi secara lokal; tidak di-push dan tidak di-deploy.** Detailed per-file injector log tersimpan di `staging/kamus-fix-log.json` (folder internal yang tidak ikut diterbitkan), termasuk daftar file per koreksi dan suplemen file generator/template.

### Koreksi 1 — Chatbot Tanya Tekkim di setiap halaman

- `kamus/assets/chat.js` terbukti mandiri: membuat tombol dan panel sendiri, memuat `/kamus/search-index.json` dengan path absolut, dan mengirim pertanyaan ke `/api/ask` dengan path absolut. Tidak ada path relatif yang perlu diperbaiki.
- Injector menambahkan `<link rel="stylesheet" href="/kamus/assets/chat.css">` sebelum `</head>` dan `<script defer src="/kamus/assets/chat.js"></script>` sebelum `</body>` pada **132 HTML non-Kamus** yang belum memiliki widget.
- **52 halaman Kamus** memperoleh widget dari `tools/build_kamus.py`; **1 halaman pengalihan Glosarium** memperolehnya dari template `tools/build.py` yang telah diperbarui. Total cakupan akhir: **185/185 HTML**.
- Audit akhir setiap file: referensi `chat.css` tepat 1, referensi `chat.js` tepat 1, Vercel Analytics tepat 1, `<title>` tepat 1, dan `</html>` tepat 1; tidak ada duplikasi.
- `tools/build.py` diperbarui mengikuti preseden Analytics: `HEAD` memuat stylesheet chat dan `FOOT` memuat script chat. `py_compile` lolos dan render test membuktikan masing-masing aset muncul tepat satu kali.

### Koreksi 2 — Kamus dan Glosarium menjadi satu

- `tools/build_kamus.py` sekarang juga membaca `glosarium.json`. Pencocokan tabrakan memakai nama/istilah ternormalisasi, slug, dan alias entri dalam.
- **19 istilah glosarium lama bertabrakan dengan entri dalam dan memakai entri dalam sebagai kanonis:** Reflux, Rasio reflux, Reflux minimum, LMTD, Fouling, Neraca massa, Relief valve, Rupture disk, Cooling tower, Range, Approach, Konversi, Selektivitas, Derajat polimerisasi, Steam trap, Kavitasi, NPSH, Transesterifikasi, dan Flooding.
- **28 istilah lain menjadi entri dasar:** Azeotrop, Batch, Blowdown, Bottoms, Continuous, DCS, Distilat, Flare, HAZOP, Kondensor, Loop kontrol, P&ID, Packing, Pengendali PID, Permit to work, Pinch, Proses kraft, Reboiler, Safety instrumented system, Seksi rectifying, Seksi stripping, SIL, Stoikiometri, Suhu wet bulb, Tahap kesetimbangan, Tray, Utilitas, dan Volatilitas relatif.
- Total katalog gabungan: **48 istilah = 20 entri dalam + 28 entri dasar**. Daftar lengkap A–Z tampil di beranda Kamus; `kamus/search-index.json` memuat 48 istilah dengan penanda `kind: "dalam"` atau `kind: "dasar"`.
- Setiap entri dasar memiliki halaman `/kamus/istilah/<slug>/` berisi definisi, bacaan terkait yang ter-resolve ke artikel/video/bedah paten yang benar, dan catatan persis: **“Entri dasar — bedah dalam (mekanisme, persamaan, sensitivitas) menyusul.”** Seluruh tautan bacaan terkait entri dasar terverifikasi menunjuk file yang ada (0 hilang).
- Chatbot dapat menjawab dari entri dasar dan melabelinya **“Sumber: Glosarium terverifikasi · Entri dasar”**. Gate kedalaman untuk 20 entri dalam tidak dilemahkan dan tetap lolos 20/20.
- Sebanyak **132 HTML standar** mengalami penulisan ulang tautan/label Glosarium oleh injector, ditambah `sitemap.xml`; 52 halaman Kamus di-generate ulang tanpa tautan lama. Audit akhir: **0** kemunculan `href="/glosarium` dan **0** label tautan `>Glosarium<` di seluruh HTML di luar `staging/`.
- `glosarium/index.html` diganti menjadi halaman pengalihan ke `/kamus` dengan meta refresh, canonical ke `/kamus/`, dan tautan fallback yang terlihat. Di `tools/build.py`, blok generator halaman Glosarium lama diganti generator pengalihan yang sama; tidak ada pola tautan `/glosarium` yang tersisa di `tools/build.py`. File `glosarium.json` tetap dipakai hanya sebagai sumber data penggabungan, bukan lagi halaman/sistem terpisah.
- `sitemap.xml`: 1 URL `/glosarium/` dihapus dan **52 URL Kamus** ditambahkan (1 beranda Kamus, 3 sektor, 48 istilah). Sitemap akhir memuat **184 URL unik**, tanpa URL Glosarium.

### Koreksi 3 — Navigasi menuju Kamus

- Injector menyisipkan `<a href="/kamus">Kamus</a>` tepat setelah tautan Jalur pada header **132 HTML standar**; halaman pengalihan sudah memilikinya dari template `tools/build.py` yang diperbarui.
- Footer standar: **133/133** halaman ber-`foot-links` kini memuat Kamus sebagai pengganti Glosarium.
- Beranda: item strip fitur 04 diubah dari Glosarium menjadi Kamus tanpa renumbering. Teksnya kini menyebut katalog gabungan **48 istilah: 20 entri dalam dan 28 entri dasar**.
- Halaman Kamus: tautan header di `tools/build_kamus.py` diselaraskan ke `<a href="/kamus">Kamus</a>`, dan footer Kamus ditambah nav berisi Kamus. Audit akhir: **185/185 HTML** memuat tautan navigasi persis tersebut setidaknya satu kali; **52/52 halaman Kamus** memuatnya juga di footer.
- `tools/build.py`: nav `HEAD` memuat Kamus setelah Jalur, footer `FOOT` mengganti Glosarium dengan Kamus, strip beranda memakai katalog Kamus gabungan, dan sitemap masa depan memuat Kamus beserta sektor dan seluruh istilahnya.

### Verifikasi lokal terakhir

| Pemeriksaan | Hasil |
|---|---|
| `python3 tools/build_kamus.py` | OK — 20 entri dalam, 28 entri dasar, 3 sektor; gate kedalaman 20/20 |
| `python3 -m py_compile tools/build.py tools/build_kamus.py` | OK |
| Render test `HEAD` + `FOOT` dari `tools/build.py` | chat CSS 1, chat JS 1, Analytics 1, nav/footer Kamus 2, tautan Glosarium 0 |
| `node --check kamus/assets/chat.js` dan `search.js` | OK |
| Server statis: `GET /` | 200; nav Kamus ada, strip 48 istilah ada, chat CSS/JS masing-masing 1 |
| Server statis: `GET /artikel/distilasi-bertingkat-minyak-mentah/` | 200; nav Kamus ada, chat CSS/JS masing-masing 1 |
| Server statis: `GET /glosarium/` | 200; meta refresh, canonical Kamus, dan fallback terlihat semua ada |
| Server statis: `GET /kamus/` dan `search-index.json` | 200; daftar A–Z 48; indeks 20 dalam + 28 dasar |
| Server statis: `GET /kamus/istilah/azeotrop/` | 200; catatan entri dasar dan tautan bedah paten terkait tampil |

## Addendum 2026-10-30 — Router heuristik Tanya Tekkim (keputusan Hadi: heuristik dulu, tanpa Jev)

- `api/ask.js` ditulis ulang: setelah glosarium lokal, pertanyaan dinilai router heuristik skor lokal (kelompok sinyal: angka+satuan +3, hitung +3, persamaan/mekanisme +3, mode gagal/gejala +3, diagnosis +3, bandingkan +2, level plant +2 / tekkim +1, sebab-akibat +1, panjang/multi-pertanyaan +1; ambang kompleks >= 4).
- Simple -> Gemini `gemini-3.5-flash-lite` (REST v1beta generateContent, header `x-goog-api-key`, env `GEMINI_API_KEY`, model dapat diganti via env `GEMINI_MODEL`). Kompleks -> DeepSeek `deepseek-flash` (env `DEEPSEEK_API_KEY`, tidak berubah).
- Fallback dua arah: kegagalan/429/kunci hilang di penyedia utama -> penyedia cadangan; tanpa kedua kunci -> 503 `ai_not_configured` (perilaku lama). Respons menambah `route`, `router: "heuristic"`, `score`, `reasons`, `fallback`; label UI kini menampilkan nama model yang menjawab.
- Bias router disengaja ke kompleks: salah lempar ke DeepSeek rugi biaya sangat kecil; salah lempar hitungan/diagnosis ke model ringan berisiko jawaban dangkal.
- Uji lokal (harness Node, fetch stub): klasifikasi 10/10 contoh lolos (termasuk flooding, kavitasi, hitung steam 1000 kg/h, PSV lifting), routing simple->Gemini, kompleks->DeepSeek, fallback Gemini 429->DeepSeek, hanya-Gemini kompleks->fallback Gemini, tanpa key->503, pertanyaan kosong->400. Semua lolos.
- SISA: `GEMINI_API_KEY` belum dipasang di Vercel Production — selama belum dipasang, pertanyaan simple otomatis fallback ke DeepSeek (chatbot tetap berfungsi penuh seperti sebelumnya).
