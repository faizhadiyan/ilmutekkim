"use client";

import { useCallback, useEffect, useRef, useState } from "react";

// Format jawaban dan skor pencarian dipertahankan dari chat.js lama.
function esc(s) { return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }

function strongMatch(idx, q) {
  var best = null, bestScore = 0;
  idx.terms.forEach(function (t) {
    var s = 0, tn = norm(t.term);
    if (q === tn) s = 100;
    else if (q.indexOf(tn) >= 0 || tn.indexOf(q) >= 0 && q.length >= 4) s = 85;
    (t.aliases || []).forEach(function (a) {
      var an = norm(a);
      if (an.length >= 3 && q.indexOf(an) >= 0) s = Math.max(s, 88);
    });
    // kecocokan kata kunci judul di dalam pertanyaan panjang
    if (!s) {
      var words = tn.split(/[^a-z0-9]+/).filter(function (w) { return w.length >= 5; });
      var hit = words.filter(function (w) { return q.indexOf(w) >= 0; }).length;
      if (words.length && hit === words.length) s = 70;
    }
    if (s > bestScore) { bestScore = s; best = t; }
  });
  return bestScore >= 70 ? best : null;
}
function entryAnswer(t, level) {
  var body = "";
  if (t.kind === "dasar" || !t.mekanisme) {
    body = "<strong>" + esc(t.term) + ".</strong> " + esc(t.definisi) +
      "<br><em>Entri dasar:</em> bedah dalam (mekanisme, persamaan, sensitivitas) menyusul.";
    return body + '<br><span class="tt-src glos">Sumber: Glosarium terverifikasi · Entri dasar</span>' +
      '<a class="tt-cite" href="/kamus/istilah/' + t.slug + '/">Baca entri lengkap: ' + esc(t.term) + "</a>";
  }
  if (level === "awam") {
    body = "<strong>" + esc(t.term) + ".</strong> " + esc(t.definisi) +
      (t.analogi ? "<br><em>Analogi:</em> " + esc(t.analogi) : "");
  } else if (level === "tekkim") {
    body = "<strong>" + esc(t.term) + " — mekanisme.</strong> " + esc(t.mekanisme) +
      "<br><em>Prinsip:</em> " + esc(t.prinsip);
  } else {
    var biaya = (t.plant.biaya || []).join(" ");
    var cek = (t.plant.checklist && t.plant.checklist[0])
      ? " Contoh diagnosis: gejala “" + esc(t.plant.checklist[0].gejala) + "” umumnya disebabkan " +
        esc(t.plant.checklist[0].penyebab) + "." : "";
    body = "<strong>" + esc(t.term) + " — sudut plant.</strong> " + esc(biaya) + cek;
  }
  var extra = '<br><span class="tt-src glos">Sumber: Glosarium terverifikasi</span>' +
    '<a class="tt-cite" href="/kamus/istilah/' + t.slug + '/">Baca entri lengkap: ' + esc(t.term) + "</a>";
  return body + extra;
}

const examples = [
  "Apa itu FFA dan mengapa penting?",
  "Mengapa kolom distilasi bisa flooding?",
  "Bagaimana kavitasi merusak pompa?",
];

