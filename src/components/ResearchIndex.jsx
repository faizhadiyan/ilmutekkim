import { staticCover } from "@/lib/staticPages";
import ResearchFilters from "@/components/ResearchFilters";

export default function ResearchIndex({ items, patent = false }) {
  const base = patent ? "/riset/paten" : "/riset";
  const topics = [...new Set(items.map((item) => item.topik))].sort();
  return <>
    <section id="seri" className="series-bar">
      <h2>Telusuri menurut topik</h2>
      <div className="chips"><button className="chip active" data-series="all">Semua</button>{topics.map((topic) => <button key={topic} className="chip" data-series={topic}>{topic}</button>)}</div>
      <input id="search" type="search" placeholder={patent ? "Cari paten, contoh: PSA, membran, MTG..." : "Cari bedah, contoh: hidrogen, katalis, pirolisis..."} aria-label={patent ? "Cari bedah paten" : "Cari bedah riset"} />
    </section>
    <section id="artikel" className="grid">{items.map((d) => {
      const cover = staticCover(`${base}/${d.slug}`, d);
      const url = `${base}/${d.slug}/`;
      return <article key={d.slug} className="card" data-series={d.topik} data-title={`${d.judul.toLowerCase()} ${d.topik.toLowerCase()} ${(patent ? d.nomor : d.journal).toLowerCase()}`}>
        <a href={url}>{cover ? <img src={cover} alt={d.judul} loading="lazy" /> : <div className="no-img">{patent ? "Bedah Paten" : "Bedah Riset"}</div>}</a>
        <div className="card-body"><p className="eyebrow">{d.topik} · {patent ? d.nomor : d.negara}</p>
          <h3><a href={url}>{d.judul}</a></h3><p>{d.lead}</p>
          <p className="meta">{patent ? `Terbit ${d.terbit} · Kesimpulan: ${d.kesimpulan}` : `${d.journal} · ${d.year} · Kesimpulan: ${d.vonis}`}</p>
        </div>
      </article>;
    })}</section>
    <p id="no-result" hidden>Tidak ditemukan bedah yang sesuai. Silakan gunakan kata kunci lain.</p>
    <ResearchFilters scope={base} />
  </>;
}
