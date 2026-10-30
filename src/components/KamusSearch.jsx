"use client";

import { useEffect } from "react";

// Port of kamus/assets/search.js; separate from the chatbot's local lookup.
export default function KamusSearch() {
  useEffect(() => {
    const input = document.getElementById("kamus-search");
    const box = document.getElementById("search-results");
    if (!input || !box) return;
    let index = null;
    let active = true;
    const initialResults = box.innerHTML;
    function norm(value) {
      return (value || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    }
    function load() {
      if (index) return Promise.resolve(index);
      return fetch("/kamus/search-index.json")
        .then((response) => response.json())
        .then((data) => { index = data; return data; })
        .catch(() => { index = { terms: [], sectors: [] }; return index; });
    }
    function score(term, query) {
      const title = norm(term.term);
      let best = 0;
      if (title === query) best = 100;
      else if (title.indexOf(query) === 0) best = 80;
      else if (title.indexOf(query) >= 0) best = 60;
      (term.aliases || []).forEach((alias) => {
        const normalized = norm(alias);
        if (normalized === query) best = Math.max(best, 90);
        else if (normalized.indexOf(query) >= 0) best = Math.max(best, 55);
      });
      if (!best && norm(term.search_text).indexOf(query) >= 0) best = 25;
      return best;
    }
    function esc(value) {
      return (value || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
    }
    function render(query) {
      if (!query || query.length < 2) { box.innerHTML = ""; return; }
      load().then((data) => {
        if (!active) return;
        const terms = data.terms.map((term) => ({ t: term, s: score(term, query) }))
          .filter((item) => item.s > 0)
          .sort((a, b) => b.s - a.s).slice(0, 12);
        const sectors = data.sectors.filter((sector) => norm(sector.nama + " " + sector.tagline).indexOf(query) >= 0);
        if (!terms.length && !sectors.length) {
          box.innerHTML = '<div class="zero"><strong>Tidak ditemukan di kamus.</strong><br>' +
            "Istilah ini belum tersedia sebagai entri terverifikasi. Ajukan pertanyaan melalui tombol " +
            "<em>Tanya Tekkim</em> di kanan bawah untuk jawaban AI (akan dilabeli sebagai belum terverifikasi), " +
            "atau coba kata kunci yang lebih umum.</div>";
          return;
        }
        let markup = "";
        if (terms.length) {
          markup += '<div class="sgroup">Istilah</div>';
          terms.forEach((item) => {
            markup += '<a class="sresult" href="/kamus/istilah/' + item.t.slug + '/"><span class="t">' +
              esc(item.t.term) + '</span>' + (item.t.kind === "dasar" ? ' <span class="count">Entri dasar</span>' : '') +
              '<div class="snip">' + esc(item.t.definisi.slice(0, 150)) + "…</div></a>";
          });
        }
        if (sectors.length) {
          markup += '<div class="sgroup">Sektor</div>';
          sectors.forEach((sector) => {
            markup += '<a class="sresult" href="/kamus/sektor/' + sector.slug + '/"><span class="t">' +
              esc(sector.nama) + '</span><div class="snip">' + esc(sector.tagline) + "</div></a>";
          });
        }
        box.innerHTML = markup;
      });
    }
    let debounce = null;
    function onInput() {
      clearTimeout(debounce);
      debounce = setTimeout(() => render(norm(input.value.trim())), 140);
    }
    function onSubmit(event) {
      event.preventDefault();
      render(norm(input.value.trim()));
    }
    function onKeydown(event) {
      if (event.key === "/" && document.activeElement !== input && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
        event.preventDefault();
        input.focus();
      }
    }
    const form = document.getElementById("search-form");
    input.addEventListener("input", onInput);
    if (form) form.addEventListener("submit", onSubmit);
    document.addEventListener("keydown", onKeydown);
    return () => {
      active = false;
      clearTimeout(debounce);
      input.removeEventListener("input", onInput);
      if (form) form.removeEventListener("submit", onSubmit);
      document.removeEventListener("keydown", onKeydown);
      box.innerHTML = initialResults;
    };
  }, []);
  return null;
}
