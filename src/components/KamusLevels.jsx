"use client";

import { useEffect } from "react";

export default function KamusLevels({ slug }) {
  useEffect(() => {
    const segment = document.querySelector(".seg");
    if (!segment) return;
    const root = segment.closest(".wrap");
    const buttons = Array.from(segment.querySelectorAll("button"));
    const layers = Array.from(root.querySelectorAll("[data-layer]"));
    const initialClasses = buttons.map((button) => button.className);
    const initialStyles = layers.map((layer) => layer.getAttribute("style"));
    function choose(event) {
      const button = event.currentTarget;
      buttons.forEach((item) => item.classList.toggle("on", item === button));
      const level = button.getAttribute("data-lv");
      layers.forEach((layer) => {
        const name = layer.getAttribute("data-layer");
        layer.style.display = (level === "semua" || name === level) ? "" : "none";
      });
    }
    buttons.forEach((button) => button.addEventListener("click", choose));
    const defaultButton = segment.querySelector('button[data-lv="tekkim"]');
    if (defaultButton) defaultButton.click();
    return () => {
      buttons.forEach((button, index) => {
        button.removeEventListener("click", choose);
        button.className = initialClasses[index];
      });
      layers.forEach((layer, index) => {
        if (initialStyles[index] === null) layer.removeAttribute("style");
        else layer.setAttribute("style", initialStyles[index]);
      });
    };
  }, [slug]);
  return null;
}
