# NOTES-3 — Artikel dan video

Inventaris awal: seluruh `_old/tools/build.py` (2.093 baris) telah dibaca. Semua 61 artikel memakai override `render_deep_body`, termasuk dua artikel arsip. Semua 32 video memakai `render_video_article`; indeks `/video/` memakai loop kartu video. Tidak ada tipe halaman tambahan.

Dua spec pilot tidak tersedia di `_sources/`: `real-photo-pilot/spec-pilot-001-kavitasi.json` dan `real-photo-pilot/spec-pilot-002-waterhammer.json`. Isi artikel tersedia lengkap di deep JSON; data tampilan yang diperlukan diambil eksplisit dari HTML jadi, tanpa menebak spec.

## Peta 61 artikel

Kolom tipe juga mencatat jalur spec awal sebelum ditimpa deep.

| Slug | Tipe rendering | Sumber data |
| --- | --- | --- |
| `distilasi-bertingkat-minyak-mentah` | deep + before_after | `_old/deep/distilasi-bertingkat-minyak-mentah.json` + `_sources/specs/2026-09-30-carousel-1.json` |
| `reflux-optimum-kolom-distilasi` | deep + slides | `_old/deep/reflux-optimum-kolom-distilasi.json` + `_sources/spec-real.json` |
| `pabrik-kelapa-sawit-tandan-ke-cpo` | deep + slides | `_old/deep/pabrik-kelapa-sawit-tandan-ke-cpo.json` + `_sources/specs/2026-09-30-carousel-2-rev4.json` |
| `baca-pid-lima-simbol-pabrik` | deep + before_after | `_old/deep/baca-pid-lima-simbol-pabrik.json` + `_sources/specs/2026-09-30-carousel-3.json` |
| `refinery-sawit-cpo-ke-minyak-goreng` | deep + slides | `_old/deep/refinery-sawit-cpo-ke-minyak-goreng.json` + `_sources/specs/2026-10-01-carousel-1.json` |
| `heat-exchanger-bikin-shutdown` | deep + slides | `_old/deep/heat-exchanger-bikin-shutdown.json` + `_sources/specs/2026-10-01-carousel-2.json` |
| `b40-biodiesel-sawit-transesterifikasi` | deep + slides | `_old/deep/b40-biodiesel-sawit-transesterifikasi.json` + `_sources/specs/2026-10-01-carousel-3-rev2.json` |
| `bbm-dari-sampah-plastik-pirolisis` | deep + slides + arsip | `_old/deep/bbm-dari-sampah-plastik-pirolisis.json` + `_sources/specs/2026-10-01-bbm-plastik.json` |
| `tekanan-relief-valve-rupture-disk` | deep + slides | `_old/deep/tekanan-relief-valve-rupture-disk.json` + `_sources/specs/2026-10-02-carousel-1.json` |
| `satu-barel-minyak-jadi-apa` | deep + slides | `_old/deep/satu-barel-minyak-jadi-apa.json` + `_sources/specs/2026-10-02-carousel-2-rev.json` |
| `pompa-vs-kompresor` | deep + slides | `_old/deep/pompa-vs-kompresor.json` + `_sources/specs/2026-10-02-carousel-3.json` |
| `naphtha-ke-plastik-petrokimia` | deep + slides | `_old/deep/naphtha-ke-plastik-petrokimia.json` + `_sources/specs/2026-10-03-carousel-1.json` |
| `cooling-tower-cara-kerja` | deep + slides | `_old/deep/cooling-tower-cara-kerja.json` + `_sources/specs/2026-10-03-carousel-2.json` |
| `cooling-tower-wet-bulb-range-approach` | deep + slides | `_old/deep/cooling-tower-wet-bulb-range-approach.json` + `_sources/2026-10-03-cooling-tower-buku.json` |
| `gas-alam-ke-urea-haber-bosch` | deep + slides | `_old/deep/gas-alam-ke-urea-haber-bosch.json` + `_sources/specs/2026-10-03-carousel-3.json` |
| `polimerisasi-konversi-carothers` | deep + slides + arsip | `_old/deep/polimerisasi-konversi-carothers.json` + `_sources/specs/2026-10-03-advanced-polimerisasi.json` |
| `neraca-massa-data-pabrik-bocor` | deep + slides | `_old/deep/neraca-massa-data-pabrik-bocor.json` + `_sources/specs/2026-10-04-carousel-1.json` |
| `oleokimia-sawit-sabun-deterjen` | deep + slides | `_old/deep/oleokimia-sawit-sabun-deterjen.json` + `_sources/specs/2026-10-04-carousel-2.json` |
| `batch-vs-continuous-pabrik` | deep + slides | `_old/deep/batch-vs-continuous-pabrik.json` + `_sources/specs/2026-10-04-carousel-3.json` |
| `tebu-ke-gula-pabrik-gula` | deep + slides | `_old/deep/tebu-ke-gula-pabrik-gula.json` + `_sources/specs/2026-10-05-carousel-1.json` |
| `utilitas-pabrik-steam-air-nitrogen` | deep + slides | `_old/deep/utilitas-pabrik-steam-air-nitrogen.json` + `_sources/specs/2026-10-05-carousel-2.json` |
| `batu-kapur-ke-semen-kiln` | deep + slides | `_old/deep/batu-kapur-ke-semen-kiln.json` + `_sources/specs/2026-10-05-carousel-3.json` |
| `safety-instrumented-system-lapisan-pengaman` | deep + slides | `_old/deep/safety-instrumented-system-lapisan-pengaman.json` + `_sources/specs/2026-10-06-carousel-1.json` |
| `pulp-kertas-proses-kraft` | deep + slides | `_old/deep/pulp-kertas-proses-kraft.json` + `_sources/specs/2026-10-06-carousel-2-rev.json` |
| `permit-to-work-kerja-panas` | deep + slides | `_old/deep/permit-to-work-kerja-panas.json` + `_sources/specs/2026-10-06-carousel-3.json` |
| `roadmap-enam-mata-kuliah-pabrik` | deep + slides | `_old/deep/roadmap-enam-mata-kuliah-pabrik.json` + `_sources/specs/2026-10-07-roadmap-1.json` |
| `cs01-step-growth-carothers-dp-runtuh` | deep + slides | `_old/deep/cs01-step-growth-carothers-dp-runtuh.json` + `_sources/specs/2026-10-08-carousel-1.json` |
| `control-room-dcs-loop-kontrol` | deep + slides | `_old/deep/control-room-dcs-loop-kontrol.json` + `_sources/specs/2026-10-08-carousel-2.json` |
| `cs02-mccabe-thiele-garis-operasi` | deep + slides | `_old/deep/cs02-mccabe-thiele-garis-operasi.json` + `_sources/specs/2026-10-09-carousel-1.json` |
| `preventive-maintenance-bongkar-terjadwal` | deep + slides | `_old/deep/preventive-maintenance-bongkar-terjadwal.json` + `_sources/specs/2026-10-09-carousel-2.json` |
| `bhopal-1984-lapisan-pengaman-yang-mati` | deep + slides | `_old/deep/bhopal-1984-lapisan-pengaman-yang-mati.json` + `_sources/specs/2026-10-21-carousel-2.json` |
| `boiler-meledak-lahirnya-katup-pengaman` | deep + slides | `_old/deep/boiler-meledak-lahirnya-katup-pengaman.json` + `_sources/specs/2026-10-19-carousel-2.json` |
| `coffey-still-1830-distilasi-kontinu` | deep + slides | `_old/deep/coffey-still-1830-distilasi-kontinu.json` + `_sources/specs/2026-10-16-carousel-2.json` |
| `cs03-reflux-minimum-jebakan-mahal` | deep + slides | `_old/deep/cs03-reflux-minimum-jebakan-mahal.json` + `_sources/specs/2026-10-10-carousel-1.json` |
| `cs04-fouling-lmtd-meleset` | deep + slides | `_old/deep/cs04-fouling-lmtd-meleset.json` + `_sources/specs/2026-10-11-carousel-1.json` |
| `cs05-azeotrop-etanol-956` | deep + slides | `_old/deep/cs05-azeotrop-etanol-956.json` + `_sources/specs/2026-10-12-carousel-1.json` |
| `cs06-purge-recycle-gas-inert` | deep + slides | `_old/deep/cs06-purge-recycle-gas-inert.json` + `_sources/specs/2026-10-13-carousel-1.json` |
| `cs07-pompa-kompresor-versi-ujian` | deep + slides | `_old/deep/cs07-pompa-kompresor-versi-ujian.json` + `_sources/specs/2026-10-14-carousel-1.json` |
| `cs08-cooling-tower-wet-bulb-ujian` | deep + slides | `_old/deep/cs08-cooling-tower-wet-bulb-ujian.json` + `_sources/specs/2026-10-15-carousel-1-rev2.json` |
| `cs09-batch-vs-cstr-volume` | deep + slides | `_old/deep/cs09-batch-vs-cstr-volume.json` + `_sources/specs/2026-10-16-carousel-1-repost-tex2.json` |
| `cs10-pid-sepuluh-simbol-ujian` | deep + slides | `_old/deep/cs10-pid-sepuluh-simbol-ujian.json` + `_sources/specs/2026-10-17-carousel-1.json` |
| `cs11-relief-set-pressure-mawp` | deep + slides | `_old/deep/cs11-relief-set-pressure-mawp.json` + `_sources/specs/2026-10-18-carousel-1.json` |
| `cs12-gliserol-satu-ton-cpo` | deep + slides | `_old/deep/cs12-gliserol-satu-ton-cpo.json` + `_sources/specs/2026-10-19-carousel-1.json` |
| `cs13-raoult-kesetimbangan-uap-cair` | deep + slides | `_old/deep/cs13-raoult-kesetimbangan-uap-cair.json` + `_sources/specs/2026-10-20-carousel-1.json` |
| `cs14-absorpsi-vs-stripping-kremser` | deep + slides | `_old/deep/cs14-absorpsi-vs-stripping-kremser.json` + `_sources/specs/2026-10-21-carousel-1.json` |
| `flixborough-sketsa-kapur-manajemen-perubahan` | deep + slides | `_old/deep/flixborough-sketsa-kapur-manajemen-perubahan.json` + `_sources/specs/2026-10-17-carousel-2.json` |
| `ipal-tujuh-tahap-air-limbah` | deep + slides | `_old/deep/ipal-tujuh-tahap-air-limbah.json` + `_sources/specs/2026-10-12-carousel-2.json` |
| `level-apd-kelas-cedera` | deep + slides | `_old/deep/level-apd-kelas-cedera.json` + `_sources/specs/2026-10-11-carousel-2.json` |
| `near-miss-hampir-celaka-wajib-lapor` | deep + slides | `_old/deep/near-miss-hampir-celaka-wajib-lapor.json` + `_sources/specs/2026-10-10-carousel-2.json` |
| `satuan-tekanan-torricelli-titik-nol` | deep + slides | `_old/deep/satuan-tekanan-torricelli-titik-nol.json` + `_sources/specs/2026-10-15-carousel-2.json` |
| `seligman-1923-plate-heat-exchanger` | deep + slides | `_old/deep/seligman-1923-plate-heat-exchanger.json` + `_sources/specs/2026-10-18-carousel-2.json` |
| `texas-city-2005-informasi-yang-hilang` | deep + slides | `_old/deep/texas-city-2005-informasi-yang-hilang.json` + `_sources/specs/2026-10-13-carousel-2.json` |
| `toolbox-meeting-lima-menit-menyelamatkan-nyawa` | deep + slides | `_old/deep/toolbox-meeting-lima-menit-menyelamatkan-nyawa.json` + `_sources/specs/2026-10-20-carousel-2.json` |
| `warna-pipa-bahasa-peringatan` | deep + slides | `_old/deep/warna-pipa-bahasa-peringatan.json` + `_sources/specs/2026-10-14-carousel-2.json` |
| `desuperheater-uap-disemprot-air` | deep + slides | `_old/deep/desuperheater-uap-disemprot-air.json` + `_sources/specs/2026-10-24-carousel-1.json` |
| `flame-arrestor-lampu-davy-1815` | deep + slides | `_old/deep/flame-arrestor-lampu-davy-1815.json` + `_sources/specs/2026-10-23-carousel-2.json` |
| `kavitasi-pompa-gelembung-mengeruk-baja` | deep + spec pilot hilang | `_old/deep/kavitasi-pompa-gelembung-mengeruk-baja.json` + **Spec tidak ditemukan:** `real-photo-pilot/spec-pilot-001-kavitasi.json`; atribut tampilan dari `_old/artikel/kavitasi-pompa-gelembung-mengeruk-baja/index.html` |
| `molecular-sieve-mengeringkan-gas` | deep + slides | `_old/deep/molecular-sieve-mengeringkan-gas.json` + `_sources/specs/2026-10-22-carousel-2.json` |
| `pigging-membersihkan-pipa-dari-dalam` | deep + slides | `_old/deep/pigging-membersihkan-pipa-dari-dalam.json` + `_sources/specs/2026-10-23-carousel-1.json` |
| `thermocouple-seebeck-1821` | deep + slides | `_old/deep/thermocouple-seebeck-1821.json` + `_sources/specs/2026-10-24-carousel-2.json` |
| `water-hammer-palu-air-pipa` | deep + spec pilot hilang | `_old/deep/water-hammer-palu-air-pipa.json` + **Spec tidak ditemukan:** `real-photo-pilot/spec-pilot-002-waterhammer.json`; atribut tampilan dari `_old/artikel/water-hammer-palu-air-pipa/index.html` |

