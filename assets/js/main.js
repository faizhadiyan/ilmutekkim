// Filter seri + pencarian artikel ilmutekkim
(function () {
  var chips = document.querySelectorAll(".chip");
  var search = document.getElementById("search");
  var cards = document.querySelectorAll(".card");
  var empty = document.getElementById("no-result");
  var vsec = document.getElementById("video");
  var asec = document.getElementById("artikel");
  var active = "all";
  function apply() {
    var q = (search && search.value || "").toLowerCase().trim();
    var shown = 0, vshown = 0, ashown = 0;
    cards.forEach(function (c) {
      var okSeries = active === "all" || c.dataset.series === active;
      var okQuery = !q || (c.dataset.title || "").indexOf(q) !== -1;
      var show = okSeries && okQuery;
      // video di luar 4 terbaru hanya muncul saat seri Video Interaktif dipilih atau dicari
      if (show && c.classList.contains("v-extra") && active === "all" && !q) show = false;
      c.style.display = show ? "" : "none";
      if (show) {
        shown++;
        if (c.classList.contains("vcard")) vshown++; else ashown++;
      }
    });
    if (empty) empty.hidden = shown !== 0;
    if (vsec) vsec.style.display = vshown ? "" : "none";
    if (asec) asec.style.display = ashown ? "" : "none";
  }
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("active"); });
      chip.classList.add("active");
      active = chip.dataset.series;
      document.querySelectorAll(".series-select").forEach(function (sel) { sel.value = active; });
      apply();
    });
  });
  if (search) search.addEventListener("input", apply);
})();

// Toggle mode terang/gelap (default mengikuti sistem perangkat, pilihan disimpan)
(function () {
  var btn = document.getElementById("themeToggle");
  if (!btn) return;
  btn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("ilm-theme", next); } catch (e) {}
  });
})();

// Strip fitur di perangkat sentuh: ketukan pertama membuka deskripsi, ketukan kedua membuka halaman
(function () {
  if (!window.matchMedia || !window.matchMedia("(hover: none)").matches) return;
  document.querySelectorAll(".tool-strip a").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      if (!a.classList.contains("open")) {
        ev.preventDefault();
        document.querySelectorAll(".tool-strip a.open").forEach(function (o) { o.classList.remove("open"); });
        a.classList.add("open");
      }
    });
  });
})();

// Di mobile, chip seri diganti dropdown pemilih; chip tetap dipakai di desktop
(function () {
  document.querySelectorAll(".chips").forEach(function (c) {
    var chips = c.querySelectorAll(".chip");
    if (!chips.length) return;
    var section = c.closest ? c.closest("section") : null;
    var h2 = section ? section.querySelector("h2") : null;
    var htxt = h2 ? h2.textContent.toLowerCase() : "";
    var label = htxt.indexOf("topik") !== -1 ? "Topik" : (htxt.indexOf("huruf") !== -1 ? "Huruf" : "Seri");
    var wrap = document.createElement("label");
    wrap.className = "series-select-wrap";
    var span = document.createElement("span");
    span.textContent = label + ":";
    var sel = document.createElement("select");
    sel.className = "series-select";
    sel.setAttribute("aria-label", "Pilih " + label.toLowerCase());
    chips.forEach(function (chip) {
      var opt = document.createElement("option");
      opt.value = chip.dataset.series;
      opt.textContent = chip.textContent;
      if (chip.classList.contains("active")) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", function () {
      var target = null;
      chips.forEach(function (chip) { if (chip.dataset.series === sel.value) target = chip; });
      if (target) target.click();
    });
    wrap.appendChild(span);
    wrap.appendChild(sel);
    c.parentNode.insertBefore(wrap, c.nextSibling);
  });
})();
