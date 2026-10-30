"use client";

import { useEffect } from "react";
import { carothersXn, lmtd, convertTemp, convertPress, convertFlow, mccabeThiele, eqY } from "@/lib/calculators";
export default function CalculatorInteractions() {
  useEffect(() => {
    const main = document.querySelector("main");
    if (!main) return;
    const cleanups = [];
    function listen(id, handler) {
      const input = el(id);
      if (!input) return;
      input.addEventListener("input", handler);
      cleanups.push(() => input.removeEventListener("input", handler));
    }
    const outputs = ["car-out", "lm-out", "cv-out", "mt-out"].map(id => el(id));
    const initial = outputs.map(output => output.innerHTML);
    function el(id) {
      return main.querySelector("#" + id);
    }
    function fmt(v, d) {
      return v === null || !isFinite(v) ? "n/a" : Number(v).toFixed(d === undefined ? 3 : d);
    }
    function runCarothers() {
      var p = parseFloat(el("car-p").value),
        r = parseFloat(el("car-r").value);
      if (!isFinite(p) || p <= 0 || p >= 1) {
        el("car-out").textContent = "Konversi harus di antara 0 dan 1.";
        return;
      }
      var xn = carothersXn(p, isFinite(r) && r > 0 && r < 1 ? r : 1);
      var baris = [0.9, 0.95, 0.99, 0.995, 0.999].map(function (pp) {
        return "<li>p = " + pp + " &rarr; Xn = " + fmt(carothersXn(pp, isFinite(r) && r > 0 && r < 1 ? r : 1), 1) + "</li>";
      }).join("");
      el("car-out").innerHTML = "<p><strong>Xn = " + fmt(xn, 2) + "</strong> unit monomer rata-rata per rantai.</p><ul>" + baris + "</ul>";
    }
    function runLmtd() {
      var thi = parseFloat(el("lm-thi").value),
        tho = parseFloat(el("lm-tho").value),
        tci = parseFloat(el("lm-tci").value),
        tco = parseFloat(el("lm-tco").value),
        mode = el("lm-mode").value;
      var dT1, dT2;
      if (mode === "counter") {
        dT1 = thi - tco;
        dT2 = tho - tci;
      } else {
        dT1 = thi - tci;
        dT2 = tho - tco;
      }
      var v = lmtd(dT1, dT2);
      el("lm-out").innerHTML = v === null ? "<p>Suhu berpotongan (temperature cross): beda suhu di salah satu ujung tidak positif. Periksa kembali suhu masuk dan keluarnya.</p>" : "<p>&Delta;T ujung 1 = " + fmt(dT1, 1) + " &deg;C, &Delta;T ujung 2 = " + fmt(dT2, 1) + " &deg;C.<br><strong>LMTD = " + fmt(v, 2) + " &deg;C</strong></p>";
    }
    function runConv() {
      var t = convertTemp(parseFloat(el("cv-tv").value) || 0, el("cv-tu").value);
      var p = convertPress(parseFloat(el("cv-pv").value) || 0, el("cv-pu").value);
      var f = convertFlow(parseFloat(el("cv-fv").value) || 0, el("cv-fu").value);
      function tabel(obj, satuan) {
        return Object.keys(obj).map(function (u) {
          return "<li>" + fmt(obj[u], 4) + " " + u + "</li>";
        }).join("");
      }
      el("cv-out").innerHTML = "<h3>Suhu</h3><ul>" + tabel(t) + "</ul><h3>Tekanan</h3><ul>" + tabel(p) + "</ul><h3>Aliran volumetrik</h3><ul>" + tabel(f) + "</ul>";
    }
    function drawMT(res, alpha, xD, xB, zF) {
      var cv = el("mt-canvas");
      if (!cv) return;
      var ctx = cv.getContext("2d"),
        W = cv.width,
        H = cv.height,
        pad = 42;
      ctx.clearRect(0, 0, W, H);
      function X(x) {
        return pad + x * (W - 2 * pad);
      }
      function Y(y) {
        return H - pad - y * (H - 2 * pad);
      }
      ctx.strokeStyle = "#C7D3EA";
      ctx.lineWidth = 1;
      ctx.strokeRect(pad, pad, W - 2 * pad, H - 2 * pad);
      ctx.beginPath();
      ctx.moveTo(X(0), Y(0));
      ctx.lineTo(X(1), Y(1));
      ctx.strokeStyle = "#666";
      ctx.stroke();
      ctx.beginPath();
      for (var i = 0; i <= 100; i++) {
        var x = i / 100,
          y = eqY(x, alpha);
        i ? ctx.lineTo(X(x), Y(y)) : ctx.moveTo(X(x), Y(y));
      }
      ctx.strokeStyle = "#00B4D8";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "#F59E0B";
      ctx.beginPath();
      ctx.moveTo(X(xB), Y(xB));
      ctx.lineTo(X(res.intersect.x), Y(res.intersect.y));
      ctx.lineTo(X(xD), Y(xD));
      ctx.stroke();
      ctx.strokeStyle = "#0066CC";
      ctx.beginPath();
      res.points.forEach(function (pt, i2) {
        i2 ? ctx.lineTo(X(pt.x), Y(pt.y)) : ctx.moveTo(X(pt.x), Y(pt.y));
      });
      ctx.stroke();
      ctx.fillStyle = "#556070";
      ctx.font = "11px sans-serif";
      ctx.fillText("x (cairan)", W / 2 - 24, H - 12);
      ctx.save();
      ctx.rotate(-Math.PI / 2);
      ctx.fillText("y (uap)", -H / 2 - 20, 14);
      ctx.restore();
      ctx.fillText("kurva setimbang", X(0.62), Y(eqY(0.62, alpha)) - 6);
      ctx.fillText("tangga tahap", X(0.08), Y(0.92));
    }
    function runMT() {
      var alpha = parseFloat(el("mt-alpha").value),
        zF = parseFloat(el("mt-zf").value),
        xD = parseFloat(el("mt-xd").value),
        xB = parseFloat(el("mt-xb").value),
        q = parseFloat(el("mt-q").value),
        f = parseFloat(el("mt-f").value);
      if (!(alpha > 1) || !(xB < zF && zF < xD) || !(xB > 0 && xD < 1)) {
        el("mt-out").textContent = "Periksa masukan: perlu alpha > 1 dan xB < zF < xD, semua fraksi di antara 0 dan 1.";
        return;
      }
      var res = mccabeThiele(alpha, zF, xD, xB, q, f);
      el("mt-out").innerHTML = "<p>R minimum = <strong>" + fmt(res.Rmin, 3) + "</strong>; R operasi = <strong>" + fmt(res.R, 3) + "</strong>.<br>Jumlah tahap minimum (reflux total, Fenske) = <strong>" + fmt(res.Nmin, 2) + "</strong>.<br>Jumlah tahap total termasuk reboiler = <strong>" + res.stages + "</strong>, umpan masuk sekitar tahap ke-<strong>" + res.feedStage + "</strong> dari atas.</p>" + "<p>Angka tahap adalah cacah tahap kesetimbangan dari tangga McCabe-Thiele, bukan jumlah tray fisik; tray nyata diperoleh setelah efisiensi tray diketahui.</p>";
      drawMT(res, alpha, xD, xB, zF);
    }
    ["car-p", "car-r"].forEach(function (id) {
      listen(id, runCarothers);
    });
    ["lm-thi", "lm-tho", "lm-tci", "lm-tco", "lm-mode"].forEach(function (id) {
      listen(id, runLmtd);
    });
    ["cv-tv", "cv-tu", "cv-pv", "cv-pu", "cv-fv", "cv-fu"].forEach(function (id) {
      listen(id, runConv);
    });
    ["mt-alpha", "mt-zf", "mt-xd", "mt-xb", "mt-q", "mt-f"].forEach(function (id) {
      listen(id, runMT);
    });
    runCarothers();
    runLmtd();
    runConv();
    runMT();
    return () => {
      cleanups.forEach(cleanup => cleanup());
      outputs.forEach((output, index) => {
        output.innerHTML = initial[index];
      });
      const canvas = el("mt-canvas");
      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    };
  }, []);
  return null;
}
