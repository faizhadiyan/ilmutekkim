#!/usr/bin/env python3
"""
ILM-R69: seluruh teks tampil wajib diksi akademis profesional (lihat GUIDELINES.md).Generate website ilmutekkim dari spec carousel IG @ilmutekkim.

Sumber kebenaran: ~/workspace/ig-ilmutekkim/specs/*.json (+ draft reflux & buku CT).
Output: situs statis di root repo ini (siap Vercel tanpa build step).
"""
import html
import json
import os
import re
import shutil

SRC = os.path.expanduser("~/workspace/ig-ilmutekkim")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ilmutekkim.vercel.app"

# slug, spec relatif, judul artikel, tanggal, url IG (terverifikasi) / None, status
ARTICLES = [
    ("distilasi-bertingkat-minyak-mentah", "specs/2026-09-30-carousel-1.json",
     "Distilasi Bertingkat: Mengapa Minyak Mentah Tidak Cukup Dipanaskan Satu Kali",
     "2026-09-30", "https://www.instagram.com/p/Dd8JoC6FLhe/", "tayang"),
    ("reflux-optimum-kolom-distilasi", "draft/spec-real.json",
     "Semakin Besar Reflux, Semakin Murni? Bedah Reflux Optimum Kolom Distilasi",
     "2026-09-30", "https://www.instagram.com/p/Dd8LkbglNQY/", "tayang"),
    ("pabrik-kelapa-sawit-tandan-ke-cpo", "specs/2026-09-30-carousel-2-rev4.json",
     "Dari Tandan Berduri Menjadi Minyak Sawit: Alur Lengkap Pabrik Kelapa Sawit",
     "2026-09-30", "https://www.instagram.com/p/Dd7_i9uFIZn/", "tayang"),
    ("baca-pid-lima-simbol-pabrik", "specs/2026-09-30-carousel-3.json",
     "Baca P&ID dalam 5 Menit: Lima Simbol yang Muncul di Hampir Semua Pabrik",
     "2026-09-30", "https://www.instagram.com/p/Dd8J_SPlMUm/", "tayang"),
    ("refinery-sawit-cpo-ke-minyak-goreng", "specs/2026-10-01-carousel-1.json",
     "Dari CPO Menjadi Minyak Goreng: Empat Tahap Refinery Sawit (Olein vs Stearin)",
     "2026-10-01", "https://www.instagram.com/p/Dd8B6u6E6PN/", "tayang"),
    ("heat-exchanger-bikin-shutdown", "specs/2026-10-01-carousel-2.json",
     "Heat Exchanger: Alat Paling Sederhana yang Paling Sering Menyebabkan Pabrik Shutdown",
     "2026-10-01", "https://www.instagram.com/p/Dd8NemJD3vA/", "tayang"),
    ("b40-biodiesel-sawit-transesterifikasi", "specs/2026-10-01-carousel-3-rev2.json",
     "B40: Bagaimana Sawit Menjadi Biodiesel Melalui Transesterifikasi",
     "2026-10-02", "https://www.instagram.com/p/Dd_bheiDuVX/", "tayang"),
    ("bbm-dari-sampah-plastik-pirolisis", "specs/2026-10-01-bbm-plastik.json",
     "Dari Sampah Plastik Menjadi BBM: Bedah Proses Pirolisis",
     "2026-10-01", "https://www.instagram.com/p/Dd7kKigk5SA/", "arsip"),
    ("tekanan-relief-valve-rupture-disk", "specs/2026-10-02-carousel-1.json",
     "Tekanan Itu Nyawa di Pabrik Kimia: Cara Kerja Relief Valve dan Rupture Disk",
     "2026-10-02", "https://www.instagram.com/p/Dd-dqjwD4Bi/", "tayang"),
    ("satu-barel-minyak-jadi-apa", "specs/2026-10-02-carousel-2-rev.json",
     "Satu Barel Minyak Menjadi Apa Saja? Bedah Produk Kilang Cilacap dan Balikpapan",
     "2026-10-02", "https://www.instagram.com/p/Dd_RdyFDNf7/", "tayang"),
    ("pompa-vs-kompresor", "specs/2026-10-02-carousel-3.json",
     "Pompa vs Kompresor: Salah Pilih Alat, Boros Listrik Bertahun-tahun",
     "2026-10-02", "https://www.instagram.com/p/Dd_Nvp1jL2U/", "tayang"),
    ("naphtha-ke-plastik-petrokimia", "specs/2026-10-03-carousel-1.json",
     "Dari Naphtha Menjadi Plastik: Alur Petrokimia Steam Cracker sampai Polimer",
     "2026-10-03", "https://www.instagram.com/p/DeBMfgKDsT_/", "tayang"),
    ("cooling-tower-cara-kerja", "specs/2026-10-03-carousel-2.json",
     "Cooling Tower: Cara Kerja AC Raksasa Pabrik yang Sering Disangka Cerobong Asap",
     "2026-10-03", "https://www.instagram.com/p/DeB5ccrD6Tv/", "tayang"),
    ("cooling-tower-wet-bulb-range-approach", "drafts/2026-10-03-cooling-tower-buku.json",
     "Menilai Cooling Tower dengan Benar: Wet Bulb, Range, Approach, dan Neraca Air",
     "2026-10-03", "https://www.instagram.com/p/DeCB7AzFDA4/", "tayang"),
    ("gas-alam-ke-urea-haber-bosch", "specs/2026-10-03-carousel-3.json",
     "Gas Alam dan Udara Menjadi Pupuk Urea: Proses Haber-Bosch di Pupuk Kaltim",
     "2026-10-03", "https://www.instagram.com/p/DeDSOk2mW6F/", "tayang"),
    ("polimerisasi-konversi-carothers", "specs/2026-10-03-advanced-polimerisasi.json",
     "Konversi 99 Persen Masih Kurang: Polimerisasi Step-Growth dan Persamaan Carothers",
     "2026-10-03", "https://www.instagram.com/p/DeBQiZJDpMO/", "arsip"),
    ("neraca-massa-data-pabrik-bocor", "specs/2026-10-04-carousel-1.json",
     "Data Pabrik Selalu Bocor Angka? Periksa Dulu Neraca Massanya",
     "2026-10-04", "https://www.instagram.com/p/DeDqycEjlro/", "tayang"),
    ("oleokimia-sawit-sabun-deterjen", "specs/2026-10-04-carousel-2.json",
     "Sabun di Rumah Berasal dari Sawit: Alur Kimia Oleokimia",
     "2026-10-04", "https://www.instagram.com/p/DeEk3baD0Mv/", "tayang"),
    ("batch-vs-continuous-pabrik", "specs/2026-10-04-carousel-3.json",
     "Batch vs Continuous: Mengapa Pabrik Makanan dan Petrokimia Berbeda Jauh Cara Kerjanya",
     "2026-10-04", "https://www.instagram.com/p/DeE3CFYj2i1/", "tayang"),
    ("tebu-ke-gula-pabrik-gula", "specs/2026-10-05-carousel-1.json",
     "Tebu Tidak Hanya Diperas: Alur Lengkap Pabrik Gula dari Ladang ke Kristal",
     "2026-10-05", "https://www.instagram.com/p/DeGWfGXjwR9/", "tayang"),
    ("utilitas-pabrik-steam-air-nitrogen", "specs/2026-10-05-carousel-2.json",
     "Utilitas Pabrik: Pabrik di Dalam Pabrik yang Tidak Terlihat (Steam, Air, Nitrogen)",
     "2026-10-05", "https://www.instagram.com/p/DeG-z3Hj3Ul/", "tayang"),
    ("batu-kapur-ke-semen-kiln", "specs/2026-10-05-carousel-3.json",
     "Batu Kapur Menjadi Semen Melalui Api 1450 Derajat: Proses Kiln dari Tambang ke Kantong",
     "2026-10-05", "https://www.instagram.com/p/DeHbo8HjxkY/", "tayang"),
    ("safety-instrumented-system-lapisan-pengaman", "specs/2026-10-06-carousel-1.json",
     "Pabrik Aman Bukan Karena Operator Sigap: Cara Kerja Safety Instrumented System",
     "2026-10-06", "https://www.instagram.com/p/DeI-sCKk7S0/", "tayang"),
    ("pulp-kertas-proses-kraft", "specs/2026-10-06-carousel-2-rev.json",
     "Kayu Keras Menjadi Kertas Lembut: Proses Kraft di Pabrik Pulp Riau",
     "2026-10-06", "https://www.instagram.com/p/DeJjGqwj0Hb/", "tayang"),
    ("permit-to-work-kerja-panas", "specs/2026-10-06-carousel-3.json",
     "Las Lima Menit Tetap Butuh Izin: Cara Kerja Permit to Work di Pabrik Kimia",
     "2026-10-06", "https://www.instagram.com/p/DeJ_8QCjtmQ/", "tayang"),
    ("roadmap-enam-mata-kuliah-pabrik", "specs/2026-10-07-roadmap-1.json",
     "Enam Mata Kuliah yang Sesungguhnya Menjalankan Pabrik: Peta Roadmap Teknik Kimia",
     "2026-10-07", "https://www.instagram.com/p/DeMyNxZjIl2/", "tayang"),
    ("cs01-step-growth-carothers-dp-runtuh", "specs/2026-10-08-carousel-1.json",
     "CS-01 Cheat Sheet: DP Polimer Runtuh Apabila Stoikiometri Menyimpang 1 Persen",
     "2026-10-08", "https://www.instagram.com/p/DeOBXd7jy3k/", "tayang"),
    ("control-room-dcs-loop-kontrol", "specs/2026-10-08-carousel-2.json",
     "Satu Layar Berisi Satu Pabrik: Bedah Control Room dan Loop Kontrol DCS",
     "2026-10-08", "https://www.instagram.com/p/DeOqlk7E_vp/", "tayang"),
    ("cs02-mccabe-thiele-garis-operasi", "specs/2026-10-09-carousel-1.json",
     "CS-02 Cheat Sheet: Dua Garis Operasi McCabe-Thiele dan Tangga Tahapnya",
     "2026-10-09", "https://www.instagram.com/p/DeQmX_cCV9e/", "tayang"),
    ("preventive-maintenance-bongkar-terjadwal", "specs/2026-10-09-carousel-2.json",
     "Preventive Maintenance: Mengapa Mesin yang Sehat Tetap Dibongkar Secara Terjadwal",
     "2026-10-09", "https://www.instagram.com/p/DeRSyKSD7Eq/", "tayang"),
    ('bhopal-1984-lapisan-pengaman-yang-mati', 'specs/2026-10-21-carousel-2.json',
     'Bhopal 1984: Satu Tangki, Satu Kota, dan Lapisan Pengaman yang Mati Satu per Satu',
     '2026-10-21', 'https://www.instagram.com/p/DewFgFFj5Ys/', 'tayang'),
    ('boiler-meledak-lahirnya-katup-pengaman', 'specs/2026-10-19-carousel-2.json',
     'Boiler yang Meledak dan Lahirnya Katup Pengaman',
     '2026-10-19', 'https://www.instagram.com/p/DerXVnXCbDY/', 'tayang'),
    ('coffey-still-1830-distilasi-kontinu', 'specs/2026-10-16-carousel-2.json',
     'Coffey Still 1830: Ketika Distilasi Berhenti Menjadi Kerja Batch',
     '2026-10-16', 'https://www.instagram.com/p/DejQ5PVj8EL/', 'tayang'),
    ('cs03-reflux-minimum-jebakan-mahal', 'specs/2026-10-10-carousel-1.json',
     'CS-03 Cheat Sheet: Reflux Minimum, Reflux Total, dan Reflux Operasi',
     '2026-10-10', 'https://www.instagram.com/p/DeTLDZZDtpu/', 'tayang'),
    ('cs04-fouling-lmtd-meleset', 'specs/2026-10-11-carousel-1.json',
     'CS-04 Cheat Sheet: Fouling Membuat Hitungan LMTD Meleset',
     '2026-10-11', 'https://www.instagram.com/p/DeVvxH8E5tw/', 'tayang'),
    ('cs05-azeotrop-etanol-956', 'specs/2026-10-12-carousel-1.json',
     'CS-05 Cheat Sheet: Azeotrop, Alasan Etanol Berhenti di 95,6 Persen',
     '2026-10-12', 'https://www.instagram.com/p/DeYUg5Zjyrm/', 'tayang'),
    ('cs06-purge-recycle-gas-inert', 'specs/2026-10-13-carousel-1.json',
     'CS-06 Cheat Sheet: Neraca Massa Recycle dan Fungsi Purge',
     '2026-10-13', 'https://www.instagram.com/p/Dea5a_sDsas/', 'tayang'),
    ('cs07-pompa-kompresor-versi-ujian', 'specs/2026-10-14-carousel-1.json',
     'CS-07 Cheat Sheet: Pompa atau Kompresor, Head atau Pressure Ratio',
     '2026-10-14', 'https://www.instagram.com/p/Dedf1zYDyml/', 'tayang'),
    ('cs08-cooling-tower-wet-bulb-ujian', 'specs/2026-10-15-carousel-1-rev2.json',
     'CS-08 Cheat Sheet: Wet Bulb, Penentu Suhu Air Dingin Cooling Tower',
     '2026-10-15', 'https://www.instagram.com/p/DegNBPdiRRj/', 'tayang'),
    ('cs09-batch-vs-cstr-volume', 'specs/2026-10-16-carousel-1-repost-tex2.json',
     'CS-09 Cheat Sheet: Batch vs CSTR, Mengapa Volumenya Berbeda Empat Kali',
     '2026-10-16', 'https://www.instagram.com/p/DejIhisD-jp/', 'tayang'),
    ('cs10-pid-sepuluh-simbol-ujian', 'specs/2026-10-17-carousel-1.json',
     'CS-10 Cheat Sheet: Sepuluh Simbol P&ID yang Paling Sering Keluar di Ujian',
     '2026-10-17', 'https://www.instagram.com/p/DelMlXojlSC/', 'tayang'),
    ('cs11-relief-set-pressure-mawp', 'specs/2026-10-18-carousel-1.json',
     'CS-11 Cheat Sheet: Set Pressure Bukan Tekanan Maksimum Bejana',
     '2026-10-18', 'https://www.instagram.com/p/Dent7ONj--g/', 'tayang'),
    ('cs12-gliserol-satu-ton-cpo', 'specs/2026-10-19-carousel-1.json',
     'CS-12 Cheat Sheet: Satu Ton CPO dan 104 Kilogram Gliserol',
     '2026-10-19', 'https://www.instagram.com/p/DeqW_c9j8zr/', 'tayang'),
    ('cs13-raoult-kesetimbangan-uap-cair', 'specs/2026-10-20-carousel-1.json',
     'CS-13 Cheat Sheet: Hukum Raoult, dari x1 = 0,4 Menjadi y1 = 0,63',
     '2026-10-20', 'https://www.instagram.com/p/Des_SHfj08w/', 'tayang'),
    ('cs14-absorpsi-vs-stripping-kremser', 'specs/2026-10-21-carousel-1.json',
     'CS-14 Cheat Sheet: Absorpsi vs Stripping, Satu Kolom Dua Arah',
     '2026-10-21', 'https://www.instagram.com/p/DevjMbqCY0t/', 'tayang'),
    ('flixborough-sketsa-kapur-manajemen-perubahan', 'specs/2026-10-17-carousel-2.json',
     'Flixborough: Sketsa Kapur, Pipa Darurat, dan Lahirnya Manajemen Perubahan',
     '2026-10-17', 'https://www.instagram.com/p/Del5OIBD_08/', 'tayang'),
    ('ipal-tujuh-tahap-air-limbah', 'specs/2026-10-12-carousel-2.json',
     'IPAL Pabrik: Tujuh Tahap Air Limbah Sebelum Kembali Bersih',
     '2026-10-12', 'https://www.instagram.com/p/DeZktCXDObg/', 'tayang'),
    ('level-apd-kelas-cedera', 'specs/2026-10-11-carousel-2.json',
     'Level APD: Salah Memilih Level, Kelas Cederanya Berbeda',
     '2026-10-11', 'https://www.instagram.com/p/DeWVbpZD9In/', 'tayang'),
    ('near-miss-hampir-celaka-wajib-lapor', 'specs/2026-10-10-carousel-2.json',
     'Near Miss: Mengapa Hampir Celaka Wajib Dilaporkan Sebelum Memakan Korban',
     '2026-10-10', 'https://www.instagram.com/p/DeT0Mbej3G3/', 'tayang'),
    ('satuan-tekanan-torricelli-titik-nol', 'specs/2026-10-15-carousel-2.json',
     'Satuan Tekanan: Torricelli, Gauge, Absolut, dan Titik Nol yang Menentukan',
     '2026-10-15', 'https://www.instagram.com/p/Degvwd3E-Wq/', 'tayang'),
    ('seligman-1923-plate-heat-exchanger', 'specs/2026-10-18-carousel-2.json',
     'Seligman 1923: Ahli Aluminium yang Mengubah Cara Susu Dipanaskan',
     '2026-10-18', 'https://www.instagram.com/p/DeoTqAqE5Mp/', 'tayang'),
    ('texas-city-2005-informasi-yang-hilang', 'specs/2026-10-13-carousel-2.json',
     'Texas City 2005: Ledakan Kilang yang Berawal dari Informasi yang Tidak Sampai',
     '2026-10-13', 'https://www.instagram.com/p/Debl-N_ji2C/', 'tayang'),
    ('toolbox-meeting-lima-menit-menyelamatkan-nyawa', 'specs/2026-10-20-carousel-2.json',
     'Toolbox Meeting: Lima Menit yang Menyelamatkan Nyawa',
     '2026-10-20', 'https://www.instagram.com/p/DetgslYjz8s/', 'tayang'),
    ('warna-pipa-bahasa-peringatan', 'specs/2026-10-14-carousel-2.json',
     'Warna Pipa di Pabrik: Bahasa Peringatan yang Lahir dari Kecelakaan',
     '2026-10-14', 'https://www.instagram.com/p/DeeMQh1D8CO/', 'tayang'),
    ('desuperheater-uap-disemprot-air', 'specs/2026-10-24-carousel-1.json',
     'Desuperheater: Mengapa Uap 450 Derajat Disemprot Air Sebelum Masuk Turbin',
     '2026-10-24', 'https://www.instagram.com/p/De3RiKpD-e5/', 'tayang'),
    ('flame-arrestor-lampu-davy-1815', 'specs/2026-10-23-carousel-2.json',
     'Flame Arrestor: Prinsip Lampu Davy 1815 yang Menjaga Vent Tangki',
     '2026-10-23', 'https://www.instagram.com/p/De1PsRYDi2k/', 'tayang'),
    ('kavitasi-pompa-gelembung-mengeruk-baja', 'real-photo-pilot/spec-pilot-001-kavitasi.json',
     'Kavitasi Pompa: Gelembung Kecil yang Mengeruk Baja dari Dalam',
     '2026-10-20', 'https://www.instagram.com/p/DevwUEFD2CT/', 'tayang'),
    ('molecular-sieve-mengeringkan-gas', 'specs/2026-10-22-carousel-2.json',
     'Molecular Sieve: Saringan yang Mengeringkan Gas dan Membersihkan Dirinya Sendiri',
     '2026-10-22', 'https://www.instagram.com/p/DeyqTBGD3KW/', 'tayang'),
    ('pigging-membersihkan-pipa-dari-dalam', 'specs/2026-10-23-carousel-1.json',
     'Pigging: Membersihkan Pipa Minyak dari Dalam Tanpa Membongkar',
     '2026-10-23', 'https://www.instagram.com/p/De0wJwmjlWI/', 'tayang'),
    ('thermocouple-seebeck-1821', 'specs/2026-10-24-carousel-2.json',
     'Thermocouple: Dua Kawat Logam yang Membaca Suhu Tanpa Baterai Sejak 1821',
     '2026-10-24', 'https://www.instagram.com/p/De3zvL7DMSA/', 'tayang'),
    ('water-hammer-palu-air-pipa', 'real-photo-pilot/spec-pilot-002-waterhammer.json',
     'Water Hammer: Palu Air, Lonjakan Tekanan yang Memecahkan Pipa',
     '2026-10-21', 'https://www.instagram.com/p/DewF1g2D3Zk/', 'tayang')
]

BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def tgl_indo(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {BULAN[int(m)]} {y}"


def clean_text(s):
    s = str(s or "")
    s = s.replace("—", ", ").replace("--", ", ")
    return re.sub(r"\s+", " ", s).strip()


# --- Video motion graphics (sumber: brief kitab suci + video-briefs JSON + IG live) ---
# slug, judul, tanggal IG, url IG, file sumber MP4, file poster sumber (boleh None -> ambil frame), durasi dtk
VIDEOS = [
    {
        "slug": "sampling-rutin-lab",
        "title": "Sampling Rutin: Mengapa Sampel Manual Tetap Diambil Setiap Jam",
        "hook": "Sensor online menyala terus-menerus, tetapi sampel manual tetap diambil setiap jam.",
        "date": "2026-10-08",
        "ig": "https://www.instagram.com/reel/DePJYIWDhaM/",
        "src": "~/workspace/ig-ilmutekkim/media/2026-10-08/motion-1/motion.mp4",
        "poster_src": "~/workspace/ig-ilmutekkim/media/2026-10-08/motion-1/cover.jpg",
        "duration": 40.9,
        "tag": "Kendali Mutu Pabrik",
        "intro": "Sensor online membaca terus menerus, tapi pabrik tetap mengambil sampel manual tiap jam untuk diuji di lab. Video ini membedah kenapa cara manual belum ditinggalkan.",
        "tension": "Sensor cuma membaca titik yang ia sentuh dan bacaannya bisa bergeser diam-diam tanpa terasa.",
        "takeaway": "Sensor menjaga detik, laboratorium menjaga kebenaran. Hasil laboratorium adalah pembanding independen yang menunjukkan sensor masih akurat.",
        "facts": [
            "Sensor online hanya mengukur di ujung probe, tidak mewakili seluruh aliran di pipa besar.",
            "Sampel diambil di titik sampel (sampling point), ditutup rapat, diberi label waktu, lalu diserahkan ke analis lab.",
            "Selisih hasil lab vs bacaan sensor ditindaklanjuti dengan cek proses, bukan dibiarkan.",
        ],
        "quiz": {
            "q": "Mengapa sampel laboratorium tetap dibutuhkan padahal sensor online sudah menyala?",
            "options": ["Karena laboratorium lebih cepat daripada sensor", "Karena sensor dapat bergeser dan hanya membaca satu titik", "Karena operator membutuhkan pekerjaan tambahan"],
            "answer": 1,
            "explain": "Sensor membaca satu titik dan dapat mengalami drift. Laboratorium memberikan nilai independen dari sampel fisik yang sama, sehingga pergeseran terdeteksi sebelum produk ikut bergeser.",
        },
        "scenes": [
            {"start": 0, "end": 6, "role": "HOOK", "title": "Sensor menyala, sampel tetap diambil", "on_screen": "Sensor online menyala terus. Sampel manual tetap diambil tiap jam", "visual": "Panel sensor hijau menyala, tangan operator membuka keran titik sampel di pipa.", "purpose": "Membuka pertanyaan kenapa cara manual belum ditinggalkan pabrik modern.", "watch": "Perhatikan dua kartu berdampingan: panel sensor vs keran titik sampel. Kontras inilah tension video ini."},
            {"start": 6, "end": 13, "role": "TENSION", "title": "Sensor cuma baca satu titik", "on_screen": "Sensor cuma membaca titik yang ia sentuh", "visual": "Probe tercelup di satu titik pipa besar, sebagian aliran lewat jauh dari ujung sensor.", "purpose": "Menunjukkan batas fisik sensor titik tunggal.", "watch": "Panah aliran yang lewat jauh dari probe adalah visual kuncinya: yang tidak tersentuh tidak terukur."},
            {"start": 13, "end": 20, "role": "TENSION", "title": "Bacaan bisa bergeser diam-diam", "on_screen": "Bacaannya bisa bergeser diam-diam. Produk ikut bergeser", "visual": "Garis bacaan merah perlahan menjauh dari garis target hijau, botol sampel terisi.", "purpose": "Menahan jawaban dengan risiko drift tanpa pembanding.", "watch": "Grafiknya kualitatif tanpa angka karangan. Yang bergeser adalah garisnya, bukan nilai yang dihafal."},
            {"start": 20, "end": 27, "role": "PAYOFF", "title": "Urutan sampling yang benar", "on_screen": "Ambil di titik sampel, tutup rapat, label waktu, kirim ke lab", "visual": "Empat langkah bernomor: buka keran, tutup botol, tulis label waktu, serahkan ke analis.", "purpose": "Memberi urutan kerja dari titik sampel sampai lab.", "watch": "Nomor 1 sampai 4 di sini urutan langkah, bukan angka proses. Label waktu adalah elemen baru scene ini."},
            {"start": 27, "end": 34, "role": "PAYOFF", "title": "Lab membuktikan sensor jujur atau bohong", "on_screen": "Hasil lab membuktikan sensor jujur atau mulai bohong", "visual": "Dua kartu: hasil lab vs bacaan sensor, badge COCOK hijau dan SELISIH dengan instruksi cek proses.", "purpose": "Menegaskan fungsi lab sebagai pembanding independen.", "watch": "Badge COCOK dan SELISIH tampil berdampingan. Tidak ada angka hasil uji karangan, hanya label kualitatif."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Sensor jaga detik, lab jaga kebenaran", "on_screen": "Sensor menjaga detik, lab menjaga kebenaran. Simpan video ini", "visual": "Botol berlabel rapi di rak lab, watermark @ilmutekkim, progress bar selesai.", "purpose": "Menutup dengan satu kalimat kesimpulan dan alasan simpan.", "watch": "Rak lab di akhir adalah bukti mutu fisiknya. Simpan video ini buat bekal masuk pabrik."},
        ],
    },
    {
        "slug": "shift-handover-logbook",
        "title": "Shift Handover: Mengapa Logbook Tulisan Tangan Belum Tergantikan",
        "hook": "Komputer mencatat angka. Logbook mencatat riwayat peralatannya.",
        "date": "2026-10-07",
        "ig": "https://www.instagram.com/reel/DeMk3GmicdD/",
        "src": "~/workspace/ig-ilmutekkim/media/2026-10-07/motion-1/motion.mp4",
        "poster_src": "~/workspace/ig-ilmutekkim/media/2026-10-07/motion-1/cover.jpg",
        "duration": 40.9,
        "tag": "Operasi Pabrik",
        "intro": "Pabrik jalan 24 jam, operator berganti tiap shift. Video ini membedah kenapa serah terima tidak cukup mengandalkan layar, dan kenapa logbook tulisan tangan masih jadi ingatan pabrik antar shift.",
        "tension": "Layar menampilkan angka proses, tapi detail kecil seperti katup rembes hanya hidup di catatan logbook.",
        "takeaway": "Logbook adalah ingatan pabrik antarshift. Tahapannya: menulis keadaan alat, membaca bersama, berkeliling memeriksa lapangan, dan menandatangani serah terima.",
        "facts": [
            "Contoh nyata di video: katup V-204 rembes, pantau tiap jam, jangan ditinggal. Detail kualitatif seperti ini tidak muncul di angka DCS.",
            "Handover yang benar ditutup tanda tangan dua operator dan stempel waktu, tanggung jawab berpindah jelas dan bisa ditelusur.",
        ],
        "quiz": {
            "q": "Apa yang dicatat logbook tetapi tidak dicatat layar DCS?",
            "options": ["Angka suhu dan tekanan", "Riwayat alat, misalnya katup mana yang rembes dan perlu dipantau", "Jadwal libur operator"],
            "answer": 1,
            "explain": "DCS mencatat angka. Logbook mencatat konteks kualitatif peralatan, gangguan kecil, dan hal yang harus diwaspadai shift berikutnya.",
        },
        "scenes": [
            {"start": 0, "end": 6, "role": "HOOK", "title": "Logbook tulisan tangan belum tergantikan layar", "on_screen": "Logbook tulisan tangan belum tergantikan layar", "visual": "Logbook terbuka membesar di layar cerah, pena menulis baris terakhir shift.", "purpose": "Membuka celah kenapa tulisan tangan masih dipakai di pabrik modern.", "watch": "Pena yang masih menulis di frame pertama adalah hook visualnya, bukan sekadar teks."},
            {"start": 6, "end": 13, "role": "TENSION", "title": "Layar angka vs logbook cerita", "on_screen": "Layar menampilkan angka. Logbook menyimpan cerita alat", "visual": "Dua panel: layar angka polos dan logbook berisi catatan katup bocor kecil.", "purpose": "Menunjukkan risiko kalau serah terima hanya mengandalkan layar.", "watch": "Kartu kanan menyebut katup spesifik. Itulah beda angka dan cerita."},
            {"start": 13, "end": 20, "role": "TENSION", "title": "Shift berganti, cerita tidak boleh berganti", "on_screen": "Shift berganti. Keadaan alat tidak boleh ikut berganti cerita", "visual": "Jam shift berputar, operator pulang keluar dan operator datang masuk dari sisi berlawanan.", "purpose": "Menahan jawaban dengan momen ganti shift yang rawan salah paham.", "watch": "Ikon PULANG dan DATANG tampil bersamaan. Momen inilah yang paling rawan miskomunikasi."},
            {"start": 20, "end": 27, "role": "PAYOFF", "title": "Tiga langkah handover yang benar", "on_screen": "Tulis keadaan alat, baca bersama, keliling cek lapangan", "visual": "Tiga langkah berurutan: menulis logbook, membaca bersama, berjalan cek katup di lapangan.", "purpose": "Memberi urutan handover langkah demi langkah.", "watch": "Langkah ketiga membawa operator keluar dari control room. Handover tidak selesai di meja."},
            {"start": 27, "end": 34, "role": "PAYOFF", "title": "Tanda tangan menutup serah terima", "on_screen": "Tanda tangan menutup serah terima. Tanggung jawab berpindah jelas", "visual": "Logbook ditandatangani dua operator, stempel waktu shift di pojok halaman.", "purpose": "Menegaskan bukti serah terima yang bisa ditelusur.", "watch": "Stempel waktu adalah elemen barunya. Tanpa itu, catatan sulit ditelusur ke shift mana."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Logbook adalah ingatan pabrik", "on_screen": "Logbook adalah ingatan pabrik antar shift. Simpan video ini", "visual": "Logbook tertutup rapi di meja control room, watermark @ilmutekkim.", "purpose": "Menutup dengan kesimpulan dan aksi simpan.", "watch": "Simpan video ini buat bekal masuk pabrik, urutan handover di tengah adalah kuncinya."},
        ],
    },
    {
        "slug": "hilirisasi-nikel-baterai-ev",
        "title": "Hilirisasi Nikel: Jalur Pengolahan Bijih Menjadi Baterai EV",
        "hook": "Bijih nikel kotor diolah menjadi baterai EV.",
        "date": "2026-10-06",
        "ig": "https://www.instagram.com/reel/DeLHZmOE0Dw/",
        "src": "~/workspace/coded-motion-graphics/videos/hilirisasi-nikel/renders/hilirisasi-nikel_v2_2026-10-07_07-38.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Hilirisasi & Proses",
        "intro": "Kadar nikel di bijih laterit cuma sekitar 1 sampai 2 persen. Video ini membedah kenapa bijihnya harus dipilah dulu, dan kenapa ada dua jalur pabrik yang sangat berbeda untuk stainless steel dan baterai EV.",
        "tension": "Kalau kadarnya cuma 1 sampai 2 persen, kenapa tidak langsung dibuat baterai?",
        "takeaway": "Nilai hilirisasi terletak pada kemampuan memilah, melebur, melarutkan, dan memurnikan di pabrik. Saprolit dan limonit tidak diperlakukan sama.",
        "facts": [
            "Saprolit (kadar lebih tinggi) masuk jalur panas RKEF: rotary kiln lalu electric furnace menjadi nickel pig iron (NPI) untuk stainless steel. NPI bukan bahan baterai langsung.",
            "Limonit (kadar lebih rendah) masuk jalur basah HPAL: asam sulfat di autoclave sekitar 250°C tekanan tinggi, lalu diendapkan jadi MHP dan dimurnikan ke nikel sulfat untuk prekursor katoda.",
            "Tantangan prosesnya wajib diingat: energi besar, konsumsi asam, dan tailing atau residu yang harus dikelola.",
        ],
        "quiz": {
            "q": "Jalur mana yang menghasilkan bahan baku untuk baterai EV?",
            "options": ["RKEF menghasilkan NPI", "HPAL menghasilkan MHP kemudian nikel sulfat", "Keduanya langsung menjadi baterai"],
            "answer": 1,
            "explain": "RKEF menghasilkan NPI untuk stainless steel. Baterai melalui HPAL: limonit dilarutkan, diendapkan menjadi MHP, kemudian menjadi nikel sulfat dan prekursor katoda.",
        },
        "scenes": [
            {"start": 0, "end": 6.8, "role": "HOOK", "title": "Biji kotor jadi baterai EV", "on_screen": "BIJI NIKEL KOTOR JADI BATERAI EV", "visual": "Rantai bijih laterit menjadi produk antara lalu sel baterai EV.", "purpose": "Mengklaim transformasi ekstrem sambil memperlihatkan rantai nilainya.", "watch": "Tiga tahap di hook ini akan dipecah satu per satu di scene berikutnya."},
            {"start": 6.8, "end": 13.6, "role": "TENSION", "title": "Kadar cuma 1 sampai 2 persen, harus dipilah", "on_screen": "Kadar Ni cuma sekitar 1 sampai 2 persen", "visual": "Bijih laterit dipilah menjadi tumpukan saprolit dan limonit.", "purpose": "Menunjukkan bijih bukan satu jenis seragam.", "watch": "Pemilahan saprolit vs limonit adalah keputusan proses pertama dan paling menentukan."},
            {"start": 13.6, "end": 20.4, "role": "PROSES", "title": "Saprolit lewat jalur panas RKEF", "on_screen": "RKEF: rotary kiln dan electric furnace", "visual": "Saprolit masuk rotary kiln lalu electric furnace, keluar nickel pig iron.", "purpose": "Menjelaskan jalur pirometalurgi untuk stainless steel.", "watch": "NPI di akhir scene ini untuk stainless, jangan tertukar dengan bahan baterai."},
            {"start": 20.4, "end": 27.2, "role": "PAYOFF", "title": "Limonit lewat jalur basah HPAL", "on_screen": "HPAL: asam sulfat sekitar 250°C di autoclave", "visual": "Limonit dilarutkan asam sulfat di autoclave suhu dan tekanan tinggi.", "purpose": "Menjelaskan jalur hidrometalurgi untuk baterai.", "watch": "Angka 250°C di sini kondisi autoclave, bukan suhu lebur. Asamnya yang melarutkan nikel."},
            {"start": 27.2, "end": 34, "role": "PAYOFF", "title": "Dari larutan jadi MHP dan nikel sulfat", "on_screen": "MHP lalu nikel sulfat untuk prekursor katoda", "visual": "Larutan nikel diendapkan jadi MHP, dimurnikan jadi nikel sulfat dan prekursor.", "purpose": "Menunjukkan larutan tidak langsung jadi baterai.", "watch": "MHP adalah produk antara (mixed hydroxide precipitate), masih perlu dimurnikan lagi."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Nilai ada di pabriknya", "on_screen": "Nilai hilirisasi ada pada memilah, melebur, melarutkan, memurnikan", "visual": "Pabrik berjalan penuh, catatan tantangan energi, asam, tailing.", "purpose": "Menutup dengan kesimpulan dan tantangan yang jujur.", "watch": "Follow untuk lanjutan seri hilirisasi: HPAL, RKEF, dan pengelolaan tailing satu per satu."},
        ],
    },
    {
        "slug": "pasir-jadi-chip-ai",
        "title": "Pasir Menjadi Chip AI: Reaksi, Distilasi, dan Kristal di Baliknya",
        "hook": "Chip AI berasal dari pasir.",
        "date": "2026-10-05",
        "ig": "https://www.instagram.com/reel/DeJFBULEyhF/",
        "src": "~/workspace/coded-motion-graphics/videos/pasir-chip-ai/renders/pasir-chip-ai_v1_2026-10-06_12-20.mp4",
        "poster_src": "~/workspace/coded-motion-graphics/videos/pasir-chip-ai/cover.jpg",
        "duration": 40.9,
        "tag": "Semikonduktor",
        "intro": "Chip AI berawal dari pasir kuarsa. Video ini membedah kenapa pasir sembarangan tidak bisa langsung jadi chip, dan kenapa kemurnian ekstrem adalah inti teknik kimianya.",
        "tension": "Kalau bahannya cuma pasir, kenapa chip tidak bisa dibuat dari pasir sembarangan?",
        "takeaway": "Chip AI lahir dari reaksi, distilasi, dan kristal yang dikendalikan insinyur proses. Semua itu adalah teknik kimia, bukan sulap.",
        "facts": [
            "Reduksi disederhanakan: SiO2 + 2C menjadi Si + 2CO di furnace listrik. Silikon metalurgi baru sekitar 98% murni, masih terlalu kotor untuk transistor nanometer.",
            "Silikon diubah jadi triklorosilan yang mudah menguap, sehingga pengotor bisa dipisahkan lewat distilasi. Proses Siemens lalu menumbuhkan polysilicon sekitar 99,9999999% (9N).",
            "Polysilicon dilelehkan pada 1.414°C dan ditarik jadi kristal tunggal (Czochralski), dipotong jadi wafer 300 mm, baru difabrikasi jadi chip.",
        ],
        "quiz": {
            "q": "Mengapa silikon harus diubah menjadi triklorosilan terlebih dahulu?",
            "options": ["Agar warnanya berubah", "Agar mudah menguap dan pengotornya dapat dipisahkan melalui distilasi", "Agar lebih murah daripada pasir"],
            "answer": 1,
            "explain": "Triklorosilan mudah menguap, sehingga distilasi dapat memisahkannya dari pengotor. Dari tahap itu proses Siemens menghasilkan polysilicon ultra murni.",
        },
        "scenes": [
            {"start": 0, "end": 6.8, "role": "HOOK", "title": "Chip AI asalnya dari pasir", "on_screen": "CHIP AI ASALNYA DARI PASIR", "visual": "Pasir berubah menjadi wafer silikon lalu chip AI.", "purpose": "Mengklaim transformasi ekstrem pasir menjadi chip.", "watch": "Transformasi di hook ini sengaja dibuat terlihat mudah. Scene berikutnya membongkar kenapa tidak semudah itu."},
            {"start": 6.8, "end": 13.6, "role": "TENSION", "title": "Baru 98% murni, masih terlalu kotor", "on_screen": "Silikon metalurgi baru sekitar 98% murni", "visual": "Pasir kuarsa direduksi dengan karbon menjadi silikon metalurgi plus label pengotor.", "purpose": "Menunjukkan hasil pertama masih jauh dari cukup.", "watch": "Angka 98% di sini contoh konservatif silikon metalurgi (rentang umum 98 sampai 99%)."},
            {"start": 13.6, "end": 20.4, "role": "TENSION", "title": "Harus jadi triklorosilan agar bisa dimurnikan", "on_screen": "Diubah jadi triklorosilan yang dapat dimurnikan", "visual": "Silikon menjadi triklorosilan, ikon transistor nanometer yang tidak toleran pengotor.", "purpose": "Menjelaskan kenapa perlu zat antara yang mudah menguap.", "watch": "Kata kuncinya mudah menguap. Sifat itulah yang membuat distilasi masuk akal."},
            {"start": 20.4, "end": 27.2, "role": "PAYOFF", "title": "Distilasi dan proses Siemens", "on_screen": "Polysilicon ultra murni sekitar 99,9999999%", "visual": "Kolom distilasi memisahkan pengotor, batang silikon panas menumbuhkan polysilicon.", "purpose": "Memberi angka kemurnian konkretnya.", "watch": "99,9999999% mewakili 9N. Chip modern umumnya di rentang 9N sampai 11N, bukan satu angka mutlak."},
            {"start": 27.2, "end": 34, "role": "PAYOFF", "title": "Leleh 1.414°C, tarik kristal, potong wafer", "on_screen": "Dilelehkan pada 1.414°C, ditarik jadi kristal tunggal, wafer 300 mm", "visual": "Lelehan ditarik jadi kristal tunggal, dipotong jadi wafer, wafer jadi chip.", "purpose": "Menunjukkan tahap kristal dan wafer.", "watch": "1.414°C adalah titik leleh silikon. Wafer 300 mm adalah ukuran umum modern."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Lahir dari reaksi, distilasi, kristal", "on_screen": "Chip lahir dari reaksi, distilasi, dan kristal yang dikendalikan", "visual": "Chip AI final dengan ajakan follow seri semikonduktor.", "purpose": "Menutup dengan kerangka teknik kimia di balik AI.", "watch": "Follow untuk lanjutan: air ultrapure, cleanroom, dan plasma etching."},
        ],
    },
    {
        "slug": "distilasi-minyak-mentah",
        "title": "Distilasi Minyak Mentah: Satu Kolom, Banyak Produk Keluar",
        "hook": "Minyak mentah masuk, banyak produk keluar. Kuncinya adalah perbedaan titik didih.",
        "date": "2026-10-05",
        "ig": "https://www.instagram.com/reel/DeG_5tXPCyo/",
        "src": "~/workspace/coded-motion-graphics/videos/minyak-mentah/renders/minyak-mentah_v2_2026-10-02.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Kilang & Distilasi",
        "intro": "Minyak mentah tidak dipisah pakai saringan, tapi pakai titik didih di satu kolom tinggi. Video ini membedah alur dari fired heater sampai produk keluar sesuai titik didihnya.",
        "tension": "Satu minyak mentah bisa jadi gas sampai residu. Apa yang memisahkannya di dalam kolom?",
        "takeaway": "Distilasi adalah pemisahan fisik, bukan reaksi kimia. Yang dipisahkan adalah titik didihnya, bukan diubah menjadi zat baru.",
        "facts": [
            "Umpan dipanaskan di fired heater sampai sekitar 350°C, masuk zona flash di bawah kolom. Di atas sekitar 120°C, di bawah sekitar 350°C.",
            "Overhead paling ringan didinginkan di kondenser ke drum reflux, sebagian balik sebagai reflux agar pisahnya tajam. Dasar dididihkan lagi di reboiler, steam membantu stripping, residu keluar setelah reboiler.",
            "Urutan produk ringan ke berat: gas di bawah 40°C, bensin 40 sampai 180°C, kerosin 180 sampai 240°C, solar 240 sampai 340°C, residu di atas 340°C.",
        ],
        "quiz": {
            "q": "Pada dasarnya, distilasi minyak mentah merupakan proses apa?",
            "options": ["Reaksi kimia yang mengubah minyak menjadi bensin", "Pemisahan fisik berdasarkan perbedaan titik didih", "Penyaringan menggunakan saringan halus"],
            "answer": 1,
            "explain": "Tidak ada zat baru yang terbentuk. Campuran dipisahkan karena komponennya menguap dan mengembun pada suhu yang berbeda di tray kolom.",
        },
        "scenes": [
            {"start": 0, "end": 6.5, "role": "HOOK", "title": "Minyak masuk, banyak produk keluar", "on_screen": "KILANG MINYAK. MINYAK MENTAH MASUK. BANYAK PRODUK KELUAR", "visual": "Kolom kilang dengan maskot tetes minyak, produk keluar bertingkat.", "purpose": "Membuka bahwa satu umpan bisa dipecah jadi banyak produk karena beda titik didih.", "watch": "Perhatikan kolomnya sejak detik pertama terbangun. Semua scene berikutnya mengisi kolom yang sama."},
            {"start": 6.5, "end": 13, "role": "KONTEKS", "title": "Bukan zat tunggal, campuran hidrokarbon", "on_screen": "BUKAN ZAT TUNGGAL. CAMPURAN HIDROKARBON. Dipanaskan sekitar 350°C", "visual": "Fired heater, tag 350°C, zona flash, tiga kartu Ringan Sedang Berat.", "purpose": "Menjelaskan umpan harus dididihkan dulu agar bisa dipisah.", "watch": "Zona flash adalah titik awal uap dan cairan berpisah di dalam kolom."},
            {"start": 13, "end": 19.5, "role": "MEKANISME", "title": "Uap naik, cairan turun di tray", "on_screen": "UAP NAIK. CAIRAN TURUN", "visual": "8 tray horizontal, partikel biru muda naik sebagai uap, biru tua turun sebagai cairan.", "purpose": "Menunjukkan kontak uap dan cairan di tiap tray.", "watch": "Yang ringan lanjut menguap, yang berat mengembun dan turun. Itulah mesin pemisahnya."},
            {"start": 19.5, "end": 26.5, "role": "PAYOFF", "title": "Paling ringan didinginkan di puncak", "on_screen": "YANG PALING RINGAN DIDINGINKAN DI PUNCAK. Sebagian kembali sebagai reflux", "visual": "Pipa overhead ke kondenser, drum reflux, pipa reflux balik dan pipa produk atas.", "purpose": "Menjelaskan overhead, kondenser, dan fungsi reflux.", "watch": "Reflux yang balik membuat pisahnya tajam, bukan sekadar membuang produk atas."},
            {"start": 26.5, "end": 33.5, "role": "PAYOFF", "title": "Atas dingin, bawah panas", "on_screen": "ATAS DINGIN BAWAH PANAS. Sekitar 120°C di atas, 350°C di bawah", "visual": "Gradien suhu di kolom, reboiler di dasar, steam masuk, residu keluar setelah reboiler.", "purpose": "Memberi angka suhu konkret dan peran reboiler plus steam stripping.", "watch": "Residu keluar setelah reboiler, bukan langsung dari dasar kolom. Detail ini yang dijaga kebenaran teknisnya."},
            {"start": 33.5, "end": 40.9, "role": "TAKEAWAY", "title": "Keluar sesuai titik didih", "on_screen": "KELUAR SESUAI TITIK DIDIH. DISTILASI ITU PISAH FISIK, BUKAN REAKSI KIMIA", "visual": "Lima kartu produk berurutan dan pipa side draw kerosin solar.", "purpose": "Mengurutkan produk ringan ke berat dan menutup dengan definisi.", "watch": "Urutkan dari bawah: residu paling berat di atas 340°C, gas paling ringan di bawah 40°C."},
        ],
    },
    {
        "slug": "process-safety-bukan-apd",
        "title": "Process Safety Bukan tentang APD: Hazard, Risk, dan Barrier Berlapis",
        "hook": "Process safety bukan tentang APD.",
        "date": "2026-10-04",
        "ig": "https://www.instagram.com/reel/DeGB-GQj-j8/",
        "src": "~/workspace/coded-motion-graphics/videos/process-safety/renders/process-safety_v3_2026-10-05_08-14.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Process Safety",
        "intro": "APD melindungi orang setelah bahaya terlepas. Process safety mencegah pelepasannya sejak awal. Video ini membedah tiga kata kuncinya dan kenapa lapisannya harus independen.",
        "tension": "Kalau APD, alarm, dan operator sudah ada, kenapa kecelakaan proses besar masih bisa terjadi?",
        "takeaway": "Process safety menjaga bahan dan energi berbahaya tetap terkendali melalui lapisan yang tidak saling bergantung.",
        "facts": [
            "Risk dibaca dari kombinasi konsekuensi dan kemungkinan, bukan bahaya saja. APD tetap berguna, tapi bukan penghalang utama pelepasan besar.",
            "Contoh hitungan ilustratif: kejadian awal 1 kali per 10 tahun, tiga lapisan independen masing-masing gagal 1 dari 10 saat dibutuhkan, hasilnya 0,0001 per tahun atau 1 per 10.000 tahun. Syaratnya: lapisan benar-benar independen.",
            "Relief digambarkan menuju sistem tertutup atau flare, bukan membuang bebas ke udara.",
        ],
        "quiz": {
            "q": "Mengapa tiga lapisan dapat menurunkan frekuensi dari 1 per 10 tahun menjadi 1 per 10.000 tahun?",
            "options": ["Karena setiap lapisan pasti berhasil", "Karena peluang gagalnya dikalikan, dengan syarat lapisannya independen", "Karena APD ditambah tiga lapis"],
            "answer": 1,
            "explain": "0,1 x 0,1 x 0,1 x 0,1 = 0,0001 per tahun. Perkalian itu hanya berlaku apabila lapisannya tidak berbagi penyebab kegagalan yang sama.",
        },
        "scenes": [
            {"start": 0, "end": 6.8, "role": "HOOK", "title": "Process safety bukan soal APD", "on_screen": "PROCESS SAFETY BUKAN SOAL APD", "visual": "Vessel bertekanan dengan lapisan pengaman di sekelilingnya.", "purpose": "Mengklaim koreksi miskonsepsi paling umum soal process safety.", "watch": "Vessel bertekanan di hook ini adalah sumber bahaya besarnya, bukan pekerja tanpa helm."},
            {"start": 6.8, "end": 13.6, "role": "TENSION", "title": "Kecelakaan personal vs kecelakaan proses", "on_screen": "Sasaran process safety adalah pelepasan bahan atau energi berskala besar", "visual": "Perbandingan kecelakaan personal dan kecelakaan proses berskala besar.", "purpose": "Membedakan dua jenis kecelakaan agar sasarannya jelas.", "watch": "APD kuat di kiri (personal), lemah di kanan (proses). Di situlah celahnya."},
            {"start": 13.6, "end": 20.4, "role": "TENSION", "title": "Hazard dan risk", "on_screen": "Hazard, risk, konsekuensi, kemungkinan", "visual": "Kartu hazard dan risk, risk sebagai gabungan konsekuensi dan kemungkinan.", "purpose": "Memperkenalkan dua kata kunci sebelum cara mengendalikannya.", "watch": "Jangan menyederhanakan risk menjadi bahaya saja. Dua komponennya tampil terpisah."},
            {"start": 20.4, "end": 27.2, "role": "PAYOFF", "title": "Barrier berlapis pada tekanan naik", "on_screen": "Kontrol proses, trip otomatis, relief valve, tanggap darurat", "visual": "Skenario tekanan naik ditahan berurutan oleh empat lapisan.", "purpose": "Menunjukkan cara kerja barrier pada satu skenario nyata.", "watch": "Urutannya penting: kontrol dulu, trip, relief, baru tanggap darurat di luar."},
            {"start": 27.2, "end": 34, "role": "PAYOFF", "title": "Hitungan lapisan independen", "on_screen": "Dari 1 per 10 tahun menjadi 1 per 10.000 tahun", "visual": "Hitungan peluang gagal 1 dari 10 dikalikan antar lapisan.", "purpose": "Membuktikan fungsi independensi lewat angka.", "watch": "Syarat independen wajib tampil. Tanpa itu, perkalian peluangnya tidak sah."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Menjaga bahaya tetap terkendali", "on_screen": "Process safety menjaga bahan dan energi berbahaya tetap terkendali", "visual": "Vessel terkendali dengan ajakan follow seri HAZOP dan relief system.", "purpose": "Menutup dengan definisi satu kalimat.", "watch": "Follow untuk membedah HAZOP, relief system, dan manajemen perubahan satu per satu."},
        ],
    },
    {
        "slug": "heat-exchanger-penghenti-pabrik",
        "title": "Heat Exchanger: Alat Paling Sederhana yang Dapat Menghentikan Pabrik",
        "hook": "Alat paling sederhana, namun dapat menghentikan pabrik.",
        "date": "2026-10-03",
        "ig": "https://www.instagram.com/reel/DeDrJkVP2Jr/",
        "src": "~/workspace/coded-motion-graphics/videos/heat-exchanger/renders/heat-exchanger_v2_2026-10-03_21-50.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Unit Operasi",
        "intro": "Heat exchanger kelihatan cuma pipa dalam tabung. Video ini membedah kenapa arah aliran dan kerak 1 milimeter bisa menentukan hemat borosnya pabrik, sampai memaksa unit berhenti.",
        "tension": "Kalau alat ini cuma pipa dalam tabung, kenapa kerak tipis bisa memaksa satu unit berhenti total?",
        "takeaway": "Arah aliran menentukan efisiensi; kerak (fouling) menentukan kapan pabrik harus berhenti untuk dibersihkan.",
        "facts": [
            "Contoh terverifikasi: panas 150 ke 90°C, dingin 30 ke 80°C. Lawan arah beda suhu penggerak rata-rata (LMTD) sekitar 65°C, searah sekitar 44°C. Rasio 65 per 44 sekitar 1,48 atau panas yang dipindah bisa sekitar 48% lebih besar pada suhu ujung yang sama.",
            "Kerak 1 mm memangkas fluks panas sekitar 10%. Literatur fouling menyebut biaya sekitar 0,25% PDB negara industri dan sekitar 186 juta barel minyak per tahun dipakai kilang dunia menambal rugi fouling (estimasi Müller-Steinhagen).",
        ],
        "quiz": {
            "q": "Pada suhu ujung yang sama, mengapa lawan arah lebih efisien daripada searah?",
            "options": ["Karena pipanya lebih panjang", "Karena perbedaan suhu penggerak rata-ratanya lebih besar (65 vs 44°C)", "Karena keraknya lebih tipis"],
            "answer": 1,
            "explain": "LMTD lawan arah 65°C berbanding searah 44°C. Perbedaan suhu yang lebih besar mendorong lebih banyak panas menyeberangi dinding yang sama.",
        },
        "scenes": [
            {"start": 0, "end": 6.8, "role": "HOOK", "title": "Alat tersepele penghenti pabrik", "on_screen": "ALAT PALING SEPELE PENGHENTI PABRIK", "visual": "Skema heat exchanger terbangun dari detik pertama, sub penukar panas.", "purpose": "Mengklaim heat exchanger adalah alat tersepele yang paling sering menghentikan pabrik.", "watch": "Alatnya diperkenalkan secara visual sejak hook, bukan hanya disebut."},
            {"start": 6.8, "end": 13.6, "role": "TENSION", "title": "Dua aliran dipisah dinding logam", "on_screen": "Dua aliran dipisah dinding, panas menyeberang, cairan tidak bertemu", "visual": "Fluida panas 150 ke 90°C dan fluida dingin 30 ke 80°C dipisah dinding logam.", "purpose": "Menjelaskan cara kerja dasar tanpa cairan bertemu.", "watch": "Contoh suhu di scene ini yang dipakai lagi untuk hitungan LMTD di payoff."},
            {"start": 13.6, "end": 20.4, "role": "TENSION", "title": "Searah atau lawan arah, beda total", "on_screen": "Arah aliran bisa searah atau lawan arah, beda suhunya berubah total", "visual": "Perbandingan beda suhu ujung 120 ke 10°C (searah) vs 70 ke 60°C (lawan arah).", "purpose": "Menahan jawaban dengan menunjukkan beda suhu sebagai tenaga pendorong.", "watch": "Dua pasang angka ujung ini jangan tertukar. Payoff menghitung rata-ratanya."},
            {"start": 20.4, "end": 27.2, "role": "PAYOFF", "title": "Angka konkretnya: 65 vs 44°C", "on_screen": "Lawan arah 65°C vs searah 44°C, panas bisa sekitar 48% lebih besar", "visual": "Hitungan LMTD lawan arah dan searah pada suhu ujung yang sama.", "purpose": "Memberi angka beda suhu penggerak rata-rata yang bisa disimpan.", "watch": "65 per 44 = 1,48. Itulah asal angka sekitar 48% di layar."},
            {"start": 27.2, "end": 34, "role": "PAYOFF", "title": "Musuhnya kerak (fouling)", "on_screen": "Kerak 1 mm memangkas fluks sekitar 10%, unit berhenti untuk dibersihkan", "visual": "Endapan di dinding menebal, angka 186 juta barel per tahun, unit berhenti.", "purpose": "Menjawab tension utama: kenapa alat sepele bisa menghentikan pabrik.", "watch": "Fouling diperkenalkan sebagai endapan di dinding sebelum istilahnya dipakai. Urutan ini disengaja."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Arah menentukan efisiensi, kerak menentukan berhenti", "on_screen": "Arahnya menentukan efisiensi, keraknya menentukan kapan pabrik berhenti", "visual": "Heat exchanger bersih berjalan, ajakan follow satu video satu alat.", "purpose": "Menutup dengan dua kalimat penentu yang bisa diingat.", "watch": "Follow @ilmutekkim. Satu video, satu alat pabrik dibedah sampai prinsip dan angkanya."},
        ],
    },
    {
        "slug": "haber-bosch-udara-jadi-pupuk",
        "title": "Haber-Bosch: Udara Menjadi Pupuk, Proses Paling Penting di Dunia",
        "hook": "Udara menjadi pupuk.",
        "date": "2026-10-03",
        "ig": "https://www.instagram.com/reel/DeCCKsyvr7j/",
        "src": "~/workspace/coded-motion-graphics/videos/amonia/renders/amonia_v3_2026-10-01_20-21.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Proses Pupuk",
        "intro": "78% udara adalah nitrogen, tapi tanaman tidak bisa memakannya langsung. Video ini membedah Haber-Bosch: persamaan, tiga syarat ekstrem, dan kenapa tanpa recycle pabriknya rugi.",
        "tension": "Nitrogen malas bereaksi karena ikatan rangkap tiganya terlalu kuat. Bagaimana cara memaksanya jadi amonia?",
        "takeaway": "Udara, tekanan, dan katalis menjadi makanan dunia: N2 + 3H2 menjadi 2NH3, kemudian menjadi urea dan pupuk nitrogen.",
        "facts": [
            "Persamaan setimbang: N2 + 3H2 menjadi 2NH3. Cek atom: N 2 atom, H 6 atom, seimbang. Ikatan N rangkap tiga sangat kuat, ikatan H tunggal mudah putus.",
            "Tiga syarat ekstrem: katalis besi memecah ikatan N, suhu tinggi 400 sampai 500°C mempercepat reaksi, tekanan tinggi 150 sampai 250 bar mendorong ke produk (Le Chatelier: 4 mol gas menjadi 2 mol gas).",
            "Reaksi eksotermik dengan delta H sekitar minus 92 kJ per mol. Sekali lewat reaktor cuma sekitar 15% yang jadi, sisanya diputar balik lewat kondensasi dan recycle. Terlalu panas, kesetimbangan bergeser balik.",
        ],
        "quiz": {
            "q": "Mengapa tekanan tinggi membantu Haber-Bosch?",
            "options": ["Karena membuat katalis meleleh", "Karena 4 mol gas menjadi 2 mol gas; semakin ditekan, semakin terbentuk amonia (Le Chatelier)", "Karena menurunkan suhu reaktor"],
            "answer": 1,
            "explain": "Jumlah mol gas berkurang dari 4 ke 2. Tekanan tinggi mendorong kesetimbangan ke sisi produk yang jumlah molnya lebih sedikit.",
        },
        "scenes": [
            {"start": 0, "end": 6.8, "role": "HOOK", "title": "Udara jadi pupuk", "on_screen": "UDARA JADI PUPUK. 78% udara adalah nitrogen", "visual": "Udara dan gas alam menjadi NH3 amonia, label Proses Haber-Bosch.", "purpose": "Mengklaim gas malas di udara bisa diubah jadi pupuk.", "watch": "78% di hook ini adalah kandungan nitrogen di udara yang kamu hirup."},
            {"start": 6.8, "end": 13.6, "role": "KONTEKS", "title": "Persamaan setimbang dan ikatan keras kepala", "on_screen": "N2 + 3H2 menjadi 2NH3. IKATAN YANG KERAS KEPALA", "visual": "N rangkap tiga sangat kuat vs H tunggal mudah putus, cek atom N 2 dan H 6.", "purpose": "Menunjukkan kenapa nitrogen malas bereaksi.", "watch": "Cek atomnya tampil di layar. Persamaan ini setimbang, bukan karangan."},
            {"start": 13.6, "end": 20.4, "role": "SYARAT", "title": "Tiga syarat ekstrem", "on_screen": "TIGA SYARAT EKSTREM. Katalis besi, 400 sampai 500°C, 150 sampai 250 bar", "visual": "Tiga kartu: katalis Fe, suhu tinggi, tekanan tinggi, plus Le Chatelier 4 mol ke 2 mol.", "purpose": "Memberi syarat yang membuat reaksi mau jalan.", "watch": "Tanpa ketiganya, nitrogen tetap malas. Tiga kartu ini jangan dibaca terpisah."},
            {"start": 20.4, "end": 27.2, "role": "LOOP", "title": "Tanpa recycle, rugi", "on_screen": "TANPA RECYCLE, RUGI. Sekali lewat cuma sekitar 15% yang jadi", "visual": "Kompresi, reaktor bed katalis Fe, kondensasi NH3 cair dipisahkan, recycle loop tertutup.", "purpose": "Menjelaskan loop pabrik amonia yang sebenarnya.", "watch": "NH3 cair dipisahkan di kondensasi, gas sisa diputar balik. Bahan tidak terbuang."},
            {"start": 27.2, "end": 34, "role": "ANGKA", "title": "Eksotermik, melepas panas", "on_screen": "EKSOTERMIK. MELEPAS PANAS. Delta H sekitar minus 92 kJ per mol", "visual": "Delta H negatif, amonia menjadi urea dan amonium nitrat.", "purpose": "Memberi angka panas reaksi dan produk lanjutannya.", "watch": "Terlalu panas justru menggeser kesetimbangan balik. Panas di sini pedang bermata dua."},
            {"start": 34, "end": 40.9, "role": "TAKEAWAY", "title": "Udara jadi makanan", "on_screen": "UDARA JADI MAKANAN. Udara + tekanan + katalis = makanan dunia", "visual": "N2 + 3H2 menjadi 2NH3 dari udara ke piring, ajakan follow.", "purpose": "Menutup dengan makna proses untuk pangan dunia.", "watch": "Intinya satu persamaan di akhir. Follow @ilmutekkim buat teknik kimia tiap hari."},
        ],
    },
    {
        "slug": "netralisasi-asam-basa",
        "title": "Netralisasi Asam Basa: Yang Sebenarnya Bereaksi Hanya Dua Ion",
        "hook": "Asam bertemu basa, keduanya saling menetralkan.",
        "date": "2026-10-02",
        "ig": "https://www.instagram.com/reel/DeBVDRiPs35/",
        "src": "~/workspace/coded-motion-graphics/videos/asam-basa/renders/asam-basa_v4_2026-10-01_13-46.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Kimia Dasar Proses",
        "intro": "HCl + NaOH menjadi NaCl + H2O terlihat seperti tukar pasangan. Video ini membedah reaksi ion bersihnya, panas yang dilepas, dan kenapa titrasi harus tepat setetes demi setetes.",
        "tension": "Kalau persamaannya terlihat sederhana, apa yang sebenarnya bertabrakan dan membentuk air?",
        "takeaway": "Asam + basa = garam + air. Pada intinya, H+ + OH- menjadi H2O, reaksi paling fundamental dari laboratorium sekolah sampai netralisasi limbah pabrik.",
        "facts": [
            "Di larutan, HCl dan NaOH sudah terurai jadi ion. Yang benar-benar bereaksi adalah H+ + OH- menjadi H2O. Na+ dan Cl- menjadi garam NaCl. Atom dan muatan seimbang.",
            "Tiap mol air yang terbentuk melepas 57 kJ panas (delta H sekitar minus 57 kJ per mol), larutan jadi hangat. Reaksinya eksotermik.",
            "Titrasi butuh tepat 1 banding 1: 1 mol HCl butuh tepat 1 mol NaOH. Kelebihan setetes saja menggeser hasil. Fenolftalein jadi saksi: bening di asam, pink di basa, titik akhir di pH 7.",
        ],
        "quiz": {
            "q": "Dalam netralisasi HCl dan NaOH, spesies yang sebenarnya membentuk air adalah?",
            "options": ["Na+ dan Cl-", "H+ dan OH-", "HCl dan NaCl"],
            "answer": 1,
            "explain": "Itulah reaksi ion bersihnya: H+ + OH- menjadi H2O. Ion Na+ dan Cl- hanya menjadi garam dan tidak ikut membentuk air.",
        },
        "scenes": [
            {"start": 0, "end": 6.5, "role": "HOOK", "title": "Asam ketemu basa", "on_screen": "ASAM KETEMU BASA. Dua cairan ekstrem saling menjinakkan", "visual": "HCl (asam lambung, pembersih lantai) dan NaOH (soda api, bahan sabun), label Netralisasi.", "purpose": "Memperkenalkan dua cairan ekstrem dan nama reaksinya.", "watch": "Contoh sehari-hari di hook ini menjembatani lab dan pabrik."},
            {"start": 6.5, "end": 13, "role": "REAKSI", "title": "Tukar pasangan", "on_screen": "HCl + NaOH menjadi NaCl + H2O. TUKAR PASANGAN", "visual": "Atom bertukar pasangan, H pindah ke OH, cek atom dan muatan seimbang.", "purpose": "Menunjukkan persamaan molekuler yang biasa diajarkan.", "watch": "Dua tanda centang di scene ini: atom seimbang dan muatan seimbang. Keduanya wajib."},
            {"start": 13, "end": 19.5, "role": "ION", "title": "Reaksi ion bersih yang sebenarnya terjadi", "on_screen": "REAKSI ION BERSIH. YANG SEBENARNYA TERJADI: H+ + OH- menjadi H2O", "visual": "H+ + OH- jadi air, Na+ + Cl- jadi garam NaCl.", "purpose": "Membongkar bahwa cuma dua ion yang benar-benar bereaksi.", "watch": "Inilah payoff pertama video ini. Persamaan molekuler di scene sebelumnya disederhanakan di sini."},
            {"start": 19.5, "end": 26.5, "role": "PANAS", "title": "Eksotermik, melepas 57 kJ", "on_screen": "EKSOTERMIK. MELEPAS PANAS. Tiap mol air melepas 57 kJ", "visual": "Delta H minus 57 kJ per mol, larutan jadi hangat.", "purpose": "Memberi angka panas netralisasi yang bisa diingat.", "watch": "Delta H negatif artinya eksoterm. Angkanya per mol H2O yang terbentuk."},
            {"start": 26.5, "end": 33.5, "role": "TITRASI", "title": "Gimana tau kapan pas? Titrasi", "on_screen": "1 banding 1. Kelebihan setetes saja bikin hasil meleset. TITRASI", "visual": "NaOH diteteskan ke HCl plus fenolftalein, bening di asam pink di basa, pH 7.", "purpose": "Menjelaskan kenapa ketepatan setetes menentukan hasil.", "watch": "Fenolftalein di sini saksi visualnya, bukan hiasan. Warnanya yang memberi tau titik akhir."},
            {"start": 33.5, "end": 40.9, "role": "TAKEAWAY", "title": "Asam + basa = garam + air", "on_screen": "ASAM + BASA = GARAM + AIR. Dari obat maag sampai air limbah pabrik", "visual": "NaCl garam dapur dan air, ajakan follow teknik kimia tiap hari.", "purpose": "Menutup dengan persamaan fundamental dan cakupan pakainya.", "watch": "Intinya di akhir: H+ + OH- menjadi H2O. Satu reaksi, banyak skala."},
        ],
    },
    {
        "slug": "water-gas-shift-co-jadi-h2",
        "title": "Water-Gas Shift: Mengubah CO Beracun Menjadi H2",
        "hook": "CO adalah gas beracun yang diubah menjadi H2.",
        "date": "2026-10-02",
        "ig": "https://www.instagram.com/reel/Dd_doTMPk6j/",
        "src": "~/workspace/coded-motion-graphics/videos/shift-conversion/renders/shift-conversion_v1_2026-10-01_04-10-25.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Pabrik Hidrogen",
        "intro": "CO + H2O menjadi CO2 + H2 terlihat sepele, tapi jadi tulang punggung pabrik hidrogen. Video ini membedah kenapa shift harus dua tahap: panas dulu, dingin kemudian.",
        "tension": "Kesetimbangan suka dingin, kinetika suka panas. Bagaimana cara memuaskan keduanya?",
        "takeaway": "Shift berarti CO menjadi H2. Dua tahap reaktor (HTS kemudian LTS) dengan pendingin di tengahnya merupakan kompromi antara kecepatan reaksi dan kesetimbangan.",
        "facts": [
            "Reaksi shift eksotermik dengan delta H sekitar minus 41 kJ per mol. Atom H di H2 produk berasal dari air (steam), bukan dari CO.",
            "HTS (high temperature shift) 350 sampai 450°C katalis Fe-Cr menurunkan CO dari 15% jadi 3%. Setelah didinginkan dan panasnya dipanen jadi steam, LTS (low temperature shift) 200 sampai 250°C katalis Cu-Zn menurunkan CO dari 3% jadi 0,3%.",
            "Gas kaya H2 lalu ke CO2 removal dan PSA menghasilkan H2 murni 99,99%. Dua tahap diperlukan karena satu suhu tidak bisa cepat sekaligus tuntas.",
        ],
        "quiz": {
            "q": "Mengapa water-gas shift dibuat dalam dua tahap, HTS dan LTS?",
            "options": ["Agar pabriknya terlihat besar", "Karena kesetimbangan menyukai dingin sedangkan kinetika menyukai panas, sehingga diperlukan suhu tinggi dahulu kemudian suhu rendah", "Karena katalisnya hanya satu jenis"],
            "answer": 1,
            "explain": "HTS berlangsung cepat pada suhu tinggi tetapi tidak tuntas. LTS pada suhu rendah menggeser kesetimbangan hingga CO tersisa 0,3%. Pendingin di tengah memanen panasnya menjadi steam.",
        },
        "scenes": [
            {"start": 0, "end": 6.5, "role": "HOOK", "title": "CO itu racun, ubah jadi H2", "on_screen": "WATER-GAS SHIFT. CO ITU RACUN. UBAH JADI H2", "visual": "Syngas dan steam masuk, label CO ditolak, H2 sebagai tujuan.", "purpose": "Mengklaim CO harus diubah, bukan dibuang begitu saja.", "watch": "Steam + CO jadi H2 adalah ringkasan satu baris di hook ini."},
            {"start": 6.5, "end": 13, "role": "REAKSI", "title": "Persamaan shift yang eksotermik", "on_screen": "CO + H2O menjadi CO2 + H2. Delta H minus 41 kJ per mol", "visual": "Persamaan shift, panas dilepas, H produk dari air.", "purpose": "Memberi persamaan dan sumber atom hidrogennya.", "watch": "Banyak yang mengira H2 berasal dari CO. Di sini ditegaskan: dari air (steam)."},
            {"start": 13, "end": 19.5, "role": "HTS", "title": "Reaktor HTS 350 sampai 450°C", "on_screen": "REACTOR HTS 350 sampai 450°C Katalis Fe-Cr CO 15% jadi 3%", "visual": "Reaktor HTS dengan katalis Fe-Cr, CO turun drastis pertama.", "purpose": "Menunjukkan tahap cepat suhu tinggi.", "watch": "Angka 15% ke 3% adalah penurunan CO tahap pertama. Masih belum cukup bersih."},
            {"start": 19.5, "end": 26.5, "role": "COOLER", "title": "Didinginkan di tengah, panas jadi steam", "on_screen": "DIDINGINKAN DI TENGAH. Panasnya dipanen jadi steam", "visual": "Interstage cooler, panas dipanen jadi steam untuk dipakai lagi.", "purpose": "Menjelaskan kenapa ada pendingin antar reaktor.", "watch": "Panas eksotermik tidak dibuang. Dipanen jadi steam, inilah heat recovery-nya."},
            {"start": 26.5, "end": 33.5, "role": "LTS", "title": "Reaktor LTS 200 sampai 250°C", "on_screen": "REACTOR LTS 200 sampai 250°C Katalis Cu-Zn CO 3% jadi 0,3%", "visual": "Reaktor LTS katalis Cu-Zn, CO turun sampai sepersepuluh lagi.", "purpose": "Menunjukkan tahap tuntas suhu rendah.", "watch": "Katalisnya beda (Cu-Zn) karena suhunya beda. Satu katalis tidak cocok untuk dua suhu."},
            {"start": 33.5, "end": 40.9, "role": "TAKEAWAY", "title": "H2 murni 99,99%", "on_screen": "H2 MURNI 99,99%. SHIFT = CO JADI H2", "visual": "CO2 removal lalu PSA, H2 99,99%, ajakan follow.", "purpose": "Menutup dengan produk akhir dan alasan dua tahap.", "watch": "Kalimat penutupnya menjawab tension awal: dua tahap karena kesetimbangan dan kinetika maunya berlawanan."},
        ],
    },
    {'slug': 'b40-transesterifikasi-motion', 'title': 'B40: Transesterifikasi Sawit Menjadi Biodiesel', 'hook': 'Solar di SPBU tidak 100 persen minyak bumi, 40 persennya sawit.', 'date': '2026-10-18', 'ig': 'https://www.instagram.com/reel/Deo14FWk23b/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-18/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-18/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Biodiesel dan Energi', 'intro': 'Sejak Januari 2025, solar di Indonesia wajib B40, yaitu campuran 40 persen biodiesel dari sawit dan 60 persen solar minyak bumi. Video ini membedah reaksi transesterifikasi yang mengubah trigliserida sawit menjadi FAME sebelum pencampuran dilakukan.', 'tension': 'Solar yang dibeli setiap hari ternyata tidak murni minyak bumi, dan minyak sawit mentah tidak dapat langsung dicampurkan karena trigliseridanya terlalu kental dan tidak stabil.', 'takeaway': 'Satu tangki solar B40 adalah hasil reaksi kimia sawit: trigliserida diubah menjadi FAME melalui transesterifikasi, kemudian dicampurkan 40 berbanding 60 dengan solar minyak bumi.', 'facts': ['B40 adalah campuran 40 persen biodiesel (FAME dari minyak sawit) dan 60 persen solar, dengan mandatori di Indonesia mulai 1 Januari 2025.', 'Transesterifikasi mengubah trigliserida dengan 3 metanol menjadi 3 FAME (biodiesel) dan gliserol, dengan katalis basa.', 'Minyak sawit mentah tidak dapat langsung dicampurkan karena trigliseridanya terlalu kental dan tidak stabil.'], 'quiz': {'answer': 1, 'explain': 'Transesterifikasi mereaksikan trigliserida dengan 3 metanol berkatalis basa menjadi 3 FAME dan gliserol. FAME yang dihasilkan kemudian dicampur 40 berbanding 60 dengan solar menjadi B40.', 'options': ['Trigliserida + air menjadi solar + gliserol', 'Trigliserida + 3 metanol menjadi 3 FAME + gliserol', 'CPO langsung dicampur tanpa reaksi menjadi B40'], 'q': 'Reaksi transesterifikasi pada pembuatan biodiesel B40 adalah?'}, 'scenes': [{'end': 7, 'on_screen': 'SOLAR DI SPBU TIDAK 100 PERSEN MINYAK BUMI, 40 PERSENNYA SAWIT', 'purpose': 'Menohok penonton dengan fakta solar yang dibeli tiap hari tidak murni minyak bumi.', 'role': 'HOOK', 'start': 0, 'title': 'Komposisi solar yang tidak murni minyak bumi', 'visual': 'Headline kinetik dua baris masuk berurutan, jeriken solar berputar pelan di tengah frame.', 'watch': 'Baca dua baris judul dan jeriken solar di tengah bingkai sebagai klaim komposisi yang akan dibuktikan.'}, {'end': 14, 'on_screen': 'SEJAK JANUARI 2025, SOLAR DI INDONESIA WAJIB B40', 'purpose': 'Membangun tension: aturan mandatori membuat fakta hook tidak bisa dihindari.', 'role': 'TENSION', 'start': 7, 'title': 'Mandatori B40 sejak Januari 2025', 'visual': 'Bar komposisi 40:60 terisi animasi, label B40 muncul, kalender Januari 2025 ditandai.', 'watch': 'Perhatikan batang komposisi 40 berbanding 60 dan penanda kalender Januari 2025 sebagai dasar aturannya.'}, {'end': 21, 'on_screen': 'TAPI MINYAK SAWIT MENTAH TIDAK BISA LANGSUNG DICAMPUR', 'purpose': 'Membangun tension kedua: ada masalah teknis yang harus dipecahkan dulu.', 'role': 'TENSION', 'start': 14, 'title': 'Trigliserida yang terlalu kental', 'visual': 'Tetesan minyak kental menetes lambat, molekul trigliserida digambar sebagai tiga rantai asam lemak.', 'watch': 'Amati tetesan yang bergerak lambat dan gambar molekul dengan tiga rantai asam lemak sebagai akar persoalannya.'}, {'end': 28, 'on_screen': 'TRANSESTERIFIKASI: TRIGLISERIDA + METANOL JADI BIODIESEL + GLISEROL', 'purpose': 'Payoff tahap satu: reaksi kimia yang mengubah minyak kental jadi biodiesel.', 'role': 'PAYOFF', 'start': 21, 'title': 'Reaksi transesterifikasi menghasilkan FAME', 'visual': 'Animasi molekul: trigliserida bertemu metanol, panah reaksi, terpecah menjadi FAME dan gliserol.', 'watch': 'Ikuti pecahnya molekul trigliserida setelah panah reaksi menjadi molekul FAME dan gliserol.'}, {'end': 35, 'on_screen': 'FAME DICAMPUR 40:60 DENGAN SOLAR, JADILAH B40', 'purpose': 'Payoff tahap dua: dari molekul ke produk yang dibeli di SPBU.', 'role': 'PAYOFF', 'start': 28, 'title': 'Pencampuran FAME 40 berbanding 60', 'visual': 'FAME mengalir ke tangki pencampur, bar 40:60 terisi, label B40 muncul di tangki.', 'watch': 'Perhatikan pengisian batang 40 berbanding 60 pada tangki pencampur sampai label B40 tampil.'}, {'end': 41, 'on_screen': 'SATU TANGKI SOLAR = HASIL REAKSI KIMIA SAWIT. SIMPAN VIDEO INI.', 'purpose': 'Takeaway satu kalimat plus ajakan simpan sebagai bahan diskusi.', 'role': 'TAKEAWAY', 'start': 35, 'title': 'Satu tangki solar sebagai hasil reaksi kimia', 'visual': 'Takeaway kinetik satu kalimat, tombol simpan berdenyut pelan, watermark @ilmutekkim.', 'watch': 'Baca kalimat penutup pada tangki sebagai rangkuman seluruh rantai reaksi dan pencampurannya.'}]},
    {'slug': 'confined-space-masuk-tangki', 'title': 'Masuk Tangki dan Ruang Terbatas: Mengapa Izin, Uji Gas, dan Penjaga Tidak Boleh Dilewati', 'hook': 'Tangki kosong terlihat aman. Isi udaranya belum tentu aman.', 'date': '2026-10-10', 'ig': 'https://www.instagram.com/reel/DeUS8KHjw_f/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-10/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-10/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Keselamatan Proses', 'intro': 'Tangki, vessel, dan ruang terbatas lain dapat menyimpan sisa uap dan udara yang tidak layak napas walaupun tampak kosong dari luar. Video ini membedah urutan pengaman yang wajib dibuktikan sebelum satu orang pun masuk ke dalamnya.', 'tension': 'Sisa uap dan oksigen yang rendah tidak terlihat dari luar, sehingga masuk tanpa urutan pengaman dapat membuat penolong yang menyusul ikut menjadi korban.', 'takeaway': 'Keadaan kosong tidak membuktikan apa pun. Yang membuktikan ruang terbatas aman dimasuki adalah izin tertulis, pengujian gas, ventilasi, penjaga di luar, dan rencana penyelamatan yang tidak mengorbankan penolong.', 'facts': ['Pekerjaan masuk ruang terbatas seperti tangki memerlukan izin tertulis dan pengujian atmosfer sebelum dan selama pekerjaan berlangsung.', 'Urutan pengamannya mencakup ventilasi, penjaga yang bertugas di luar ruang terbatas, dan rencana penyelamatan yang telah disiapkan sebelum pekerjaan dimulai.', 'Penolong tidak boleh masuk tanpa alat pelindung pernapasan yang sesuai, karena udara yang melumpuhkan pekerja pertama akan melumpuhkan penolong dengan cara yang sama.'], 'quiz': {'q': 'Mengapa penolong tidak boleh langsung masuk mengejar pekerja yang pingsan di dalam tangki?', 'options': ['Karena jumlah pekerja di luar harus tetap genap', 'Karena udara yang melumpuhkan pekerja pertama akan melumpuhkan penolong juga, sehingga penyelamatan mensyaratkan alat napas dan peralatan penarik dari luar', 'Karena izin tertulis melarang lebih dari satu orang di dalam tangki'], 'answer': 1, 'explain': 'Bahaya di ruang terbatas adalah atmosfernya, bukan lokasinya. Penolong yang masuk tanpa alat pelindung pernapasan menghirup udara yang sama dan menjadi korban berikutnya, sehingga penyelamatan dirancang melalui penjaga di luar, tali penarik, dan alat napas yang sesuai.'}, 'scenes': [{'start': 0, 'end': 6, 'role': 'HOOK', 'title': 'Tangki kosong yang tampak aman', 'on_screen': 'Tangki kosong terlihat aman. Isi udaranya belum tentu aman', 'visual': 'Tangki besar cerah terbuka, pekerja mendekat lalu berhenti di garis izin, awan gas samar di dalam tangki mulai terlihat', 'purpose': 'Membuka serangan bahwa tangki kosong yang terlihat aman bisa menyimpan bahaya tidak terlihat', 'watch': 'Perhatikan pekerja yang berhenti di garis izin dan awan gas samar di dalam tangki: keduanya adalah pernyataan utama video ini.'}, {'start': 6, 'end': 13, 'role': 'TENSION', 'title': 'Bahaya yang tidak dapat dinilai dengan mata', 'on_screen': 'Sisa uap dan oksigen rendah tidak terlihat dari luar', 'visual': 'Potongan tangki memperlihatkan lapisan gas samar di dasar dan indikator oksigen yang belum diperiksa', 'purpose': 'Menunjukkan bahaya yang tidak bisa dinilai hanya dengan mata', 'watch': 'Lapisan gas di dasar tangki dan indikator oksigen yang belum diperiksa menunjukkan bahwa penampakan kosong tidak memberikan informasi tentang atmosfer di dalamnya.'}, {'start': 13, 'end': 20, 'role': 'TENSION', 'title': 'Siapa yang membuktikan udara di dalam aman', 'on_screen': 'Siapa yang membuktikan udara di dalam aman sebelum orang masuk?', 'visual': 'Detektor gas diulurkan ke dalam tangki dari luar, layar alat menampilkan hasil uji bertahap', 'purpose': 'Menahan jawaban dengan pertanyaan siapa yang memastikan udara di dalam layak napas', 'watch': 'Detektor diulurkan dari luar sebelum ada orang di dalam, dan urutan posisi ini merupakan bagian dari pengamannya, bukan detail kebetulan.'}, {'start': 20, 'end': 27, 'role': 'PAYOFF', 'title': 'Urutan pengaman sebelum masuk', 'on_screen': 'Izin tertulis, uji gas, ventilasi, baru boleh masuk', 'visual': 'Empat kartu urutan muncul berurutan dengan ukuran seragam: izin, detektor gas, blower ventilasi, pekerja masuk dengan tali pengaman', 'purpose': 'Memberi urutan pengaman inti sebelum satu orang pun masuk', 'watch': 'Empat kartu tampil berurutan dengan ukuran seragam: izin, uji gas, ventilasi, dan terakhir pekerja masuk dengan tali pengaman.'}, {'start': 27, 'end': 34, 'role': 'PAYOFF', 'title': 'Penjaga di luar dan penyelamatan tanpa korban baru', 'on_screen': 'Satu orang menjaga di luar. Penolong tidak masuk tanpa alat napas', 'visual': 'Pekerja di dalam terhubung tali ke tripod, penjaga di luar memegang ujung tali dan radio, ikon larangan masuk tanpa alat napas muncul', 'purpose': 'Menegaskan peran penjaga di luar dan larangan penyelamatan tanpa alat', 'watch': 'Tali yang menghubungkan pekerja ke tripod dan penjaga yang memegang ujungnya di luar adalah mekanisme penyelamatan yang tidak menuntut penolong masuk.'}, {'start': 34, 'end': 40.9, 'role': 'TAKEAWAY', 'title': 'Izin dan uji gas yang membuktikan keamanan', 'on_screen': 'Kosong terlihatnya, izin dan uji gas yang membuktikan amannya. Simpan video ini', 'visual': 'Tangki cerah dengan semua perangkat pengaman lengkap, pekerja keluar dengan selamat, watermark @ilmutekkim', 'purpose': 'Menutup dengan kesimpulan satu kalimat dan aksi simpan', 'watch': 'Adegan penutup menampilkan perangkat pengaman yang lengkap dan pekerja yang keluar dengan selamat, sebagai hasil dari urutan yang tidak dilompati.'}]},
    {'slug': 'dead-leg-pipa-buntu-berbahaya', 'title': 'Dead Leg: Pipa Buntu yang Diam-Diam Berbahaya', 'hook': 'Pipa buntu yang tidak dialiri justru menyimpan bahaya yang tidak terlihat.', 'date': '2026-10-15', 'ig': 'https://www.instagram.com/reel/DehLEvYE7tO/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-15/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-15/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Perpipaan dan Keselamatan Proses', 'intro': 'Dead leg adalah cabang pipa buntu yang tidak dialiri fluida. Video ini membedah alasan cabang yang diam tersebut berbahaya, dari fluida yang stagnan sampai kontaminan yang terdorong masuk ke aliran utama saat katup dibuka.', 'tension': 'Cabang pipa yang tidak dipakai terlihat tidak bermasalah, padahal di dalamnya fluida stagnan, korosi berjalan terus, dan endapan menumpuk tanpa terlihat dari luar.', 'takeaway': 'Pipa yang tidak dialiri tetap harus dirawat. Cabang buntu dihindari dari desain, dibuat sesingkat mungkin apabila terpaksa ada, dan dibilas secara berkala.', 'facts': ['Dead leg adalah cabang pipa buntu tanpa aliran sehingga fluidanya stagnan.', 'Kondisi stagnan mempercepat korosi setempat dan pertumbuhan mikroba pada dinding pipa.', 'Aturan praktis perlindungan korosi menyatakan cabang dari jalur beraliran dengan rasio panjang terhadap diameter (L/D) melebihi 3 kemungkinan besar bermasalah.'], 'quiz': {'answer': 1, 'explain': 'Di dalam cabang tanpa aliran, fluida stagnan sehingga korosi setempat dan endapan menumpuk tanpa terbawa aliran. Saat katup dibuka atau aliran dialihkan, tumpukan itu terdorong masuk ke aliran utama dan mengotori produk.', 'options': ['Karena cabang buntu menerima tekanan paling tinggi di pabrik', 'Karena fluida di dalamnya stagnan sehingga korosi dan endapan menumpuk, kemudian terdorong ke aliran utama saat aliran berubah', 'Karena cabang buntu selalu terbuat dari bahan yang lebih lemah'], 'q': 'Mengapa cabang pipa buntu yang tidak dialiri berbahaya bagi aliran utama?'}, 'scenes': [{'end': 6, 'on_screen': 'PIPA BUNTU / DIAM-DIAM BERBAHAYA', 'purpose': 'Menancapkan fakta bahwa pipa yang tidak dipakai justru berbahaya.', 'role': 'HOOK', 'start': 0, 'title': 'Cabang buntu disorot pada pipa utama', 'visual': 'Pipa utama beranimasi aliran; satu cabang buntu disorot lingkaran peringatan.', 'watch': 'Perhatikan cabang yang disorot peringatan pada pipa utama yang beraliran sebagai pokok persoalan video ini.'}, {'end': 13, 'on_screen': 'Dead leg: cabang pipa yang tidak dialiri', 'purpose': 'Menjelaskan apa itu dead leg: cabang tanpa aliran.', 'role': 'TENSION', 'start': 6, 'title': 'Aliran berhenti di mulut cabang', 'visual': 'Aliran berhenti di mulut cabang; partikel di dalam cabang diam.', 'watch': 'Bandingkan partikel yang bergerak pada aliran utama dengan partikel yang diam di dalam cabang.'}, {'end': 20, 'on_screen': 'Diam bukan berarti aman: korosi dan endapan menumpuk', 'purpose': 'Menunjukkan bahaya yang menumpuk diam-diam: korosi dan endapan.', 'role': 'TENSION', 'start': 13, 'title': 'Korosi dan endapan menumpuk di cabang', 'visual': 'Dinding cabang menebal karat; endapan menumpuk di dasar cabang.', 'watch': 'Amati lapisan karat yang menebal pada dinding dan endapan yang bertambah di dasar cabang.'}, {'end': 27, 'on_screen': 'Saat aliran berubah, semuanya ikut ke produk', 'purpose': 'Menunjukkan momen bahaya: kontaminan terdorong ke aliran utama.', 'role': 'PAYOFF', 'start': 20, 'title': 'Kontaminan terdorong ke aliran utama', 'visual': 'Valve terbuka; endapan terdorong masuk ke pipa utama dan terbawa aliran.', 'watch': 'Ikuti gerakan endapan dari cabang masuk ke pipa utama sesaat setelah katup terbuka.'}, {'end': 35, 'on_screen': 'Hindari cabang buntu. Kalau terpaksa, buat sependek mungkin dan flush berkala.', 'purpose': 'Memberi solusi desain yang benar.', 'role': 'PAYOFF', 'start': 27, 'title': 'Desain ulang cabang dan pembilasan berkala', 'visual': 'Cabang buntu dipotong menjadi loop; jadwal flush muncul sebagai checklist.', 'watch': 'Perhatikan perubahan bentuk cabang menjadi lintasan berputar dan daftar periksa pembilasan sebagai penyelesaiannya.'}, {'end': 41, 'on_screen': 'Pipa yang tidak dialiri tetap harus dirawat. Simpan video ini.', 'purpose': 'Takeaway satu kalimat dan ajakan simpan.', 'role': 'TAKEAWAY', 'start': 35, 'title': 'Pipa tanpa aliran tetap memerlukan perawatan', 'visual': 'Kartu takeaway muncul; watermark dan progress bar penuh.', 'watch': 'Baca kartu penutup sebagai kesimpulan bahwa ketiadaan aliran tidak menghapus kewajiban perawatan.'}]},
    {'slug': 'flare-stack-api-kilang-menyala', 'title': 'Flare Stack: Mengapa Api di Kilang Menyala Terus sebagai Alat Pengaman Terakhir', 'hook': 'Api di kilang menyala terus, bukan buang-buang gas.', 'date': '2026-10-13', 'ig': 'https://www.instagram.com/reel/DecBcGjD3fR/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-13/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-13/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Kilang dan Keselamatan Proses', 'intro': 'Api yang menyala terus di ujung cerobong tertinggi kilang sering dibaca sebagai pemborosan gas. Video ini membedah dari mana gas yang dibakar itu berasal, mengapa gas tersebut harus melewati knockout drum terlebih dahulu, dan mengapa pilot burner tidak boleh padam.', 'tension': 'Banyak orang mengira api di kilang adalah gas yang dibakar sia-sia, padahal api tersebut adalah alat pengaman terakhir yang tidak boleh padam.', 'takeaway': 'Flare adalah alat pengaman terakhir: tekanan berlebih dibuang dari sistem, gasnya dibakar menjadi karbon dioksida dan uap air, dan apinya dijaga agar tidak pernah padam.', 'facts': ['Flare membakar gas hidrokarbon berlebih menjadi karbon dioksida dan uap air agar gas tersebut tidak dilepas mentah ke udara.', 'Gas menuju flare berasal dari katup pengaman, blowdown, dan pelepasan saat penyalaan atau penghentian operasi.', 'Knockout drum memisahkan cairan dari aliran gas, sehingga hanya gas yang sampai ke ujung flare.'], 'quiz': {'q': 'Mengapa gas berlebih tidak dilepas mentah ke udara, melainkan dialirkan ke flare untuk dibakar?', 'options': ['Agar kilang tampak beroperasi pada malam hari', 'Karena pembakaran mengubah gas hidrokarbon menjadi karbon dioksida dan uap air, sedangkan pelepasan mentah membuang hidrokarbon yang belum terbakar langsung ke udara', 'Karena gas tidak dapat mengalir tanpa dibakar'], 'answer': 1, 'explain': 'Gas berlebih harus keluar dari sistem demi keselamatan tekanan, tetapi pelepasannya tidak harus berbentuk gas hidrokarbon mentah. Flare membakarnya menjadi karbon dioksida dan uap air, dan pilot burner menjaga pembakaran itu selalu tersedia pada saat gas datang.'}, 'scenes': [{'start': 0, 'end': 6.5, 'role': 'HOOK', 'title': 'Api kilang yang menyala terus', 'on_screen': 'API DI KILANG MENYALA TERUS BUKAN BUANG-BUANG GAS', 'visual': 'Kilang malam yang terang, flare stack tinggi dengan api menyala di ujungnya. Kamera mendekat ke api.', 'purpose': 'Hook: api flare yang terlihat boros ternyata alat pengaman', 'watch': 'Flare stack adalah cerobong tertinggi di kilang dan apinya berada di ujung paling atas; posisi itu sendiri merupakan petunjuk bahwa fungsinya berkaitan dengan pelepasan ke tempat yang aman.'}, {'start': 6.5, 'end': 13, 'role': 'TENSION', 'title': 'Miskonsepsi bahwa gas dibakar sia-sia', 'on_screen': 'ORANG MENGIRA GAS DIBAKAR SIA-SIA', 'visual': 'Siluet pengamat menunjuk ke arah api, tanda tanya besar muncul di sampingnya.', 'purpose': 'Tension: miskonsepsi umum bahwa flare adalah pemborosan', 'watch': 'Tanda tanya di samping pengamat merumuskan miskonsepsi yang akan dijawab: gas yang terlihat terbakar belum tentu gas yang terbuang tanpa fungsi.'}, {'start': 13, 'end': 20, 'role': 'TENSION', 'title': 'Gas berlebih harus keluar dari sistem', 'on_screen': 'GAS BERLEBIH HARUS KELUAR DARI SISTEM', 'visual': 'Bejana bertekanan dengan relief valve terbuka, aliran gas keluar dengan panah ke atas.', 'purpose': 'Tension: tekanan berlebih wajib dibuang, tidak bisa ditahan', 'watch': 'Katup pengaman yang terbuka pada bejana bertekanan adalah titik awal alirannya: gas ini keluar karena tekanan di dalam sistem wajib diturunkan.'}, {'start': 20, 'end': 27, 'role': 'PAYOFF', 'title': 'Jalur gas melalui knockout drum', 'on_screen': 'GAS MENGALIR KE FLARE LEWAT KNOCKOUT DRUM', 'visual': 'Aliran gas bergerak lewat pipa ke knockout drum yang memisahkan tetesan cairan, lalu gas lanjut naik ke flare stack.', 'purpose': 'Payoff: jalur gas dari sistem ke flare divisualkan', 'watch': 'Knockout drum berada di tengah jalur dan memisahkan tetesan cairan dari aliran, sehingga yang melanjutkan perjalanan naik ke ujung flare hanyalah gas.'}, {'start': 27, 'end': 34, 'role': 'PAYOFF', 'title': 'Pilot burner yang menjaga api tetap menyala', 'on_screen': 'PILOT BURNER MENJAGA API TETAP MENYALA', 'visual': 'Ujung flare diperbesar, pilot burner kecil menyala terus, gas terbakar menjadi label karbon dioksida dan uap air.', 'purpose': 'Payoff: api tidak boleh padam karena gas mentah akan lolos', 'watch': 'Pilot burner adalah api kecil yang menyala terus di ujung flare, dan label hasil bakarnya menunjukkan perubahan gas hidrokarbon menjadi karbon dioksida dan uap air.'}, {'start': 34, 'end': 40.9, 'role': 'TAKEAWAY', 'title': 'Flare sebagai alat pengaman terakhir', 'on_screen': 'FLARE = ALAT PENGAMAN TERAKHIR. SIMPAN VIDEO INI.', 'visual': 'Tiga kartu ringkas: buang tekanan, bakar jadi CO2, jangan padam. Kartu CTV simpan muncul.', 'purpose': 'Takeaway: tiga poin ringkas dan CTV simpan', 'watch': 'Tiga kartu penutup merangkum fungsinya secara berurutan: buang tekanan, bakar menjadi CO2, dan jangan padam.'}]},
    {'slug': 'gudang-bahan-kimia-segregasi-bunding', 'title': 'Gudang Bahan Kimia: Segregasi Berdasarkan Kompatibilitas dan Fungsi Bunding Penahan Tumpahan', 'hook': 'Gudang kimia salah tata bisa jadi bom waktu.', 'date': '2026-10-12', 'ig': 'https://www.instagram.com/reel/DeZiI7IiXbS/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-12/motion-1-v2/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-12/motion-1-v2/cover.jpg', 'duration': 40.9, 'tag': 'Penyimpanan Bahan Kimia', 'intro': 'Gudang bahan kimia tidak ditata berdasarkan kerapian, melainkan berdasarkan kompatibilitas bahan yang disimpan di dalamnya. Video ini membedah dua pasangan bahan yang tidak boleh bertemu, pembagian zona penyimpanan menurut kelas bahaya, dan fungsi bunding sebagai pertahanan lapis kedua.', 'tension': 'Gudang kimia yang mencampur oksidator dengan bahan mudah terbakar adalah bom waktu yang menunggu pemicu.', 'takeaway': 'Periksa kompatibilitas sebelum menyimpan, pisahkan bahan ke dalam zona menurut kelas bahayanya, dan pastikan bunding tersedia untuk menahan tumpahan tetap berada di zonanya.', 'facts': ['Mencampur pemutih (natrium hipoklorit) dengan asam melepaskan gas klorin yang beracun.', 'Bahan oksidator yang tercampur dengan bahan mudah terbakar dapat memicu kebakaran.', 'Isi gudang bahan kimia dipisahkan berdasarkan kompatibilitas ke dalam zona mudah terbakar, zona korosif, dan zona oksidator, masing-masing dengan jarak dan pembatas fisik, sedangkan bunding menahan tumpahan agar tidak menyebar ke zona lain.'], 'quiz': {'q': 'Pasangan bahan mana yang pelepasannya menghasilkan gas klorin beracun apabila tercampur?', 'options': ['Asam dengan pemutih (natrium hipoklorit)', 'Oksidator dengan bahan mudah terbakar', 'Dua bahan korosif dari kelas yang sama'], 'answer': 0, 'explain': 'Asam yang bertemu pemutih (natrium hipoklorit) melepaskan gas klorin yang beracun. Pasangan oksidator dengan bahan mudah terbakar berbahaya melalui jalur yang berbeda, yaitu pemicuan kebakaran, dan keduanya menjadi alasan segregasi gudang berdasarkan kompatibilitas.'}, 'scenes': [{'start': 0, 'end': 6.5, 'role': 'HOOK', 'title': 'Gudang kimia yang salah tata', 'on_screen': 'GUDANG KIMIA SALAH TATA BISA JADI BOM WAKTU', 'visual': 'Gudang terang berisi drum-drum berlabel. Satu drum menetes, tetesan mengalir ke drum lain. Ikon peringatan muncul.', 'purpose': 'Hook: gudang kimia yang salah tata menyimpan bahaya tak terlihat', 'watch': 'Satu drum yang menetes dan tetesannya yang mengalir menuju drum lain adalah seluruh persoalannya: di gudang kimia, kebocoran kecil bergerak menuju bahan lain.'}, {'start': 6.5, 'end': 13, 'role': 'TENSION', 'title': 'Asam bertemu pemutih menghasilkan gas klorin', 'on_screen': 'ASAM + PEMUTIH = GAS KLORIN BERACUN', 'visual': 'Dua drum (asam dan pemutih) bersebelahan, cairannya bercampur, muncul awan gas berlabel bahaya.', 'purpose': 'Tension: contoh konkret inkompatibilitas yang menghasilkan gas beracun', 'watch': 'Dua drum yang bersebelahan dan awan gas yang muncul dari campurannya menunjukkan bahwa kedekatan fisik saja sudah cukup menjadi jalur kejadian.'}, {'start': 13, 'end': 20, 'role': 'TENSION', 'title': 'Oksidator bertemu bahan mudah terbakar', 'on_screen': 'OKSIDATOR + BAHAN MUDAH TERBAKAR = API', 'visual': 'Drum oksidator di samping karton bahan mudah terbakar, muncul simbol api dan peringatan.', 'purpose': 'Tension: contoh kedua, oksidator bertemu bahan mudah terbakar', 'watch': 'Simbol api pada pasangan kedua ini membedakannya dari pasangan pertama: yang satu menghasilkan gas beracun, yang lain memicu kebakaran.'}, {'start': 20, 'end': 27, 'role': 'PAYOFF', 'title': 'Segregasi berdasarkan kompatibilitas', 'on_screen': 'PISAH BERDASARKAN KOMPATIBILITAS', 'visual': 'Denah gudang terbagi tiga zona berwarna: mudah terbakar, korosif, oksidator, dengan pembatas fisik dan label tiap zona.', 'purpose': 'Payoff: solusi segregasi divisualkan sebagai peta zonasi', 'watch': 'Denah yang terbagi menjadi zona mudah terbakar, korosif, dan oksidator dengan pembatas fisik dan label pada setiap zona adalah wujud praktis dari segregasi.'}, {'start': 27, 'end': 34, 'role': 'PAYOFF', 'title': 'Bunding menahan tumpahan di zonanya', 'on_screen': 'BUNDING MENAHAN TUMPAHAN DI ZONANYA', 'visual': 'Tangki di dalam tanggul bunding. Cairan tumpah dari tangki tertahan di dalam tanggul, tidak mengalir ke zona lain.', 'purpose': 'Payoff: bunding sebagai pertahanan lapis kedua', 'watch': 'Cairan tumpah yang berhenti di dalam tanggul dan tidak mengalir ke zona lain adalah fungsi bunding yang harus dibaca pada adegan ini.'}, {'start': 34, 'end': 40.9, 'role': 'TAKEAWAY', 'title': 'Periksa kompatibilitas sebelum menyimpan', 'on_screen': 'CEK KOMPATIBILITAS SEBELUM MENYIMPAN. SIMPAN VIDEO INI.', 'visual': 'Tiga kartu ringkas: cek kompatibilitas, pisah zona, pastikan bunding. Kartu CTV simpan muncul.', 'purpose': 'Takeaway: tiga aturan ringkas dan CTV simpan', 'watch': 'Tiga kartu penutup merangkum seluruh urutannya: periksa kompatibilitas, pisahkan zona, dan pastikan bunding tersedia.'}]},
    {'slug': 'hybrid-pompa-sentrifugal', 'title': 'Pompa Sentrifugal: Tidak Menghisap, Melainkan Melempar', 'hook': 'Pompa sentrifugal tidak menghisap. Alat ini melempar cairan ke luar.', 'date': '2026-10-20', 'ig': 'https://www.instagram.com/reel/DetKKk4jMy6/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/pump-final/renders/pump-ep2.mp4', 'poster_src': None, 'duration': 40.5, 'tag': 'Peralatan Proses', 'intro': 'Video ini membuka dengan impeller yang berputar dalam tampilan tiga dimensi dan melempar cairan ke luar sejak detik pertama. Urutan berikutnya menjelaskan peran tekanan atmosfer pada sisi masuk, perubahan kecepatan menjadi tekanan di volute, dan hukum afinitas yang mengatur hubungan putaran dengan laju alir, head, dan daya.', 'tension': 'Apabila pompa sentrifugal tidak menghisap, apa yang mendorong air sampai dapat naik ke tangki atas?', 'takeaway': 'Yang bekerja pada pompa sentrifugal bukan hisapan, melainkan lemparan impeller. Lemparan tersebut menghasilkan kecepatan, volute mengubah kecepatan menjadi tekanan, dan tekanan inilah yang menggerakkan cairan menuju discharge.', 'facts': ['Cairan masuk secara axial melalui suction di tengah impeller dan keluar secara radial melalui discharge. Impeller yang berputar melempar cairan ke luar.', 'Di dalam volute yang salurannya melebar, kecepatan aliran turun dan tekanan naik, sehingga kecepatan yang diberikan impeller berubah menjadi tekanan pada sisi discharge.', 'Contoh hukum afinitas dengan basis 1.450 rpm, Q 100 m3/jam, H 30 m, dan P 15 kW: pada putaran 2.900 rpm diperoleh Q 200 m3/jam, H 120 m, dan P 120 kW, sehingga daya naik delapan kali untuk putaran dua kali.'], 'quiz': {'answer': 2, 'explain': 'Hukum afinitas menyatakan daya sebanding dengan putaran pangkat tiga. Putaran yang naik dua kali menghasilkan daya dua pangkat tiga, yaitu delapan kali, sebagaimana ditunjukkan contoh dari 15 kW menjadi 120 kW.', 'options': ['Dua kali', 'Empat kali', 'Delapan kali'], 'q': 'Menurut hukum afinitas, apabila putaran pompa sentrifugal dinaikkan menjadi dua kali, berapa kali daya yang dibutuhkan?'}, 'scenes': [{'end': 6.5, 'on_screen': 'POMPA SENTRIFUGAL / TIDAK MENGHISAP, DIA MELEMPAR', 'purpose': 'Membuka dengan klaim mekanisme utama melalui gerak impeller tiga dimensi sejak detik pertama.', 'role': 'HOOK', 'start': 0, 'title': 'Impeller berputar dan melempar cairan', 'visual': 'Tampilan tiga dimensi impeller yang berputar, dengan partikel biru masuk dari tengah impeller lalu terlempar ke luar menuju discharge.', 'watch': 'Ikuti gerak partikel dari tengah menuju arah luar, karena arah lemparan tersebut adalah klaim utama yang dijelaskan pada seluruh bagian berikutnya.'}, {'end': 13, 'on_screen': 'LALU KENAPA AIR BISA NAIK? / KE TANGKI ATAS. Kalau tidak menghisap, apa yang mendorong?', 'purpose': 'Menahan penjelasan dengan pertanyaan mengenai kemampuan pompa menaikkan air tanpa hisapan.', 'role': 'TENSION', 'start': 6.5, 'title': 'Pertanyaan mengenai kenaikan air ke tangki atas', 'visual': 'Panel dua dimensi berisi tangki bawah, pompa, dan tangki atas yang dihubungkan pipa, disertai kotak bertanda tanya.', 'watch': 'Baca rangkaian tangki bawah, pompa, dan tangki atas sebagai satu jalur aliran, kemudian perhatikan pertanyaan yang menahan penjelasannya.'}, {'end': 20, 'on_screen': 'Masuk axial. Impeller. Keluar radial. Cairan masuk dari tengah, impeller melemparnya ke luar.', 'purpose': 'Menunjukkan arah masuk dan keluar aliran serta posisi impeller melalui potongan tiga dimensi.', 'role': 'MEKANISME', 'start': 13, 'title': 'Masuk dari tengah dan keluar secara radial', 'visual': 'Tampilan tiga dimensi yang sama dengan gerak kamera lebih lambat, dilengkapi label masuk axial, impeller, dan keluar radial.', 'watch': 'Bedakan kedua label arah berdasarkan posisinya: masuk axial berada di tengah impeller dan keluar radial berada pada sisi kelilingnya.'}, {'end': 27, 'on_screen': 'KECEPATAN JADI TEKANAN. Saluran volute melebar, kecepatan turun, tekanan naik.', 'purpose': 'Menjelaskan perubahan energi kinetik menjadi tekanan di dalam volute.', 'role': 'MEKANISME', 'start': 20, 'title': 'Kecepatan berubah menjadi tekanan di volute', 'visual': 'Diagram volute berbentuk spiral yang melebar secara bertahap, disertai panah aliran yang mengikuti pelebaran saluran.', 'watch': 'Ikuti pelebaran penampang spiral dari bagian sempit menuju discharge dan kaitkan pelebaran tersebut dengan penurunan kecepatan serta kenaikan tekanan.'}, {'end': 34, 'on_screen': 'PUTAR 2X LEBIH CEPAT / DAYA NAIK 8X. Q 100 menjadi 200 m3/jam, H 30 menjadi 120 m, P 15 menjadi 120 kW. Contoh affinity law, basis 1.450 rpm.', 'purpose': 'Memberi contoh terhitung hukum afinitas sebagai hasil kuantitatif utama.', 'role': 'PAYOFF', 'start': 27, 'title': 'Contoh hukum afinitas pada putaran dua kali', 'visual': 'Tiga baris perbandingan berisi Q, H, dan P pada keadaan basis dan pada putaran dua kali, disertai catatan contoh hukum afinitas dengan basis 1.450 rpm.', 'watch': 'Bandingkan ketiga baris secara vertikal untuk melihat bahwa kenaikan daya jauh melampaui kenaikan laju alir pada kenaikan putaran yang sama.'}, {'end': 40.5, 'on_screen': 'YANG BEKERJA BUKAN HISAPAN, TAPI LEMPARAN. LIHAT KALKULATOR TEKNIK KIMIA di website @ilmutekkim, link di bio.', 'purpose': 'Menutup dengan kesimpulan mekanisme dan ajakan membuka kalkulator teknik kimia di website.', 'role': 'TAKEAWAY', 'start': 34, 'title': 'Yang bekerja adalah lemparan, bukan hisapan', 'visual': 'Kartu kesimpulan satu kalimat dan ajakan membuka kalkulator teknik kimia pada website ilmutekkim.', 'watch': 'Kalimat penutup mengembalikan pembaca pada gerak impeller di bagian awal, sehingga klaim pembuka dan kesimpulan membentuk satu rangkaian yang sama.'}]},
    {'slug': 'hybrid-shell-and-tube-heat-exchanger', 'title': 'Shell-and-Tube Heat Exchanger: Dua Fluida Bertukar Panas Tanpa Bertemu', 'hook': 'Dua fluida bertukar panas, tidak pernah bertemu.', 'date': '2026-10-20', 'ig': 'https://www.instagram.com/reel/DetExfJDDvK/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/hx3d-final/renders/hx3d-ep1-v4.mp4', 'poster_src': None, 'duration': 40.5, 'tag': 'Penukar Panas', 'intro': 'Video ini memperlihatkan penukar panas shell and tube dalam potongan tiga dimensi: fluida panas mengalir di dalam pipa, fluida dingin mengalir mengelilinginya di dalam shell, dan panas berpindah melalui dinding pipa tanpa kedua fluida pernah bercampur.', 'tension': 'Apabila kedua fluida tidak pernah bersentuhan, melalui apa panasnya berpindah dari satu aliran ke aliran lainnya?', 'takeaway': 'Yang berpindah adalah panasnya, bukan fluidanya. Penukar panas memindahkan energi melalui dinding pipa, sehingga dua fluida tidak perlu bercampur.', 'facts': ['Fluida panas mengalir di dalam pipa pada sisi tube dan fluida dingin mengalir di dalam shell mengelilingi pipa. Panas berpindah melalui dinding pipa dan kedua fluida tidak bercampur.', 'Sekat atau baffle di dalam shell memaksa aliran sisi shell berbelok zigzag, memperpanjang jalur aliran dan menaikkan turbulensi.', 'Contoh hitungan dengan kalor jenis 2,0 kJ/kg °C: aliran panas 10 kg/detik turun dari 180 °C menjadi 120 °C dan aliran dingin 12 kg/detik naik dari 40 °C menjadi 90 °C, keduanya setara 1.200 kW dengan LMTD sekitar 85 °C pada susunan arus berlawanan.'], 'quiz': {'answer': 0, 'explain': 'Kedua fluida dipisahkan oleh dinding pipa pada seluruh lintasan di dalam alat. Energi berpindah melintasi dinding tersebut dari fluida panas ke fluida dingin, sedangkan fluida masing masing tetap berada pada sisinya.', 'options': ['Melalui dinding pipa, dari fluida panas menuju fluida dingin', 'Melalui pencampuran langsung kedua fluida di dalam shell', 'Melalui sekat yang menyerap panas dari kedua fluida'], 'q': 'Apabila kedua fluida tidak pernah bertemu, melalui apa panas berpindah di dalam penukar panas shell and tube?'}, 'scenes': [{'end': 6.5, 'on_screen': 'DUA FLUIDA TUKARAN PANAS / TIDAK PERNAH BERTEMU. Yang satu panas, yang satu dingin. Di alat ini mereka bertukar energi tanpa pernah bersentuhan.', 'purpose': 'Mengunci perhatian dengan paradoks pertukaran panas tanpa pertemuan kedua fluida.', 'role': 'HOOK', 'start': 0, 'title': 'Dua fluida bertukar panas tanpa bertemu', 'visual': 'Dua bar aliran, oranye berlabel panas dan biru berlabel dingin, saling mendekat lalu berhenti di dinding tengah berwarna gelap.', 'watch': 'Perhatikan dinding di antara kedua bar aliran, karena dinding tersebut adalah jawaban yang akan dijelaskan pada bagian mekanisme.'}, {'end': 13, 'on_screen': 'MINYAK MENTAH DIPANASKAN / PAKAI PANAS SISA. Sebelum masuk kolom distilasi, minyak mentah harus panas. Pabrik memakai panas produk yang juga panas. Tapi panasnya pindah lewat apa?', 'purpose': 'Memberi konteks pemanfaatan panas sisa sebelum mekanisme alat dijelaskan.', 'role': 'TENSION', 'start': 6.5, 'title': 'Minyak mentah dipanaskan dengan panas sisa', 'visual': 'Strip alur kilang sederhana berisi kolom distilasi mini, aliran produk panas berwarna oranye, kotak penukar panas bertanda tanya, dan aliran minyak mentah berwarna biru.', 'watch': 'Baca strip alur dari kolom menuju penukar panas untuk memahami posisi alat ini sebelum kolom distilasi, kemudian perhatikan pertanyaan penutup bagiannya.'}, {'end': 20, 'on_screen': 'Fluida panas, di dalam pipa. Fluida dingin, di dalam shell. Fluida panas mengalir di dalam pipa. Fluida dingin mengalir mengelilinginya.', 'purpose': 'Memperlihatkan susunan dua aliran yang saling mengelilingi tanpa bercampur melalui potongan tiga dimensi.', 'role': 'MEKANISME', 'start': 13, 'title': 'Susunan aliran di dalam pipa dan di dalam shell', 'visual': 'Model potongan shell and tube dengan shell transparan, berkas pipa, dan sekat. Aliran oranye bergerak di dalam pipa dan aliran biru bergerak di dalam shell mengelilingi pipa.', 'watch': 'Bedakan kedua warna berdasarkan posisinya terhadap dinding pipa: oranye berada di dalam pipa dan biru berada di sekeliling pipa di dalam shell.'}, {'end': 27, 'on_screen': 'Sekat (baffle). Panas menyeberang lewat dinding pipa. Sekat memaksa fluida dingin berbelok-belok: jalur lebih panjang, kontak lebih lama.', 'purpose': 'Menjelaskan fungsi sekat dan menunjukkan titik tempat panas melintasi dinding pipa.', 'role': 'MEKANISME', 'start': 20, 'title': 'Sekat dan lintasan panas melalui dinding pipa', 'visual': 'Potongan tiga dimensi yang sama dengan label sekat, aliran sisi shell yang berbelok zigzag di antara sekat, dan cahaya berdenyut pada dinding pipa pada saat label perpindahan panas tampil.', 'watch': 'Ikuti lintasan zigzag aliran sisi shell dan kaitkan belokan tersebut dengan label dinding pipa tempat panas menyeberang.'}, {'end': 34, 'on_screen': 'PANASNYA PINDAH / 1.200 kW. Minyak 10 kg/detik kehilangan 60 °C, minyak 12 kg/detik naik 50 °C. Energinya persis sama. LMTD sekitar 85 °C. Contoh hitungan, kalor jenis 2,0 kJ/kg °C.', 'purpose': 'Memberi contoh hitungan yang keseimbangan energinya konsisten dan terverifikasi.', 'role': 'PAYOFF', 'start': 27, 'title': 'Contoh hitungan sebesar 1.200 kW dan LMTD sekitar 85 °C', 'visual': 'Grafik profil suhu sepanjang alat dengan garis oranye turun dari 180 °C menjadi 120 °C dan garis biru naik dari 40 °C menjadi 90 °C, disertai chip angka daya dan LMTD yang seukuran.', 'watch': 'Bandingkan arah kedua garis suhu pada grafik, kemudian baca kedua chip angka sebagai pasangan hasil dari contoh hitungan yang sama.'}, {'end': 40.5, 'on_screen': 'YANG PINDAH PANASNYA, BUKAN FLUIDANYA. Heat exchanger memindahkan energi lewat dinding pipa, jadi dua fluida tidak perlu bercampur. HITUNG LMTD SENDIRI. Kalkulatornya di website @ilmutekkim, link di bio.', 'purpose': 'Menutup dengan kesimpulan mekanisme dan ajakan menghitung LMTD pada kalkulator website.', 'role': 'TAKEAWAY_CTV', 'start': 34, 'title': 'Yang berpindah adalah panas, bukan fluida', 'visual': 'Kartu kesimpulan satu kalimat dan tombol ajakan menghitung LMTD sendiri pada kalkulator website ilmutekkim.', 'watch': 'Kalimat penutup memisahkan secara tegas perpindahan energi dari perpindahan fluida, dan ajakan di bawahnya menunjuk perhitungan yang baru saja dikerjakan.'}]},
    {'slug': 'loto-gembok-pribadi-motion', 'title': 'LOTO: Mesin yang Dimatikan Belum Tentu Aman', 'hook': 'Mesin sudah dimatikan, tetapi belum aman.', 'date': '2026-10-20', 'ig': 'https://www.instagram.com/reel/DeuDeQsk1T6/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-20/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-20/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Keselamatan Proses', 'intro': 'Mematikan mesin dari panel hanya menghentikan perintah operasi. Video ini menguraikan energi tersimpan yang tetap berada di dalam mesin, risiko penyalaan kembali oleh orang lain, dan urutan lengkap lockout dan tagout menurut standar OSHA hingga verifikasi bahwa mesin benar-benar diam.', 'tension': 'Mesin yang dimatikan dari panel terlihat aman, padahal energi tersimpan di dalamnya dan kemungkinan dinyalakan kembali oleh orang lain tetap dapat mencelakai teknisi yang sedang melakukan perawatan.', 'takeaway': 'Gembok pribadi pada titik isolasi adalah tanda bahwa ada pekerja yang sedang bekerja di dalam mesin. Hanya pemilik gembok yang memegang kuncinya dan hanya pemiliknya yang boleh melepaskannya.', 'facts': ['LOTO diatur dalam standar OSHA 29 CFR 1910.147 tentang pengendalian energi berbahaya dan berlaku efektif sejak 1990.', 'OSHA memperkirakan kepatuhan pada prosedur LOTO mencegah sekitar 120 kematian dan 50.000 cedera setiap tahun di Amerika Serikat.', 'Energi berbahaya yang wajib dikendalikan mencakup energi listrik, mekanik, hidrolik, pneumatik, kimia, dan termal.'], 'quiz': {'answer': 0, 'explain': 'Gembok pribadi memastikan titik isolasi tidak dapat dibuka oleh siapa pun selain pekerja yang keselamatannya bergantung pada keadaan mesin tersebut. Kunci hanya dipegang pemiliknya, dan kunci hanya boleh dilepas oleh pekerja yang memasangnya.', 'options': ['Karena gembok itu merupakan tanda bahwa ada pekerja yang sedang berada di dalam area mesin dan hanya pemiliknya yang memegang kunci pelepasan', 'Karena gembok pribadi memiliki kekuatan mekanik yang lebih besar dari gembok bersama', 'Karena tag peringatan tidak dapat dibaca tanpa gembok pribadi'], 'q': 'Mengapa gembok pada prosedur LOTO harus bersifat pribadi dan hanya dilepas oleh pekerja yang memasangnya?'}, 'scenes': [{'end': 6, 'on_screen': 'MESIN SUDAH DIMATIKAN / TAPI BELUM AMAN', 'purpose': 'Hook: keyakinan umum bahwa mesin mati sama dengan mesin aman dibantah sejak detik pertama.', 'role': 'HOOK', 'start': 0, 'title': 'Mesin dimatikan, keadaan aman belum tercapai', 'visual': 'Panel listrik digambar programatik, saklar utama berputar ke posisi OFF dan lampu indikator padam. Seorang teknisi mendekat membawa kunci pas, lalu percikan kecil menyambar dari dalam panel yang terbuka. Headline dua baris muncul kinetik.', 'watch': 'Perhatikan percikan yang tetap muncul setelah saklar berada pada posisi mati, karena peristiwa tersebut adalah bukti visual pertama bahwa energi belum hilang.'}, {'end': 13, 'on_screen': 'Energi tersimpan: listrik, tekanan, pegas, gravitasi', 'purpose': 'Tension: penonton melihat empat sumber energi yang tidak hilang saat saklar dimatikan.', 'role': 'TENSION', 'start': 6, 'title': 'Energi tersimpan yang tetap aktif', 'visual': 'Kamera menyorot satu per satu: kapasitor dengan ikon muatan listrik, tabung hidrolik dengan jarum tekanan masih tinggi, pegas tertekan bergetar menahan beban, dan beban menggantung di rantai di atas area kerja. Tiap sumber berdenyut merah sebagai tanda masih aktif.', 'watch': 'Ikuti empat sumber yang disorot secara berurutan dan baca denyut merahnya sebagai penanda bahwa setiap sumber masih menyimpan energi.'}, {'end': 20, 'on_screen': 'Orang lain bisa menyalakan lagi tanpa tahu ada yang servis', 'purpose': 'Tension: tanpa kunci dan tag, bahaya kedua datang dari orang lain yang tidak tahu ada teknisi di dalam mesin.', 'role': 'TENSION', 'start': 13, 'title': 'Risiko penyalaan kembali oleh orang lain', 'visual': 'Tangan pekerja kedua masuk dari sisi lain dan hampir memutar saklar kembali ke ON, sementara teknisi pertama masih berada di dalam area mesin. Tanda silang merah besar membatalkan gerakan itu, layar berhenti tepat sebelum saklar bergerak.', 'watch': 'Perhatikan posisi dua pekerja yang saling tidak terlihat pada bagian ini, karena ketidaktahuan tersebut adalah sumber bahaya keduanya.'}, {'end': 27, 'on_screen': 'Isolasi, lalu kunci dengan gembok pribadi dan tag', 'purpose': 'Payoff: tiga langkah pertama LOTO ditunjukkan sebagai gerakan berurutan yang bisa diikuti penonton.', 'role': 'PAYOFF', 'start': 20, 'title': 'Isolasi, gembok pribadi, dan tag peringatan', 'visual': 'Katup dan saklar isolasi ditutup penuh, hasp baja terpasang di titik isolasi, gembok pribadi berwarna terang mengunci dengan bunyi klik, dan tag peringatan terikat di sebelahnya bertuliskan nama pemilik gembok.', 'watch': 'Baca urutan gerakannya dari penutupan titik isolasi sampai tag terikat, karena setiap elemen menutup celah yang ditinggalkan elemen sebelumnya.'}, {'end': 34, 'on_screen': 'Buang sisa energi, lalu uji: mesin harus tetap diam', 'purpose': 'Payoff: sisa energi dibuang sampai nol dan verifikasi isolasi dibuktikan dengan percobaan menyalakan yang gagal total.', 'role': 'PAYOFF', 'start': 27, 'title': 'Pelepasan sisa energi dan verifikasi keadaan nol', 'visual': 'Jarum pengukur tekanan dan muatan turun perlahan sampai nol, pegas dilepas tegangannya. Teknisi menekan tombol start untuk verifikasi dan tidak ada satu pun bagian mesin yang bergerak. Kunci gembok tetap di saku pemiliknya.', 'watch': 'Ikuti jarum pengukur sampai mencapai nol, kemudian perhatikan ketiadaan gerak mesin pada saat tombol start ditekan sebagai hasil verifikasinya.'}, {'end': 40.9, 'on_screen': 'Gembok itu tanda: ada nyawa di dalam mesin. Follow @ilmutekkim', 'purpose': 'Takeaway menutup dengan makna gembok pribadi, CTV mengajak follow.', 'role': 'TAKEAWAY_CTV', 'start': 34, 'title': 'Gembok pribadi sebagai tanda keberadaan pekerja', 'visual': 'Gembok pribadi membesar menjadi ikon penutup di tengah frame gelap rapi, teks takeaway tampil di bawahnya, watermark dan progress bar penuh.', 'watch': 'Gembok yang membesar pada penutup merangkum seluruh urutan, sehingga maknanya sebagai penanda keberadaan pekerja menjadi kalimat terakhir yang dibaca.'}]},
    {'slug': 'pks-tbs-menjadi-cpo-motion', 'title': 'Dari Tandan Buah Segar Menjadi CPO: Alur Pabrik Kelapa Sawit', 'hook': 'Tandan berduri menjadi minyak goreng melalui rantai unit yang tidak dapat dilompati.', 'date': '2026-10-16', 'ig': 'https://www.instagram.com/reel/Dejv1_pE_Jq/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-16/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-16/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Pabrik Kelapa Sawit', 'intro': 'Tandan buah segar kelapa sawit diolah menjadi CPO melalui sterilizer, thresher, digester, screw press, dan clarifier. Video ini membedah fungsi setiap unit dan alasan urutan tersebut tidak dapat dilompati.', 'tension': 'Minyak pada tandan buah segar terkunci di dalam daging buah. Minyak tersebut tidak keluar dengan sendirinya dan tidak dapat diambil hanya dengan memeras tandan secara langsung.', 'takeaway': 'Setiap unit di pabrik kelapa sawit mempunyai satu fungsi yang tidak dapat dilompati: sterilisasi, perontokan, pelumat, pemerasan, dan klarifikasi bekerja berurutan sampai CPO diperoleh.', 'facts': ['Sterilisasi tandan buah segar memakai uap pada suhu 130-140°C, tekanan 1,5-2,8 bar, waktu sekitar 90 menit, dengan siklus 3 puncak tekanan.', 'Uap sterilisasi mematikan enzim lipase dan melunakkan buah agar brondolan mudah lepas dari tandan.', 'Daging buah dilumatkan lalu diperas dengan screw press, dan minyak kasar dimurnikan dari air dan padatan di clarifier sehingga diperoleh CPO.'], 'quiz': {'answer': 1, 'explain': 'Sterilisasi dengan uap bertekanan mematikan enzim lipase dan melunakkan buah. Tanpa tahap ini, brondolan sukar lepas dari tandan dan mutu minyak menurun, sehingga tahap berikutnya tidak bekerja dengan baik.', 'options': ['Memisahkan minyak dari air dan padatan', 'Mematikan enzim lipase dan melunakkan buah agar brondolan mudah lepas', 'Memeras daging buah sampai minyak kasar keluar'], 'q': 'Apa fungsi utama sterilisasi tandan buah segar dengan uap bertekanan?'}, 'scenes': [{'end': 5, 'on_screen': 'TANDAN BERDURI / JADI MINYAK GORENG', 'purpose': 'Menancapkan kontras bahan mentah berduri dan produk akhirnya.', 'role': 'HOOK', 'start': 0, 'title': 'Tandan buah segar dan produk akhirnya', 'visual': 'Tandan buah segar besar berputar di tengah; panah ke botol minyak goreng di kanan.', 'watch': 'Perhatikan kontras antara tandan berduri dan botol minyak sebagai jarak proses yang akan dijelaskan.'}, {'end': 11, 'on_screen': 'MINYAKNYA TERKUNCI / DI DALAM DAGING BUAH', 'purpose': 'Membangun masalah: minyak ada tapi tidak bisa diambil langsung.', 'role': 'TENSION', 'start': 5, 'title': 'Minyak terkunci di daging buah', 'visual': 'Zoom ke penampang buah; tetes minyak terjebak di serat daging buah.', 'watch': 'Amati tetes minyak yang terjebak di serat daging buah pada penampang yang diperbesar.'}, {'end': 17, 'on_screen': 'JAWABANNYA: RANTAI UNIT / YANG TIDAK BISA DILOMPATI', 'purpose': 'Menjanjikan solusi berupa urutan unit yang berurutan.', 'role': 'TENSION', 'start': 11, 'title': 'Rantai lima unit yang berurutan', 'visual': 'Unit sterilizer, thresher, digester, press, clarifier muncul berurutan sebagai rantai.', 'watch': 'Baca urutan lima unit yang muncul berurutan sebagai peta keseluruhan proses pabrik.'}, {'end': 27, 'on_screen': 'STERILIZER: UAP MEMBUKA KUNCI / THRESHER: BRONDOLAN LEPAS', 'purpose': 'Menunjukkan dua tahap pertama yang membebaskan buah dari tandan.', 'role': 'PAYOFF', 'start': 17, 'title': 'Sterilizer melunakkan, thresher melepas brondolan', 'visual': 'Uap masuk sterilizer, buah melunak; tandan diguncang di thresher, brondolan jatuh lepas.', 'watch': 'Ikuti perubahan dari tandan utuh menjadi brondolan lepas setelah uap dan guncangan bekerja berurutan.'}, {'end': 36, 'on_screen': 'PRESS: MINYAK KASAR KELUAR / CLARIFIER: CPO NAIK KE ATAS', 'purpose': 'Menunjukkan pemerasan dan pemisahan sampai CPO jernih diperoleh.', 'role': 'PAYOFF', 'start': 27, 'title': 'Pemerasan dan klarifikasi menghasilkan CPO', 'visual': 'Digester mengaduk daging buah; screw press memeras, minyak kasar mengalir ke clarifier; CPO jernih naik ke atas tangki.', 'watch': 'Perhatikan minyak kasar dari pemerasan berubah menjadi lapisan CPO jernih yang naik ke atas tangki klarifikasi.'}, {'end': 41, 'on_screen': 'TIAP UNIT SATU FUNGSI / LOMPATI SATU, MINYAK HILANG', 'purpose': 'Menutup dengan takeaway dan CTA; tidak ada elemen baru, rantai unit dari scene sebelumnya tetap tampil.', 'role': 'TAKEAWAY', 'start': 36, 'title': 'Setiap unit satu fungsi', 'visual': 'Rantai unit penuh menyala berurutan; teks CTA tampil di bawah.', 'watch': 'Baca penyalaan berurutan rantai lima unit pada penutup sebagai penegasan urutan yang tidak dapat dilompati.'}]},
    {'slug': 'refinery-sawit-olein-stearin-motion', 'title': 'Refinery Sawit: Dari CPO Merah Menjadi Olein dan Stearin', 'hook': 'CPO merah pekat tidak dapat langsung dipakai menggoreng.', 'date': '2026-10-17', 'ig': 'https://www.instagram.com/reel/DemUgZjDhRL/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-17/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-17/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Refinery Sawit', 'intro': 'CPO berwarna merah pekat dan masih membawa getah, warna, dan bau. Video ini membedah tiga tahap pemurnian menjadi RBDPO dan tahap fraksionasi yang membaginya menjadi olein cair dan stearin padat.', 'tension': 'CPO berwarna merah pekat karena karoten dan masih membawa getah, warna, serta bau. Minyak dalam keadaan tersebut belum layak dipakai sebagai minyak goreng.', 'takeaway': 'Pemurnian mengubah CPO menjadi RBDPO yang bersih, dan fraksionasi membagi RBDPO menjadi olein cair untuk minyak goreng serta stearin padat untuk margarin dan shortening.', 'facts': ['CPO dimurnikan melalui degumming, bleaching, dan deodorisasi menjadi RBDPO (refined, bleached, deodorized palm oil).', 'Fraksionasi memisahkan RBDPO menjadi olein yang cair untuk minyak goreng dan stearin yang padat untuk margarin dan shortening melalui kristalisasi.', 'Standar spesifikasi yang dikutip menetapkan nilai iod olein minimal 56 dan stearin maksimal 48 g I2/100 g minyak.'], 'quiz': {'answer': 1, 'explain': 'RBDPO didinginkan secara perlahan sehingga sebagian mengkristal. Fraksi yang tetap cair adalah olein untuk minyak goreng, sedangkan kristal padat yang dipisahkan adalah stearin untuk margarin dan shortening.', 'options': ['Olein adalah fraksi padat dan stearin adalah fraksi cair', 'Olein adalah fraksi cair untuk minyak goreng dan stearin adalah fraksi padat untuk margarin', 'Olein dan stearin adalah dua nama untuk minyak yang sama'], 'q': 'Setelah fraksionasi RBDPO, fraksi mana yang menjadi minyak goreng?'}, 'scenes': [{'end': 7, 'on_screen': 'CPO MERAH PEKAT / TIDAK BISA LANGSUNG DIGORENG', 'purpose': 'Menohok penonton dengan fakta bahwa minyak sawit mentah tidak bisa langsung dipakai menggoreng.', 'role': 'HOOK', 'start': 0, 'title': 'Tangki CPO merah pekat', 'visual': 'Tangki berisi minyak merah pekat, headline dua baris muncul dengan teks kinetik.', 'watch': 'Perhatikan warna merah pekat minyak di dalam tangki sebagai titik awal persoalan pemurniannya.'}, {'end': 14, 'on_screen': 'Di dalamnya masih ada getah, warna, dan bau yang harus dibuang', 'purpose': 'Membangun tension: CPO mentah kotor dan perlu dibersihkan dulu.', 'role': 'TENSION', 'start': 7, 'title': 'Getah, warna, dan bau pada CPO', 'visual': 'Partikel pengotor disorot di dalam minyak merah, lalu ditandai satu per satu.', 'watch': 'Ikuti penandaan satu per satu atas getah, warna, dan bau sebagai daftar pengotor yang harus disingkirkan.'}, {'end': 21, 'on_screen': 'Tiga tahap pemurnian: degumming, bleaching, deodorisasi', 'purpose': 'Menunjukkan urutan pemurnian yang tidak bisa dilompati.', 'role': 'TENSION', 'start': 14, 'title': 'Tiga tahap pemurnian yang berurutan', 'visual': 'Tiga kotak unit berurutan, minyak mengalir dan warnanya berangsur jernih di tiap tahap.', 'watch': 'Amati perubahan warna minyak pada setiap kotak unit sebagai tanda kemajuan pemurniannya.'}, {'end': 28, 'on_screen': 'Hasilnya RBDPO: minyak sawit bersih siap fraksionasi', 'purpose': 'Payoff tahap satu: minyak sudah bersih, siap dipisah.', 'role': 'PAYOFF', 'start': 21, 'title': 'RBDPO jernih siap difraksionasi', 'visual': 'Aliran minyak kuning jernih keluar dari unit terakhir menuju tangki kristalisasi.', 'watch': 'Perhatikan aliran kuning jernih yang meninggalkan unit terakhir menuju tangki kristalisasi.'}, {'end': 35, 'on_screen': 'Didinginkan perlahan, kristal padat terbentuk lalu dipisah', 'purpose': 'Payoff tahap dua: mekanisme fraksionasi divisualkan.', 'role': 'PAYOFF', 'start': 28, 'title': 'Kristalisasi dan pemisahan dua fraksi', 'visual': 'Tangki didinginkan, kristal padat terbentuk, filter memisah dua aliran: cair dan padat.', 'watch': 'Ikuti pembentukan kristal padat dan pemisahannya oleh penyaring menjadi aliran cair dan aliran padat.'}, {'end': 41, 'on_screen': 'Cair = olein untuk minyak goreng. Padat = stearin untuk margarin. Simpan dan tag temanmu.', 'purpose': 'Takeaway dua produk plus ajakan simpan dan tag.', 'role': 'TAKEAWAY', 'start': 35, 'title': 'Olein cair dan stearin padat', 'visual': 'Dua kartu produk muncul: OLEIN (cair, minyak goreng) dan STEARIN (padat, margarin), lalu CTV.', 'watch': 'Bandingkan dua kartu produk pada penutup untuk mengunci pasangan fraksi dan kegunaannya.'}]},
    {'slug': 'satu-barel-minyak-motion', 'title': 'Satu Barel Minyak Mentah: Tidak Semua Menjadi Bensin', 'hook': 'Satu barel minyak mentah tidak disuling menjadi bensin semua.', 'date': '2026-10-19', 'ig': 'https://www.instagram.com/reel/DereQLzCclF/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-19/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-19/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Kilang dan Distilasi', 'intro': 'Satu barel minyak mentah sering dibayangkan berubah seluruhnya menjadi bensin. Video ini menunjukkan pembagian sebenarnya di kilang: setelah dipanaskan dan masuk menara distilasi, satu barel terpecah menjadi beberapa fraksi dengan proporsi yang ditentukan data kilang, bukan oleh perkiraan.', 'tension': 'Satu barel minyak mentah tidak disuling menjadi bensin semua, dan fraksi lain yang keluar dari menara memiliki volume yang sama pentingnya untuk dibaca.', 'takeaway': 'Minyak mentah tidak dipakai dalam keadaan mentah. Kilang memecahnya menurut titik didih menjadi beragam produk, dan total volume produk akhir dapat melebihi volume umpan karena processing gain.', 'facts': ['Satu barel minyak mentah setara 42 galon AS atau 159 liter.', 'Kilang di Amerika Serikat menghasilkan 19 sampai 20 galon bensin motor, 11 sampai 13 galon distilat termasuk diesel, dan 4 galon avtur dari satu barel 42 galon.', 'Fraksi unit distilasi mentah terpisah menurut titik didih dari atas ke bawah sebagai gas, nafta, kerosen, diesel, dan residu, dan total volume produk akhir melebihi 42 galon karena processing gain pada saat densitas produk turun.'], 'quiz': {'answer': 1, 'explain': 'Processing gain adalah kenaikan volume yang terjadi karena produk hasil pengolahan memiliki densitas lebih rendah dari minyak mentah umpannya. Massa tidak bertambah, yang berubah adalah volume yang ditempati oleh massa tersebut.', 'options': ['Karena volume barel bertambah selama penyimpanan', 'Karena processing gain terjadi saat densitas produk turun, sehingga volume akhir lebih besar dari volume umpan', 'Karena sebagian produk dihitung dua kali di kilang'], 'q': 'Mengapa total volume produk dari satu barel dapat melebihi 42 galon?'}, 'scenes': [{'end': 6.5, 'on_screen': '1 BAREL MINYAK MENTAH TIDAK JADI BENSIN SEMUA. 1 barel = 159 liter.', 'purpose': 'Patahkan miskonsepsi: satu barel tidak disuling jadi bensin semua.', 'role': 'HOOK', 'start': 0, 'title': 'Satu barel setara 159 liter', 'visual': 'Ikon barel minyak raksasa di tengah, label 159 liter muncul dengan pop.', 'watch': 'Perhatikan label volume pada barel di awal, karena seluruh pembagian produk berikutnya dibaca terhadap satuan volume yang sama.'}, {'end': 13, 'on_screen': 'Minyak mentah dipanaskan, masuk menara distilasi raksasa.', 'purpose': 'Tunjukkan minyak mentah harus dipecah dulu di menara distilasi.', 'role': 'TENSION', 'start': 6.5, 'title': 'Minyak mentah masuk menara distilasi', 'visual': 'Barel menuang ke kolom CDU; uap naik digambar sebagai aliran ke atas.', 'watch': 'Ikuti arah tuangan barel menuju kolom dan aliran uap yang naik, karena arah gerak tersebut menandai awal pemisahan fraksi.'}, {'end': 20, 'on_screen': 'Fraksi pisah sesuai titik didih: ringan di atas, berat di bawah.', 'purpose': 'Jelaskan prinsip pemisahan: titik didih menentukan posisi fraksi.', 'role': 'TENSION', 'start': 13, 'title': 'Pemisahan menurut titik didih', 'visual': 'Lima keran samping kolom menyala berurutan dari atas ke bawah: gas, nafta, kerosen, diesel, residu.', 'watch': 'Baca urutan lima keran dari atas ke bawah sebagai urutan ringan ke berat, bukan sebagai daftar produk yang berdiri sendiri.'}, {'end': 27.5, 'on_screen': 'Data EIA: 19-20 galon bensin, 11-13 galon diesel, 4 galon avtur per barel.', 'purpose': 'Beri angka nyata dari data publik EIA.', 'role': 'PAYOFF', 'start': 20, 'title': 'Angka produk menurut data EIA', 'visual': 'Tiga kartu angka muncul berurutan: bensin, diesel, avtur.', 'watch': 'Bandingkan ketiga kartu angka secara berurutan untuk melihat bahwa bensin merupakan bagian terbesar, tetapi bukan keseluruhan isi barel.'}, {'end': 34.5, 'on_screen': 'Sisanya: gas, aspal, bahan plastik. Total produk lebih dari 42 galon.', 'purpose': 'Lengkapi sisanya dan beri fakta processing gain.', 'role': 'PAYOFF', 'start': 27.5, 'title': 'Produk sisa dan processing gain', 'visual': 'Kartu sisa produk muncul; barel membesar sedikit dengan anotasi processing gain.', 'watch': 'Perhatikan pembesaran barel pada bagian ini sebagai gambaran visual kenaikan volume, bukan penambahan massa bahan.'}, {'end': 40.9, 'on_screen': 'Minyak mentah tidak dipakai mentah. Kilang memecahnya jadi puluhan produk. Follow @ilmutekkim.', 'purpose': 'Simpulkan dan ajak follow.', 'role': 'TAKEAWAY_CTV', 'start': 34.5, 'title': 'Kilang memecah minyak mentah menjadi beragam produk', 'visual': 'Lima kartu fraksi tersusun rapi; watermark dan progress bar penuh.', 'watch': 'Susunan lima kartu di penutup merangkum seluruh pemisahan, sehingga urutannya dapat dibaca kembali dalam satu pandangan.'}]},
    {'slug': 'sistem-kerja-tiga-shift', 'title': 'Sistem Kerja Tiga Shift: Mengapa Pabrik Beroperasi 24 Jam dan Harga yang Dibayar Operator', 'hook': 'Pabrik jalan 24 jam nonstop. Manusia tidak dirancang begitu.', 'date': '2026-10-11', 'ig': 'https://www.instagram.com/reel/DeW3vJ4DDgl/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-11/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-11/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Operasi Pabrik', 'intro': 'Pabrik proses kontinu dirancang beroperasi 24 jam, sedangkan manusia memerlukan tidur yang teratur. Video ini membedah alasan pabrik tidak dapat dimatikan setiap malam, pembagian tiga shift yang menutup 24 jam, dan harga rotasi tersebut pada pola tidur operator.', 'tension': 'Pabrik proses tidak dapat dimatikan seperti lampu, tetapi manusia tidak dirancang bekerja 24 jam, sehingga tiga shift merupakan kompromi yang harganya dibayar pada pola tidur operator.', 'takeaway': 'Tiga shift dengan durasi 8 jam per regu menutup 24 jam operasi tanpa jeda. Sistem ini menyelesaikan masalah keberlanjutan proses, dan memindahkan bebannya ke ritme sirkadian operator yang harus dikelola melalui tidur terjadwal dan serah terima yang ketat.', 'facts': ['Pabrik proses kontinu dirancang beroperasi 24 jam karena penyalaan dan penghentian operasi merupakan operasi yang berisiko, mahal, dan memberikan tegangan termal pada peralatan.', 'Pola umum pembagian kerja 24 jam adalah 3 shift dengan durasi masing-masing 8 jam, yaitu pagi, siang, dan malam.', 'Harga rotasi shift dibayar pada pola tidur operator: jam tidur bergeser pada setiap rotasi dan ritme sirkadian terganggu, sehingga adaptasinya menuntut tidur terjadwal dan serah terima antarshift yang ketat.'], 'quiz': {'q': 'Mengapa pabrik proses kontinu tidak dimatikan setiap malam seperti lampu?', 'options': ['Karena penyalaan dan penghentian operasi berisiko, mahal, dan memberikan tegangan termal pada peralatan', 'Karena operator lebih menyukai bekerja pada malam hari', 'Karena listrik lebih murah pada malam hari'], 'answer': 0, 'explain': 'Penghentian dan penyalaan kembali bukan tindakan ringan pada pabrik proses. Keduanya merupakan operasi yang berisiko dan mahal serta membebani peralatan dengan tegangan termal, sehingga pabrik dirancang beroperasi terus dan kebutuhan jaganya dibagi ke dalam tiga shift.'}, 'scenes': [{'start': 0, 'end': 6, 'role': 'HOOK', 'title': 'Pabrik beroperasi 24 jam, manusia memerlukan tidur', 'on_screen': 'Pabrik jalan 24 jam nonstop. Manusia tidak dirancang begitu', 'visual': 'Pabrik menyala di malam hari, jam dinding berputar cepat 24 jam, tiga blok shift muncul bergantian', 'purpose': 'Membuka kontras pabrik yang tidak pernah tidur dengan manusia yang butuh tidur', 'watch': 'Pabrik yang tetap menyala pada malam hari dan jam yang berputar penuh 24 jam menetapkan kontras yang akan dijawab oleh pembagian tiga shift.'}, {'start': 6, 'end': 13, 'role': 'TENSION', 'title': 'Mematikan reaktor tidak sama dengan mematikan lampu', 'on_screen': 'Matikan reaktor tidak seperti matikan lampu', 'visual': 'Reaktor besar dengan suhu dan tekanan stabil, lalu tombol mati ditekan dan grafik suhu jatuh bebas dengan peringatan', 'purpose': 'Menjelaskan kenapa pabrik proses tidak bisa dimatikan tiap malam', 'watch': 'Grafik suhu yang jatuh bebas setelah tombol mati ditekan menunjukkan penghentian bukan tindakan netral, melainkan gangguan besar pada keadaan operasi yang stabil.'}, {'start': 13, 'end': 20, 'role': 'TENSION', 'title': 'Pembagian 24 jam ke dalam tiga shift', 'on_screen': 'Solusinya: 3 shift, 8 jam tiap regu, 24 jam tertutup', 'visual': 'Timeline lingkaran 24 jam terbagi tiga segmen warna: pagi, siang, malam, tiap segmen berlabel 8 jam', 'purpose': 'Menunjukkan solusi 3 shift sebagai pembagi 24 jam yang rapi', 'watch': 'Lingkaran 24 jam yang terbagi menjadi tiga segmen berlabel 8 jam adalah keseluruhan sistemnya dalam satu gambar: pagi, siang, dan malam menutup hari tanpa jeda.'}, {'start': 20, 'end': 27, 'role': 'PAYOFF', 'title': 'Harga rotasi pada pola tidur operator', 'on_screen': 'Masalahnya: jam tidur ikut bergeser tiap rotasi', 'visual': 'Ikon tempat tidur bergeser mengikuti segmen shift yang berputar, ritme sirkadian digambar sebagai gelombang yang kacau', 'purpose': 'Menunjukkan harga rotasi shift pada pola tidur operator', 'watch': 'Ikon tempat tidur yang terus bergeser dan gelombang ritme sirkadian yang terganggu menggambarkan beban yang dipindahkan dari proses kepada operator.'}, {'start': 27, 'end': 34, 'role': 'PAYOFF', 'title': 'Cara operator beradaptasi terhadap rotasi', 'on_screen': 'Operator bertahan dengan tidur terjadwal dan serah terima ketat', 'visual': 'Checklist muncul satu per satu: tidur terjadwal, cahaya terang saat jaga, logbook serah terima antar shift', 'purpose': 'Memberi cara adaptasi nyata yang dipakai operator shift', 'watch': 'Daftar periksa adaptasinya terdiri atas tidur terjadwal, cahaya terang saat bertugas, dan catatan serah terima antarshift, tiga unsur yang tampil satu per satu.'}, {'start': 34, 'end': 40.9, 'role': 'TAKEAWAY', 'title': 'Tiga segmen yang menutup satu hari penuh', 'on_screen': 'Simpan buat bekal masuk pabrik. Follow @ilmutekkim', 'visual': 'Tiga segmen shift menyatu menjadi lingkaran utuh, watermark dan progress bar menutup video', 'purpose': 'Menutup dengan ajakan simpan dan follow yang konkret', 'watch': 'Tiga segmen yang menyatu kembali menjadi lingkaran utuh menegaskan bahwa tidak ada satu jam pun dalam sehari yang tidak terjaga di pabrik proses.'}]},
    {'slug': 'tangki-putih-floating-roof', 'title': 'Tangki Putih dan Atap Terapung: Mengendalikan Rugi Penguapan Tangki Minyak', 'hook': 'Tangki minyak dicat putih, bukan agar terlihat bersih.', 'date': '2026-10-14', 'ig': 'https://www.instagram.com/reel/DeenaYwjNPS/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-14/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-14/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Tangki Penyimpanan', 'intro': 'Tangki penyimpanan bensin dan minyak di area tangki dicat putih dan sebagian dilengkapi atap terapung. Video ini membedah alasan rekayasa di balik kedua keputusan desain tersebut, dari radiasi matahari sampai ruang uap di atas permukaan cairan.', 'tension': 'Pada siang hari, dinding tangki yang gelap menyerap panas matahari dan memanaskan isi tangki. Uap cairan yang mudah menguap terbentuk, keluar melalui ventilasi, dan produk yang tersimpan berkurang ke udara.', 'takeaway': 'Warna putih memantulkan panas matahari sehingga suhu dinding lebih rendah, sedangkan atap terapung meniadakan ruang uap sehingga rugi penguapan dapat ditekan secara nyata.', 'facts': ['Tangki atap terapung dipakai untuk menyimpan cairan yang mudah menguap seperti bensin agar rugi penguapan kecil.', 'Permukaan terang memantulkan radiasi matahari sehingga suhu dinding tangki lebih rendah dibandingkan permukaan gelap.', 'Pemasangan atap terapung dan seal mengendalikan emisi penguapan tangki atap tetap dengan efisiensi 60 sampai 99 persen, tergantung pada jenis atap, jenis seal, dan jenis cairan yang disimpan.'], 'quiz': {'answer': 1, 'explain': 'Atap terapung bergerak mengikuti permukaan cairan. Dengan ruang uap yang hampir nol, tempat pembentukan uap hampir tidak tersedia, dan pengendalian emisi penguapannya mencapai 60 sampai 99 persen menurut EPA AP-42.', 'options': ['Karena atap terapung mendinginkan cairan melalui ventilasi terbuka', 'Karena atap terapung naik dan turun mengikuti permukaan cairan sehingga ruang uap hampir nol dan uap tidak memiliki ruang untuk terbentuk', 'Karena atap terapung membuat warna tangki menjadi putih'], 'q': 'Mengapa atap terapung menekan rugi penguapan pada tangki bensin?'}, 'scenes': [{'end': 6, 'on_screen': 'TANGKI MINYAK DICAT PUTIH / BUKAN BIAR KELIHATAN BERSIH', 'purpose': 'Menanam pertanyaan kenapa warna putih.', 'role': 'HOOK', 'start': 0, 'title': 'Tangki putih di bawah matahari terik', 'visual': 'Tangki silinder putih di bawah matahari terik, kamera zoom in perlahan.', 'watch': 'Perhatikan tangki silinder putih dan matahari terik pada bingkai pembuka sebagai titik awal pertanyaan desainnya.'}, {'end': 13, 'on_screen': 'SIANG HARI, TANGKI GELAP JADI OVEN', 'purpose': 'Menunjukkan panas matahari sebagai musuh.', 'role': 'TENSION', 'start': 6, 'title': 'Tangki gelap menyerap panas matahari', 'visual': 'Tangki gelap di samping tangki putih; termometer di tangki gelap naik, garis panas bergetar.', 'watch': 'Bandingkan termometer pada tangki gelap dan tangki putih untuk membaca perbedaan penyerapan panasnya.'}, {'end': 20, 'on_screen': 'UAP BENSIN MENGUAP = UANG HILANG', 'purpose': 'Mengubah fisika jadi kerugian konkret.', 'role': 'TENSION', 'start': 13, 'title': 'Ruang uap dan produk yang hilang ke udara', 'visual': 'Potongan tangki: ruang uap di atas cairan membesar, partikel uap keluar lewat ventilasi atap.', 'watch': 'Amati ruang di atas permukaan cairan dan partikel uap yang keluar melalui ventilasi sebagai wujud rugi produknya.'}, {'end': 27, 'on_screen': 'CAT PUTIH MEMANTULKAN PANAS', 'purpose': 'Solusi pertama: pantulkan panasnya.', 'role': 'PAYOFF', 'start': 20, 'title': 'Cat putih memantulkan panas', 'visual': 'Sinar matahari memantul dari dinding tangki putih; termometer turun; tidak ada elemen baru selain kelanjutan pantulan.', 'watch': 'Ikuti arah sinar yang memantul dari dinding putih dan penurunan termometer sebagai bukti visual solusinya.'}, {'end': 35, 'on_screen': 'ATAP TERAPUNG, RUANG UAP HAMPIR NOL. RUGI PENGUAPAN TURUN 60-99%', 'purpose': 'Solusi kedua: hapus ruang tempat uap terbentuk.', 'role': 'PAYOFF', 'start': 27, 'title': 'Atap terapung meniadakan ruang uap', 'visual': 'Penampang tangki: atap terapung turun mengikuti permukaan cairan, ruang uap menyusut sampai tipis.', 'watch': 'Perhatikan atap yang turun mengikuti permukaan cairan sampai ruang uap menyusut menjadi lapisan yang sangat tipis.'}, {'end': 41, 'on_screen': 'PUTIH + ATAP TERAPUNG = PRODUK AMAN', 'purpose': 'Merangkum dan mengajak simpan.', 'role': 'TAKEAWAY', 'start': 35, 'title': 'Dua pertahanan terhadap rugi penguapan', 'visual': 'Tangki utuh dengan progress bar penuh dan watermark; tidak ada elemen baru, penutup ajakan simpan.', 'watch': 'Baca tiga kartu ringkas pada penutup sebagai rangkuman dua pertahanan dan hasil akhirnya bagi produk.'}]},
    {'slug': 'turnaround-pabrik-berhenti-total', 'title': 'Turnaround: Mengapa Pabrik Sengaja Berhenti Total Berminggu-minggu', 'hook': 'Pabrik berhenti total berminggu-minggu tiap beberapa tahun. Itu turnaround, bukan pabrik bangkrut.', 'date': '2026-10-09', 'ig': 'https://www.instagram.com/reel/DeSjnUSD25s/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-09/motion-1/motion-fixed-equal-heights.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-09/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Perawatan dan Keandalan Pabrik', 'intro': 'Setiap beberapa tahun, pabrik proses yang sehat justru direncanakan berhenti total selama berminggu-minggu. Video ini membedah pekerjaan apa saja yang hanya dapat dilakukan pada jendela berhenti tersebut dan mengapa menundanya jauh lebih berbahaya.', 'tension': 'Berhenti produksi berminggu-minggu tampak merugikan, padahal menunda jendela ini berarti memaksa peralatan yang aus bekerja terus sampai gagal secara mendadak.', 'takeaway': 'Turnaround adalah penghentian terencana yang menentukan keandalan pabrik bertahun-tahun ke depan: peralatan dibuka, diperiksa, dibersihkan, dan diuji sebelum unit dinyalakan kembali secara bertahap.', 'facts': ['Turnaround adalah penghentian terencana seluruh unit proses selama beberapa minggu untuk membuka, memeriksa, membersihkan, dan memperbaiki peralatan statis dan berputar yang tidak dapat dikerjakan saat operasi.', 'Pekerjaan inti pada jendela ini mencakup pembukaan kolom, penggantian katalis, dan pembersihan penukar panas.', 'Ribuan pekerjaan perawatan dikerjakan sekaligus dalam satu jendela berhenti yang direncanakan bertahun-tahun sebelumnya.'], 'quiz': {'q': 'Mengapa pekerjaan turnaround tidak dapat dicicil saat pabrik tetap beroperasi?', 'options': ['Karena jumlah pekerjanya tidak mencukupi', 'Karena peralatan seperti kolom dan katalis hanya dapat dibuka dan diganti saat unit berhenti total', 'Karena perawatan hanya boleh dilakukan pada akhir tahun'], 'answer': 1, 'explain': 'Kolom harus dibuka, katalis lama diangkat, dan penukar panas dibersihkan dari dalam. Seluruh pekerjaan itu mensyaratkan unit berhenti dan kosong, sehingga semuanya ditumpuk dalam satu jendela turnaround yang direncanakan.'}, 'scenes': [{'start': 0, 'end': 6, 'role': 'HOOK', 'title': 'Pabrik berhenti total, bukan bangkrut', 'on_screen': 'Pabrik berhenti total berminggu-minggu. Bukan bangkrut', 'visual': 'Kilang cerah perlahan meredup unit demi unit, gerbang utama ditutup, papan hitung mundur turnaround muncul', 'purpose': 'Membuka serangan kenapa pabrik yang sehat justru direncanakan berhenti total', 'watch': 'Perhatikan unit yang meredup satu per satu dan papan hitung mundurnya: penghentian ini terjadwal, bukan kejadian mendadak.'}, {'start': 6, 'end': 13, 'role': 'TENSION', 'title': 'Peralatan yang hanya dapat dibuka saat unit berhenti', 'on_screen': 'Ada alat yang cuma bisa dibuka saat pabrik mati total', 'visual': 'Kolom distilasi terbuka dari atas, katalis lama berwarna gelap diangkat keluar dengan derek kecil', 'purpose': 'Menunjukkan pekerjaan besar yang mustahil dikerjakan saat unit beroperasi', 'watch': 'Kolom yang terbuka dari atas dan katalis gelap yang diangkat keluar adalah bukti visual bahwa pekerjaan ini mensyaratkan unit berhenti.'}, {'start': 13, 'end': 20, 'role': 'TENSION', 'title': 'Ribuan pekerjaan menunggu satu jendela', 'on_screen': 'Ribuan pekerjaan menunggu satu jendela berhenti ini', 'visual': 'Daftar pekerjaan panjang bergulir cepat, bundel penukar panas dicabut dan disemprot bersih', 'purpose': 'Menahan jawaban dengan besarnya daftar kerja yang menumpuk untuk satu jendela', 'watch': 'Daftar pekerjaan yang bergulir panjang menunjukkan skala jendela ini, sedangkan bundel penukar panas yang disemprot menunjukkan salah satu pekerjaannya.'}, {'start': 20, 'end': 27, 'role': 'PAYOFF', 'title': 'Urutan kerja: buka, bersihkan, ganti, uji', 'on_screen': 'Buka, bersihkan, ganti yang aus, uji satu per satu', 'visual': 'Empat langkah berurutan muncul: membuka kolom, membersihkan kerak, mengganti katup aus, menguji tekanan dengan pengukur', 'purpose': 'Memberi urutan kerja inti turnaround dari buka sampai uji', 'watch': 'Ikuti urutan empat langkahnya sampai pengujian tekanan, karena unit tidak dinyalakan kembali sebelum setiap peralatan diuji satu per satu.'}, {'start': 27, 'end': 34, 'role': 'PAYOFF', 'title': 'Penyalaan kembali secara bertahap', 'on_screen': 'Dinyalakan lagi bertahap, unit per unit, sampai stabil', 'visual': 'Unit menyala satu per satu dari kiri ke kanan, grafik suhu naik landai dan stabil di garis operasi', 'purpose': 'Menegaskan penyalaan kembali sebagai tahap paling diawasi dalam turnaround', 'watch': 'Grafik suhu yang naik landai lalu stabil di garis operasi menunjukkan penyalaan kembali dilakukan bertahap, unit per unit.'}, {'start': 34, 'end': 40.9, 'role': 'TAKEAWAY', 'title': 'Berhenti terencana, beroperasi andal bertahun-tahun', 'on_screen': 'Berhenti direncanakan hari ini, jalan andal bertahun-tahun. Simpan video ini', 'visual': 'Pabrik cerah berjalan penuh dengan kalender kecil menandai turnaround berikutnya dan watermark @ilmutekkim', 'purpose': 'Menutup dengan kesimpulan satu kalimat dan aksi simpan', 'watch': 'Kalender kecil di akhir menandai turnaround berikutnya: jendela berhenti ini berulang secara terjadwal sepanjang umur pabrik.'}]},
    {'slug': 'buildup-boiler-pltu-dari-ceret', 'title': 'Membangun Pembangkit Listrik dari Satu Ceret Dapur', 'hook': 'Uap dari satu ceret dapur menyembur dari corong lalu hilang ke udara. Uap yang sama, setelah ditangkap dan diperkuat tahap demi tahap, memutar turbin dan menyalakan satu kota.', 'date': '2026-10-24', 'ig': 'https://www.instagram.com/reel/De2xbaEDve5/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-exp2-textured/buildup-exp2-final/renders/buildup-exp2-v3-textured.mp4', 'poster_src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-exp2-textured/buildup-exp2-final/renders/cover-exp2-v3textured.jpg', 'duration': 69.7, 'tag': 'Energi dan Utilitas', 'intro': 'Video ini memulai pembangunan dari satu ceret di atas kompor, yang uapnya keluar dari corong lalu hilang begitu saja. Setiap langkah menambahkan satu komponen yang menutup cacat langkah sebelumnya, dari kincir kecil sampai generator, sampai ceret yang sama bertransformasi menjadi pembangkit listrik tenaga uap yang siklus airnya tertutup.', 'tension': 'Putaran kincir dari uap ceret lemah dan mati begitu airnya habis, sedangkan uap yang dihasilkan satu ceret terlalu sedikit dan masih basah. Bagaimana rantai kelemahan itu ditutup sampai putaran berubah menjadi listrik?', 'takeaway': 'Pembangkit listrik tenaga uap adalah ceret yang uapnya ditangkap, tekanannya dinaikkan, jumlah uapnya dilipatgandakan, uapnya dikeringkan, dan putarannya disambungkan ke generator. Prinsipnya tetap satu dari awal sampai akhir, yaitu air mendidih menjadi uap dan uap bertekanan memutar turbin. Yang berubah hanya skalanya.', 'facts': ['Uap yang diarahkan melalui pipa ke kincir dapat memutar benda. Putaran tersebut lemah selama tekanan uap kecil, dan berhenti setelah air di dalam ceret habis.', 'Superheater adalah pipa tambahan pada titik terpanas api. Uap basah yang melewatinya keluar kering dan jauh lebih panas, dengan tenaga yang melonjak.', 'Kondensor menutup siklus air pembangkit. Uap bekas diubah kembali menjadi air dan dipompa balik ke boiler untuk dipakai lagi.'], 'quiz': {'answer': 0, 'explain': 'Uap dari jaringan pipa air masih basah dan penuh tetesan air. Superheater melewatkan uap tersebut melalui pipa tambahan pada titik terpanas api, sehingga uap keluar kering dan jauh lebih panas sebelum memasuki turbin.', 'options': ['Mengeringkan uap basah dan menaikkan suhunya pada titik terpanas api', 'Mengembunkan uap bekas menjadi air', 'Mengisi ulang air ke dalam ceret secara terus-menerus'], 'q': 'Apa fungsi superheater pada rantai pembangunan pembangkit ini?'}, 'scenes': [{'end': 6.0, 'on_screen': 'CERET. Airnya mendidih, dan uapnya menyembur keluar lewat corong, hilang begitu saja ke udara.', 'purpose': 'Menetapkan benda utama beserta cacat pertamanya, yaitu energi uap yang terbuang seluruhnya.', 'role': 'HOOK', 'start': 0.0, 'title': 'Ceret di atas kompor kehilangan uapnya ke udara', 'visual': 'Ceret air di atas kompor pada dapur yang hangat. Uap menyembur dari corong dan hilang ke udara tanpa dimanfaatkan.', 'watch': 'Perhatikan corong ceret dan uap yang hilang, karena ceret inilah benda yang sama sampai menjadi pembangkit pada bagian terakhir.'}, {'end': 11.2, 'on_screen': 'KINCIR. Sambungkan pipa ke corongnya, arahkan uapnya ke kincir kecil. Kincirnya berputar.', 'purpose': 'Menunjukkan fungsi pertama uap sebagai penggerak, sekaligus menyatakan cacatnya berupa putaran yang lemah.', 'role': 'PROSES', 'start': 6.0, 'title': 'Pipa dan kincir menangkap tenaga uap pertama', 'visual': 'Pipa tersambung dari corong ceret menuju kincir kecil. Aliran uap memutar kincir tersebut, walaupun putarannya lemah dan tersendat.', 'watch': 'Ikuti jalur pipa dari corong menuju kincir dan perhatikan bahwa putaran muncul hanya setelah uap diarahkan, bukan dibiarkan hilang.'}, {'end': 16.3, 'on_screen': 'TANGKI UMPAN. Air di ceret cepat habis, dan kincir pun berhenti. Pasang tangki yang mengisi ulang airnya terus-menerus.', 'purpose': 'Menutup cacat keberlangsungan, karena kincir berhenti setiap kali air di dalam ceret habis.', 'role': 'PROSES', 'start': 11.2, 'title': 'Tangki umpan mengisi air terus-menerus', 'visual': 'Tangki terpasang di samping ceret dan mengalirkan air pengisi terus-menerus ke dalam ceret melalui pipa.', 'watch': 'Perhatikan aliran pengisi dari tangki menuju ceret sebagai aliran yang menjaga proses tetap berjalan tanpa pengisian manual.'}, {'end': 25.0, 'on_screen': 'KATUP PENGAMAN. Dindingnya jauh lebih tebal, tutup rapat semuanya. Tekanannya naik, putarannya jauh lebih kencang.', 'purpose': 'Menutup cacat kekuatan putaran dengan menaikkan tekanan uap, dengan katup pengaman sebagai penjaga batas tekanan.', 'role': 'PROSES', 'start': 16.3, 'title': 'Dinding tebal dan katup pengaman menaikkan tekanan', 'visual': 'Dinding ceret dipertebal dan ditutup rapat, lengkap dengan katup pengaman. Tekanan di dalam naik dan putaran kincir menjadi jauh lebih kencang.', 'watch': 'Bandingkan kecepatan putaran pada bagian ini dengan putaran lemah pada bagian kedua, dan kaitkan selisihnya dengan tekanan yang naik.'}, {'end': 32.5, 'on_screen': 'PIPA AIR. Ganti perutnya dengan jaringan pipa-pipa berisi air, yang dipanaskan api dari segala sisi. Uapnya sekarang berlimpah.', 'purpose': 'Menutup cacat jumlah, karena satu ceret hanya menghasilkan sedikit uap walaupun tekanannya telah naik.', 'role': 'PROSES', 'start': 25.0, 'title': 'Jaringan pipa air melipatgandakan jumlah uap', 'visual': 'Badan ceret diganti jaringan pipa air di dalam kotak api. Air di dalam pipa dipanaskan dari segala sisi dan uap yang dihasilkan berlipat-lipat.', 'watch': 'Perhatikan luas permukaan pipa yang terkena api sebagai alasan jumlah uap bertambah, menggantikan satu dinding perut ceret.'}, {'end': 40.7, 'on_screen': 'SUPERHEATER. Lewatkan dulu lewat pipa tambahan di titik terpanas apinya. Uapnya keluar kering dan jauh lebih panas.', 'purpose': 'Menutup cacat kualitas uap, karena uap basah membawa tetesan air dan tenaganya lebih kecil daripada uap kering yang super panas.', 'role': 'PROSES', 'start': 32.5, 'title': 'Superheater mengeringkan uap pada titik terpanas', 'visual': 'Pipa tambahan terpasang pada titik terpanas api. Uap basah yang penuh tetesan air melewatinya dan keluar kering dengan suhu jauh lebih tinggi.', 'watch': 'Ikuti jalur uap memasuki pipa tambahan pada daerah api terpanas dan keluar dalam keadaan kering sebelum menuju penggerak berikutnya.'}, {'end': 48.4, 'on_screen': 'TURBIN. Ubah dia jadi turbin: deretan sudu bertingkat, tempat uap mengembang tahap demi tahap.', 'purpose': 'Menutup cacat kekuatan penggerak, karena kincir mainan tidak kuat menahan tenaga uap kering yang telah melonjak.', 'role': 'PROSES', 'start': 40.7, 'title': 'Kincir berubah menjadi turbin sudu bertingkat', 'visual': 'Kincir kecil berubah menjadi turbin dengan deretan sudu bertingkat. Uap mengembang tahap demi tahap dan memutar poros dengan halus dan kuat.', 'watch': 'Perhatikan deretan sudu yang bertingkat sebagai tempat pengembangan uap bertahap, berbeda dari satu kincir tunggal pada bagian awal.'}, {'end': 54.5, 'on_screen': 'GENERATOR. Sambungkan porosnya ke generator. Dan untuk pertama kalinya, lampunya menyala.', 'purpose': 'Melengkapi rantai konversi energi dari panas menjadi gerak dan dari gerak menjadi listrik, yang merupakan tujuan seluruh pembangunan.', 'role': 'PROSES', 'start': 48.4, 'title': 'Generator mengubah putaran menjadi listrik pertama', 'visual': 'Poros turbin tersambung ke generator. Lampu menyala untuk pertama kali sebagai tanda putaran telah berubah menjadi listrik.', 'watch': 'Lampu yang menyala pada bagian ini adalah hasil pertama yang dicari sejak uap ceret dibiarkan hilang pada bagian pertama.'}, {'end': 65.0, 'on_screen': 'BOILER. KONDENSOR. Besarkan semuanya ke skala pabrik. Siklusnya sekarang tertutup sempurna.', 'purpose': 'Mengubah seluruh rantai menjadi pembangkit yang utuh dan menutup siklus airnya, sehingga uap bekas tidak lagi terbuang.', 'role': 'PAYOFF', 'start': 54.5, 'title': 'Transformasi menjadi pembangkit listrik tenaga uap', 'visual': 'Gedung boiler berdinding pipa air dengan steam drum di puncak dan cerobong menjulang, turbin dan generator raksasa segaris, serta kondensor yang mengembunkan uap bekas untuk dipompa balik ke boiler.', 'watch': 'Ikuti panah siklus pada keadaan akhir ini, dari uap bekas menuju kondensor, lalu air yang dipompa balik menuju boiler.'}, {'end': 69.7, 'on_screen': 'KAMU BARU SAJA MEMBANGUN PEMBANGKIT LISTRIK.', 'purpose': 'Menutup pembangunan dengan benda hasil akhir pada skala penuh di lingkungannya, menyalurkan listrik ke kota.', 'role': 'TAKEAWAY', 'start': 65.0, 'title': 'Pembangkit beroperasi dan menerangi satu kota', 'visual': 'Tampilan menjauh memperlihatkan pembangkit yang beroperasi penuh pada senja, dengan jaringan transmisi dan lampu kota yang menyala di kejauhan.', 'watch': 'Kalimat penutup pada bagian ini merujuk pada ceret kecil pada bagian pertama, yang kini berdiri sebagai pembangkit.'}]},
    {'slug': 'buildup-kolom-distilasi-alembik', 'title': 'Membangun Kolom Distilasi dari Alembik, Alat Suling Tertua', 'hook': 'Alembik hanya mampu satu kali penguapan, dan hasilnya masih kotor. Kolom distilasi adalah jawaban atas keterbatasan tersebut.', 'date': '2026-10-23', 'ig': 'https://www.instagram.com/reel/De02HvcDhBY/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-ep1-final/renders/buildup-ep1-v13-gemini-vo.mp4', 'poster_src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-ep1-final/renders/buildup-ep1-v13-cover.jpg', 'duration': 72.4, 'tag': 'Peralatan Proses', 'intro': 'Video ini memulai pembangunan dari alembik, alat suling tertua yang hanya melakukan satu kali penguapan dan satu kali kondensasi. Setiap keterbatasan alat tersebut ditutup oleh satu penambahan, sampai seluruh tahap pemisahan tertumpuk menjadi satu kolom yang bekerja terus-menerus.', 'tension': 'Penguapan yang diulang berkali-kali memang menaikkan kemurnian, tetapi tahap yang terpisah menuntut ruang yang besar dan boros energi. Bagaimana seluruh tahap itu dapat digabungkan tanpa menghilangkan fungsinya?', 'takeaway': 'Kolom distilasi adalah alembik yang tahapnya ditumpuk menjadi satu menara. Tray menyediakan pertemuan uap dan cairan, reboiler dan kondensor menjaga aliran kedua arah, dan reflux menaikkan kemurnian produk atas, seluruhnya berdasarkan satu prinsip, yaitu perbedaan titik didih.', 'facts': ['Distilasi memisahkan campuran berdasarkan perbedaan titik didih. Komponen yang lebih mudah menguap naik sebagai uap, kemudian uap tersebut didinginkan kembali menjadi cairan.', 'Setiap tray di dalam kolom bekerja seperti satu kali penguapan mini. Kolom kilang pada umumnya berisi 30 sampai 50 tray.', 'Reflux adalah pengembalian sebagian cairan dari kondensor ke puncak kolom. Aliran balik ini menyapu komponen berat turun dan menaikkan kemurnian produk atas.'], 'quiz': {'answer': 0, 'explain': 'Alembik melakukan satu kali penguapan dan satu kali kondensasi, yang setara dengan satu tahap pemisahan. Kemurnian naik secara bertahap apabila tahap tersebut diulang, dan pengulangan itulah yang kemudian ditumpuk menjadi tray di dalam kolom.', 'options': ['Karena pemisahan hanya berlangsung satu tahap, sehingga komponen ringan dan berat belum terpisah sempurna', 'Karena alembik tidak memiliki sumber panas', 'Karena uap pada alembik tidak dapat didinginkan kembali'], 'q': 'Mengapa hasil satu kali penguapan pada alembik masih kotor?'}, 'scenes': [{'end': 10.9, 'on_screen': 'ALAT SULING TERTUA. Masalahnya: cuma satu kali penguapan. Hasilnya masih kotor.', 'purpose': 'Memperkenalkan bentuk primitif distilasi beserta cacat utamanya, yaitu pemisahan satu tahap yang kemurniannya terbatas.', 'role': 'HOOK', 'start': 0.0, 'title': 'Alembik, alat suling tertua dengan satu kali penguapan', 'visual': 'Alembik di atas pemanas dengan leher angsa menuju kondensor sederhana. Uap berwarna oranye naik dan tetesan berwarna biru keluar menuju wadah kecil.', 'watch': 'Perhatikan jalur tunggal uap dari bejana menuju wadah hasil, karena jalur tunggal inilah yang membatasi kemurnian produk.'}, {'end': 21.7, 'on_screen': 'Tambah: uapkan sekali lagi. Lebih murni. Tapi tahap terpisah begini makan tempat.', 'purpose': 'Menunjukkan bahwa pengulangan tahap menaikkan kemurnian, sekaligus membuka cacat baru berupa kebutuhan ruang dan energi.', 'role': 'PROSES', 'start': 10.9, 'title': 'Penguapan kedua menaikkan kemurnian tetapi boros tempat', 'visual': 'Tahap kedua muncul di atas tahap pertama. Uap hasil penguapan pertama diuapkan kembali pada bejana kedua yang lebih kecil.', 'watch': 'Bandingkan susunan dua bejana terpisah ini dengan satu bejana pada bagian sebelumnya untuk melihat pertambahan ruang yang dituntut.'}, {'end': 33.8, 'on_screen': 'Tumpuk jadi satu kolom. Tiap tray = satu kali penguapan mini.', 'purpose': 'Menutup cacat ruang dengan menumpuk seluruh tahap ke dalam satu menara, dengan tray sebagai pengganti setiap bejana terpisah.', 'role': 'PROSES', 'start': 21.7, 'title': 'Semua tahap ditumpuk menjadi satu kolom bertray', 'visual': 'Dua tahap yang terpisah melebur menjadi satu kolom vertikal. Tray bertingkat muncul satu per satu di dalam kolom yang transparan.', 'watch': 'Hitung kemunculan tray satu per satu dan kaitkan setiap tray dengan satu kali penguapan mini pada tahap terpisah sebelumnya.'}, {'end': 45.9, 'on_screen': 'Tambah: reboiler di bawah, kondensor di atas. Uap naik, cairan turun, bertemu di tiap tray.', 'purpose': 'Memberi sumber uap yang naik dan sumber cairan yang turun secara terus-menerus, sehingga pertemuan pada setiap tray dapat berlangsung tanpa henti.', 'role': 'PROSES', 'start': 33.8, 'title': 'Reboiler di bawah dan kondensor di atas menggerakkan dua aliran', 'visual': 'Reboiler menyala di dasar kolom dan mendidihkan cairan, sedangkan kondensor muncul di puncak. Uap oranye naik dan cairan biru turun dari tray ke tray.', 'watch': 'Ikuti dua arah aliran yang berlawanan, uap yang naik dari dasar dan cairan yang turun dari puncak, lalu perhatikan titik pertemuannya pada setiap tray.'}, {'end': 57.9, 'on_screen': 'Tambah: reflux. Sebagian hasil dikembalikan. Puncak kolom makin murni.', 'purpose': 'Menjelaskan aliran balik yang memperkaya komponen ringan di puncak dan menyapu komponen berat turun, sehingga kemurnian produk atas naik.', 'role': 'PROSES', 'start': 45.9, 'title': 'Reflux mengembalikan sebagian cairan ke puncak kolom', 'visual': 'Aliran produk dari kondensor bercabang. Sebagian keluar sebagai distilat dan sebagian kembali ke puncak kolom sebagai reflux yang menyala jalurnya.', 'watch': 'Perhatikan percabangan di keluaran kondensor dan bedakan bagian yang keluar sebagai produk dengan bagian yang kembali ke puncak.'}, {'end': 65.2, 'on_screen': 'Umpan masuk terus-menerus. Ringan keluar atas, berat keluar bawah.', 'purpose': 'Melengkapi pembangunan dengan operasi kontinu, keadaan akhir yang membedakan kolom industri dari penyulingan bertahap yang terputus-putus.', 'role': 'PAYOFF', 'start': 57.9, 'title': 'Umpan kontinu melengkapi kolom yang beroperasi penuh', 'visual': 'Pipa umpan masuk di tengah kolom secara terus-menerus, produk atas keluar secara kontinu, dan produk bawah yang berwarna oranye tua keluar dari dasar. Kamera mengorbit mengelilingi kolom yang utuh.', 'watch': 'Baca ketiga aliran secara bersamaan, umpan yang masuk di tengah, produk ringan yang keluar dari atas, dan produk berat yang keluar dari bawah.'}, {'end': 72.4, 'on_screen': '30-50 TRAY DALAM SATU KOLOM KILANG. KAMU BARU SAJA MEMBANGUN KOLOM DISTILASI.', 'purpose': 'Mengaitkan kolom hasil pembangunan dengan skala kolom kilang yang sebenarnya dan menutup rangkaian dengan prinsip yang sama dari awal sampai akhir.', 'role': 'TAKEAWAY', 'start': 65.2, 'title': 'Kolom kilang berisi 30 sampai 50 tray', 'visual': 'Angka besar 30 sampai 50 tray dalam satu kolom kilang, diikuti kalimat penutup dan ajakan melihat kalkulator teknik kimia di website.', 'watch': 'Angka pada bagian penutup ini adalah skala rujukan untuk kolom hasil pembangunan pada bagian bagian sebelumnya.'}]},
    {'slug': 'buildup-kolom-distilasi-remake', 'title': 'Membangun Kolom Distilasi dari Satu Tabung Logam', 'hook': 'Satu tabung logam terbuka di atas api kehilangan seluruh uapnya ke udara. Dari tabung yang sama, kolom distilasi dibangun satu tambahan pada satu waktu.', 'date': '2026-10-23', 'ig': 'https://www.instagram.com/reel/De1fCD3jxYa/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-exp1-final/renders/buildup-exp1-v4-factory.mp4', 'poster_src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-exp1-final/renders/cover-exp1-v4factory.jpg', 'duration': 69.8, 'tag': 'Peralatan Proses', 'intro': 'Video ini memulai pembangunan dari satu tabung logam terbuka di atas api, yang uapnya naik lalu hilang ke udara. Tabung tersebut tidak pernah diganti. Setiap langkah menambahkan satu komponen fisik yang menutup cacat langkah sebelumnya, sampai tabung yang sama berdiri sebagai kolom baja di tengah kilang.', 'tension': 'Uap yang telah ditangkap tetap belum menjadi cairan, hasil yang telah menjadi cairan tetap masih kotor, dan proses berhenti setiap kali campuran di dalam tabung habis. Cacat mana yang harus ditutup lebih dahulu agar pemisahan dapat berlangsung terus-menerus?', 'takeaway': 'Kolom distilasi adalah satu tabung yang ditutup, diberi pendingin, diberi umpan kontinu, diberi reflux, ditumbuhkan dengan tray di dalamnya, dan dilengkapi kondensor besar. Prinsipnya tetap satu dari awal sampai akhir, yaitu perbedaan titik didih, dan kolom kilang pada umumnya berisi 30 sampai 50 tray.', 'facts': ['Uap yang hanya ditampung melalui pipa tetap berwujud uap. Uap berubah menjadi cairan pertama setelah pipa tersebut dibungkus air dingin sebagai pendingin.', 'Reflux mengembalikan sebagian hasil ke puncak tabung. Uap yang naik dipaksa bertemu cairan yang turun, dan setiap pertemuan menaikkan kemurnian pemisahan.', 'Tray ditumpuk di dalam tabung yang tumbuh memanjang. Kolom kilang pada umumnya berisi 30 sampai 50 tray.'], 'quiz': {'answer': 0, 'explain': 'Tabung yang ditutup dan diberi pipa hanya memaksa uap keluar melalui pipa, dan uap tersebut tetap berwujud uap. Tetesan pertama muncul setelah pipa dibungkus air dingin, yang mengembunkan uap menjadi cairan.', 'options': ['Pendingin berupa air dingin yang membungkus pipa', 'Tangki umpan yang mengalirkan bahan terus-menerus', 'Pipa keluar di dasar tabung'], 'q': 'Komponen apa yang mengubah uap di dalam pipa menjadi tetesan cairan pertama?'}, 'scenes': [{'end': 5.6, 'on_screen': 'TABUNG TERBUKA. Uap yang paling ringan naik, lalu hilang begitu saja ke udara.', 'purpose': 'Menetapkan benda utama beserta cacat pertamanya, yaitu uap yang terbuang sehingga tidak ada hasil yang diperoleh.', 'role': 'HOOK', 'start': 0.0, 'title': 'Tabung terbuka di atas api kehilangan uapnya', 'visual': 'Campuran dipanaskan di dalam tabung logam terbuka di atas api. Uap ringan naik dari mulut tabung dan hilang ke udara tanpa ditangkap.', 'watch': 'Perhatikan mulut tabung yang terbuka dan arah uap yang hilang, karena tabung inilah benda yang sama sampai bagian terakhir.'}, {'end': 12.4, 'on_screen': 'TUTUP DAN PIPA. Uapnya dipaksa keluar lewat pipa itu. Masalahnya, dia tetap uap.', 'purpose': 'Menangkap uap yang sebelumnya hilang, sekaligus menyatakan cacat berikutnya bahwa uap yang tertangkap belum menjadi cairan.', 'role': 'PROSES', 'start': 5.6, 'title': 'Tabung ditutup dan diberi pipa, tetapi uap tetap uap', 'visual': 'Tabung yang sama ditutup dan pipa miring terpasang di puncaknya. Uap dipaksa keluar melalui pipa tersebut.', 'watch': 'Ikuti perubahan jalur uap dari mulut terbuka menuju pipa miring, lalu perhatikan bahwa wujudnya belum berubah.'}, {'end': 19.1, 'on_screen': 'PENDINGIN. Uap yang menyentuh pipa dingin berubah jadi tetesan.', 'purpose': 'Menutup cacat wujud dengan kondensasi, sehingga proses untuk pertama kali menghasilkan cairan, walaupun hasilnya masih kotor.', 'role': 'PROSES', 'start': 12.4, 'title': 'Pendingin pada pipa menghasilkan tetesan pertama', 'visual': 'Pipa dibungkus air dingin. Uap yang menyentuh dinding pipa yang dingin berubah menjadi tetesan dan jatuh ke dalam wadah sebagai cairan pertama.', 'watch': 'Perhatikan tetesan pertama yang jatuh ke wadah dan kaitkan kemunculannya dengan pendingin yang baru terpasang pada pipa.'}, {'end': 26.1, 'on_screen': 'TANGKI UMPAN. Campuran habis, tetesan berhenti. Pasang tangki dan pipa umpan yang mengalir terus.', 'purpose': 'Menutup cacat keberlangsungan, karena campuran di dalam tabung yang habis sebelumnya menghentikan tetesan hasil.', 'role': 'PROSES', 'start': 19.1, 'title': 'Tangki umpan membuat proses tidak pernah berhenti', 'visual': 'Tangki dan pipa umpan terpasang pada sisi tengah tabung dan mengalirkan campuran terus-menerus, menggantikan pengisian yang terputus-putus.', 'watch': 'Bedakan aliran umpan yang masuk terus-menerus ini dengan pengisian satu kali pada tabung di bagian awal.'}, {'end': 33.7, 'on_screen': 'REFLUX. Kembalikan sebagian tetesan ke puncak. Setiap pertemuan membuatnya makin murni.', 'purpose': 'Menutup cacat kemurnian dengan pertemuan berlawanan arah, yang memperkaya komponen ringan di puncak tabung.', 'role': 'PROSES', 'start': 26.1, 'title': 'Reflux memaksa uap bertemu cairan yang turun', 'visual': 'Sebagian tetesan hasil dikembalikan melalui pipa ke puncak tabung. Uap yang naik bertemu cairan yang turun di dalam tabung yang sama.', 'watch': 'Ikuti aliran balik dari wadah hasil menuju puncak dan perhatikan bahwa aliran ini bergerak berlawanan dengan uap yang naik.'}, {'end': 41.2, 'on_screen': 'TRAY. Satu pertemuan belum cukup. Tabung tumbuh memanjang, piringan ditumpuk di dalamnya.', 'purpose': 'Mengalikan jumlah pertemuan tanpa mengganti benda utama, dengan tray sebagai tempat setiap pertemuan tambahan.', 'role': 'PROSES', 'start': 33.7, 'title': 'Tabung tumbuh memanjang dan tray ditumpuk di dalamnya', 'visual': 'Tabung yang sama meregang ke atas dan tray ditumpuk satu di atas yang lain di dalamnya, sehingga pertemuan uap dan cairan berulang berkali-kali.', 'watch': 'Perhatikan pertambahan tinggi tabung dan tumpukan tray di dalamnya sebagai satu rangkaian pertumbuhan dari benda yang sama.'}, {'end': 47.9, 'on_screen': 'PIPA KELUAR DASAR. Cairan berat mengumpul di dasar. Yang berat keluar dari bawah.', 'purpose': 'Menutup cacat penumpukan cairan berat yang membuat tabung kepenuhan dan mengganggu operasi yang kontinu.', 'role': 'PROSES', 'start': 41.2, 'title': 'Pipa keluar di dasar mengeluarkan komponen berat', 'visual': 'Pipa keluar terpasang di dasar tabung. Cairan berat yang mengumpul dikeluarkan terus-menerus dari bawah, sedangkan komponen ringan tetap naik ke atas.', 'watch': 'Perhatikan dasar tabung sebagai titik keluar komponen berat, berlawanan posisi dengan puncak tempat komponen ringan berkumpul.'}, {'end': 56.0, 'on_screen': 'KONDENSOR. Pendingin kecil tumbuh jadi pendingin besar, dengan air yang dipompa memutar tanpa henti.', 'purpose': 'Menutup cacat kapasitas panas yang naik seiring tabung bekerja lebih keras dan menghasilkan uap lebih banyak.', 'role': 'PROSES', 'start': 47.9, 'title': 'Pendingin kecil tumbuh menjadi kondensor besar', 'visual': 'Pendingin pada pipa tumbuh menjadi kondensor besar dengan sirkulasi air yang dipompa. Panas dibuang keluar dan uap tetap berubah menjadi cairan pada beban yang lebih besar.', 'watch': 'Bandingkan ukuran pendingin pada bagian ini dengan pendingin pipa pada bagian ketiga untuk melihat pertumbuhan komponen yang sama.'}, {'end': 63.6, 'on_screen': 'Tutup cangkangnya sampai jadi baja utuh, pasang tangga di sisinya, sambungkan pipa di puncaknya ke tangki penyimpanan.', 'purpose': 'Mengubah seluruh tambahan yang terpisah menjadi satu kolom pabrik yang utuh, dengan peralatan pendamping berbentuk industri, bukan bentuk laboratorium yang diperbesar.', 'role': 'PAYOFF', 'start': 56.0, 'title': 'Tabung bertransformasi menjadi kolom pabrik yang utuh', 'visual': 'Cangkang menutup menjadi baja utuh dan badan meregang ke proporsi menara, lengkap dengan kepala kubah, tangga, platform, kondensor tertutup, reflux drum, dan pipa produk tertutup menuju tangki penyimpanan di tanah.', 'watch': 'Periksa keadaan akhir ini terhadap keadaan awalnya. Benda utamanya tetap tabung yang sama, sedangkan bentuk pendampingnya telah menjadi peralatan pabrik.'}, {'end': 69.8, 'on_screen': 'KAMU BARU SAJA MEMBANGUN KOLOM DISTILASI.', 'purpose': 'Menutup pembangunan dengan benda hasil akhir pada skala penuh di lingkungannya, beroperasi sebagaimana kolom kilang yang sebenarnya.', 'role': 'TAKEAWAY', 'start': 63.6, 'title': 'Kolom berdiri setinggi gedung di tengah kilang', 'visual': 'Tampilan menjauh memperlihatkan kolom pabrik raksasa yang tetap beroperasi di tengah kilang, dengan produk mengalir melalui pipa tertutup.', 'watch': 'Kalimat penutup pada bagian ini merujuk pada seluruh rantai tambahan sejak tabung terbuka pada bagian pertama.'}]},
    {'slug': 'buildup-reaktor-dari-panci-presto', 'title': 'Membangun Reaktor Kimia dari Satu Panci Presto', 'hook': 'Satu panci presto di atas kompor menyemburkan uap liar lewat katup dan dapat meledak apabila lengah. Reaktor kimia adalah panci yang sama setelah tekanan, campuran, dan suhunya dikendalikan.', 'date': '2026-10-24', 'ig': 'https://www.instagram.com/reel/De3pr_sjL7d/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-exp3-final/renders/buildup-exp3-v1.mp4', 'poster_src': '/home/hatch/workspace/coded-motion-graphics/videos/buildup-experimental/buildup-exp3-final/renders/cover-exp3-v1.jpg', 'duration': 69.9, 'tag': 'Peralatan Proses', 'intro': 'Video ini memulai pembangunan dari satu panci presto di atas kompor, yang isinya mendidih, tekanannya naik, dan uapnya menyembur liar lewat katup. Setiap langkah menambahkan satu pengendalian atau satu penguat yang menutup cacat langkah sebelumnya, sampai panci yang sama berdiri sebagai reaktor raksasa di tengah pabrik kimia.', 'tension': 'Isi panci yang tidak tercampur gosong di bawah dan mentah di atas, isi yang menghasilkan panas sendiri membuat suhu lari naik, dan badan yang tipis menyerah pada tekanan yang terus-menerus. Pengendalian apa yang harus ditambahkan lebih dahulu agar reaksi dapat berjalan aman dan kontinu?', 'takeaway': 'Reaktor kimia adalah panci presto yang tekanannya dijaga dan terbaca, isinya tercampur rata, panas berlebihnya dibuang, umpannya mengalir terus, badannya diperkuat, dan seluruh keadaannya dikendalikan otomatis. Prinsipnya tetap satu dari awal sampai akhir, yaitu reaksi yang dikendalikan. Yang berubah hanya skalanya.', 'facts': ['Katup pengaman yang membuka dan menutup teratur, lengkap dengan alat ukur tekanan, membuat tekanan di dalam panci stabil dan terbaca.', 'Jaket pendingin adalah lingkaran pada badan tempat air dingin mengalir terus. Panas berlebih dari isi yang menghasilkan panas sendiri dibuang melalui jaket tersebut, sehingga suhu menjadi jinak.', 'Bejana reaktor dibangun dari stainless berdinding tebal dengan tutup flensa yang dibaut rapat, menggantikan badan presto yang tipis dan menyerah pada tekanan serta aliran terus-menerus.'], 'quiz': {'answer': 0, 'explain': 'Setelah pengaduk membuat isi tercampur rata, isi mulai menghasilkan panasnya sendiri dan suhu lari naik. Jaket pendingin yang dilingkarkan pada badan, tempat air dingin mengalir terus, membuang panas berlebih tersebut dan membuat suhu jinak.', 'options': ['Jaket pendingin yang dilingkarkan pada badan', 'Katup pengaman pada tutup', 'Pengaduk yang dipasang dari atas'], 'q': 'Komponen apa yang membuang panas berlebih ketika isi reaktor mulai menghasilkan panasnya sendiri dan suhu lari naik?'}, 'scenes': [{'end': 6.6, 'on_screen': 'PRESTO. DITEKAN PANCI PRESTO, UAPNYA MENYEMBUR LIAR. Uap menyembur liar, tekanan tidak terkendali.', 'purpose': 'Menetapkan benda utama beserta cacat pertamanya, yaitu tekanan yang naik tanpa kendali dan ancaman meledak apabila lengah.', 'role': 'HOOK', 'start': 0.0, 'title': 'Panci presto menyemburkan uap liar lewat katup', 'visual': 'Panci presto di atas kompor pada dapur yang hangat. Isinya mendidih, tekanannya naik, dan uap menyembur liar lewat katup dengan desis yang tidak terkendali.', 'watch': 'Perhatikan katup pada tutup dan semburan uapnya, karena panci inilah benda yang sama sampai menjadi reaktor pada bagian terakhir.'}, {'end': 13.5, 'on_screen': 'KATUP PENGAMAN. Pasang katup pengaman + alat ukur. Tekanannya terbaca dan stabil.', 'purpose': 'Menutup cacat kendali tekanan, sekaligus membuka cacat berikutnya bahwa isi tidak tercampur, dengan bagian bawah gosong dan bagian atas mentah.', 'role': 'PROSES', 'start': 6.6, 'title': 'Katup pengaman dan alat ukur membuat tekanan terbaca', 'visual': 'Katup pengaman yang membuka dan menutup teratur terpasang pada tutup, lengkap dengan alat ukur tekanan. Semburan liar berhenti dan tekanan menjadi stabil.', 'watch': 'Perhatikan alat ukur pada tutup sebagai tanda tekanan kini terbaca, bukan lagi ditebak dari semburan uap.'}, {'end': 20.3, 'on_screen': 'PENGADUK. Pasang pengaduk dari atas. Tercampur rata, matang merata.', 'purpose': 'Menutup cacat pencampuran, sekaligus membuka cacat berikutnya bahwa isi menghasilkan panasnya sendiri dan suhu lari naik.', 'role': 'PROSES', 'start': 13.5, 'title': 'Pengaduk dari atas membuat isi tercampur rata', 'visual': 'Pengaduk terpasang dari atas menembus tutup dan berputar mengaduk seluruh isi. Perbedaan bagian bawah dan bagian atas hilang karena campuran menjadi rata.', 'watch': 'Ikuti putaran pengaduk dari puncak menembus tutup dan perhatikan bahwa geraknya menjangkau seluruh isi, bukan hanya permukaan.'}, {'end': 27.1, 'on_screen': 'JAKET PENDINGIN. Lingkari jaket pendingin. Suhunya jinak, panas berlebih dibuang.', 'purpose': 'Menutup cacat pengendalian suhu, sekaligus membuka cacat kapasitas, karena sekali masak tetap sedikit dan proses harus berhenti untuk pengisian ulang.', 'role': 'PROSES', 'start': 20.3, 'title': 'Jaket pendingin membuang panas berlebih', 'visual': 'Jaket pendingin melingkari badan panci dan air dingin mengalir terus di dalamnya. Suhu yang sebelumnya lari naik menjadi jinak.', 'watch': 'Perhatikan lingkaran jaket pada badan sebagai jalur air dingin yang terpisah dari isi yang didinginkan di dalamnya.'}, {'end': 33.5, 'on_screen': 'UMPAN KONTINU. Sambung umpan kontinu. Mengalir terus, tanpa pernah berhenti.', 'purpose': 'Menutup cacat keberlangsungan operasi batch, sekaligus membuka cacat kekuatan, karena badan presto yang tipis mulai menyerah pada tekanan dan aliran terus-menerus.', 'role': 'PROSES', 'start': 27.1, 'title': 'Umpan kontinu membuat aliran tidak pernah berhenti', 'visual': 'Pipa umpan tersambung dari tangki bahan dan pipa keluar terpasang untuk produk. Bahan mengalir masuk terus dan produk keluar terus tanpa membuka tutup.', 'watch': 'Bedakan aliran masuk dari tangki bahan dan aliran keluar produk sebagai dua aliran yang berjalan bersamaan tanpa henti.'}, {'end': 40.0, 'on_screen': 'BEJANA STAINLESS. Bangun bejana stainless tebal. Kuat menahan tekanan terus-menerus.', 'purpose': 'Menutup cacat kekuatan bahan, sekaligus membuka cacat penjagaan, karena belum ada yang menjaga suhu, tekanan, dan level selama dua puluh empat jam penuh.', 'role': 'PROSES', 'start': 33.5, 'title': 'Bejana stainless berdinding tebal menggantikan badan tipis', 'visual': 'Badan dibangun ulang menjadi bejana stainless berdinding tebal dengan tutup flensa yang dibaut rapat di sekelilingnya. Bejana kini kuat menahan tekanan operasi kontinu.', 'watch': 'Perhatikan baut pada sekeliling flensa tutup sebagai tanda penutupan telah berubah dari segel presto menjadi sambungan berkekuatan industri.'}, {'end': 47.2, 'on_screen': 'PANEL KENDALI. Pasang panel kendali otomatis. Terpantau dan terkendali sendiri.', 'purpose': 'Menutup cacat penjagaan terus-menerus, sekaligus menyatakan cacat terakhir bahwa skala bejana masih sekecil panci.', 'role': 'PROSES', 'start': 40.0, 'title': 'Sensor dan panel kendali otomatis menjaga seluruh keadaan', 'visual': 'Sensor terpasang pada berbagai titik dan terhubung ke panel kendali otomatis. Suhu, tekanan, dan level terpantau dan terkendali sendiri dengan aman tanpa dijaga.', 'watch': 'Perhatikan hubungan antara sensor pada bejana dan panel kendali sebagai satu rangkaian pemantauan yang bekerja tanpa penjagaan manusia.'}, {'end': 54.3, 'on_screen': 'Lengkapi jadi pabrik mini. Satu kesatuan proses, bekerja sendiri.', 'purpose': 'Melengkapi bejana menjadi satu kesatuan proses yang utuh sebelum perubahan skala, dengan penyimpanan dan pemindahan bahan tersambung seluruhnya.', 'role': 'PROSES', 'start': 47.2, 'title': 'Tangki dan pompa melengkapi satu kesatuan proses mini', 'visual': 'Tangki bahan terpasang pada satu sisi, tangki produk pada sisi lain, dan pompa penghubung di antaranya. Bejana berdiri sebagai satu pabrik kimia mini yang bekerja sendiri di halaman.', 'watch': 'Baca rangkaian ini sebagai satu sistem, dari tangki bahan melalui bejana menuju tangki produk, dengan pompa sebagai penghubungnya.'}, {'end': 64.3, 'on_screen': 'REAKTOR. Besarkan semuanya ke skala pabrik. Dia tidak lagi dimasak. Dia memproduksi.', 'purpose': 'Mengubah kesatuan proses mini menjadi reaktor pabrik yang utuh, dengan seluruh pengendalian dari langkah sebelumnya hadir dalam bentuk industri.', 'role': 'PAYOFF', 'start': 54.3, 'title': 'Bejana tumbuh menjadi reaktor raksasa di pabrik kimia', 'visual': 'Bejana tumbuh di tempat menjadi reaktor raksasa stainless dengan pengaduk bermotor besar di puncak, jaket pendingin raksasa pada badan, platform bertingkat, pipa dari tangki penyimpanan, dan panel kendali industri.', 'watch': 'Periksa keadaan akhir ini terhadap panci pada bagian pertama. Pengaduk, jaket, dan pengendaliannya tetap ada, sedangkan gagang dan katup kecil khas presto telah hilang.'}, {'end': 69.9, 'on_screen': 'KAMU BARU SAJA MEMBANGUN REAKTOR KIMIA.', 'purpose': 'Menutup pembangunan dengan benda hasil akhir pada skala penuh di lingkungannya, beroperasi sebagai jantung pabrik kimia.', 'role': 'TAKEAWAY', 'start': 64.3, 'title': 'Reaktor berdiri sebagai jantung pabrik kimia', 'visual': 'Tampilan menjauh memperlihatkan kompleks pabrik kimia yang beroperasi pada siang terang, dengan reaktor, kolom, dan deretan tangki penyimpanan di lingkungannya.', 'watch': 'Kalimat penutup pada bagian ini merujuk pada panci presto pada bagian pertama, yang kini berdiri sebagai reaktor.'}]},
    {'slug': 'ko-drum-penjaga-kompresor', 'title': 'KO Drum: Penjaga Kompresor dari Tetesan Cairan', 'hook': 'Satu tetesan cairan yang lolos dapat menghancurkan kompresor.', 'date': '2026-10-23', 'ig': 'https://www.instagram.com/reel/De1xWppDg8e/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-23/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-23/motion-1/cover.jpg', 'duration': 41.0, 'tag': 'Separasi Gas dan Kompresor', 'intro': 'Kompresor dirancang untuk memampatkan gas, tetapi aliran gas dari proses tidak pernah benar-benar kering. Video ini membedah mengapa tetesan cairan yang terbawa aliran berbahaya bagi kompresor, dan bagaimana KO drum memisahkannya sebelum gas tiba di mesin.', 'tension': 'Gas yang masuk kompresor tidak pernah benar-benar kering, dan tetesan cairan yang terbawa di dalamnya dapat merusak mesin yang seharusnya hanya memampatkan gas.', 'takeaway': 'KO drum adalah asuransi yang sederhana sebelum mesin yang mahal: gas masuk, kecepatannya turun, tetesan jatuh oleh gravitasi, cairan dibuang melalui drain, dan gas kering keluar dari atas menuju kompresor.', 'facts': ['KO drum memisahkan tetesan cairan dari aliran gas secara gravitasi sebelum gas masuk kompresor.', 'Cairan tidak termampatkan, sehingga tetesan yang masuk ke kompresor menghantam bilah dengan keras dan merusak bilah serta seal.', 'Di dalam KO drum, kecepatan gas diturunkan sehingga tetesan jatuh oleh gravitasi; gas kering keluar dari atas, sedangkan cairan terkumpul di bawah dan dibuang melalui drain.'], 'quiz': {'q': 'Mengapa tetesan cairan berbahaya bagi kompresor?', 'options': ['Karena cairan membuat gas lebih mudah dimampatkan', 'Karena cairan tidak termampatkan, sehingga tetesan menghantam bilah kompresor dengan keras', 'Karena cairan menurunkan suhu gas masuk'], 'answer': 1, 'explain': 'Kompresor dirancang untuk gas yang volumenya menyusut ketika dimampatkan. Cairan hampir tidak menyusut, sehingga energi tumbukan tetesan diterima langsung oleh bilah dan seal. KO drum mencegah tetesan itu tiba di mesin dengan memisahkannya secara gravitasi.'}, 'scenes': [{'start': 0.0, 'end': 4.0, 'role': 'HOOK', 'title': 'Tetesan cairan mengancam kompresor', 'on_screen': 'TETESAN AIR INI BISA MENGHANCURKAN KOMPRESOR', 'visual': 'Kompresor digambar di tengah, satu tetesan air jatuh ke arahnya dengan efek tegang.', 'purpose': 'Menancapkan ancaman: tetesan kecil vs mesin mahal.', 'watch': 'Satu tetesan air yang jatuh ke arah kompresor pada bingkai pembuka menetapkan ancaman yang akan dijawab oleh urutan pengamanannya.'}, {'start': 4.0, 'end': 11.0, 'role': 'TENSION', 'title': 'Gas proses yang tidak pernah kering', 'on_screen': 'Gas dari proses tidak pernah benar-benar kering', 'visual': 'Pipa horizontal, aliran gas digambar dengan tetesan-tetesan kecil ikut mengalir.', 'purpose': 'Membangun konteks: cairan selalu ikut terbawa aliran gas.', 'watch': 'Tetesan kecil yang ikut mengalir di dalam pipa menunjukkan bahwa cairan terbawa aliran gas dari proses secara alami.'}, {'start': 11.0, 'end': 18.0, 'role': 'TENSION', 'title': 'Cairan yang tidak termampatkan menabrak bilah', 'on_screen': 'Kompresor untuk gas. Cairan tidak bisa dimampatkan.', 'visual': 'Bilah kompresor berputar, tetesan menabrak bilah dan memicu retakan visual.', 'purpose': 'Menjelaskan kenapa tetesan berbahaya bagi kompresor.', 'watch': 'Tetesan yang menabrak bilah berputar dan retakan yang muncul menggambarkan kerusakan yang terjadi di dalam kompresor.'}, {'start': 18.0, 'end': 26.0, 'role': 'PAYOFF', 'title': 'Pemisahan gravitasi di dalam KO drum', 'on_screen': 'KO drum: gas masuk, kecepatan turun, tetesan jatuh.', 'visual': 'Drum vertikal: gas masuk dari samping, tetesan jatuh ke bawah oleh gravitasi, gas kering keluar dari atas.', 'purpose': 'Memperkenalkan solusi: pemisahan gravitasi di KO drum.', 'watch': 'Drum vertikal dengan gas masuk dari samping, tetesan jatuh ke bawah, dan gas kering keluar dari atas adalah keseluruhan prinsip kerjanya dalam satu gambar.'}, {'start': 26.0, 'end': 34.0, 'role': 'PAYOFF', 'title': 'Cairan terkumpul dan dibuang melalui drain', 'on_screen': 'Cairan terkumpul di bawah, didrain otomatis.', 'visual': 'Level cairan di dasar drum naik, valve drain terbuka berkala, gas bersih mengalir ke kompresor.', 'purpose': 'Melengkapi siklus: cairan tidak menumpuk, gas kering lanjut aman.', 'watch': 'Level cairan yang naik di dasar drum dan katup drain yang terbuka berkala menunjukkan bahwa cairan hasil pemisahan tidak dibiarkan menumpuk.'}, {'start': 34.0, 'end': 41.0, 'role': 'TAKEAWAY_CTV', 'title': 'Urutan pengaman sebelum kompresor', 'on_screen': 'KO drum = asuransi murah sebelum mesin mahal. Simpan urutannya.', 'visual': 'Rangkuman tiga langkah: pisahkan, drain, lindungi; tombol save disorot halus.', 'purpose': 'Takeaway satu kalimat yang bisa diingat plus ajakan simpan yang beralasan.', 'watch': 'Rangkuman tiga langkah pada penutup, yaitu pisahkan, drain, dan lindungi, adalah urutan yang perlu diingat dari video ini.'}]},
    {'slug': 'lpg-cairan-dalam-tabung', 'title': 'Isi Tabung LPG Bukan Gas, Melainkan Cairan', 'hook': 'Isi tabung LPG bukan gas, melainkan cairan.', 'date': '2026-10-21', 'ig': 'https://www.instagram.com/reel/Dewnp1uD5cl/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-21/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-21/motion-1/cover.jpg', 'duration': 40.9, 'tag': 'Perubahan Fasa', 'intro': 'Tabung LPG di dapur lazim disebut tabung gas, tetapi isinya bukan gas yang dimampatkan. Video ini membedah bagaimana campuran propana dan butana dapat tersimpan sebagai cairan di dalam tabung, serta apa yang terjadi pada saat katup dibuka.', 'tension': 'Tabung terasa berisi gas bertekanan, padahal yang di dalam adalah cairan; begitu katup dibuka, cairan itu mendidih menjadi gas.', 'takeaway': 'Tekanan di dalam tabung menjaga LPG tetap cair, dan pembukaan katup menurunkan tekanan sehingga cairan mendidih menjadi gas yang mengalir ke kompor.', 'facts': ['LPG adalah campuran propana (C3H8) dan butana (C4H10), dengan titik didih propana minus 42 derajat C dan butana minus 0,5 derajat C pada 1 atm.', 'Tabung LPG hanya diisi 80 sampai 85 persen dari kapasitasnya agar cairan memiliki ruang untuk memuai pada saat suhu naik.', 'Satu liter LPG cair mengembang menjadi sekitar 250 liter gas, dan uap LPG yang lebih berat dari udara menyebabkan gas yang bocor mengendap di lantai.'], 'quiz': {'q': 'Mengapa tabung LPG tidak diisi penuh sampai 100 persen?', 'options': ['Agar tabung lebih ringan dibawa', 'Agar cairan memiliki ruang memuai pada saat suhu naik', 'Agar gas lebih cepat habis'], 'answer': 1, 'explain': 'Cairan memuai ketika suhu naik. Pengisian 80 sampai 85 persen menyisakan ruang uap di atas cairan, sehingga kenaikan suhu tidak langsung menaikkan tekanan secara berlebihan di dalam tabung tertutup.'}, 'scenes': [{'start': 0.0, 'end': 6.0, 'role': 'HOOK', 'title': 'Isi tabung LPG adalah cairan', 'on_screen': 'ISI TABUNG LPG / BUKAN GAS, TAPI CAIRAN', 'visual': 'Tabung LPG 3 kg digambar utuh, lalu potongan melintang memperlihatkan cairan memenuhi sebagian besar tabung dengan ruang uap di atasnya.', 'purpose': 'Menanamkan kejutan: isi tabung adalah cairan, bukan gas bertekanan.', 'watch': 'Potongan melintang tabung memperlihatkan cairan yang mengisi sebagian besar tabung dengan ruang uap di atasnya.'}, {'start': 6.0, 'end': 13.0, 'role': 'TENSION', 'title': 'Titik didih propana dan butana', 'on_screen': 'PROPANA MENDIDIH -42°C, BUTANA -0,5°C', 'visual': 'Dua kartu molekul muncul: propana C3H8 (-42°C) dan butana C4H10 (-0,5°C); panah suhu ruang 30°C menekan dari atas.', 'purpose': 'Menjelaskan kenapa LPG ingin menjadi gas pada suhu ruang.', 'watch': 'Dua kartu molekul dan panah suhu ruang menunjukkan bahwa kedua komponen berada jauh di atas titik didihnya pada keadaan tanpa tekanan.'}, {'start': 13.0, 'end': 20.0, 'role': 'TENSION', 'title': 'Tekanan menahan LPG tetap cair', 'on_screen': 'TEKANAN MENAHANNYA TETAP CAIR', 'visual': 'Indikator tekanan naik menekan molekul; garis batas isi 80-85 persen digambar di tabung dengan label ruang muai.', 'purpose': 'Tekanan di tabung menahan keduanya sebagai cairan; ruang muai dijelaskan.', 'watch': 'Garis batas isi 80 sampai 85 persen pada tabung menandai ruang muai yang sengaja disisakan di atas cairan.'}, {'start': 20.0, 'end': 27.0, 'role': 'PAYOFF', 'title': 'Katup dibuka, cairan mendidih menjadi gas', 'on_screen': 'KATUP DIBUKA, CAIRAN MENDIDIH JADI GAS / 1 LITER CAIRAN = SEKITAR 250 LITER GAS', 'visual': 'Katup terbuka, tekanan turun, gelembung naik di cairan, aliran gas ke kompor; label 1:250 muncul di samping tabung.', 'purpose': 'Katup dibuka: tekanan turun, cairan mendidih menjadi gas dengan rasio muai.', 'watch': 'Gelembung yang naik di dalam cairan dan label 1:250 menunjukkan perubahan fasa beserta perbandingan volumenya.'}, {'start': 27.0, 'end': 34.0, 'role': 'PAYOFF', 'title': 'Tabung mendingin dan gas bocor mengendap', 'on_screen': 'TABUNG MENDINGIN SAAT DIPAKAI / GAS BOCOR MENGENDAP DI LANTAI', 'visual': 'Embun dingin muncul di dinding tabung; simulasi kebocoran: awan gas turun dan mengendap di lantai, bukan naik.', 'purpose': 'Dua akibat fisika yang bisa dirasakan: tabung dingin dan gas berat mengendap.', 'watch': 'Embun dingin pada dinding tabung dan awan gas yang turun ke lantai adalah dua akibat fisika yang ditampilkan berurutan.'}, {'start': 34.0, 'end': 40.9, 'role': 'TAKEAWAY_CTV', 'title': 'Tekanan menjaga cairan, katup melepas gas', 'on_screen': 'TEKANAN JAGA CAIR, KATUP LEPAS JADI GAS', 'visual': 'Ringkasan tiga ikon berurutan: cairan, tekanan, gas; watermark @ilmutekkim dan teks ajakan follow.', 'purpose': 'Takeaway satu kalimat plus ajakan follow sebagai CTV.', 'watch': 'Tiga ikon berurutan pada penutup merangkum rantai kejadiannya: cairan, tekanan, lalu gas.'}]},
    {'slug': 'ntu-efektivitas-penukar-panas', 'title': 'Metode NTU Efektivitas: Menghitung Penukar Panas Tanpa Menebak Suhu Keluar', 'hook': 'Duty penukar panas dapat dihitung tanpa mengetahui suhu keluarnya terlebih dahulu.', 'date': '2026-10-21', 'ig': 'https://www.instagram.com/reel/DewMhqEPPP7/', 'src': '/home/hatch/workspace/coded-motion-graphics/videos/2026-10-21-ntu-efektivitas/renders/ntu-efektivitas_v3_2026-10-21.mp4', 'poster_src': '/home/hatch/workspace/coded-motion-graphics/videos/2026-10-21-ntu-efektivitas/renders/cover_v3_2026-10-21.jpg', 'duration': 38.0, 'tag': 'Penukar Panas', 'intro': 'Metode LMTD menuntut suhu keluar diketahui, padahal pada penukar panas yang sudah terpasang suhu keluar justru merupakan besaran yang dicari. Video ini mengerjakan satu contoh hitungan counterflow secara tuntas dengan metode NTU efektivitas, dari laju kapasitas panas sampai suhu keluar kedua aliran.', 'tension': 'Suhu keluar belum diketahui sehingga LMTD menuntut tebakan dan iterasi, padahal duty menentukan suhu keluar itu sendiri.', 'takeaway': 'Tanpa suhu keluar, duty tetap dapat dihitung: pada contoh ini duty aktual 101,65 kW, dengan suhu keluar aliran panas 69,2 derajat C dan aliran dingin 55,4 derajat C, dan neraca energinya tertutup.', 'facts': ['C adalah laju kapasitas panas, C = m dot cp. Pada contoh ini Ch bernilai 2 kW/K dan Cc bernilai 4 kW/K, sehingga Cmin 2 kW/K dan Cmax 4 kW/K.', 'Qmax = Cmin (Th,in dikurangi Tc,in) = 2 x 90 = 180 kW, dan NTU = UA/Cmin = 1,00 menyatakan ukuran penukar panas relatif terhadap Cmin.', 'Pada NTU 1,00 dan Cr 0,50, efektivitas counterflow adalah 0,565, sehingga Q = 101,65 kW atau 56,5 persen dari Qmax.'], 'quiz': {'q': 'Mengapa metode NTU efektivitas dipilih ketika suhu keluar penukar panas belum diketahui?', 'options': ['Karena metode LMTD tidak berlaku pada aliran counterflow', 'Karena metode ini menghitung duty dari suhu masuk, kapasitas panas, dan UA tanpa menebak suhu keluar terlebih dahulu', 'Karena metode ini tidak memerlukan data laju aliran'], 'answer': 1, 'explain': 'LMTD memerlukan suhu keluar untuk menghitung beda suhu rata-rata, sehingga suhu keluar harus ditebak dan perhitungan diulang. Metode NTU efektivitas bekerja dari besaran yang diketahui di sisi masuk dan ukuran penukar panas, lalu suhu keluar diperoleh sesudahnya dari neraca energi.'}, 'scenes': [{'start': 0, 'end': 5, 'role': 'HOOK', 'title': 'Metode NTU efektivitas dan laju kapasitas panas', 'on_screen': 'METODE NTU / EFEKTIVITAS / Penukar panas counterflow, satu contoh hitungan tuntas. / CONTOH: Th,in 120 derajat C, Tc,in 30 derajat C, Ch 2, Cc 4, UA 2 kW/K / 1 / Laju Kapasitas Panas / C = m dot cp / Ch 2,0 kW/K panas / Cc 4,0 kW/K dingin', 'visual': 'Judul metode muncul di detik 0, strip data soal, lalu kartu 1 menumpuk dengan batang Ch dan Cc terisi proporsional.', 'purpose': 'Pembuka langsung ke judul metode, strip data soal, dan kartu 1 laju kapasitas panas.', 'watch': 'Perhatikan strip data soal di bagian awal, karena seluruh angka pada kartu berikutnya berasal dari lima besaran masuk tersebut.'}, {'start': 5, 'end': 11, 'role': 'TENSION', 'title': 'Rasio kapasitas dan perpindahan panas maksimum', 'on_screen': '2 / Rasio Kapasitas / Cr = Cmin / Cmax / Cr 0,50 / 3 / Perpindahan Panas Maksimum / Qmax = Cmin (Th,in dikurangi Tc,in) / Qmax 180 kW', 'visual': 'Kartu 2 dan 3 menumpuk. Slider Cr bergerak ke 0,50, chip beda suhu 90 K muncul, Qmax menghitung ke 180.', 'purpose': 'Kartu 2 rasio kapasitas dan kartu 3 Qmax. Duty aktual masih ditahan.', 'watch': 'Slider Cr yang berhenti pada 0,50 dan chip beda suhu 90 K menunjukkan dua besaran yang menentukan batas perpindahan panasnya.'}, {'start': 11, 'end': 17.5, 'role': 'TENSION', 'title': 'Jumlah satuan perpindahan', 'on_screen': '4 / Jumlah Satuan Perpindahan / NTU = UA / Cmin / NTU 1,00 / ukuran penukar panas relatif terhadap Cmin', 'visual': 'Kartu 4 menumpuk. Strip aliran counterflow panah berlawanan arah bergerak, skala NTU terisi sampai 1,00.', 'purpose': 'Kartu 4 NTU: ukuran penukar panas dan strip aliran counterflow. Efektivitas masih ditahan.', 'watch': 'Panah kedua aliran yang berlawanan arah menegaskan susunan counterflow, sedangkan skala NTU yang terisi sampai 1,00 menyatakan ukuran relatif penukar panas.'}, {'start': 17.5, 'end': 24, 'role': 'PAYOFF', 'title': 'Efektivitas counterflow', 'on_screen': '5 / Efektivitas Counterflow / relasi counterflow untuk Cr kurang dari 1 / epsilon 0,565 / titik kerja NTU 1,00 dan epsilon 0,565 pada kurva Cr 0,5', 'visual': 'Kartu 5 menumpuk. Tiga kurva epsilon NTU tergambar, titik kerja bergerak ke NTU 1,00, garis pemandu muncul.', 'purpose': 'Kartu 5 efektivitas counterflow dari relasi dan kurva epsilon NTU, titik kerja ditandai.', 'watch': 'Titik kerja pada kurva Cr 0,5 adalah hasil bacaan utamanya: NTU 1,00 berpasangan dengan efektivitas 0,565.'}, {'start': 24, 'end': 30, 'role': 'PAYOFF', 'title': 'Duty dan suhu keluar', 'on_screen': '6 / Duty dan Suhu Keluar / Q = epsilon Qmax / Q 101,65 kW / 56,5 persen dari Qmax / Th,out 69,2 derajat C / Tc,out 55,4 derajat C', 'visual': 'Kartu 6 menumpuk. Batang duty terisi 56,5 persen, suhu keluar menghitung ke nilai akhir.', 'purpose': 'Kartu 6 jawaban akhir: duty aktual dan suhu keluar kedua aliran.', 'watch': 'Batang duty yang terisi 56,5 persen menunjukkan posisi duty aktual terhadap batas maksimumnya sebelum suhu keluar ditampilkan.'}, {'start': 30, 'end': 38, 'role': 'TAKEAWAY_CTV', 'title': 'Neraca energi dan kesimpulan', 'on_screen': 'Neraca energi cocok: Ch delta Th = Cc delta Tc = Q = 101,65 kW / Tanpa suhu keluar, duty tetap bisa dihitung. / SIMPAN HITUNGAN INI / Follow @ilmutekkim untuk cheat sheet perpindahan panas berikutnya.', 'visual': 'Strip hijau neraca energi dan strip biru takeaway plus CTV muncul di bawah poster utuh berisi enam kartu, lalu ditahan.', 'purpose': 'Strip neraca energi membuktikan hitungan konsisten, takeaway dan CTV, poster utuh ditahan sampai akhir untuk tangkapan layar.', 'watch': 'Poster utuh berisi enam kartu pada penutup merangkum seluruh urutan hitungan dalam satu bingkai.'}]},
    {'slug': 'steam-trap-katup-kondensat', 'title': 'Steam Trap: Katup Kecil yang Membuang Kondensat Tanpa Membuang Uap', 'hook': 'Steam trap yang rusak membuang steam hidup secara diam-diam.', 'date': '2026-10-22', 'ig': 'https://www.instagram.com/reel/DezMjuWDvr4/', 'src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-22/motion-1/motion.mp4', 'poster_src': '/home/hatch/workspace/ig-ilmutekkim/media/2026-10-22/motion-1/cover.jpg', 'duration': 41.5, 'tag': 'Sistem Uap dan Utilitas', 'intro': 'Steam trap adalah katup kecil yang terpasang pada jalur pembuangan sistem steam. Video ini membedah tugas gandanya, yaitu membuang kondensat tanpa membuang steam hidup, serta alasan kerusakan pada alat ini sering tidak terlihat.', 'tension': 'Steam trap yang rusak terbuka membuang steam hidup terus-menerus, dan kebocoran itu tidak terlihat karena wujudnya sama seperti kondensat yang dibuang normal.', 'takeaway': 'Steam trap yang baik membuang kondensat dan menahan steam hidup secara otomatis. Trap yang gagal terbuka membuang steam hidup secara kontinu, sehingga pemeriksaannya merupakan bagian dari efisiensi sistem steam.', 'facts': ['Steam trap adalah katup otomatis yang membuang kondensat sambil mencegah kehilangan steam hidup, dan seluruh tugas itu dikerjakan tanpa listrik.', 'Kondensat terbentuk ketika steam melepaskan panas latennya; kondensat yang tidak dibuang menyebabkan water hammer dan menurunkan perpindahan panas.', 'Tiga keluarga utama steam trap adalah mekanis (pelampung dan ember terbalik), termostatik (bimetal), dan termodinamik (cakram), dan masing-masing dipilih berdasarkan tekanan serta beban kondensatnya.'], 'quiz': {'q': 'Apa tugas ganda steam trap pada sistem steam?', 'options': ['Membuang steam hidup dan menahan kondensat', 'Membuang kondensat dan menahan steam hidup secara otomatis', 'Menaikkan tekanan steam dan membuang udara'], 'answer': 1, 'explain': 'Kondensat harus keluar karena genangannya menyebabkan water hammer dan menurunkan perpindahan panas, sedangkan steam hidup harus tertahan karena steam adalah pembawa energi yang mahal. Steam trap memisahkan keduanya secara otomatis berdasarkan perbedaan sifat air dan steam.'}, 'scenes': [{'start': 0.0, 'end': 6.5, 'role': 'HOOK', 'title': 'Steam trap rusak membuang steam hidup', 'on_screen': 'STEAM TRAP RUSAK BUANG UANG DIAM-DIAM', 'visual': "Pipa steam dengan steam trap di bawahnya; animasi uap keluar terus dari lubang buang, label 'steam hidup terbuang'.", 'purpose': 'Menancapkan masalah: steam trap yang gagal-terbuka membuang steam hidup tanpa terlihat.', 'watch': 'Aliran uap yang keluar terus dari lubang buang adalah tanda kegagalan yang dibahas: steam hidup terbuang bersama jalur pembuangan kondensat.'}, {'start': 6.5, 'end': 13.0, 'role': 'TENSION', 'title': 'Steam melepaskan panas dan menjadi air', 'on_screen': 'STEAM MELEPAS PANAS = JADI AIR', 'visual': 'Penampang pipa: partikel steam berubah menjadi tetesan air yang menggenang di dasar pipa.', 'purpose': 'Menjelaskan kenapa kondensat harus dibuang: steam melepaskan panas laten dan berubah jadi air.', 'watch': 'Partikel steam yang berubah menjadi tetesan air dan menggenang di dasar pipa menunjukkan asal kondensat di dalam jalur steam.'}, {'start': 13.0, 'end': 20.0, 'role': 'TENSION', 'title': 'Kondensat yang dibiarkan dan water hammer', 'on_screen': 'AIR DI PIPA = WATER HAMMER', 'visual': 'Genangan air terseret aliran steam, menabrak belokan pipa; gelombang kejut digambar sebagai garis kejut.', 'purpose': 'Menunjukkan akibat kondensat dibiarkan: water hammer dan perpindahan panas yang turun.', 'watch': 'Genangan air yang terseret aliran dan menabrak belokan pipa menghasilkan gelombang kejut yang digambarkan sebagai garis kejut.'}, {'start': 20.0, 'end': 29.0, 'role': 'PAYOFF', 'title': 'Tiga tipe steam trap', 'on_screen': '3 TIPE: PELAMPUNG, EMBER, CAKRAM', 'visual': 'Tiga panel sejajar: bola pelampung naik-turun membuka katup; ember terbalik tenggelam-timbul; cakram membuka-menutup cepat oleh steam kilat.', 'purpose': 'Menunjukkan cara kerja tiga tipe steam trap: pelampung, ember terbalik, cakram termodinamik.', 'watch': 'Tiga panel sejajar membandingkan gerak pelampung, ember terbalik, dan cakram termodinamik sebagai tiga mekanisme pemisahan yang berbeda.'}, {'start': 29.0, 'end': 36.0, 'role': 'PAYOFF', 'title': 'Air lewat, steam tertahan', 'on_screen': 'AIR LEWAT, STEAM TERTAHAN. OTOMATIS.', 'visual': 'Zoom ke satu trap: tetesan air keluar dari lubang buang, partikel steam memantul kembali ke dalam.', 'purpose': 'Menegaskan prinsip inti: air lewat, steam tertahan, otomatis tanpa listrik.', 'watch': 'Tetesan air yang lolos melalui lubang buang dan partikel steam yang memantul kembali menunjukkan prinsip pemisahan pada satu alat.'}, {'start': 36.0, 'end': 41.5, 'role': 'TAKEAWAY_CTV', 'title': 'Panduan tiga tipe steam trap', 'on_screen': 'SIMPAN: PANDUAN 3 TIPE STEAM TRAP', 'visual': 'Tiga ikon tipe trap berderet dengan nama tipenya; watermark @ilmutekkim + progress bar penuh.', 'purpose': 'Takeaway satu kalimat + CTV simpan sebagai referensi tipe trap.', 'watch': 'Tiga ikon tipe trap yang berderet pada penutup merangkum pilihan mekanisme yang tersedia untuk sistem steam.'}]}
]



# --- Artikel versi baca untuk halaman video (ILM-R63 + ILM-R64: mendalam, hook kitab suci, sitasi) ---
VIDEO_ARTICLES = {
    'sampling-rutin-lab': {
        "lead": 'Pabrik modern telah dilengkapi sensor yang membaca proses setiap detik. Mengapa operatornya tetap berjalan membawa botol sampel ke laboratorium setiap jam?',
        "sections": [
            {"h": 'Sensor hanya mengukur titik yang disentuhnya', "t": 6, "paras": [
                'Sensor online seperti probe pH, konduktivitas, atau densitas hanya mengukur fluida yang menyentuh ujung probenya. Pada pipa berdiameter besar, sebagian besar aliran melintas jauh dari titik tersebut, dan fluida yang tidak tersentuh sensor tidak ikut terukur. Bacaan pada layar merupakan potret satu titik, bukan potret keseluruhan aliran [1].',
                'Di sinilah sampel fisik mengambil perannya. Sejumlah kecil fluida benar-benar dikeluarkan dari proses dan diperiksa secara langsung, sehingga yang dinilai adalah bahannya sendiri, bukan sinyal listrik yang mewakilinya.',
            ]},
            {"h": 'Bacaan sensor yang bergeser secara perlahan', "t": 13, "paras": [
                'Sensor mengalami drift: bacaannya bergeser secara perlahan menjauhi nilai sebenarnya karena kerak menempel pada probe, elektroda menua, atau komponen elektronikanya berubah. Pergeseran ini tidak memicu alarm, karena dari sudut pandang sistem, angkanya tampak normal.',
                'Apabila tidak ada pembanding independen, yang bergeser bukan hanya garis pada layar. Mutu produk ikut bergeser keluar dari spesifikasi, dan penyimpangan baru terdeteksi setelah mutu produk telah menurun [1].',
            ]},
            {"h": 'Sampel yang mewakili: titik, wadah, dan label waktu', "t": 20, "paras": [
                'Pengambilan sampel yang benar dimulai dari titik sampel yang memang dirancang pada pipa, bukan dari keran mana pun yang tersedia. Cairan pertama dibuang terlebih dahulu agar yang masuk ke botol adalah fluida yang segar dari aliran, kemudian botol ditutup rapat, terutama apabila komponennya mudah menguap.',
                'Setiap botol diberi label waktu. Detail ini menentukan nilai hasil laboratorium: angka laboratorium harus dapat dipasangkan dengan kondisi proses pada jam yang sama, bukan dibandingkan dengan bacaan sensor dari waktu yang berbeda [1].',
            ]},
            {"h": 'Laboratorium sebagai pembanding independen', "t": 27, "paras": [
                'Di laboratorium, sampel diukur dengan metode yang terkalibrasi terhadap standar, misalnya titrasi atau spektrofotometri. Hasilnya merupakan angka independen yang tidak mewarisi kesalahan sensor lapangan [2].',
                'Hasil laboratorium tersebut kemudian dibandingkan dengan bacaan sensor pada waktu yang sama. Apabila keduanya sesuai, sensor terbukti akurat. Apabila selisihnya melewati batas, tindak lanjutnya adalah kalibrasi atau pemeriksaan proses, bukan membiarkan selisih itu membesar tanpa terdeteksi.',
            ]},
            {"h": 'Mengapa tidak semua pengukuran digantikan sensor', "t": None, "paras": [
                'Tidak semua variabel memiliki sensor inline yang andal dan ekonomis, dan setiap titik ukur tambahan menambah biaya pemasangan serta perawatan. Selama mutu produk harus dibuktikan melalui pengukuran langsung atas bahannya, sampel fisik ke laboratorium tetap menjadi rujukan yang tidak tergantikan [1].',
            ]},
        ],
        "refs": [
            "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.",
            'Skoog, D. A., West, D. M., Holler, F. J., & Crouch, S. R. (2014). Fundamentals of Analytical Chemistry (9th ed.). Cengage Learning.',
        ]},
    'shift-handover-logbook': {
        "lead": 'Peralatan tidak berubah pada saat shift berganti. Yang berubah adalah orangnya, dan pada celah pergantian itulah riwayat peralatan paling sering hilang.',
        "sections": [
            {"h": 'Layar menampilkan angka, logbook menyimpan riwayat', "t": 6, "paras": [
                'Sistem kontrol menampilkan angka proses: suhu, tekanan, level, dan laju alir. Yang tidak tampil di sana adalah konteks kualitatif peralatan, misalnya katup V-204 yang rembes dan harus dipantau setiap jam, bunyi pompa yang berubah, atau perbaikan sementara yang sedang berjalan.',
                'Detail semacam itu tidak memiliki kolom pada layar angka. Ia hanya hidup apabila dituliskan, dan logbook adalah tempat pabrik merekam ingatan proses di antara pergantian shift [1].',
            ]},
            {"h": 'Mengapa momen pergantian shift paling rawan', "t": 13, "paras": [
                'Serah terima merupakan perpindahan informasi antara dua orang yang menghadapi keadaan lapangan yang sama tetapi dengan pemahaman yang berbeda. Operator yang pulang membawa konteks delapan jam terakhir; operator yang datang memulai dari nol. Setiap detail yang tidak terucap atau tidak tertulis akan hilang pada titik ini.',
                'Karena itu, literatur keselamatan proses menempatkan komunikasi shift sebagai salah satu barrier, lapisan pengaman yang sama seriusnya dengan alarm dan interlock [1].',
            ]},
            {"h": 'Tiga langkah serah terima yang benar', "t": 20, "paras": [
                'Urutannya sederhana, tetapi tidak satu pun tahapnya dapat dilewati. Pertama, tuliskan keadaan peralatan apa adanya, termasuk yang tidak normal. Kedua, bacalah catatan itu bersama operator pengganti agar kesalahpahaman terdeteksi pada saat itu juga, bukan setelah kejadian.',
                'Ketiga, lakukan pemeriksaan lapangan berdua. Langkah ini yang paling sering dikorbankan, padahal serah terima tidak selesai di meja control room: katup yang dicatat rembes harus dilihat langsung oleh orang yang akan menjaganya.',
            ]},
            {"h": 'Tanda tangan yang menutup serah terima', "t": 27, "paras": [
                'Serah terima ditutup dengan tanda tangan kedua operator dan stempel waktu. Dari titik itu, tanggung jawab berpindah secara jelas dan dapat ditelusuri: apabila di kemudian hari terjadi suatu kejadian, catatan menunjukkan shift mana yang mengetahui apa, dan kapan [1].',
                'Tanpa bukti tertulis yang ditandatangani, investigasi kejadian berubah menjadi perdebatan berdasarkan ingatan. Dengan logbook, yang diperiksa adalah catatan, bukan klaim.',
            ]},
            {"h": 'Media kertas atau elektronik, prinsipnya tetap sama', "t": None, "paras": [
                'Banyak pabrik kini memakai logbook elektronik, dan hal itu sah. Medianya dapat berubah, prinsipnya tidak: keadaan peralatan ditulis secara spesifik, dibaca bersama oleh kedua shift, diverifikasi di lapangan, kemudian ditutup dengan pengesahan yang dapat ditelusuri [2].',
            ]},
        ],
        "refs": [
            'Center for Chemical Process Safety. (2007). Guidelines for Risk Based Process Safety. AIChE/Wiley.',
            'Health and Safety Executive. (2006). Managing Shift Work: Health and Safety Guidance (HSG256). HSE Books.',
        ]},
    'hilirisasi-nikel-baterai-ev': {
        "lead": 'Bijih nikel Indonesia memiliki kadar hanya sekitar 1 sampai 2 persen. Mengapa bijih tersebut tidak diolah langsung menjadi baterai?',
        "sections": [
            {"h": 'Pemilahan awal: saprolit dan limonit', "t": 6.8, "paras": [
                'Bijih laterit tidak seragam. Profilnya berlapis, dan dua jenis utamanya, saprolit dan limonit, berbeda kadar serta kimia mineralnya. Dengan kadar nikel total hanya sekitar 1 sampai 2 persen, hampir seluruh massa bijih adalah material bukan nikel yang harus disingkirkan melalui proses [1].',
                'Karena itu, keputusan pertama di pabrik bukanlah melebur atau melarutkan, melainkan memilah. Jenis bijih menentukan jalur prosesnya, dan pemilahan yang keliru berarti jalur proses yang keliru.',
            ]},
            {"h": 'Jalur pirometalurgi RKEF untuk saprolit', "t": 13.6, "paras": [
                'Saprolit yang kadarnya relatif lebih tinggi diolah melalui jalur pirometalurgi RKEF: dikeringkan dan dikalsinasi di rotary kiln, kemudian direduksi di electric furnace. Produknya nickel pig iron (NPI), besi kasar yang kaya nikel [1].',
                'NPI merupakan bahan baku stainless steel, bukan bahan baterai. Bentuk kimia dan kadarnya memang dirancang untuk peleburan baja, sehingga rantai baterai tidak dimulai dari sini.',
            ]},
            {"h": 'Jalur hidrometalurgi HPAL untuk limonit', "t": 20.4, "paras": [
                'Limonit yang kadarnya lebih rendah menempuh jalur hidrometalurgi HPAL (high pressure acid leaching). Bijih dilarutkan dengan asam sulfat di dalam autoclave pada sekitar 250°C dan tekanan tinggi, sehingga nikel berpindah dari padatan ke larutan [1].',
                'Angka 250°C di sini adalah kondisi pelarutan, bukan suhu lebur. Pemisahan nikel dilakukan oleh asamnya, dan bejana prosesnya adalah bejana tekan, bukan tungku.',
            ]},
            {"h": 'Dari larutan menjadi MHP dan nikel sulfat', "t": 27.2, "paras": [
                'Larutan nikel dari HPAL tidak langsung menjadi baterai. Nikel diendapkan sebagai MHP (mixed hydroxide precipitate), produk antara yang masih harus dimurnikan lebih lanjut menjadi nikel sulfat, garam dengan kemurnian yang dituntut industri baterai [2].',
                'Nikel sulfat inilah bahan prekursor katoda baterai kendaraan listrik. Dengan demikian, rantai nilainya panjang: bijih, larutan, endapan, garam murni, prekursor, dan akhirnya sel baterai.',
            ]},
            {"h": 'Harga proses yang dibayar: energi, asam, dan tailing', "t": None, "paras": [
                'Kedua jalur tersebut membayar konsekuensi prosesnya masing-masing. RKEF menuntut energi listrik yang besar untuk furnace; HPAL menuntut asam sulfat dalam jumlah besar serta pengelolaan residu atau tailing yang volumenya sangat besar, karena 98 persen lebih massa bijih berakhir bukan sebagai produk [1].',
                'Di situlah nilai hilirisasi sebenarnya diuji: bukan pada bijihnya, melainkan pada kemampuan pabrik memilah, melebur, melarutkan, dan memurnikan dengan biaya proses yang masih dapat diterima.',
            ]},
        ],
        "refs": [
            'Habashi, F. (Ed.). (1997). Handbook of Extractive Metallurgy. Wiley-VCH.',
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Nickel. Wiley-VCH.",
        ]},
    'pasir-jadi-chip-ai': {
        "lead": 'Chip AI paling canggih berawal dari bahan yang sama dengan pasir di pantai. Yang membedakannya bukan bahannya, melainkan kemurniannya.',
        "sections": [
            {"h": 'Reduksi karbotermik: pasir menjadi silikon metalurgi', "t": 6.8, "paras": [
                'Langkah pertama adalah reduksi pasir kuarsa (SiO₂) dengan karbon di furnace listrik: SiO₂ + 2C → Si + 2CO. Produknya silikon metalurgi dengan kemurnian baru sekitar 98 sampai 99 persen [1].',
                'Untuk baja, angka itu sudah cukup. Untuk transistor berukuran nanometer, sisa pengotor sebesar 1 sampai 2 persen terlalu besar, karena sifat listrik semikonduktor ditentukan oleh pengotor pada tingkat yang jauh lebih halus.',
            ]},
            {"h": 'Mengapa harus menjadi gas terlebih dahulu: triklorosilan', "t": 13.6, "paras": [
                'Kunci rekayasa kimianya terletak di sini. Silikon diubah menjadi triklorosilan, senyawa yang mudah menguap. Begitu berbentuk gas, pemisahan pengotor dapat dilakukan dengan distilasi fraksinasi, prinsip yang sama dengan kolom distilasi di kilang minyak [1].',
                'Kata kuncinya adalah mudah menguap: hanya zat yang dapat diuapkan dan diembunkan berulang kali yang dapat dimurnikan sampai tingkat ekstrem melalui perbedaan titik didih.',
            ]},
            {"h": 'Proses Siemens dan arti kemurnian 9N', "t": 20.4, "paras": [
                'Triklorosilan murni diuraikan kembali pada batang silikon panas melalui proses Siemens, menumbuhkan polysilicon dengan kemurnian sekitar 99,9999999 persen, yang ditulis 9N (sembilan angka sembilan) [1].',
                'Chip modern umumnya memakai silikon di rentang 9N sampai 11N. Sebagai gambaran skala: pada 9N, dari satu miliar atom, hanya sekitar satu atom yang bukan silikon.',
            ]},
            {"h": 'Pelelehan 1.414°C, penarikan kristal, dan pemotongan wafer', "t": 27.2, "paras": [
                'Polysilicon dilelehkan pada titik leleh silikon, 1.414°C, kemudian ditarik perlahan menjadi kristal tunggal. Kristal ini dipotong menjadi wafer, umumnya berdiameter 300 mm, dan dari wafer itulah chip AI difabrikasi lapis demi lapis [2].',
                'Urutan lengkapnya menunjukkan peran teknik kimia dari hulu: reaksi reduksi, pemurnian melalui distilasi, dan pertumbuhan kristal. Chip lahir dari proses kimia yang dikendalikan, bukan sekadar dari pasir yang dipotong.',
            ]},
        ],
        "refs": [
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Silicon. Wiley-VCH.",
            'Doering, R., & Nishi, Y. (Eds.). (2007). Handbook of Semiconductor Manufacturing Technology (2nd ed.). CRC Press.',
        ]},
    'distilasi-minyak-mentah': {
        "lead": 'Satu kali pendidihan minyak mentah tidak akan pernah menghasilkan bensin. Campurannya terlalu rapat, dan fisika pemisahannya tidak bekerja dengan cara demikian.',
        "sections": [
            {"h": 'Campuran ratusan hidrokarbon, bukan zat tunggal', "t": 6.5, "paras": [
                'Minyak mentah adalah campuran ratusan senyawa hidrokarbon dengan titik didih yang berdekatan dan bertumpuk. Satu kali pendidihan hanya menghasilkan uap yang komposisinya tetap berupa campuran, karena fraksi ringan dan berat menguap bersamaan [1].',
                'Oleh karena itu, umpan dipanaskan hingga sekitar 350°C di fired heater, kemudian masuk ke zona flash di kolom, titik awal uap dan cairan mulai berpisah. Dari titik ini, pemisahan diselesaikan bukan oleh satu pendidihan, melainkan oleh kontak berulang.',
            ]},
            {"h": 'Kontak uap dan cairan yang berulang di tray', "t": 13, "paras": [
                'Di dalam kolom, uap naik dan cairan turun melewati tray-tray. Pada setiap tray, uap dan cairan berkontak dan saling bertukar komponen: komponen yang ringan cenderung lanjut menguap, sedangkan yang berat mengembun dan turun.',
                'Satu kolom pada dasarnya adalah rangkaian banyak tahap kesetimbangan yang ditumpuk secara vertikal. Pengulangan kontak inilah mesin pemisahnya, dan inilah yang tidak dapat digantikan oleh satu kali rebusan [1][2].',
            ]},
            {"h": 'Reflux: faktor penentu ketajaman pemisahan', "t": 19.5, "paras": [
                'Uap paling ringan keluar dari puncak kolom, didinginkan di kondenser, ditampung di reflux drum, kemudian sebagian dikembalikan ke kolom sebagai reflux. Cairan yang kembali ini membasahi tray-tray atas dan mempertemukan uap yang naik dengan cairan yang lebih murni.',
                'Tanpa reflux, produk atas tercemar fraksi yang lebih berat. Reflux yang dikembalikan bukan pemborosan, melainkan harga untuk ketajaman pemisahan [2].',
            ]},
            {"h": 'Profil suhu dan produk per tingkat', "t": 26.5, "paras": [
                'Karena campuran mengembun dan menguap secara bertingkat, suhu kolom membentuk gradien: sekitar 120°C di puncak dan 350°C di dasar yang dipanaskan reboiler. Produk diambil pada tingkat yang suhunya sesuai dengan titik didihnya, dari gas paling ringan di atas sampai residu paling berat di bawah [1].',
                'Urutan produknya mengikuti titik didih, bukan jenis zat yang direaksikan. Distilasi adalah pemisahan fisik berdasarkan volatilitas; tidak ada molekul yang diubah menjadi molekul lain di dalam kolom.',
            ]},
        ],
        "refs": [
            'Seader, J. D., Henley, E. J., & Roper, D. K. (2016). Separation Process Principles (4th ed.). Wiley.',
            'Kister, H. Z. (1992). Distillation Design. McGraw-Hill.',
        ]},
    'process-safety-bukan-apd': {
        "lead": 'Helm dan sarung tangan tidak menghentikan vessel yang pecah. Kecelakaan proses berskala besar dicegah jauh sebelum bahayanya terlepas.',
        "sections": [
            {"h": 'Dua jenis kecelakaan yang sering dicampur', "t": 6.8, "paras": [
                'Kecelakaan personal seperti terpeleset, terjepit, atau tersiram dalam skala kecil adalah wilayah APD, dan APD memang efektif di sana. Process safety menyasar kejadian yang berbeda kelas: pelepasan bahan atau energi berbahaya dalam skala besar dari vessel, pipa, dan reaktor bertekanan [1].',
                'Pada pelepasan besar, yang menentukan keselamatan bukanlah helm pekerja, melainkan apakah pelepasan tersebut dicegah sejak dari desain dan operasi prosesnya.',
            ]},
            {"h": 'Hazard, risk, dan dua komponen risk', "t": 13.6, "paras": [
                'Hazard adalah potensi bahayanya: bahan mudah terbakar, tekanan tinggi, dan suhu ekstrem. Risk adalah gabungan dua komponen, yaitu seberapa parah konsekuensinya dan seberapa mungkin kejadian itu terjadi [1].',
                'Menyederhanakan risk menjadi sekadar keberadaan bahaya membuat prioritas pengamanan salah arah. Dua bahaya yang sama dapat menuntut perlakuan berbeda karena kemungkinan dan konsekuensinya berbeda.',
            ]},
            {"h": 'Barrier berlapis saat tekanan naik', "t": 20.4, "paras": [
                'Pengamanan proses disusun berlapis dan bekerja secara berurutan. Kontrol proses dasar menahan kondisi tetap normal. Apabila gagal, trip otomatis menghentikan proses. Apabila tekanan masih naik, relief valve membuangnya ke sistem tertutup atau flare. Tanggap darurat adalah lapisan terakhir, bukan yang pertama [2].',
                'Urutannya penting: setiap lapisan menangkap kegagalan lapisan sebelumnya, dan lapisan terluar hanya bekerja apabila semua lapisan di dalamnya sudah gagal.',
            ]},
            {"h": 'Syarat independensi dalam perhitungan lapisan', "t": 27.2, "paras": [
                'Ilustrasinya sebagai berikut. Kejadian awal terjadi 1 kali per 10 tahun. Tiga lapisan independen, masing-masing gagal 1 dari 10 kali saat dibutuhkan, membuat frekuensinya menjadi 0,0001 per tahun, atau 1 per 10.000 tahun.',
                'Perkalian itu hanya sah apabila lapisannya benar-benar independen. Apabila satu penyebab yang sama dapat menjatuhkan dua lapisan sekaligus, misalnya sensor yang sama dipakai untuk kontrol dan trip, estimasi keamanannya gugur. Independensi bukan detail administratif, melainkan syarat matematisnya [2].',
            ]},
            {"h": 'APD tetap perlu, tetapi posisinya terakhir', "t": None, "paras": [
                'Process safety tidak membuang APD. APD tetap dipakai setiap hari untuk risiko personal. Bedanya, APD berada di urutan terakhir hierarki pengendalian: ia melindungi orang setelah bahaya terlepas, sedangkan process safety bekerja agar pelepasan itu tidak pernah terjadi [1].',
            ]},
        ],
        "refs": [
            'Crowl, D. A., & Louvar, J. F. (2019). Chemical Process Safety: Fundamentals with Applications (4th ed.). Pearson.',
            'Center for Chemical Process Safety. (2007). Guidelines for Risk Based Process Safety. AIChE/Wiley.',
        ]},
    'heat-exchanger-penghenti-pabrik': {
        "lead": 'Kerak setebal 1 milimeter sanggup memaksa satu unit pabrik berhenti total, dan kerak tersebut menempel justru pada peralatan yang paling sering dianggap sepele.',
        "sections": [
            {"h": 'Panas menyeberang, cairan tidak bertemu', "t": 6.8, "paras": [
                'Heat exchanger bekerja dengan prinsip yang sangat sederhana: dua aliran dipisahkan dinding logam, panas menyeberang melewati dinding, dan kedua cairannya tidak pernah bertemu. Sebagai ilustrasi, aliran panas turun dari 150 ke 90°C, sedangkan aliran dingin naik dari 30 ke 80°C [1].',
                'Kesederhanaan prinsip tersebut dapat menyesatkan. Alat ini menentukan berapa banyak energi yang berhasil dipakai ulang di pabrik, dan energi merupakan salah satu biaya operasi terbesar.',
            ]},
            {"h": 'LMTD: beda suhu penggerak panas', "t": 13.6, "paras": [
                'Laju pindah panas digerakkan oleh beda suhu antara dua aliran, yang berubah di sepanjang alat. Ukuran penggeraknya diringkas sebagai LMTD (log mean temperature difference), beda suhu rata-rata logaritmik antara kedua ujungnya [1].',
                'Di sinilah arah aliran menentukan. Pada konfigurasi searah, beda suhu menyusut tajam di sepanjang alat. Pada lawan arah, beda suhunya terjaga lebih merata dari ujung ke ujung, dan LMTD-nya lebih besar [2].',
            ]},
            {"h": '65 berbanding 44°C: asal angka 48 persen', "t": 20.4, "paras": [
                'Dengan angka ujung yang sama persis (150 ke 90°C dan 30 ke 80°C), lawan arah menghasilkan LMTD sekitar 65°C, sedangkan searah hanya sekitar 44°C. Rasionya 65 per 44, yaitu 1,48.',
                'Artinya, pada luas permukaan yang sama, panas yang dipindahkan dapat menjadi sekitar 48 persen lebih besar hanya dengan membalik arah aliran. Itulah sebabnya heat exchanger industri hampir selalu dirancang lawan arah [1].',
            ]},
            {"h": 'Fouling: kerak, biaya, dan penghentian operasi', "t": 27.2, "paras": [
                'Tantangan terbesarnya adalah fouling, endapan kerak yang tumbuh pada dinding pindah panas. Kerak adalah isolator: ketebalan 1 mm saja sudah memangkas fluks panas sekitar 10 persen, dan alat harus bekerja lebih keras untuk hasil yang sama.',
                'Skala kerugiannya tidak kecil. Literatur fouling mengestimasi biayanya sekitar 0,25 persen PDB negara industri, dan sekitar 186 juta barel minyak per tahun dipakai kilang dunia hanya untuk menambal kerugian akibat fouling. Konsekuensi yang paling mahal adalah penghentian total unit untuk dibersihkan.',
            ]},
            {"h": 'Merancang melawan kerak sejak di kertas', "t": None, "paras": [
                'Karena fouling tidak terhindarkan, perancangan heat exchanger menyisihkan margin berupa faktor pengotoran sejak awal, sebagaimana diatur dalam standar perancangan penukar panas. Alat dirancang sedikit lebih besar dari kebutuhan bersihnya, agar saat kerak tumbuh, pabrik masih memiliki waktu sebelum harus berhenti [3].',
            ]},
        ],
        "refs": [
            'Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2007). Fundamentals of Heat and Mass Transfer (6th ed.). Wiley.',
            'Kern, D. Q. (1950). Process Heat Transfer. McGraw-Hill.',
            'Tubular Exchanger Manufacturers Association. (2019). Standards of the Tubular Exchanger Manufacturers Association (10th ed.). TEMA.',
        ]},
    'haber-bosch-udara-jadi-pupuk': {
        "lead": 'Udara mengandung sekitar 78 persen nitrogen, tetapi tidak ada tanaman yang dapat memanfaatkannya secara langsung. Satu proses industri mengubah gas inert tersebut menjadi sumber nitrogen bagi pangan dunia.',
        "sections": [
            {"h": 'Ikatan rangkap tiga yang sangat stabil', "t": 6.8, "paras": [
                'Reaksinya ringkas: N₂ + 3H₂ → 2NH₃. Atomnya seimbang, 2 nitrogen dan 6 hidrogen di kedua sisi. Kesulitannya bukan pada persamaan, melainkan pada ikatan rangkap tiga pada molekul N₂ yang sangat kuat, yang membuat nitrogen sukar bereaksi [1].',
                'Seluruh rekayasa Haber-Bosch pada dasarnya adalah cara memaksa ikatan itu putus dalam skala industri, secara terus-menerus, dengan biaya yang masih dapat diterima.',
            ]},
            {"h": 'Tiga syarat ekstrem dan tarik-menariknya', "t": 13.6, "paras": [
                'Tiga syarat dipakai bersamaan. Katalis besi membantu memecah ikatan N₂. Suhu 400 sampai 500°C mempercepat reaksi. Tekanan 150 sampai 250 bar mendorong kesetimbangan ke arah produk, karena 4 mol gas berubah menjadi 2 mol gas, sesuai prinsip Le Chatelier [1][2].',
                'Syarat-syarat ini saling bertarik. Suhu tinggi baik untuk kecepatan, tetapi buruk untuk kesetimbangan reaksi eksotermik. Tekanan tinggi baik untuk hasil, tetapi mahal untuk peralatan. Angka operasinya merupakan kompromi di tengah tarik-menarik tersebut.',
            ]},
            {"h": 'Satu lintasan hanya 15 persen: mengapa recycle menentukan', "t": 20.4, "paras": [
                'Sekali campuran gas melewati reaktor, hanya sekitar 15 persen yang berubah menjadi amonia. Amonia kemudian dipisahkan dengan kondensasi, dan gas yang belum bereaksi dikembalikan masuk reaktor.',
                'Tanpa recycle, lebih dari 80 persen bahan baku terbuang pada setiap putaran. Recycle bukan aksesori, melainkan penentu pabrik ini untung atau rugi [1].',
            ]},
            {"h": 'Sifat eksotermik: panas yang membantu sekaligus menghambat', "t": 27.2, "paras": [
                'Reaksinya eksotermik dengan ΔH sekitar minus 92 kJ per mol. Panas yang dilepas membantu menjaga suhu reaktor, tetapi apabila bed katalis terlalu panas, kesetimbangan justru bergeser kembali menjauhi produk.',
                'Karena itu, reaktor amonia dirancang mengelola panasnya sendiri dengan hati-hati, dengan pendinginan di antara tahap-tahap agar konversi per lintasan tetap tinggi tanpa mengorbankan kesetimbangan [1].',
            ]},
            {"h": 'Dari amonia ke urea dan pupuk', "t": None, "paras": [
                'Amonia merupakan produk antara dalam rantai ini. Sebagian besar amonia dunia diolah lebih lanjut menjadi urea dan pupuk nitrogen lain, dan dari sanalah nitrogen dari udara akhirnya sampai ke tanaman. Tanpa proses ini, separuh lebih pangan dunia tidak memiliki sumber nitrogennya [2].',
            ]},
        ],
        "refs": [
            'Appl, M. (1999). Ammonia: Principles and Industrial Practice. Wiley-VCH.',
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Ammonia. Wiley-VCH.",
        ]},
    'netralisasi-asam-basa': {
        "lead": 'Persamaan asam basa yang lazim dipelajari di sekolah menyembunyikan pemeran utamanya. Spesi yang sesungguhnya bereaksi dalam netralisasi ternyata hanyalah dua ion.',
        "sections": [
            {"h": 'Tukar pasangan yang terlihat', "t": 6.5, "paras": [
                'Ditulis sebagai molekul, netralisasi tampak seperti tukar pasangan: HCl + NaOH → NaCl + H₂O. Atom dan muatannya seimbang, dan untuk keperluan praktis persamaan ini benar.',
                'Namun, persamaan molekuler menyembunyikan apa yang sebenarnya terjadi di dalam larutan, karena di dalam air, kedua zat itu sudah tidak berbentuk molekul lagi [1].',
            ]},
            {"h": 'Reaksi ion bersih: H⁺ + OH⁻ → H₂O', "t": 13, "paras": [
                'Asam kuat dan basa kuat terurai sempurna menjadi ion-ionnya di dalam larutan. Dari semua ion yang ada, yang benar-benar bereaksi hanyalah H⁺ + OH⁻ → H₂O. Inilah reaksi ion bersihnya.',
                'Ion Na⁺ dan Cl⁻ tidak berubah dari awal sampai akhir; keduanya merupakan ion penonton yang akhirnya tinggal sebagai garam NaCl di larutan. Persamaan yang panjang ternyata digerakkan oleh satu reaksi ion yang sangat sederhana [1][2].',
            ]},
            {"h": '57 kJ per mol air: dari mana panasnya', "t": 19.5, "paras": [
                'Pembentukan air dari H⁺ dan OH⁻ melepas sekitar 57 kJ panas per mol air yang terbentuk. Reaksinya eksotermik, dan itulah sebabnya wadah campuran terasa hangat saat asam dan basa kuat dicampurkan.',
                'Karena reaksi ionnya selalu sama, entalpi netralisasi asam kuat oleh basa kuat hampir konstan untuk pasangan asam basa kuat mana pun. Yang berubah hanyalah ion penontonnya [2].',
            ]},
            {"h": 'Titrasi: tepat 1 banding 1 dan indikator fenolftalein', "t": 26.5, "paras": [
                'Perbandingan reaksinya tepat 1 banding 1: satu mol HCl membutuhkan tepat satu mol NaOH. Kelebihan satu tetes saja membuat campuran meleset dari titik ekuivalen, yang untuk pasangan asam kuat dan basa kuat berada di pH 7 [1].',
                'Fenolftalein menjadi penanda visualnya: bening di asam, merah muda di basa. Perubahan warnanya menandai kapan penambahan harus berhenti, tetes demi tetes.',
            ]},
            {"h": 'Satu reaksi, banyak skala', "t": None, "paras": [
                'Reaksi yang sama bekerja pada antasida yang menetralkan asam lambung, di laboratorium sekolah saat titrasi, dan di pabrik saat air limbah asam atau basa dinetralkan sebelum dibuang. Skalanya berbeda jauh, reaksi ionnya persis sama [1].',
            ]},
        ],
        "refs": [
            'Skoog, D. A., West, D. M., Holler, F. J., & Crouch, S. R. (2014). Fundamentals of Analytical Chemistry (9th ed.). Cengage Learning.',
            "Atkins, P., & de Paula, J. (2014). Atkins' Physical Chemistry (10th ed.). Oxford University Press.",
        ]},
    'water-gas-shift-co-jadi-h2': {
        "lead": 'Untuk membuat hidrogen murni, pabrik terlebih dahulu menghasilkan CO, gas beracun yang kemudian harus disingkirkan sampai tersisa 0,3 persen.',
        "sections": [
            {"h": 'Hidrogen produk berasal dari air, bukan dari CO', "t": 6.5, "paras": [
                'Reaksi water-gas shift adalah CO + H₂O → CO₂ + H₂, eksotermik dengan ΔH sekitar minus 41 kJ per mol. Reaksi ini adalah tulang punggung pabrik hidrogen karena mengubah CO yang tidak diinginkan menjadi H₂ tambahan [1].',
                'Perlu diluruskan bahwa atom hidrogen pada produk H₂ berasal dari air (steam), bukan dari CO. CO menyumbang karbonnya untuk dibawa pergi sebagai CO₂.',
            ]},
            {"h": 'Tahap suhu tinggi: HTS untuk kecepatan reaksi', "t": 13, "paras": [
                'Tahap pertama adalah HTS (high temperature shift) pada 350 sampai 450°C dengan katalis Fe-Cr. Suhu tinggi membuat reaksi berjalan cepat, dan kadar CO turun dari sekitar 15 persen menjadi 3 persen [1][2].',
                'Sebagian besar pekerjaan selesai pada tahap ini, tetapi 3 persen masih jauh dari cukup bersih untuk hidrogen murni. Menyelesaikan sisanya pada suhu setinggi ini tidak efisien, karena kesetimbangan reaksi eksotermik memburuk saat panas.',
            ]},
            {"h": 'Pendinginan di tengah dan pemulihan panasnya', "t": 19.5, "paras": [
                'Di antara kedua tahap, gas didinginkan. Panas dari reaksi eksotermik tahap pertama tidak dibuang begitu saja, melainkan dipulihkan untuk menghasilkan steam.',
                'Pendinginan ini melayani dua tujuan sekaligus: menyiapkan gas ke suhu tahap kedua yang lebih rendah, dan memulihkan energi reaksinya sebagai utilitas yang berguna [1].',
            ]},
            {"h": 'Tahap suhu rendah: LTS untuk ketuntasan reaksi', "t": 26.5, "paras": [
                'Tahap kedua adalah LTS (low temperature shift) pada 200 sampai 250°C dengan katalis Cu-Zn, menurunkan CO dari 3 persen menjadi 0,3 persen. Katalisnya berbeda karena suhunya berbeda; satu katalis tidak cocok untuk dua rezim suhu ini [1][2].',
                'Setelah CO₂ disingkirkan dan gas dimurnikan melalui PSA, hasilnya adalah hidrogen murni 99,99 persen. Dua tahap reaktor dengan pendingin di tengah merupakan kompromi yang menyelesaikan konflik klasik: kesetimbangan menyukai dingin, kinetika menyukai panas.',
            ]},
        ],
        "refs": [
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Hydrogen. Wiley-VCH.",
            'Newsome, D. S. (1980). The Water-Gas Shift Reaction. Catalysis Reviews: Science and Engineering, 21(2).',
        ]},
    'b40-transesterifikasi-motion': {'lead': 'Empat puluh persen isi tangki solar yang dibeli di SPBU bukan berasal dari minyak bumi. Bagian tersebut berasal dari minyak sawit yang telah diubah secara kimia, dan perubahan kimia itulah syarat agar sawit dapat bercampur dan bekerja sebagai bahan bakar diesel.', 'refs': ['Kementerian Energi dan Sumber Daya Mineral Republik Indonesia. Mandatori B40 mulai 1 Januari 2025.', 'Knothe, G., Krahl, J., & Van Gerpen, J. (Eds.). (2010). The Biodiesel Handbook (2nd ed.). AOCS Press.'], 'sections': [{'h': 'Mandatori B40 dan komposisi 40 berbanding 60', 'paras': ['Sejak Januari 2025, solar yang dijual di Indonesia wajib memenuhi mandatori B40 dari Kementerian ESDM. B40 adalah campuran 40 persen biodiesel berupa FAME dari minyak sawit dan 60 persen solar dari minyak bumi [1].', 'Komposisi ini berarti bahan bakar diesel di SPBU bukan lagi produk satu sumber. Bagian terbesar tetap solar fosil, sedangkan 40 persen sisanya adalah produk reaksi kimia dari minyak nabati yang harus memenuhi mutu campuran yang sama.'], 't': 7}, {'h': 'Mengapa minyak sawit mentah tidak dapat langsung dicampur', 'paras': ['Minyak sawit mentah tersusun atas trigliserida, molekul dengan tiga rantai asam lemak. Trigliserida tersebut terlalu kental dan tidak stabil untuk langsung dituang dan dicampurkan sebagai bahan bakar diesel [2].', 'Persoalannya terletak pada struktur molekulnya, bukan pada asal bahannya. Selama minyak masih berbentuk trigliserida, sifat alir dan kestabilannya tidak sesuai untuk mesin diesel, sehingga molekulnya harus diubah terlebih dahulu.'], 't': 14}, {'h': 'Transesterifikasi: trigliserida dan metanol menjadi FAME dan gliserol', 'paras': ['Perubahan itu dilakukan melalui transesterifikasi: trigliserida direaksikan dengan 3 metanol memakai katalis basa, menghasilkan 3 FAME (fatty acid methyl ester) dan gliserol. FAME inilah biodiesel yang sesungguhnya [2].', 'Reaksi ini memotong tiga rantai asam lemak dari kerangka trigliserida dan memasangkan setiap rantai dengan metanol. Produk sampingnya, gliserol, dipisahkan dari FAME dan mempunyai nilai guna tersendiri sebagai bahan baku sabun dan kosmetik, sebagaimana dicatat dalam materi video.'], 't': 21}, {'h': 'Dari FAME menjadi B40 di tangki pencampur', 'paras': ['FAME yang telah dipisahkan dari gliserol kemudian dicampurkan dengan solar minyak bumi pada perbandingan 40 berbanding 60. Hasil pencampuran inilah B40 yang didistribusikan dan dijual sebagai solar di SPBU [1].', 'Urutan prosesnya menegaskan bahwa B40 bukan campuran minyak sawit mentah dengan solar. Terdapat reaksi kimia penuh di tengahnya, dan tanpa reaksi tersebut, bagian sawit pada campuran tidak akan memenuhi syarat sebagai bahan bakar.'], 't': 28}, {'h': 'Satu tangki solar sebagai hasil reaksi kimia', 'paras': ['Dengan komposisi tersebut, setiap tangki solar yang dibeli konsumen mengandung hasil transesterifikasi dalam jumlah yang besar, yaitu 40 persen dari volumenya [1].', 'Kesimpulan ini mengubah cara membaca kebijakan B40: mandatori tersebut bukan sekadar keputusan pencampuran bahan, melainkan keputusan untuk menjalankan reaksi transesterifikasi trigliserida dalam skala nasional, dengan gliserol sebagai produk samping yang menyertainya [1][2].'], 't': None}]},
    'confined-space-masuk-tangki': {'lead': 'Sebuah tangki yang telah dikosongkan tampak seperti bejana baja yang tidak berbahaya. Namun yang menentukan keselamatan orang yang masuk ke dalamnya bukanlah isi cairannya yang telah hilang, melainkan udara yang tertinggal di dalamnya dan tidak dapat dinilai dengan mata.', 'sections': [{'h': 'Ruang terbatas dan bahaya atmosfer yang tidak terlihat', 't': 6, 'paras': ['Tangki, vessel, dan ruang terbatas sejenis dapat menyimpan sisa uap bahan yang pernah dikandungnya, serta udara dengan kadar oksigen yang tidak cukup untuk menopang pernapasan. Kedua keadaan itu tidak terlihat dari luar: dinding bejana tampak bersih, ruangannya tampak kosong, dan tidak ada tanda visual yang membedakan udara layak napas dari udara yang melumpuhkan [1].', 'Karena bahayanya berada pada atmosfer, penilaiannya tidak dapat digantikan oleh pengalaman atau keberanian. Satu-satunya penilaian yang sah adalah pengukuran, dan pengukuran itu harus dilakukan sebelum ada orang yang berada di dalam ruang tersebut [1][2].']}, {'h': 'Pengujian gas dan ventilasi sebelum masuk', 't': 13, 'paras': ['Pengujian atmosfer dilakukan dengan detektor gas yang diulurkan ke dalam ruang terbatas dari luar, sehingga hasil uji diperoleh sebelum ada pekerja yang menghirup udara di dalamnya. Pengujian dilakukan sebelum masuk dan dilanjutkan selama pekerjaan berlangsung, karena kondisi atmosfer dapat berubah selama pekerjaan berjalan [1].', 'Apabila hasil uji belum layak, ruang tersebut diberi ventilasi untuk mengganti udaranya dengan udara segar sampai pengukuran membuktikan keadaannya aman. Ventilasi bukan jalan pintas untuk melewati pengujian; keduanya berurutan, ventilasi memperbaiki keadaan dan pengujian membuktikannya [1][2].']}, {'h': 'Izin tertulis sebagai gerbang awal pekerjaan', 't': 20, 'paras': ['Pekerjaan masuk ruang terbatas dimulai dari izin tertulis, bukan dari tangga menuju lubang masuk. Izin tersebut memaksa seluruh prasyarat diperiksa dan dinyatakan secara eksplisit sebelum pekerjaan dimulai: isolasi peralatan, pengujian atmosfer, ventilasi, penjaga, dan rencana penyelamatan [1].', 'Fungsi izin bukan administratif semata. Dokumen itu mengubah daftar pengaman dari ingatan seseorang menjadi komitmen tertulis yang dapat diperiksa ulang oleh pihak lain, dan pekerjaan tidak sah dimulai selama satu pun prasyaratnya belum terpenuhi [2].']}, {'h': 'Penjaga di luar dan peran tali penarik', 't': 27, 'paras': ['Selama pekerjaan berlangsung, satu orang bertugas sebagai penjaga di luar ruang terbatas. Penjaga menjaga komunikasi dengan pekerja di dalam, memegang kendali jalur penyelamatan, dan tidak meninggalkan posnya untuk alasan apa pun [1].', 'Pekerja di dalam terhubung dengan tali pengaman ke peralatan penarik seperti tripod di lubang masuk. Susunan ini memungkinkan pekerja yang tidak sadarkan diri ditarik keluar dari luar, tanpa satu pun penolong harus masuk ke atmosfer yang sama [2].']}, {'h': 'Penyelamatan yang tidak menghasilkan korban berikutnya', 't': None, 'paras': ['Pola kecelakaan ruang terbatas yang paling dikenal adalah berantainya korban: pekerja pertama pingsan oleh atmosfer, penolong menyusul masuk tanpa alat napas, dan penolong tersebut pingsan oleh udara yang sama. Rencana penyelamatan disusun sebelum pekerjaan dimulai justru untuk memutus rantai tersebut [1].', 'Kesimpulannya tegas. Ruang terbatas dinyatakan aman bukan karena terlihat kosong, melainkan karena izinnya tertulis, gasnya teruji, udaranya terventilasi, penjaganya berada di luar, dan penyelamatannya telah dirancang tanpa mengorbankan penolong [1][2].']}], 'refs': ["Mannan, S. (Ed.). (2012). Lees' Loss Prevention in the Process Industries: Hazard Identification, Assessment and Control (4th ed.). Butterworth-Heinemann.", "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."]},
    'dead-leg-pipa-buntu-berbahaya': {'lead': 'Cabang pipa yang tidak pernah dialiri tampak seperti bagian yang paling aman di pabrik, karena tidak ada aliran, tidak ada tekanan yang berubah, dan tidak ada proses yang berjalan di dalamnya. Penilaian tersebut terbalik: keadaan diam di dalam cabang itulah yang menjadi sumber bahayanya.', 'refs': ['Towler, G., & Sinnott, R. (2013). Chemical Engineering Design: Principles, Practice and Economics of Plant and Process Design (2nd ed.). Butterworth-Heinemann.', 'Revie, R. W., & Uhlig, H. H. (2008). Corrosion and Corrosion Control: An Introduction to Corrosion Science and Engineering (4th ed.). Wiley-Interscience.', 'Chemical Processing. Watch Out For Dead-Legs.'], 'sections': [{'h': 'Definisi dead leg: cabang tanpa aliran', 'paras': ['Dead leg adalah cabang pipa buntu yang tidak dialiri, sehingga fluida di dalamnya stagnan. Cabang semacam ini lazim muncul sebagai sisa perubahan desain, jalur cadangan yang tidak pernah dipakai, atau sambungan untuk keperluan yang telah dihapus, sedangkan pipanya tetap tertinggal pada sistem [1].', 'Karena tidak ada aliran yang melewatinya, cabang tersebut luput dari perhatian operasi sehari-hari. Fluida yang terperangkap di dalamnya tidak berganti, dan kondisinya tidak terpantau oleh instrumen pada aliran utama.'], 't': 6}, {'h': 'Korosi dan endapan pada fluida yang stagnan', 'paras': ['Keadaan stagnan mempercepat korosi setempat pada dinding pipa dan mendukung pertumbuhan mikroba pada dinding tersebut. Tanpa aliran, produk korosi dan endapan tidak terbawa pergi, melainkan menumpuk di dasar dan dinding cabang [2].', 'Penumpukan ini berjalan perlahan dan tidak terlihat dari luar. Cabang yang dari luar tampak utuh dapat menyimpan lapisan karat dan endapan dalam jumlah yang terus bertambah selama cabang tersebut dibiarkan tanpa aliran dan tanpa pembilasan.'], 't': 13}, {'h': 'Aturan praktis panjang terhadap diameter', 'paras': ['Risiko dead leg berkaitan dengan seberapa dalam cabang menjulur dari aliran utama. Aturan praktis perlindungan korosi yang dikutip dalam materi video menyatakan bahwa cabang dari jalur beraliran dengan rasio panjang terhadap diameter (L/D) melebihi 3 kemungkinan besar bermasalah [3].', 'Makna aturan tersebut bersifat desain: semakin panjang cabang relatif terhadap diameternya, semakin dalam zona stagnannya dan semakin kecil kemungkinan ujung cabang tersentuh pertukaran fluida dengan aliran utama. Cabang pendek jauh lebih mudah dijaga dibandingkan cabang panjang.'], 't': 13}, {'h': 'Momen pelepasan: kontaminan terdorong ke aliran utama', 'paras': ['Bahaya dead leg muncul pada saat kondisi berubah. Ketika katup dibuka atau aliran dialihkan, fluida pada aliran utama mulai bergerak melewati mulut cabang dan menyeret isi cabang yang telah lama stagnan [1].', 'Karat, endapan, dan fluida yang telah berubah komposisinya ikut terdorong masuk ke aliran utama dan mengotori produk. Dengan demikian, cabang yang selama ini dianggap tidak berperan justru menentukan mutu aliran pada saat sistem dioperasikan kembali.'], 't': 20}, {'h': 'Penyelesaian dari desain dan pembilasan berkala', 'paras': ['Penyelesaian yang diutamakan adalah penyelesaian desain: cabang buntu dihindari sejak perancangan dan cabang yang tidak lagi diperlukan dilepas dari sistem. Apabila keberadaan cabang tidak dapat dihindari, cabang dibuat sesingkat mungkin agar zona stagnannya sekecil mungkin [1][3].', 'Untuk cabang yang terpaksa dipertahankan, pembilasan berkala menjadi kewajiban perawatan: fluida di dalam cabang digerakkan dan diganti secara terjadwal, sehingga korosi setempat, endapan, dan pertumbuhan mikroba tidak dibiarkan menumpuk tanpa terdeteksi [1].'], 't': 27}]},
    'flare-stack-api-kilang-menyala': {'lead': 'Api di ujung cerobong tertinggi sebuah kilang menyala siang dan malam, dan dari kejauhan api itu tampak seperti gas yang dibakar tanpa hasil. Penilaian tersebut keliru pada satu hal mendasar: yang dibakar di sana bukan produk yang gagal dijual, melainkan gas berlebih yang memang harus dikeluarkan dari sistem demi keselamatan.', 'sections': [{'h': 'Sumber gas flare: katup pengaman, blowdown, dan pelepasan operasi', 't': 13, 'paras': ['Gas yang tiba di flare berasal dari beberapa jalur yang semuanya bersifat pengaman. Katup pengaman melepas gas ketika tekanan sistem naik melewati batasnya, blowdown mengosongkan tekanan peralatan secara terkendali, dan pelepasan juga terjadi pada saat penyalaan atau penghentian operasi, ketika keadaan proses belum atau tidak lagi stabil [1].', 'Pada semua jalur itu, alternatifnya bukanlah menyimpan gas tersebut lebih lama. Tekanan berlebih yang ditahan di dalam peralatan bertekanan merupakan bahaya mekanis langsung, sehingga gas wajib keluar dari sistem. Persoalan rekayasanya bukan apakah gas dikeluarkan, melainkan dalam bentuk apa gas itu tiba di udara [1][2].']}, {'h': 'Knockout drum: memisahkan cairan sebelum gas naik', 't': 20, 'paras': ['Aliran dari sistem tidak langsung naik ke ujung flare. Aliran tersebut melewati knockout drum, bejana pemisah yang menahan cairan yang terbawa bersama gas, sehingga hanya fase gas yang melanjutkan perjalanan ke flare stack [1].', 'Pemisahan ini penting karena cairan yang terbawa sampai ke ujung flare akan terbakar sebagai tetesan jatuh dan membahayakan area di bawahnya. Knockout drum memastikan pembakaran di ujung stack terjadi pada fase yang memang dirancang untuk dibakar di sana, yaitu gas [1][2].']}, {'h': 'Mengapa dibakar, bukan dilepas mentah', 't': 27, 'paras': ['Flare menjawab persoalan tersebut dengan pembakaran. Gas hidrokarbon yang dialirkan ke ujung flare dibakar menjadi karbon dioksida dan uap air, sehingga yang dilepas ke atmosfer adalah hasil pembakaran, bukan hidrokarbon mentah yang belum terbakar [1].', 'Praktik sistem pelepas tekanan dan flare ini diatur dalam rekomendasi praktik API RP 521, yang menjadi rujukan perancangan sistem pelepas tekanan dan penurun tekanan pada fasilitas proses. Di dalam kerangka itu, flare bukan aksesori cerobong, melainkan ujung dari sistem pengaman tekanan keseluruhan [2].']}, {'h': 'Pilot burner: api kecil yang tidak boleh padam', 't': 27, 'paras': ['Di ujung flare terdapat pilot burner, api kecil yang dijaga menyala terus-menerus. Fungsinya adalah menjamin penyalaan: pada saat gelombang gas berlebih tiba, yang kedatangannya tidak terjadwal, api penyala harus sudah tersedia pada detik itu juga [2].', 'Apabila pilot padam, gas yang tiba tidak terbakar dan lolos mentah ke udara, tepat pada keadaan yang seharusnya dicegah oleh flare. Karena itu keberlangsungan api kecil ini sama pentingnya dengan besarnya api utama, dan pemantauannya merupakan bagian dari operasi flare itu sendiri [1].']}, {'h': 'Alat pengaman terakhir pada sistem tekanan', 't': None, 'paras': ['Disebut alat pengaman terakhir karena flare bekerja pada ujung rangkaian pengaman tekanan. Ketika pengendalian normal tidak lagi cukup dan katup pengaman telah melepas gas, flare adalah tahap yang memastikan pelepasan tersebut berakhir sebagai pembakaran terkendali di ketinggian, bukan sebagai awan hidrokarbon mentah [2].', 'Maka api yang menyala terus di kilang dibaca secara terbalik dari kesan pertamanya. Api itu bukan tanda pemborosan, melainkan tanda bahwa jalur pengaman terakhir kilang dalam keadaan siap, dan kesiapan itulah yang tidak boleh padam [1][2].']}], 'refs': ['American Petroleum Institute. (2020). API Recommended Practice 521: Pressure-Relieving and Depressuring Systems (7th ed.). API Publishing Services.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."]},
    'gudang-bahan-kimia-segregasi-bunding': {'lead': 'Dua drum yang diletakkan bersebelahan di gudang tampak seperti persoalan kerapian. Apabila isi kedua drum itu tidak kompatibel, kedekatan tersebut adalah jalur kejadian: satu kebocoran kecil sudah cukup untuk mempertemukan keduanya tanpa campur tangan siapa pun.', 'sections': [{'h': 'Inkompatibilitas pertama: asam dan pemutih menghasilkan gas klorin', 't': 6.5, 'paras': ['Pemutih berbahan natrium hipoklorit adalah bahan rumah tangga dan industri yang umum, dan asam adalah bahan korosif yang sama umumnya. Apabila keduanya tercampur, reaksi yang terjadi melepaskan gas klorin, gas beracun yang membahayakan pernapasan orang di sekitarnya [1].', 'Kejadian semacam ini tidak memerlukan kesalahan pencampuran yang disengaja. Drum asam yang menetes ke arah drum pemutih yang bersebelahan sudah merupakan pencampuran, dan gasnya terbentuk di tempat bahan itu bertemu, di lantai gudang yang sama [2].']}, {'h': 'Inkompatibilitas kedua: oksidator dan bahan mudah terbakar', 't': 13, 'paras': ['Pasangan berbahaya kedua bekerja melalui jalur yang berbeda. Bahan oksidator menyediakan oksigen bagi pembakaran, sehingga apabila oksidator tercampur atau tersimpan menempel dengan bahan mudah terbakar, pasangan tersebut dapat memicu kebakaran dengan energi penyalaan yang jauh lebih kecil daripada bahan mudah terbakar yang berdiri sendiri [1].', 'Kedua contoh ini memperlihatkan prinsip yang sama dari dua sisi. Bahaya gudang kimia tidak hanya ditentukan oleh sifat setiap bahan secara sendiri, melainkan juga oleh bahan apa yang berada di sebelahnya. Penilaian penyimpanan karena itu selalu berpasangan, bukan per bahan [1][2].']}, {'h': 'Segregasi: zonasi gudang berdasarkan kelas bahaya', 't': 20, 'paras': ['Jawaban rekayasanya adalah segregasi, yaitu pemisahan isi gudang berdasarkan kompatibilitas. Bahan dikelompokkan ke dalam zona menurut kelas bahayanya, antara lain zona mudah terbakar, zona korosif, dan zona oksidator, dan setiap zona dipisahkan oleh jarak serta pembatas fisik dari zona lainnya [1].', 'Klasifikasi bahaya yang menjadi dasar pengelompokan ini mengikuti sistem klasifikasi dan pelabelan bahan kimia yang terharmonisasi secara global, sehingga label pada setiap kemasan memberikan informasi kelas bahaya yang sama di pabrik mana pun. Label tersebut bukan hiasan kemasan; label itulah yang menentukan zona tempat bahan boleh disimpan [1].']}, {'h': 'Bunding sebagai pertahanan lapis kedua', 't': 27, 'paras': ['Segregasi mengasumsikan bahan tetap berada di zonanya, dan bunding disiapkan untuk keadaan apabila asumsi itu gagal. Bunding adalah tanggul penampung yang mengelilingi area penyimpanan, dirancang menahan cairan yang tumpah agar tetap berada di dalam area tersebut [2].', 'Dengan tumpahan tertahan di zonanya, satu kebocoran tidak berubah menjadi pertemuan antar bahan yang tidak kompatibel di zona lain. Segregasi mencegah pertemuan dalam keadaan normal, sedangkan bunding membatasi akibatnya dalam keadaan bocor; keduanya merupakan dua lapis pertahanan yang berbeda dan tidak saling menggantikan [2].']}, {'h': 'Aturan praktis sebelum menyimpan bahan apa pun', 't': None, 'paras': ['Urutan keputusan di gudang kimia karena itu tetap. Pertama, periksa kompatibilitas bahan terhadap isi zona tempat bahan akan disimpan, berdasarkan kelas bahaya pada labelnya. Kedua, simpan bahan hanya di zona yang sesuai dengan kelasnya [1].', 'Ketiga, pastikan area penyimpanan tersebut memiliki bunding yang mampu menahan tumpahan. Gudang yang mengikuti ketiga aturan ini tidak lagi bergantung pada keberuntungan bahwa tidak ada drum yang menetes [1][2].']}], 'refs': ['United Nations. (2019). Globally Harmonized System of Classification and Labelling of Chemicals (GHS) (8th revised ed.). United Nations.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."]},
    'hybrid-pompa-sentrifugal': {'lead': 'Pompa sentrifugal dipahami secara keliru sebagai alat yang menghisap cairan dari sisi masuknya. Mekanisme sebenarnya berjalan terbalik: cairan terlebih dahulu dilempar ke luar, dan lemparan tersebut yang kemudian menghasilkan tekanan untuk mendorong cairan sampai ke tangki yang lebih tinggi.', 'refs': ["Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.", 'Karassik, I. J., Messina, J. P., Cooper, P., & Heald, C. C. (2008). Pump Handbook (4th ed.). McGraw-Hill.', 'Coulson, J. M., & Richardson, J. F. (1999). Chemical Engineering, Volume 1: Fluid Flow, Heat Transfer and Mass Transfer (6th ed.). Butterworth-Heinemann.'], 'sections': [{'h': 'Lemparan impeller dan peran tekanan atmosfer pada sisi masuk', 'paras': ['Impeller adalah komponen berputar di jantung pompa sentrifugal. Pada saat impeller berputar, cairan yang berada di antara sudu sudunya ikut terlempar ke arah luar oleh gerak putar tersebut, meninggalkan daerah bertekanan lebih rendah di bagian tengah impeller [1][2].', 'Penurunan tekanan di tengah inilah yang membuka jalan bagi cairan berikutnya. Tekanan atmosfer yang menekan permukaan cairan di tangki sumber mendorong cairan masuk menuju daerah bertekanan rendah tersebut. Pompa tidak menarik cairan dari kejauhan; tekanan dari luar yang mendorong cairan masuk [2].'], 't': 0}, {'h': 'Mengapa air tetap dapat naik menuju tangki atas', 'paras': ['Pertanyaan yang wajar muncul dari penjelasan tersebut adalah mengenai kemampuan pompa menaikkan air ke tangki atas apabila alat ini tidak menghisap. Jawabannya terletak pada sisi keluar pompa, bukan pada sisi masuknya.', 'Cairan yang terlempar keluar impeller membawa kecepatan tinggi. Kecepatan tersebut kemudian diubah menjadi tekanan, dan tekanan inilah yang mendorong cairan melalui pipa discharge menuju ketinggian yang lebih besar. Kenaikan air dijelaskan oleh tekanan yang dihasilkan, bukan oleh hisapan pada sisi masuk [1][2].'], 't': 6.5}, {'h': 'Masuk secara axial dari tengah dan keluar secara radial', 'paras': ['Arah aliran di dalam pompa memiliki pola yang tetap. Cairan masuk secara axial melalui suction, yaitu sejajar dengan poros dan menuju tengah impeller, kemudian berubah arah dan keluar secara radial, tegak lurus terhadap poros, melalui discharge [1][2].', 'Perubahan arah tersebut bukan detail geometri semata. Aliran masuk secara axial diterima di tengah, dipercepat oleh putaran impeller dalam arah radial, dan diarahkan keluar dengan energi kinetik yang jauh lebih besar dari energi pada saat masuk.'], 't': 13}, {'h': 'Volute: perubahan kecepatan menjadi tekanan', 'paras': ['Setelah meninggalkan impeller, cairan memasuki volute, saluran berbentuk spiral yang mengelilingi impeller dan luas penampangnya melebar secara bertahap. Pelebaran saluran membuat kecepatan aliran turun secara bertahap [2][3].', 'Penurunan kecepatan pada saluran yang melebar disertai kenaikan tekanan, sesuai kekekalan energi aliran: energi kinetik yang berkurang berubah menjadi energi tekanan. Tekanan pada discharge inilah hasil akhir pompa, yaitu besaran yang dipakai untuk melawan ketinggian dan tahanan pipa [3].'], 't': 20}, {'h': 'Hukum afinitas dan contoh kenaikan putaran dua kali', 'paras': ['Hubungan antara putaran dan kinerja pompa diringkas oleh hukum afinitas untuk pompa yang sama: laju alir Q sebanding dengan putaran N, head H sebanding dengan N kuadrat, dan daya P sebanding dengan N pangkat tiga [1][2]. Perbandingan tersebut berlaku pada titik operasi yang sebanding dan menunjukkan ketimpangan yang besar antara kenaikan putaran dan kenaikan daya.', 'Contoh terhitung pada video memakai basis putaran 1.450 rpm dengan Q sebesar 100 m3/jam, H sebesar 30 m, dan P sebesar 15 kW. Pada putaran 2.900 rpm, yaitu dua kali basisnya, Q menjadi 200 m3/jam atau dua kali, H menjadi 120 m atau empat kali, dan P menjadi 120 kW atau delapan kali. Daya naik delapan kali untuk putaran yang hanya naik dua kali adalah konsekuensi yang wajib diperhitungkan sebelum putaran pompa diubah.'], 't': 27}, {'h': 'Syarat terisi cairan: pompa sentrifugal tidak memancing aliran dari keadaan kering', 'paras': ['Seluruh mekanisme lemparan mensyaratkan impeller terisi cairan. Pompa sentrifugal tidak dapat menghisap sendiri dari keadaan kering atau tidak bersifat self-priming, karena impeller yang berputar di dalam udara tidak menghasilkan penurunan tekanan yang cukup untuk memulai aliran [2].', 'Karena itu, pengoperasian dimulai dari keadaan terisi atau primed. Setelah cairan berada di dalam pompa, lemparan impeller menurunkan tekanan di tengah dan tekanan atmosfer mengambil peran mendorong cairan berikutnya masuk, sebagaimana dijelaskan pada bagian awal artikel ini.'], 't': None}]},
    'hybrid-shell-and-tube-heat-exchanger': {'lead': 'Dua fluida dapat saling bertukar energi tanpa satu tetes pun berpindah di antara keduanya. Penjelasan atas peristiwa tersebut terletak pada sebuah dinding logam dan pada susunan aliran yang dirancang dengan cermat di dalam penukar panas shell and tube.', 'refs': ['Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2007). Fundamentals of Heat and Mass Transfer (6th ed.). Wiley.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.", 'Kern, D. Q. (1950). Process Heat Transfer. McGraw-Hill.'], 'sections': [{'h': 'Pemanfaatan panas sisa untuk memanaskan minyak mentah', 'paras': ['Sebelum masuk kolom distilasi, minyak mentah harus dipanaskan terlebih dahulu. Pemanasan tersebut dapat memanfaatkan panas produk yang keluar dari proses dalam keadaan panas, sehingga energi yang telah dibayar sebagai bahan bakar tidak terbuang sebagai panas sisa [2].', 'Rangkaian pemanfaatan ini dikenal sebagai preheat train. Di dalam rangkaian tersebut, penukar panas menjadi perantara: produk panas menyerahkan sebagian energinya kepada minyak mentah dingin, dan kedua aliran melanjutkan perjalanannya ke tujuan masing-masing.'], 't': 6.5}, {'h': 'Dua aliran yang terpisah oleh dinding pipa', 'paras': ['Di dalam penukar panas shell and tube, fluida panas mengalir di dalam pipa pipa yang disebut sisi tube, sedangkan fluida dingin mengalir di dalam shell dan mengelilingi bagian luar pipa. Kedua fluida tidak bercampur pada titik mana pun di dalam alat [1][3].', 'Perpindahan panas berlangsung melalui dinding pipa. Energi bergerak dari fluida panas menuju dinding, melintasi ketebalan logam, kemudian berpindah ke fluida dingin di sisi seberang. Yang melintasi dinding adalah energi dalam bentuk panas, bukan fluida itu sendiri [1].'], 't': 13}, {'h': 'Sekat yang memaksa aliran sisi shell berbelok', 'paras': ['Ruang shell dilengkapi sekat atau baffle, pelat yang dipasang melintang di antara berkas pipa. Sekat memaksa aliran sisi shell berbelok dalam lintasan zigzag, bukan mengalir lurus dari ujung ke ujung alat [1][3].', 'Lintasan yang berbelok memiliki dua akibat yang saling berkaitan. Jalur aliran menjadi lebih panjang sehingga waktu kontak dengan permukaan pipa bertambah, dan turbulensi aliran meningkat sehingga lapisan fluida di dekat dinding terus diperbarui. Kedua akibat tersebut memperkuat perpindahan panas ke pipa.'], 't': 20}, {'h': 'Contoh hitungan: keseimbangan energi sebesar 1.200 kW', 'paras': ['Contoh hitungan pada video memakai dua aliran minyak dengan kalor jenis 2,0 kJ/kg °C. Aliran panas sebesar 10 kg/detik turun dari 180 °C menjadi 120 °C, sedangkan aliran dingin sebesar 12 kg/detik naik dari 40 °C menjadi 90 °C. Contoh ini dilabeli sebagai contoh hitungan, bukan data operasi suatu pabrik tertentu [1].', 'Energi yang dilepas aliran panas adalah 10 dikali 2,0 dikali 60, yaitu 1.200 kW. Energi yang diterima aliran dingin adalah 12 dikali 2,0 dikali 50, yaitu 1.200 kW pula. Kesamaan kedua hasil tersebut adalah syarat keseimbangan energi: panas yang dilepas satu aliran sama dengan panas yang diterima aliran lainnya.'], 't': 27}, {'h': 'Beda suhu rata rata logaritmik sekitar 85 °C pada arus berlawanan', 'paras': ['Pada susunan arus berlawanan, selisih suhu di kedua ujung alat adalah 90 °C dan 80 °C. Beda suhu penggerak perpindahan panas diringkas sebagai beda suhu rata rata logaritmik atau LMTD, yang untuk kedua ujung tersebut dihitung sebagai (90 dikurangi 80) dibagi ln(90/80), yaitu 84,9 atau sekitar 85 °C [1].', 'Nilai LMTD adalah ukuran kekuatan pendorong perpindahan panas di sepanjang alat. Pembaca dapat menghitung ulang nilai tersebut pada kalkulator LMTD di website ilmutekkim dengan memasukkan suhu masuk dan keluar kedua aliran dari contoh yang sama.'], 't': 27}]},
    'loto-gembok-pribadi-motion': {'lead': 'Menekan saklar ke posisi mati menghentikan perintah operasi mesin, tetapi tidak menghapus energi yang telah tersimpan di dalamnya. Dari celah antara dua keadaan inilah prosedur lockout dan tagout atau LOTO memperoleh maknanya.', 'refs': ['Occupational Safety and Health Administration. 29 CFR 1910.147: The Control of Hazardous Energy (Lockout/Tagout). U.S. Department of Labor.', 'Occupational Safety and Health Administration. Fact Sheet: Lockout/Tagout. U.S. Department of Labor.', 'Crowl, D. A., & Louvar, J. F. (2019). Chemical Process Safety: Fundamentals with Applications (4th ed.). Pearson.'], 'sections': [{'h': 'Energi tersimpan yang tetap ada setelah mesin berhenti', 'paras': ['Mesin yang telah dimatikan tetap dapat menyimpan energi dalam beberapa bentuk. Muatan listrik tertahan di kapasitor, tekanan tertahan di sistem hidrolik dan pneumatik, pegas tertahan dalam keadaan tertekan, dan beban yang tergantung tertahan oleh gravitasi pada posisi terangkat [1].', 'Standar OSHA mengelompokkan energi yang wajib dikendalikan sebagai energi listrik, mekanik, hidrolik, pneumatik, kimia, dan termal [1][3]. Penghentian operasi hanya menutup satu jalur, yaitu perintah untuk bergerak; pengendalian energi harus menutup seluruh jalur pelepasan yang masih tersedia.'], 't': 6}, {'h': 'Risiko kedua: penyalaan kembali oleh orang lain', 'paras': ['Bahaya selama perawatan tidak hanya berasal dari mesin itu sendiri. Pekerja lain yang tidak mengetahui bahwa perawatan sedang berlangsung dapat menyalakan kembali peralatan dari panel yang sama, dan energi mengalir ke area tempat teknisi sedang bekerja.', 'Risiko ini menjelaskan mengapa pengamanan tidak cukup berupa pengamatan atau pengumuman lisan. Diperlukan penghalang fisik berupa kunci pada titik isolasi, disertai penanda yang menyatakan bahwa peralatan tidak boleh dioperasikan [1].'], 't': 13}, {'h': 'Isolasi, pemasangan kunci, dan pemasangan tag', 'paras': ['Urutan pengendalian menurut OSHA 29 CFR 1910.147 dimulai dari persiapan dan penghentian mesin, dilanjutkan isolasi peralatan dari sumber energinya [1]. Pada titik isolasi kemudian dipasang kunci (lock) dan tag peringatan, sehingga saklar atau katup tidak dapat dikembalikan ke posisi operasi.', 'Kunci yang dipakai adalah gembok pribadi. Setiap pekerja memasang gemboknya sendiri pada titik isolasi bersama, dan kunci gembok tersebut hanya dipegang oleh pemiliknya. Dengan susunan ini, tidak ada satu orang pun yang dapat membuka pengaman pekerja lain [1].'], 't': 20}, {'h': 'Pelepasan energi tersimpan dan verifikasi isolasi', 'paras': ['Setelah peralatan dikunci, energi yang tersimpan harus dilepaskan atau ditahan secara aman: tekanan dibuang, muatan listrik dikosongkan, dan bagian yang tertekan dikembalikan ke keadaan tanpa energi. Tahap ini menutup celah yang tidak terselesaikan oleh penguncian titik isolasi [1].', 'Urutan ditutup dengan verifikasi isolasi, yang dalam praktik dilakukan dengan mencoba mengoperasikan peralatan. Mesin harus tetap diam. Percobaan tersebut bukan formalitas, melainkan pembuktian bahwa isolasi, penguncian, dan pelepasan energi telah bekerja sebagai satu kesatuan [1][3].'], 't': 27}, {'h': 'Gembok pribadi dan dampak kepatuhan pada prosedur', 'paras': ['Aturan pelepasan kunci menegaskan prinsip kepemilikan tersebut: kunci hanya boleh dilepas oleh pekerja yang memasangnya, dengan pengecualian yang diatur secara ketat oleh standar [1]. Gembok di titik isolasi dengan demikian berfungsi sebagai penanda keberadaan seseorang yang keselamatannya bergantung pada keadaan mesin yang tetap diam.', 'Skala dampaknya terukur. OSHA memperkirakan kepatuhan terhadap prosedur LOTO mencegah sekitar 120 kematian dan 50.000 cedera setiap tahun di Amerika Serikat [2]. Angka tersebut menunjukkan bahwa urutan enam tahap ini bukan beban administratif, melainkan pengendalian yang hasilnya dapat dihitung.'], 't': 34}]},
    'pks-tbs-menjadi-cpo-motion': {'lead': 'Tandan buah segar yang berduri dan tidak dapat dimakan menyimpan minyak di dalam daging buahnya. Minyak tersebut tidak dapat diambil dengan satu alat, melainkan dilepaskan tahap demi tahap oleh rantai unit yang urutannya tidak dapat ditukar.', 'refs': ['Pahan, I. Panduan Lengkap Kelapa Sawit. Penebar Swadaya.', 'Jurnal Teknik Kimia, Universitas Sriwijaya. Kondisi sterilisasi tandan buah segar 130-140°C, tekanan 1,5-2,8 bar, sekitar 90 menit, siklus 3 puncak tekanan, mengutip Gold et al. (2012); konfirmasi rentang dalam MDPI (2021).'], 'sections': [{'h': 'Minyak yang terkunci di dalam daging buah', 'paras': ['Pada tandan buah segar, minyak sawit tersimpan di dalam sel daging buah dan terikat pada struktur seratnya. Selama sel tersebut utuh dan enzim di dalam buah masih aktif, minyak tidak dapat dipisahkan secara efisien dan mutunya menurun selama penundaan pengolahan [1].', 'Karena itu, pabrik kelapa sawit tidak memulai dari pemerasan. Pekerjaan pertama pabrik adalah membuka kunci struktur buah dan menghentikan aktivitas enzim, dan pekerjaan itu dilakukan dengan panas uap, bukan dengan tekanan mekanis.'], 't': 5}, {'h': 'Sterilisasi: uap bertekanan membuka kunci buah', 'paras': ['Sterilisasi merebus tandan dengan uap bertekanan. Kondisi yang dikutip dalam materi video adalah suhu 130-140°C, tekanan 1,5-2,8 bar, waktu sekitar 90 menit, dengan siklus 3 puncak tekanan, sedangkan literatur pembanding yang dikutip sumber yang sama memberi rentang 130-160°C dan 60-90 menit [2].', 'Panas uap ini mempunyai dua fungsi sekaligus: mematikan enzim lipase yang merusak mutu minyak dan melunakkan daging buah, sehingga buah atau brondolan mudah terlepas dari tandannya pada tahap berikutnya [1][2].'], 't': 17}, {'h': 'Perontokan: brondolan dilepas dari tandan', 'paras': ['Setelah dilunakkan, tandan masuk ke thresher yang mengguncang dan memutar tandan sehingga brondolan terlepas dan jatuh, sedangkan tandan kosong tersisih sebagai aliran terpisah [1].', 'Urutan ini tidak dapat ditukar dengan pemerasan. Tandan yang belum disterilisasi dan belum dirontokkan membawa struktur tandan yang besar dan keras masuk ke unit berikutnya, dan minyak yang masih berada di dalam buah yang menempel tidak akan terperas dengan sempurna.'], 't': 17}, {'h': 'Pelumat dan pemerasan: minyak kasar keluar', 'paras': ['Brondolan kemudian dilumatkan di digester. Pelumat memecah daging buah dan menyiapkan massa buah agar minyak mudah keluar, lalu screw press memeras massa tersebut sampai minyak sawit kasar mengalir keluar [1].', 'Hasil pemerasan masih berupa minyak kasar, yaitu campuran minyak dengan air dan padatan halus yang ikut terperas. Pada titik ini minyak telah bebas dari buah, tetapi belum memenuhi mutu minyak sawit mentah yang siap disimpan dan dikirim.'], 't': 27}, {'h': 'Klarifikasi: CPO jernih naik ke atas', 'paras': ['Minyak kasar dipisahkan di clarifier. Di dalam tangki klarifikasi, campuran dibiarkan memisah berdasarkan perbedaan massa jenis: minyak yang lebih ringan naik ke atas, sedangkan air dan padatan turun dan dikeluarkan dari bawah [1].', 'Lapisan atas yang jernih itulah CPO (crude palm oil). Rangkaian lengkapnya menunjukkan prinsip pabrik ini: sterilisasi membuka kunci, perontokan melepas buah, pelumat dan pemerasan mengeluarkan minyak, dan klarifikasi memisahkannya dari air serta padatan. Melompati satu unit berarti sebagian minyak ikut terbuang bersama aliran lain.'], 't': 27}]},
    'refinery-sawit-olein-stearin-motion': {'lead': 'Minyak goreng yang jernih di dapur berawal dari CPO yang berwarna merah pekat. Di antara kedua wujud itu terdapat dua pekerjaan yang berbeda: pemurnian yang membersihkan minyak, dan fraksionasi yang membagi minyak bersih menjadi dua fraksi dengan kegunaan yang berlawanan.', 'refs': ['Lee, et al. Processing, Characteristics, and Potential Application of Red Palm Oil: A Review.', 'Malaysian Palm Oil Board (MPOB). Publikasi proses refinery dan fraksionasi minyak sawit.', 'PORAM Specification; Malaysian Standard MS 815:2007; Codex Alimentarius CXS 210-1999.'], 'sections': [{'h': 'Warna merah CPO dan pengotor yang dibawanya', 'paras': ['CPO berwarna merah karena kandungan karoten di dalamnya. Bersamaan dengan warna itu, CPO masih membawa getah, pengotor, dan bau yang harus dibuang sebelum minyak layak dipakai sebagai bahan pangan [1].', 'Karena itu, CPO mentah tidak langsung dipakai menggoreng. Warna kuning keemasan minyak goreng yang dikenal konsumen adalah hasil pengolahan, bukan warna asli minyak sawit mentah [1][2].'], 't': 7}, {'h': 'Tiga tahap pemurnian menuju RBDPO', 'paras': ['Pemurnian CPO berlangsung melalui tiga tahap yang berurutan: degumming, bleaching, dan deodorisasi. Degumming menyingkirkan getah, bleaching menyerap warna dan pengotor yang tersisa, dan deodorisasi menghilangkan bau serta komponen penyebab rasa yang tidak dikehendaki [1][2].', 'Hasil ketiga tahap tersebut adalah RBDPO (refined, bleached, deodorized palm oil), minyak sawit bersih yang jernih. Urutannya tidak dapat dilompati, karena setiap tahap menyingkirkan kelompok pengotor yang berbeda dan menyiapkan minyak untuk tahap berikutnya.'], 't': 14}, {'h': 'Fraksionasi: pendinginan perlahan dan kristalisasi', 'paras': ['RBDPO yang telah bersih kemudian difraksionasi. Minyak didinginkan secara perlahan sampai sebagian komponennya mengkristal menjadi padatan, sedangkan sebagian lain tetap cair pada suhu yang sama [2].', 'Kristal padat tersebut kemudian dipisahkan dengan penyaringan dari fraksi cairnya. Mekanisme pemisahannya adalah kristalisasi dan pemisahan fisik, bukan reaksi kimia: satu minyak bersih dibagi menjadi dua fraksi berdasarkan perilaku kristalisasinya.'], 't': 28}, {'h': 'Olein cair dan stearin padat', 'paras': ['Fraksi yang tetap cair disebut olein dan dipakai sebagai minyak goreng. Fraksi yang memadat disebut stearin dan dipakai sebagai bahan margarin dan shortening, produk yang justru memerlukan struktur padat [2].', 'Perbedaan kedua fraksi itu dibakukan dalam spesifikasi: standar yang dikutip dalam materi video menetapkan nilai iod (iodine value) olein minimal 56 dan stearin maksimal 48 g I2/100 g minyak, dengan ketentuan Codex CXS 210-1999 yang sejalan untuk batas stearin maksimal 48 [3]. Nilai iod yang lebih tinggi pada olein sejalan dengan sifatnya yang lebih cair, dan nilai yang lebih rendah pada stearin sejalan dengan sifatnya yang lebih padat.'], 't': 35}, {'h': 'Satu bahan baku, dua produk yang saling melengkapi', 'paras': ['Refinery sawit dengan demikian tidak menghasilkan satu produk tunggal. Dari CPO yang sama, pemurnian menghasilkan minyak bersih, dan fraksionasi membagi minyak bersih itu menjadi fraksi cair untuk menggoreng dan fraksi padat untuk margarin serta shortening [2].', 'Pembagian ini meningkatkan nilai keseluruhan minyak sawit: bagian yang dahulu dianggap sisa padat mempunyai pasarnya sendiri, dan setiap tahap, dari penghilangan getah sampai pemisahan kristal, menentukan mutu fraksi yang dihasilkan.'], 't': None}]},
    'satu-barel-minyak-motion': {'lead': 'Satu barel minyak mentah setara 159 liter, tetapi angka tersebut adalah satuan volume umpan, bukan janji mengenai satu jenis produk. Berapa galon bensin yang sesungguhnya diperoleh dari satu barel, dan ke mana sisa volumenya pergi?', 'refs': ['U.S. Energy Information Administration. Frequently Asked Questions: How Many Gallons of Gasoline and Diesel Fuel Are Made from One Barrel of Oil? U.S. Department of Energy.', 'Seader, J. D., Henley, E. J., & Roper, D. K. (2016). Separation Process Principles (4th ed.). Wiley.', 'Kister, H. Z. (1992). Distillation Design. McGraw-Hill.'], 'sections': [{'h': 'Satu barel sebagai satuan volume, bukan satuan produk', 'paras': ['Barel adalah satuan volume standar perdagangan minyak: satu barel setara 42 galon AS atau 159 liter [1]. Satuan ini menyatakan jumlah minyak mentah yang masuk ke kilang, dan tidak menyatakan komposisi produk yang akan keluar darinya.', 'Kesalahan baca yang umum adalah memperlakukan satuan umpan sebagai satuan produk, seolah satu barel otomatis berarti satu barel bensin. Kilang tidak bekerja dengan cara tersebut, karena minyak mentah adalah campuran yang harus dipecah terlebih dahulu sebelum setiap bagiannya dapat dimanfaatkan [2].'], 't': 0}, {'h': 'Pemanasan dan masuknya umpan ke unit distilasi mentah', 'paras': ['Tahap pertama di kilang adalah pemanasan minyak mentah, kemudian aliran masuk ke menara distilasi pada unit distilasi mentah atau crude distillation unit (CDU). Di dalam menara, komponen yang lebih mudah menguap bergerak ke atas, sedangkan komponen yang lebih sukar menguap tertinggal di bagian bawah [2][3].', 'Prinsip yang sama berlaku pada kilang dengan skala dan konfigurasi berbeda. Komposisi produk akhir dapat menyesuaikan jenis minyak mentah yang diolah, tetapi urutan pemisahannya tetap ditentukan oleh perilaku penguapan setiap fraksi di dalam menara.'], 't': 6.5}, {'h': 'Titik didih sebagai dasar pemisahan fraksi', 'paras': ['Pemisahan di menara distilasi adalah pemisahan fisik berdasarkan perbedaan titik didih. Fraksi ringan menempati bagian atas menara, sedangkan fraksi berat menempati bagian bawah, dan setiap fraksi diambil melalui saluran keluar pada tingkat yang sesuai dengan rentang didihnya [2][3].', 'Urutan fraksi dari atas ke bawah adalah gas, nafta, kerosen, diesel, dan residu. Urutan ini bukan susunan administratif, melainkan konsekuensi langsung dari volatilitas: semakin ringan suatu fraksi, semakin tinggi posisinya di dalam menara sebelum mengembun dan diambil sebagai produk.'], 't': 13}, {'h': 'Membaca angka EIA: bensin, distilat, dan avtur', 'paras': ['Data U.S. Energy Information Administration (EIA) untuk kilang di Amerika Serikat memberikan gambaran kuantitatifnya: dari satu barel 42 galon diperoleh 19 sampai 20 galon bensin motor dan 11 sampai 13 galon distilat, kelompok produk yang mencakup diesel [1].', 'Selain kedua produk utama tersebut, satu barel yang sama menghasilkan 4 galon avtur, bahan bakar untuk pesawat terbang [1]. Ketiga angka ini saja telah menunjukkan bahwa bensin, sekalipun merupakan porsi terbesar, hanya menempati kurang dari separuh volume barel.'], 't': 20}, {'h': 'Processing gain dan produk di luar bahan bakar utama', 'paras': ['Sisa volume barel tidak hilang. Bagian lain keluar sebagai gas, aspal, dan bahan baku plastik, sehingga daftar produk satu barel selalu lebih panjang dari daftar bahan bakar cairnya [1].', 'Total volume seluruh produk akhir bahkan melebihi 42 galon. Fenomena ini disebut processing gain: pengolahan memecah molekul besar menjadi molekul yang lebih kecil dengan densitas lebih rendah, sehingga massa yang sama menempati volume yang lebih besar [1][2]. Kenaikan tersebut adalah kenaikan volume, bukan penciptaan massa baru.'], 't': 27.5}]},
    'sistem-kerja-tiga-shift': {'lead': 'Pada malam hari, ketika sebagian besar tempat kerja gelap dan kosong, pabrik proses tetap menyala penuh. Keberlanjutan itu bukan kebiasaan, melainkan konsekuensi rancangan: proses kontinu tidak mengenal jam tutup, dan manusia yang menjaganya harus dibagi ke dalam regu bergilir.', 'sections': [{'h': 'Mengapa proses kontinu tidak dapat dimatikan setiap malam', 't': 6, 'paras': ['Pabrik proses seperti kilang dan pabrik kimia dirancang beroperasi 24 jam. Reaktor, kolom, dan peralatan bertekanan di dalamnya mencapai keadaan operasi yang stabil melalui pemanasan dan penekanan bertahap, dan keadaan itu tidak dapat dimatikan lalu dinyalakan kembali setiap hari tanpa konsekuensi [1].', 'Penyalaan dan penghentian operasi merupakan operasi yang berisiko dan mahal, serta memberikan tegangan termal pada peralatan karena material peralatan memuai dan menyusut mengikuti perubahan suhu yang besar. Atas alasan tersebut, penghentian diperlakukan sebagai peristiwa besar yang direncanakan, bukan sebagai rutinitas harian [1][2].']}, {'h': 'Pembagian tiga shift yang menutup 24 jam', 't': 13, 'paras': ['Solusi yang dipakai industri proses adalah membagi hari menjadi tiga shift dengan durasi masing-masing 8 jam: pagi, siang, dan malam. Tiga regu bergantian menjaga proses yang sama, sehingga 24 jam tertutup tanpa jeda dan tidak ada satu jam pun yang tidak terjaga [2].', 'Pembagian ini menyelesaikan persoalan dari sisi proses secara tuntas. Peralatan beroperasi kontinu sebagaimana dirancang, sedangkan kebutuhan jaga manusia didistribusikan kepada tiga regu yang masing-masing bekerja dalam rentang waktu yang terbatas [1].']}, {'h': 'Harga rotasi: jam tidur yang terus bergeser', 't': 20, 'paras': ['Harga sistem ini dibayar oleh operator. Pada setiap rotasi, regu berpindah segmen waktu, dan jam tidur ikut bergeser mengikuti segmen yang baru. Tubuh yang baru menyesuaikan diri dengan jadwal malam harus kembali menyesuaikan diri dengan jadwal pagi pada rotasi berikutnya.', 'Gangguan tersebut mengenai ritme sirkadian, jam biologis yang mengatur kantuk dan kesiagaan mengikuti pola terang dan gelap. Rotasi yang terus bergerak berarti ritme itu tidak pernah menetap, dan kelelahan menjadi risiko operasional yang harus dikelola, bukan sekadar ketidaknyamanan pribadi [1].']}, {'h': 'Adaptasi operator: tidur terjadwal dan serah terima ketat', 't': 27, 'paras': ['Operator yang bertahan dalam sistem ini mengelola tidurnya secara terjadwal, bukan menunggu kantuk datang. Tidur diperlakukan sebagai bagian dari kesiapan bertugas, dan paparan cahaya terang selama jaga dipakai untuk menjaga kesiagaan pada segmen malam.', 'Unsur adaptasi yang lain bersifat operasional: serah terima antarshift yang ketat. Karena penjaga proses berganti tiga kali sehari, keadaan peralatan dan gangguan yang sedang berjalan harus berpindah antarregu secara lengkap melalui catatan serah terima, agar keberlanjutan jaga tidak terputus oleh pergantian orang [1][2].']}, {'h': 'Kompromi yang menentukan ritme hidup operator', 't': None, 'paras': ['Sistem tiga shift pada dasarnya adalah kompromi yang disadari. Proses menuntut keberlanjutan penuh, fisiologi manusia menuntut tidur yang teratur, dan pembagian 8 jam per regu adalah titik temu yang memungkinkan keduanya berjalan bersama [2].', 'Konsekuensinya melampaui dinding pabrik. Sistem shift menentukan ritme hidup operator selama bertahun-tahun: waktu tidur, waktu bersama keluarga, dan waktu istirahat semuanya disusun mengelilingi lingkaran 24 jam yang tidak pernah berhenti [1].']}], 'refs': ["Mannan, S. (Ed.). (2012). Lees' Loss Prevention in the Process Industries: Hazard Identification, Assessment and Control (4th ed.). Butterworth-Heinemann.", "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."]},
    'tangki-putih-floating-roof': {'lead': 'Warna putih pada tangki minyak bukan pilihan estetika. Warna tersebut adalah pertahanan pertama terhadap panas matahari, dan di dalam tangki yang sama, atap yang terapung di atas cairan adalah pertahanan kedua terhadap ruang tempat uap terbentuk.', 'refs': ['American Petroleum Institute. API Standard 650: Welded Tanks for Oil Storage.', 'Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2007). Fundamentals of Heat and Mass Transfer (6th ed.). Wiley.', 'U.S. Environmental Protection Agency. AP-42, Chapter 7, Section 1: Organic Liquid Storage Tanks.'], 'sections': [{'h': 'Radiasi matahari dan suhu dinding tangki', 'paras': ['Dinding tangki yang terpapar matahari menerima radiasi secara terus menerus sepanjang siang. Permukaan gelap menyerap sebagian besar radiasi tersebut dan mengubahnya menjadi panas, sehingga suhu dinding dan cairan di dekatnya naik. Permukaan terang berperilaku sebaliknya: sebagian besar radiasi dipantulkan kembali sebelum sempat menjadi panas [2].', 'Perbedaan perilaku ini menentukan beban panas yang harus ditanggung isi tangki setiap hari. Pada tangki berisi cairan yang mudah menguap, setiap kenaikan suhu dinding berarti tekanan uap cairan yang lebih tinggi dan kecenderungan menguap yang lebih besar.'], 't': 6}, {'h': 'Ruang uap sebagai tempat pembentukan uap', 'paras': ['Pada tangki beratap tetap, terdapat ruang kosong di antara permukaan cairan dan atap. Ruang uap inilah tempat uap cairan terkumpul. Saat suhu naik, uap bertambah, dan kelebihan uap keluar melalui ventilasi agar tekanan di dalam tangki tetap terkendali [3].', 'Setiap uap yang keluar melalui ventilasi adalah produk yang hilang ke udara. Kerugiannya bukan sekadar soal emisi, melainkan juga soal jumlah produk yang tersimpan: cairan yang mudah menguap seperti bensin menyusut volumenya selama penyimpanan apabila ruang uap dan panas matahari tidak dikendalikan [1][3].'], 't': 13}, {'h': 'Cat putih sebagai pertahanan radiasi', 'paras': ['Pertahanan pertama bekerja di permukaan luar. Cat putih memantulkan radiasi matahari, sehingga suhu dinding tangki lebih rendah dibandingkan tangki berwarna gelap pada paparan yang sama [2].', 'Pertahanan ini bersifat pasif dan bekerja tanpa energi tambahan. Selama permukaan cat terjaga, panas yang masuk ke cairan berkurang, tekanan uap lebih rendah, dan laju pembentukan uap di ruang di atas cairan ikut menurun.'], 't': 20}, {'h': 'Atap terapung dan peniadaan ruang uap', 'paras': ['Pertahanan kedua bekerja di dalam tangki. Atap terapung adalah atap yang mengapung langsung di atas permukaan cairan dan bergerak naik serta turun mengikuti perubahan level cairan. Karena atap selalu menempel pada permukaan, ruang uap di atas cairan menyusut sampai hampir nol [1].', 'Tanpa ruang uap, uap hampir tidak memiliki tempat untuk terbentuk dan terkumpul. Data EPA AP-42 yang dikutip dalam materi video menunjukkan pemasangan atap terapung dan seal mengendalikan emisi penguapan tangki beratap tetap dengan efisiensi 60 sampai 99 persen, tergantung pada jenis atap, jenis seal, dan jenis cairan yang disimpan [3].'], 't': 27}, {'h': 'Dua pertahanan yang bekerja pada dua sisi berbeda', 'paras': ['Kedua solusi tersebut tidak saling menggantikan karena keduanya bekerja pada sisi persoalan yang berbeda. Cat putih mengurangi panas yang masuk dari luar, sedangkan atap terapung menghapus ruang tempat uap terbentuk di dalam [1][2].', 'Kombinasinya menjelaskan bentuk tangki penyimpanan minyak yang lazim terlihat di area tangki: silinder putih dengan atap yang bergerak mengikuti isi. Bentuk tersebut adalah jawaban rekayasa atas satu persoalan fisika yang sama, yaitu penguapan cairan yang mudah menguap selama penyimpanan.'], 't': None}]},
    'turnaround-pabrik-berhenti-total': {'lead': 'Pabrik yang berhenti total selama berminggu-minggu umumnya dibayangkan sebagai pabrik yang bermasalah. Pada pabrik proses, penghentian semacam itu justru direncanakan bertahun-tahun sebelumnya dan merupakan syarat agar pabrik dapat beroperasi andal pada tahun-tahun berikutnya.', 'sections': [{'h': 'Penghentian terencana, bukan kegagalan operasi', 't': 0, 'paras': ['Turnaround adalah penghentian terencana seluruh unit proses selama beberapa minggu. Tujuannya bukan memperbaiki satu kerusakan, melainkan membuka, memeriksa, membersihkan, dan memperbaiki peralatan statis dan berputar yang selama operasi tidak dapat disentuh dari dalam [1].', 'Perbedaan mendasarnya dengan penghentian darurat terletak pada persiapannya. Turnaround dijadwalkan jauh hari, daftar pekerjaannya disusun dan ditumpuk secara sengaja, sedangkan penghentian darurat terjadi karena peralatan gagal lebih dahulu. Yang pertama merupakan keputusan perawatan; yang kedua merupakan konsekuensi dari perawatan yang tertunda [2].']}, {'h': 'Pekerjaan yang hanya mungkin saat unit berhenti total', 't': 6, 'paras': ['Sejumlah peralatan pabrik secara fisik tidak dapat dibuka selama unit beroperasi. Kolom distilasi harus dikosongkan dan dibuka dari atas sebelum bagian dalamnya dapat diperiksa, dan katalis yang telah menurun aktivitasnya hanya dapat diangkat keluar dan diganti pada kondisi unit berhenti [1].', 'Hal yang sama berlaku untuk penukar panas. Bundelnya harus dicabut dari rumahnya agar kerak yang menumpuk pada permukaan perpindahan panas dapat dibersihkan secara langsung. Selama unit berjalan, permukaan tersebut tertutup aliran proses dan tidak terjangkau oleh pekerjaan pembersihan apa pun [1].']}, {'h': 'Ribuan pekerjaan dalam satu jendela berhenti', 't': 13, 'paras': ['Karena jendela berhenti total jarang terjadi, ribuan pekerjaan perawatan ditumpuk ke dalamnya sekaligus. Setiap pekerjaan yang mensyaratkan unit kosong, tidak bertekanan, dan aman dibuka dicatat selama masa operasi, lalu dieksekusi berurutan ketika jendela itu tiba [2].', 'Konsentrasi pekerjaan inilah yang membuat turnaround menjadi jendela rawat terbesar dalam siklus hidup pabrik. Melewatkan satu pekerjaan penting berarti pekerjaan tersebut harus menunggu jendela berikutnya, atau dikerjakan melalui penghentian darurat yang biayanya dan risikonya jauh lebih besar [2].']}, {'h': 'Urutan kerja: membuka, membersihkan, mengganti, menguji', 't': 20, 'paras': ['Urutan inti turnaround bersifat tetap. Peralatan dibuka, bagian dalamnya dibersihkan dari kerak dan endapan, komponen yang aus seperti katup diganti, kemudian setiap peralatan diuji satu per satu, termasuk pengujian tekanan dengan pengukur, sebelum dinyatakan layak beroperasi kembali [1].', 'Tahap pengujian tidak dapat dilompati. Peralatan yang baru dibuka dan dipasang kembali harus dibuktikan integritasnya dalam keadaan terkendali, bukan dibuktikan oleh tekanan operasi pada saat unit telah berjalan penuh [2].']}, {'h': 'Penyalaan kembali sebagai tahap paling diawasi', 't': 27, 'paras': ['Setelah seluruh pekerjaan selesai, unit tidak dinyalakan serentak. Penyalaan kembali dilakukan bertahap, unit per unit, dengan suhu dan kondisi operasi dinaikkan secara landai sampai stabil di garis operasi [2].', 'Di sinilah nilai turnaround dibuktikan. Penghentian yang direncanakan hari ini membeli operasi yang andal bertahun-tahun, sedangkan penundaannya memaksa peralatan aus bekerja sampai gagal mendadak pada waktu yang tidak dipilih oleh siapa pun [1][2].']}], 'refs': ["Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.", "Mannan, S. (Ed.). (2012). Lees' Loss Prevention in the Process Industries: Hazard Identification, Assessment and Control (4th ed.). Butterworth-Heinemann."]},
    'buildup-boiler-pltu-dari-ceret': {'lead': 'Pembangkit listrik tenaga uap dapat ditelusur dari peralatan dapur yang paling sederhana. Ceret membuang uapnya ke udara, sedangkan pembangkit menangkap uap tersebut, menaikkan tekanannya, melipatgandakan jumlahnya, mengeringkannya, dan memakai putarannya untuk menghasilkan listrik [1][2].', 'refs': ["Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.", 'El-Wakil, M. M. (1984). Powerplant Technology. McGraw-Hill.', 'Coulson, J. M., & Richardson, J. F. (1999). Chemical Engineering, Volume 1: Fluid Flow, Heat Transfer and Mass Transfer (6th ed.). Butterworth-Heinemann.'], 'sections': [{'h': 'Menangkap uap dan menjaga air tidak habis', 'paras': ['Air yang mendidih di dalam ceret menghasilkan uap yang menyembur dari corong dan hilang ke udara. Menyambungkan pipa ke corong dan mengarahkan uap ke kincir kecil mengubah uap yang terbuang menjadi tenaga putar. Langkah ini membuktikan fungsi dasar uap bertekanan sebagai penggerak, walaupun putaran yang dihasilkan lemah [1][2].', 'Dua cacat muncul segera. Putaran lemah karena tekanan masih kecil, dan kincir berhenti setelah air di dalam ceret habis. Cacat kedua ditutup oleh tangki umpan yang mengisi ulang air terus-menerus, dan cacat pertama ditutup pada langkah berikutnya dengan menaikkan tekanan [2].'], 't': 0.0}, {'h': 'Tekanan, jaringan pipa air, dan uap kering', 'paras': ['Dinding yang dipertebal, penutupan yang rapat, dan katup pengaman menaikkan tekanan uap, sehingga putaran menjadi jauh lebih kencang. Katup pengaman menjaga kenaikan tersebut tetap berada dalam batas yang aman. Setelah tekanan naik, batas berikutnya adalah jumlah, karena satu ceret hanya menghasilkan sedikit uap [1][2].', 'Jumlah uap dilipatgandakan dengan mengganti perut ceret menjadi jaringan pipa air di dalam kotak api, yang dipanaskan dari segala sisi dan merupakan bentuk dasar boiler pipa air. Uap yang berlimpah itu masih basah, sehingga dilewatkan melalui superheater, pipa tambahan pada titik terpanas api. Uap keluar kering dan jauh lebih panas, dan tenaganya melonjak sebelum memasuki turbin [1].'], 't': 16.3}, {'h': 'Turbin, generator, dan penutupan siklus', 'paras': ['Kincir kecil tidak kuat menahan tenaga sebesar itu, sehingga penggerak diganti turbin sudu bertingkat. Di dalam turbin, uap mengembang tahap demi tahap pada deretan sudu dan memutar poros dengan halus dan kuat. Poros tersebut kemudian disambungkan ke generator, dan untuk pertama kalinya lampu menyala, yang menandai putaran telah berubah menjadi listrik [2].', 'Pada skala pabrik, kotak api menjadi gedung boiler berdinding pipa air dengan steam drum di puncak, turbin dan generator membesar segaris, dan kondensor menutup siklus air. Uap bekas diubah kembali menjadi air dan dipompa balik ke boiler untuk dipakai lagi. Prinsipnya tetap satu dari awal sampai akhir, yaitu air mendidih menjadi uap dan uap bertekanan memutar turbin. Yang berubah hanya skalanya [1][2].'], 't': 40.7}]},
    'buildup-kolom-distilasi-alembik': {'lead': 'Kolom distilasi sering tampak sebagai menara yang rumit, padahal susunannya dapat ditelusur dari alat suling tertua. Alembik melakukan satu kali penguapan dan satu kali kondensasi, sedangkan kolom menumpuk pengulangan proses tersebut menjadi puluhan tray dalam satu menara [1][2].', 'refs': ['McCabe, W. L., Smith, J. C., & Harriott, P. (2005). Unit Operations of Chemical Engineering (7th ed.). McGraw-Hill.', 'Parkash, S. (2003). Refining Processes Handbook. Gulf Professional Publishing.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."], 'sections': [{'h': 'Alembik sebagai satu tahap pemisahan', 'paras': ['Distilasi memisahkan campuran berdasarkan perbedaan titik didih. Komponen yang lebih mudah menguap meninggalkan cairan sebagai uap, kemudian uap tersebut didinginkan kembali menjadi cairan. Pada alembik, rangkaian itu hanya terjadi satu kali, sehingga alat ini setara dengan satu tahap pemisahan [1].', 'Konsekuensi satu tahap adalah kemurnian yang terbatas. Uap yang terbentuk masih membawa sebagian komponen yang lebih berat, sehingga hasil kondensasinya masih kotor. Keterbatasan ini bukan kekurangan pemanasan, melainkan kekurangan jumlah tahap, dan dari keterbatasan inilah seluruh pembangunan berikutnya berangkat [1].'], 't': 0.0}, {'h': 'Pengulangan tahap dan alasan penumpukannya', 'paras': ['Apabila uap hasil penguapan pertama diuapkan sekali lagi, kemurnian komponen ringan naik secara bertahap. Setiap pengulangan menambah satu tahap pemisahan. Prinsip bertahap ini adalah dasar pemisahan bertingkat yang dipakai pada kolom modern [1].', 'Tahap yang dibangun sebagai bejana terpisah menuntut ruang yang besar dan boros energi, karena setiap tahap memerlukan bejana, pemanas, dan pendingin sendiri. Solusinya adalah menumpuk seluruh tahap menjadi satu kolom vertikal. Di dalam kolom tersebut, tray bertingkat menggantikan bejana terpisah, dan setiap tray bekerja seperti satu kali penguapan mini [1][2].'], 't': 10.9}, {'h': 'Reboiler, kondensor, dan pertemuan uap dengan cairan', 'paras': ['Dua aliran berlawanan arah menjaga setiap tray tetap bekerja. Reboiler di dasar kolom mendidihkan cairan dan menyediakan uap yang naik, sedangkan kondensor di puncak mengembunkan uap menjadi cairan yang turun dari tray ke tray. Uap naik, cairan turun, dan keduanya bertemu di setiap tray [1].', 'Pertemuan pada tray adalah tempat pemisahan berlangsung. Uap yang naik melepaskan sebagian komponen berat ke cairan, sedangkan cairan yang turun melepaskan komponen ringan ke uap. Akibatnya, komposisi uap semakin kaya komponen ringan menuju puncak, dan komposisi cairan semakin kaya komponen berat menuju dasar [1].'], 't': 33.8}, {'h': 'Reflux dan operasi kontinu kolom', 'paras': ['Reflux adalah pengembalian sebagian cairan dari kondensor ke puncak kolom. Aliran balik ini menyapu komponen berat turun dan memperkaya komponen ringan di puncak, sehingga kemurnian produk atas atau distilat naik. Tanpa reflux, bagian atas kolom kehilangan cairan pencuci dan pemisahannya melemah [1].', 'Pembangunan ditutup dengan operasi kontinu. Umpan masuk terus-menerus di tengah kolom, produk ringan keluar dari atas, dan produk berat keluar dari bawah. Kolom kilang pada umumnya berisi 30 sampai 50 tray, suatu jumlah tahap yang tidak mungkin dicapai oleh alembik tunggal, dengan prinsip yang tetap satu, yaitu perbedaan titik didih [2].'], 't': 45.9}]},
    'buildup-kolom-distilasi-remake': {'lead': 'Satu tabung logam terbuka kehilangan seluruh uapnya ke udara, dan dari kegagalan sederhana itu kolom distilasi dapat dibangun tanpa mengganti bendanya. Setiap tambahan menutup satu cacat yang dinyatakan oleh langkah sebelumnya, dari penangkapan uap sampai transformasi menjadi menara baja di tengah kilang [1][2].', 'refs': ['McCabe, W. L., Smith, J. C., & Harriott, P. (2005). Unit Operations of Chemical Engineering (7th ed.). McGraw-Hill.', 'Parkash, S. (2003). Refining Processes Handbook. Gulf Professional Publishing.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."], 'sections': [{'h': 'Menangkap uap dan mengubahnya menjadi cairan', 'paras': ['Tabung terbuka di atas api memanaskan campuran, dan uap yang paling ringan naik lalu hilang ke udara. Menutup tabung dan memasang pipa miring di puncaknya memaksa uap keluar melalui jalur tertentu. Penutupan ini menangkap uap, tetapi belum mengubah wujudnya, karena uap yang melewati pipa tetap berwujud uap [1].', 'Perubahan wujud terjadi setelah pipa dibungkus air dingin. Uap yang menyentuh dinding pipa yang dingin mengembun dan jatuh sebagai tetesan ke dalam wadah. Tetesan tersebut adalah cairan pertama hasil proses, dan langkah ini memperkenalkan kondensasi sebagai pasangan wajib dari penguapan pada setiap pemisahan distilasi [1].'], 't': 0.0}, {'h': 'Umpan kontinu dan reflux sebagai penguat pemisahan', 'paras': ['Proses yang bertumpu pada satu tabung berisi campuran akan berhenti setelah campuran tersebut habis dan tetesan berhenti. Tangki dan pipa umpan yang terpasang pada sisi tengah tabung mengalirkan bahan terus-menerus, sehingga proses tidak pernah berhenti. Keberlangsungan aliran ini adalah syarat operasi kolom industri yang kontinu [1].', 'Hasil yang mengalir terus-menerus tetap masih lemah, sehingga sebagian tetesan dikembalikan ke puncak tabung sebagai reflux. Uap yang naik dipaksa bertemu cairan yang turun, dan setiap pertemuan memindahkan komponen berat ke cairan dan komponen ringan ke uap. Pertemuan berulang inilah yang membuat pemisahan jauh lebih kuat daripada satu kali penguapan [1].'], 't': 19.1}, {'h': 'Tray, keluaran dasar, dan kondensor yang membesar', 'paras': ['Satu pertemuan belum cukup, sehingga tabung tumbuh memanjang ke atas dan tray ditumpuk di dalamnya. Setiap tray menyediakan satu pertemuan baru antara uap dan cairan dalam tabung yang sama. Kolom kilang pada umumnya berisi 30 sampai 50 tray, yang berarti puluhan pertemuan berurutan dalam satu menara [2].', 'Dua tambahan melengkapi operasi tersebut. Pipa keluar di dasar mengeluarkan cairan berat yang mengumpul, sehingga tabung tidak kepenuhan dan komponen berat keluar dari bawah secara terus-menerus. Di puncak, pendingin kecil tumbuh menjadi kondensor besar dengan air yang dipompa memutar tanpa henti, membuang panas keluar dan menjaga uap tetap berubah menjadi cairan pada beban yang meningkat [1].'], 't': 33.7}, {'h': 'Transformasi menjadi kolom pabrik', 'paras': ['Langkah terakhir menutup cangkang sampai menjadi baja utuh, memasang tangga di sisinya, dan menyambungkan pipa di puncaknya ke tangki penyimpanan. Pada keadaan akhir, koil dan wadah penerima terbuka telah berubah menjadi kondensor tertutup, reflux drum, dan pipa produk tertutup, sedangkan kolom berdiri dengan proporsi menara di atas fondasi, lengkap dengan platform dan tangga berkandang [2].', 'Transformasi ini menjaga identitas benda utama. Tabung kecil pada awal video adalah cangkang kolom pada akhir video, tumbuh di tempat tanpa diganti benda lain yang telah jadi. Prinsip yang bekerja tidak berubah dari awal sampai akhir, yaitu perbedaan titik didih, dan yang berubah adalah kelengkapan serta skala peralatannya [1][2].'], 't': 56.0}]},
    'buildup-reaktor-dari-panci-presto': {'lead': 'Reaktor kimia dan panci presto berbagi titik awal yang sama, yaitu bejana tertutup yang isinya dipanaskan sampai tekanannya naik. Perbedaan keduanya bukan pada prinsipnya, melainkan pada pengendalian. Reaktor adalah bejana yang tekanan, pencampuran, dan suhunya dijaga secara berlapis sampai reaksi dapat berjalan terus-menerus dengan aman [1][2].', 'refs': ['Levenspiel, O. (1999). Chemical Reaction Engineering (3rd ed.). John Wiley & Sons.', 'Fogler, H. S. (2016). Elements of Chemical Reaction Engineering (5th ed.). Prentice Hall.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."], 'sections': [{'h': 'Tekanan yang dijaga dan pencampuran yang merata', 'paras': ['Panci presto di atas kompor mendidihkan isinya, tekanannya naik, dan uapnya menyembur liar lewat katup. Katup pengaman yang membuka dan menutup teratur, lengkap dengan alat ukur tekanan pada tutup, membuat tekanan stabil dan terbaca. Pengendalian tekanan adalah lapis pertama yang membedakan bejana reaksi dari bejana masak biasa [2][3].', 'Tekanan yang terkendali belum menjamin hasil yang merata. Isi yang tidak tercampur gosong di bagian bawah dan mentah di bagian atas. Pengaduk yang dipasang dari atas dan menembus tutup berputar mengaduk seluruh isi, sehingga campuran menjadi rata dan pematangan merata. Pada reaktor, pencampuran menentukan keseragaman suhu dan komposisi di seluruh volume [1][2].'], 't': 0.0}, {'h': 'Pembuangan panas dan operasi yang kontinu', 'paras': ['Pencampuran yang merata membuka persoalan berikutnya. Isi mulai menghasilkan panasnya sendiri dan suhu lari naik. Jaket pendingin yang dilingkarkan pada badan, tempat air dingin mengalir terus, membuang panas berlebih tersebut dan membuat suhu jinak. Pengendalian suhu adalah syarat keselamatan utama pada reaksi yang menghasilkan panas [1][2].', 'Operasi yang berhenti setiap kali isi habis kemudian diubah menjadi kontinu. Pipa umpan dari tangki bahan dan pipa keluar untuk produk membuat bahan mengalir masuk dan produk mengalir keluar tanpa pernah berhenti dan tanpa membuka tutup. Dengan perubahan ini, bejana tidak lagi bekerja per masakan, melainkan sebagai peralatan proses yang beroperasi terus-menerus [2].'], 't': 20.3}, {'h': 'Bejana yang kuat dan kendali otomatis', 'paras': ['Aliran terus-menerus menuntut kekuatan yang tidak dimiliki badan presto yang tipis. Badan dibangun ulang menjadi bejana stainless berdinding tebal dengan tutup flensa yang dibaut rapat di sekelilingnya, sehingga kuat menahan tekanan operasi kontinu. Pemilihan bahan dan ketebalan dinding adalah bagian dari rancangan bejana tekan, bukan sekadar pembesaran bentuk [3].', 'Kekuatan bejana dilengkapi penjagaan. Sensor dipasang pada berbagai titik dan dihubungkan ke panel kendali otomatis, sehingga suhu, tekanan, dan level terpantau dan terkendali sendiri dengan aman tanpa dijaga, termasuk selama dua puluh empat jam penuh. Pada keadaan akhir skala pabrik, bejana tumbuh menjadi reaktor raksasa dengan pengaduk bermotor besar di puncak dan jaket pendingin raksasa pada badannya. Prinsipnya tetap satu, yaitu reaksi yang dikendalikan, dengan tekanan dijaga, campuran rata, dan suhu jinak [1][2].'], 't': 33.5}]},
    'ko-drum-penjaga-kompresor': {'lead': 'Kompresor adalah mesin untuk gas, tetapi gas yang tiba kepadanya hampir tidak pernah bersih dari cairan. Peralatan apa yang berdiri di antara aliran proses dan mesin tersebut, dan mengapa peralatan itu tidak boleh dilewati?', 'sections': [{'h': 'Gas proses yang tidak pernah benar-benar kering', 't': 4, 'paras': ['Aliran gas yang keluar dari peralatan proses hampir selalu membawa cairan. Sebagian uap di dalam aliran mengembun ketika suhu atau tekanan berubah di sepanjang pipa, dan sebagian cairan terbawa sebagai tetesan halus yang terseret oleh kecepatan aliran gas itu sendiri [1].', 'Keadaan ini bukan kelainan operasi, melainkan keadaan normal aliran dari proses. Karena itu perlindungan kompresor tidak dapat bergantung pada harapan bahwa gas akan tiba dalam keadaan kering, melainkan harus dirancang sebagai bagian tetap dari jalur masuk kompresor [1][2].']}, {'h': 'Mengapa cairan merusak mesin yang dirancang untuk gas', 't': 11, 'paras': ['Kompresor bekerja dengan memampatkan gas: volume gas menyusut ketika tekanannya dinaikkan, dan bilah mesin dirancang untuk aliran yang dapat dimampatkan tersebut. Cairan berperilaku sebaliknya, karena volumenya hampir tidak berubah ketika ditekan [1].', 'Tetesan cairan yang tiba di bilah yang berputar karena itu diterima sebagai tumbukan, bukan sebagai aliran. Tumbukan berulang merusak bilah dan seal, dan kerusakan itu terjadi di dalam mesin yang bernilai tinggi dan sulit diganti [1].']}, {'h': 'Prinsip KO drum: menurunkan kecepatan, membiarkan gravitasi bekerja', 't': 18, 'paras': ['KO drum, singkatan dari knock out drum, adalah bejana vertikal yang dipasang di hulu kompresor. Gas masuk ke dalam bejana yang penampangnya jauh lebih besar daripada pipa, sehingga kecepatan aliran turun secara tajam [1].', 'Pada kecepatan yang rendah, tetesan cairan tidak lagi terseret oleh aliran dan jatuh oleh gravitasi ke dasar bejana. Gas yang telah terpisah dari tetesannya keluar dari bagian atas drum dan melanjutkan perjalanan ke kompresor dalam keadaan kering [1].']}, {'h': 'Cairan yang terkumpul dan pembuangannya melalui drain', 't': 26, 'paras': ['Pemisahan tidak selesai pada jatuhnya tetesan. Cairan terkumpul di dasar drum dan levelnya naik seiring waktu, sehingga cairan itu harus dibuang melalui katup drain yang terbuka secara berkala atau berdasarkan levelnya [1].', 'Apabila pembuangan gagal dan level cairan naik sampai mencapai jalur keluar gas, cairan dapat kembali terbawa aliran dan perlindungan drum menjadi tidak berguna. Pengawasan level dan drain karena itu merupakan bagian dari fungsi pengamanannya, bukan pelengkapnya [2].']}, {'h': 'Penempatan di hulu dan kedudukannya sebagai pengaman', 't': None, 'paras': ['Kedudukan KO drum ditentukan oleh urutan alirannya: alat ini berada sesudah peralatan proses dan tepat sebelum kompresor, sehingga tidak ada jalur bagi gas untuk tiba di mesin tanpa melewati pemisahan terlebih dahulu [1][2].', 'Dibaca sebagai sistem, KO drum adalah asuransi yang sederhana sebelum mesin yang mahal. Alat ini tidak menambah kapasitas kompresor dan tidak mengubah komposisi gas; tugasnya satu, yaitu memastikan bahwa yang masuk ke kompresor hanyalah fasa yang memang dirancang untuk dimampatkan mesin tersebut [1].']}], 'refs': ['Gas Processors Suppliers Association. GPSA Engineering Data Book (Gas Processing).', 'American Petroleum Institute. API RP 14C.']},
    'lpg-cairan-dalam-tabung': {'lead': 'Tabung yang setiap hari disebut tabung gas ternyata tidak berisi gas. Mengapa campuran yang tersimpan di dalamnya berbentuk cairan, dan mengapa bentuk itu berubah tepat pada saat katup dibuka?', 'sections': [{'h': 'Campuran propana dan butana yang cenderung menjadi gas', 't': 6, 'paras': ['LPG adalah campuran propana (C3H8) dan butana (C4H10). Propana mendidih pada minus 42 derajat C dan butana pada minus 0,5 derajat C pada tekanan 1 atm, sehingga pada suhu ruang kedua komponen tersebut berada jauh di atas titik didihnya dan cenderung berbentuk gas [1][2].', 'Kecenderungan itu menimbulkan pertanyaan inti mengenai penyimpanannya: apabila kedua bahan ini cenderung menjadi gas pada suhu ruang, bagaimana cairan dapat tersimpan stabil di dalam tabung dalam waktu yang lama?']}, {'h': 'Tekanan uap yang menahan cairan', 't': 13, 'paras': ['Jawabannya adalah tekanan yang dibangun oleh LPG itu sendiri. Di dalam tabung tertutup, sebagian cairan menguap dan uapnya menekan permukaan cairan sampai tercapai kesetimbangan uap dan cairan, yaitu keadaan ketika laju penguapan sama dengan laju pengembunan [2].', 'Sebagai gambaran besarnya, tekanan uap butana adalah sekitar 2,2 bar pada 20 derajat C, dan tekanan uap propana jauh lebih tinggi. Campuran keduanya menghasilkan tekanan tabung yang cukup untuk menahan LPG tetap cair pada suhu ruang [1].']}, {'h': 'Ruang muai: alasan pengisian hanya 80 sampai 85 persen', 't': 13, 'paras': ['Cairan memuai ketika suhu naik, dan pemuaian itu memerlukan ruang. Karena itu tabung LPG hanya diisi 80 sampai 85 persen dari kapasitasnya, dan sisa ruang di atas cairan berfungsi sebagai ruang muai sekaligus tempat uap berada [1].', 'Apabila tabung diisi penuh tanpa ruang sisa, kenaikan suhu akan memaksa cairan yang memuai menekan dinding tabung tanpa ruang untuk berkembang. Ruang kosong yang tampak seperti kekurangan isi tersebut sesungguhnya adalah bagian dari desain keselamatannya [1][3].']}, {'h': 'Katup dibuka: pendidihan dan pengembangan volume', 't': 20, 'paras': ['Pada saat katup dibuka, tekanan di atas cairan turun dan kesetimbangan bergeser. Cairan mulai mendidih pada suhu ruang, berubah menjadi gas, dan mengalir keluar menuju kompor, sedangkan cairan yang tersisa terus menguap untuk menggantikan gas yang terpakai [3].', 'Perubahan fasa ini disertai pengembangan volume yang besar: satu liter LPG cair mengembang menjadi sekitar 250 liter gas. Rasio sekitar 250 berbanding 1 inilah alasan penyimpanan sebagai cairan jauh lebih ringkas daripada penyimpanan sebagai gas pada tekanan rendah [1].']}, {'h': 'Dua akibat yang teramati: tabung dingin dan gas mengendap', 't': 27, 'paras': ['Pendidihan memerlukan panas laten, dan panas itu diambil dari cairan serta dinding tabung. Akibatnya tabung terasa dingin pada saat dipakai, dan pada pemakaian besar embun dapat terbentuk pada dinding luarnya [3].', 'Akibat kedua berkaitan dengan keselamatan: uap LPG lebih berat daripada udara, sehingga gas yang bocor tidak naik dan tersebar, melainkan turun dan mengendap di lantai. Karena itu kebocoran LPG berbahaya terutama pada ruang tertutup, dan bau khasnya berasal dari odorant etil merkaptan yang sengaja ditambahkan agar kebocoran terdeteksi [1][2].']}], 'refs': ['Wikipedia contributors. Liquefied petroleum gas. Wikipedia, The Free Encyclopedia.', 'Energypedia. Liquefied Petroleum Gas (LPG). energypedia.info.', 'Elgas. LPG Liquid vs Vapour. elgas.com.au.']},
    'ntu-efektivitas-penukar-panas': {'lead': 'Sebuah penukar panas terpasang di pabrik dan suhu keluarnya belum terukur. Berapa duty yang sebenarnya dipindahkan alat tersebut, dan berapa suhu keluar kedua alirannya?', 'sections': [{'h': 'Masalah suhu keluar yang belum diketahui', 't': 0, 'paras': ['Metode beda suhu rata-rata logaritmik (LMTD) menghitung duty dari beda suhu di kedua ujung penukar panas. Apabila suhu keluar belum diketahui, beda suhu tersebut belum dapat dihitung, sehingga perancang harus menebak suhu keluar, menghitung, lalu mengulang perhitungan sampai tebakannya konsisten [1].', 'Metode NTU efektivitas membalik urutan itu. Perhitungan dimulai dari besaran yang memang diketahui, yaitu suhu masuk kedua aliran, laju kapasitas panas masing-masing aliran, dan nilai UA penukar panas. Suhu keluar bukan masukan, melainkan hasil akhir perhitungan [1].']}, {'h': 'Laju kapasitas panas, rasio kapasitas, dan perpindahan panas maksimum', 't': 5, 'paras': ['Laju kapasitas panas C didefinisikan sebagai C = m dot cp, hasil kali laju aliran massa dan panas jenis. Pada contoh ini, aliran panas memiliki Ch 2 kW/K dan aliran dingin memiliki Cc 4 kW/K, sehingga Cmin adalah 2 kW/K dan Cmax adalah 4 kW/K [1].', 'Rasio kapasitas Cr = Cmin/Cmax = 2/4 = 0,50, dan nilainya selalu berada di antara 0 dan 1. Dari Cmin pula dihitung perpindahan panas maksimum yang mungkin, Qmax = Cmin (Th,in dikurangi Tc,in) = 2 x 90 = 180 kW, yaitu duty batas apabila penukar panas counterflow berukuran tak berhingga [1].']}, {'h': 'NTU sebagai ukuran relatif penukar panas', 't': 11, 'paras': ['Jumlah satuan perpindahan didefinisikan sebagai NTU = UA/Cmin. Dengan UA 2 kW/K dan Cmin 2 kW/K, diperoleh NTU 1,00. Besaran ini tidak berdimensi dan menyatakan ukuran penukar panas relatif terhadap laju kapasitas panas terkecil [1].', 'Makna praktisnya terletak pada perbandingan tersebut. Penukar panas yang sama akan memberikan NTU berbeda apabila dipasang pada aliran dengan Cmin berbeda, karena kemampuan aliran menyerap panas menentukan seberapa jauh suhu dapat berubah di dalam alat [1].']}, {'h': 'Efektivitas counterflow dan duty aktual', 't': 17.5, 'paras': ['Untuk aliran counterflow dengan Cr kurang dari 1, relasi efektivitas NTU memberikan epsilon 0,565 pada NTU 1,00 dan Cr 0,50. Efektivitas adalah perbandingan antara duty aktual dan duty maksimum yang mungkin, epsilon = Q/Qmax [1].', 'Duty aktualnya mengikuti langsung: Q = epsilon Qmax = 101,65 kW, yaitu 56,5 persen dari Qmax. Angka ini diperoleh tanpa satu pun suhu keluar yang ditebak, dan titik kerja yang sama terbaca pada kurva efektivitas untuk Cr 0,5 [1].']}, {'h': 'Suhu keluar dari neraca energi dan batas pemakaian metode', 't': 24, 'paras': ['Suhu keluar diperoleh dari neraca energi masing-masing aliran. Hasilnya, aliran panas keluar pada 69,2 derajat C dan aliran dingin keluar pada 55,4 derajat C. Pemeriksaan konsistensinya tertutup: Ch kali delta Th sama dengan Cc kali delta Tc sama dengan Q sebesar 101,65 kW [1].', 'Metode ini paling tepat dipakai pada saat suhu keluar belum diketahui, misalnya pada rating penukar panas yang sudah terpasang. Apabila kedua suhu keluar sudah diketahui, metode LMTD justru lebih langsung, sehingga pemilihan metode ditentukan oleh besaran yang tersedia, bukan oleh kebiasaan [1][2].']}], 'refs': ['Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2007). Fundamentals of Heat and Mass Transfer (6th ed.). John Wiley & Sons.', "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education."]},
    'steam-trap-katup-kondensat': {'lead': 'Sebuah katup kecil di titik rendah sistem steam menentukan apakah energi boiler mengalir ke proses atau terbuang ke jalur pembuangan. Apa yang sebenarnya dipisahkan oleh steam trap, dan mengapa kegagalannya hampir tidak pernah terlihat?', 'sections': [{'h': 'Tugas ganda: membuang air, menahan steam', 't': 0, 'paras': ['Steam trap adalah katup otomatis yang dipasang pada titik rendah sistem steam. Tugasnya ganda dan tampak bertentangan: kondensat harus dibuang secepatnya, sedangkan steam hidup tidak boleh ikut lolos melalui jalur pembuangan yang sama [1].', 'Seluruh tugas itu dikerjakan secara otomatis tanpa listrik dan tanpa operator yang berjaga. Trap membuka dan menutup berdasarkan keadaan fluida yang tiba di dalamnya, sehingga pemisahan air dan steam berlangsung terus selama sistem beroperasi [1][3].']}, {'h': 'Asal kondensat: steam yang melepaskan panas laten', 't': 6.5, 'paras': ['Steam membawa energi dalam bentuk panas laten dan melepaskannya ketika memanaskan peralatan atau ketika kehilangan panas ke lingkungan melalui dinding pipa. Steam yang telah melepaskan panas latennya berubah menjadi air panas yang disebut kondensat [1].', 'Kondensat selalu terbentuk selama sistem steam beroperasi, termasuk pada jalur distribusi yang terisolasi dengan baik. Persoalannya bukan mencegah kondensat terbentuk, melainkan mengeluarkannya dari tempat yang tidak memerlukannya [1][2].']}, {'h': 'Akibat kondensat yang tertahan: water hammer dan perpindahan panas menurun', 't': 13, 'paras': ['Kondensat yang tidak dibuang menggenang di dasar pipa dan di dalam peralatan. Genangan itu mengurangi ruang efektif untuk perpindahan panas, karena permukaan yang tertutup air tidak lagi berkontak langsung dengan steam yang membawa panas laten [1].', 'Bahaya mekanisnya adalah water hammer: genangan air yang terseret aliran steam menabrak belokan atau katup sebagai massa cairan yang hampir tidak termampatkan, dan gelombang kejutnya dapat merusak pipa serta sambungannya [1].']}, {'h': 'Tiga keluarga steam trap dan prinsip kerjanya', 't': 20, 'paras': ['Keluarga mekanis bekerja berdasarkan perbedaan densitas air dan steam. Pada tipe pelampung, bola pelampung naik mengikuti level kondensat dan membuka katup pembuangan; pada tipe ember terbalik, ember yang terisi steam mengapung dan menutup katup, lalu tenggelam ketika steam di dalamnya mengembun dan membukanya kembali [1][3].', 'Keluarga termostatik bekerja berdasarkan perbedaan suhu, misalnya elemen bimetal yang melengkung mengikuti suhu kondensat, sedangkan keluarga termodinamik bekerja berdasarkan perbedaan perilaku aliran, dengan cakram yang membuka dan menutup cepat oleh steam kilat. Pemilihan keluarga dan tipe ditentukan oleh tekanan kerja dan beban kondensat pada titik pemasangannya [1][3].']}, {'h': 'Kegagalan terbuka yang tidak terlihat dan audit trap', 't': 29, 'paras': ['Kegagalan yang paling merugikan adalah trap yang gagal terbuka. Trap semacam itu membuang steam hidup secara kontinu melalui jalur pembuangan, dan kebocorannya sulit terlihat karena wujud steam yang lolos tampak sama dengan buangan kondensat yang normal [2].', 'Kerugiannya muncul secara tidak langsung, antara lain sebagai tagihan bahan bakar yang membengkak karena boiler harus menghasilkan steam pengganti. Karena itu audit rutin memeriksa kondisi trap dengan termografi atau ultrasonik, agar trap yang gagal terbuka terdeteksi dari suhu dan bunyinya, bukan dari besarnya kerugian yang telah terjadi [2].']}], 'refs': ['Spirax Sarco. Steam Trapping and Condensate Recovery.', 'U.S. Department of Energy. Steam Best Practices.', 'Armstrong International. Steam Trap Handbook.']}
}


def render_video_article(v):
    # ILM-R63: halaman video = artikel versi baca; label struktur produksi tidak boleh tampil ke pembaca
    art = VIDEO_ARTICLES[v["slug"]]
    out = '<section class="article-body">\n'
    for sec in art["sections"]:
        t = sec.get("t")
        if t is not None:
            out += (f'<h2 class="art-h" data-start="{t}">{esc(sec["h"])}'
                    f' <button class="seek" type="button" data-start="{t}" title="Lompat ke bagian ini di video">&#9654; {fmt_time(t)}</button></h2>\n')
        else:
            out += f'<h2 class="art-h">{esc(sec["h"])}</h2>\n'
        for p in sec["paras"]:
            out += f"<p>{esc(p)}</p>\n"
    out += "</section>\n"
    return out


def paras_of(caption):
    parts = [clean_text(p) for p in str(caption or "").split("\n")]
    out = []
    for p in parts:
        if not p or p.startswith("#"):
            continue
        if p.lower().startswith("follow @ilmutekkim"):
            continue
        out.append(p)
    return out


def resolve_img(path, slug, name):
    """Kompres gambar dari workspace IG ke assets/img/<slug>/<name>.jpg (maks 1280px, q80)."""
    if not path:
        return None
    p = str(path)
    if not os.path.isabs(p):
        p = os.path.join(SRC, p)
    if not os.path.isfile(p):
        return None
    dst_dir = os.path.join(ROOT, "assets", "img", slug)
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name + ".jpg")
    if not os.path.exists(dst):
        try:
            from PIL import Image
            im = Image.open(p).convert("RGB")
            if im.width > 1280:
                im = im.resize((1280, int(im.height * 1280 / im.width)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=80, optimize=True)
        except Exception:
            shutil.copyfile(p, dst)
    return f"/assets/img/{slug}/{name}.jpg"


def fmt_time(sec):
    sec = float(sec or 0)
    m = int(sec // 60)
    s = int(round(sec % 60))
    if s == 60:
        m += 1
        s = 0
    return f"{m}:{s:02d}"


def resolve_video(v):
    """Salin/kompres MP4 sumber ke assets/video/<slug>.mp4 (720p, crf 28) + poster. Return (video_url, poster_url)."""
    import subprocess
    slug = v["slug"]
    src = os.path.expanduser(v["src"])
    dst_dir = os.path.join(ROOT, "assets", "video")
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, slug + ".mp4")
    poster = os.path.join(dst_dir, slug + "-poster.jpg")
    vurl = f"/assets/video/{slug}.mp4"
    purl = f"/assets/video/{slug}-poster.jpg"
    if not os.path.isfile(src):
        return None, None
    if not os.path.exists(dst):
        try:
            subprocess.run(["ffmpeg", "-y", "-i", src, "-vf", "scale=720:-2",
                            "-c:v", "libx264", "-crf", "28", "-preset", "medium",
                            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", dst],
                           check=True, capture_output=True, timeout=300)
        except Exception:
            shutil.copyfile(src, dst)
    if not os.path.exists(poster):
        psrc = os.path.expanduser(v["poster_src"]) if v.get("poster_src") else None
        done = False
        if psrc and os.path.isfile(psrc):
            try:
                from PIL import Image
                im = Image.open(psrc).convert("RGB")
                if im.width > 720:
                    im = im.resize((720, int(im.height * 720 / im.width)), Image.LANCZOS)
                im.save(poster, "JPEG", quality=82, optimize=True)
                done = True
            except Exception:
                pass
        if not done:
            try:
                subprocess.run(["ffmpeg", "-y", "-ss", "1.2", "-i", dst, "-frames:v", "1",
                                "-q:v", "3", poster], check=True, capture_output=True, timeout=60)
            except Exception:
                pass
    if not os.path.exists(poster):
        purl = None
    return vurl, purl


def seg_text(segments):
    if isinstance(segments, list):
        return clean_text("".join(str(x[0]) if isinstance(x, (list, tuple)) else str(x)
                                  for x in segments))
    return clean_text(segments)


def rows_html(rows):
    if not rows:
        return ""
    items = []
    for r in rows:
        if not isinstance(r, (list, tuple)):
            continue
        cells = [clean_text(c) for c in r]
        if len(cells) >= 3:
            items.append(f'<li><span class="step-num">{esc(cells[0])}</span>'
                         f'<div><strong>{esc(cells[1])}</strong>'
                         f'<p>{esc(cells[2])}</p></div></li>')
        elif len(cells) == 2:
            items.append(f'<li><div><strong>{esc(cells[0])}</strong>'
                         f'<p>{esc(cells[1])}</p></div></li>')
        elif len(cells) == 1:
            items.append(f"<li><div><p>{esc(cells[0])}</p></div></li>")
    return '<ol class="steps">' + "".join(items) + "</ol>" if items else ""


def slide_section(s, slug, idx):
    stype = s.get("type", "body")
    title = clean_text(s.get("title") or "")
    pill = clean_text(s.get("pill") or "")
    paras = [clean_text(p) for p in s.get("paras", []) if clean_text(p)]
    callout = clean_text(s.get("callout") or "")
    out = []
    head = title or pill
    if stype == "quote":
        q = clean_text(s.get("quote") or "")
        h = clean_text(s.get("hook") or "")
        out.append('<section class="misconception"><p class="eyebrow">Yang sering dikira</p>')
        if q:
            out.append(f'<blockquote>&ldquo;{esc(q)}&rdquo;</blockquote>')
        if h:
            out.append(f"<p>{esc(h)}</p>")
        out.append("</section>")
    elif stype == "conclusion":
        h = clean_text(s.get("head") or "")
        bullets = [clean_text(b) for b in s.get("bullets", []) if clean_text(b)]
        eq = clean_text(s.get("equation") or "")
        out.append('<section class="conclusion"><p class="eyebrow">Kesimpulan</p>')
        if h:
            out.append(f"<h2>{esc(h)}</h2>")
        if bullets:
            out.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in bullets) + "</ul>")
        if eq:
            out.append(f'<div class="formula">{esc(eq)}</div>')
        out.append("</section>")
    else:
        out.append("<section>")
        if head:
            out.append(f"<h2>{esc(head)}</h2>")
        for p in paras:
            out.append(f"<p>{esc(p)}</p>")
        fig = None
        for key, name in (("photo", f"foto-{idx}"), ("diagram", f"diagram-{idx}")):
            if s.get(key):
                url = resolve_img(s.get(key), slug, name)
                if url:
                    fig = (url, s.get("credit"), s.get("credit_url"))
                    break
        if fig:
            url, credit, curl = fig
            cap = ""
            if credit:
                cap = f'Foto: {esc(credit)}'
                if curl:
                    cap = f'Foto: <a href="{esc(curl)}" rel="noopener" target="_blank">{esc(credit)}</a>'
            out.append(f'<figure><img src="{url}" alt="{esc(head)}" loading="lazy">'
                       + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
        out.append(rows_html(s.get("fill_rows")))
        out.append(rows_html(s.get("fill_cards")))
        grid = s.get("fill_grid")
        if grid:
            cards = []
            for r in grid:
                if isinstance(r, (list, tuple)) and len(r) >= 2:
                    cards.append(f'<div class="mini-card"><strong>{esc(clean_text(r[0]))}</strong>'
                                 f'<p>{esc(clean_text(r[1]))}</p></div>')
            if cards:
                out.append('<div class="mini-grid">' + "".join(cards) + "</div>")
        formula = clean_text(s.get("formula") or s.get("equation") or "")
        if formula:
            out.append(f'<div class="formula">{esc(formula)}</div>')
        bullets = [clean_text(b) for b in s.get("bullets", []) if clean_text(b)]
        if bullets:
            out.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in bullets) + "</ul>")
        out.append("</section>")
    if callout and stype != "conclusion":
        out.append(f'<aside class="fact">{esc(callout)}</aside>')
    return "\n".join(x for x in out if x)


def before_after_sections(d, slug):
    out = []
    bad = clean_text(d.get("bad_prompt") or "")
    bad_hook = clean_text(d.get("bad_hook_line") or "")
    out.append('<section class="misconception"><p class="eyebrow">Masalahnya</p>')
    if bad:
        out.append(f'<blockquote>&ldquo;{esc(bad)}&rdquo;</blockquote>')
    if bad_hook:
        out.append(f"<p>{esc(bad_hook)}</p>")
    out.append("</section>")
    res = d.get("bad_result_lines")
    if isinstance(res, list):
        items = "".join(f"<li>{esc(clean_text(x))}</li>" for x in res if clean_text(x))
        syms = d.get("slide3_symbols") or []
        if syms:
            items = "".join(
                f"<li><strong>{esc(clean_text(x.get('name')))}:</strong> {esc(clean_text(x.get('desc')))}</li>"
                for x in syms)
        if items:
            out.append(f"<section><h2>{esc(clean_text(d.get('bad_result_pill') or 'Yang perlu diketahui'))}</h2>"
                       f"<ul>{items}</ul></section>")
    elif clean_text(res):
        out.append(f"<section><h2>{esc(clean_text(d.get('bad_result_pill') or 'Kenyataannya'))}</h2>"
                   f"<p>{esc(clean_text(res))}</p></section>")
    if clean_text(d.get("bad_why")):
        out.append(f"<section><h2>{esc(clean_text(d.get('bad_why_title') or 'Kenapa bisa begitu'))}</h2>"
                   f"<p>{esc(clean_text(d.get('bad_why')))}</p></section>")
    good = seg_text(d.get("good_prompt_segments"))
    if good:
        out.append(f"<section><h2>{esc(clean_text(d.get('good_pill') or 'Cara yang benar'))}</h2>"
                   f"<p>{esc(good)}</p></section>")
    if clean_text(d.get("good_why")):
        out.append(f"<section><h2>{esc(clean_text(d.get('good_why_title') or 'Intinya'))}</h2>"
                   f"<p>{esc(clean_text(d.get('good_why')))}</p></section>")
    gr = d.get("good_result_lines")
    if isinstance(gr, list):
        body = "".join(f"<p>{esc(clean_text(x))}</p>" for x in gr if clean_text(x))
    else:
        body = f"<p>{esc(clean_text(gr))}</p>" if clean_text(gr) else ""
    if body:
        out.append(f"<section><h2>{esc(clean_text(d.get('good_result_pill') or 'Contoh nyata'))}</h2>{body}</section>")
    if clean_text(d.get("conclusion_head")) or clean_text(d.get("conclusion_body")):
        out.append('<section class="conclusion"><p class="eyebrow">Kesimpulan</p>'
                   f"<h2>{esc(clean_text(d.get('conclusion_head')))}</h2>"
                   f"<p>{esc(clean_text(d.get('conclusion_body')))}</p></section>")
    return "\n".join(out)


HEAD = """<!DOCTYPE html>
<html lang="id">
<head>
<script>(function(){{try{{var t=localStorage.getItem("ilm-theme");if(!t){{t=window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}}document.documentElement.setAttribute("data-theme",t);}}catch(e){{document.documentElement.setAttribute("data-theme","light");}}}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
{ogimg}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v=23">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23131518'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23F4F4F2' font-family='Arial' font-weight='bold'>IT</text></svg>">
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
<link rel="stylesheet" href="/kamus/assets/chat.css">
</head>
<body>
<header class="site-header">
  <a class="brand" href="/">ilmu<span>tekkim</span></a>
  <button type="button" class="theme-toggle" id="themeToggle" aria-label="Beralih antara mode terang dan mode gelap" title="Mode terang / gelap"><span class="ic-sun" aria-hidden="true">&#9728;</span><span class="ic-moon" aria-hidden="true">&#9790;</span></button>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
  <label for="nav-toggle" class="burger" aria-label="Buka menu">&#9776;</label>
  <nav>
    <a href="/">Articles &amp; Videos</a>
    <a href="/riset/">Riset</a>
    <a href="/jalur/">Jalur</a>
    <a href="/kamus">Kamus</a>
  </nav>
</header>
<main>
"""

FOOT = """
</main>
<footer>
  <div class="foot-brand">ilmu<span>tekkim</span></div>
  <p>Kajian teknik kimia proses: unit operasi, alur pabrik, keselamatan proses, dan kecerdasan buatan. Ditulis oleh insinyur kimia lulusan Institut Teknologi Bandung.</p>
  <p class="foot-btns"><a class="btn-ig" href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">Instagram @ilmutekkim</a> <a class="btn-ig" href="https://www.tiktok.com/@ilmutekkim" target="_blank" rel="noopener">TikTok @ilmutekkim</a></p>
  <p class="foot-links"><a href="/">Beranda</a><span>&middot;</span><a href="/video/">Video</a><span>&middot;</span><a href="/riset/">Riset</a><span>&middot;</span><a href="/jalur/">Jalur</a><span>&middot;</span><a href="/kamus">Kamus</a><span>&middot;</span><a href="/referensi/">Referensi</a><span>&middot;</span><a href="/kalkulator/">Kalkulator</a><span>&middot;</span><a href="/tentang/">Tentang</a></p>
  <p class="fine">Artikel dan video di situs ini merupakan versi baca dan versi tonton dari konten Instagram @ilmutekkim. Foto berasal dari Pexels dan Unsplash, kredit tercantum di tiap gambar.</p>
</footer>
<script src="/assets/js/main.js?v=11"></script>
<script defer src="/kamus/assets/chat.js"></script>
</body>
</html>
"""



def load_deep(slug):
    fp = os.path.join(ROOT, "deep", slug + ".json")
    if os.path.isfile(fp):
        try:
            return json.load(open(fp))
        except Exception:
            return None
    return None


def article_figures(d, slug):
    figs = []
    for idx, s in enumerate(d.get("slides", []), 1):
        for key, name in (("photo", f"foto-{idx}"), ("diagram", f"diagram-{idx}")):
            if s.get(key):
                url = resolve_img(s.get(key), slug, name)
                if url:
                    figs.append((url, s.get("credit"), s.get("credit_url"),
                                 clean_text(s.get("title") or "")))
                    break
    return figs


def _ref_key(r):
    return "".join(ch for ch in str(r).lower() if ch.isalnum())[:40]


def merge_refs(deep_refs, spec_refs):
    out = [clean_text(r) for r in (deep_refs or []) if clean_text(r)]
    keys = {_ref_key(r) for r in out}
    for r in spec_refs or []:
        if _ref_key(r) not in keys:
            out.append(r)
            keys.add(_ref_key(r))
    return out


def render_deep_body(deep, figs):
    # ILM-R64: artikel mendalam akademis (hook kitab suci, prose per subtopik, fakta, sitasi)
    out = []
    fi = 0

    def fig_html(fig):
        url, credit, curl, head = fig
        cap = ""
        if credit:
            cap = f'Foto: {esc(credit)}'
            if curl:
                cap = f'Foto: <a href="{esc(curl)}" rel="noopener" target="_blank">{esc(credit)}</a>'
        return (f'<figure><img src="{url}" alt="{esc(head)}" loading="lazy">'
                + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")

    for sec in deep.get("sections") or []:
        out.append("<section>")
        if sec.get("h"):
            out.append(f"<h2>{esc(sec['h'])}</h2>")
        for p in sec.get("paras") or []:
            if clean_text(p):
                out.append(f"<p>{esc(p)}</p>")
        out.append("</section>")
        if fi < len(figs):
            out.append(fig_html(figs[fi]))
            fi += 1
    while fi < len(figs):
        out.append(fig_html(figs[fi]))
        fi += 1
    facts = [clean_text(f) for f in (deep.get("facts") or []) if clean_text(f)]
    if facts:
        out.append('<section class="factbox"><h2>Fakta kunci</h2><ul>'
                   + "".join(f"<li>{esc(f)}</li>" for f in facts) + "</ul></section>")
    closing = clean_text(deep.get("closing") or "")
    if closing:
        out.append(f'<section><h2>Kesimpulannya</h2><p>{esc(closing)}</p></section>')
    return "\n".join(x for x in out if x)



def load_research():
    rdir = os.path.join(ROOT, "research")
    items = []
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            if f.endswith(".json"):
                items.append(json.load(open(os.path.join(rdir, f))))
    items.sort(key=lambda d: d.get("date_bedah", ""), reverse=True)
    return items


def authors_short(authors):
    a = [str(x) for x in (authors or []) if str(x).strip()]
    if len(a) > 3:
        return ", ".join(a[:3]) + ", dkk."
    return ", ".join(a)


def render_bedah(d):
    # ILM-R65: halaman bedah riset (masalah, metode, temuan, batas kritis, arti pabrik, kesimpulan)
    out = []
    out.append(f'<p class="cov-label">{esc(d["coverage"])}</p>')
    out.append(f'<p class="lead">{esc(d["lead"])}</p>')
    cov = resolve_img(d.get("cover_file"), d["slug"], "cover")
    if cov:
        out.append(f'<figure><img src="{cov}" alt="{esc(d["judul"])}">'
                   f'<figcaption>{esc(d.get("cover_credit") or "")}</figcaption></figure>')
    out.append('<section class="paper-box"><p class="eyebrow">Paper yang dibedah</p>'
               f'<h2 class="paper-title">{esc(d["paper_title"])}</h2>'
               f'<p>{esc(authors_short(d["authors"]))} &middot; {esc(d["journal"])} &middot; {esc(str(d["year"]))}</p>'
               f'<a class="btn ghost" href="{esc(d["doi"])}" target="_blank" rel="noopener">Buka DOI paper</a></section>')
    out.append(f'<section><h2>Masalah yang diselesaikan</h2><p>{esc(d["masalah"])}</p></section>')
    out.append(f'<section><h2>Metode dan skala</h2><p>{esc(d["metode"])}</p></section>')
    out.append('<section><h2>Temuan kunci</h2><ul>'
               + "".join(f"<li>{esc(x)}</li>" for x in d["temuan"]) + "</ul></section>")
    out.append('<section><h2>Batas dan catatan kritis</h2><ul>'
               + "".join(f"<li>{esc(x)}</li>" for x in d["batas"]) + "</ul></section>")
    out.append(f'<section><h2>Arti buat pabrik</h2><p>{esc(d["arti_pabrik"])}</p></section>')
    out.append(f'<section class="verdict"><p class="eyebrow">Kesimpulan bedah</p><h2>{esc(d["vonis"])}</h2>'
               f'<p>{esc(d["vonis_alasan"])}</p></section>')
    if d.get("terkait"):
        links = "".join(
            f'<a class="btn ghost" href="/{ "artikel" if t["type"] == "artikel" else "video" }/{esc(t["slug"])}/">{esc(t["title"])}</a> '
            for t in d["terkait"])
        out.append(f'<section><h2>Baca terkait di ilmutekkim</h2><p>{links}</p></section>')
    return "\n".join(out)


def load_paten():
    pdir = os.path.join(ROOT, "paten")
    items = []
    if os.path.isdir(pdir):
        for f in sorted(os.listdir(pdir)):
            if f.endswith(".json"):
                items.append(json.load(open(os.path.join(pdir, f))))
    items.sort(key=lambda d: d.get("date_bedah", ""), reverse=True)
    return items


def render_paten(d):
    # ILM-R66: halaman bedah paten (masalah, klaim parafrase, cara kerja, batas, arti pabrik, kesimpulan)
    out = []
    out.append(f'<p class="cov-label">{esc(d["coverage"])}</p>')
    out.append(f'<p class="lead">{esc(d["lead"])}</p>')
    cov = resolve_img(d.get("cover_file"), d["slug"], "cover")
    if cov:
        out.append(f'<figure><img src="{cov}" alt="{esc(d["judul"])}">'
                   f'<figcaption>{esc(d.get("cover_credit") or "")}</figcaption></figure>')
    out.append('<section class="paper-box"><p class="eyebrow">Paten yang dibedah</p>'
               f'<h2 class="paper-title">{esc(d["judul_paten"])}</h2>'
               f'<p>{esc(d["nomor"])} &middot; Inventor: {esc(d["inventor"])} &middot; Pemilik saat terbit: {esc(d["pemilik"])}</p>'
               f'<p>Diajukan {esc(d["diajukan"])} &middot; Terbit {esc(d["terbit"])}</p>'
               f'<p><strong>Status:</strong> {esc(d["status"])}</p>'
               f'<a class="btn ghost" href="{esc(d["sumber"])}" target="_blank" rel="noopener">Buka dokumen paten</a></section>')
    out.append(f'<section><h2>Masalah yang diselesaikan</h2><p>{esc(d["masalah"])}</p></section>')
    out.append('<section><h2>Klaim inti, dengan kata kami</h2><p class="meta">Klaim paten adalah teks hukum; di bawah ini parafrasenya, bukan salinan.</p><ul>'
               + "".join(f"<li>{esc(x)}</li>" for x in d["klaim"]) + "</ul></section>")
    out.append(f'<section><h2>Cara kerjanya</h2><p>{esc(d["cara"])}</p></section>')
    out.append('<section><h2>Batas dan catatan kritis</h2><ul>'
               + "".join(f"<li>{esc(x)}</li>" for x in d["batas"]) + "</ul></section>")
    out.append(f'<section><h2>Arti buat pabrik</h2><p>{esc(d["arti"])}</p></section>')
    out.append(f'<section class="verdict"><p class="eyebrow">Kesimpulan bedah</p><h2>{esc(d["kesimpulan"])}</h2>'
               f'<p>{esc(d["kesimpulan_alasan"])}</p></section>')
    if d.get("terkait"):
        links = "".join(
            f'<a class="btn ghost" href="/{ "artikel" if t["type"] == "artikel" else "video" }/{esc(t["slug"])}/">{esc(t["title"])}</a> '
            for t in d["terkait"])
        out.append(f'<section><h2>Baca terkait di ilmutekkim</h2><p>{links}</p></section>')
    return "\n".join(out)


def load_jalur():
    fp = os.path.join(ROOT, "jalur.json")
    return json.load(open(fp)) if os.path.exists(fp) else []


def load_glosarium():
    fp = os.path.join(ROOT, "glosarium.json")
    return json.load(open(fp)) if os.path.exists(fp) else []


def _kamus_key(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def _kamus_slug(value):
    return re.sub(r"[^a-z0-9]+", "-", _kamus_key(value)).strip("-")


def load_kamus_catalog(glosarium):
    """Katalog Kamus gabungan untuk strip beranda dan sitemap.

    Istilah glosarium lama yang sudah memiliki entri dalam tidak dihitung
    sebagai entri dasar terpisah; entri dalamnya yang menjadi kanonis.
    """
    terms_fp = os.path.join(ROOT, "kamus-data", "terms.json")
    sectors_fp = os.path.join(ROOT, "kamus-data", "sectors.json")
    if not (os.path.exists(terms_fp) and os.path.exists(sectors_fp)):
        return {"deep_slugs": [], "dasar_slugs": [], "sector_slugs": [], "total": len(glosarium)}
    deep_terms = json.load(open(terms_fp))
    sector_meta = json.load(open(sectors_fp))
    deep_keys = set()
    for term in deep_terms:
        for value in [term.get("term", ""), term.get("slug", "")] + term.get("aliases", []):
            deep_keys.add(_kamus_key(value))
            deep_keys.add(_kamus_slug(value))
    dasar_slugs = []
    for entry in glosarium:
        slug = _kamus_slug(entry["term"])
        if _kamus_key(entry["term"]) not in deep_keys and slug not in deep_keys:
            dasar_slugs.append(slug)
    return {
        "deep_slugs": [term["slug"] for term in deep_terms],
        "dasar_slugs": dasar_slugs,
        "sector_slugs": [sector["slug"] for sector in sector_meta.get("sectors", [])],
        "total": len(deep_terms) + len(dasar_slugs),
    }


def main():
    # ILM-R65: gate QC bedah riset. Build GAGAL bila satu bedah pun tidak lolos.
    import subprocess
    qc = subprocess.run(["python3", os.path.join(ROOT, "tools", "qc_research.py")],
                        capture_output=True, text=True)
    print(qc.stdout.strip())
    if qc.returncode != 0:
        raise SystemExit("Build dibatalkan: QC riset ILM-R65 gagal")
    # ILM-R66: gate QC bedah paten. Build GAGAL bila satu bedah paten pun tidak lolos.
    qcp = subprocess.run(["python3", os.path.join(ROOT, "tools", "qc_patent.py")],
                         capture_output=True, text=True)
    print(qcp.stdout.strip())
    if qcp.returncode != 0:
        raise SystemExit("Build dibatalkan: QC paten ILM-R66 gagal")
    articles = []
    for slug, rel, title, date, ig, status in ARTICLES:
        d = json.load(open(os.path.join(SRC, rel)))
        series = clean_text(d.get("series_label") or "Teknik Kimia").title()
        cover = resolve_img(d.get("cover_photo") or d.get("cover_image"), slug, "cover")
        lead = paras_of(d.get("caption"))
        if d.get("format") == "before_after":
            body = before_after_sections(d, slug)
        else:
            body = "\n".join(slide_section(s, slug, i)
                             for i, s in enumerate(d.get("slides", []), 1))
        refs = [clean_text(r) for r in d.get("references", []) if clean_text(r)]
        deep = load_deep(slug)
        deep_lead = ""
        if deep:
            body = render_deep_body(deep, article_figures(d, slug))
            refs = merge_refs(deep.get("refs"), refs)
            deep_lead = clean_text(deep.get("lead") or "")
        articles.append(dict(slug=slug, title=title, date=date, ig=ig, status=status,
                             series=series, cover=cover, lead=lead, body=body, refs=refs, deep_lead=deep_lead,
                             sub=clean_text(d.get("cover_sub") or ""),
                             credit=clean_text(d.get("cover_credit") or ""),
                             credit_url=d.get("credit_url") or d.get("cover_credit_url") or "",
                             teaser=clean_text(d.get("cta_teaser") or "")))
    articles.sort(key=lambda a: a["date"], reverse=True)

    # siapkan video (salin/kompres sekali)
    videos = []
    for v in VIDEOS:
        vurl, purl = resolve_video(v)
        vv = dict(v)
        vv["video_url"] = vurl
        vv["poster_url"] = purl
        videos.append(vv)
    videos.sort(key=lambda x: x["date"], reverse=True)

    # halaman artikel
    for i, a in enumerate(articles):
        url = f"{BASE}/artikel/{a['slug']}/"
        desc = (a.get("deep_lead") or (a["lead"][0] if a["lead"] else a["sub"]))[:155]  # ILM-R69: meta dari lead formal
        ogimg = f'<meta property="og:image" content="{BASE}{a["cover"]}">\n' if a["cover"] else ""
        page = HEAD.format(title=f"{esc(a['title'])} | ilmutekkim", desc=esc(desc),
                           url=url, ogtype="article", ogimg=ogimg)
        page += '<article class="post">\n'
        page += f'<p class="eyebrow">{esc(a["series"])}</p>\n<h1>{esc(a["title"])}</h1>\n'
        meta = f'<p class="meta">{tgl_indo(a["date"])} &middot; ilmutekkim'
        if a["status"] == "arsip":
            meta += " &middot; arsip produksi"
        meta += "</p>"
        page += meta + "\n"
        if a["ig"]:
            page += (f'<p class="ig-link">Versi carousel: '
                     f'<a href="{a["ig"]}" target="_blank" rel="noopener">lihat di Instagram @ilmutekkim</a></p>\n')
        if a["cover"]:
            cap = ""
            if a["credit"]:
                cap = f'Foto: {esc(a["credit"])}'
                if a["credit_url"]:
                    cap = (f'Foto: <a href="{esc(a["credit_url"])}" rel="noopener" '
                           f'target="_blank">{esc(a["credit"])}</a>')
            page += (f'<figure class="hero-img"><img src="{a["cover"]}" alt="{esc(a["title"])}">'
                     + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>\n")
        if a.get("deep_lead"):
            page += f'<p class="lead">{esc(a["deep_lead"])}</p>\n'
        else:
            if a["sub"]:
                page += f'<p class="lead">{esc(a["sub"])}</p>\n'
            for p in a["lead"][:2]:
                page += f'<p class="intro">{esc(p)}</p>\n'
        page += a["body"] + "\n"
        if a["refs"]:
            page += ('<section class="refs"><h2>Referensi</h2><ul>'
                     + "".join(f"<li>{esc(r)}</li>" for r in a["refs"]) + "</ul></section>\n")
        prev_a = articles[i + 1] if i + 1 < len(articles) else None
        next_a = articles[i - 1] if i > 0 else None
        page += '<nav class="post-nav">'
        if prev_a:
            page += f'<a href="/artikel/{prev_a["slug"]}/">&larr; {esc(prev_a["title"])}</a>'
        if next_a:
            page += f'<a href="/artikel/{next_a["slug"]}/">{esc(next_a["title"])} &rarr;</a>'
        page += "</nav>\n"
        page += ('<div class="cta-box"><h2>Lanjut baca di Instagram</h2>'
                 "<p>Konten teknik kimia tiap hari: proses pabrik, safety, dan cara baca alat. "
                 "Ditulis insinyur kimia ITB.</p>"
                 '<a class="btn" href="https://www.instagram.com/ilmutekkim" target="_blank" '
                 'rel="noopener">Follow @ilmutekkim</a></div>\n')
        page += "</article>" + FOOT
        out = os.path.join(ROOT, "artikel", a["slug"])
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "index.html"), "w").write(page)

    # halaman video detail + indeks video
    for vi, v in enumerate(videos):
        vurl_page = f"{BASE}/video/{v['slug']}/"
        desc_v = clean_text(v["intro"])[:155]
        ogimg_v = f'<meta property="og:image" content="{BASE}{v["poster_url"]}">\n' if v.get("poster_url") else ""
        page = HEAD.format(title=f"{esc(v['title'])} | Video ilmutekkim", desc=esc(desc_v),
                           url=vurl_page, ogtype="article", ogimg=ogimg_v)
        page += '<article class="post video-post">\n'
        page += f'<p class="eyebrow">Video interaktif &middot; {esc(v["tag"])}</p>\n<h1>{esc(v["title"])}</h1>\n'
        page += f'<p class="meta">{tgl_indo(v["date"])} &middot; {fmt_time(v["duration"])}</p>\n'
        page += (f'<p class="ig-link">Versi Reel: <a href="{v["ig"]}" target="_blank" rel="noopener">tonton di Instagram @ilmutekkim</a></p>\n')
        page += f'<p class="lead">{esc(VIDEO_ARTICLES[v["slug"]].get("lead") or v["hook"])}</p>\n'
        # player interaktif
        poster_attr = f' poster="{esc(v["poster_url"])}"' if v.get("poster_url") else ""
        page += ('<div class="player-wrap">'
                 f'<video id="vplayer" controls playsinline preload="metadata"{poster_attr}>'
                 f'<source src="{esc(v["video_url"] or "")}" type="video/mp4">Browser tidak mendukung video.</video>'
                 '<div class="player-bar"><span id="vnow">0:00</span><div class="track"><div id="vprog"></div></div>'
                 f'<span>{fmt_time(v["duration"])}</span></div>'
                 '<p class="player-hint">Klik tombol &#9654; di judul bagian artikel untuk lompat ke detiknya di video. Bagian yang sedang diputar akan menyala.</p></div>\n')
        # artikel versi baca (ILM-R63)
        page += render_video_article(v)
        if v.get("facts"):
            page += ('<section class="factbox"><h2>Fakta kunci</h2><ul>'
                     + "".join(f"<li>{esc(x)}</li>" for x in v["facts"]) + "</ul></section>\n")
        page += f'<section><h2>Kesimpulannya</h2><p>{esc(v["takeaway"])}</p></section>\n'
        _vrefs = VIDEO_ARTICLES[v["slug"]].get("refs") or []
        if _vrefs:
            page += ('<section class="refs"><h2>Referensi</h2><ol>'
                     + "".join(f"<li>{esc(r)}</li>" for r in _vrefs) + "</ol></section>\n")
        # kuis interaktif
        q = v["quiz"]
        opts = "".join(
            f'<button type="button" class="quiz-opt" data-ok="{1 if i == q["answer"] else 0}">{esc(o)}</button>'
            for i, o in enumerate(q["options"]))
        page += (f'<section class="quiz"><h2>Cek paham (interaktif)</h2><p>{esc(q["q"])}</p>'
                 f'<div class="quiz-opts">{opts}</div>'
                 f'<p class="quiz-explain" hidden>{esc(q["explain"])}</p></section>\n')
        page += ('<div class="cta-box"><h2>Tonton versi Reel-nya</h2>'
                 "<p>Tonton versi singkatnya sebagai Reel di Instagram, atau baca versi lengkapnya di sini sambil lompat ke detik yang mau diulang.</p>"
                 f'<a class="btn" href="{v["ig"]}" target="_blank" rel="noopener">Buka Reel @ilmutekkim</a> '
                 '<a class="btn ghost" href="/video/">Semua video</a></div>\n')
        prev_v = videos[vi + 1] if vi + 1 < len(videos) else None
        next_v = videos[vi - 1] if vi > 0 else None
        page += '<nav class="post-nav">'
        if prev_v:
            page += f'<a href="/video/{prev_v["slug"]}/">&larr; {esc(prev_v["title"])}</a>'
        if next_v:
            page += f'<a href="/video/{next_v["slug"]}/">{esc(next_v["title"])} &rarr;</a>'
        page += "</nav>\n"
        page += "</article>"
        # script interaktif khusus halaman video (seek + highlight + kuis)
        page += """<script>
(function(){
  var vid=document.getElementById('vplayer'); if(!vid) return;
  var prog=document.getElementById('vprog'), now=document.getElementById('vnow');
  var heads=[].slice.call(document.querySelectorAll('.art-h'));
  function fmt(t){t=Math.max(0,t|0);return (t/60|0)+':'+('0'+(t%60)).slice(-2);}
  document.querySelectorAll('.seek').forEach(function(b){
    b.addEventListener('click',function(){
      vid.currentTime=parseFloat(b.dataset.start); vid.play();
    });
  });
  vid.addEventListener('timeupdate',function(){
    var t=vid.currentTime, d=vid.duration||40.9;
    if(prog) prog.style.width=(d? (t/d*100):0)+'%';
    if(now) now.textContent=fmt(t);
    var cur=null;
    heads.forEach(function(h){ if(parseFloat(h.dataset.start)<=t) cur=h; });
    heads.forEach(function(h){ h.classList.toggle('active',h===cur); });
  });
  document.querySelectorAll('.quiz-opt').forEach(function(b){
    b.addEventListener('click',function(){
      var box=b.closest('.quiz'); box.querySelectorAll('.quiz-opt').forEach(function(x){x.classList.remove('right','wrong');});
      b.classList.add(b.dataset.ok==='1'?'right':'wrong');
      var ex=box.querySelector('.quiz-explain'); if(ex) ex.hidden=false;
    });
  });
})();
</script>"""
        page += FOOT
        outv = os.path.join(ROOT, "video", v["slug"])
        os.makedirs(outv, exist_ok=True)
        open(os.path.join(outv, "index.html"), "w").write(page)

    # indeks video /video/
    vcards = ""
    for v in videos:
        thumb = (f'<img src="{v["poster_url"]}" alt="{esc(v["title"])}" loading="lazy">' if v.get("poster_url")
                 else '<div class="no-img">ilmutekkim</div>')
        vcards += (f'<article class="card vcard"><a href="/video/{v["slug"]}/">{thumb}'
                   f'<span class="play-badge">&#9654; {fmt_time(v["duration"])}</span></a><div class="card-body">'
                   f'<p class="eyebrow">{esc(v["tag"])}</p>'
                   f'<h3><a href="/video/{v["slug"]}/">{esc(v["title"])}</a></h3>'
                   f'<p>{esc(v["hook"])}</p>'
                   f'<p class="meta">{tgl_indo(v["date"])} &middot; artikel + kuis</p></div></article>\n')
    vindex = HEAD.format(title="Video Teknik Kimia | ilmutekkim",
                         desc="Versi artikel dari video teknik kimia @ilmutekkim: tonton videonya, baca penjelasan mendalamnya per subtopik, lalu periksa pemahaman melalui kuis.",
                         url=BASE + "/video/", ogtype="website", ogimg="")
    vindex += f"""
<article class="post wide">
<p class="eyebrow">Video</p>
<h1>Video teknik kimia, versi artikel.</h1>
<p class="lead">Sepuluh video teknik kimia dari @ilmutekkim, masing-masing disertai versi artikel yang lengkap.
Video dapat ditonton bersamaan dengan membaca penjelasan mendalam per subtopik, melompat ke detik tertentu dari judul bagiannya, kemudian menjawab kuis pemeriksa pemahaman.</p>
<p class="meta">{len(videos)} video &middot; tersinkron dari Reel @ilmutekkim &middot; diperbarui {tgl_indo(videos[0]["date"]) if videos else ""}</p>
</article>
<section class="grid video-grid">
{vcards}
</section>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "video"), exist_ok=True)
    open(os.path.join(ROOT, "video", "index.html"), "w").write(vindex)


    # halaman riset /riset/ + bedah /riset/<slug>/ (ILM-R65)
    research = load_research()
    paten = load_paten()
    rcards = ""
    for d in research:
        rcards += (f'<article class="card" data-series="{esc(d["topik"])}" '
                   f'data-title="{esc(d["judul"].lower())} {esc(d["topik"].lower())} {esc(d["journal"].lower())}">'
                   f'<a href="/riset/{d["slug"]}/">'
                   + (f'<img src="{resolve_img(d.get("cover_file"), d["slug"], "cover")}" alt="{esc(d["judul"])}" loading="lazy">'
                      if resolve_img(d.get("cover_file"), d["slug"], "cover") else '<div class="no-img">Bedah Riset</div>')
                   + '</a><div class="card-body">'
                   f'<p class="eyebrow">{esc(d["topik"])} &middot; {esc(d["negara"])}</p>'
                   f'<h3><a href="/riset/{d["slug"]}/">{esc(d["judul"])}</a></h3>'
                   f'<p>{esc(d["lead"])}</p>'
                   f'<p class="meta">{esc(d["journal"])} &middot; {esc(str(d["year"]))} &middot; Kesimpulan: {esc(d["vonis"])}</p></div></article>\n')
    rtopics = sorted(set(d["topik"] for d in research))
    rchips = "".join(f'<button class="chip" data-series="{esc(t)}">{esc(t)}</button>' for t in rtopics)
    rindex = HEAD.format(title="Riset Teknik Kimia, Dibedah | ilmutekkim",
                         desc="Bedah paper jurnal teknik kimia internasional dan Indonesia: masalah, metode, temuan, catatan kritis, dan kesimpulan baca full paper atau cukup abstraknya.",
                         url=BASE + "/riset/", ogtype="website", ogimg="")
    rindex += f"""
<article class="post wide">
<p class="eyebrow">Riset</p>
<h1>Bedah paper jurnal: dari masalah sampai kesimpulan.</h1>
<p class="lead">Setiap bedah di halaman ini ditulis dari abstrak paper yang terverifikasi: permasalahan yang dikaji, metode yang digunakan, angka temuan persis sebagaimana tertulis, batas keberlakuannya, serta implikasinya bagi praktik industri. Setiap bedah ditutup dengan kesimpulan yang eksplisit: paper tersebut perlu dibaca penuh, atau abstraknya dinilai telah memadai.</p>
<p class="meta">{len(research)} bedah jurnal &middot; campuran internasional dan Indonesia &middot; standar bedah: angka hanya dari abstrak, abstrak tidak disalin, selalu ada catatan kritis</p>
</article>
<section class="post wide tight">
<h2>Rak bedah paten</h2>
<p>Paten adalah dokumen teknologi yang terbuka: paten kedaluwarsa berarti teknologi yang bebas dipelajari dan dipakai sebagai titik awal, paten aktif berarti peta arah pemegangnya. Di rak ini paten klasik teknik kimia dibedah dengan standar yang sama: nomor, inventor, dan tanggal diverifikasi dari dokumen aslinya, klaimnya diparafrase, dan statusnya ditulis apa adanya. Saat ini ada {len(paten)} bedah paten.</p>
<p><a class="btn" href="/riset/paten/">Buka rak bedah paten</a></p>
</section>

<section id="seri" class="series-bar">
  <h2>Telusuri menurut topik</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{rchips}</div>
  <input id="search" type="search" placeholder="Cari bedah, contoh: hidrogen, katalis, pirolisis..." aria-label="Cari bedah riset">
</section>
<section id="artikel" class="grid">
{rcards}
</section>
<p id="no-result" hidden>Tidak ditemukan bedah yang sesuai. Silakan gunakan kata kunci lain.</p>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "riset"), exist_ok=True)
    open(os.path.join(ROOT, "riset", "index.html"), "w").write(rindex)
    for ri, d in enumerate(research):
        url = f"{BASE}/riset/{d['slug']}/"
        page = HEAD.format(title=f"{esc(d['judul'])} | Riset ilmutekkim", desc=esc(d["lead"])[:155],
                           url=url, ogtype="article", ogimg="")
        page += '<article class="post">\n'
        page += f'<p class="eyebrow">Riset &middot; {esc(d["topik"])} &middot; {esc(d["negara"])}</p>\n<h1>{esc(d["judul"])}</h1>\n'
        page += f'<p class="meta">{tgl_indo(d["date_bedah"])} &middot; ilmutekkim</p>\n'
        page += render_bedah(d) + "\n"
        prev_r = research[ri + 1] if ri + 1 < len(research) else None
        next_r = research[ri - 1] if ri > 0 else None
        page += '<nav class="post-nav">'
        if prev_r:
            page += f'<a href="/riset/{prev_r["slug"]}/">&larr; {esc(prev_r["judul"])}</a>'
        if next_r:
            page += f'<a href="/riset/{next_r["slug"]}/">{esc(next_r["judul"])} &rarr;</a>'
        page += "</nav>\n"
        page += ('<div class="cta-box"><h2>Semua bedah riset</h2>'
                 "<p>Bedah jurnal teknik kimia internasional dan Indonesia, ditulis dari abstrak terverifikasi dengan catatan kritis dan kesimpulan.</p>"
                 '<a class="btn" href="/riset/">Ke halaman riset</a></div>\n')
        page += "</article>" + FOOT
        outr = os.path.join(ROOT, "riset", d["slug"])
        os.makedirs(outr, exist_ok=True)
        open(os.path.join(outr, "index.html"), "w").write(page)

    # rak paten /riset/paten/ + bedah /riset/paten/<slug>/ (ILM-R66)
    pcards = ""
    for d in paten:
        pcards += (f'<article class="card" data-series="{esc(d["topik"])}" '
                   f'data-title="{esc(d["judul"].lower())} {esc(d["topik"].lower())} {esc(d["nomor"].lower())}">'
                   f'<a href="/riset/paten/{d["slug"]}/">'
                   + (f'<img src="{resolve_img(d.get("cover_file"), d["slug"], "cover")}" alt="{esc(d["judul"])}" loading="lazy">'
                      if resolve_img(d.get("cover_file"), d["slug"], "cover") else '<div class="no-img">Bedah Paten</div>')
                   + '</a><div class="card-body">'
                   f'<p class="eyebrow">{esc(d["topik"])} &middot; {esc(d["nomor"])}</p>'
                   f'<h3><a href="/riset/paten/{d["slug"]}/">{esc(d["judul"])}</a></h3>'
                   f'<p>{esc(d["lead"])}</p>'
                   f'<p class="meta">Terbit {esc(d["terbit"])} &middot; Kesimpulan: {esc(d["kesimpulan"])}</p></div></article>\n')
    ptopics = sorted(set(d["topik"] for d in paten))
    pchips = "".join(f'<button class="chip" data-series="{esc(t)}">{esc(t)}</button>' for t in ptopics)
    pindex = HEAD.format(title="Bedah Paten Teknik Kimia | ilmutekkim",
                         desc="Bedah paten klasik teknik kimia dari dokumen aslinya: masalah, klaim inti parafrase, cara kerja, batas kritis, dan status. Paten kedaluwarsa adalah teknologi yang bebas dipelajari.",
                         url=BASE + "/riset/paten/", ogtype="website", ogimg="")
    pindex += f"""
<article class="post wide">
<p class="eyebrow">Riset &middot; Paten</p>
<h1>Bedah paten: baca dokumen teknologinya, bukan rumornya.</h1>
<p class="lead">Setiap bedah di rak ini ditulis dari dokumen paten aslinya yang terbuka untuk umum: nomor, inventor, pemilik, dan tanggalnya diverifikasi, klaim intinya diparafrase, prinsip kerjanya dijelaskan, batasnya dicatat, dan status hukumnya ditulis sebagaimana tercatat. Paten yang sudah kedaluwarsa adalah dokumen publik: teknologinya bebas dipelajari siapa pun.</p>
<p class="meta">{len(paten)} bedah paten &middot; standar bedah: data hanya dari dokumen paten, klaim diparafrase, status bersumber dan bertanggal akses</p>
</article>
<section class="post wide tight">
<h2>Rak bedah jurnal</h2>
<p>Bedah paper jurnal teknik kimia internasional dan Indonesia ada di halaman riset: masalah, metode, temuan persis dari abstrak, catatan kritis, dan kesimpulan baca.</p>
<p><a class="btn" href="/riset/">Buka rak bedah jurnal</a></p>
</section>

<section id="seri" class="series-bar">
  <h2>Telusuri menurut topik</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{pchips}</div>
  <input id="search" type="search" placeholder="Cari paten, contoh: PSA, membran, MTG..." aria-label="Cari bedah paten">
</section>
<section id="artikel" class="grid">
{pcards}
</section>
<p id="no-result" hidden>Tidak ditemukan bedah yang sesuai. Silakan gunakan kata kunci lain.</p>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "riset", "paten"), exist_ok=True)
    open(os.path.join(ROOT, "riset", "paten", "index.html"), "w").write(pindex)
    for pi, d in enumerate(paten):
        url = f"{BASE}/riset/paten/{d['slug']}/"
        page = HEAD.format(title=f"{esc(d['judul'])} | Bedah Paten ilmutekkim", desc=esc(d["lead"])[:155],
                           url=url, ogtype="article", ogimg="")
        page += '<article class="post">\n'
        page += f'<p class="eyebrow">Riset &middot; Paten &middot; {esc(d["topik"])}</p>\n<h1>{esc(d["judul"])}</h1>\n'
        page += f'<p class="meta">{tgl_indo(d["date_bedah"])} &middot; ilmutekkim</p>\n'
        page += render_paten(d) + "\n"
        prev_p = paten[pi + 1] if pi + 1 < len(paten) else None
        next_p = paten[pi - 1] if pi > 0 else None
        page += '<nav class="post-nav">'
        if prev_p:
            page += f'<a href="/riset/paten/{prev_p["slug"]}/">&larr; {esc(prev_p["judul"])}</a>'
        if next_p:
            page += f'<a href="/riset/paten/{next_p["slug"]}/">{esc(next_p["judul"])} &rarr;</a>'
        page += "</nav>\n"
        page += ('<div class="cta-box"><h2>Semua bedah paten</h2>'
                 "<p>Bedah paten klasik teknik kimia dari dokumen aslinya, dengan klaim parafrase dan status yang ditulis apa adanya.</p>"
                 '<a class="btn" href="/riset/paten/">Ke rak bedah paten</a></div>\n')
        page += "</article>" + FOOT
        outp = os.path.join(ROOT, "riset", "paten", d["slug"])
        os.makedirs(outp, exist_ok=True)
        open(os.path.join(outp, "index.html"), "w").write(page)

    # jalur belajar /jalur/ + /jalur/<slug>/, pengalihan kamus, referensi /referensi/ (ILM-R67)
    jalur = load_jalur()
    glosarium = load_glosarium()
    kamus = load_kamus_catalog(glosarium)
    art_map = {a["slug"]: a["title"] for a in articles}
    vid_map = {v["slug"]: v["title"] for v in videos}
    pat_map = {d["slug"]: d["judul"] for d in paten}

    def resolve_tautan(t):
        typ, sl = t.get("type"), t.get("slug")
        if typ == "artikel" and sl in art_map:
            return f"/artikel/{sl}/", art_map[sl]
        if typ == "video" and sl in vid_map:
            return f"/video/{sl}/", vid_map[sl]
        if typ == "paten" and sl in pat_map:
            return f"/riset/paten/{sl}/", pat_map[sl]
        raise SystemExit(f"Build dibatalkan: tautan tidak dikenal (ILM-R67): {t}")

    label_tipe = {"artikel": "Artikel", "video": "Video", "paten": "Bedah paten"}
    jcards = ""
    for t in jalur:
        first_url, _ = resolve_tautan(t["steps"][0])
        jcov = resolve_img(t.get("cover_file"), t["slug"], "cover")
        jcards += (f'<article class="card"><a href="/jalur/{t["slug"]}/">'
                   + (f'<img src="{jcov}" alt="{esc(t["judul"])}" loading="lazy">' if jcov else '<div class="no-img">Jalur Belajar</div>')
                   + '</a>'
                   f'<div class="card-body"><p class="eyebrow">Jalur belajar &middot; {len(t["steps"])} langkah</p>'
                   f'<h3><a href="/jalur/{t["slug"]}/">{esc(t["judul"])}</a></h3><p>{esc(t["desc"])}</p>'
                   f'<p class="meta"><a href="{first_url}">Mulai dari langkah 1 &rarr;</a></p></div></article>\n')
    jindex = HEAD.format(title="Jalur Belajar Teknik Kimia | ilmutekkim",
                         desc="Urutan baca terkurasi ilmutekkim: membaca pabrik dari nol, distilasi inti, kilang dan petrokimia, sawit, utilitas, keselamatan proses, dan pabrik Indonesia.",
                         url=BASE + "/jalur/", ogtype="website", ogimg="")
    jindex += f"""
<article class="post wide">
<p class="eyebrow">Jalur belajar</p>
<h1>Belajar teknik kimia pakai urutan, bukan acak.</h1>
<p class="lead">Artikel yang baik sekalipun sulit diikuti apabila dibaca tanpa urutan konseptual. Halaman ini menyusun bacaan ilmutekkim menjadi {len(jalur)} jalur belajar: setiap jalur merupakan urutan langkah yang disusun secara disengaja, dari konsep yang harus dipahami terlebih dahulu menuju konsep yang prasyaratnya telah terpenuhi. Setiap langkah berupa artikel, video, atau bedah paten yang telah tersedia di situs ini, disertai satu kalimat penjelasan mengenai kedudukannya dalam jalur tersebut.</p>
<p class="meta">{len(jalur)} jalur &middot; {sum(len(t["steps"]) for t in jalur)} langkah &middot; semua langkah resolve ke konten ilmutekkim</p>
</article>
<section class="grid">
{jcards}
</section>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "jalur"), exist_ok=True)
    open(os.path.join(ROOT, "jalur", "index.html"), "w").write(jindex)
    for t in jalur:
        steps_html = ""
        for i, st in enumerate(t["steps"], 1):
            u, ttl = resolve_tautan(st)
            steps_html += (f'<section class="stepcard"><p class="eyebrow">Langkah {i} &middot; {label_tipe[st["type"]]}</p>'
                           f'<h2><a href="{u}">{esc(ttl)}</a></h2><p>{esc(st["note"])}</p>'
                           f'<p><a class="btn ghost" href="{u}">Buka langkah {i}</a></p></section>\n')
        jpage = HEAD.format(title=f"Jalur {esc(t['judul'])} | ilmutekkim", desc=esc(t["desc"])[:155],
                            url=f"{BASE}/jalur/{t['slug']}/", ogtype="article", ogimg="")
        jpage += f"""
<article class="post">
<p class="eyebrow">Jalur belajar</p>
<h1>{esc(t["judul"])}</h1>
<p class="lead">{esc(t["desc"])}</p>
<p class="meta">{len(t["steps"])} langkah &middot; baca berurutan dari atas</p>
{("<figure><img src=\"" + resolve_img(t.get("cover_file"), t["slug"], "cover") + "\" alt=\"" + esc(t["judul"]) + "\"><figcaption>" + esc(t.get("cover_credit") or "") + "</figcaption></figure>") if resolve_img(t.get("cover_file"), t["slug"], "cover") else ""}
{steps_html}
<div class="cta-box"><h2>Semua jalur belajar</h2>
<p>Tujuh jalur terkurasi: dari membaca pabrik untuk pemula sampai tur pabrik Indonesia.</p>
<a class="btn" href="/jalur/">Ke semua jalur</a></div>
</article>
""" + FOOT
        outj = os.path.join(ROOT, "jalur", t["slug"])
        os.makedirs(outj, exist_ok=True)
        open(os.path.join(outj, "index.html"), "w").write(jpage)

    # Glosarium lama telah digabungkan ke Kamus. Rute lama hanya menjadi
    # pengalihan agar tautan eksternal dan penanda lama tetap berguna.
    gindex = HEAD.format(title="Kamus Industri Kimia | ilmutekkim",
                         desc="Kamus Industri Kimia IlmuTekkim: istilah teknik kimia dengan definisi, mekanisme, persamaan, sensitivitas, dan bedah plant.",
                         url=BASE + "/kamus/", ogtype="website", ogimg="")
    gindex = gindex.replace("<head>\n", "<head>\n<meta http-equiv=\"refresh\" content=\"0; url=/kamus\">\n", 1)
    gindex += """
<article class="post wide">
<p class="eyebrow">Kamus</p>
<h1>Kamus Industri Kimia IlmuTekkim</h1>
<p class="lead">Glosarium telah digabungkan ke dalam Kamus Industri Kimia. Anda akan dialihkan secara otomatis ke satu-satunya kamus di situs ini.</p>
<p>Jika pengalihan tidak berjalan, <a href="/kamus">buka Kamus Industri Kimia</a>.</p>
</article>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "glosarium"), exist_ok=True)
    open(os.path.join(ROOT, "glosarium", "index.html"), "w").write(gindex)

    import re as _re
    ref_entries = {}
    for a in articles:
        for r in a["refs"]:
            key = _re.sub(r"[^a-z0-9]+", "", r.lower())[:60]
            ref_entries.setdefault(key, {"text": r, "dipakai": []})
            ref_entries[key]["dipakai"].append((f"/artikel/{a['slug']}/", a["title"]))
    ref_list = sorted(ref_entries.values(), key=lambda e: e["text"].lower())
    buku_html = ""
    for e in ref_list:
        links = ", ".join(f'<a href="{u}">{esc(t)}</a>' for u, t in e["dipakai"][:3])
        if len(e["dipakai"]) > 3:
            links += f', dan {len(e["dipakai"]) - 3} artikel lain'
        buku_html += f'<li>{esc(e["text"])}<br><span class="meta">Dipakai di: {links}</span></li>\n'
    paper_html = ""
    for d in research:
        paper_html += (f'<li><a href="/riset/{d["slug"]}/">{esc(d["paper_title"])}</a><br>'
                       f'<span class="meta">{esc(authors_short(d["authors"]))} &middot; {esc(d["journal"])} &middot; {esc(str(d["year"]))}</span></li>\n')
    paten_html = ""
    for d in paten:
        paten_html += (f'<li><a href="/riset/paten/{d["slug"]}/">{esc(d["nomor"])}: {esc(d["judul_paten"])}</a><br>'
                       f'<span class="meta">{esc(d["pemilik"])} &middot; terbit {esc(d["terbit"])}</span></li>\n')
    rfp = HEAD.format(title="Referensi dan Perpustakaan | ilmutekkim",
                      desc="Semua sitasi yang dipakai ilmutekkim dikumpulkan di satu tempat: buku dan standar yang dikutip artikel, paper yang dibedah, dan paten yang dibedah.",
                      url=BASE + "/referensi/", ogtype="website", ogimg="")
    rfp += f"""
<article class="post">
<p class="eyebrow">Referensi</p>
<h1>Perpustakaan ilmutekkim.</h1>
<p class="lead">Semua sitasi yang muncul di situs ini dikumpulkan di satu halaman. Bagian pertama adalah buku, standar, dan literatur yang dikutip artikel dan video. Bagian berikutnya adalah paper dan paten yang dibedah di halaman riset. Halaman ini tidak memuat sitasi baru; isinya persis sitasi yang telah digunakan tulisan-tulisan di situs ini.</p>
<h2>Buku dan literatur yang dikutip</h2>
<ol class="refs">
{buku_html}
</ol>
<h2>Paper yang dibedah</h2>
<ol class="refs">
{paper_html}
</ol>
<h2>Paten yang dibedah</h2>
<ol class="refs">
{paten_html}
</ol>
</article>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "referensi"), exist_ok=True)
    open(os.path.join(ROOT, "referensi", "index.html"), "w").write(rfp)

    # kalkulator interaktif /kalkulator/ (ILM-R68)
    kpage = HEAD.format(title="Kalkulator Teknik Kimia | ilmutekkim",
                        desc="Kalkulator teknik kimia interaktif: derajat polimerisasi Carothers, LMTD heat exchanger, McCabe-Thiele distilasi biner, dan konversi satuan proses.",
                        url=BASE + "/kalkulator/", ogtype="website", ogimg="")
    kpage += """
<article class="post">
<p class="eyebrow">Kalkulator</p>
<h1>Kalkulator teknik kimia.</h1>
<p class="lead">Empat kalkulator untuk konsep yang berulang kali dibahas di situs ini. Setiap kalkulator menggunakan persamaan standar, mencantumkan asumsinya secara eksplisit, dan menautkan artikel yang menjelaskan konsepnya. Hasil perhitungan merupakan titik awal analisis, bukan pengganti simulasi proses.</p>

<section class="calc-card">
<h2>Derajat polimerisasi Carothers (step-growth)</h2>
<p>Xn = (1 + r) / (1 + r &minus; 2rp). Pada stoikiometri sempurna (r = 1) persamaan menyederhana menjadi Xn = 1 / (1 &minus; p). Asumsi: polimerisasi step-growth tanpa reaksi samping.</p>
<div class="calc-grid">
<div><label>Konversi p</label><input id="car-p" type="number" step="0.001" min="0" max="0.9999" value="0.99"></div>
<div><label>Rasio stoikiometri r (1 = sempurna)</label><input id="car-r" type="number" step="0.001" min="0.1" max="1" value="1"></div>
</div>
<div class="calc-out" id="car-out"></div>
<p><a class="btn ghost" href="/artikel/polimerisasi-konversi-carothers/">Konsepnya: polimerisasi dan persamaan Carothers</a> <a class="btn ghost" href="/artikel/cs01-step-growth-carothers-dp-runtuh/">Cheat sheet: DP runtuh</a></p>
</section>

<section class="calc-card">
<h2>LMTD heat exchanger</h2>
<p>LMTD = (&Delta;T1 &minus; &Delta;T2) / ln(&Delta;T1 / &Delta;T2). Asumsi: aliran murni berlawanan arah atau searah sesuai pilihan, tanpa faktor koreksi konfigurasi shell-and-tube.</p>
<div class="calc-grid">
<div><label>Panas masuk (&deg;C)</label><input id="lm-thi" type="number" step="any" value="150"></div>
<div><label>Panas keluar (&deg;C)</label><input id="lm-tho" type="number" step="any" value="100"></div>
<div><label>Dingin masuk (&deg;C)</label><input id="lm-tci" type="number" step="any" value="30"></div>
<div><label>Dingin keluar (&deg;C)</label><input id="lm-tco" type="number" step="any" value="80"></div>
<div><label>Susunan aliran</label><select id="lm-mode"><option value="counter">Berlawanan arah</option><option value="co">Searah</option></select></div>
</div>
<div class="calc-out" id="lm-out"></div>
<p><a class="btn ghost" href="/artikel/heat-exchanger-bikin-shutdown/">Konsepnya: heat exchanger</a></p>
</section>

<section class="calc-card">
<h2>McCabe-Thiele distilasi biner</h2>
<p>Metode grafis McCabe-Thiele untuk campuran biner. Asumsi: volatilitas relatif konstan, kondensor total, luapan molar konstan, dan garis umpan sesuai nilai q. Contoh baku di bawah adalah pola benzena-toluena.</p>
<div class="calc-grid">
<div><label>Volatilitas relatif &alpha;</label><input id="mt-alpha" type="number" step="0.01" min="1.01" value="2.45"></div>
<div><label>Fraksi umpan zF</label><input id="mt-zf" type="number" step="0.01" min="0.01" max="0.99" value="0.44"></div>
<div><label>Fraksi distilat xD</label><input id="mt-xd" type="number" step="0.01" min="0.01" max="0.999" value="0.97"></div>
<div><label>Fraksi bottoms xB</label><input id="mt-xb" type="number" step="0.001" min="0.001" max="0.99" value="0.02"></div>
<div><label>q umpan (1 = cair jenuh)</label><input id="mt-q" type="number" step="0.05" min="-1" max="2" value="1"></div>
<div><label>Faktor R / R minimum</label><input id="mt-f" type="number" step="0.05" min="1.01" max="5" value="1.3"></div>
</div>
<div class="calc-out" id="mt-out"></div>
<canvas id="mt-canvas" width="520" height="520"></canvas>
<p><a class="btn ghost" href="/artikel/distilasi-bertingkat-minyak-mentah/">Konsepnya: distilasi bertingkat</a> <a class="btn ghost" href="/artikel/reflux-optimum-kolom-distilasi/">Konsep reflux optimum</a></p>
</section>

<section class="calc-card">
<h2>Konversi satuan proses</h2>
<p>Suhu, tekanan, dan aliran volumetrik yang paling sering dipakai di pabrik.</p>
<div class="calc-grid">
<div><label>Suhu</label><input id="cv-tv" type="number" step="any" value="100"></div>
<div><label>Satuan suhu</label><select id="cv-tu"><option value="C">&deg;C</option><option value="F">&deg;F</option><option value="K">K</option></select></div>
<div><label>Tekanan</label><input id="cv-pv" type="number" step="any" value="1"></div>
<div><label>Satuan tekanan</label><select id="cv-pu"><option value="atm">atm</option><option value="bar">bar</option><option value="kPa">kPa</option><option value="Pa">Pa</option><option value="psi">psi</option></select></div>
<div><label>Aliran</label><input id="cv-fv" type="number" step="any" value="10"></div>
<div><label>Satuan aliran</label><select id="cv-fu"><option value="m3/h">m&sup3;/jam</option><option value="m3/s">m&sup3;/s</option><option value="L/s">L/s</option><option value="gpm (US)">gpm (US)</option></select></div>
</div>
<div class="calc-out" id="cv-out"></div>
<p><a class="btn ghost" href="/artikel/utilitas-pabrik-steam-air-nitrogen/">Konsepnya: utilitas pabrik</a></p>
</section>
</article>
<script src="/assets/js/calc.js?v=1"></script>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "kalkulator"), exist_ok=True)
    open(os.path.join(ROOT, "kalkulator", "index.html"), "w").write(kpage)

    # beranda
    series_list = sorted(set(a["series"] for a in articles))
    chips = ('<button class="chip" data-series="Video">Video</button>'
             + "".join(f'<button class="chip" data-series="{esc(s)}">{esc(s)}</button>'
                       for s in series_list))
    cards = ""
    for a in articles:
        excerpt = (a["lead"][1] if len(a["lead"]) > 1 else (a["lead"][0] if a["lead"] else a["sub"]))[:170]
        img = (f'<img src="{a["cover"]}" alt="{esc(a["title"])}" loading="lazy">' if a["cover"]
               else '<div class="no-img">ilmutekkim</div>')
        badge = ' <span class="badge">Arsip</span>' if a["status"] == "arsip" else ""
        cards += (f'<article class="card" data-series="{esc(a["series"])}" '
                  f'data-title="{esc(a["title"].lower())} {esc(a["series"].lower())}">'
                  f'<a href="/artikel/{a["slug"]}/">{img}</a><div class="card-body">'
                  f'<p class="eyebrow">{esc(a["series"])}{badge}</p>'
                  f'<h3><a href="/artikel/{a["slug"]}/">{esc(a["title"])}</a></h3>'
                  f'<p>{esc(excerpt)}</p>'
                  f'<p class="meta">{tgl_indo(a["date"])}</p></div></article>\n')
    home = HEAD.format(title="ilmutekkim | Bikin Teknik Kimia Asik: Pabrik, Proses, Safety",
                       desc="Bedah proses teknik kimia dari pabriknya langsung: distilasi, kilang, "
                            "sawit, semen, pulp, sampai safety. Ditulis insinyur kimia ITB.",
                       url=BASE + "/", ogtype="website", ogimg="")
    # strip video terbaru untuk beranda (4 terbaru)
    vstrip = ""
    for vi, v in enumerate(videos):
        thumb = (f'<img src="{v["poster_url"]}" alt="{esc(v["title"])}" loading="lazy">' if v.get("poster_url")
                 else '<div class="no-img">ilmutekkim</div>')
        extra = ' v-extra' if vi >= 4 else ""
        extstyle = ' style="display:none"' if vi >= 4 else ""
        vstrip += (f'<article class="card vcard{extra}" data-series="Video"{extstyle} '
                   f'data-title="{esc(v["title"].lower())} {esc(v["tag"].lower())} video"><a href="/video/{v["slug"]}/">{thumb}'
                   f'<span class="play-badge">&#9654; {fmt_time(v["duration"])}</span></a><div class="card-body">'
                   f'<p class="eyebrow">{esc(v["tag"])}</p>'
                   f'<h3><a href="/video/{v["slug"]}/">{esc(v["title"])}</a></h3>'
                   f'<p>{esc(v["hook"])}</p>'
                   f'<p class="meta">{tgl_indo(v["date"])} &middot; tonton + baca artikelnya</p></div></article>\n')
    home += f"""
<section class="hero">
  <nav class="tool-strip" aria-label="Fitur utama situs">
    <a href="#artikel"><span>01</span><b>Artikel dan Video</b><i>{len(articles)} artikel mendalam bersitasi dan {len(videos)} video dengan artikel pendamping</i></a>
    <a href="/riset/"><span>02</span><b>Riset</b><i>{len(research)} bedah jurnal dan {len(paten)} bedah paten dengan catatan kritis dan kesimpulan eksplisit</i></a>
    <a href="/jalur/"><span>03</span><b>Jalur Belajar</b><i>{len(jalur)} jalur terkurasi, {sum(len(t["steps"]) for t in jalur)} langkah berurutan dari konsep dasar ke aplikasi</i></a>
    <a href="/kamus"><span>04</span><b>Kamus</b><i>{kamus['total']} istilah teknik kimia: {len(kamus['deep_slugs'])} entri dalam dan {len(kamus['dasar_slugs'])} entri dasar dengan bacaan lanjutan</i></a>
    <a href="/referensi/"><span>05</span><b>Referensi</b><i>Seluruh literatur, paper yang dibedah, dan dokumen paten dalam satu perpustakaan</i></a>
    <a href="/kalkulator/"><span>06</span><b>Kalkulator</b><i>Polimerisasi Carothers, LMTD, rancangan McCabe-Thiele, dan konversi satuan proses</i></a>
  </nav>
  <div class="hero-grid">
    <h1>Teknik kimia, ditelaah dari prosesnya.</h1>
    <div class="hero-side">
      <p>Distilasi, kilang minyak, pengolahan kelapa sawit, semen, pulp dan kertas, hingga sistem pengaman proses.
      Setiap topik ditelaah secara bertahap dan mendalam, dilengkapi sitasi literatur standar teknik kimia.</p>
      <a class="btn" href="#artikel">Telusuri {len(articles)} artikel</a>
      <a class="btn ghost" href="/video/">Lihat {len(videos)} video</a>
    </div>
  </div>
</section>
<section id="seri" class="series-bar">
  <h2>Telusuri menurut seri</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{chips}</div>
  <input id="search" type="search" placeholder="Cari artikel, contoh: distilasi, semen, pompa..." aria-label="Cari artikel">
</section>
<section id="video" class="video-home">
  <div class="video-home-head"><h2>Video terbaru</h2><a href="/video/">Lihat semua video &rarr;</a></div>
  <p class="video-home-sub">Setiap video @ilmutekkim disertai artikel pendamping yang mendalam. Pilih kartu untuk menonton beserta penjelasan lengkapnya.</p>
  <div class="grid video-grid">
{vstrip}
  </div>
</section>
<section id="artikel" class="grid">
{cards}
</section>
<p id="no-result" hidden>Tidak ditemukan artikel yang sesuai. Silakan gunakan kata kunci lain.</p>
""" + FOOT
    open(os.path.join(ROOT, "index.html"), "w").write(home)

    # tentang
    tentang = HEAD.format(title="Tentang ilmutekkim", desc="ilmutekkim adalah arsip baca konten "
                          "teknik kimia @ilmutekkim: pabrik, proses, keselamatan, dan kecerdasan buatan.",
                          url=BASE + "/tentang/", ogtype="website", ogimg="")
    tentang += """
<article class="post narrow">
<p class="eyebrow">Tentang</p>
<h1>Tentang ilmutekkim.</h1>
<p class="lead">ilmutekkim adalah media pembelajaran teknik kimia dari sudut pandang praktisi pabrik:
bukan hafalan rumus, melainkan bagaimana proses sesungguhnya beroperasi di lapangan.</p>
<p>Setiap artikel di situs ini merupakan versi baca dari carousel Instagram
<a href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">@ilmutekkim</a>:
satu topik ditelaah mulai dari kesalahpahaman yang paling sering beredar, kenyataan prosesnya,
diagram alurnya, hingga contoh penerapannya di industri Indonesia.</p>
<p>Setiap <a href="/video/">video</a> merupakan versi tonton dari konten @ilmutekkim:
pengunjung dapat menonton sambil membaca artikel lengkapnya, melompat ke detik tertentu
dari judul bagiannya, kemudian memeriksa pemahaman melalui kuis singkat.</p>
<h2>Yang dibahas</h2>
<ul>
<li>Unit operasi: distilasi, heat exchanger, pompa, kompresor, cooling tower.</li>
<li>Alur pabrik Indonesia: kelapa sawit, kilang, petrokimia, pupuk, gula, semen, pulp dan kertas.</li>
<li>Keselamatan proses: relief valve, safety instrumented system, permit to work.</li>
<li>Dasar yang kerap lemah: neraca massa, pembacaan P&amp;ID, mode batch versus kontinu.</li>
</ul>
<h2>Alasan versi situs web</h2>
<p>Carousel mudah disimpan, tetapi sukar ditemukan kembali. Di situs ini seluruh artikel dapat ditelusuri,
dibaca secara utuh tanpa menggeser slide, dan ditemukan melalui mesin pencari. Konten terbaru tetap diterbitkan
terlebih dahulu di Instagram setiap hari.</p>
<div class="cta-box"><h2>Titik awal yang disarankan</h2>
<p>Pembaca baru disarankan memulai dari <a href="/artikel/distilasi-bertingkat-minyak-mentah/">distilasi bertingkat</a>,
kemudian <a href="/artikel/baca-pid-lima-simbol-pabrik/">pembacaan P&amp;ID</a>.</p>
<a class="btn" href="/#artikel">Lihat semua artikel</a></div>
</article>
""" + FOOT
    os.makedirs(os.path.join(ROOT, "tentang"), exist_ok=True)
    open(os.path.join(ROOT, "tentang", "index.html"), "w").write(tentang)

    # sitemap + robots
    urls = ([BASE + "/", BASE + "/tentang/", BASE + "/video/", BASE + "/riset/", BASE + "/riset/paten/",
             BASE + "/jalur/", BASE + "/kamus/", BASE + "/referensi/", BASE + "/kalkulator/"]
            + [f"{BASE}/kamus/sektor/{slug}/" for slug in kamus["sector_slugs"]]
            + [f"{BASE}/kamus/istilah/{slug}/" for slug in kamus["deep_slugs"] + kamus["dasar_slugs"]]
            + [f"{BASE}/jalur/{t['slug']}/" for t in jalur]
            + [f"{BASE}/riset/{d['slug']}/" for d in research]
            + [f"{BASE}/riset/paten/{d['slug']}/" for d in paten]
            + [f"{BASE}/artikel/{a['slug']}/" for a in articles]
            + [f"{BASE}/video/{v['slug']}/" for v in videos])
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"OK: {len(articles)} artikel, {len(videos)} video, {len(series_list)} seri")


if __name__ == "__main__":
    main()
