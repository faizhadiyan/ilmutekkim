import { notFound } from "next/navigation";
import KamusShell from "@/components/KamusShell";
import { BasicKamusTerm, DeepKamusTerm } from "@/components/KamusTerm";
import { kamusMetadata, terms, termsBySlug } from "@/lib/kamus";

export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  return terms.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!Object.hasOwn(termsBySlug, slug)) notFound();
  return kamusMetadata(`/kamus/istilah/${slug}`);
}

export default async function KamusTermPage({ params }) {
  const { slug } = await params;
  if (!Object.hasOwn(termsBySlug, slug)) notFound();
  const term = termsBySlug[slug];
  return <KamusShell>{term.kind === "dasar" ? <BasicKamusTerm term={term} /> : <DeepKamusTerm term={term} />}</KamusShell>;
}
