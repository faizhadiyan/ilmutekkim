import { patents } from "@/lib/staticPages";

// Literal copy from _old/riset/paten/index.html.
export default function PatentIntro() {
  return <>
    <article className="post wide">
      <p className="eyebrow">{"Riset · Paten"}</p>
      <h1>{"Bedah paten: baca dokumen teknologinya, bukan rumornya."}</h1>
      <p className="lead">{"Setiap bedah di rak ini ditulis dari dokumen paten aslinya yang terbuka untuk umum: nomor, inventor, pemilik, dan tanggalnya diverifikasi, klaim intinya diparafrase, prinsip kerjanya dijelaskan, batasnya dicatat, dan status hukumnya ditulis sebagaimana tercatat. Paten yang sudah kedaluwarsa adalah dokumen publik: teknologinya bebas dipelajari siapa pun."}</p>
      <p className="meta">{patents.length}{" bedah paten · standar bedah: data hanya dari dokumen paten, klaim diparafrase, status bersumber dan bertanggal akses"}</p>
    </article>
    <section className="post wide tight">
      <h2>{"Rak bedah jurnal"}</h2>
      <p>{"Bedah paper jurnal teknik kimia internasional dan Indonesia ada di halaman riset: masalah, metode, temuan persis dari abstrak, catatan kritis, dan kesimpulan baca."}</p>
      <p>
        <a className="btn" href="/riset/">{"Buka rak bedah jurnal"}</a>
      </p>
    </section>
    </>;
}
