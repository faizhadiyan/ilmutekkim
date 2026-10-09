#!/usr/bin/env python3
"""Generate website ilmutekkim dari spec carousel IG @ilmutekkim.

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
     "Distilasi Bertingkat: Kenapa Minyak Mentah Tidak Cukup Direbus Sekali",
     "2026-09-30", "https://www.instagram.com/p/Dd8JoC6FLhe/", "tayang"),
    ("reflux-optimum-kolom-distilasi", "draft/spec-real.json",
     "Makin Besar Reflux, Makin Murni? Bedah Reflux Optimum Kolom Distilasi",
     "2026-09-30", "https://www.instagram.com/p/Dd8LkbglNQY/", "tayang"),
    ("pabrik-kelapa-sawit-tandan-ke-cpo", "specs/2026-09-30-carousel-2-rev5.json",
     "Dari Tandan Berduri Jadi Minyak Sawit: Alur Lengkap Pabrik Kelapa Sawit",
     "2026-09-30", "https://www.instagram.com/p/Dd7_i9uFIZn/", "tayang"),
    ("baca-pid-lima-simbol-pabrik", "specs/2026-09-30-carousel-3.json",
     "Baca P&ID dalam 5 Menit: Lima Simbol yang Muncul di Hampir Semua Pabrik",
     "2026-09-30", "https://www.instagram.com/p/Dd8J_SPlMUm/", "tayang"),
    ("refinery-sawit-cpo-ke-minyak-goreng", "specs/2026-10-01-carousel-1.json",
     "Dari CPO Jadi Minyak Goreng: Empat Tahap Refinery Sawit (Olein vs Stearin)",
     "2026-10-01", "https://www.instagram.com/p/Dd8B6u6E6PN/", "tayang"),
    ("heat-exchanger-bikin-shutdown", "specs/2026-10-01-carousel-2.json",
     "Heat Exchanger: Alat Paling Sederhana yang Paling Sering Bikin Pabrik Shutdown",
     "2026-10-01", "https://www.instagram.com/p/Dd8NemJD3vA/", "tayang"),
    ("b40-biodiesel-sawit-transesterifikasi", "specs/2026-10-01-carousel-3-rev2.json",
     "B40: Bagaimana Sawit Jadi Biodiesel Lewat Transesterifikasi",
     "2026-10-02", "https://www.instagram.com/p/Dd_bheiDuVX/", "tayang"),
    ("bbm-dari-sampah-plastik-pirolisis", "specs/2026-10-01-bbm-plastik.json",
     "Dari Sampah Plastik Jadi BBM: Bedah Proses Pirolisis",
     "2026-10-01", "https://www.instagram.com/p/Dd7kKigk5SA/", "arsip"),
    ("tekanan-relief-valve-rupture-disk", "specs/2026-10-02-carousel-1.json",
     "Tekanan Itu Nyawa di Pabrik Kimia: Cara Kerja Relief Valve dan Rupture Disk",
     "2026-10-02", "https://www.instagram.com/p/Dd-dqjwD4Bi/", "tayang"),
    ("satu-barel-minyak-jadi-apa", "specs/2026-10-02-carousel-2-rev.json",
     "Satu Barel Minyak Jadi Apa Saja? Bedah Produk Kilang Cilacap dan Balikpapan",
     "2026-10-02", "https://www.instagram.com/p/Dd_RdyFDNf7/", "tayang"),
    ("pompa-vs-kompresor", "specs/2026-10-02-carousel-3.json",
     "Pompa vs Kompresor: Salah Pilih Alat, Boros Listrik Bertahun-tahun",
     "2026-10-02", "https://www.instagram.com/p/Dd_Nvp1jL2U/", "tayang"),
    ("naphtha-ke-plastik-petrokimia", "specs/2026-10-03-carousel-1.json",
     "Dari Naphtha Jadi Plastik: Alur Petrokimia Steam Cracker sampai Polimer",
     "2026-10-03", "https://www.instagram.com/p/DeBMfgKDsT_/", "tayang"),
    ("cooling-tower-cara-kerja", "specs/2026-10-03-carousel-2.json",
     "Cooling Tower: Cara Kerja AC Raksasa Pabrik yang Sering Dikira Cerobong Asap",
     "2026-10-03", "https://www.instagram.com/p/DeB5ccrD6Tv/", "tayang"),
    ("cooling-tower-wet-bulb-range-approach", "drafts/2026-10-03-cooling-tower-buku.json",
     "Menilai Cooling Tower dengan Benar: Wet Bulb, Range, Approach, dan Neraca Air",
     "2026-10-03", "https://www.instagram.com/p/DeCB7AzFDA4/", "tayang"),
    ("gas-alam-ke-urea-haber-bosch", "specs/2026-10-03-carousel-3.json",
     "Gas Alam dan Udara Jadi Pupuk Urea: Proses Haber-Bosch di Pupuk Kaltim",
     "2026-10-03", "https://www.instagram.com/p/DeDSOk2mW6F/", "tayang"),
    ("polimerisasi-konversi-carothers", "specs/2026-10-03-advanced-polimerisasi.json",
     "Konversi 99 Persen Masih Kurang: Polimerisasi Step-Growth dan Persamaan Carothers",
     "2026-10-03", "https://www.instagram.com/p/DeBQiZJDpMO/", "arsip"),
    ("neraca-massa-data-pabrik-bocor", "specs/2026-10-04-carousel-1.json",
     "Data Pabrik Selalu Bocor Angka? Cek Dulu Neraca Massanya",
     "2026-10-04", "https://www.instagram.com/p/DeDqycEjlro/", "tayang"),
    ("oleokimia-sawit-sabun-deterjen", "specs/2026-10-04-carousel-2.json",
     "Sabun di Rumahmu Ternyata dari Sawit: Alur Kimia Oleokimia",
     "2026-10-04", "https://www.instagram.com/p/DeEk3baD0Mv/", "tayang"),
    ("batch-vs-continuous-pabrik", "specs/2026-10-04-carousel-3.json",
     "Batch vs Continuous: Kenapa Pabrik Makanan dan Petrokimia Beda Jauh Cara Kerjanya",
     "2026-10-04", "https://www.instagram.com/p/DeE3CFYj2i1/", "tayang"),
    ("tebu-ke-gula-pabrik-gula", "specs/2026-10-05-carousel-1.json",
     "Tebu Tidak Cuma Diperas: Alur Lengkap Pabrik Gula dari Ladang ke Kristal",
     "2026-10-05", "https://www.instagram.com/p/DeGWfGXjwR9/", "tayang"),
    ("utilitas-pabrik-steam-air-nitrogen", "specs/2026-10-05-carousel-2.json",
     "Utilitas Pabrik: Pabrik di Dalam Pabrik yang Tidak Terlihat (Steam, Air, Nitrogen)",
     "2026-10-05", "https://www.instagram.com/p/DeG-z3Hj3Ul/", "tayang"),
    ("batu-kapur-ke-semen-kiln", "specs/2026-10-05-carousel-3.json",
     "Batu Kapur Jadi Semen Lewat Api 1450 Derajat: Proses Kiln dari Tambang ke Kantong",
     "2026-10-05", "https://www.instagram.com/p/DeHbo8HjxkY/", "tayang"),
    ("safety-instrumented-system-lapisan-pengaman", "specs/2026-10-06-carousel-1.json",
     "Pabrik Aman Bukan Karena Operator Sigap: Cara Kerja Safety Instrumented System",
     "2026-10-06", "https://www.instagram.com/p/DeI-sCKk7S0/", "tayang"),
    ("pulp-kertas-proses-kraft", "specs/2026-10-06-carousel-2-rev.json",
     "Kayu Keras Jadi Kertas Lembut: Proses Kraft di Pabrik Pulp Riau",
     "2026-10-06", "https://www.instagram.com/p/DeJjGqwj0Hb/", "tayang"),
    ("permit-to-work-kerja-panas", "specs/2026-10-06-carousel-3.json",
     "Las Lima Menit Tetap Butuh Izin: Cara Kerja Permit to Work di Pabrik Kimia",
     "2026-10-06", "https://www.instagram.com/p/DeJ_8QCjtmQ/", "tayang"),
    ("roadmap-enam-mata-kuliah-pabrik", "specs/2026-10-07-roadmap-1.json",
     "Enam Mata Kuliah yang Menjalankan Pabrik Beneran: Peta Roadmap Teknik Kimia",
     "2026-10-07", "https://www.instagram.com/p/DeMyNxZjIl2/", "tayang"),
    ("cs01-step-growth-carothers-dp-runtuh", "specs/2026-10-08-carousel-1.json",
     "CS-01 Cheat Sheet: DP Polimer Runtuh Kalau Stoikiometri Meleset 1 Persen",
     "2026-10-08", "https://www.instagram.com/p/DeOBXd7jy3k/", "tayang"),
    ("control-room-dcs-loop-kontrol", "specs/2026-10-08-carousel-2.json",
     "Satu Layar Isinya Satu Pabrik: Bedah Control Room dan Loop Kontrol DCS",
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
        "title": "Sampling Rutin: Kenapa Sampel Manual Tetap Diambil Tiap Jam",
        "hook": "Sensor online menyala terus, sampel manual tetap diambil tiap jam",
        "date": "2026-10-08",
        "ig": "https://www.instagram.com/reel/DePJYIWDhaM/",
        "src": "~/workspace/ig-ilmutekkim/media/2026-10-08/motion-1/motion.mp4",
        "poster_src": "~/workspace/ig-ilmutekkim/media/2026-10-08/motion-1/cover.jpg",
        "duration": 40.9,
        "tag": "Kendali Mutu Pabrik",
        "intro": "Sensor online membaca terus menerus, tapi pabrik tetap mengambil sampel manual tiap jam untuk diuji di lab. Video ini membedah kenapa cara manual belum ditinggalkan.",
        "tension": "Sensor cuma membaca titik yang ia sentuh dan bacaannya bisa bergeser diam-diam tanpa terasa.",
        "takeaway": "Sensor menjaga detik, lab menjaga kebenaran. Hasil lab adalah pembanding independen yang membuktikan sensor masih jujur.",
        "facts": [
            "Sensor online hanya mengukur di ujung probe, tidak mewakili seluruh aliran di pipa besar.",
            "Sampel diambil di titik sampel (sampling point), ditutup rapat, diberi label waktu, lalu diserahkan ke analis lab.",
            "Selisih hasil lab vs bacaan sensor ditindaklanjuti dengan cek proses, bukan dibiarkan.",
        ],
        "quiz": {
            "q": "Kenapa sampel lab tetap dibutuhkan padahal sensor online sudah menyala?",
            "options": ["Karena lab lebih cepat dari sensor", "Karena sensor bisa bergeser dan hanya membaca satu titik", "Karena operator butuh pekerjaan tambahan"],
            "answer": 1,
            "explain": "Sensor membaca satu titik dan bisa drift. Lab memberi nilai independen dari sampel fisik yang sama, jadi pergeseran ketahuan sebelum produk ikut bergeser.",
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
        "title": "Shift Handover: Kenapa Logbook Tulisan Tangan Belum Tergantikan",
        "hook": "Komputer mencatat angka. Logbook mencatat cerita alatnya",
        "date": "2026-10-07",
        "ig": "https://www.instagram.com/reel/DeMk3GmicdD/",
        "src": "~/workspace/ig-ilmutekkim/media/2026-10-07/motion-1/motion.mp4",
        "poster_src": "~/workspace/ig-ilmutekkim/media/2026-10-07/motion-1/cover.jpg",
        "duration": 40.9,
        "tag": "Operasi Pabrik",
        "intro": "Pabrik jalan 24 jam, operator berganti tiap shift. Video ini membedah kenapa serah terima tidak cukup mengandalkan layar, dan kenapa logbook tulisan tangan masih jadi ingatan pabrik antar shift.",
        "tension": "Layar menampilkan angka proses, tapi detail kecil seperti katup rembes hanya hidup di catatan logbook.",
        "takeaway": "Logbook adalah ingatan pabrik antar shift. Urutannya: tulis keadaan alat, baca bersama, keliling cek lapangan, tanda tangan serah terima.",
        "facts": [
            "Contoh nyata di video: katup V-204 rembes, pantau tiap jam, jangan ditinggal. Detail kualitatif seperti ini tidak muncul di angka DCS.",
            "Handover yang benar ditutup tanda tangan dua operator dan stempel waktu, tanggung jawab berpindah jelas dan bisa ditelusur.",
        ],
        "quiz": {
            "q": "Apa yang dicatat logbook tapi tidak dicatat layar DCS?",
            "options": ["Angka suhu dan tekanan", "Cerita alat, misalnya katup mana yang rembes dan perlu dipantau", "Jadwal libur operator"],
            "answer": 1,
            "explain": "DCS mencatat angka. Logbook mencatat konteks kualitatif alat, gangguan kecil, dan hal yang harus diwaspadai shift berikut.",
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
        "title": "Hilirisasi Nikel: Biji Kotor Jadi Baterai EV, Begini Jalurnya",
        "hook": "Biji nikel kotor jadi baterai EV",
        "date": "2026-10-06",
        "ig": "https://www.instagram.com/reel/DeLHZmOE0Dw/",
        "src": "~/workspace/coded-motion-graphics/videos/hilirisasi-nikel/renders/hilirisasi-nikel_v2_2026-10-07_07-38.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Hilirisasi & Proses",
        "intro": "Kadar nikel di bijih laterit cuma sekitar 1 sampai 2 persen. Video ini membedah kenapa bijihnya harus dipilah dulu, dan kenapa ada dua jalur pabrik yang sangat berbeda untuk stainless steel dan baterai EV.",
        "tension": "Kalau kadarnya cuma 1 sampai 2 persen, kenapa tidak langsung dibuat baterai?",
        "takeaway": "Nilai hilirisasi ada pada kemampuan memilah, melebur, melarutkan, dan memurnikan di pabrik. Saprolit dan limonit tidak diperlakukan sama.",
        "facts": [
            "Saprolit (kadar lebih tinggi) masuk jalur panas RKEF: rotary kiln lalu electric furnace menjadi nickel pig iron (NPI) untuk stainless steel. NPI bukan bahan baterai langsung.",
            "Limonit (kadar lebih rendah) masuk jalur basah HPAL: asam sulfat di autoclave sekitar 250°C tekanan tinggi, lalu diendapkan jadi MHP dan dimurnikan ke nikel sulfat untuk prekursor katoda.",
            "Tantangan prosesnya wajib diingat: energi besar, konsumsi asam, dan tailing atau residu yang harus dikelola.",
        ],
        "quiz": {
            "q": "Jalur mana yang menghasilkan bahan untuk baterai EV?",
            "options": ["RKEF menjadi NPI", "HPAL menjadi MHP lalu nikel sulfat", "Keduanya langsung menjadi baterai"],
            "answer": 1,
            "explain": "RKEF menghasilkan NPI untuk stainless steel. Baterai lewat HPAL: limonit dilarutkan, diendapkan jadi MHP, lalu ke nikel sulfat dan prekursor katoda.",
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
        "title": "Pasir Jadi Chip AI: Reaksi, Distilasi, dan Kristal di Baliknya",
        "hook": "Chip AI asalnya dari pasir",
        "date": "2026-10-05",
        "ig": "https://www.instagram.com/reel/DeJFBULEyhF/",
        "src": "~/workspace/coded-motion-graphics/videos/pasir-chip-ai/renders/pasir-chip-ai_v1_2026-10-06_12-20.mp4",
        "poster_src": "~/workspace/coded-motion-graphics/videos/pasir-chip-ai/cover.jpg",
        "duration": 40.9,
        "tag": "Semikonduktor",
        "intro": "Chip AI berawal dari pasir kuarsa. Video ini membedah kenapa pasir sembarangan tidak bisa langsung jadi chip, dan kenapa kemurnian ekstrem adalah inti teknik kimianya.",
        "tension": "Kalau bahannya cuma pasir, kenapa chip tidak bisa dibuat dari pasir sembarangan?",
        "takeaway": "Chip AI lahir dari reaksi, distilasi, dan kristal yang dikendalikan insinyur proses. Bukan sulap, ini teknik kimia.",
        "facts": [
            "Reduksi disederhanakan: SiO2 + 2C menjadi Si + 2CO di furnace listrik. Silikon metalurgi baru sekitar 98% murni, masih terlalu kotor untuk transistor nanometer.",
            "Silikon diubah jadi triklorosilan yang mudah menguap, sehingga pengotor bisa dipisahkan lewat distilasi. Proses Siemens lalu menumbuhkan polysilicon sekitar 99,9999999% (9N).",
            "Polysilicon dilelehkan pada 1.414°C dan ditarik jadi kristal tunggal (Czochralski), dipotong jadi wafer 300 mm, baru difabrikasi jadi chip.",
        ],
        "quiz": {
            "q": "Kenapa silikon harus diubah jadi triklorosilan dulu?",
            "options": ["Agar warnanya berubah", "Agar mudah menguap dan pengotornya bisa dipisahkan lewat distilasi", "Agar lebih murah dari pasir"],
            "answer": 1,
            "explain": "Triklorosilan mudah menguap, jadi distilasi bisa memisahkannya dari pengotor. Dari situ proses Siemens menghasilkan polysilicon ultra murni.",
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
        "hook": "Minyak mentah masuk, banyak produk keluar. Kuncinya beda titik didih",
        "date": "2026-10-05",
        "ig": "https://www.instagram.com/reel/DeG_5tXPCyo/",
        "src": "~/workspace/coded-motion-graphics/videos/minyak-mentah/renders/minyak-mentah_v2_2026-10-02.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Kilang & Distilasi",
        "intro": "Minyak mentah tidak dipisah pakai saringan, tapi pakai titik didih di satu kolom tinggi. Video ini membedah alur dari fired heater sampai produk keluar sesuai titik didihnya.",
        "tension": "Satu minyak mentah bisa jadi gas sampai residu. Apa yang memisahkannya di dalam kolom?",
        "takeaway": "Distilasi itu pisah fisik, bukan reaksi kimia. Yang dipisah titik didihnya, bukan diubah jadi zat baru.",
        "facts": [
            "Umpan dipanaskan di fired heater sampai sekitar 350°C, masuk zona flash di bawah kolom. Di atas sekitar 120°C, di bawah sekitar 350°C.",
            "Overhead paling ringan didinginkan di kondenser ke drum reflux, sebagian balik sebagai reflux agar pisahnya tajam. Dasar dididihkan lagi di reboiler, steam membantu stripping, residu keluar setelah reboiler.",
            "Urutan produk ringan ke berat: gas di bawah 40°C, bensin 40 sampai 180°C, kerosin 180 sampai 240°C, solar 240 sampai 340°C, residu di atas 340°C.",
        ],
        "quiz": {
            "q": "Distilasi minyak mentah itu pada dasarnya apa?",
            "options": ["Reaksi kimia yang mengubah minyak jadi bensin", "Pemisahan fisik berdasarkan beda titik didih", "Penyaringan pakai saringan halus"],
            "answer": 1,
            "explain": "Tidak ada zat baru yang dibuat. Campuran dipisah karena komponennya menguap dan mengembun pada suhu berbeda di tray kolom.",
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
        "title": "Process Safety Bukan Soal APD: Hazard, Risk, dan Barrier Berlapis",
        "hook": "Process safety bukan soal APD",
        "date": "2026-10-04",
        "ig": "https://www.instagram.com/reel/DeGB-GQj-j8/",
        "src": "~/workspace/coded-motion-graphics/videos/process-safety/renders/process-safety_v3_2026-10-05_08-14.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Process Safety",
        "intro": "APD melindungi orang setelah bahaya terlepas. Process safety mencegah pelepasannya sejak awal. Video ini membedah tiga kata kuncinya dan kenapa lapisannya harus independen.",
        "tension": "Kalau APD, alarm, dan operator sudah ada, kenapa kecelakaan proses besar masih bisa terjadi?",
        "takeaway": "Process safety menjaga bahan dan energi berbahaya tetap terkendali lewat lapisan yang saling tidak tergantung.",
        "facts": [
            "Risk dibaca dari kombinasi konsekuensi dan kemungkinan, bukan bahaya saja. APD tetap berguna, tapi bukan penghalang utama pelepasan besar.",
            "Contoh hitungan ilustratif: kejadian awal 1 kali per 10 tahun, tiga lapisan independen masing-masing gagal 1 dari 10 saat dibutuhkan, hasilnya 0,0001 per tahun atau 1 per 10.000 tahun. Syaratnya: lapisan benar-benar independen.",
            "Relief digambarkan menuju sistem tertutup atau flare, bukan membuang bebas ke udara.",
        ],
        "quiz": {
            "q": "Kenapa tiga lapisan bisa menurunkan frekuensi dari 1 per 10 tahun jadi 1 per 10.000 tahun?",
            "options": ["Karena tiap lapisan pasti berhasil", "Karena peluang gagalnya dikalikan, dengan syarat lapisannya independen", "Karena APD ditambah tiga lapis"],
            "answer": 1,
            "explain": "0,1 x 0,1 x 0,1 x 0,1 = 0,0001 per tahun. Itu hanya berlaku kalau lapisannya tidak berbagi penyebab gagal yang sama.",
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
        "title": "Heat Exchanger: Alat Paling Sepele yang Bisa Menghentikan Pabrik",
        "hook": "Alat paling sepele, penghenti pabrik",
        "date": "2026-10-03",
        "ig": "https://www.instagram.com/reel/DeDrJkVP2Jr/",
        "src": "~/workspace/coded-motion-graphics/videos/heat-exchanger/renders/heat-exchanger_v2_2026-10-03_21-50.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Unit Operasi",
        "intro": "Heat exchanger kelihatan cuma pipa dalam tabung. Video ini membedah kenapa arah aliran dan kerak 1 milimeter bisa menentukan hemat borosnya pabrik, sampai memaksa unit berhenti.",
        "tension": "Kalau alat ini cuma pipa dalam tabung, kenapa kerak tipis bisa memaksa satu unit berhenti total?",
        "takeaway": "Arah aliran menentukan efisiensi, kerak (fouling) menentukan kapan pabrik berhenti untuk dibersihkan.",
        "facts": [
            "Contoh terverifikasi: panas 150 ke 90°C, dingin 30 ke 80°C. Lawan arah beda suhu penggerak rata-rata (LMTD) sekitar 65°C, searah sekitar 44°C. Rasio 65 per 44 sekitar 1,48 atau panas yang dipindah bisa sekitar 48% lebih besar pada suhu ujung yang sama.",
            "Kerak 1 mm memangkas fluks panas sekitar 10%. Literatur fouling menyebut biaya sekitar 0,25% PDB negara industri dan sekitar 186 juta barel minyak per tahun dipakai kilang dunia menambal rugi fouling (estimasi Müller-Steinhagen).",
        ],
        "quiz": {
            "q": "Pada suhu ujung yang sama, kenapa lawan arah lebih efisien dari searah?",
            "options": ["Karena pipanya lebih panjang", "Karena beda suhu penggerak rata-ratanya lebih besar (65 vs 44°C)", "Karena keraknya lebih tipis"],
            "answer": 1,
            "explain": "LMTD lawan arah 65°C vs searah 44°C. Beda suhu yang lebih besar mendorong lebih banyak panas menyeberang dinding yang sama.",
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
        "title": "Haber-Bosch: Udara Jadi Pupuk, Proses Paling Penting di Dunia",
        "hook": "Udara jadi pupuk",
        "date": "2026-10-03",
        "ig": "https://www.instagram.com/reel/DeCCKsyvr7j/",
        "src": "~/workspace/coded-motion-graphics/videos/amonia/renders/amonia_v3_2026-10-01_20-21.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Proses Pupuk",
        "intro": "78% udara adalah nitrogen, tapi tanaman tidak bisa memakannya langsung. Video ini membedah Haber-Bosch: persamaan, tiga syarat ekstrem, dan kenapa tanpa recycle pabriknya rugi.",
        "tension": "Nitrogen malas bereaksi karena ikatan rangkap tiganya terlalu kuat. Bagaimana cara memaksanya jadi amonia?",
        "takeaway": "Udara plus tekanan plus katalis menjadi makanan dunia: N2 + 3H2 menjadi 2NH3, lalu menjadi urea dan pupuk nitrogen.",
        "facts": [
            "Persamaan setimbang: N2 + 3H2 menjadi 2NH3. Cek atom: N 2 atom, H 6 atom, seimbang. Ikatan N rangkap tiga sangat kuat, ikatan H tunggal mudah putus.",
            "Tiga syarat ekstrem: katalis besi memecah ikatan N, suhu tinggi 400 sampai 500°C mempercepat reaksi, tekanan tinggi 150 sampai 250 bar mendorong ke produk (Le Chatelier: 4 mol gas menjadi 2 mol gas).",
            "Reaksi eksotermik dengan delta H sekitar minus 92 kJ per mol. Sekali lewat reaktor cuma sekitar 15% yang jadi, sisanya diputar balik lewat kondensasi dan recycle. Terlalu panas, kesetimbangan bergeser balik.",
        ],
        "quiz": {
            "q": "Kenapa tekanan tinggi membantu Haber-Bosch?",
            "options": ["Karena membuat katalis meleleh", "Karena 4 mol gas menjadi 2 mol gas, makin ditekan makin jadi amonia (Le Chatelier)", "Karena menurunkan suhu reaktor"],
            "answer": 1,
            "explain": "Jumlah mol gas berkurang dari 4 ke 2. Tekanan tinggi mendorong kesetimbangan ke sisi produk yang molnya lebih sedikit.",
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
        "title": "Netralisasi Asam Basa: Yang Sebenarnya Bereaksi Cuma Dua Ion",
        "hook": "Asam ketemu basa, saling menjinakkan",
        "date": "2026-10-02",
        "ig": "https://www.instagram.com/reel/DeBVDRiPs35/",
        "src": "~/workspace/coded-motion-graphics/videos/asam-basa/renders/asam-basa_v4_2026-10-01_13-46.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Kimia Dasar Proses",
        "intro": "HCl + NaOH menjadi NaCl + H2O terlihat seperti tukar pasangan. Video ini membedah reaksi ion bersihnya, panas yang dilepas, dan kenapa titrasi harus tepat setetes demi setetes.",
        "tension": "Kalau persamaannya terlihat sederhana, apa yang sebenarnya bertabrakan dan membentuk air?",
        "takeaway": "Asam + basa = garam + air. Intinya H+ + OH- menjadi H2O, reaksi paling fundamental dari lab sekolah sampai netralisasi limbah pabrik.",
        "facts": [
            "Di larutan, HCl dan NaOH sudah terurai jadi ion. Yang benar-benar bereaksi adalah H+ + OH- menjadi H2O. Na+ dan Cl- menjadi garam NaCl. Atom dan muatan seimbang.",
            "Tiap mol air yang terbentuk melepas 57 kJ panas (delta H sekitar minus 57 kJ per mol), larutan jadi hangat. Reaksinya eksotermik.",
            "Titrasi butuh tepat 1 banding 1: 1 mol HCl butuh tepat 1 mol NaOH. Kelebihan setetes saja menggeser hasil. Fenolftalein jadi saksi: bening di asam, pink di basa, titik akhir di pH 7.",
        ],
        "quiz": {
            "q": "Dalam netralisasi HCl dan NaOH, yang sebenarnya membentuk air adalah?",
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
        "title": "Water-Gas Shift: CO Itu Racun, Ubah Jadi H2",
        "hook": "CO itu racun, ubah jadi H2",
        "date": "2026-10-02",
        "ig": "https://www.instagram.com/reel/Dd_doTMPk6j/",
        "src": "~/workspace/coded-motion-graphics/videos/shift-conversion/renders/shift-conversion_v1_2026-10-01_04-10-25.mp4",
        "poster_src": None,
        "duration": 40.9,
        "tag": "Pabrik Hidrogen",
        "intro": "CO + H2O menjadi CO2 + H2 terlihat sepele, tapi jadi tulang punggung pabrik hidrogen. Video ini membedah kenapa shift harus dua tahap: panas dulu, dingin kemudian.",
        "tension": "Kesetimbangan suka dingin, kinetika suka panas. Bagaimana cara memuaskan keduanya?",
        "takeaway": "Shift = CO jadi H2. Dua tahap reaktor (HTS lalu LTS) dengan pendingin di tengah adalah kompromi antara kecepatan dan kesetimbangan.",
        "facts": [
            "Reaksi shift eksotermik dengan delta H sekitar minus 41 kJ per mol. Atom H di H2 produk berasal dari air (steam), bukan dari CO.",
            "HTS (high temperature shift) 350 sampai 450°C katalis Fe-Cr menurunkan CO dari 15% jadi 3%. Setelah didinginkan dan panasnya dipanen jadi steam, LTS (low temperature shift) 200 sampai 250°C katalis Cu-Zn menurunkan CO dari 3% jadi 0,3%.",
            "Gas kaya H2 lalu ke CO2 removal dan PSA menghasilkan H2 murni 99,99%. Dua tahap diperlukan karena satu suhu tidak bisa cepat sekaligus tuntas.",
        ],
        "quiz": {
            "q": "Kenapa water-gas shift dibuat dua tahap HTS dan LTS?",
            "options": ["Agar pabriknya terlihat besar", "Karena kesetimbangan suka dingin tapi kinetika suka panas, jadi perlu panas dulu lalu dingin", "Karena katalisnya cuma satu jenis"],
            "answer": 1,
            "explain": "HTS cepat di suhu tinggi tapi tidak tuntas. LTS di suhu rendah menggeser kesetimbangan sampai CO tersisa 0,3%. Pendingin di tengah memanen panasnya jadi steam.",
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
    "sampling-rutin-lab": {
        "lead": "Pabrik modern punya sensor yang membaca proses tiap detik. Kenapa operatornya masih jalan membawa botol sampel ke lab tiap jam?",
        "sections": [
            {"h": "Sensor hanya membaca titik yang ia sentuh", "t": 6, "paras": [
                "Sensor online seperti probe pH, konduktivitas, atau densitas hanya mengukur fluida yang menyentuh ujung probenya. Di pipa besar, sebagian besar aliran lewat jauh dari titik itu, dan yang tidak tersentuh sensor tidak ikut terukur. Bacaan di layar adalah potret satu titik, bukan potret seluruh aliran [1].",
                "Di sinilah sampel fisik mengambil peran. Sejumlah kecil fluida benar-benar dikeluarkan dari proses dan diperiksa langsung, sehingga yang dinilai adalah bahannya, bukan sinyal listrik yang mewakilinya."]},
            {"h": "Bacaan sensor bisa bergeser diam-diam", "t": 13, "paras": [
                "Sensor mengalami drift: bacaannya bergeser pelan menjauhi nilai sebenarnya karena kerak menempel di probe, elektroda menua, atau elektronikanya berubah. Pergeseran ini tidak memicu alarm, karena dari sudut pandang sistem, angkanya terlihat normal saja.",
                "Kalau tidak ada pembanding independen, yang bergeser bukan cuma garis di layar. Produk ikut bergeser keluar spesifikasi, dan penyimpangan baru ketahuan setelah mutu produk terlanjur turun [1]."]},
            {"h": "Sampel yang mewakili: titik, wadah, label waktu", "t": 20, "paras": [
                "Sampling yang benar dimulai dari titik sampel yang memang dirancang di pipa, bukan dari keran sembarangan. Cairan pertama dibuang dulu agar yang masuk botol adalah fluida yang segar dari aliran, lalu botol ditutup rapat, terutama bila komponennya mudah menguap.",
                "Setiap botol diberi label waktu. Detail ini menentukan nilai hasil lab: angka laboratorium harus bisa dipasangkan dengan kondisi proses pada jam yang sama, bukan dibandingkan dengan bacaan sensor dari waktu yang berbeda [1]."]},
            {"h": "Lab sebagai pembanding independen", "t": 27, "paras": [
                "Di lab, sampel diukur dengan metode yang terkalibrasi terhadap standar, misalnya titrasi atau spektrofotometri. Hasilnya adalah angka independen yang tidak mewarisi kesalahan sensor lapangan [2].",
                "Hasil lab lalu dibandingkan dengan bacaan sensor pada waktu yang sama. Bila cocok, sensor terbukti jujur. Bila selisih melewati batas, tindak lanjutnya adalah kalibrasi atau cek proses, bukan membiarkan selisih itu membesar diam-diam."]},
            {"h": "Kenapa tidak semua diganti sensor saja", "t": None, "paras": [
                "Tidak semua variabel punya sensor inline yang andal dan ekonomis, dan setiap titik ukur tambahan menambah biaya pasang serta perawatan. Selama mutu produk harus dibuktikan dengan pengukuran langsung atas bahannya, sampel fisik ke lab tetap menjadi rujukan yang tidak tergantikan [1]."]},
        ],
        "refs": [
            "Green, D. W., & Southard, M. Z. (Eds.). (2019). Perry's Chemical Engineers' Handbook (9th ed.). McGraw-Hill Education.",
            "Skoog, D. A., West, D. M., Holler, F. J., & Crouch, S. R. (2014). Fundamentals of Analytical Chemistry (9th ed.). Cengage Learning.",
        ]},
    "shift-handover-logbook": {
        "lead": "Alatnya tidak berubah saat shift berganti. Yang berubah orangnya, dan di celah pergantian itulah cerita alat paling sering hilang.",
        "sections": [
            {"h": "Layar menampilkan angka, logbook menyimpan cerita", "t": 6, "paras": [
                "Sistem kontrol menampilkan angka proses: suhu, tekanan, level, laju alir. Yang tidak tampil di sana adalah konteks kualitatif alat, misalnya katup V-204 yang rembes dan harus dipantau tiap jam, bunyi pompa yang berubah, atau perbaikan sementara yang sedang berjalan.",
                "Detail seperti itu tidak punya kolom di layar angka. Ia hanya hidup bila ditulis, dan logbook adalah tempat pabrik menuliskan ingatannya antar shift [1]."]},
            {"h": "Kenapa momen ganti shift paling rawan", "t": 13, "paras": [
                "Serah terima adalah perpindahan informasi antara dua orang dengan keadaan lapangan yang sama tapi pemahaman yang berbeda. Operator yang pulang membawa konteks delapan jam terakhir; operator yang datang mulai dari nol. Setiap detail yang tidak terucap atau tertulis akan hilang di titik ini.",
                "Karena itu literatur keselamatan proses menempatkan komunikasi shift sebagai salah satu barrier, lapisan pengaman yang sama seriusnya dengan alarm dan interlock [1]."]},
            {"h": "Tiga langkah handover yang benar", "t": 20, "paras": [
                "Urutannya sederhana tapi tidak bisa dilompati. Pertama, tulis keadaan alat apa adanya, termasuk yang tidak normal. Kedua, baca catatan itu bersama operator pengganti agar salah tafsir ketahuan saat itu juga, bukan setelah kejadian.",
                "Ketiga, keliling cek lapangan berdua. Langkah ini yang paling sering dikorbankan, padahal handover tidak selesai di meja control room: katup yang dicatat rembes harus dilihat langsung oleh orang yang akan menjaganya."]},
            {"h": "Tanda tangan menutup serah terima", "t": 27, "paras": [
                "Serah terima ditutup tanda tangan dua operator dan stempel waktu. Dari titik itu, tanggung jawab berpindah dengan jelas dan bisa ditelusur: bila nanti ada kejadian, catatan menunjukkan shift mana yang mengetahui apa, dan kapan [1].",
                "Tanpa bukti tertulis yang ditandatangani, investigasi kejadian berubah jadi adu ingatan. Dengan logbook, yang diperiksa adalah catatan, bukan klaim."]},
            {"h": "Kertas atau elektronik, prinsipnya sama", "t": None, "paras": [
                "Banyak pabrik kini memakai logbook elektronik, dan itu sah saja. Medianya boleh berubah, prinsipnya tidak: keadaan alat ditulis spesifik, dibaca bersama oleh dua shift, diverifikasi di lapangan, lalu ditutup dengan pengesahan yang bisa ditelusur [2]."]},
        ],
        "refs": [
            "Center for Chemical Process Safety. (2007). Guidelines for Risk Based Process Safety. AIChE/Wiley.",
            "Health and Safety Executive. (2006). Managing Shift Work: Health and Safety Guidance (HSG256). HSE Books.",
        ]},
    "hilirisasi-nikel-baterai-ev": {
        "lead": "Bijih nikel Indonesia kadarnya cuma sekitar 1 sampai 2 persen. Kenapa tidak langsung dibuat baterai saja?",
        "sections": [
            {"h": "Memilah dulu: saprolit dan limonit", "t": 6.8, "paras": [
                "Bijih laterit tidak seragam. Profilnya berlapis, dan dua jenis utamanya, saprolit dan limonit, berbeda kadar serta kimia mineralnya. Dengan kadar nikel total hanya sekitar 1 sampai 2 persen, hampir seluruh massa bijih adalah material bukan nikel yang harus disingkirkan lewat proses [1].",
                "Karena itu keputusan pertama di pabrik bukan melebur atau melarutkan, melainkan memilah. Jenis bijih menentukan jalur prosesnya, dan salah pilah berarti salah pabrik."]},
            {"h": "Jalur panas RKEF untuk saprolit", "t": 13.6, "paras": [
                "Saprolit yang kadarnya relatif lebih tinggi diolah lewat jalur pirometalurgi RKEF: dikeringkan dan dikalsinasi di rotary kiln, lalu direduksi di electric furnace. Produknya nickel pig iron (NPI), besi kasar kaya nikel [1].",
                "NPI adalah bahan baku stainless steel, bukan bahan baterai. Bentuk kimia dan kadarnya memang dirancang untuk peleburan baja, sehingga rantai baterai tidak mulai dari sini."]},
            {"h": "Jalur basah HPAL untuk limonit", "t": 20.4, "paras": [
                "Limonit yang kadarnya lebih rendah menempuh jalur hidrometalurgi HPAL (high pressure acid leaching). Bijih dilarutkan dengan asam sulfat di dalam autoclave pada sekitar 250°C dan tekanan tinggi, sehingga nikel berpindah dari padatan ke larutan [1].",
                "Angka 250°C di sini adalah kondisi pelarutan, bukan suhu lebur. Yang bekerja memisahkan nikel adalah asamnya, dan bejana prosesnya adalah bejana tekan, bukan tungku."]},
            {"h": "Dari larutan jadi MHP dan nikel sulfat", "t": 27.2, "paras": [
                "Larutan nikel dari HPAL tidak langsung menjadi baterai. Nikel diendapkan sebagai MHP (mixed hydroxide precipitate), produk antara yang masih harus dimurnikan lagi menjadi nikel sulfat, garam dengan kemurnian yang dituntut industri baterai [2].",
                "Nikel sulfat inilah bahan prekursor katoda baterai kendaraan listrik. Jadi rantai nilainya panjang: bijih, larutan, endapan, garam murni, prekursor, baru sel baterai."]},
            {"h": "Harga yang dibayar: energi, asam, dan tailing", "t": None, "paras": [
                "Kedua jalur membayar harga prosesnya sendiri. RKEF menuntut energi listrik besar untuk furnace; HPAL menuntut asam sulfat dalam jumlah besar dan pengelolaan residu atau tailing yang volumenya raksasa, karena 98 persen lebih massa bijih berakhir bukan sebagai produk [1].",
                "Di situlah nilai hilirisasi sebenarnya diuji: bukan pada bijihnya, tapi pada kemampuan pabrik memilah, melebur, melarutkan, dan memurnikan dengan harga proses yang masih masuk akal."]},
        ],
        "refs": [
            "Habashi, F. (Ed.). (1997). Handbook of Extractive Metallurgy. Wiley-VCH.",
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Nickel. Wiley-VCH.",
        ]},
    "pasir-jadi-chip-ai": {
        "lead": "Chip AI paling canggih berawal dari bahan yang sama dengan pasir di pantai. Yang membedakan bukan bahannya, melainkan kemurniannya.",
        "sections": [
            {"h": "Reduksi karbotermik: pasir jadi silikon metalurgi", "t": 6.8, "paras": [
                "Langkah pertama adalah reduksi pasir kuarsa (SiO\u2082) dengan karbon di furnace listrik: SiO\u2082 + 2C \u2192 Si + 2CO. Produknya silikon metalurgi dengan kemurnian baru sekitar 98 sampai 99 persen [1].",
                "Untuk baja, angka itu sudah cukup. Untuk transistor berukuran nanometer, sisa pengotor 1 sampai 2 persen terlalu kotor, karena sifat listrik semikonduktor ditentukan oleh pengotor pada tingkat yang jauh lebih halus."]},
            {"h": "Kenapa harus jadi gas dulu: triklorosilan", "t": 13.6, "paras": [
                "Trik teknik kimianya ada di sini. Silikon diubah menjadi triklorosilan, senyawa yang mudah menguap. Begitu berbentuk gas, pemisahan pengotor bisa dilakukan dengan distilasi fraksinasi, prinsip yang sama dengan kolom distilasi di kilang minyak [1].",
                "Kata kuncinya adalah mudah menguap: hanya zat yang bisa diuapkan dan diembunkan berulang kali yang bisa dimurnikan sampai tingkat ekstrem lewat perbedaan titik didih."]},
            {"h": "Proses Siemens dan arti kemurnian 9N", "t": 20.4, "paras": [
                "Triklorosilan murni diuraikan kembali pada batang silikon panas lewat proses Siemens, menumbuhkan polysilicon dengan kemurnian sekitar 99,9999999 persen, yang ditulis 9N (sembilan angka sembilan) [1].",
                "Chip modern umumnya memakai silikon di rentang 9N sampai 11N. Sebagai bayangan skala: pada 9N, dari satu miliar atom, hanya sekitar satu atom yang bukan silikon."]},
            {"h": "Leleh 1.414\u00b0C, tarik kristal, potong wafer", "t": 27.2, "paras": [
                "Polysilicon dilelehkan pada titik leleh silikon, 1.414\u00b0C, lalu ditarik perlahan menjadi kristal tunggal. Kristal ini dipotong menjadi wafer, umumnya berdiameter 300 mm, dan dari wafer itulah chip AI difabrikasi lapis demi lapis [2].",
                "Urutan lengkapnya menunjukkan peran teknik kimia dari hulu: reaksi reduksi, pemurnian lewat distilasi, pertumbuhan kristal. Chip lahir dari proses kimia yang dikendalikan, bukan dari pasir yang dipotong begitu saja."]},
        ],
        "refs": [
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Silicon. Wiley-VCH.",
            "Doering, R., & Nishi, Y. (Eds.). (2007). Handbook of Semiconductor Manufacturing Technology (2nd ed.). CRC Press.",
        ]},
    "distilasi-minyak-mentah": {
        "lead": "Merebus minyak mentah sekali tidak akan pernah menghasilkan bensin. Campurannya terlalu rapat, dan fisika pemisahannya tidak bekerja seperti itu.",
        "sections": [
            {"h": "Campuran ratusan hidrokarbon, bukan zat tunggal", "t": 6.5, "paras": [
                "Minyak mentah adalah campuran ratusan senyawa hidrokarbon dengan titik didih yang berdekatan dan bertumpuk. Sekali rebus hanya menghasilkan uap yang komposisinya tetap campuran, karena fraksi ringan dan berat menguap bersamaan [1].",
                "Umpan karena itu dipanaskan sekitar 350°C di fired heater lalu masuk zona flash di kolom, titik awal uap dan cairan mulai berpisah. Dari titik ini, pemisahan diselesaikan bukan oleh satu pendidihan, melainkan oleh kontak berulang."]},
            {"h": "Kontak uap dan cairan berulang di tray", "t": 13, "paras": [
                "Di dalam kolom, uap naik dan cairan turun melewati tray-tray. Pada setiap tray, uap dan cairan berkontak dan saling bertukar komponen: yang ringan cenderung lanjut menguap, yang berat mengembun dan turun.",
                "Satu kolom pada dasarnya adalah rangkaian banyak tahap kesetimbangan yang ditumpuk vertikal. Pengulangan kontak inilah mesin pemisahnya, dan inilah yang tidak bisa digantikan oleh satu kali rebusan [1][2]."]},
            {"h": "Reflux: yang membuat pisahnya tajam", "t": 19.5, "paras": [
                "Uap paling ringan keluar dari puncak kolom, didinginkan di kondenser, ditampung di reflux drum, lalu sebagian dikembalikan ke kolom sebagai reflux. Cairan yang kembali ini membasahi tray-tray atas dan mempertemukan uap naik dengan cairan yang lebih murni.",
                "Tanpa reflux, produk atas tercemar fraksi yang lebih berat. Reflux yang dikembalikan bukan pemborosan, melainkan harga untuk ketajaman pisah [2]."]},
            {"h": "Profil suhu dan produk per tingkat", "t": 26.5, "paras": [
                "Karena campuran mengembun dan menguap bertingkat, suhu kolom membentuk gradien: sekitar 120°C di puncak dan 350°C di dasar yang dipanaskan reboiler. Produk diambil pada tingkat yang suhunya sesuai titik didihnya, dari gas paling ringan di atas sampai residu paling berat di bawah [1].",
                "Urutan produknya mengikuti titik didih, bukan jenis zat yang direaksikan. Distilasi adalah pisah fisik berdasarkan volatilitas; tidak ada molekul yang diubah menjadi molekul lain di dalam kolom."]},
        ],
        "refs": [
            "Seader, J. D., Henley, E. J., & Roper, D. K. (2016). Separation Process Principles (4th ed.). Wiley.",
            "Kister, H. Z. (1992). Distillation Design. McGraw-Hill.",
        ]},
    "process-safety-bukan-apd": {
        "lead": "Helm dan sarung tangan tidak menghentikan vessel yang pecah. Kecelakaan proses berskala besar dicegah jauh sebelum bahayanya terlepas.",
        "sections": [
            {"h": "Dua jenis kecelakaan yang sering dicampur", "t": 6.8, "paras": [
                "Kecelakaan personal seperti terpeleset, terjepit, atau tersiram kecil adalah wilayah APD, dan APD memang efektif di sana. Process safety menyasar kejadian yang berbeda kelas: pelepasan bahan atau energi berbahaya dalam skala besar dari vessel, pipa, dan reaktor bertekanan [1].",
                "Pada pelepasan besar, yang menentukan selamat atau tidak bukanlah helm pekerja, melainkan apakah pelepasannya dicegah sejak dari desain dan operasi prosesnya."]},
            {"h": "Hazard, risk, dan dua komponen risk", "t": 13.6, "paras": [
                "Hazard adalah potensi bahayanya: bahan mudah terbakar, tekanan tinggi, suhu ekstrem. Risk adalah gabungan dua komponen, seberapa parah konsekuensinya dan seberapa mungkin kejadian itu terjadi [1].",
                "Menyederhanakan risk menjadi sekadar ada bahaya membuat prioritas pengamanan salah arah. Dua bahaya yang sama bisa menuntut perlakuan berbeda karena kemungkinan dan konsekuensinya berbeda."]},
            {"h": "Barrier berlapis saat tekanan naik", "t": 20.4, "paras": [
                "Pengamanan proses disusun berlapis dan bekerja berurutan. Kontrol proses dasar menahan kondisi tetap normal. Bila gagal, trip otomatis menghentikan proses. Bila tekanan masih naik, relief valve membuangnya ke sistem tertutup atau flare. Tanggap darurat adalah lapisan terakhir, bukan yang pertama [2].",
                "Urutannya penting: setiap lapisan menangkap kegagalan lapisan sebelumnya, dan lapisan luar hanya bekerja bila semua lapisan di dalamnya sudah gagal."]},
            {"h": "Syarat independen dalam hitungan lapisan", "t": 27.2, "paras": [
                "Ilustrasi hitungnya begini. Kejadian awal terjadi 1 kali per 10 tahun. Tiga lapisan independen, masing-masing gagal 1 dari 10 kali saat dibutuhkan, membuat frekuensinya 0,0001 per tahun, atau 1 per 10.000 tahun.",
                "Perkalian itu hanya sah bila lapisannya benar-benar independen. Bila satu penyebab yang sama bisa menjatuhkan dua lapisan sekaligus, misalnya sensor yang sama dipakai kontrol dan trip, angka amannya runtuh. Independensi bukan detail administratif, melainkan syarat matematisnya [2]."]},
            {"h": "APD tetap perlu, tapi posisinya terakhir", "t": None, "paras": [
                "Process safety tidak membuang APD. APD tetap dipakai setiap hari untuk risiko personal. Bedanya, APD berada di urutan terakhir hierarki pengendalian: ia melindungi orang setelah bahaya terlepas, sedangkan process safety bekerja agar pelepasannya tidak pernah terjadi [1]."]},
        ],
        "refs": [
            "Crowl, D. A., & Louvar, J. F. (2019). Chemical Process Safety: Fundamentals with Applications (4th ed.). Pearson.",
            "Center for Chemical Process Safety. (2007). Guidelines for Risk Based Process Safety. AIChE/Wiley.",
        ]},
    "heat-exchanger-penghenti-pabrik": {
        "lead": "Kerak setebal 1 milimeter sanggup memaksa satu unit pabrik berhenti total. Dan kerak itu menempel di alat yang paling dianggap sepele.",
        "sections": [
            {"h": "Panas menyeberang, cairan tidak bertemu", "t": 6.8, "paras": [
                "Heat exchanger bekerja dengan prinsip yang sangat sederhana: dua aliran dipisahkan dinding logam, panas menyeberang melewati dinding, dan kedua cairannya tidak pernah bertemu. Contoh angka di artikel ini: aliran panas turun dari 150 ke 90°C, aliran dingin naik dari 30 ke 80°C [1].",
                "Kesederhanaannya menipu. Alat ini menentukan berapa banyak energi yang berhasil dipakai ulang di pabrik, dan energi adalah salah satu biaya operasi terbesar."]},
            {"h": "LMTD: beda suhu penggerak panas", "t": 13.6, "paras": [
                "Laju pindah panas digerakkan oleh beda suhu antara dua aliran, yang berubah sepanjang alat. Ukuran penggeraknya diringkas sebagai LMTD (log mean temperature difference), beda suhu rata-rata logaritmik antara ujung-ujungnya [1].",
                "Di sinilah arah aliran menentukan. Pada konfigurasi searah, beda suhu menyusut tajam di sepanjang alat. Pada lawan arah, beda suhunya terjaga lebih merata dari ujung ke ujung, dan LMTD-nya lebih besar [2]."]},
            {"h": "65 vs 44\u00b0C: dari mana angka 48 persen", "t": 20.4, "paras": [
                "Dengan angka ujung yang sama persis (150 ke 90°C dan 30 ke 80°C), lawan arah menghasilkan LMTD sekitar 65°C, sedangkan searah hanya sekitar 44°C. Rasionya 65 per 44, yaitu 1,48.",
                "Artinya, pada luas permukaan yang sama, panas yang dipindahkan bisa sekitar 48 persen lebih besar hanya dengan membalik arah aliran. Itulah sebabnya heat exchanger industri hampir selalu dirancang lawan arah [1]."]},
            {"h": "Fouling: kerak, biaya, dan shutdown", "t": 27.2, "paras": [
                "Musuh besarnya adalah fouling, endapan kerak yang tumbuh di dinding pindah panas. Kerak adalah isolator: tebal 1 mm saja sudah memangkas fluks panas sekitar 10 persen, dan alat harus bekerja lebih keras untuk hasil yang sama.",
                "Skala kerugiannya tidak kecil. Literatur fouling mengestimasi biayanya sekitar 0,25 persen PDB negara industri, dan sekitar 186 juta barel minyak per tahun dipakai kilang dunia hanya untuk menambal rugi fouling. Ujung yang paling mahal: unit berhenti total untuk dibersihkan."]},
            {"h": "Merancang melawan kerak sejak di kertas", "t": None, "paras": [
                "Karena fouling tidak terhindarkan, perancangan heat exchanger menyisihkan margin berupa faktor pengotoran sejak awal, sebagaimana diatur dalam standar perancangan penukar panas. Alat dirancang sedikit lebih besar dari kebutuhan bersihnya, agar saat kerak tumbuh, pabrik masih punya waktu sebelum harus berhenti [3]."]},
        ],
        "refs": [
            "Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2007). Fundamentals of Heat and Mass Transfer (6th ed.). Wiley.",
            "Kern, D. Q. (1950). Process Heat Transfer. McGraw-Hill.",
            "Tubular Exchanger Manufacturers Association. (2019). Standards of the Tubular Exchanger Manufacturers Association (10th ed.). TEMA.",
        ]},
    "haber-bosch-udara-jadi-pupuk": {
        "lead": "Udara yang kamu hirup 78 persennya nitrogen, tapi tidak ada tanaman yang bisa memakannya. Satu proses industri mengubah gas malas itu menjadi makanan dunia.",
        "sections": [
            {"h": "Ikatan rangkap tiga yang keras kepala", "t": 6.8, "paras": [
                "Reaksinya ringkas: N\u2082 + 3H\u2082 \u2192 2NH\u2083. Atomnya seimbang, 2 nitrogen dan 6 hidrogen di kedua sisi. Kesulitannya bukan di persamaan, melainkan di ikatan rangkap tiga pada molekul N\u2082 yang sangat kuat, membuat nitrogen terkenal malas bereaksi [1].",
                "Seluruh rekayasa Haber-Bosch pada dasarnya adalah cara memaksa ikatan itu putus dalam skala industri, terus-menerus, dengan harga yang masih masuk akal."]},
            {"h": "Tiga syarat ekstrem dan tarik-menariknya", "t": 13.6, "paras": [
                "Tiga syarat dipakai bersamaan. Katalis besi membantu memecah ikatan N\u2082. Suhu 400 sampai 500°C mempercepat reaksi. Tekanan 150 sampai 250 bar mendorong kesetimbangan ke arah produk, karena 4 mol gas berubah menjadi 2 mol gas, sesuai prinsip Le Chatelier [1][2].",
                "Syarat-syarat ini saling bertarik. Suhu tinggi baik untuk kecepatan tapi buruk untuk kesetimbangan reaksi eksotermik. Tekanan tinggi baik untuk hasil tapi mahal untuk peralatan. Angka operasinya adalah kompromi di tengah tarik-menarik itu."]},
            {"h": "Sekali lewat cuma 15 persen: kenapa recycle menentukan", "t": 20.4, "paras": [
                "Sekali campuran gas melewati reaktor, hanya sekitar 15 persen yang berubah menjadi amonia. Amonia lalu dipisahkan dengan kondensasi, dan gas yang belum bereaksi diputar balik masuk reaktor lagi.",
                "Tanpa recycle, lebih dari 80 persen bahan baku terbuang setiap putaran. Recycle bukan aksesori, melainkan penentu pabrik ini untung atau rugi [1]."]},
            {"h": "Eksotermik: panas sebagai pedang bermata dua", "t": 27.2, "paras": [
                "Reaksinya eksotermik dengan \u0394H sekitar minus 92 kJ per mol. Panas yang dilepas membantu menjaga suhu reaktor, tapi bila bed katalis terlalu panas, kesetimbangan justru bergeser balik menjauhi produk.",
                "Karena itu reaktor amonia dirancang mengelola panasnya sendiri dengan hati-hati, mendinginkan antar tahap agar konversi per lintasan tetap tinggi tanpa mengorbankan kesetimbangan [1]."]},
            {"h": "Dari amonia ke urea dan pupuk", "t": None, "paras": [
                "Amonia adalah pintu tengahnya. Sebagian besar amonia dunia diolah lagi menjadi urea dan pupuk nitrogen lain, dan dari sanalah nitrogen dari udara akhirnya sampai ke tanaman. Tanpa proses ini, separuh lebih pangan dunia tidak punya sumber nitrogennya [2]."]},
        ],
        "refs": [
            "Appl, M. (1999). Ammonia: Principles and Industrial Practice. Wiley-VCH.",
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Ammonia. Wiley-VCH.",
        ]},
    "netralisasi-asam-basa": {
        "lead": "Persamaan asam basa yang kamu hafal di sekolah menyembunyikan pemeran utamanya. Yang benar-benar bereaksi ternyata cuma dua ion.",
        "sections": [
            {"h": "Tukar pasangan yang terlihat", "t": 6.5, "paras": [
                "Ditulis sebagai molekul, netralisasi tampak seperti tukar pasangan: HCl + NaOH \u2192 NaCl + H\u2082O. Atom dan muatannya seimbang, dan untuk keperluan praktis persamaan ini benar.",
                "Tapi persamaan molekuler menyembunyikan apa yang sebenarnya terjadi di dalam larutan, karena di dalam air, kedua zat itu sudah tidak berbentuk molekul lagi [1]."]},
            {"h": "Reaksi ion bersih: H\u207a + OH\u207b \u2192 H\u2082O", "t": 13, "paras": [
                "Asam kuat dan basa kuat terurai sempurna menjadi ion-ionnya di larutan. Dari semua ion yang ada, yang benar-benar bereaksi hanyalah H\u207a + OH\u207b \u2192 H\u2082O. Inilah reaksi ion bersihnya.",
                "Ion Na\u207a dan Cl\u207b tidak berubah dari awal sampai akhir; keduanya ion penonton yang akhirnya tinggal sebagai garam NaCl di larutan. Persamaan yang panjang ternyata digerakkan satu reaksi ion yang sangat sederhana [1][2]."]},
            {"h": "57 kJ per mol air: dari mana panasnya", "t": 19.5, "paras": [
                "Pembentukan air dari H\u207a dan OH\u207b melepas sekitar 57 kJ panas per mol air yang terbentuk. Reaksinya eksotermik, dan itulah sebabnya gelas terasa hangat saat asam dan basa kuat dicampur.",
                "Karena reaksi ionnya selalu sama, entalpi netralisasi asam kuat oleh basa kuat hampir konstan untuk pasangan asam basa kuat mana pun. Yang berubah hanyalah ion penontonnya [2]."]},
            {"h": "Titrasi: tepat 1 banding 1 dan saksi fenolftalein", "t": 26.5, "paras": [
                "Perbandingan reaksinya tepat 1 banding 1: satu mol HCl membutuhkan tepat satu mol NaOH. Kelebihan setetes saja membuat campuran meleset dari titik ekuivalen, yang untuk pasangan asam kuat dan basa kuat berada di pH 7 [1].",
                "Fenolftalein menjadi saksi visualnya: bening di asam, pink di basa. Perubahan warnanya menandai kapan penambahan harus berhenti, setetes demi setetes."]},
            {"h": "Satu reaksi, banyak skala", "t": None, "paras": [
                "Reaksi yang sama bekerja di obat maag yang menetralkan asam lambung, di lab sekolah saat titrasi, dan di pabrik saat air limbah asam atau basa dinetralkan sebelum dibuang. Skalanya berbeda jauh, reaksi ionnya persis sama [1]."]},
        ],
        "refs": [
            "Skoog, D. A., West, D. M., Holler, F. J., & Crouch, S. R. (2014). Fundamentals of Analytical Chemistry (9th ed.). Cengage Learning.",
            "Atkins, P., & de Paula, J. (2014). Atkins' Physical Chemistry (10th ed.). Oxford University Press.",
        ]},
    "water-gas-shift-co-jadi-h2": {
        "lead": "Untuk membuat hidrogen murni, pabrik lebih dulu menghasilkan CO, gas beracun yang kemudian harus disingkirkan sampai tinggal 0,3 persen.",
        "sections": [
            {"h": "Hidrogennya berasal dari air, bukan dari CO", "t": 6.5, "paras": [
                "Reaksi water-gas shift adalah CO + H\u2082O \u2192 CO\u2082 + H\u2082, eksotermik dengan \u0394H sekitar minus 41 kJ per mol. Reaksi ini adalah tulang punggung pabrik hidrogen karena mengubah CO yang tidak diinginkan menjadi H\u2082 tambahan [1].",
                "Yang sering salah kaprah: atom hidrogen pada produk H\u2082 berasal dari air (steam), bukan dari CO. CO menyumbang karbonnya untuk dibawa pergi sebagai CO\u2082."]},
            {"h": "Tahap panas: HTS supaya reaksi cepat", "t": 13, "paras": [
                "Tahap pertama adalah HTS (high temperature shift) pada 350 sampai 450°C dengan katalis Fe-Cr. Suhu tinggi membuat reaksi berjalan cepat, dan kadar CO turun dari sekitar 15 persen menjadi 3 persen [1][2].",
                "Sebagian besar pekerjaan selesai di tahap ini, tapi 3 persen masih jauh dari cukup bersih untuk hidrogen murni. Menyelesaikan sisanya di suhu setinggi ini tidak efisien, karena kesetimbangan reaksi eksotermik memburuk saat panas."]},
            {"h": "Didinginkan di tengah, panasnya dipanen", "t": 19.5, "paras": [
                "Di antara dua tahap, gas didinginkan. Panas dari reaksi eksotermik tahap pertama tidak dibuang begitu saja, melainkan dipanen untuk menghasilkan steam.",
                "Pendinginan ini melayani dua tujuan sekaligus: menyiapkan gas ke suhu tahap kedua yang lebih rendah, dan memulihkan energi reaksinya sebagai utilitas yang berguna [1]."]},
            {"h": "Tahap dingin: LTS supaya reaksi tuntas", "t": 26.5, "paras": [
                "Tahap kedua adalah LTS (low temperature shift) pada 200 sampai 250°C dengan katalis Cu-Zn, menurunkan CO dari 3 persen menjadi 0,3 persen. Katalisnya berbeda karena suhunya berbeda; satu katalis tidak cocok untuk dua dunia suhu ini [1][2].",
                "Setelah CO\u2082 disingkirkan dan gas dimurnikan lewat PSA, hasilnya hidrogen murni 99,99 persen. Dua tahap reaktor dengan pendingin di tengah adalah kompromi yang menyelesaikan konflik klasik: kesetimbangan menyukai dingin, kinetika menyukai panas."]},
        ],
        "refs": [
            "Ullmann's Encyclopedia of Industrial Chemistry. (2012). Hydrogen. Wiley-VCH.",
            "Newsome, D. S. (1980). The Water-Gas Shift Reaction. Catalysis Reviews: Science and Engineering, 21(2).",
        ]},
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
<link rel="stylesheet" href="/assets/css/style.css?v=4">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23131518'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23F4F4F2' font-family='Arial' font-weight='bold'>IT</text></svg>">
</head>
<body>
<header class="site-header">
  <a class="brand" href="/">ilmu<span>tekkim</span></a>
  <nav>
    <a href="/">Articles &amp; Videos</a>
    <a href="/riset/">Riset</a> <a href="/jalur/">Jalur</a> <a href="/glosarium/">Glosarium</a> <a href="/referensi/">Referensi</a> <a href="/kalkulator/">Kalkulator</a>
    <a class="btn-ig" href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">Instagram</a>
  </nav>
</header>
<main>
"""

