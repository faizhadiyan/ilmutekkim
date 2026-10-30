// Server component: every card, including hidden older videos, is in the initial HTML.
export default function HomeCard({ card, video = false }) {
  return (
    <article
      className={video ? `card vcard${card.extra ? " v-extra" : ""}` : "card"}
      data-series={card.series}
      style={video && card.extra ? { display: "none" } : undefined}
      data-title={card.searchTitle}
    >
      <a href={card.href}>
        {card.image
          ? <img src={card.image} alt={card.title} loading="lazy" />
          : <div className="no-img">ilmutekkim</div>}
        {video && <span className="play-badge">{`▶ ${card.duration}`}</span>}
      </a>
      <div className="card-body">
        <p className="eyebrow">{card.label}{card.badge && <> <span className="badge">{card.badge}</span></>}</p>
        <h3><a href={card.href}>{card.title}</a></h3>
        <p>{card.excerpt}</p>
        <p className="meta">{card.date}{video && " · tonton + baca artikelnya"}</p>
      </div>
    </article>
  );
}