const welcome = "Selamat datang di Tanya Tekkim. Ajukan pertanyaan istilah atau proses teknik kimia. " +
  "Pertanyaan yang tersedia di glosarium akan dijawab dari entri terverifikasi; pertanyaan lain diteruskan ke AI dan dilabeli sebagai belum terverifikasi.";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [level, setLevel] = useState("awam");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [sending, setSending] = useState(false);
  const [scrollRevision, setScrollRevision] = useState(0);
  const inputRef = useRef(null);
  const messagesRef = useRef(null);
  const indexRef = useRef(null);
  const levelRef = useRef("awam");
  const nextMessageId = useRef(1);

  const greet = useCallback(() => {
    setMessages((current) => current.length ? current : [{ id: 0, who: "bot", html: welcome }]);
  }, []);

  useEffect(() => {
    const api = {
      open() {
        setOpen(true);
        greet();
        inputRef.current?.focus();
      },
    };
    window.TanyaTekkim = api;
    return () => {
      if (window.TanyaTekkim === api) delete window.TanyaTekkim;
    };
  }, [greet]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  useEffect(() => {
    const msgs = messagesRef.current;
    if (msgs) msgs.scrollTop = msgs.scrollHeight;
  }, [messages.length, scrollRevision]);

  function addMsg(html, who) {
    const id = nextMessageId.current++;
    setMessages((current) => [...current, { id, who, html }]);
    return id;
  }

  function updateMsg(id, html) {
    setMessages((current) => current.map((message) => message.id === id ? { ...message, html } : message));
  }

  function load() {
    if (indexRef.current) return Promise.resolve(indexRef.current);
    return fetch("/kamus/search-index.json").then((r) => r.json())
      .then((j) => { indexRef.current = j; return j; })
      .catch(() => { indexRef.current = { terms: [] }; return indexRef.current; });
  }

  async function submitQuestion(value) {
    const q = value.trim();
    if (!q) return;
    addMsg(esc(q), "user");
    setQuestion("");
    setSending(true);
    const wait = addMsg("⏳ Mencari di glosarium terlebih dahulu…", "bot");
    const idx = await load();
    const t = strongMatch(idx, norm(q));
    if (t) {
      updateMsg(wait, entryAnswer(t, levelRef.current));
      setSending(false);
      return;
    }
    updateMsg(wait, "⏳ Tidak ditemukan di glosarium. Menanyakan AI…");
    try {
      const r = await fetch("/api/ask", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, level: levelRef.current }),
      });
      const j = await r.json();
      if (r.ok && j.answer) {
        updateMsg(wait, esc(j.answer).replace(/\n/g, "<br>") +
          '<br><span class="tt-src ai">AI — belum terverifikasi' +
          (j.model ? " · " + esc(j.model) : "") + "</span>");
      } else if (j && j.error === "ai_not_configured") {
        updateMsg(wait, "Istilah ini belum ada di glosarium dan fitur AI belum dikonfigurasi pada server. " +
          "Coba cari istilah terkait melalui kolom pencarian kamus." +
          '<br><span class="tt-src ai">AI — belum tersedia</span>');
      } else if (j && j.error === "rate_limited") {
        updateMsg(wait, "Terlalu banyak pertanyaan dalam waktu singkat. Tunggu beberapa menit, lalu coba kembali.");
      } else {
        updateMsg(wait, "AI tidak dapat menjawab saat ini. Coba kembali beberapa saat lagi." +
          '<br><span class="tt-src ai">AI — belum terverifikasi</span>');
      }
    } catch {
      updateMsg(wait, "Koneksi ke layanan AI gagal. Coba kembali beberapa saat lagi.");
    }
    setSending(false);
    // chat.js menggulir saat pesan ditambahkan dan setelah permintaan AI selesai.
    setScrollRevision((current) => current + 1);
  }

  return (
    <>
      <button id="tt-btn" type="button" aria-label="Buka chatbot Tanya Tekkim" onClick={() => {
        setOpen((current) => !current);
        greet();
        inputRef.current?.focus();
      }}>💬 Tanya Tekkim</button>
      <div id="tt-panel" role="dialog" aria-label="Tanya Tekkim" className={open ? "open" : undefined}>
        <div id="tt-head">
          <div>
            <div className="t">Tanya Tekkim</div>
            <div className="s">Asisten kamus teknik kimia IlmuTekkim</div>
          </div>
          <button id="tt-close" type="button" aria-label="Tutup" onClick={() => setOpen(false)}>×</button>
        </div>
        <div id="tt-levels">
          <span>Level:</span>
          <button type="button" className={level === "awam" ? "tt-lv on" : "tt-lv"} data-lv="awam" onClick={() => {
            levelRef.current = "awam";
            setLevel("awam");
          }}>Awam</button>
          <button type="button" className={level === "tekkim" ? "tt-lv on" : "tt-lv"} data-lv="tekkim" onClick={() => {
            levelRef.current = "tekkim";
            setLevel("tekkim");
          }}>Tekkim</button>
          <button type="button" className={level === "plant" ? "tt-lv on" : "tt-lv"} data-lv="plant" onClick={() => {
            levelRef.current = "plant";
            setLevel("plant");
          }}>Plant</button>
        </div>
        <div id="tt-msgs" ref={messagesRef}>
          {messages.map((message) => (
            <div key={message.id} className={"tt-msg " + message.who} dangerouslySetInnerHTML={{ __html: message.html }} />
          ))}
        </div>
        <div id="tt-examples">
          {examples.map((q) => (
            <button key={q} type="button" className="tt-ex" onClick={() => submitQuestion(q)}>{q}</button>
          ))}
        </div>
        <form id="tt-form" onSubmit={(event) => {
          event.preventDefault();
          submitQuestion(question);
        }}>
          <input id="tt-input" ref={inputRef} type="text" maxLength="500" placeholder="Tulis pertanyaan…" autoComplete="off" value={question} onChange={(event) => setQuestion(event.target.value)} />
          <button id="tt-send" type="submit" disabled={sending}>Kirim</button>
        </form>
      </div>
    </>
  );
}