FOOT = """
</main>
<footer>
  <div class="foot-brand">ilmu<span>tekkim</span></div>
  <p>Bikin teknik kimia asik. Pabrik, proses, safety, dan AI. Ditulis insinyur kimia ITB.</p>
  <p><a href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">@ilmutekkim di Instagram</a> &middot; <a href="/video/">Video interaktif</a> &middot; <a href="/riset/">Riset</a> <a href="/jalur/">Jalur</a> <a href="/glosarium/">Glosarium</a> <a href="/referensi/">Referensi</a> <a href="/kalkulator/">Kalkulator</a> &middot; <a href="/tentang/">Tentang</a></p>
  <p class="fine">Artikel dan video di situs ini adalah versi baca dan tonton dari konten Instagram @ilmutekkim. Foto berasal dari Pexels dan Unsplash, kredit tercantum di tiap gambar.</p>
</footer>
<script src="/assets/js/main.js?v=5"></script>
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
        desc = (a["lead"][0] if a["lead"] else a["sub"])[:155]
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
                         desc="Versi artikel dari video teknik kimia @ilmutekkim: tonton videonya, baca penjelasan mendalamnya per subtopik, lalu cek pahammu lewat kuis.",
                         url=BASE + "/video/", ogtype="website", ogimg="")
    vindex += f"""
