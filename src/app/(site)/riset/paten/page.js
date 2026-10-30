import { patents, staticPageMetadata } from "@/lib/staticPages";
import PatentIntro from "@/components/PatentIntro";
import ResearchIndex from "@/components/ResearchIndex";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/riset/paten");

export default function Page() {
  return <main><PatentIntro /><ResearchIndex items={patents} patent /></main>;
}
