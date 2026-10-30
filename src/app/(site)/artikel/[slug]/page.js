import { notFound } from "next/navigation";
import ArticlePost from "@/components/ArticlePost";
import { articles, getArticle } from "@/lib/articles";
import { pageMetadata } from "@/lib/pageMetadata";

export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  return articles.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!getArticle(slug)) notFound();
  return pageMetadata(`/artikel/${slug}`);
}

export default async function ArticlePage({ params }) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();
  return <ArticlePost article={article} articles={articles} index={articles.findIndex((a) => a.slug === slug)} />;
}
