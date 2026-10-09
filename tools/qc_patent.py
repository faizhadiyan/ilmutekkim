#!/usr/bin/env python3
"""QC mekanis bedah paten website ilmutekkim (ILM-R66).

Gate keras, dijalankan di dalam build sebelum render:
1. Field wajib lengkap; coverage persis "Berdasarkan dokumen paten publik";
   sumber adalah URL; nomor paten berformat wajar.
2. ANTI KARANG-ANGKA: setiap token angka di badan bedah (judul, lead, masalah,
   klaim, cara, batas, arti, alasan kesimpulan) WAJIB muncul di teks sumber
   terverifikasi (src_text). Field bibliografis (nomor, tanggal, status) adalah
   data terverifikasi itu sendiri dan tidak dipindai.
3. ANTI SALIN: tidak boleh ada >=3 urutan 8 kata identik dengan teks sumber.
4. Klaim hanya parafrase; kesimpulan dalam daftar yang diizinkan;
   tautan terkait harus benar-benar ada di situs.
Keluar 1 bila ada pelanggaran (build gagal).
"""
# ILM-R66
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = os.path.join(ROOT, "paten")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build as BLD  # noqa: E402

KESIMPULAN = {"Baca dokumen patennya", "Cukup baca bedahnya"}
WAJIB = ["slug", "judul", "topik", "nomor", "judul_paten", "inventor",
         "pemilik", "diajukan", "terbit", "status", "sumber", "coverage",
         "date_bedah", "lead", "masalah", "klaim", "cara", "batas", "arti",
         "kesimpulan", "kesimpulan_alasan", "terkait", "src_text"]
FIELD_ANGKA = ["judul", "lead", "masalah", "cara", "arti", "kesimpulan_alasan"]

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
VALID = {a[0] for a in BLD.ARTICLES} | {v["slug"] for v in BLD.VIDEOS}


def norm_text(t):
    t = unicodedata.normalize("NFKC", str(t)).translate(SUB).lower()
    return re.sub(r"[^a-z0-9 ]+", " ", t)


def angka_dari(t):
    t = unicodedata.normalize("NFKC", str(t)).translate(SUB).replace(",", ".")
    out = set()
    for m in re.findall(r"\d+(?:\.\d+)?", t):
        v = m.rstrip("0").rstrip(".") if "." in m else m
        out.add(v or "0")
        out.add(str(int(float(m))) if float(m) == int(float(m)) else v)
    return out


def shingle(t, n=8):
    w = norm_text(t).split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def main():
    files = sorted(f for f in os.listdir(PAT) if f.endswith(".json"))
    gagal, peringatan = [], []
    for fn in files:
        d = json.load(open(os.path.join(PAT, fn)))
        slug = d.get("slug", fn)
        for k in WAJIB:
            if k not in d or d[k] in ("", [], None):
                gagal.append(f"{slug}: field wajib kosong: {k}")
        if d.get("coverage") != "Berdasarkan dokumen paten publik":
            gagal.append(f"{slug}: coverage salah: {d.get('coverage')!r}")
        if not str(d.get("sumber", "")).startswith("http"):
            gagal.append(f"{slug}: sumber bukan URL")
        if not re.match(r"^[A-Z]{2}[0-9]{4,}[A-Z0-9]*$", str(d.get("nomor", ""))):
            gagal.append(f"{slug}: nomor paten tak wajar: {d.get('nomor')!r}")
        if d.get("kesimpulan") not in KESIMPULAN:
            gagal.append(f"{slug}: kesimpulan di luar daftar: {d.get('kesimpulan')!r}")
        bagian = [d.get(k, "") for k in FIELD_ANGKA]
        bagian += d.get("klaim", []) + d.get("batas", [])
        teks = "\n".join(str(x) for x in bagian)
        src = d.get("src_text", "")
        ekstra = angka_dari(teks) - angka_dari(src)
        if ekstra:
            gagal.append(f"{slug}: angka tak ada di teks sumber: {sorted(ekstra)}")
        tabrak = shingle(teks) & shingle(src)
        if len(tabrak) >= 3:
            gagal.append(f"{slug}: {len(tabrak)} shingle 8-kata sama dgn sumber")
        elif tabrak:
            peringatan.append(f"{slug}: {len(tabrak)} shingle (di bawah ambang)")
        kata = len(teks.split())
        if not 250 <= kata <= 950:
            gagal.append(f"{slug}: panjang {kata} kata di luar 250-950")
        for k in WAJIB:
            v = d.get(k)
            for s in (v if isinstance(v, list) else [v]):
                if isinstance(s, str) and ("—" in s or "--" in s):
                    gagal.append(f"{slug}: em dash/double hyphen di {k}")
        for t in d.get("terkait", []):
            if t.get("slug") not in VALID:
                gagal.append(f"{slug}: terkait tak dikenal: {t.get('slug')}")
    for p in peringatan:
        print("PERINGATAN:", p)
    if gagal:
        print("QC PATEN GAGAL:")
        for g in gagal:
            print(" -", g)
        return 1
    print(f"QC PATEN: {len(files)}/{len(files)} bedah paten LOLOS gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
