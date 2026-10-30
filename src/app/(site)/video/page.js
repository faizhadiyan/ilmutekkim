import { videos } from "@/lib/videos";
import { formatTime, indonesianDate } from "@/lib/content";
import { pageMetadata } from "@/lib/pageMetadata";

export const dynamic = "force-static";
export const metadata = pageMetadata("/video");

export default function VideoIndex() {
  return <main>
    <article className="post wide">
      <p className="eyebrow">Video</p>
      <h1>Video teknik kimia, versi artikel.</h1>
      <p className="lead">Sepuluh video teknik kimia dari @ilmutekkim, masing-masing disertai versi artikel yang lengkap.
Video dapat ditonton bersamaan dengan membaca penjelasan mendalam per subtopik, melompat ke detik tertentu dari judul bagiannya, kemudian menjawab kuis pemeriksa pemahaman.</p>
      <p className="meta">{videos.length} video · tersinkron dari Reel @ilmutekkim · diperbarui {videos.length > 0 ? indonesianDate(videos[0].date) : ""}</p>
    </article>
    <section className="grid video-grid">{videos.map((v) => <article className="card vcard" key={v.slug}>
      <a href={`/video/${v.slug}/`}>{v.poster_url ? <img src={v.poster_url} alt={v.title} loading="lazy" /> : <div className="no-img">ilmutekkim</div>}<span className="play-badge">▶ {formatTime(v.duration)}</span></a>
      <div className="card-body"><p className="eyebrow">{v.tag}</p><h3><a href={`/video/${v.slug}/`}>{v.title}</a></h3><p>{v.hook}</p><p className="meta">{indonesianDate(v.date)} · artikel + kuis</p></div>
    </article>)}</section>
  </main>;
}
