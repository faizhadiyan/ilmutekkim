// POST /api/ask — proxy AI untuk chatbot Tanya Tekkim (Kamus IlmuTekkim).
// Vercel serverless function, Node, tanpa dependensi (global fetch).
// Body: { question: string, level: "awam" | "tekkim" | "plant" }
//
// ROUTER HEURISTIK (keputusan Hadi 2026-10-30, tanpa Jev):
// pertanyaan yang lolos glosarium lokal dinilai kompleksitasnya dengan
// skor aturan lokal (nol panggilan AI, nol biaya, nol latensi tambahan):
//   skor < 4  -> simple  -> Gemini Flash-Lite (GEMINI_API_KEY, free tier)
//   skor >= 4 -> kompleks -> DeepSeek Flash (DEEPSEEK_API_KEY)
// Kegagalan / kunci hilang di satu penyedia -> fallback ke penyedia lain.
// Tanpa kedua kunci -> 503 { error: "ai_not_configured" } agar antarmuka
// dapat menurun dengan anggun (glosarium lokal tetap bekerja).

const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 20;
const MAX_QUESTION = 500;
const COMPLEX_THRESHOLD = 4;
const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-3.5-flash-lite";
const DEEPSEEK_MODEL = "deepseek-flash";
const hits = new Map(); // ip -> [timestamps]

function rateLimited(ip) {
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (arr.length >= MAX_PER_WINDOW) { hits.set(ip, arr); return true; }
  arr.push(now); hits.set(ip, arr);
  return false;
}

const LEVEL_INSTRUCTION = {
  awam: "Jawab ringkas dengan bahasa yang mudah dipahami pembaca awam, gunakan satu analogi apabila membantu.",
  tekkim: "Jawab pada kedalaman mahasiswa teknik kimia: sertakan mekanisme, prinsip atau persamaan kunci yang relevan beserta arti simbolnya.",
  plant: "Jawab pada kedalaman praktisi plant: tekankan variabel operasi, dampak biaya dan efisiensi, serta langkah diagnosis sebab-akibat.",
};

const SYSTEM_PROMPT = [
  "Anda adalah tutor teknik kimia untuk Kamus Industri Kimia IlmuTekkim.",
  "Jawab dalam Bahasa Indonesia yang baku dan profesional.",
  "Susun jawaban secara terstruktur dan ringkas (maksimum sekitar 250 kata).",
  "Nyatakan ketidakpastian secara eksplisit apabila konsepnya tidak pasti atau di luar cakupan teknik kimia proses.",
  "Dilarang mengarang angka spesifik plant atau perusahaan. Apabila menyebut angka, gunakan rentang umum textbook dan labeli secara eksplisit sebagai rentang umum textbook, bukan data plant.",
  "Jangan mengaku sebagai entri glosarium terverifikasi; jawaban ini berstatus bantuan AI.",
].join(" ");

// --- Router heuristik -------------------------------------------------------
// Skor per KELOMPOK sinyal (maksimum per kelompok, sinonim tidak menumpuk).
// Bias disengaja ke kompleks: salah lempar ke DeepSeek hanya rugi biaya
// sangat kecil; salah lempar pertanyaan hitungan/diagnosis ke model ringan
// berisiko jawaban dangkal atau angka ngawur.
const UNIT_RE = /(kg|ton|kj|mj|gcal|kcal|°\s?c|\bkelvin\b|\bbar\b|kpa|mpa|\batm\b|liter|\bm3\b|\bmol\b|rpm|\bkw\b|\bmw\b|%|persen)/;
const GROUPS = [
  { name: "hitung", score: 3, re: /(hitung|kalkulasi|perhitungan|menghitung|estimasi(kan)? kebutuhan)/ },
  { name: "persamaan/mekanisme", score: 3, re: /(persamaan|rumus|derivasi|mekanisme|turunkan rumus|buktikan)/ },
  { name: "mode gagal/gejala", score: 3, re: /(flooding|kavitasi|fouling|water hammer|ledakan|meledak|bocor|kebocoran|merusak|kerusakan|gagal|macet|buntu|tersumbat|lifting|fluktuasi|tidak stabil|overpressure|terbakar)/ },
  { name: "diagnosis", score: 3, re: /(penyebab|mengatasi|mengatasinya|solusi|diagnos|troubleshoot|periksa|gejala| cara cek|kenapa .* (naik|turun|berubah|bergetar|panas|dingin))/ },
  { name: "bandingkan", score: 2, re: /(bandingkan|perbandingan|perbedaan antara|beda antara| versus | vs |lebih baik mana|lebih bagus mana)/ },
  { name: "sebab-akibat", score: 1, re: /(kenapa|mengapa|kok bisa|bagaimana bisa|bagaimana[^?]*\b(merusak|menyebabkan|mengakibatkan|terjadi)\b)/ },
  { name: "detail", score: 1, re: /(secara detail|secara mendalam|langkah-langkah|step by step|secara rinci)/ },
];

