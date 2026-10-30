#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator Kamus Industri Kimia IlmuTekkim (mandiri, tanpa dependensi).

Sumber: kamus-data/terms.json, kamus-data/sectors.json, dan glosarium.json
Keluaran:
  kamus/index.html                     beranda pencarian + daftar lengkap A-Z
  kamus/sektor/<slug>/index.html       halaman sektor + diagram alur
  kamus/istilah/<slug>/index.html      halaman istilah dalam 3 lapis dan entri dasar
  kamus/search-index.json              indeks pencarian + data chatbot

Gate kedalaman (depth gate): build GAGAL apabila satu entri pun tidak
memuat mekanisme, prinsip + persamaan, variabel bersensitivitas, dan
kegagalan/batas operasi, lengkap dengan lapis plant dan referensi.
Jalankan: python3 tools/build_kamus.py
"""
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "kamus-data")
OUT = os.path.join(ROOT, "kamus")
BASE = "https://ilmutekkim.site"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800'
         '&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">')


def esc(s):
    return html.escape(str(s), quote=True)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def norm_key(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", norm_key(value)).strip("-")


def load_glosarium():
    with open(os.path.join(ROOT, "glosarium.json"), encoding="utf-8") as f:
        return json.load(f)


def target_title(relative_path, fallback_slug):
    path = os.path.join(ROOT, relative_path)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            match = re.search(r"<title>(.*?)</title>", f.read(), flags=re.I | re.S)
        if match:
            title = re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()
            for suffix in (" | ilmutekkim", " — ilmutekkim", " - ilmutekkim"):
                if title.lower().endswith(suffix.lower()):
                    title = title[:-len(suffix)].strip()
            if title:
                return title
    return fallback_slug.replace("-", " ").title()


def basic_terms(deep_terms):
    """Gabungkan glosarium lama sebagai entri dasar, kecuali yang sudah dibedah dalam."""
    deep_keys = set()
    for term in deep_terms:
        for value in [term.get("term", ""), term.get("slug", "")] + term.get("aliases", []):
            deep_keys.add(norm_key(value))
            deep_keys.add(slugify(value))

    type_map = {
        "artikel": ("artikel", "Artikel"),
        "video": ("video", "Video"),
        "paten": (os.path.join("riset", "paten"), "Bedah paten"),
    }
    merged = []
    for entry in load_glosarium():
        term = entry["term"]
        slug = slugify(term)
        if norm_key(term) in deep_keys or slug in deep_keys:
            continue
        links = []
        for related in entry.get("terkait", []):
            folder, label = type_map.get(related.get("type"), type_map["artikel"])
            rel_slug = related["slug"]
            relative_page = os.path.join(folder, rel_slug, "index.html")
            links.append({
                "type": related.get("type", "artikel"),
                "label": target_title(relative_page, rel_slug),
                "type_label": label,
                "url": "/" + relative_page.replace(os.sep, "/").replace("index.html", ""),
            })
        merged.append({
            "slug": slug,
            "term": term,
            "definisi": entry["definisi"],
            "terkait": links,
            "kind": "dasar",
        })
    return sorted(merged, key=lambda x: x["term"].lower())


def depth_gate(terms):
    """Kembalikan daftar pelanggaran gate kedalaman."""
    errs = []
    for t in terms:
        s = t.get("slug", "?")
        if not t.get("definisi") or not t.get("analogi"):
            errs.append(f"{s}: lapis 0 (definisi/analogi) tidak lengkap")
        if not t.get("mekanisme"):
            errs.append(f"{s}: gate 1 gagal - mekanisme kosong")
        if not t.get("prinsip") or not t.get("persamaan"):
            errs.append(f"{s}: gate 2 gagal - prinsip/persamaan kosong")
        for p in t.get("persamaan", []):
            if not p.get("rumus") or not p.get("simbol") or not p.get("asumsi"):
                errs.append(f"{s}: gate 2 gagal - persamaan tanpa simbol/asumsi")
        if not t.get("variabel"):
            errs.append(f"{s}: gate 3 gagal - variabel kosong")
        for v in t.get("variabel", []):
            if not v.get("rentang") or "textbook" not in v["rentang"]:
                errs.append(f"{s}: gate 3 gagal - rentang variabel tanpa label textbook")
            if v.get("arah") not in ("naik", "turun") or not v.get("efek"):
                errs.append(f"{s}: gate 3 gagal - variabel tanpa arah sensitivitas/efek")
        if not t.get("kegagalan"):
            errs.append(f"{s}: gate 4 gagal - kegagalan/batas operasi kosong")
        pl = t.get("plant", {})
        if not pl.get("biaya") or not pl.get("checklist") or not pl.get("contoh"):
            errs.append(f"{s}: lapis plant tidak lengkap (biaya/checklist/contoh)")
        if not t.get("terkait") or not t.get("referensi"):
            errs.append(f"{s}: terkait/referensi kosong")
    return errs


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}">
<script>(function(){{try{{var t=localStorage.getItem("ilm-theme");if(!t){{t=window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}}document.documentElement.setAttribute("data-theme",t);}}catch(e){{document.documentElement.setAttribute("data-theme","light");}}}})();</script>
{FONTS}
<link rel="stylesheet" href="/assets/css/style.css?v=24">
<link rel="stylesheet" href="/kamus/assets/kamus.css">
<link rel="stylesheet" href="/kamus/assets/chat.css?v=2">
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<header class="site-header">
  <a class="brand" href="/">ilmu<span>tekkim</span></a>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
  <label for="nav-toggle" class="burger" aria-label="Buka menu">&#9776;</label>
  <nav>
    <a href="/">Articles &amp; Videos</a>
    <a href="/riset/">Riset</a>
    <a href="/jalur/">Jalur</a>
    <a href="/kamus">Kamus</a>
  </nav>
  <button type="button" class="theme-toggle" id="themeToggle" aria-label="Beralih antara mode terang dan mode gelap" title="Mode terang / gelap"><span class="ic-sun" aria-hidden="true">&#9728;</span><span class="ic-moon" aria-hidden="true">&#9790;</span></button>
</header>
"""


