// Tanya Tekkim: chatbot pop-up Kamus Industri Kimia.
// Alur: (1) cari di search-index.json lokal; kecocokan kuat dijawab dari
// entri glosarium pada lapis level terpilih + sitasi. (2) Selain itu POST
// /api/ask dan jawaban dilabeli "AI — belum terverifikasi".
(function () {
  var level = "awam";
  var INDEX = null;
  var btn = document.createElement("button");
  btn.id = "tt-btn"; btn.type = "button"; btn.textContent = "💬 Tanya Tekkim";
  btn.setAttribute("aria-label", "Buka chatbot Tanya Tekkim");
  var panel = document.createElement("div");
  panel.id = "tt-panel"; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Tanya Tekkim");
  panel.innerHTML =
    '<div id="tt-head"><div><div class="t">Tanya Tekkim</div><div class="s">Asisten kamus teknik kimia IlmuTekkim</div></div>' +
    '<button id="tt-close" type="button" aria-label="Tutup">×</button></div>' +
    '<div id="tt-levels"><span>Level:</span>' +
    '<button type="button" class="tt-lv on" data-lv="awam">Awam</button>' +
    '<button type="button" class="tt-lv" data-lv="tekkim">Tekkim</button>' +
    '<button type="button" class="tt-lv" data-lv="plant">Plant</button></div>' +
    '<div id="tt-msgs"></div>' +
    '<div id="tt-examples"></div>' +
    '<form id="tt-form"><input id="tt-input" type="text" maxlength="500" placeholder="Tulis pertanyaan…" autocomplete="off">' +
    '<button id="tt-send" type="submit">Kirim</button></form>';
  document.body.appendChild(btn); document.body.appendChild(panel);
  var msgs = panel.querySelector("#tt-msgs");
  var input = panel.querySelector("#tt-input");
  var send = panel.querySelector("#tt-send");
  var examples = ["Apa itu FFA dan mengapa penting?", "Mengapa kolom distilasi bisa flooding?", "Bagaimana kavitasi merusak pompa?"];
  var exBox = panel.querySelector("#tt-examples");
  examples.forEach(function (q) {
    var b = document.createElement("button"); b.type = "button"; b.className = "tt-ex"; b.textContent = q;
    b.addEventListener("click", function () { input.value = q; form.dispatchEvent(new Event("submit")); });
    exBox.appendChild(b);
  });
  function esc(s) { return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
  function addMsg(text, who, extra) {
    var d = document.createElement("div");
    d.className = "tt-msg " + who; d.innerHTML = text + (extra || "");
    msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight; return d;
  }
  function greet() {
    if (msgs.childElementCount) return;
    addMsg("Selamat datang di Tanya Tekkim. Ajukan pertanyaan istilah atau proses teknik kimia. " +
      "Pertanyaan yang tersedia di glosarium akan dijawab dari entri terverifikasi; pertanyaan lain diteruskan ke AI dan dilabeli sebagai belum terverifikasi.", "bot");
  }
  btn.addEventListener("click", function () { panel.classList.toggle("open"); greet(); input.focus(); });
  panel.querySelector("#tt-close").addEventListener("click", function () { panel.classList.remove("open"); });
  panel.querySelectorAll(".tt-lv").forEach(function (b) {
    b.addEventListener("click", function () {
      level = b.getAttribute("data-lv");
      panel.querySelectorAll(".tt-lv").forEach(function (x) { x.classList.toggle("on", x === b); });
    });
  });
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function load() {
    if (INDEX) return Promise.resolve(INDEX);
    return fetch("/kamus/search-index.json").then(function (r) { return r.json(); })
      .then(function (j) { INDEX = j; return j; })
      .catch(function () { INDEX = { terms: [] }; return INDEX; });
  }
  function strongMatch(idx, q) {
    var best = null, bestScore = 0;
    idx.terms.forEach(function (t) {
      var s = 0, tn = norm(t.term);
      if (q === tn) s = 100;
      else if (q.indexOf(tn) >= 0 || tn.indexOf(q) >= 0 && q.length >= 4) s = 85;
      (t.aliases || []).forEach(function (a) {
        var an = norm(a);
        if (an.length >= 3 && q.indexOf(an) >= 0) s = Math.max(s, 88);
      });
      // kecocokan kata kunci judul di dalam pertanyaan panjang
      if (!s) {
        var words = tn.split(/[^a-z0-9]+/).filter(function (w) { return w.length >= 5; });
        var hit = words.filter(function (w) { return q.indexOf(w) >= 0; }).length;
        if (words.length && hit === words.length) s = 70;
      }
      if (s > bestScore) { bestScore = s; best = t; }
    });
    return bestScore >= 70 ? best : null;
  }
  function entryAnswer(t) {
    var body = "";
    if (t.kind === "dasar" || !t.mekanisme) {
      body = "<strong>" + esc(t.term) + ".</strong> " + esc(t.definisi) +
        "<br><em>Entri dasar:</em> bedah dalam (mekanisme, persamaan, sensitivitas) menyusul.";
      return body + '<br><span class="tt-src glos">Sumber: Glosarium terverifikasi · Entri dasar</span>' +
        '<a class="tt-cite" href="/kamus/istilah/' + t.slug + '/">Baca entri lengkap: ' + esc(t.term) + "</a>";
    }
    if (level === "awam") {
      body = "<strong>" + esc(t.term) + ".</strong> " + esc(t.definisi) +
        (t.analogi ? "<br><em>Analogi:</em> " + esc(t.analogi) : "");
    } else if (level === "tekkim") {
      body = "<strong>" + esc(t.term) + " — mekanisme.</strong> " + esc(t.mekanisme) +
        "<br><em>Prinsip:</em> " + esc(t.prinsip);
    } else {
      var biaya = (t.plant.biaya || []).join(" ");
      var cek = (t.plant.checklist && t.plant.checklist[0])
        ? " Contoh diagnosis: gejala “" + esc(t.plant.checklist[0].gejala) + "” umumnya disebabkan " +
          esc(t.plant.checklist[0].penyebab) + "." : "";
      body = "<strong>" + esc(t.term) + " — sudut plant.</strong> " + esc(biaya) + cek;
    }
    var extra = '<br><span class="tt-src glos">Sumber: Glosarium terverifikasi</span>' +
      '<a class="tt-cite" href="/kamus/istilah/' + t.slug + '/">Baca entri lengkap: ' + esc(t.term) + "</a>";
    return body + extra;
  }
  var form = panel.querySelector("#tt-form");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    addMsg(esc(q), "user"); input.value = ""; send.disabled = true;
    var wait = addMsg("⏳ Mencari di glosarium terlebih dahulu…", "bot");
    load().then(function (idx) {
      var t = strongMatch(idx, norm(q));
      if (t) { wait.innerHTML = entryAnswer(t); send.disabled = false; return; }
      wait.innerHTML = "⏳ Tidak ditemukan di glosarium. Menanyakan AI…";
      return fetch("/api/ask", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, level: level })
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok && res.j.answer) {
            wait.innerHTML = esc(res.j.answer).replace(/\n/g, "<br>") +
              '<br><span class="tt-src ai">AI — belum terverifikasi</span>';
          } else if (res.j && res.j.error === "ai_not_configured") {
            wait.innerHTML = "Istilah ini belum ada di glosarium dan fitur AI belum dikonfigurasi pada server. " +
              "Coba cari istilah terkait melalui kolom pencarian kamus." +
              '<br><span class="tt-src ai">AI — belum tersedia</span>';
          } else if (res.j && res.j.error === "rate_limited") {
            wait.innerHTML = "Terlalu banyak pertanyaan dalam waktu singkat. Tunggu beberapa menit, lalu coba kembali.";
          } else {
            wait.innerHTML = "AI tidak dapat menjawab saat ini. Coba kembali beberapa saat lagi." +
              '<br><span class="tt-src ai">AI — belum terverifikasi</span>';
          }
        }).catch(function () {
          wait.innerHTML = "Koneksi ke layanan AI gagal. Coba kembali beberapa saat lagi.";
        }).then(function () { send.disabled = false; msgs.scrollTop = msgs.scrollHeight; });
    });
  });
  // Dipakai halaman utama sebagai pintu masuk dari keadaan nol hasil.
  window.TanyaTekkim = { open: function () { panel.classList.add("open"); greet(); input.focus(); } };
})();
