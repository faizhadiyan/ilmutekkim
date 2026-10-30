import home from "@/data/home.json";
import HomeCard from "@/components/HomeCard";
import HomeInteractions from "@/components/HomeInteractions";

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <nav className="tool-strip" aria-label="Fitur utama situs">
          <a href="#artikel"><span>01</span><b>Artikel dan Video</b><i>61 artikel mendalam bersitasi dan 32 video dengan artikel pendamping</i></a>
          <a href="/riset/"><span>02</span><b>Riset</b><i>19 bedah jurnal dan 5 bedah paten dengan catatan kritis dan kesimpulan eksplisit</i></a>
          <a href="/jalur/"><span>03</span><b>Jalur Belajar</b><i>7 jalur terkurasi, 40 langkah berurutan dari konsep dasar ke aplikasi</i></a>
          <a href="/kamus"><span>04</span><b>Kamus</b><i>48 istilah teknik kimia: 20 entri dalam dan 28 entri dasar dengan bacaan lanjutan</i></a>
          <a href="/referensi/"><span>05</span><b>Referensi</b><i>Seluruh literatur, paper yang dibedah, dan dokumen paten dalam satu perpustakaan</i></a>
          <a href="/kalkulator/"><span>06</span><b>Kalkulator</b><i>Polimerisasi Carothers, LMTD, rancangan McCabe-Thiele, dan konversi satuan proses</i></a>
        </nav>
        <div className="hero-grid">
          <h1>Teknik kimia, ditelaah dari prosesnya.</h1>
          <div className="hero-side">
            <p>Distilasi, kilang minyak, pengolahan kelapa sawit, semen, pulp dan kertas, hingga sistem pengaman proses.
              Setiap topik ditelaah secara bertahap dan mendalam, dilengkapi sitasi literatur standar teknik kimia.</p>
            <a className="btn" href="#artikel">Telusuri 61 artikel</a>
            <a className="btn ghost" href="/video/">Lihat 32 video</a>
          </div>
        </div>
      </section>
      <section id="seri" className="series-bar">
        <h2>Telusuri menurut seri</h2>
        <div className="chips">
          <button className="chip active" data-series="all">Semua</button>
          {home.series.map((series) => (
            <button className="chip" data-series={series} key={series}>{series}</button>
          ))}
        </div>
        <input id="search" type="search" placeholder="Cari artikel, contoh: distilasi, semen, pompa..." aria-label="Cari artikel" />
      </section>
      <section id="video" className="video-home">
        <div className="video-home-head"><h2>Video terbaru</h2><a href="/video/">Lihat semua video &rarr;</a></div>
        <p className="video-home-sub">Setiap video @ilmutekkim disertai artikel pendamping yang mendalam. Pilih kartu untuk menonton beserta penjelasan lengkapnya.</p>
        <div className="grid video-grid">
          {home.videos.map((card) => <HomeCard card={card} video key={card.slug} />)}
        </div>
      </section>
      <section id="artikel" className="grid">
        {home.articles.map((card) => <HomeCard card={card} key={card.slug} />)}
      </section>
      <p id="no-result" hidden>Tidak ditemukan artikel yang sesuai. Silakan gunakan kata kunci lain.</p>
      <HomeInteractions />
    </main>
  );
}
