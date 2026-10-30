export function ArticleFigure({ figure, hero = false }) {
  const { url, credit, creditUrl, head } = figure;
  return (
    <figure className={hero ? "hero-img" : undefined}>
      <img src={url} alt={head} loading={hero ? undefined : "lazy"} />
      {credit && <figcaption>Foto: {creditUrl
        ? <a href={creditUrl} rel="noopener" target="_blank">{credit}</a>
        : credit}</figcaption>}
    </figure>
  );
}

export function References({ refs, ordered = false }) {
  if (!refs.length) return null;
  const List = ordered ? "ol" : "ul";
  return <section className="refs"><h2>Referensi</h2><List>{refs.map((ref, i) => <li key={i}>{ref}</li>)}</List></section>;
}

export function PostNavigation({ items, index, type }) {
  const previous = items[index + 1];
  const next = items[index - 1];
  return <nav className="post-nav">
    {previous && <a href={`/${type}/${previous.slug}/`}>← {previous.title}</a>}
    {next && <a href={`/${type}/${next.slug}/`}>{next.title} →</a>}
  </nav>;
}
