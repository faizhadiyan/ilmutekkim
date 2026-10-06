# ilmutekkim

Website arsip baca untuk konten teknik kimia Instagram
[@ilmutekkim](https://www.instagram.com/ilmutekkim): pabrik, proses, safety, dan AI.
Ditulis insinyur kimia ITB.

Setiap artikel di situs ini adalah versi baca (teks utuh) dari carousel Instagram
@ilmutekkim, dibedah tahap demi tahap: miskonsepsi, kenyataan proses, diagram alur,
contoh nyata di industri Indonesia, dan referensinya.

## Isi

- 25 artikel lengkap (distilasi, reflux, P&ID, kilang, sawit, biodiesel B40,
  petrokimia, cooling tower, urea Haber-Bosch, neraca massa, oleokimia,
  batch vs continuous, gula, utilitas, semen, safety instrumented system,
  pulp kraft, permit to work, dan lainnya)
- Filter per seri dan pencarian artikel
- Halaman tentang

## Teknologi

Situs statis murni (HTML, CSS, JS) tanpa build step, di-host di Vercel (free tier).
Halaman digenerate dari spec konten carousel oleh `tools/build.py`:

```bash
python3 tools/build.py
```

Identitas visual mengikuti @ilmutekkim: navy `#0B1B3F`, cyan `#00B4D8`,
amber `#F59E0B`, font Plus Jakarta Sans dan Noto Sans.

## Deploy

Repo ini terhubung ke Vercel: setiap push ke `main` otomatis ter-deploy.
Konfigurasi ada di `vercel.json` (clean URL, cache aset statis).

## Kredit foto

Foto berasal dari Pexels dan Unsplash; kredit tercantum di tiap gambar.
