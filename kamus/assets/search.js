// Pencarian klien Kamus Industri Kimia: memuat search-index.json,
// peringkat judul persis > alias > isi, hasil tergrup Istilah / Sektor.
(function () {
  var input = document.getElementById("kamus-search");
  var box = document.getElementById("search-results");
  if (!input || !box) return;
  var INDEX = null;
  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function load() {
    if (INDEX) return Promise.resolve(INDEX);
    return fetch("/kamus/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { INDEX = j; return j; })
      .catch(function () { INDEX = { terms: [], sectors: [] }; return INDEX; });
  }
  function score(term, q) {
    var t = norm(term.term), best = 0;
    if (t === q) best = 100;
    else if (t.indexOf(q) === 0) best = 80;
    else if (t.indexOf(q) >= 0) best = 60;
    (term.aliases || []).forEach(function (a) {
      var an = norm(a);
      if (an === q) best = Math.max(best, 90);
      else if (an.indexOf(q) >= 0) best = Math.max(best, 55);
    });
    if (!best && norm(term.search_text).indexOf(q) >= 0) best = 25;
    return best;
  }
  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
  }
  function render(q) {
    if (!q || q.length < 2) { box.innerHTML = ""; return; }
    load().then(function (idx) {
      var terms = idx.terms.map(function (t) { return { t: t, s: score(t, q) }; })
        .filter(function (x) { return x.s > 0; })
        .sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
      var secs = idx.sectors.filter(function (s) {
        return norm(s.nama + " " + s.tagline).indexOf(q) >= 0;
      });
      if (!terms.length && !secs.length) {
        box.innerHTML = '<div class="zero"><strong>Tidak ditemukan di kamus.</strong><br>' +
          "Istilah ini belum tersedia sebagai entri terverifikasi. Ajukan pertanyaan melalui tombol " +
          "<em>Tanya Tekkim</em> di kanan bawah untuk jawaban AI (akan dilabeli sebagai belum terverifikasi), " +
          "atau coba kata kunci yang lebih umum.</div>";
        return;
      }
      var h = "";
      if (terms.length) {
        h += '<div class="sgroup">Istilah</div>';
        terms.forEach(function (x) {
          h += '<a class="sresult" href="/kamus/istilah/' + x.t.slug + '/"><span class="t">' +
            esc(x.t.term) + '</span>' + (x.t.kind === "dasar" ? ' <span class="count">Entri dasar</span>' : '') +
            '<div class="snip">' + esc(x.t.definisi.slice(0, 150)) + "…</div></a>";
        });
      }
      if (secs.length) {
        h += '<div class="sgroup">Sektor</div>';
        secs.forEach(function (s) {
          h += '<a class="sresult" href="/kamus/sektor/' + s.slug + '/"><span class="t">' +
            esc(s.nama) + '</span><div class="snip">' + esc(s.tagline) + "</div></a>";
        });
      }
      box.innerHTML = h;
    });
  }
  var deb = null;
  input.addEventListener("input", function () {
    clearTimeout(deb);
    deb = setTimeout(function () { render(norm(input.value.trim())); }, 140);
  });
  var form = document.getElementById("search-form");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault(); render(norm(input.value.trim()));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== input && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus();
    }
  });
})();