FOOT = """
<div class="foot"><nav><a href="/kamus">Kamus</a> · <a href="/artikel/">Artikel</a> · <a href="/video/">Video</a> · <a href="/riset/">Riset</a> · <a href="/jalur/">Jalur Belajar</a></nav>
<p>Kamus Industri Kimia — bagian dari <a href="/">ilmutekkim.site</a>.
Seluruh angka operasi pada kamus ini adalah rentang umum textbook, bukan data plant atau data perusahaan mana pun.</p></div>
</div>
<script src="/assets/js/main.js?v=11"></script>
<script src="/kamus/assets/chat.js" defer></script>
</body>
</html>
"""

SEG_JS = """
<script>
document.querySelectorAll('.seg button').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.seg button').forEach(function(x){x.classList.toggle('on',x===b);});
    var lv=b.getAttribute('data-lv');
    document.querySelectorAll('[data-layer]').forEach(function(el){
      var l=el.getAttribute('data-layer');
      el.style.display = (lv==='semua' || l===lv) ? '' : 'none';
    });
  });
});
var def=document.querySelector('.seg button[data-lv="tekkim"]');
if(def){def.click();}
</script>
"""


def term_card(t, fondasi_nama):
    return (f'<a class="sresult" href="/kamus/istilah/{t["slug"]}/">'
            f'<span class="t">{esc(t["term"])}</span>'
            f'<div class="snip">{esc(fondasi_nama.get(t["fondasi"], ""))} — '
            f'{esc(t["definisi"][:130])}…</div></a>')


