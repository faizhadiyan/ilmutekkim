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
