import records from "@/data/videos.json";
import readingArticles from "@/data/video-articles.json";
import assets from "@/data/video-assets.json";

// Preserve the original resolver results, including missing videos/posters.
export const videos = [...records].sort((a, b) => b.date.localeCompare(a.date))
  .map((video) => ({ ...video, ...assets[video.slug], article: readingArticles[video.slug] }));

export function getVideo(slug) {
  return videos.find((video) => video.slug === slug);
}
