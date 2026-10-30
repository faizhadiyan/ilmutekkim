import { notFound } from "next/navigation";
import { research, staticPageMetadata } from "@/lib/staticPages";
import ResearchPost from "@/components/ResearchPost";

export const dynamic = "force-static";
export const dynamicParams = false;
export function generateStaticParams() {
  return research.map(({ slug }) => ({ slug }));
}
export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!research.some((item) => item.slug === slug)) notFound();
  return staticPageMetadata(`/riset/${slug}`);
}
export default async function Page({ params }) {
  const { slug } = await params;
  const item = research.find((record) => record.slug === slug);
  if (!item) notFound();
  return <ResearchPost item={item} items={research} />;
}
