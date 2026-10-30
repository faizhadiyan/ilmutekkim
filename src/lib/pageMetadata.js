import pages from "@/data/page-metadata.json";

export function pageMetadata(path) {
  const page = pages[path];
  return {
    title: { absolute: page.title },
    description: page.description,
    alternates: { canonical: page.canonical },
    openGraph: {
      ...page.openGraph,
      ...(page.images.length ? { images: page.images } : {}),
    },
  };
}
