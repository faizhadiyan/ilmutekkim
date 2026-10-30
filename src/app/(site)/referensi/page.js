import { Fragment } from "react";
import { research, patents, authorsShort, referenceEntries, staticPageMetadata } from "@/lib/staticPages";
import ReferenceIntro from "@/components/ReferenceIntro";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/referensi");

export default function Page() {
  return <main><article className="post"><ReferenceIntro />
    <h2>Buku dan literatur yang dikutip</h2>
    <ol className="refs">{referenceEntries().map((entry, index) => <li key={index}>{entry.text}<br />
      <span className="meta">Dipakai di: {entry.used.slice(0, 3).map((link, i) => <Fragment key={i}>{i > 0 && ", "}<a href={link.url}>{link.title}</a></Fragment>)}{entry.used.length > 3 && `, dan ${entry.used.length - 3} artikel lain`}</span>
    </li>)}</ol>
    <h2>Paper yang dibedah</h2>
    <ol className="refs">{research.map((d) => <li key={d.slug}><a href={`/riset/${d.slug}/`}>{d.paper_title}</a><br />
      <span className="meta">{authorsShort(d.authors)} · {d.journal} · {d.year}</span>
    </li>)}</ol>
    <h2>Paten yang dibedah</h2>
    <ol className="refs">{patents.map((d) => <li key={d.slug}><a href={`/riset/paten/${d.slug}/`}>{d.nomor}: {d.judul_paten}</a><br />
      <span className="meta">{d.pemilik} · terbit {d.terbit}</span>
    </li>)}</ol>
  </article></main>;
}
