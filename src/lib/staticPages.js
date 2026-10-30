import { research as researchSources, paten as patentSources } from "@/data/static-pages/sources";
import learningSources from "@/data/static-pages/jalur.json";
import glossary from "@/data/static-pages/glosarium.json";
import metadata from "@/data/static-pages/page-metadata.json";
import assets from "@/data/static-pages/assets.json";
import terms from "@/data/kamus/terms.json";
import sectors from "@/data/kamus/sectors.json";
import { articles, getArticle } from "@/lib/articles";
import videos from "@/data/videos.json";

// Python's sorted filenames followed by a stable descending date sort.
function byDate(items) {
  return [...items].sort((a, b) => a.date_bedah < b.date_bedah ? 1 : a.date_bedah > b.date_bedah ? -1 : 0);
}
export const research = byDate(researchSources);
export const patents = byDate(patentSources);
export const learningPaths = learningSources;

export function authorsShort(authors) {
  const names = (authors || []).map(String).filter((name) => name.trim());
  return names.slice(0, 3).join(", ") + (names.length > 3 ? ", dkk." : "");
}

export function staticPageMetadata(path) {
  if (!Object.hasOwn(metadata, path)) return null;
  const page = metadata[path];
  return {
    title: { absolute: page.title },
    description: page.description,
    alternates: { canonical: page.canonical },
    openGraph: { ...page.openGraph },
  };
}

// Reuse the old resolver's observed result, independent of production file access.
export function staticCover(path, item) {
  const url = `/assets/img/${item.slug}/cover.jpg`;
  return item.cover_file && assets[path]?.includes(url) ? url : null;
}

export function resolveLearningLink(step) {
  const { type, slug } = step;
  const item = (type === "artikel" ? articles : type === "video" ? videos : type === "paten" ? patents : [])
    .find((record) => record.slug === slug);
  if (!item) throw new Error(`Tautan jalur tidak dikenal: ${type}/${slug}`);
  return {
    url: `/${type === "paten" ? "riset/paten" : type}/${slug}/`,
    title: type === "paten" ? item.judul : item.title,
  };
}

// load_kamus_catalog: normalize aliases before deduplicating the old glossary.
function kamusKey(value) { return String(value).toLowerCase().replace(/[^a-z0-9]+/g, " ").trim(); }
function kamusSlug(value) { return kamusKey(value).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
export function loadKamusCatalog() {
  const keys = new Set();
  for (const term of terms) {
    for (const value of [term.term || "", term.slug || "", ...(term.aliases || [])]) {
      keys.add(kamusKey(value)); keys.add(kamusSlug(value));
    }
  }
  const basic = glossary.filter((entry) => !keys.has(kamusKey(entry.term)) && !keys.has(kamusSlug(entry.term)))
    .map((entry) => kamusSlug(entry.term));
  return {
    deep_slugs: terms.map((term) => term.slug), dasar_slugs: basic,
    sector_slugs: (sectors.sectors || []).map((sector) => sector.slug), total: terms.length + basic.length,
  };
}

// Reference-library key differs deliberately from merge_refs (ASCII, 60 chars).
export function referenceEntries() {
  const entries = new Map();
  for (const record of articles) {
    for (const ref of getArticle(record.slug).refs) {
      const key = ref.toLowerCase().replace(/[^a-z0-9]+/g, "").slice(0, 60);
      if (!entries.has(key)) entries.set(key, { text: ref, used: [] });
      entries.get(key).used.push({ url: `/artikel/${record.slug}/`, title: record.title });
    }
  }
  // Code point ordering matches Python, without locale-dependent collation.
  return [...entries.values()].sort((a, b) => {
    const x = a.text.toLowerCase(), y = b.text.toLowerCase();
    return x < y ? -1 : x > y ? 1 : 0;
  });
}
