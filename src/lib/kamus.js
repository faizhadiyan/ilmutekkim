import deepTerms from "@/data/kamus/terms.json";
import basicTerms from "@/data/kamus/basic-terms.json";
import catalog from "@/data/kamus/sectors.json";
import pages from "@/data/kamus/page-metadata.json";

export { deepTerms, basicTerms };
export const { sectors, fondasi, sector_terms: sectorTerms } = catalog;
export const terms = [...deepTerms, ...basicTerms];
export const termsBySlug = Object.fromEntries(terms.map((term) => [term.slug, term]));
export const sectorsBySlug = Object.fromEntries(sectors.map((sector) => [sector.slug, sector]));
export const fondasiNames = Object.fromEntries(fondasi.map((item) => [item.slug, item.nama]));

// Python's source catalog sorts lowercase strings by code point, not locale.
export const alphabeticalTerms = [...terms].sort((a, b) => {
  const left = a.term.toLowerCase();
  const right = b.term.toLowerCase();
  return left < right ? -1 : left > right ? 1 : 0;
});

export function kamusMetadata(path) {
  const page = pages[path];
  return {
    title: { absolute: page.title },
    description: page.description,
    alternates: { canonical: page.canonical },
    // Legacy Kamus heads have no OG tags; clear the root homepage's defaults.
    openGraph: null,
  };
}

// Match Python string slicing for the catalog's snippets.
export function excerpt(text, length) {
  return Array.from(text).slice(0, length).join("");
}
