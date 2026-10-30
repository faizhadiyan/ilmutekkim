import { Fragment } from "react";
import { formatTime, indonesianDate } from "@/lib/content";
import { PostNavigation, References } from "@/components/ArticleParts";
import VideoInteractions from "@/components/VideoInteractions";

export function VideoArticleBody({ article, sectionStarts }) {
  return <section className="article-body">{article.sections.map((section, i) => {
    const timed = section.t !== null && section.t !== undefined;
    const start = sectionStarts?.[i] ?? String(section.t);
    return <Fragment key={i}>
      <h2 className="art-h" data-start={timed ? start : undefined}>{section.h}{timed && <> <button className="seek" type="button" data-start={start} title="Lompat ke bagian ini di video">▶ {formatTime(section.t)}</button></>}</h2>
      {section.paras.map((p, j) => <p key={j}>{p}</p>)}
    </Fragment>;
  })}</section>;
}

export default function VideoPost({ video: v, videos, index }) {
  // React removes src="". Preserve the old empty source on the two videos
  // whose production resolver returned no file; this HTML contains no input.
  const source = v.video_url ? {
    children: <><source src={v.video_url} type="video/mp4" />Browser tidak mendukung video.</>,
  } : {
    dangerouslySetInnerHTML: { __html: '<source src="" type="video/mp4">Browser tidak mendukung video.' },
  };
  return <main><article className="post video-post">
    <p className="eyebrow">Video interaktif · {v.tag}</p>
    <h1>{v.title}</h1>
    <p className="meta">{indonesianDate(v.date)} · {formatTime(v.duration)}</p>
    <p className="ig-link">Versi Reel: <a href={v.ig} target="_blank" rel="noopener">tonton di Instagram @ilmutekkim</a></p>
    <p className="lead">{v.article.lead || v.hook}</p>
    <div className="player-wrap">
      <video id="vplayer" controls playsInline preload="metadata" poster={v.poster_url || undefined} {...source} />
      <div className="player-bar"><span id="vnow">0:00</span><div className="track"><div id="vprog" /></div><span>{formatTime(v.duration)}</span></div>
      <p className="player-hint">Klik tombol ▶ di judul bagian artikel untuk lompat ke detiknya di video. Bagian yang sedang diputar akan menyala.</p>
    </div>
    <VideoArticleBody article={v.article} sectionStarts={v.sectionStarts} />
    {v.facts?.length > 0 && <section className="factbox"><h2>Fakta kunci</h2><ul>{v.facts.map((fact, i) => <li key={i}>{fact}</li>)}</ul></section>}
    <section><h2>Kesimpulannya</h2><p>{v.takeaway}</p></section>
    <References refs={v.article.refs || []} ordered />
    <section className="quiz"><h2>Cek paham (interaktif)</h2><p>{v.quiz.q}</p>
      <div className="quiz-opts">{v.quiz.options.map((option, i) => <button type="button" className="quiz-opt" data-ok={i === v.quiz.answer ? "1" : "0"} key={i}>{option}</button>)}</div>
      <p className="quiz-explain" hidden>{v.quiz.explain}</p>
    </section>
    <div className="cta-box"><h2>Tonton versi Reel-nya</h2>
      <p>Tonton versi singkatnya sebagai Reel di Instagram, atau baca versi lengkapnya di sini sambil lompat ke detik yang mau diulang.</p>
      <a className="btn" href={v.ig} target="_blank" rel="noopener">Buka Reel @ilmutekkim</a>{" "}
      <a className="btn ghost" href="/video/">Semua video</a>
    </div>
    <PostNavigation items={videos} index={index} type="video" />
    <VideoInteractions slug={v.slug} />
  </article></main>;
}
