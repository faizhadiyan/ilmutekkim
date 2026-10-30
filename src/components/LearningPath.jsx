import { resolveLearningLink, staticCover } from "@/lib/staticPages";

export default function LearningPath({ path }) {
  const cover = staticCover(`/jalur/${path.slug}`, path);
  const labels = { artikel: "Artikel", video: "Video", paten: "Bedah paten" };
  return <main><article className="post">
    <p className="eyebrow">Jalur belajar</p><h1>{path.judul}</h1>
    <p className="lead">{path.desc}</p><p className="meta">{path.steps.length} langkah · baca berurutan dari atas</p>
    {cover && <figure><img src={cover} alt={path.judul} /><figcaption>{path.cover_credit || ""}</figcaption></figure>}
    {path.steps.map((step, index) => {
      const link = resolveLearningLink(step), number = index + 1;
      return <section key={index} className="stepcard"><p className="eyebrow">Langkah {number} · {labels[step.type]}</p>
        <h2><a href={link.url}>{link.title}</a></h2><p>{step.note}</p>
        <p><a className="btn ghost" href={link.url}>Buka langkah {number}</a></p>
      </section>;
    })}
    <div className="cta-box"><h2>Semua jalur belajar</h2>
      <p>Tujuh jalur terkurasi: dari membaca pabrik untuk pemula sampai tur pabrik Indonesia.</p>
      <a className="btn" href="/jalur/">Ke semua jalur</a>
    </div>
  </article></main>;
}
