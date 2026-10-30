import { Fragment } from "react";
import { authorsShort, staticCover } from "@/lib/staticPages";
import { indonesianDate } from "@/lib/content";

function ListSection({ title, items }) {
  return <section><h2>{title}</h2><ul>{items.map((item, index) => <li key={index}>{item}</li>)}</ul></section>;
}

export default function ResearchPost({ item: d, items, patent = false }) {
  const base = patent ? "/riset/paten" : "/riset";
  const cover = staticCover(`${base}/${d.slug}`, d);
  const index = items.findIndex((item) => item.slug === d.slug);
  const previous = items[index + 1], next = items[index - 1];
  return <main><article className="post">
    <p className="eyebrow">{patent ? `Riset · Paten · ${d.topik}` : `Riset · ${d.topik} · ${d.negara}`}</p>
    <h1>{d.judul}</h1>
    <p className="meta">{indonesianDate(d.date_bedah)} · ilmutekkim</p>
    <p className="cov-label">{d.coverage}</p>
    <p className="lead">{d.lead}</p>
    {cover && <figure><img src={cover} alt={d.judul} /><figcaption>{d.cover_credit || ""}</figcaption></figure>}
    {patent ? <section className="paper-box">
      <p className="eyebrow">Paten yang dibedah</p><h2 className="paper-title">{d.judul_paten}</h2>
      <p>{d.nomor} · Inventor: {d.inventor} · Pemilik saat terbit: {d.pemilik}</p>
      <p>Diajukan {d.diajukan} · Terbit {d.terbit}</p>
      <p><strong>Status:</strong> {d.status}</p>
      <a className="btn ghost" href={d.sumber} target="_blank" rel="noopener">Buka dokumen paten</a>
    </section> : <section className="paper-box">
      <p className="eyebrow">Paper yang dibedah</p><h2 className="paper-title">{d.paper_title}</h2>
      <p>{authorsShort(d.authors)} · {d.journal} · {d.year}</p>
      <a className="btn ghost" href={d.doi} target="_blank" rel="noopener">Buka DOI paper</a>
    </section>}
    <section><h2>Masalah yang diselesaikan</h2><p>{d.masalah}</p></section>
    {patent ? <>
      <section><h2>Klaim inti, dengan kata kami</h2><p className="meta">Klaim paten adalah teks hukum; di bawah ini parafrasenya, bukan salinan.</p><ul>{d.klaim.map((claim, i) => <li key={i}>{claim}</li>)}</ul></section>
      <section><h2>Cara kerjanya</h2><p>{d.cara}</p></section>
    </> : <>
      <section><h2>Metode dan skala</h2><p>{d.metode}</p></section>
      <ListSection title="Temuan kunci" items={d.temuan} />
    </>}
    <ListSection title="Batas dan catatan kritis" items={d.batas} />
    <section><h2>Arti buat pabrik</h2><p>{patent ? d.arti : d.arti_pabrik}</p></section>
    <section className="verdict"><p className="eyebrow">Kesimpulan bedah</p><h2>{patent ? d.kesimpulan : d.vonis}</h2><p>{patent ? d.kesimpulan_alasan : d.vonis_alasan}</p></section>
    {d.terkait?.length > 0 && <section><h2>Baca terkait di ilmutekkim</h2><p>{d.terkait.map((link, i) => <Fragment key={i}><a className="btn ghost" href={`/${link.type === "artikel" ? "artikel" : "video"}/${link.slug}/`}>{link.title}</a>{" "}</Fragment>)}</p></section>}
    <nav className="post-nav">
      {previous && <a href={`${base}/${previous.slug}/`}>← {previous.judul}</a>}
      {next && <a href={`${base}/${next.slug}/`}>{next.judul} →</a>}
    </nav>
    <div className="cta-box"><h2>{patent ? "Semua bedah paten" : "Semua bedah riset"}</h2>
      <p>{patent ? "Bedah paten klasik teknik kimia dari dokumen aslinya, dengan klaim parafrase dan status yang ditulis apa adanya." : "Bedah jurnal teknik kimia internasional dan Indonesia, ditulis dari abstrak terverifikasi dengan catatan kritis dan kesimpulan."}</p>
      <a className="btn" href={`${base}/`}>{patent ? "Ke rak bedah paten" : "Ke halaman riset"}</a>
    </div>
  </article></main>;
}