def build_index(terms, sectors, fondasi, sector_terms, dasar):
    fondasi_nama = {f["slug"]: f["nama"] for f in fondasi}
    counts = {}
    for t in terms:
        counts[t["fondasi"]] = counts.get(t["fondasi"], 0) + 1
    sec_cards = ""
    for s in sectors:
        n = len(sector_terms.get(s["slug"], []))
        sec_cards += (f'<div class="card"><h3><a href="/kamus/sektor/{s["slug"]}/">{esc(s["nama"])}</a></h3>'
                      f'<p>{esc(s["tagline"])}</p><span class="count">{n} istilah terkait</span></div>')
    chips = "".join(
        f'<a class="chip" href="#fondasi-{f["slug"]}">{esc(f["nama"])} <b>{counts.get(f["slug"], 0)}</b></a>'
        for f in fondasi)
    populer = "".join(term_card(t, fondasi_nama) for t in terms if t.get("populer"))
    all_items = [(t["term"].lower(), term_card(t, fondasi_nama)) for t in terms]
    for b in dasar:
        all_items.append((b["term"].lower(),
                          f'<a class="sresult" href="/kamus/istilah/{b["slug"]}/">'
                          f'<span class="t">{esc(b["term"])}</span> <span class="count">Entri dasar</span>'
                          f'<div class="snip">{esc(b["definisi"][:150])}…</div></a>'))
    all_cards = "".join(card for _, card in sorted(all_items, key=lambda x: x[0]))
    fondasi_sections = ""
    for f in fondasi:
        items = [t for t in terms if t["fondasi"] == f["slug"]]
        if not items:
            continue
        fondasi_sections += (f'<section class="blk" id="fondasi-{f["slug"]}"><h2>{esc(f["nama"])}</h2>'
                             + "".join(term_card(t, fondasi_nama) for t in items) + "</section>")
    body = f"""
<div class="wrap">
<div class="hero">
<h1>Kamus Industri Kimia</h1>
<p class="sub">Kamus proses teknik kimia untuk seluruh industri kimia Indonesia: istilah, mekanisme,
persamaan kunci, variabel operasi, dan bedah plant — disusun per sektor industri dan per fondasi keilmuan,
dengan kedalaman teknik kimia sebagai standar entri utamanya.</p>
<p class="lead">{len(terms) + len(dasar)} istilah tersedia: {len(terms)} entri dalam dan {len(dasar)} entri dasar.</p>
<form class="searchbox" id="search-form" role="search">
<input id="kamus-search" type="search" autocomplete="off"
 placeholder="Cari istilah: reflux, FFA, steam cracking, kavitasi…  (tekan / untuk fokus)">
<button type="submit">Cari</button>
</form>
<div id="search-results" aria-live="polite"></div>
</div>
<section class="blk"><h2>Sektor Industri</h2>
<p class="lead">Setiap sektor menyajikan alur proses ujung ke ujung; setiap simpul alur tertaut ke entri istilahnya.</p>
<div class="grid">{sec_cards}</div></section>
<section class="blk"><h2>Fondasi Teknik Kimia</h2>
<p class="lead">Istilah fondasi berlaku lintas sektor dan menjadi rumah kanonis setiap konsep.</p>
<div class="chips">{chips}</div></section>
<section class="blk"><h2>Istilah Populer</h2>{populer}</section>
<section class="blk" id="semua-istilah"><h2>Semua Istilah A–Z ({len(terms) + len(dasar)})</h2>
<p class="lead">Daftar lengkap kamus gabungan. Entri dalam memuat mekanisme, persamaan, sensitivitas, dan bedah plant; entri dasar memuat definisi serta bacaan terkait dan akan diperdalam secara bertahap.</p>{all_cards}</section>
{fondasi_sections}
"""
    return head("Kamus Industri Kimia — IlmuTekkim",
                "Kamus proses teknik kimia per sektor industri: definisi, mekanisme, persamaan, variabel operasi, dan bedah plant.") + body + FOOT + \
        '<script src="/kamus/assets/search.js" defer></script>'


