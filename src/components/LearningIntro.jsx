import { learningPaths } from "@/lib/staticPages";

// Literal copy from _old/jalur/index.html.
export default function LearningIntro() {
  return <>
    <article className="post wide">
      <p className="eyebrow">{"Jalur belajar"}</p>
      <h1>{"Belajar teknik kimia pakai urutan, bukan acak."}</h1>
      <p className="lead">{"Artikel yang baik sekalipun sulit diikuti apabila dibaca tanpa urutan konseptual. Halaman ini menyusun bacaan ilmutekkim menjadi "}{learningPaths.length}{" jalur belajar: setiap jalur merupakan urutan langkah yang disusun secara disengaja, dari konsep yang harus dipahami terlebih dahulu menuju konsep yang prasyaratnya telah terpenuhi. Setiap langkah berupa artikel, video, atau bedah paten yang telah tersedia di situs ini, disertai satu kalimat penjelasan mengenai kedudukannya dalam jalur tersebut."}</p>
      <p className="meta">{learningPaths.length}{" jalur · "}{learningPaths.reduce((sum, path) => sum + path.steps.length, 0)}{" langkah · semua langkah resolve ke konten ilmutekkim"}</p>
    </article>
    </>;
}
