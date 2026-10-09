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
    ("pabrik-kelapa-sawit-tandan-ke-cpo", "specs/2026-09-30-carousel-2-rev5.json",
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
        ]}
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
<link rel="stylesheet" href="/assets/css/style.css?v=21">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23131518'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23F4F4F2' font-family='Arial' font-weight='bold'>IT</text></svg>">
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
  <p class="foot-links"><a href="/">Beranda</a><span>&middot;</span><a href="/video/">Video</a><span>&middot;</span><a href="/riset/">Riset</a><span>&middot;</span><a href="/jalur/">Jalur</a><span>&middot;</span><a href="/glosarium/">Glosarium</a><span>&middot;</span><a href="/referensi/">Referensi</a><span>&middot;</span><a href="/kalkulator/">Kalkulator</a><span>&middot;</span><a href="/tentang/">Tentang</a></p>
  <p class="fine">Artikel dan video di situs ini merupakan versi baca dan versi tonton dari konten Instagram @ilmutekkim. Foto berasal dari Pexels dan Unsplash, kredit tercantum di tiap gambar.</p>
</footer>
<script src="/assets/js/main.js?v=9"></script>
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

    # jalur belajar /jalur/ + /jalur/<slug>/, glosarium /glosarium/, referensi /referensi/ (ILM-R67)
    jalur = load_jalur()
    glosarium = load_glosarium()
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

    art_cover = {a["slug"]: a.get("cover") for a in articles}
    pat_cover = {d2["slug"]: resolve_img(d2.get("cover_file"), d2["slug"], "cover") for d2 in paten}
    vid_cover = {v["slug"]: v.get("poster_url") for v in videos}
    def gcover(g):
        for t in g["terkait"]:
            c = art_cover.get(t["slug"]) if t["type"] == "artikel" else vid_cover.get(t["slug"]) if t["type"] == "video" else pat_cover.get(t["slug"]) if t["type"] == "paten" else None
            if c:
                return c
        return None
    gcards = ""
    for g in sorted(glosarium, key=lambda x: x["term"].lower()):
        huruf = g["term"][0].lower()
        links = ""
        for t in g["terkait"]:
            u, ttl = resolve_tautan(t)
            links += f'<a class="btn ghost clamp" href="{u}">{esc(ttl)}</a> '
        gcov = gcover(g)
        gcards += (f'<article class="card" data-series="{esc(huruf)}" '
                   f'data-title="{esc(g["term"].lower())}">'
                   + (f'<img src="{gcov}" alt="{esc(g["term"])}" loading="lazy">' if gcov else "")
                   + '<div class="card-body">'
                   f'<p class="eyebrow">Istilah pabrik</p><h3>{esc(g["term"])}</h3>'
                   f'<p>{esc(g["definisi"])}</p><p>{links}</p></div></article>\n')
    huruf_list = sorted(set(g["term"][0].upper() for g in glosarium))
    gchips = "".join(f'<button class="chip" data-series="{esc(h.lower())}">{esc(h)}</button>' for h in huruf_list)
    gindex = HEAD.format(title="Glosarium Istilah Pabrik | ilmutekkim",
                         desc="Kamus istilah teknik kimia dan pabrik dalam bahasa polos: reflux, LMTD, wet bulb, SIS, SIL, kavitasi, dan lainnya, masing-masing dengan bacaan lanjutannya.",
                         url=BASE + "/glosarium/", ogtype="website", ogimg="")
    gindex += f"""
<article class="post wide">
<p class="eyebrow">Glosarium</p>
<h1>Istilah pabrik, dijelaskan polos.</h1>
<p class="lead">Istilah di halaman ini adalah istilah yang benar-benar muncul di artikel, video, dan bedah ilmutekkim. Setiap definisi dirumuskan secara ringkas dan tepat, kemudian ditautkan ke bacaan yang menggunakannya agar istilah tersebut dapat dipahami dalam konteks prosesnya.</p>
<p class="meta">{len(glosarium)} istilah &middot; setiap istilah menautkan bacaan lanjutan di situs ini</p>
</article>
<section id="seri" class="series-bar">
  <h2>Jelajahi per huruf</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{gchips}</div>
  <input id="search" type="search" placeholder="Cari istilah, contoh: reflux, kavitasi, sil..." aria-label="Cari istilah glosarium">
</section>
<section id="artikel" class="grid">
{gcards}
</section>
<p id="no-result" hidden>Tidak ditemukan istilah yang sesuai. Silakan gunakan kata kunci lain.</p>
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
    <a href="/glosarium/"><span>04</span><b>Glosarium</b><i>{len(glosarium)} istilah proses terdefinisi secara tepat dengan bacaan lanjutan</i></a>
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
             BASE + "/jalur/", BASE + "/glosarium/", BASE + "/referensi/", BASE + "/kalkulator/"]
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
