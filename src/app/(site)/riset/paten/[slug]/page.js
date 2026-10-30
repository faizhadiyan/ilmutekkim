import { notFound } from "next/navigation";
import { patents, staticPageMetadata } from "@/lib/staticPages";
import ResearchPost from "@/components/ResearchPost";

export const dynamic = "force-static";
export const dynamicParams = false;
export function generateStaticParams() {
  return patents.map(({ slug }) => ({ slug }));
}
export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!patents.some((item) => item.slug === slug)) notFound();
  return staticPageMetadata(`/riset/paten/${slug}`);
}
export default async function Page({ params }) {
  const { slug } = await params;
  const item = patents.find((record) => record.slug === slug);
  if (!item) notFound();
  return <ResearchPost item={item} items={patents} patent />;
}
