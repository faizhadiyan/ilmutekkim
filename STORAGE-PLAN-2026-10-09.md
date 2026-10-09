# Rencana Storage Video Website ilmutekkim — untuk keputusan Hadi

Dibuat 2026-10-09 (proactive research). Belum ada yang diubah di situs live.

## Fakta terukur (cek lokal 2026-10-09 09:34 WIB)
- Folder situs lokal: 31 MB total.
- `assets/video/`: 14 MB untuk 10 video MP4 (720p CRF28) + 10 poster JPG. Rata-rata ±1,3-1,4 MB per video.
- Ritme produksi: 1 motion graphics per hari → tambahan ±0,5 GB per tahun.
- Repo GitHub `faizhadiyan/ilmutekkim` nyaman di bawah 1 GB; di ritme sekarang ambang 1 GB tercapai dalam ±2 tahun. Batas keras per file GitHub 100 MB tidak relevan (file kita ±1,4 MB).

## Opsi

### A. Tetap di GitHub (status quo)
- Biaya Rp0, nol pekerjaan sekarang.
- Konsekuensi: repo makin berat, clone/deploy makin lambat; dalam ±2 tahun perlu migrasi dalam keadaan terdesak, bukan terencana.

### B. Cloudflare R2 (rekomendasi)
- Free tier resmi (developers.cloudflare.com/r2/pricing/, dicek 2026-10-09): 10 GB storage/bulan, 1 juta operasi Class A, 10 juta Class B, egress gratis. Di atas free tier: $0,015/GB/bulan.
- 10 GB free tier = ±7.000 video ukuran sekarang, atau >10 tahun ritme 1 video/hari, sebelum bayar sepeser pun.
- Pekerjaan migrasi (perkiraan 1 sesi): buat bucket R2 + custom domain (mis. `video.ilmutekkim...` atau subdomain), upload 10 MP4 + poster, ubah `tools/build.py` agar URL video menunjuk R2, hapus MP4 dari repo, deploy ulang, verifikasi 10 halaman video live.
- Risiko: perlu akun Cloudflare + kartu/payment method untuk aktivasi R2 (Cloudflare mensyaratkan payment method meski free tier). Ini langkah yang hanya bisa dilakukan Hadi.

### C. Git LFS / Releases
- Menambah kompleksitas deploy Vercel tanpa menyelesaikan akar masalah hosting video di repo kode. Tidak direkomendasikan.

## Rekomendasi
Pilih B, tapi eksekusinya tidak mendesak hari ini: kerjakan saat Hadi punya 15 menit untuk aktivasi Cloudflare + payment method, sisanya asisten yang kerjakan. Sampai saat itu opsi A aman (±2 tahun ruang napas).

## Keputusan yang dibutuhkan dari Hadi (satu baris)
1. `R2 sekarang` — Hadi aktivasi Cloudflare R2, asisten migrasi + verifikasi.
2. `Nanti saja` — tetap GitHub, asisten catat pengingat ambang 500 MB repo.
