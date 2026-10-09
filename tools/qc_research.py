#!/usr/bin/env python3
"""Gate QC bedah riset ilmutekkim (ILM-R65).

Setiap bedah di research/*.json WAJIB lolos semua pemeriksaan sebelum build:
1. Field wajib lengkap; cakupan harus "Berdasarkan abstrak"; DOI format resolver.
2. Setiap angka di badan bedah harus persis ada di abstrak sumber (abstract_src),
   setelah normalisasi koma desimal dan subscript kimia (CO2, TiO2, dsb).
3. Parafrase: tumpang tindih 8-kata berurutan dengan abstrak maksimal 2 shingle.
4. Panjang bedah 300-800 kata; kesimpulan akhir valid; slug terkait harus ada di situs.
5. Dilarang em dash dan double hyphen di badan bedah.
Exit 0 = semua lolos. Exit 1 = build tidak boleh jalan.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RDIR = os.path.join(ROOT, "research")
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
PROSE_FIELDS = ("lead", "masalah", "metode", "arti_pabrik", "vonis_alasan")
LIST_FIELDS = ("temuan", "batas")
REQUIRED = ("slug", "judul", "topik", "negara", "paper_title", "authors", "year",
            "journal", "doi", "coverage", "date_bedah", "lead", "masalah", "metode",
            "temuan", "batas", "arti_pabrik", "vonis", "vonis_alasan", "abstract_src")


def norm_text(t):
    return str(t).translate(SUB)


def numbers(t):
    t = norm_text(t).replace(",", ".")
    return set(re.findall(r"\d+(?:\.\d+)?", t))


def words(t):
    return re.findall(r"[a-z0-9]+", norm_text(t).lower())


def shingles(t, n=8):
    w = words(t)
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def prose_of(d):
    parts = [str(d.get(f, "")) for f in PROSE_FIELDS]
    for f in LIST_FIELDS:
        parts += [str(x) for x in d.get(f, [])]
    return "\n".join(parts)


def check_file(fp):
    errs, warns = [], []
    try:
        d = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        return [f"JSON tidak valid: {e}"], warns
    slug = d.get("slug") or os.path.basename(fp)
    for f in REQUIRED:
        if not d.get(f):
            errs.append(f"field wajib kosong: {f}")
    if d.get("coverage") != "Berdasarkan abstrak":
        errs.append("coverage harus 'Berdasarkan abstrak'")
    doi = str(d.get("doi") or "")
    if not re.match(r"^https://doi\.org/10\.\S+$", doi):
        errs.append(f"DOI tidak valid: {doi}")
    if d.get("vonis") not in ("Baca full paper-nya", "Cukup baca abstraknya"):
        errs.append(f"vonis tidak valid: {d.get('vonis')}")
    if d.get("negara") not in ("Internasional", "Indonesia"):
        errs.append(f"negara tidak valid: {d.get('negara')}")
    prose = prose_of(d)
    abstract = str(d.get("abstract_src") or "")
    # gate angka: semua angka bedah harus ada di abstrak
    extra = numbers(prose) - numbers(abstract)
    if extra:
        errs.append(f"angka tidak ada di abstrak: {sorted(extra)}")
    # gate parafrase
    ov = shingles(prose) & shingles(abstract)
    if len(ov) >= 3:
        errs.append(f"parafrase gagal: {len(ov)} shingle 8-kata identik dengan abstrak")
    elif ov:
        warns.append(f"{len(ov)} shingle 8-kata mirip abstrak (toleransi maks 2)")
    # panjang
    wc = len(prose.split())
    if not (300 <= wc <= 850):
        errs.append(f"panjang bedah {wc} kata di luar 300-850")
    # larangan dash
    if "—" in prose or "--" in prose:
        errs.append("mengandung em dash atau double hyphen")
    # slug terkait harus eksis
    for t in d.get("terkait") or []:
        folder = "artikel" if t.get("type") == "artikel" else "video"
        if not os.path.isdir(os.path.join(ROOT, folder, str(t.get("slug") or ""))):
            errs.append(f"slug terkait tidak ada di situs: {folder}/{t.get('slug')}")
    return errs, warns


def main():
    files = sorted(f for f in os.listdir(RDIR) if f.endswith(".json")) if os.path.isdir(RDIR) else []
    if not files:
        print("QC RISET GAGAL: tidak ada file bedah di research/")
        return 1
    failed = 0
    for f in files:
        errs, warns = check_file(os.path.join(RDIR, f))
        if errs:
            failed += 1
            print(f"GAGAL {f}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"LOLOS {f}" + (f" (peringatan: {'; '.join(warns)})" if warns else ""))
    print(f"QC riset: {len(files) - failed}/{len(files)} bedah lolos (ILM-R65)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