function classifyQuestion(question, level) {
  const q = " " + question.toLowerCase() + " ";
  let score = 0;
  const reasons = [];
  const add = (name, pts) => { score += pts; reasons.push(name + "+" + pts); };

  const hasDigit = /\d/.test(q);
  if (hasDigit && UNIT_RE.test(q)) add("angka+satuan", 3);
  else if (hasDigit) add("angka", 2);

  for (const g of GROUPS) if (g.re.test(q)) add(g.name, g.score);

  if (level === "plant") add("level plant", 2);
  else if (level === "tekkim") add("level tekkim", 1);

  if (question.length >= 180) add("panjang>=180", 1);
  if (question.length >= 320) add("panjang>=320", 1);
  if ((question.match(/\?/g) || []).length >= 2) add("multi-pertanyaan", 1);
  if (question.split(/\s+/).length >= 35) add("kata>=35", 1);

  return { route: score >= COMPLEX_THRESHOLD ? "complex" : "simple", score, reasons };
}

// --- Penyedia ---------------------------------------------------------------
async function fetchWithTimeout(url, opts, ms) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms || 20000);
  try { return await fetch(url, Object.assign({}, opts, { signal: c.signal })); }
  finally { clearTimeout(t); }
}

async function askDeepSeek(question, level) {
  const key = process.env.DEEPSEEK_API_KEY;
  if (!key) throw new Error("deepseek_not_configured");
  const r = await fetchWithTimeout("https://api.deepseek.com/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + key },
    body: JSON.stringify({
      model: DEEPSEEK_MODEL,
      messages: [
        { role: "system", content: SYSTEM_PROMPT + " " + LEVEL_INSTRUCTION[level] },
        { role: "user", content: question },
      ],
      max_tokens: 900,
      temperature: 0.3,
      thinking: { type: "disabled" },
    }),
  });
  if (!r.ok) throw new Error("deepseek_upstream_" + r.status);
  const data = await r.json();
  const answer = data && data.choices && data.choices[0] && data.choices[0].message
    ? (data.choices[0].message.content || "").trim() : "";
  if (!answer) throw new Error("deepseek_empty");
  return answer;
}

async function askGemini(question, level) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) throw new Error("gemini_not_configured");
  const prompt = SYSTEM_PROMPT + " " + LEVEL_INSTRUCTION[level] + "\n\nPertanyaan: " + question;
  const r = await fetchWithTimeout(
    "https://generativelanguage.googleapis.com/v1beta/models/" + GEMINI_MODEL + ":generateContent",
    {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.3, maxOutputTokens: 900 },
      }),
    });
  if (!r.ok) throw new Error("gemini_upstream_" + r.status);
  const data = await r.json();
  const parts = data && data.candidates && data.candidates[0] && data.candidates[0].content
    ? (data.candidates[0].content.parts || []) : [];
  const answer = parts.map((p) => p.text || "").join("").trim();
  if (!answer) throw new Error("gemini_empty");
  return answer;
}

// --- Handler ----------------------------------------------------------------
module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "method_not_allowed", message: "Use POST {question, level}" });
    return;
  }
  const ip = (req.headers && (req.headers["x-forwarded-for"] || "")).split(",")[0].trim() || "unknown";
  if (rateLimited(ip)) {
    res.status(429).json({ error: "rate_limited" });
    return;
  }
  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch (e) { body = null; }
  }
  const question = body && typeof body.question === "string" ? body.question.trim() : "";
  const level = body && LEVEL_INSTRUCTION[body.level] ? body.level : "awam";
  if (!question) { res.status(400).json({ error: "question_required" }); return; }
  if (question.length > MAX_QUESTION) { res.status(400).json({ error: "question_too_long", max: MAX_QUESTION }); return; }

  if (!process.env.DEEPSEEK_API_KEY && !process.env.GEMINI_API_KEY) {
    res.status(503).json({ error: "ai_not_configured" });
    return;
  }

  const c = classifyQuestion(question, level);
  const primary = c.route === "complex"
    ? { name: DEEPSEEK_MODEL, fn: askDeepSeek }
    : { name: GEMINI_MODEL, fn: askGemini };
  const secondary = c.route === "complex"
    ? { name: GEMINI_MODEL, fn: askGemini }
    : { name: DEEPSEEK_MODEL, fn: askDeepSeek };

  let lastErr = null;
  for (const p of [primary, secondary]) {
    try {
      const answer = await p.fn(question, level);
      res.status(200).json({
        answer, source: "ai", verified: false, model: p.name, level,
        route: c.route, router: "heuristic", score: c.score, reasons: c.reasons,
        fallback: p.name !== primary.name,
      });
      return;
    } catch (e) { lastErr = e; }
  }
  const msg = lastErr && /_not_configured/.test(lastErr.message || "")
    ? "ai_not_configured" : "ai_upstream_error";
  res.status(msg === "ai_not_configured" ? 503 : 502).json({ error: msg, route: c.route, score: c.score });
};

module.exports.classifyQuestion = classifyQuestion;
