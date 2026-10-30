// Kalkulator interaktif ilmutekkim (ILM-R68)
// Fungsi hitung murni standar: Carothers, LMTD, konversi satuan, McCabe-Thiele.

function carothersXn(p, r) {
  if (r === undefined || r === null || r >= 1) {
    return 1 / (1 - p);
  }
  return (1 + r) / (1 + r - 2 * r * p);
}

function lmtd(dT1, dT2) {
  if (dT1 <= 0 || dT2 <= 0) return null;
  if (Math.abs(dT1 - dT2) < 1e-9) return dT1;
  return (dT1 - dT2) / Math.log(dT1 / dT2);
}

var TEMP = {
  C: { toK: function (v) { return v + 273.15; }, fromK: function (k) { return k - 273.15; } },
  F: { toK: function (v) { return (v - 32) * 5 / 9 + 273.15; }, fromK: function (k) { return (k - 273.15) * 9 / 5 + 32; } },
  K: { toK: function (v) { return v; }, fromK: function (k) { return k; } }
};
var PRESS_PA = { Pa: 1, kPa: 1e3, bar: 1e5, atm: 101325, psi: 6894.757293168 };
var FLOW_M3S = { "m3/s": 1, "m3/h": 1 / 3600, "L/s": 1e-3, "gpm (US)": 3.785411784e-3 / 60 };

function convertTemp(v, from) {
  var k = TEMP[from].toK(v);
  return { C: TEMP.C.fromK(k), F: TEMP.F.fromK(k), K: k };
}
function convertPress(v, from) {
  var pa = v * PRESS_PA[from], out = {};
  Object.keys(PRESS_PA).forEach(function (u) { out[u] = pa / PRESS_PA[u]; });
  return out;
}
function convertFlow(v, from) {
  var m3s = v * FLOW_M3S[from], out = {};
  Object.keys(FLOW_M3S).forEach(function (u) { out[u] = m3s / FLOW_M3S[u]; });
  return out;
}

function eqY(x, alpha) { return alpha * x / (1 + (alpha - 1) * x); }
function eqX(y, alpha) { return y / (alpha - (alpha - 1) * y); }

// McCabe-Thiele biner, volatilitas relatif konstan, kondensor total.
// q: kondisi umpan (1 = cair jenuh). Mengembalikan Rmin, Nmin (Fenske),
// jumlah tahap total (termasuk reboiler), tahap umpan, dan titik tangga untuk gambar.
function mccabeThiele(alpha, zF, xD, xB, q, rFactor) {
  function qline(x) {
    if (Math.abs(q - 1) < 1e-12) return null; // vertikal x = zF
    return (q / (q - 1)) * x - zF / (q - 1);
  }
  // titik pinch: perpotongan kurva setimbang dengan garis umpan
  var px, py;
  if (Math.abs(q - 1) < 1e-12) {
    px = zF; py = eqY(zF, alpha);
  } else {
    var lo = 0.0001, hi = 0.9999, fLo = eqY(lo, alpha) - qline(lo), fHi = eqY(hi, alpha) - qline(hi);
    if (fLo * fHi > 0) { px = zF; py = eqY(zF, alpha); }
    else {
      for (var i = 0; i < 200; i++) {
        var mid = (lo + hi) / 2, fMid = eqY(mid, alpha) - qline(mid);
        if (fLo * fMid <= 0) { hi = mid; } else { lo = mid; fLo = fMid; }
      }
      px = (lo + hi) / 2; py = eqY(px, alpha);
    }
  }
  var mPinch = (xD - py) / (xD - px);
  var Rmin = mPinch / (1 - mPinch);
  var R = rFactor * Rmin;
  var mRect = R / (R + 1), bRect = xD / (R + 1);
  // titik potong garis rectifying dengan garis umpan
  var ix, iy;
  if (Math.abs(q - 1) < 1e-12) {
    ix = zF; iy = mRect * zF + bRect;
  } else {
    var mq = q / (q - 1), bq = -zF / (q - 1);
    ix = (bq - bRect) / (mRect - mq); iy = mRect * ix + bRect;
  }
  var mStrip = (iy - xB) / (ix - xB), bStrip = xB - mStrip * xB;
  function opY(x) { return x > ix ? mRect * x + bRect : mStrip * x + bStrip; }
  // tangga tahap: mulai kondensor total y1 = xD
  var pts = [{ x: xD, y: xD }];
  var y = xD, stages = 0, feedStage = 0;
  while (stages < 500) {
    var x = eqX(y, alpha);
    pts.push({ x: x, y: y });
    stages++;
    if (x <= xB) break;
    var yNext = opY(x);
    if (!feedStage && x <= ix) feedStage = stages;
    pts.push({ x: x, y: yNext });
    y = yNext;
  }
  var Nmin = Math.log((xD / (1 - xD)) * ((1 - xB) / xB)) / Math.log(alpha);
  return {
    Rmin: Rmin, R: R, Nmin: Nmin, stages: stages, feedStage: feedStage || stages,
    intersect: { x: ix, y: iy }, points: pts,
    lines: { mRect: mRect, bRect: bRect, mStrip: mStrip, bStrip: bStrip }
  };
}


export { carothersXn, lmtd, convertTemp, convertPress, convertFlow, mccabeThiele, eqY, eqX };
