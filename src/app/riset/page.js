import { research, staticPageMetadata } from "@/lib/staticPages";
import ResearchIntro from "@/components/ResearchIntro";
import ResearchIndex from "@/components/ResearchIndex";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/riset");

export default function Page() {
  return <main><ResearchIntro /><ResearchIndex items={research} /></main>;
}
