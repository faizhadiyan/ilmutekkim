"use client";

import { useEffect } from "react";

// Only behavior is hydrated; the player, article and quiz are server markup.
export default function VideoInteractions({ slug }) {
  useEffect(() => {
    const video = document.getElementById("vplayer");
    if (!video) return;
    const root = video.closest("article");
    const progress = root.querySelector("#vprog");
    const now = root.querySelector("#vnow");
    const heads = Array.from(root.querySelectorAll(".art-h"));
    const seekButtons = Array.from(root.querySelectorAll(".seek"));
    const options = Array.from(root.querySelectorAll(".quiz-opt"));
    const explanations = Array.from(root.querySelectorAll(".quiz-explain"));
    const initial = {
      progress: progress?.getAttribute("style"),
      now: now?.textContent,
      heads: heads.map((head) => head.className),
      options: options.map((option) => option.className),
      hidden: explanations.map((explanation) => explanation.hidden),
    };
    function format(t) {
      t = Math.max(0, t | 0);
      return (t / 60 | 0) + ":" + ("0" + (t % 60)).slice(-2);
    }
    function seek(event) {
      video.currentTime = parseFloat(event.currentTarget.dataset.start);
      video.play();
    }
    function update() {
      const t = video.currentTime;
      const duration = video.duration || 40.9;
      if (progress) progress.style.width = (duration ? t / duration * 100 : 0) + "%";
      if (now) now.textContent = format(t);
      let current = null;
      heads.forEach((head) => { if (parseFloat(head.dataset.start) <= t) current = head; });
      heads.forEach((head) => head.classList.toggle("active", head === current));
    }
    function answer(event) {
      const button = event.currentTarget;
      const box = button.closest(".quiz");
      box.querySelectorAll(".quiz-opt").forEach((option) => option.classList.remove("right", "wrong"));
      button.classList.add(button.dataset.ok === "1" ? "right" : "wrong");
      const explanation = box.querySelector(".quiz-explain");
      if (explanation) explanation.hidden = false;
    }
    seekButtons.forEach((button) => button.addEventListener("click", seek));
    video.addEventListener("timeupdate", update);
    options.forEach((button) => button.addEventListener("click", answer));
    return () => {
      seekButtons.forEach((button) => button.removeEventListener("click", seek));
      video.removeEventListener("timeupdate", update);
      options.forEach((button) => button.removeEventListener("click", answer));
      if (progress) {
        if (initial.progress === null) progress.removeAttribute("style");
        else progress.setAttribute("style", initial.progress);
      }
      if (now) now.textContent = initial.now;
      heads.forEach((head, i) => { head.className = initial.heads[i]; });
      options.forEach((option, i) => { option.className = initial.options[i]; });
      explanations.forEach((explanation, i) => { explanation.hidden = initial.hidden[i]; });
    };
  }, [slug]);
  return null;
}