<article class="post wide">
<p class="eyebrow">Video interaktif</p>
<h1>Video teknik kimia, versi artikel.</h1>
<p class="lead">Sepuluh video teknik kimia dari @ilmutekkim, masing-masing dengan versi artikel lengkapnya.
Di Instagram enak ditonton, di sini enak dibaca: tonton videonya, baca penjelasan mendalam per subtopik sambil lompat ke detik tertentu dari judul bagiannya, lalu jawab kuisnya.</p>
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
<p class="lead">Setiap bedah di halaman ini ditulis dari abstrak paper yang terverifikasi: masalahnya apa, metodenya bagaimana, angka temuannya persis seperti tertulis, batasnya di mana, dan artinya apa buat pabrik. Di akhir selalu ada kesimpulan yang bisa langsung dipakai: paper ini perlu dibaca penuh, atau abstraknya saja sudah cukup.</p>
<p class="meta">{len(research)} bedah jurnal &middot; campuran internasional dan Indonesia &middot; standar bedah: angka hanya dari abstrak, abstrak tidak disalin, selalu ada catatan kritis</p>
</article>
<section id="seri" class="series-bar">
  <h2>Jelajahi per topik</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{rchips}</div>
  <input id="search" type="search" placeholder="Cari bedah, contoh: hidrogen, katalis, pirolisis..." aria-label="Cari bedah riset">
