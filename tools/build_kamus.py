#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator Kamus Industri Kimia IlmuTekkim (mandiri, tanpa dependensi).

Sumber: kamus-data/terms.json dan kamus-data/sectors.json
Keluaran:
  kamus/index.html                     beranda pencarian
  kamus/sektor/<slug>/index.html       halaman sektor + diagram alur
  kamus/istilah/<slug>/index.html      halaman istilah 3 lapis
  kamus/search-index.json              indeks pencarian + data chatbot

Gate kedalaman (depth gate): build GAGAL apabila satu entri pun tidak
memuat mekanisme, prinsip + persamaan, variabel bersensitivitas, dan
kegagalan/batas operasi, lengkap dengan lapis plant dan referensi.
Jalankan: python3 tools/build_kamus.py
"""
import html
import json
import os
import sys

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
{FONTS}
<link rel="stylesheet" href="/kamus/assets/kamus.css">
<link rel="stylesheet" href="/kamus/assets/chat.css">
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<header class="khead"><div class="wrap">
<a class="brand" href="/kamus/">ilmu<span>tekkim</span> · Kamus</a>
<nav>
<a href="/kamus/">Kamus</a><a href="/">Beranda Situs</a><a href="/artikel/">Artikel</a>
<a href="/video/">Video</a><a href="/glosarium/">Glosarium</a><a href="/jalur/">Jalur Belajar</a>
</nav></div></header>
"""


FOOT = """
<div class="foot">Kamus Industri Kimia — bagian dari <a href="/">ilmutekkim.site</a>.
Seluruh angka operasi pada kamus ini adalah rentang umum textbook, bukan data plant atau data perusahaan mana pun.</div>
</div>
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


def build_index(terms, sectors, fondasi, sector_terms):
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
    terbaru = "".join(term_card(t, fondasi_nama)
                      for t in sorted(terms, key=lambda x: x["slug"])[:6])
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
dengan kedalaman teknik kimia sebagai standar setiap entri.</p>
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
<section class="blk"><h2>Jelajahi Kamus</h2>{terbaru}</section>
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
    terms_by_slug = {t["slug"]: t for t in terms}
    sectors_by_slug = {s["slug"]: s for s in sectors}
    fondasi_nama = {f["slug"]: f["nama"] for f in fondasi}

    def write(rel, content):
        p = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", rel)

    write("index.html", build_index(terms, sectors, fondasi, sector_terms))
    for s in sectors:
        write(os.path.join("sektor", s["slug"], "index.html"),
              build_sector(s, terms_by_slug, sector_terms.get(s["slug"], []), fondasi_nama))
    for t in terms:
        write(os.path.join("istilah", t["slug"], "index.html"),
              build_term(t, terms_by_slug, sectors_by_slug, fondasi_nama))

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
            "plant": t["plant"], "search_text": search_text,
        })
    idx = {"terms": index_terms,
           "sectors": [{"slug": s["slug"], "nama": s["nama"], "tagline": s["tagline"]} for s in sectors]}
    with open(os.path.join(OUT, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    print("wrote search-index.json")
    print(f"OK: {len(terms)} entri, {len(sectors)} sektor, gate kedalaman lolos untuk semua entri.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
