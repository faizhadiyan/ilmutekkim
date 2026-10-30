import { Fragment } from "react";
import { cleanText, segmentText, slideFigure } from "@/lib/content";
import { ArticleFigure } from "@/components/ArticleParts";

function textItems(items) {
  return (items || []).map(cleanText).filter(Boolean);
}

export function Rows({ rows }) {
  const valid = (rows || []).filter((row) => Array.isArray(row) && row.length > 0);
  if (!valid.length) return null;
  return <ol className="steps">{valid.map((row, i) => {
    const cells = row.map(cleanText);
    return <li key={i}>
      {cells.length >= 3 && <span className="step-num">{cells[0]}</span>}
      <div>
        {cells.length >= 2 && <strong>{cells[cells.length >= 3 ? 1 : 0]}</strong>}
        <p>{cells[cells.length >= 3 ? 2 : cells.length - 1]}</p>
      </div>
    </li>;
  })}</ol>;
}

export function SlideSection({ slide, slug, index, images }) {
  const type = slide.type || "body";
  const head = cleanText(slide.title || "") || cleanText(slide.pill || "");
  const callout = cleanText(slide.callout || "");
  const bullets = textItems(slide.bullets);
  const figure = slideFigure(slide, slug, index, images, head);
  const formula = cleanText(slide.formula || slide.equation || "");
  const grid = (slide.fill_grid || []).filter((row) => Array.isArray(row) && row.length >= 2);
  return <>
    {type === "quote" ? <section className="misconception">
      <p className="eyebrow">Yang sering dikira</p>
      {cleanText(slide.quote) && <blockquote>“{cleanText(slide.quote)}”</blockquote>}
      {cleanText(slide.hook) && <p>{cleanText(slide.hook)}</p>}
    </section> : type === "conclusion" ? <section className="conclusion">
      <p className="eyebrow">Kesimpulan</p>
      {cleanText(slide.head) && <h2>{cleanText(slide.head)}</h2>}
      {bullets.length > 0 && <ul>{bullets.map((b, i) => <li key={i}>{b}</li>)}</ul>}
      {cleanText(slide.equation) && <div className="formula">{cleanText(slide.equation)}</div>}
    </section> : <section>
      {head && <h2>{head}</h2>}
      {textItems(slide.paras).map((p, i) => <p key={i}>{p}</p>)}
      {figure && <ArticleFigure figure={figure} />}
      <Rows rows={slide.fill_rows} />
      <Rows rows={slide.fill_cards} />
      {grid.length > 0 && <div className="mini-grid">{grid.map((row, i) => <div className="mini-card" key={i}><strong>{cleanText(row[0])}</strong><p>{cleanText(row[1])}</p></div>)}</div>}
      {formula && <div className="formula">{formula}</div>}
      {bullets.length > 0 && <ul>{bullets.map((b, i) => <li key={i}>{b}</li>)}</ul>}
    </section>}
    {callout && type !== "conclusion" && <aside className="fact">{callout}</aside>}
  </>;
}

export function BeforeAfterSections({ spec: d }) {
  const result = d.bad_result_lines;
  const symbols = d.slide3_symbols || [];
  const resultItems = Array.isArray(result) ? textItems(result) : [];
  const good = segmentText(d.good_prompt_segments);
  const goodResults = Array.isArray(d.good_result_lines) ? textItems(d.good_result_lines) : textItems([d.good_result_lines]);
  return <>
    <section className="misconception"><p className="eyebrow">Masalahnya</p>
      {cleanText(d.bad_prompt) && <blockquote>“{cleanText(d.bad_prompt)}”</blockquote>}
      {cleanText(d.bad_hook_line) && <p>{cleanText(d.bad_hook_line)}</p>}
    </section>
    {Array.isArray(result) ? (symbols.length > 0 || resultItems.length > 0) && <section>
      <h2>{cleanText(d.bad_result_pill || "Yang perlu diketahui")}</h2>
      <ul>{symbols.length > 0 ? symbols.map((s, i) => <li key={i}><strong>{cleanText(s.name)}:</strong> {cleanText(s.desc)}</li>) : resultItems.map((r, i) => <li key={i}>{r}</li>)}</ul>
    </section> : cleanText(result) && <section><h2>{cleanText(d.bad_result_pill || "Kenyataannya")}</h2><p>{cleanText(result)}</p></section>}
    {cleanText(d.bad_why) && <section><h2>{cleanText(d.bad_why_title || "Kenapa bisa begitu")}</h2><p>{cleanText(d.bad_why)}</p></section>}
    {good && <section><h2>{cleanText(d.good_pill || "Cara yang benar")}</h2><p>{good}</p></section>}
    {cleanText(d.good_why) && <section><h2>{cleanText(d.good_why_title || "Intinya")}</h2><p>{cleanText(d.good_why)}</p></section>}
    {goodResults.length > 0 && <section><h2>{cleanText(d.good_result_pill || "Contoh nyata")}</h2>{goodResults.map((p, i) => <p key={i}>{p}</p>)}</section>}
    {(cleanText(d.conclusion_head) || cleanText(d.conclusion_body)) && <section className="conclusion"><p className="eyebrow">Kesimpulan</p><h2>{cleanText(d.conclusion_head)}</h2><p>{cleanText(d.conclusion_body)}</p></section>}
  </>;
}

export function DeepBody({ deep, figures }) {
  const sections = deep.sections || [];
  const facts = textItems(deep.facts);
  return <>
    {sections.map((section, i) => <Fragment key={i}>
      <section>
        {section.h && <h2>{section.h}</h2>}
        {(section.paras || []).filter((p) => cleanText(p)).map((p, j) => <p key={j}>{p}</p>)}
      </section>
      {figures[i] && <ArticleFigure figure={figures[i]} />}
    </Fragment>)}
    {figures.slice(sections.length).map((figure, i) => <ArticleFigure figure={figure} key={i} />)}
    {facts.length > 0 && <section className="factbox"><h2>Fakta kunci</h2><ul>{facts.map((fact, i) => <li key={i}>{fact}</li>)}</ul></section>}
    {cleanText(deep.closing) && <section><h2>Kesimpulannya</h2><p>{cleanText(deep.closing)}</p></section>}
  </>;
}