def build_sector(s, terms_by_slug, sector_term_slugs, fondasi_nama):
    nodes = []
    for i, n in enumerate(s["flow"]):
        label = esc(n["label"])
        if n.get("slug") and n["slug"] in terms_by_slug:
            nodes.append(f'<a class="fnode" href="/kamus/istilah/{n["slug"]}/">{label}</a>')
        else:
            nodes.append(f'<span class="fnode">{label}</span>')
        if i < len(s["flow"]) - 1:
            nodes.append('<span class="farrow">→</span>')
    items = "".join(term_card(terms_by_slug[sl], fondasi_nama) for sl in sector_term_slugs)
    body = f"""
<div class="wrap">
<div class="crumbs"><a href="/kamus/">Kamus</a> › Sektor › {esc(s['nama'])}</div>
<div class="termhead"><h1>Sektor {esc(s['nama'])}</h1></div>
<p>{esc(s['deskripsi'])}</p>
<section class="blk"><h2>Alur Proses</h2>
<p class="lead">{esc(s['aliran'])} Simpul berwarna cyan dapat diklik menuju entri istilahnya.</p>
<div class="flow">{''.join(nodes)}</div></section>
<section class="blk"><h2>Bahan Baku dan Produk</h2>
<div class="card"><p><strong>Bahan baku:</strong> {esc(s['bahan'])}</p>
<p style="margin-top:8px"><strong>Produk:</strong> {esc(s['produk'])}</p></div></section>
<section class="blk"><h2>Istilah pada Sektor Ini ({len(sector_term_slugs)})</h2>{items}</section>
"""
    return head(f"Sektor {s['nama']} — Kamus Industri Kimia IlmuTekkim",
                s["tagline"]) + body + FOOT


def build_basic_term(b):
    links = "".join(
        f'<a class="sresult" href="{esc(link["url"])}"><span class="t">{esc(link["label"])}</span>'
        f'<div class="snip">{esc(link["type_label"])} terkait dengan istilah ini</div></a>'
        for link in b["terkait"])
    if not links:
        links = '<p class="lead">Belum ada bacaan terkait yang terhubung ke entri ini.</p>'
    body = f"""
<div class="wrap">
<div class="crumbs"><a href="/kamus/">Kamus</a> › Entri Dasar › {esc(b['term'])}</div>
<div class="termhead"><h1>{esc(b['term'])}</h1>
<div class="badges"><span class="badge ver">Entri glosarium</span>
<span class="badge fon">Entri dasar</span></div></div>

<div class="l0"><h2>Definisi</h2><p>{esc(b['definisi'])}</p></div>

<section class="layer"><h2>Status Kedalaman</h2>
<p><strong>Entri dasar — bedah dalam (mekanisme, persamaan, sensitivitas) menyusul.</strong></p>
<p>Entri ini dipertahankan sebagai definisi awal dalam kamus gabungan agar istilah dan bacaan terkaitnya tetap dapat ditemukan. Statusnya tidak disamakan dengan entri dalam yang telah melalui gate kedalaman Kamus Industri Kimia.</p></section>

<section class="blk"><h2>Bacaan Terkait</h2>{links}</section>
<section class="blk"><p><a class="chip" href="/kamus/#semua-istilah">Lihat semua istilah A–Z</a></p></section>
"""
    return head(f"{b['term']} — Kamus Industri Kimia IlmuTekkim", b["definisi"][:155]) + body + FOOT


