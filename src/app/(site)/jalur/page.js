import { learningPaths, resolveLearningLink, staticCover, staticPageMetadata } from "@/lib/staticPages";
import LearningIntro from "@/components/LearningIntro";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/jalur");

export default function Page() {
  return <main><LearningIntro /><section className="grid">{learningPaths.map((path) => {
    const cover = staticCover(`/jalur/${path.slug}`, path);
    const first = resolveLearningLink(path.steps[0]);
    const url = `/jalur/${path.slug}/`;
    return <article key={path.slug} className="card"><a href={url}>
      {cover ? <img src={cover} alt={path.judul} loading="lazy" /> : <div className="no-img">Jalur Belajar</div>}
    </a><div className="card-body"><p className="eyebrow">Jalur belajar · {path.steps.length} langkah</p>
      <h3><a href={url}>{path.judul}</a></h3><p>{path.desc}</p>
      <p className="meta"><a href={first.url}>Mulai dari langkah 1 →</a></p>
    </div></article>;
  })}</section></main>;
}
