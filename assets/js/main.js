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
