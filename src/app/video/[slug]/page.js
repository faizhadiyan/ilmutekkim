import { notFound } from "next/navigation";
import VideoPost from "@/components/VideoPost";
import { getVideo, videos } from "@/lib/videos";
import { pageMetadata } from "@/lib/pageMetadata";

export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  return videos.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  if (!getVideo(slug)) notFound();
  return pageMetadata(`/video/${slug}`);
}

export default async function VideoPage({ params }) {
  const { slug } = await params;
  const video = getVideo(slug);
  if (!video) notFound();
  return <VideoPost video={video} videos={videos} index={videos.findIndex((v) => v.slug === slug)} />;
}