</section>
<section id="artikel" class="grid">
{rcards}
</section>
<p id="no-result" hidden>Tidak ada bedah yang cocok. Coba kata kunci lain.</p>
<section class="post wide">
<h2>Rak bedah paten</h2>
<p>Paten adalah dokumen teknologi yang terbuka: paten kedaluwarsa berarti teknologi yang bebas dipelajari dan dipakai sebagai titik awal, paten aktif berarti peta arah pemegangnya. Di rak ini paten klasik teknik kimia dibedah dengan standar yang sama: nomor, inventor, dan tanggal diverifikasi dari dokumen aslinya, klaimnya diparafrase, dan statusnya ditulis apa adanya. Saat ini ada {len(paten)} bedah paten.</p>
<p><a class="btn" href="/riset/paten/">Buka rak bedah paten</a></p>
</section>
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
<p class="lead">Setiap bedah di rak ini ditulis dari dokumen paten aslinya yang terbuka untuk umum: nomor, inventor, pemilik, dan tanggalnya diverifikasi, klaim intinya diparafrase dengan kata kami, cara kerjanya dijelaskan, batasnya dicatat, dan statusnya ditulis apa adanya. Paten yang sudah kedaluwarsa adalah dokumen publik: teknologinya bebas dipelajari siapa pun.</p>
<p class="meta">{len(paten)} bedah paten &middot; standar bedah: data hanya dari dokumen paten, klaim diparafrase, status bersumber dan bertanggal akses</p>
</article>
<section id="seri" class="series-bar">
  <h2>Jelajahi per topik</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{pchips}</div>
  <input id="search" type="search" placeholder="Cari paten, contoh: PSA, membran, MTG..." aria-label="Cari bedah paten">
