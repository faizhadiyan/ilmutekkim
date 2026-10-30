"use client";

export default function Header() {
  function toggleTheme() {
    var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("ilm-theme", next); } catch (e) {}
  }

  return (
    <header className="site-header">
      <a className="brand" href="/">ilmu<span>tekkim</span></a>
      <input type="checkbox" id="nav-toggle" className="nav-toggle" aria-hidden="true" />
      <label htmlFor="nav-toggle" className="burger" aria-label="Buka menu">&#9776;</label>
      <nav>
        <a href="/">Articles &amp; Videos</a>
        <a href="/riset/">Riset</a>
        <a href="/jalur/">Jalur</a>
        <a href="/kamus">Kamus</a>
      </nav>
      <button type="button" className="theme-toggle" id="themeToggle" onClick={toggleTheme} aria-label="Beralih antara mode terang dan mode gelap" title="Mode terang / gelap"><span className="ic-sun" aria-hidden="true">&#9728;</span><span className="ic-moon" aria-hidden="true">&#9790;</span></button>
    </header>
  );
}
