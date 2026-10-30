"use client";

import { useEffect } from "react";

// Port the non-theme handlers from main.js onto the server-rendered research/patent indexes.
// No wrapper or client-rendered card markup is needed.
export default function ResearchFilters({ scope }) {
  useEffect(() => {
    const main = document.querySelector("main");
    if (!main) return;

    const chips = main.querySelectorAll(".chip");
    const search = main.querySelector("#search");
    const cards = main.querySelectorAll(".card");
    const empty = main.querySelector("#no-result");
    const vsec = main.querySelector("#video");
    const asec = main.querySelector("#artikel");
    const tools = main.querySelectorAll(".tool-strip a");
    const chipGroups = main.querySelectorAll(".chips");
    const cleanups = [];
    let active = "all";

    function listen(element, event, handler) {
      element.addEventListener(event, handler);
      cleanups.push(() => element.removeEventListener(event, handler));
    }

    // Restore the source DOM on unmount, including React's development effect replay.
    function rememberAttribute(element, name) {
      const value = element.getAttribute(name);
      cleanups.push(() => {
        if (value === null) element.removeAttribute(name);
        else element.setAttribute(name, value);
      });
    }

    cards.forEach((card) => rememberAttribute(card, "style"));
    [vsec, asec].forEach((section) => {
      if (section) rememberAttribute(section, "style");
    });
    [...chips, ...tools, ...chipGroups].forEach((element) => rememberAttribute(element, "class"));
    if (empty) rememberAttribute(empty, "hidden");

    function apply() {
      const q = (search && search.value || "").toLowerCase().trim();
      let shown = 0, vshown = 0, ashown = 0;
      cards.forEach((card) => {
        const okSeries = active === "all" || card.dataset.series === active;
        const okQuery = !q || (card.dataset.title || "").indexOf(q) !== -1;
        let show = okSeries && okQuery;
        if (show && card.classList.contains("v-extra") && active === "all" && !q) show = false;
        card.style.display = show ? "" : "none";
        if (show) {
          shown++;
          if (card.classList.contains("vcard")) vshown++; else ashown++;
        }
      });
      if (empty) empty.hidden = shown !== 0;
      if (vsec) vsec.style.display = vshown ? "" : "none";
      if (asec) asec.style.display = ashown ? "" : "none";
    }

    chips.forEach((chip) => {
      listen(chip, "click", () => {
        chips.forEach((other) => other.classList.remove("active"));
        chip.classList.add("active");
        active = chip.dataset.series;
        apply();
      });
    });
    if (search) listen(search, "input", apply);

    if (window.matchMedia && window.matchMedia("(hover: none)").matches) {
      tools.forEach((link) => {
        listen(link, "click", (event) => {
          if (!link.classList.contains("open")) {
            event.preventDefault();
            main.querySelectorAll(".tool-strip a.open").forEach((other) => other.classList.remove("open"));
            link.classList.add("open");
          }
        });
      });
    }

    if (window.matchMedia && window.matchMedia("(max-width: 760px)").matches) {
      chipGroups.forEach((group) => {
        const groupChips = Array.from(group.querySelectorAll(".chip"));
        if (groupChips.length < 3) return;
        const section = group.closest ? group.closest("section") : null;
        const h2 = section ? section.querySelector("h2") : null;
        const heading = h2 ? h2.textContent.toLowerCase() : "";
        const label = heading.indexOf("topik") !== -1 ? "Topik" : (heading.indexOf("huruf") !== -1 ? "Huruf" : "Seri");
        const count = groupChips.length - 1;
        const rows = [];
        groupChips.forEach((chip) => {
          if (rows.indexOf(chip.offsetTop) === -1) rows.push(chip.offsetTop);
        });
        rows.sort((a, b) => a - b);
        if (rows.length <= 2) return;
        const limit = rows[1];
        groupChips.forEach((chip) => {
          if (chip.offsetTop > limit) chip.classList.add("chip-extra");
        });
        const openText = "Tampilkan semua " + label.toLowerCase() + " (" + count + ") \u25BE";
        const button = document.createElement("button");
        button.type = "button";
        button.className = "chip chips-more";
        button.textContent = openText;
        button.setAttribute("aria-expanded", "false");
        listen(button, "click", () => {
          const open = group.classList.toggle("expanded");
          button.textContent = open ? "Tutup \u25B4" : openText;
          button.setAttribute("aria-expanded", open ? "true" : "false");
        });
        group.parentNode.insertBefore(button, group.nextSibling);
        cleanups.push(() => button.remove());
      });
    }

    return () => cleanups.forEach((cleanup) => cleanup());
  }, [scope]);

  return null;
}