</section>
<section id="artikel" class="grid">
{pcards}
</section>
<p id="no-result" hidden>Tidak ada bedah yang cocok. Coba kata kunci lain.</p>
<section class="post wide">
<h2>Rak bedah jurnal</h2>
<p>Bedah paper jurnal teknik kimia internasional dan Indonesia ada di halaman riset: masalah, metode, temuan persis dari abstrak, catatan kritis, dan kesimpulan baca.</p>
<p><a class="btn" href="/riset/">Buka rak bedah jurnal</a></p>
</section>
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
    ptop = ""
    for d in paten:
        pcov = resolve_img(d.get("cover_file"), d["slug"], "cover")
        ptop += (f'<article class="card"><a href="/riset/paten/{d["slug"]}/">'
                 + (f'<img src="{pcov}" alt="{esc(d["judul"])}" loading="lazy">' if pcov else '<div class="no-img">Bedah Paten</div>')
                 + f'</a><div class="card-body"><p class="eyebrow">Bedah paten &middot; {esc(d["nomor"])}</p>'
                 + f'<h3><a href="/riset/paten/{d["slug"]}/">{esc(d["judul"])}</a></h3>'
                 + f'<p class="meta">Terbit {esc(d["terbit"])}</p></div></article>\n')
    jindex = HEAD.format(title="Jalur Belajar Teknik Kimia | ilmutekkim",
                         desc="Urutan baca terkurasi ilmutekkim: membaca pabrik dari nol, distilasi inti, kilang dan petrokimia, sawit, utilitas, keselamatan proses, dan pabrik Indonesia.",
                         url=BASE + "/jalur/", ogtype="website", ogimg="")
    jindex += f"""
<article class="post wide">
<p class="eyebrow">Jalur belajar</p>
<h1>Belajar teknik kimia pakai urutan, bukan acak.</h1>
<p class="lead">Artikel yang bagus tetap membingungkan bila dibaca tanpa urutan. Di halaman ini bacaan ilmutekkim disusun menjadi {len(jalur)} jalur: setiap jalur adalah urutan langkah yang disengaja, dari yang harus dipahami dulu sampai yang baru masuk akal sesudahnya. Setiap langkah adalah artikel, video, atau bedah paten yang sudah ada di situs ini, dengan satu kalimat penjelas kenapa ia duduk di posisi itu.</p>
<p class="meta">{len(jalur)} jalur &middot; {sum(len(t["steps"]) for t in jalur)} langkah &middot; semua langkah resolve ke konten ilmutekkim</p>
</article>
<section class="post wide">
<p class="eyebrow">Ditaruh di atas, biar kelihatan</p>
<h2>Bedah paten yang jadi bagian jalur.</h2>
<p>Paten adalah dokumen teknologi terbuka, dan beberapa langkah di jalur bawah ini sengaja membaca dokumen paten aslinya: PSA Skarstrom, distilasi reaktif Eastman, dividing wall column BASF, membran Monsanto, dan MTG Mobil. Semuanya sudah kedaluwarsa, jadi bebas dipelajari siapa pun.</p>
</section>
<section class="grid">
{ptop}
</section>
<section class="post wide">
<h2>Tujuh jalur belajarnya</h2>
</section>
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
            steps_html += (f'<section class="factbox"><p class="eyebrow">Langkah {i} &middot; {label_tipe[st["type"]]}</p>'
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
            links += f'<a class="btn ghost" href="{u}">{esc(ttl)}</a> '
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
<p class="lead">Istilah di halaman ini adalah istilah yang benar-benar muncul di artikel, video, dan bedah ilmutekkim. Setiap definisi ditulis pendek dan tepat, tanpa karangan, lalu ditautkan ke bacaan yang memakainya agar istilah langsung terlihat dalam konteks prosesnya.</p>
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
<p id="no-result" hidden>Tidak ada istilah yang cocok. Coba kata kunci lain.</p>
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
<p class="lead">Semua sitasi yang muncul di situs ini dikumpulkan di satu halaman. Bagian pertama adalah buku, standar, dan literatur yang dikutip artikel dan video. Bagian berikutnya adalah paper dan paten yang dibedah di halaman riset. Tidak ada sitasi baru di halaman ini: isinya persis yang sudah dipakai tulisan-tulisan di situs ini.</p>
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
<h1>Hitung sendiri, jangan cuma percaya angka jadi.</h1>
<p class="lead">Empat kalkulator kecil untuk konsep yang berulang kali muncul di situs ini. Setiap kalkulator hanya memakai persamaan standar, menulis asumsinya terang-terangan, dan menautkan artikel yang menjelaskan konsepnya. Hasilnya adalah titik awal berpikir, bukan pengganti simulasi proses.</p>

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
    chips = ('<button class="chip" data-series="Video Interaktif">Video Interaktif</button>'
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
        vstrip += (f'<article class="card vcard{extra}" data-series="Video Interaktif"{extstyle} '
                   f'data-title="{esc(v["title"].lower())} {esc(v["tag"].lower())} video interaktif"><a href="/video/{v["slug"]}/">{thumb}'
                   f'<span class="play-badge">&#9654; {fmt_time(v["duration"])}</span></a><div class="card-body">'
                   f'<p class="eyebrow">{esc(v["tag"])}</p>'
                   f'<h3><a href="/video/{v["slug"]}/">{esc(v["title"])}</a></h3>'
                   f'<p>{esc(v["hook"])}</p>'
                   f'<p class="meta">{tgl_indo(v["date"])} &middot; tonton + baca artikelnya</p></div></article>\n')
    home += f"""
