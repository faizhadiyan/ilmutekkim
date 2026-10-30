import KamusLevels from "@/components/KamusLevels";
import { fondasiNames, sectorsBySlug, termsBySlug } from "@/lib/kamus";

export function BasicKamusTerm({ term }) {
  return (
    <>
      <div className="crumbs"><a href="/kamus/">Kamus</a> › Entri Dasar › {term.term}</div>
      <div className="termhead"><h1>{term.term}</h1>
        <div className="badges"><span className="badge ver">Entri glosarium</span>{"\n"}
          <span className="badge fon">Entri dasar</span></div>
      </div>
      <div className="l0"><h2>Definisi</h2><p>{term.definisi}</p></div>
      <section className="layer"><h2>Status Kedalaman</h2>
        <p><strong>Entri dasar — bedah dalam (mekanisme, persamaan, sensitivitas) menyusul.</strong></p>
        <p>Entri ini dipertahankan sebagai definisi awal dalam kamus gabungan agar istilah dan bacaan terkaitnya tetap dapat ditemukan. Statusnya tidak disamakan dengan entri dalam yang telah melalui gate kedalaman Kamus Industri Kimia.</p>
      </section>
      <section className="blk"><h2>Bacaan Terkait</h2>
        {term.terkait.length ? term.terkait.map((link, index) => (
          <a className="sresult" href={link.url} key={index}><span className="t">{link.label}</span>
            <div className="snip">{link.type_label} terkait dengan istilah ini</div>
          </a>
        )) : <p className="lead">Belum ada bacaan terkait yang terhubung ke entri ini.</p>}
      </section>
      <section className="blk"><p><a className="chip" href="/kamus/#semua-istilah">Lihat semua istilah A–Z</a></p></section>
    </>
  );
}

export function DeepKamusTerm({ term }) {
  const foundation = fondasiNames[term.fondasi] || "";
  return (
    <>
      <div className="crumbs"><a href="/kamus/">Kamus</a> › {foundation} › {term.term}</div>
      <div className="termhead"><h1>{term.term}</h1>
        <div className="badges"><span className="badge ver">Glosarium terverifikasi</span>{"\n"}
          <span className="badge fon">{foundation}</span>{term.sectors.map((slug) => (
            <a className="badge sec" href={`/kamus/sektor/${slug}/`} key={slug}>{sectorsBySlug[slug].nama}</a>
          ))}</div>
      </div>
      <div className="l0"><h2>Definisi</h2><p>{term.definisi}</p>
        <div className="analogi"><strong>Analogi:</strong> {term.analogi}</div>
      </div>
      <div className="seg" role="tablist" aria-label="Level kedalaman">
        <button type="button" data-lv="awam">Awam</button>{"\n"}
        <button type="button" data-lv="tekkim" className="on">Tekkim</button>{"\n"}
        <button type="button" data-lv="plant">Plant</button>{"\n"}
        <button type="button" data-lv="semua">Semua</button>
      </div>
      <p className="note">Pilih level kedalaman: Awam menampilkan lapis inti konsep pada kedalaman pengantar,{"\n"}
        Tekkim menampilkan lapis mekanisme dan persamaan, Plant menampilkan lapis penerapan di pabrik.{"\n"}
        Definisi selalu ditampilkan pada setiap level.</p>
      <section className="layer" data-layer="tekkim"><h2>Lapis Tekkim — Mekanisme dan Prinsip</h2>
        <h3>Mekanisme</h3><p>{term.mekanisme}</p>
        <h3>Prinsip dan Persamaan Kunci</h3><p>{term.prinsip}</p>
        {term.persamaan.map((equation, index) => (
          <div className="eq" key={index}>
            {/* The source data intentionally contains entities and subscript HTML. */}
            <div className="rumus" dangerouslySetInnerHTML={{ __html: equation.rumus }} />
            <div className="simbol">{equation.simbol}</div>
            <div className="asumsi">Asumsi: {equation.asumsi}</div>
          </div>
        ))}
        <h3>Variabel Operasi dan Sensitivitas</h3>
        <p className="note">Seluruh rentang adalah rentang umum textbook, bukan data plant.</p>
        <table className="sens"><thead><tr><th>Variabel</th><th>Rentang Umum</th><th>Arah Perubahan</th><th>Efek dan Alasannya</th></tr></thead>
          <tbody>{term.variabel.map((variable, index) => (
            <tr key={index}><td><strong>{variable.nama}</strong></td><td>{variable.rentang}</td>
              <td>{variable.arah === "naik" ? <span className="up">↑ naik</span> : <span className="down">↓ turun</span>}</td><td>{variable.efek}</td></tr>
          ))}</tbody>
        </table>
        <h3>Batas Operasi dan Mode Kegagalan</h3><ul className="tight">{term.kegagalan.map((item, index) => <li key={index}>{item}</li>)}</ul>
      </section>
      <section className="layer" data-layer="plant"><h2>Lapis Plant — Biaya, Diagnosis, dan Contoh</h2>
        <h3>Pendorong Biaya dan Efisiensi</h3><ul className="tight">{term.plant.biaya.map((item, index) => <li key={index}>{item}</li>)}</ul>
        <h3>Daftar Periksa Diagnosis Sebab-Akibat</h3>
        <table className="sens check"><thead><tr><th>Gejala</th><th>Penyebab yang Mungkin</th><th>Tindakan Pemeriksaan</th></tr></thead>
          <tbody>{term.plant.checklist.map((item, index) => (
            <tr key={index}><td>{item.gejala}</td><td>{item.penyebab}</td><td>{item.tindakan}</td></tr>
          ))}</tbody>
        </table>
        <div className="contoh"><strong>Contoh hitungan (angka textbook):</strong> {term.plant.contoh}</div>
      </section>
      <section className="layer" data-layer="awam"><h2>Mulai dari Sini</h2>
        <p>Untuk pembaca yang baru pertama kali menemui istilah ini, definisi dan analogi pada bagian atas{"\n"}
          halaman adalah ringkasan yang memadai. Lapis Tekkim menambahkan mekanisme, persamaan, dan variabel{"\n"}
          yang menentukan perilaku konsep ini, sedangkan Lapis Plant menunjukkan penerapannya pada operasi pabrik.</p>
      </section>
      <section className="blk"><h2>Istilah Terkait</h2><div className="chips">{term.terkait.map((slug) => (
        <a className="chip" href={`/kamus/istilah/${slug}/`} key={slug}>{termsBySlug[slug].term}</a>
      ))}</div></section>
      <section className="blk refs"><h2>Referensi</h2><ul className="tight">{term.referensi.map((item, index) => <li key={index}>{item}</li>)}</ul>
        <p>Terakhir diperbarui: {term.updated} · Sumber entri: Glosarium terverifikasi IlmuTekkim.{"\n"}
          Seluruh angka adalah rentang umum textbook, bukan data plant.</p>
      </section>
      <KamusLevels slug={term.slug} />
    </>
  );
}
