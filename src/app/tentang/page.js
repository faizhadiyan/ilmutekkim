import { staticPageMetadata } from "@/lib/staticPages";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/tentang");

export default function Page() {
  return (
    <main>
      <article className="post narrow">
        <p className="eyebrow">{"Tentang"}</p>
        <h1>{"Tentang ilmutekkim."}</h1>
        <p className="lead">{"ilmutekkim adalah media pembelajaran teknik kimia dari sudut pandang praktisi pabrik:\nbukan hafalan rumus, melainkan bagaimana proses sesungguhnya beroperasi di lapangan."}</p>
        <p>
          {"Setiap artikel di situs ini merupakan versi baca dari carousel Instagram\n"}
          <a href="https://www.instagram.com/ilmutekkim" target="_blank" rel="noopener">{"@ilmutekkim"}</a>
          {":\nsatu topik ditelaah mulai dari kesalahpahaman yang paling sering beredar, kenyataan prosesnya,\ndiagram alurnya, hingga contoh penerapannya di industri Indonesia."}
        </p>
        <p>
          {"Setiap "}
          <a href="/video/">{"video"}</a>
          {" merupakan versi tonton dari konten @ilmutekkim:\npengunjung dapat menonton sambil membaca artikel lengkapnya, melompat ke detik tertentu\ndari judul bagiannya, kemudian memeriksa pemahaman melalui kuis singkat."}
        </p>
        <h2>{"Yang dibahas"}</h2>
        <ul>
          <li>{"Unit operasi: distilasi, heat exchanger, pompa, kompresor, cooling tower."}</li>
          <li>{"Alur pabrik Indonesia: kelapa sawit, kilang, petrokimia, pupuk, gula, semen, pulp dan kertas."}</li>
          <li>{"Keselamatan proses: relief valve, safety instrumented system, permit to work."}</li>
          <li>{"Dasar yang kerap lemah: neraca massa, pembacaan P&ID, mode batch versus kontinu."}</li>
        </ul>
        <h2>{"Alasan versi situs web"}</h2>
        <p>{"Carousel mudah disimpan, tetapi sukar ditemukan kembali. Di situs ini seluruh artikel dapat ditelusuri,\ndibaca secara utuh tanpa menggeser slide, dan ditemukan melalui mesin pencari. Konten terbaru tetap diterbitkan\nterlebih dahulu di Instagram setiap hari."}</p>
        <div className="cta-box">
          <h2>{"Titik awal yang disarankan"}</h2>
          <p>
            {"Pembaca baru disarankan memulai dari "}
            <a href="/artikel/distilasi-bertingkat-minyak-mentah/">{"distilasi bertingkat"}</a>
            {",\nkemudian "}
            <a href="/artikel/baca-pid-lima-simbol-pabrik/">{"pembacaan P&ID"}</a>
            {"."}
          </p>
          <a className="btn" href="/#artikel">{"Lihat semua artikel"}</a>
        </div>
      </article>
    </main>
    );
}
