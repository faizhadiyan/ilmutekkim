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
     "2026-09-30", "https://www.instagram.com/p/Dd5outoD9Ou/", "tayang"),
    ("reflux-optimum-kolom-distilasi", "draft/spec-real.json",
     "Makin Besar Reflux, Makin Murni? Bedah Reflux Optimum Kolom Distilasi",
     "2026-09-30", "https://www.instagram.com/p/Dd8ALotlHDT/", "tayang"),
    ("pabrik-kelapa-sawit-tandan-ke-cpo", "specs/2026-09-30-carousel-2-rev5.json",
     "Dari Tandan Berduri Jadi Minyak Sawit: Alur Lengkap Pabrik Kelapa Sawit",
     "2026-09-30", None, "tayang"),
    ("baca-pid-lima-simbol-pabrik", "specs/2026-09-30-carousel-3.json",
     "Baca P&ID dalam 5 Menit: Lima Simbol yang Muncul di Hampir Semua Pabrik",
     "2026-09-30", "https://www.instagram.com/p/Dd5T1nhD8Xn/", "tayang"),
    ("refinery-sawit-cpo-ke-minyak-goreng", "specs/2026-10-01-carousel-1.json",
     "Dari CPO Jadi Minyak Goreng: Empat Tahap Refinery Sawit (Olein vs Stearin)",
     "2026-10-01", None, "tayang"),
    ("heat-exchanger-bikin-shutdown", "specs/2026-10-01-carousel-2.json",
     "Heat Exchanger: Alat Paling Sederhana yang Paling Sering Bikin Pabrik Shutdown",
     "2026-10-01", None, "tayang"),
    ("b40-biodiesel-sawit-transesterifikasi", "specs/2026-10-01-carousel-3-rev2.json",
     "B40: Bagaimana Sawit Jadi Biodiesel Lewat Transesterifikasi",
     "2026-10-02", "https://www.instagram.com/p/Dd_bheiDuVX/", "tayang"),
    ("bbm-dari-sampah-plastik-pirolisis", "specs/2026-10-01-bbm-plastik.json",
     "Dari Sampah Plastik Jadi BBM: Bedah Proses Pirolisis",
     "2026-10-01", None, "arsip"),
    ("tekanan-relief-valve-rupture-disk", "specs/2026-10-02-carousel-1.json",
     "Tekanan Itu Nyawa di Pabrik Kimia: Cara Kerja Relief Valve dan Rupture Disk",
     "2026-10-02", None, "tayang"),
    ("satu-barel-minyak-jadi-apa", "specs/2026-10-02-carousel-2-rev.json",
     "Satu Barel Minyak Jadi Apa Saja? Bedah Produk Kilang Cilacap dan Balikpapan",
     "2026-10-02", None, "tayang"),
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
     "2026-10-03", "https://www.instagram.com/p/DeCVD9HjtAt/", "tayang"),
    ("polimerisasi-konversi-carothers", "specs/2026-10-03-advanced-polimerisasi.json",
     "Konversi 99 Persen Masih Kurang: Polimerisasi Step-Growth dan Persamaan Carothers",
     "2026-10-03", None, "arsip"),
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
     "2026-10-05", None, "tayang"),
    ("utilitas-pabrik-steam-air-nitrogen", "specs/2026-10-05-carousel-2.json",
     "Utilitas Pabrik: Pabrik di Dalam Pabrik yang Tidak Terlihat (Steam, Air, Nitrogen)",
     "2026-10-05", "https://www.instagram.com/p/DeG-z3Hj3Ul/", "tayang"),
    ("batu-kapur-ke-semen-kiln", "specs/2026-10-05-carousel-3.json",
     "Batu Kapur Jadi Semen Lewat Api 1450 Derajat: Proses Kiln dari Tambang ke Kantong",
     "2026-10-05", None, "tayang"),
    ("safety-instrumented-system-lapisan-pengaman", "specs/2026-10-06-carousel-1.json",
     "Pabrik Aman Bukan Karena Operator Sigap: Cara Kerja Safety Instrumented System",
     "2026-10-06", None, "tayang"),
    ("pulp-kertas-proses-kraft", "specs/2026-10-06-carousel-2-rev.json",
     "Kayu Keras Jadi Kertas Lembut: Proses Kraft di Pabrik Pulp Riau",
     "2026-10-06", "https://www.instagram.com/p/DeJjGqwj0Hb/", "tayang"),
    ("permit-to-work-kerja-panas", "specs/2026-10-06-carousel-3.json",
     "Las Lima Menit Tetap Butuh Izin: Cara Kerja Permit to Work di Pabrik Kimia",
     "2026-10-06", None, "arsip"),
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
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Noto+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230B1B3F'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%2300B4D8' font-family='Arial' font-weight='bold'>IT</text></svg>">
</head>
<body>
<header class="site-header">
  <a class="brand" href="/">ilmu<span>tekkim</span></a>
  <nav>
    <a href="/#artikel">Artikel</a>
    <a href="/#seri">Seri</a>
    <a href="/tentang/">Tentang</a>
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
  <p><a href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">@ilmutekkim di Instagram</a> &middot; <a href="/tentang/">Tentang</a></p>
  <p class="fine">Seluruh artikel di situs ini adalah versi baca dari carousel Instagram @ilmutekkim. Foto berasal dari Pexels dan Unsplash, kredit tercantum di tiap gambar.</p>
