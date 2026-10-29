// POST /api/ask — proxy AI untuk chatbot Tanya Tekkim (Kamus IlmuTekkim).
// Vercel serverless function, Node, tanpa dependensi (global fetch).
// Body: { question: string, level: "awam" | "tekkim" | "plant" }
// Tanpa DEEPSEEK_API_KEY -> 503 { error: "ai_not_configured" } agar
// antarmuka dapat menurun dengan anggun (glosarium lokal tetap bekerja).

const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 20;
const MAX_QUESTION = 500;
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

  const key = process.env.DEEPSEEK_API_KEY;
  if (!key) { res.status(503).json({ error: "ai_not_configured" }); return; }

  try {
    const r = await fetch("https://api.deepseek.com/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + key },
      body: JSON.stringify({
        model: "deepseek-flash",
        messages: [
          { role: "system", content: SYSTEM_PROMPT + " " + LEVEL_INSTRUCTION[level] },
          { role: "user", content: question },
        ],
        max_tokens: 900,
        temperature: 0.3,
        // Upaya menonaktifkan/menurunkan mode berpikir apabila didukung API;
        // parameter yang tidak dikenal dapat ditolak penyedia — lihat catatan
        // pada penanganan kegagalan.
        thinking: { type: "disabled" },
      }),
    });
    if (!r.ok) {
      res.status(502).json({ error: "ai_upstream_error", status: r.status });
      return;
    }
    const data = await r.json();
    const answer = data && data.choices && data.choices[0] && data.choices[0].message
      ? (data.choices[0].message.content || "").trim() : "";
    if (!answer) { res.status(502).json({ error: "ai_empty_answer" }); return; }
    res.status(200).json({ answer, source: "ai", verified: false, model: "deepseek-flash", level });
  } catch (e) {
    res.status(502).json({ error: "ai_unreachable" });
  }
};
