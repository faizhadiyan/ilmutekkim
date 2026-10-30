export default function KamusShell({ children }) {
  return (
    <div className="wrap">
      {children}
      <div className="foot">
        <nav><a href="/kamus">Kamus</a> · <a href="/artikel/">Artikel</a> · <a href="/video/">Video</a> · <a href="/riset/">Riset</a> · <a href="/jalur/">Jalur Belajar</a></nav>
        <p>Kamus Industri Kimia — bagian dari <a href="/">ilmutekkim.site</a>.{"\n"}
          Seluruh angka operasi pada kamus ini adalah rentang umum textbook, bukan data plant atau data perusahaan mana pun.</p>
      </div>
    </div>
  );
}