</footer>
<script src="/assets/js/main.js"></script>
</body>
</html>
"""


def main():
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
        articles.append(dict(slug=slug, title=title, date=date, ig=ig, status=status,
                             series=series, cover=cover, lead=lead, body=body, refs=refs,
                             sub=clean_text(d.get("cover_sub") or ""),
                             credit=clean_text(d.get("cover_credit") or ""),
                             credit_url=d.get("credit_url") or d.get("cover_credit_url") or "",
                             teaser=clean_text(d.get("cta_teaser") or "")))
    articles.sort(key=lambda a: a["date"], reverse=True)

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
        if a["sub"]:
            page += f'<p class="lead">{esc(a["sub"])}</p>\n'
        for p in a["lead"][:2]:
            if p != a["lead"][0] or True:
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

    # beranda
    series_list = sorted(set(a["series"] for a in articles))
    chips = "".join(f'<button class="chip" data-series="{esc(s)}">{esc(s)}</button>'
                    for s in series_list)
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
    home += f"""
<section class="hero">
  <p class="eyebrow light">Seputar Dunia Proses Teknik Kimia</p>
  <h1>Teknik kimia, dibedah dari pabriknya.</h1>
  <p>Distilasi, kilang minyak, pabrik sawit, semen, pulp, sampai lapisan pengaman sebelum ledakan.
  Semua dibedah tahap demi tahap, pakai bahasa yang bisa diikuti tanpa buka textbook.</p>
  <a class="btn" href="#artikel">Baca {len(articles)} artikel</a>
  <a class="btn ghost" href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">Follow di Instagram</a>
</section>
<section id="seri" class="series-bar">
  <h2>Jelajahi per seri</h2>
  <div class="chips"><button class="chip active" data-series="all">Semua</button>{chips}</div>
  <input id="search" type="search" placeholder="Cari artikel, contoh: distilasi, semen, pompa..." aria-label="Cari artikel">
</section>
<section id="artikel" class="grid">
{cards}
</section>
<p id="no-result" hidden>Tidak ada artikel yang cocok. Coba kata kunci lain.</p>
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
    urls = [BASE + "/", BASE + "/tentang/"] + [f"{BASE}/artikel/{a['slug']}/" for a in articles]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"OK: {len(articles)} artikel, {len(series_list)} seri")


if __name__ == "__main__":
    main()