def build_term(t, terms_by_slug, sectors_by_slug, fondasi_nama):
    eqs = ""
    for p in t["persamaan"]:
        eqs += (f'<div class="eq"><div class="rumus">{p["rumus"]}</div>'
                f'<div class="simbol">{esc(p["simbol"])}</div>'
                f'<div class="asumsi">Asumsi: {esc(p["asumsi"])}</div></div>')
    rows = ""
    for v in t["variabel"]:
        arrow = '<span class="up">↑ naik</span>' if v["arah"] == "naik" else '<span class="down">↓ turun</span>'
        rows += (f'<tr><td><strong>{esc(v["nama"])}</strong></td><td>{esc(v["rentang"])}</td>'
                 f'<td>{arrow}</td><td>{esc(v["efek"])}</td></tr>')
    gagal = "".join(f"<li>{esc(g)}</li>" for g in t["kegagalan"])
    biaya = "".join(f"<li>{esc(b)}</li>" for b in t["plant"]["biaya"])
    cek = ""
    for c in t["plant"]["checklist"]:
        cek += (f'<tr><td>{esc(c["gejala"])}</td><td>{esc(c["penyebab"])}</td><td>{esc(c["tindakan"])}</td></tr>')
    terkait = "".join(
        f'<a class="chip" href="/kamus/istilah/{r}/">{esc(terms_by_slug[r]["term"])}</a>'
        for r in t["terkait"])
    refs = "".join(f"<li>{esc(r)}</li>" for r in t["referensi"])
    sec_badges = "".join(
        f'<a class="badge sec" href="/kamus/sektor/{s}/">{esc(sectors_by_slug[s]["nama"])}</a>'
        for s in t["sectors"])
    body = f"""
<div class="wrap">
<div class="crumbs"><a href="/kamus/">Kamus</a> › {esc(fondasi_nama.get(t['fondasi'], ''))} › {esc(t['term'])}</div>
<div class="termhead"><h1>{esc(t['term'])}</h1>
<div class="badges"><span class="badge ver">Glosarium terverifikasi</span>
<span class="badge fon">{esc(fondasi_nama.get(t['fondasi'], ''))}</span>{sec_badges}</div></div>

<div class="l0"><h2>Definisi</h2><p>{esc(t['definisi'])}</p>
<div class="analogi"><strong>Analogi:</strong> {esc(t['analogi'])}</div></div>

<div class="seg" role="tablist" aria-label="Level kedalaman">
<button type="button" data-lv="awam">Awam</button>
<button type="button" data-lv="tekkim" class="on">Tekkim</button>
<button type="button" data-lv="plant">Plant</button>
<button type="button" data-lv="semua">Semua</button>
</div>
<p class="note">Pilih level kedalaman: Awam menampilkan lapis inti konsep pada kedalaman pengantar,
Tekkim menampilkan lapis mekanisme dan persamaan, Plant menampilkan lapis penerapan di pabrik.
Definisi selalu ditampilkan pada setiap level.</p>

<section class="layer" data-layer="tekkim"><h2>Lapis Tekkim — Mekanisme dan Prinsip</h2>
<h3>Mekanisme</h3><p>{esc(t['mekanisme'])}</p>
<h3>Prinsip dan Persamaan Kunci</h3><p>{esc(t['prinsip'])}</p>{eqs}
<h3>Variabel Operasi dan Sensitivitas</h3>
<p class="note">Seluruh rentang adalah rentang umum textbook, bukan data plant.</p>
<table class="sens"><thead><tr><th>Variabel</th><th>Rentang Umum</th><th>Arah Perubahan</th><th>Efek dan Alasannya</th></tr></thead>
<tbody>{rows}</tbody></table>
<h3>Batas Operasi dan Mode Kegagalan</h3><ul class="tight">{gagal}</ul></section>

<section class="layer" data-layer="plant"><h2>Lapis Plant — Biaya, Diagnosis, dan Contoh</h2>
<h3>Pendorong Biaya dan Efisiensi</h3><ul class="tight">{biaya}</ul>
<h3>Daftar Periksa Diagnosis Sebab-Akibat</h3>
<table class="sens check"><thead><tr><th>Gejala</th><th>Penyebab yang Mungkin</th><th>Tindakan Pemeriksaan</th></tr></thead>
<tbody>{cek}</tbody></table>
<div class="contoh"><strong>Contoh hitungan (angka textbook):</strong> {esc(t['plant']['contoh'])}</div>
</section>

<section class="layer" data-layer="awam"><h2>Mulai dari Sini</h2>
<p>Untuk pembaca yang baru pertama kali menemui istilah ini, definisi dan analogi pada bagian atas
halaman adalah ringkasan yang memadai. Lapis Tekkim menambahkan mekanisme, persamaan, dan variabel
yang menentukan perilaku konsep ini, sedangkan Lapis Plant menunjukkan penerapannya pada operasi pabrik.</p></section>

<section class="blk"><h2>Istilah Terkait</h2><div class="chips">{terkait}</div></section>
<section class="blk refs"><h2>Referensi</h2><ul class="tight">{refs}</ul>
<p>Terakhir diperbarui: {esc(t['updated'])} · Sumber entri: Glosarium terverifikasi IlmuTekkim.
Seluruh angka adalah rentang umum textbook, bukan data plant.</p></section>
"""
    return head(f"{t['term']} — Kamus Industri Kimia IlmuTekkim",
                t["definisi"][:155]) + body + FOOT + SEG_JS


