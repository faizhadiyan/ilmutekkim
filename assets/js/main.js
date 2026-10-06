// Filter seri + pencarian artikel ilmutekkim
(function () {
  var chips = document.querySelectorAll(".chip");
  var search = document.getElementById("search");
  var cards = document.querySelectorAll(".card");
  var empty = document.getElementById("no-result");
  var active = "all";
  function apply() {
    var q = (search && search.value || "").toLowerCase().trim();
    var shown = 0;
    cards.forEach(function (c) {
      var okSeries = active === "all" || c.dataset.series === active;
      var okQuery = !q || (c.dataset.title || "").indexOf(q) !== -1;
      var show = okSeries && okQuery;
      c.style.display = show ? "" : "none";
      if (show) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
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
