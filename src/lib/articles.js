import manifest from "@/data/articles/manifest.json";
import sources from "@/data/articles/sources";
import { articleFigures, captionParagraphs, cleanText, mergeReferences, resolveImage, titleCase } from "@/lib/content";

// Array.sort is stable: dates that tie retain the ARTICLES order in build.py.
export const articles = [...manifest].sort((a, b) => b.date.localeCompare(a.date));

export function getArticle(slug) {
  const record = articles.find((article) => article.slug === slug);
  if (!record) return null;
  const { spec, deep } = sources[slug];
  const refs = (spec?.references || []).map(cleanText).filter(Boolean);
  return {
    ...record, spec, deep,
    series: spec ? titleCase(cleanText(spec.series_label || "Teknik Kimia")) : record.legacyFallback.series,
    cover: spec ? resolveImage(spec.cover_photo || spec.cover_image, slug, "cover", record.images) : null,
    lead: captionParagraphs(spec?.caption),
    deepLead: cleanText(deep?.lead || ""),
    sub: cleanText(spec?.cover_sub || ""),
    credit: cleanText(spec?.cover_credit || ""),
    creditUrl: spec?.credit_url || spec?.cover_credit_url || "",
    refs: spec ? (deep ? mergeReferences(deep.refs, refs) : refs) : record.legacyFallback.refs,
    figures: spec ? articleFigures(spec, slug, record.images) : [],
  };
}