## Peta 33 halaman video

| Slug | Tipe rendering | Sumber data |
| --- | --- | --- |
| `/video/` (indeks) | indeks video | `_old/tools/build.py`: `VIDEOS`, loop indeks video; metadata/copy `_old/video/index.html` |
| `sampling-rutin-lab` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[sampling-rutin-lab]` + `VIDEO_ARTICLES[sampling-rutin-lab]` |
| `shift-handover-logbook` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[shift-handover-logbook]` + `VIDEO_ARTICLES[shift-handover-logbook]` |
| `hilirisasi-nikel-baterai-ev` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[hilirisasi-nikel-baterai-ev]` + `VIDEO_ARTICLES[hilirisasi-nikel-baterai-ev]` |
| `pasir-jadi-chip-ai` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[pasir-jadi-chip-ai]` + `VIDEO_ARTICLES[pasir-jadi-chip-ai]` |
| `distilasi-minyak-mentah` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[distilasi-minyak-mentah]` + `VIDEO_ARTICLES[distilasi-minyak-mentah]` |
| `process-safety-bukan-apd` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[process-safety-bukan-apd]` + `VIDEO_ARTICLES[process-safety-bukan-apd]` |
| `heat-exchanger-penghenti-pabrik` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[heat-exchanger-penghenti-pabrik]` + `VIDEO_ARTICLES[heat-exchanger-penghenti-pabrik]` |
| `haber-bosch-udara-jadi-pupuk` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[haber-bosch-udara-jadi-pupuk]` + `VIDEO_ARTICLES[haber-bosch-udara-jadi-pupuk]` |
| `netralisasi-asam-basa` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[netralisasi-asam-basa]` + `VIDEO_ARTICLES[netralisasi-asam-basa]` |
| `water-gas-shift-co-jadi-h2` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[water-gas-shift-co-jadi-h2]` + `VIDEO_ARTICLES[water-gas-shift-co-jadi-h2]` |
| `b40-transesterifikasi-motion` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[b40-transesterifikasi-motion]` + `VIDEO_ARTICLES[b40-transesterifikasi-motion]` |
| `confined-space-masuk-tangki` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[confined-space-masuk-tangki]` + `VIDEO_ARTICLES[confined-space-masuk-tangki]` |
| `dead-leg-pipa-buntu-berbahaya` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[dead-leg-pipa-buntu-berbahaya]` + `VIDEO_ARTICLES[dead-leg-pipa-buntu-berbahaya]` |
| `flare-stack-api-kilang-menyala` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[flare-stack-api-kilang-menyala]` + `VIDEO_ARTICLES[flare-stack-api-kilang-menyala]` |
| `gudang-bahan-kimia-segregasi-bunding` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[gudang-bahan-kimia-segregasi-bunding]` + `VIDEO_ARTICLES[gudang-bahan-kimia-segregasi-bunding]` |
| `hybrid-pompa-sentrifugal` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[hybrid-pompa-sentrifugal]` + `VIDEO_ARTICLES[hybrid-pompa-sentrifugal]` |
| `hybrid-shell-and-tube-heat-exchanger` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[hybrid-shell-and-tube-heat-exchanger]` + `VIDEO_ARTICLES[hybrid-shell-and-tube-heat-exchanger]` |
| `loto-gembok-pribadi-motion` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[loto-gembok-pribadi-motion]` + `VIDEO_ARTICLES[loto-gembok-pribadi-motion]` |
| `pks-tbs-menjadi-cpo-motion` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[pks-tbs-menjadi-cpo-motion]` + `VIDEO_ARTICLES[pks-tbs-menjadi-cpo-motion]` |
| `refinery-sawit-olein-stearin-motion` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[refinery-sawit-olein-stearin-motion]` + `VIDEO_ARTICLES[refinery-sawit-olein-stearin-motion]` |
| `satu-barel-minyak-motion` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[satu-barel-minyak-motion]` + `VIDEO_ARTICLES[satu-barel-minyak-motion]` |
| `sistem-kerja-tiga-shift` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[sistem-kerja-tiga-shift]` + `VIDEO_ARTICLES[sistem-kerja-tiga-shift]` |
| `tangki-putih-floating-roof` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[tangki-putih-floating-roof]` + `VIDEO_ARTICLES[tangki-putih-floating-roof]` |
| `turnaround-pabrik-berhenti-total` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[turnaround-pabrik-berhenti-total]` + `VIDEO_ARTICLES[turnaround-pabrik-berhenti-total]` |
| `buildup-boiler-pltu-dari-ceret` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[buildup-boiler-pltu-dari-ceret]` + `VIDEO_ARTICLES[buildup-boiler-pltu-dari-ceret]` |
| `buildup-kolom-distilasi-alembik` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[buildup-kolom-distilasi-alembik]` + `VIDEO_ARTICLES[buildup-kolom-distilasi-alembik]` |
| `buildup-kolom-distilasi-remake` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[buildup-kolom-distilasi-remake]` + `VIDEO_ARTICLES[buildup-kolom-distilasi-remake]` |
| `buildup-reaktor-dari-panci-presto` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[buildup-reaktor-dari-panci-presto]` + `VIDEO_ARTICLES[buildup-reaktor-dari-panci-presto]` |
| `ko-drum-penjaga-kompresor` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[ko-drum-penjaga-kompresor]` + `VIDEO_ARTICLES[ko-drum-penjaga-kompresor]` |
| `lpg-cairan-dalam-tabung` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[lpg-cairan-dalam-tabung]` + `VIDEO_ARTICLES[lpg-cairan-dalam-tabung]` |
| `ntu-efektivitas-penukar-panas` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[ntu-efektivitas-penukar-panas]` + `VIDEO_ARTICLES[ntu-efektivitas-penukar-panas]` |
| `steam-trap-katup-kondensat` | video + `render_video_article` + player/kuis | `_old/tools/build.py`: `VIDEOS[steam-trap-katup-kondensat]` + `VIDEO_ARTICLES[steam-trap-katup-kondensat]` |

## Hasil dan cakupan

Sesi 3 selesai mengikuti **SESSION-3.md**, yaitu 61 halaman artikel, 32 halaman detail video, dan satu indeks video. Ringkasan peta sesi pada BRIEF.md menyebut kamus/halaman statis, tetapi cakupan khusus sesi ini secara eksplisit melarang pekerjaan tersebut. Tidak ada slug dalam cakupan yang tertinggal.

Route baru:

- `src/app/artikel/[slug]/page.js`: `generateStaticParams()` menghasilkan 61 slug, `dynamicParams = false`, dan `dynamic = "force-static"`.
- `src/app/video/[slug]/page.js`: konfigurasi yang sama untuk 32 slug video.
- `src/app/video/page.js`: indeks statis berisi seluruh 32 kartu dalam urutan lama.

Kedua route detail menunggu `params` sesuai pola App Router yang digunakan proyek. Slug yang tidak dikenal ditangani `notFound()` pada fungsi halaman dan metadata. Setiap halaman menyediakan `<main>` sendiri. Artikel menggunakan `.post`, video `.post.video-post`, dan indeks memiliki `.post.wide` diikuti `.grid.video-grid`, tanpa wrapper tambahan.

Beranda, Header, Footer, ChatWidget, layout, CSS, konfigurasi, dependensi, lockfile, dan `public/` tidak diubah. Tidak membuat kamus, halaman statis lain, API, sitemap, atau robots. Tidak menyalin/menghasilkan biner. Tidak ada bug sesi 1–2 yang perlu diperbaiki untuk menyelesaikan cakupan ini.

## Skema data dan asalnya

- `src/data/articles/specs/`: **57 spec** yang digunakan daftar `ARTICLES`, disalin byte demi byte dari `_sources/specs/`. Varian revisi yang dipilih persis mengikuti daftar tersebut; spec lain yang tidak dirujuk tidak ikut disalin.
- `src/data/articles/drafts/`: **dua draft**, `spec-real.json` dan `2026-10-03-cooling-tower-buku.json`, disalin byte demi byte dari akar `_sources/`. Direktori asal generator (`draft/` dan `drafts/`) dipetakan eksplisit ke lokasi yang diberikan di workspace ini.
- `src/data/articles/deep/`: **61 deep JSON**, disalin byte demi byte dari `_old/deep/`. Mempertahankan `lead`, `sections` (`h`, `paras`), `facts`, `refs`, `closing`, dan field sumber lainnya.
- `src/data/articles/sources.js`: indeks impor JSON untuk server, dipetakan menurut slug menjadi `{ spec, deep }`. Dua spec yang hilang bernilai `null`; tidak dibuatkan spec pengganti.
- `src/data/articles/manifest.json`: satu record per artikel berisi `slug`, `title`, `date`, `ig`, `status` dari `ARTICLES`, lokasi sumber/copy, dan daftar URL gambar yang benar-benar tercatat pada HTML lama. Dua record pilot menambahkan `legacyFallback` berisi asal HTML, `series`, dan daftar referensi final dari HTML tersebut. Keduanya tidak mempunyai figur pada HTML lama. Isi badan tetap dibaca dari deep JSON, bukan disimpan sebagai potongan HTML.
- `src/data/videos.json`: keseluruhan nilai literal **32 record `VIDEOS`**, diekstrak lewat AST Python tanpa menjalankan generator. Memuat metadata, hook, intro, tension, takeaway, facts, quiz, scenes, serta path sumber media asli.
- `src/data/video-articles.json`: keseluruhan nilai literal **32 entri `VIDEO_ARTICLES`**, termasuk lead, bagian bertanda waktu, paragraf, dan referensi. Serialisasi berubah dari literal Python menjadi JSON, tetapi nilai dan teks tidak diedit.
- `src/data/video-assets.json`: hasil resolver yang teramati dari HTML lama untuk setiap slug (`video_url`, `poster_url`), beserta `sectionStarts` untuk ejaan atribut waktu, termasuk `0.0`, `56.0`, dan nilai lain yang akan kehilangan akhiran `.0` jika langsung diubah dari angka JavaScript menjadi string.
- `src/data/page-metadata.json`: **94 record** hasil pembacaan head tiap HTML lama: title, description, canonical, seluruh OG yang ada (type/title/description/url/image). `src/lib/pageMetadata.js` menghasilkan judul absolut dan OG lengkap per halaman sehingga metadata beranda tidak bocor ke detail.

Tidak ada pembacaan `_old/` atau `_sources/` pada runtime aplikasi. Semua data yang diperlukan renderer sudah berada di `src/data/`.

## Renderer dan transformasi

`src/lib/content.js` memport `clean_text`, `paras_of`, `seg_text`, `tgl_indo`, `fmt_time`, pengubahan label seri dengan semantik `str.title`, kunci deduplikasi referensi, `merge_refs`, pemilihan figur slide, serta `article_figures`.

- `clean_text`: mengganti em dash dan dua tanda hubung dengan koma/spasi, melipat whitespace Python, lalu memangkas tepinya. Daftar dan objek mempertahankan representasi teks Python ketika digunakan sebagai nilai teks. Ini diperlukan oleh beberapa field persamaan berbentuk daftar pada spec; isinya sengaja tidak disunting menjadi formula baru.
- Paragraf caption: split per baris, bersihkan, singkirkan baris kosong, hashtag, dan awalan `follow @ilmutekkim`. Cabang non-deep mempertahankan subtitle dan maksimum dua paragraf intro seperti generator.
- `merge_refs`: bersihkan daftar deep terlebih dahulu; tambahkan referensi spec yang belum ada berdasarkan 40 karakter alfanumerik Unicode pertama dari teks lowercase. Urutan, referensi deep yang berulang, dan bentuk teks yang ditambahkan mengikuti sumber.
- Tanggal memakai nama bulan Indonesia yang sama. Format waktu server mempertahankan pembulatan Python dengan ties to even, termasuk `6.5 → 0:06`, `17.5 → 0:18`, dan carry ke menit berikutnya. Jam progres ketika video dimainkan tetap memakai pemotongan integer seperti script browser lama.
- Urutan artikel/video memakai sort tanggal menurun yang stabil, sehingga navigasi sebelumnya/berikutnya pada tanggal yang sama tetap mengikuti urutan deklarasi generator.
- Resolusi aset mengikuti hasil yang tercatat pada HTML lama. Gambar dipilih dengan urutan `photo` lalu `diagram`, memakai nama `/assets/img/<slug>/foto-<n>.jpg`, `diagram-<n>.jpg`, dan `cover.jpg` yang sama. Operasi kompresi/salin gambar, ffmpeg, dan pengambilan poster tidak dijalankan: aset biner tetap dipasang operator. Ketersediaan file mentah pada mesin sesi ini tidak dijadikan alasan untuk menghilangkan gambar yang ada di HTML lama.

`ArticleBody.jsx` menyediakan `Rows`, `SlideSection`, `BeforeAfterSections`, dan `DeepBody`. Cabang slide mempertahankan quote, conclusion, body/gambar, fill_rows, fill_cards, fill_grid, formula/equation, bullets, serta callout. Before/after mempertahankan simbol, hasil string/list, penjelasan, segmen teks, dan kesimpulan. Semua **61 halaman aktual** memakai override deep: paragraf deep ditampilkan dengan teks asli, figur disisipkan sesudah section secara berurutan, sisa figur diletakkan setelah section terakhir, lalu fakta dan closing. Tidak menambahkan kembali slide atau caption yang sudah ditimpa oleh deep.

`ArticleParts.jsx` menyediakan figur/kredit, referensi, dan navigasi bersama. `ArticlePost.jsx` mempertahankan urutan header, label arsip, tautan carousel, cover/kredit, lead, body, referensi, navigasi, dan CTA. Ada **58 cover dan 127 figur badan** pada hasil artikel; semua URL dan kredit cocok dengan HTML sumber.

`VideoPost.jsx` menyediakan pemutar, artikel pendamping bertanda waktu, fakta, kesimpulan, referensi bernomor, kuis, CTA, dan navigasi. `scenes` tetap disimpan dalam data, tetapi tidak dirender menjadi transkrip/segmen produksi baru: generator aktual hanya menampilkan artikel `VIDEO_ARTICLES`. Copy indeks yang menyebut **“Sepuluh video”** tetap dipertahankan walaupun hitungan aktualnya 32, karena larangan perubahan copy.

`VideoInteractions.jsx` adalah satu-satunya komponen klien baru dan mengembalikan `null`. Efek memasang seek/play, progres, penyorotan heading terakhir dengan waktu mulai ≤ posisi putar, dan kuis sesuai script inline lama. Heading tanpa waktu tidak menjadi kandidat aktif. Klik opsi menandai hanya opsi yang dipilih sebagai `right`/`wrong` dan menampilkan penjelasan. Listener serta perubahan DOM dibersihkan saat efek dilepas; dependensi slug menangani perpindahan antarhalaman. Tidak memuat ulang `main.js` atau handler tema.

Dua video memiliki `video_url` dan `poster_url` kosong pada HTML lama: `distilasi-minyak-mentah` dan `water-gas-shift-co-jadi-h2`. Keduanya tetap memakai `<source src="" type="video/mp4">` dan placeholder kartu. Untuk dua source tersebut saja, isi `<video>` menggunakan string HTML konstan agar React tidak menghapus atribut `src=""`. Tidak ada input pengguna pada string tersebut. Sisa markup memakai JSX server biasa.

## Verifikasi

Memakai dependensi yang sudah tersedia, Babel bawaan Next memeriksa JSX/impor, lalu `react-dom/server` merender setiap route ke berkas sementara. Ini **bukan build Next** dan tidak memakai hasil `.next` yang sudah ada.

| Kelompok | Hasil | Contoh yang tercakup |
| --- | --- | --- |
| Artikel deep | **61/61 DOM `<main>` cocok** | distilasi bertingkat, reflux optimum, cooling tower wet bulb, desuperheater, thermocouple |
| Spec before/after yang ditimpa deep | **2/2**, termasuk dalam 61 | distilasi bertingkat, baca P&ID |
| Artikel arsip | **2/2**, termasuk dalam 61 | pirolisis plastik, polimerisasi Carothers |
| Deep dengan spec pilot hilang | **2/2**, termasuk dalam 61 | kavitasi pompa, water hammer |
| Detail video | **32/32 DOM `<main>` cocok** | sampling lab, shift handover, NTU, pompa hybrid, empat video buildup, dua source kosong |
| Indeks video | **1/1 DOM `<main>` cocok** | seluruh 32 kartu, urutan, placeholder, tanggal, durasi, href |
| Metadata | **94/94 cocok persis** | title absolut, description, OG, canonical, dan gambar OG bila ada |

Perbandingan memakai parser HTML `lxml`, memeriksa hierarki, urutan, elemen, atribut, kelas, href, path aset, serta teks. Whitespace pemformatan, urutan atribut, dan serialisasi atribut boolean dinormalisasi. Teks gabungan pada elemen inline juga dibandingkan agar spasi di sekitar tautan/tombol tidak hilang. Karena parser lxml berbasis HTML4, tag void HTML5 `<source>` dinormalisasi menjadi bentuk self-closing sebelum parsing kedua sisi. Script inline video dikeluarkan dari perbandingan struktur dan diperiksa terpisah melalui harness perilaku.

Pemeriksaan tambahan:

- `generateStaticParams` tepat **61 dan 32 slug unik**, cocok dengan semua direktori HTML sumber; kedua flag route diperiksa. Slug tak dikenal diuji menghasilkan 404 pada halaman dan metadata.
- **448 perbandingan DOM renderer spec lulus**: seluruh 441 slide dari 59 spec/draft, kedua before/after asli, dan lima kasus tambahan untuk cabang quote/conclusion/rows/cards/grid/simbol/hasil string-list. Pembandingnya fungsi Python asli yang dimuat terbatas lewat AST, tanpa mengimpor atau menjalankan `main()` generator.
- **466 perbandingan transformasi Python/JavaScript lulus**, mencakup caption, label seri, segmen, referensi, pemilihan figur, whitespace Unicode, karakter khusus, dan batas pembulatan waktu.
- **2.768 perbandingan keadaan perilaku video lulus** terhadap script inline asli pada seluruh 32 video: waktu sebelum/tepat/sesudah heading, heading dengan waktu sama, heading tanpa waktu, durasi belum tersedia/nol/normal, seek/play, progres, pergantian jawaban kuis, serta pemasangan ulang dan pembersihan listener. DOM dan media disimulasikan; ini bukan pemutaran video/browser nyata.
- **120/120 copy JSON identik byte demi byte**: 59 spec/draft + 61 deep. Nilai hasil ekstraksi `VIDEOS` dan `VIDEO_ARTICLES` cocok seluruhnya dengan AST sumber.
- SHA-256 seluruh **296 berkas `_old/` tidak berubah**. Total **311 berkas lama** dalam snapshot (`_old`, `src`, `public`, package/lockfile/config yang diperiksa) tetap identik. Semua perubahan aplikasi adalah berkas baru dalam cakupan Sesi 3.
- Harness dan hasil sementara berada di `/tmp/ilmutekkim-session-3-*`, tanpa dependensi atau berkas pengujian baru di proyek.
- **Tidak menjalankan `npm install`, `npm run build`, generator lama, atau perintah instalasi/build pengganti.** `node_modules`, lockfile, dan `.next` sudah tersedia sebelum sesi ini.

## Risiko dan serah terima

1. Operator masih perlu menjalankan build Next untuk membuktikan SSG final, lalu memeriksa hidrasi dan tampilan browser desktop/mobile. Pemeriksaan JSX/SSR/parser serta simulasi interaksi tidak menggantikan build, screenshot, atau pemutaran media nyata.
2. Seluruh aset biner tetap menjadi tanggung jawab operator di `public/assets/`. Dua video dengan source kosong merupakan keadaan sumber yang sengaja dipertahankan; tidak ditambahkan file atau URL berdasarkan dugaan. Ketersediaan video tersebut memerlukan keputusan terpisah jika kelak hendak diubah.
3. Spec pilot kavitasi dan water hammer belum ditemukan. Kedua halaman sudah lengkap dan setara HTML lama dari deep + fallback tampilan yang terdokumentasi, tetapi regenerasi dari spec asli tetap memerlukan kedua file tersebut jika dibutuhkan kelak.
4. Kamus, indeks pencarian chat, halaman statis/riset/jalur/kalkulator/referensi, `/api/ask`, sitemap, dan robots tetap menunggu sesi yang dialokasikan. Tautan ke sana dipertahankan persis. Dengan penyelesaian Sesi 3 ini, seluruh tujuan kartu artikel/video beranda sudah mempunyai route.
5. Canonical tetap memakai domain dan slash dari HTML lama; konfigurasi proyek tetap `trailingSlash: false`. Perilaku redirect slash dan integrasi metadata final perlu diperiksa operator dalam runtime Next.

Tidak ada halaman dalam cakupan Sesi 3 yang belum selesai dan tidak ada pertanyaan yang menghalangi serah terima.
