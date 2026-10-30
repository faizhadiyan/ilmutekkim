import { staticPageMetadata } from "@/lib/staticPages";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/glosarium");

export default function Page() {
  return (
    <>
      <meta httpEquiv="refresh" content="0; url=/kamus" />
      <main>
        <article className="post wide">
          <p className="eyebrow">{"Kamus"}</p>
          <h1>{"Kamus Industri Kimia IlmuTekkim"}</h1>
          <p className="lead">{"Glosarium telah digabungkan ke dalam Kamus Industri Kimia. Anda akan dialihkan secara otomatis ke satu-satunya kamus di situs ini."}</p>
          <p>
            {"Jika pengalihan tidak berjalan, "}
            <a href="/kamus">{"buka Kamus Industri Kimia"}</a>
            {"."}
          </p>
        </article>
      </main>
    </>
    );
}