<section class="hero">
  <div class="meta-strip">
    <div><span>01</span>Artikel<b>{len(articles)} bedah proses</b></div>
    <div><span>02</span>Video<b>{len(videos)} video</b></div>
    <div><span>03</span>Seri<b>{len(series_list) + 1} seri topik</b></div>
    <div><span>04</span>Sumber<b>IG @ilmutekkim tersinkron</b></div>
  </div>
  <div class="hero-grid">
    <h1>Teknik kimia, dibedah dari pabriknya.</h1>
    <div class="hero-side">
      <p>Distilasi, kilang minyak, pabrik sawit, semen, pulp, sampai lapisan pengaman sebelum ledakan.
      Semua dibedah tahap demi tahap, pakai bahasa yang bisa diikuti tanpa buka textbook.</p>
      <a class="btn" href="#artikel">Baca {len(articles)} artikel</a>
      <a class="btn ghost" href="/video/">Tonton {len(videos)} video interaktif</a>
    </div>
  </div>
</section>
<section id="seri" class="series-bar">
  <h2>Jelajahi per seri</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{chips}</div>
  <input id="search" type="search" placeholder="Cari artikel, contoh: distilasi, semen, pompa..." aria-label="Cari artikel">
</section>
<section id="video" class="video-home">
  <div class="video-home-head"><h2>Video interaktif terbaru</h2><a href="/video/">Lihat semua video &rarr;</a></div>
  <p class="video-home-sub">Video teknik kimia 41 detik dari @ilmutekkim, masing-masing dengan versi artikel lengkap. Klik kartu untuk menonton sambil membaca penjelasannya.</p>
  <div class="grid video-grid">
{vstrip}
  </div>
