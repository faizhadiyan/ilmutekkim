import { excerpt, fondasiNames } from "@/lib/kamus";

export default function KamusTermCard({ term }) {
  const basic = term.kind === "dasar";
  return (
    <a className="sresult" href={`/kamus/istilah/${term.slug}/`}>
      <span className="t">{term.term}</span>
      {basic ? <> <span className="count">Entri dasar</span></> : null}
      <div className="snip">{`${basic ? "" : `${fondasiNames[term.fondasi] || ""} — `}${excerpt(term.definisi, basic ? 150 : 130)}…`}</div>
    </a>
  );
}