def main():
    terms = load("terms.json")
    meta = load("sectors.json")
    sectors, fondasi = meta["sectors"], meta["fondasi"]
    sector_terms = meta["sector_terms"]
    errs = depth_gate(terms)
    slugs = [t["slug"] for t in terms]
    if len(set(slugs)) != len(slugs):
        errs.append("slug ganda ditemukan")
    known = set(slugs)
    for t in terms:
        for r in t["terkait"]:
            if r not in known:
                errs.append(f"{t['slug']}: terkait tidak dikenal: {r}")
    if errs:
        print("BUILD GAGAL — gate kedalaman:")
        for e in errs:
            print(" -", e)
        return 1
    dasar = basic_terms(terms)
    dasar_slugs = [b["slug"] for b in dasar]
    if len(set(dasar_slugs)) != len(dasar_slugs) or known.intersection(dasar_slugs):
        print("BUILD GAGAL — slug entri dasar ganda atau bertabrakan dengan entri dalam.")
        return 1
    terms_by_slug = {t["slug"]: t for t in terms}
    sectors_by_slug = {s["slug"]: s for s in sectors}
    fondasi_nama = {f["slug"]: f["nama"] for f in fondasi}

    def write(rel, content):
        p = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", rel)

    write("index.html", build_index(terms, sectors, fondasi, sector_terms, dasar))
    for s in sectors:
        write(os.path.join("sektor", s["slug"], "index.html"),
              build_sector(s, terms_by_slug, sector_terms.get(s["slug"], []), fondasi_nama))
    for t in terms:
        write(os.path.join("istilah", t["slug"], "index.html"),
              build_term(t, terms_by_slug, sectors_by_slug, fondasi_nama))
    for b in dasar:
        write(os.path.join("istilah", b["slug"], "index.html"), build_basic_term(b))

    index_terms = []
    for t in terms:
        search_text = " ".join([
            t["definisi"], t["mekanisme"], t["prinsip"], t["analogi"],
            " ".join(v["nama"] + " " + v["efek"] for v in t["variabel"]),
            " ".join(t["kegagalan"]),
        ])
        index_terms.append({
            "slug": t["slug"], "term": t["term"], "aliases": t.get("aliases", []),
            "fondasi": t["fondasi"], "sectors": t["sectors"],
            "definisi": t["definisi"], "analogi": t["analogi"],
            "mekanisme": t["mekanisme"], "prinsip": t["prinsip"],
            "plant": t["plant"], "search_text": search_text, "kind": "dalam",
        })
    for b in dasar:
        search_text = " ".join([
            b["term"], b["definisi"],
            " ".join(link["label"] for link in b["terkait"]),
        ])
        index_terms.append({
            "slug": b["slug"], "term": b["term"], "aliases": [],
            "fondasi": "entri-dasar", "sectors": [],
            "definisi": b["definisi"], "analogi": "",
            "mekanisme": "", "prinsip": "",
            "plant": {"biaya": [], "checklist": [], "contoh": ""},
            "search_text": search_text, "kind": "dasar",
            "terkait": b["terkait"],
        })
    idx = {"terms": index_terms,
           "sectors": [{"slug": s["slug"], "nama": s["nama"], "tagline": s["tagline"]} for s in sectors]}
    with open(os.path.join(OUT, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    print("wrote search-index.json")
    print(f"OK: {len(terms)} entri dalam, {len(dasar)} entri dasar, {len(sectors)} sektor, "
          "gate kedalaman lolos untuk semua entri dalam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