</section>
<section id="artikel" class="grid">
{cards}
</section>
<p id="no-result" hidden>Tidak ada artikel yang cocok. Coba kata kunci lain.</p>
<section class="post wide">
<h2>Tidak tahu mulai dari mana?</h2>
<p>Tiga pintu masuk selain membaca acak: jalur belajar yang menyusun bacaan dalam urutan yang benar, glosarium istilah pabrik dengan bacaan lanjutannya, dan halaman referensi berisi semua sitasi yang dipakai situs ini.</p>
<p><a class="btn" href="/jalur/">Jalur belajar</a> <a class="btn ghost" href="/glosarium/">Glosarium</a> <a class="btn ghost" href="/referensi/">Referensi</a> <a class="btn ghost" href="/kalkulator/">Kalkulator</a></p>
</section>
""" + FOOT
    open(os.path.join(ROOT, "index.html"), "w").write(home)

    # tentang
    tentang = HEAD.format(title="Tentang ilmutekkim", desc="ilmutekkim adalah arsip baca konten "
                          "teknik kimia @ilmutekkim: pabrik, proses, safety, dan AI.",
                          url=BASE + "/tentang/", ogtype="website", ogimg="")
    tentang += """
<article class="post narrow">
<p class="eyebrow">Tentang</p>
<h1>Bikin teknik kimia asik.</h1>
<p class="lead">ilmutekkim adalah akun belajar teknik kimia dari sudut pandang orang pabrik:
bukan hafalan rumus, tapi bagaimana proses beneran jalan di lapangan.</p>
<p>Setiap artikel di situs ini adalah versi baca dari carousel Instagram
<a href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">@ilmutekkim</a>:
satu topik dibedah dari miskonsepsi yang paling sering beredar, kenyataan prosesnya,
diagram alurnya, sampai contoh nyata di industri Indonesia.</p>
<p>Setiap <a href="/video/">video interaktif</a> adalah versi tonton dari konten @ilmutekkim:
di sini kamu bisa menonton sambil membaca artikel lengkapnya, lompat ke detik tertentu
dari judul bagiannya, lalu mengecek paham lewat kuis singkat.</p>
<h2>Yang dibahas</h2>
<ul>
<li>Unit operasi: distilasi, heat exchanger, pompa, kompresor, cooling tower.</li>
<li>Alur pabrik Indonesia: kelapa sawit, kilang, petrokimia, pupuk, gula, semen, pulp dan kertas.</li>
<li>Keselamatan proses: relief valve, safety instrumented system, permit to work.</li>
<li>Dasar yang sering bocor: neraca massa, baca P&amp;ID, batch vs continuous.</li>
</ul>
<h2>Kenapa versi website</h2>
<p>Carousel enak buat disimpan, tapi susah dicari lagi. Di sini semua artikel bisa dicari,
dibaca utuh tanpa swipe, dan dibuka dari mesin pencari. Konten barunya tetap tayang
duluan di Instagram tiap hari.</p>
<div class="cta-box"><h2>Mulai dari mana</h2>
<p>Baru di sini? Mulai dari <a href="/artikel/distilasi-bertingkat-minyak-mentah/">distilasi bertingkat</a>,
lalu <a href="/artikel/baca-pid-lima-simbol-pabrik/">cara baca P&amp;ID dalam 5 menit</a>.</p>
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
