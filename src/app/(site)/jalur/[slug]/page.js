import { notFound } from "next/navigation";
import { learningPaths, staticPageMetadata } from "@/lib/staticPages";
import LearningPath from "@/components/LearningPath";

export const dynamic = "force-static";
export const dynamicParams = false;
export function generateStaticParams() {
  return learningPaths.map(({ slug }) => ({ slug }));
}
export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!learningPaths.some((path) => path.slug === slug)) notFound();
  return staticPageMetadata(`/jalur/${slug}`);
}
export default async function Page({ params }) {
  const { slug } = await params;
  const path = learningPaths.find((record) => record.slug === slug);
  if (!path) notFound();
  return <LearningPath path={path} />;
}
