import { indonesianDate } from "@/lib/content";
import { BeforeAfterSections, DeepBody, SlideSection } from "@/components/ArticleBody";
import { ArticleFigure, PostNavigation, References } from "@/components/ArticleParts";

export default function ArticlePost({ article: a, articles, index }) {
  return <main><article className="post">
    <p className="eyebrow">{a.series}</p>
    <h1>{a.title}</h1>
    <p className="meta">{indonesianDate(a.date)} · ilmutekkim{a.status === "arsip" && " · arsip produksi"}</p>
    {a.ig && <p className="ig-link">Versi carousel: <a href={a.ig} target="_blank" rel="noopener">lihat di Instagram @ilmutekkim</a></p>}
    {a.cover && <ArticleFigure hero figure={{ url: a.cover, credit: a.credit, creditUrl: a.creditUrl, head: a.title }} />}
    {a.deepLead ? <p className="lead">{a.deepLead}</p> : <>
      {a.sub && <p className="lead">{a.sub}</p>}
      {a.lead.slice(0, 2).map((p, i) => <p className="intro" key={i}>{p}</p>)}
    </>}
    {a.deep ? <DeepBody deep={a.deep} figures={a.figures} />
      : a.spec.format === "before_after" ? <BeforeAfterSections spec={a.spec} />
        : (a.spec.slides || []).map((slide, i) => <SlideSection slide={slide} slug={a.slug} index={i + 1} images={a.images} key={i} />)}
    <References refs={a.refs} />
    <PostNavigation items={articles} index={index} type="artikel" />
    <div className="cta-box"><h2>Lanjut baca di Instagram</h2>
      <p>Konten teknik kimia tiap hari: proses pabrik, safety, dan cara baca alat. Ditulis insinyur kimia ITB.</p>
      <a className="btn" href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">Follow @ilmutekkim</a>
    </div>
  </article></main>;
}
