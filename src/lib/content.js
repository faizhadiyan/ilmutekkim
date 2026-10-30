// Text/date rules from _old/tools/build.py. Keep source prose unedited.
const pythonWhitespace = /[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+/g;
const months = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];

function pythonTruthy(value) {
  if (Array.isArray(value)) return value.length > 0;
  if (value && typeof value === "object") return Object.keys(value).length > 0;
  return Boolean(value);
}

function pythonRepr(value) {
  if (typeof value !== "string") return pythonString(value);
  const quote = value.includes("'") && !value.includes('"') ? '"' : "'";
  const escaped = Array.from(value, (char) => {
    if (char === "\\") return "\\\\";
    if (char === quote) return "\\" + char;
    if (char === "\n") return "\\n";
    if (char === "\r") return "\\r";
    if (char === "\t") return "\\t";
    if (char !== " " && /[\p{C}\p{Z}]/u.test(char)) {
      const code = char.codePointAt(0);
      return code < 256 ? "\\x" + code.toString(16).padStart(2, "0")
        : code < 65536 ? "\\u" + code.toString(16).padStart(4, "0")
          : "\\U" + code.toString(16).padStart(8, "0");
    }
    return char;
  }).join("");
  return quote + escaped + quote;
}

function pythonString(value) {
  if (value === null || value === undefined) return "None";
  if (typeof value === "boolean") return value ? "True" : "False";
  if (Array.isArray(value)) return "[" + value.map(pythonRepr).join(", ") + "]";
  if (typeof value === "object") return "{" + Object.entries(value).map(([key, item]) => pythonRepr(key) + ": " + pythonRepr(item)).join(", ") + "}";
  return String(value);
}

export function cleanText(value) {
  const text = pythonString(pythonTruthy(value) ? value : "");
  return text.replaceAll("—", ", ").replaceAll("--", ", ")
    .replace(pythonWhitespace, " ").replace(/^ | $/g, "");
}

export function captionParagraphs(caption) {
  return String(caption || "").split("\n").map(cleanText)
    .filter((p) => p && !p.startsWith("#") && !p.toLowerCase().startsWith("follow @ilmutekkim"));
}

export function segmentText(segments) {
  return cleanText(Array.isArray(segments)
    ? segments.map((part) => pythonString(Array.isArray(part) ? part[0] : part)).join("")
    : segments);
}

// Python str.title(): a digit or punctuation also starts a new cased run.
export function titleCase(value) {
  let previousCased = false;
  return Array.from(value, (char) => {
    const next = previousCased ? char.toLowerCase() : char.toUpperCase();
    previousCased = char.toLowerCase() !== char.toUpperCase();
    return next;
  }).join("");
}

export function indonesianDate(iso) {
  const [year, month, day] = iso.split("-");
  return `${Number(day)} ${months[Number(month)]} ${year}`;
}

export function formatTime(seconds) {
  const value = Number(seconds || 0);
  let minutes = Math.floor(value / 60);
  const remainder = value % 60 < 0 ? value % 60 + 60 : value % 60;
  const floor = Math.floor(remainder);
  // Python round uses ties to even (e.g. 6.5 → 6, 17.5 → 18).
  let rounded = remainder - floor === 0.5
    ? (floor % 2 === 0 ? floor : floor + 1) : Math.round(remainder);
  if (rounded === 60) { minutes += 1; rounded = 0; }
  return `${minutes}:${String(rounded).padStart(2, "0")}`;
}

function referenceKey(value) {
  return Array.from(String(value).toLowerCase()).filter((char) => /[\p{L}\p{N}]/u.test(char)).slice(0, 40).join("");
}

export function mergeReferences(deepRefs, specRefs) {
  const out = (deepRefs || []).map(cleanText).filter(Boolean);
  const keys = new Set(out.map(referenceKey));
  for (const ref of specRefs || []) {
    const key = referenceKey(ref);
    if (!keys.has(key)) { out.push(ref); keys.add(key); }
  }
  return out;
}

// The old resolver depended on files on the production machine. Freeze its
// observed result from the old HTML; asset deployment belongs to the operator.
export function resolveImage(path, slug, name, images) {
  if (!path) return null;
  const url = `/assets/img/${slug}/${name}.jpg`;
  return images.includes(url) ? url : null;
}

export function slideFigure(slide, slug, index, images, head) {
  for (const [key, name] of [["photo", `foto-${index}`], ["diagram", `diagram-${index}`]]) {
    const url = resolveImage(slide[key], slug, name, images);
    if (url) return { url, credit: slide.credit, creditUrl: slide.credit_url, head };
  }
  return null;
}

export function articleFigures(spec, slug, images) {
  return (spec.slides || []).map((slide, index) =>
    slideFigure(slide, slug, index + 1, images, cleanText(slide.title || ""))).filter(Boolean);
}
