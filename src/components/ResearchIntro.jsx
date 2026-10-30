import { research, patents } from "@/lib/staticPages";

// Literal copy from _old/riset/index.html.
export default function ResearchIntro() {
  return <>
    <article className="post wide">
      <p className="eyebrow">{"Riset"}</p>
      <h1>{"Bedah paper jurnal: dari masalah sampai kesimpulan."}</h1>
      <p className="lead">{"Setiap bedah di halaman ini ditulis dari abstrak paper yang terverifikasi: permasalahan yang dikaji, metode yang digunakan, angka temuan persis sebagaimana tertulis, batas keberlakuannya, serta implikasinya bagi praktik industri. Setiap bedah ditutup dengan kesimpulan yang eksplisit: paper tersebut perlu dibaca penuh, atau abstraknya dinilai telah memadai."}</p>
      <p className="meta">{research.length}{" bedah jurnal · campuran internasional dan Indonesia · standar bedah: angka hanya dari abstrak, abstrak tidak disalin, selalu ada catatan kritis"}</p>
    </article>
    <section className="post wide tight">
      <h2>{"Rak bedah paten"}</h2>
      <p>{"Paten adalah dokumen teknologi yang terbuka: paten kedaluwarsa berarti teknologi yang bebas dipelajari dan dipakai sebagai titik awal, paten aktif berarti peta arah pemegangnya. Di rak ini paten klasik teknik kimia dibedah dengan standar yang sama: nomor, inventor, dan tanggal diverifikasi dari dokumen aslinya, klaimnya diparafrase, dan statusnya ditulis apa adanya. Saat ini ada "}{patents.length}{" bedah paten."}</p>
      <p>
        <a className="btn" href="/riset/paten/">{"Buka rak bedah paten"}</a>
      </p>
    </section>
    </>;
}
