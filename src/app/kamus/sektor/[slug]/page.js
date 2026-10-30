import { Fragment } from "react";
import { notFound } from "next/navigation";
import KamusShell from "@/components/KamusShell";
import KamusTermCard from "@/components/KamusTermCard";
import { kamusMetadata, sectors, sectorsBySlug, sectorTerms, termsBySlug } from "@/lib/kamus";

export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  return sectors.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!Object.hasOwn(sectorsBySlug, slug)) notFound();
  return kamusMetadata(`/kamus/sektor/${slug}`);
}

export default async function KamusSectorPage({ params }) {
  const { slug } = await params;
  if (!Object.hasOwn(sectorsBySlug, slug)) notFound();
  const sector = sectorsBySlug[slug];
  const items = sectorTerms[slug] || [];
  return (
    <KamusShell>
      <div className="crumbs"><a href="/kamus/">Kamus</a> › Sektor › {sector.nama}</div>
      <div className="termhead"><h1>Sektor {sector.nama}</h1></div>
      <p>{sector.deskripsi}</p>
      <section className="blk"><h2>Alur Proses</h2>
        <p className="lead">{sector.aliran} Simpul berwarna cyan dapat diklik menuju entri istilahnya.</p>
        <div className="flow">{sector.flow.map((node, index) => (
          <Fragment key={index}>
            {node.slug && termsBySlug[node.slug] ? <a className="fnode" href={`/kamus/istilah/${node.slug}/`}>{node.label}</a> : <span className="fnode">{node.label}</span>}
            {index < sector.flow.length - 1 ? <span className="farrow">→</span> : null}
          </Fragment>
        ))}</div>
      </section>
      <section className="blk"><h2>Bahan Baku dan Produk</h2>
        <div className="card"><p><strong>Bahan baku:</strong> {sector.bahan}</p>
          <p style={{ marginTop: 8 }}><strong>Produk:</strong> {sector.produk}</p></div>
      </section>
      <section className="blk"><h2>Istilah pada Sektor Ini ({items.length})</h2>{items.map((item) => <KamusTermCard key={item} term={termsBySlug[item]} />)}</section>
    </KamusShell>
  );
}
