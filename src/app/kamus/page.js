import KamusShell from "@/components/KamusShell";
import KamusTermCard from "@/components/KamusTermCard";
import KamusSearch from "@/components/KamusSearch";
import { alphabeticalTerms, basicTerms, deepTerms, fondasi, kamusMetadata, sectors, sectorTerms } from "@/lib/kamus";

export const dynamic = "force-static";
export const metadata = kamusMetadata("/kamus");

export default function KamusPage() {
  const count = deepTerms.length + basicTerms.length;
  return (
    <KamusShell>
      <div className="hero">
        <h1>Kamus Industri Kimia</h1>
        <p className="sub">Kamus proses teknik kimia untuk seluruh industri kimia Indonesia: istilah, mekanisme,{"\n"}
          persamaan kunci, variabel operasi, dan bedah plant — disusun per sektor industri dan per fondasi keilmuan,{"\n"}
          dengan kedalaman teknik kimia sebagai standar entri utamanya.</p>
        <p className="lead">{count} istilah tersedia: {deepTerms.length} entri dalam dan {basicTerms.length} entri dasar.</p>
        <form className="searchbox" id="search-form" role="search">
          <input id="kamus-search" type="search" autoComplete="off" placeholder="Cari istilah: reflux, FFA, steam cracking, kavitasi…  (tekan / untuk fokus)" />
          <button type="submit">Cari</button>
        </form>
        <div id="search-results" aria-live="polite" />
      </div>
      <section className="blk"><h2>Sektor Industri</h2>
        <p className="lead">Setiap sektor menyajikan alur proses ujung ke ujung; setiap simpul alur tertaut ke entri istilahnya.</p>
        <div className="grid">{sectors.map((sector) => (
          <div className="card" key={sector.slug}>
            <h3><a href={`/kamus/sektor/${sector.slug}/`}>{sector.nama}</a></h3>
            <p>{sector.tagline}</p><span className="count">{(sectorTerms[sector.slug] || []).length} istilah terkait</span>
          </div>
        ))}</div>
      </section>
      <section className="blk"><h2>Fondasi Teknik Kimia</h2>
        <p className="lead">Istilah fondasi berlaku lintas sektor dan menjadi rumah kanonis setiap konsep.</p>
        <div className="chips">{fondasi.map((item) => (
          <a className="chip" href={`#fondasi-${item.slug}`} key={item.slug}>{item.nama} <b>{deepTerms.filter((term) => term.fondasi === item.slug).length}</b></a>
        ))}</div>
      </section>
      <section className="blk"><h2>Istilah Populer</h2>{deepTerms.filter((term) => term.populer).map((term) => <KamusTermCard key={term.slug} term={term} />)}</section>
      <section className="blk" id="semua-istilah"><h2>Semua Istilah A–Z ({count})</h2>
        <p className="lead">Daftar lengkap kamus gabungan. Entri dalam memuat mekanisme, persamaan, sensitivitas, dan bedah plant; entri dasar memuat definisi serta bacaan terkait dan akan diperdalam secara bertahap.</p>
        {alphabeticalTerms.map((term) => <KamusTermCard key={term.slug} term={term} />)}
      </section>
      {fondasi.map((item) => {
        const items = deepTerms.filter((term) => term.fondasi === item.slug);
        return items.length ? (
          <section className="blk" id={`fondasi-${item.slug}`} key={item.slug}>
            <h2>{item.nama}</h2>{items.map((term) => <KamusTermCard key={term.slug} term={term} />)}
          </section>
        ) : null;
      })}
      <KamusSearch />
    </KamusShell>
  );
}
