import { staticPageMetadata } from "@/lib/staticPages";
import CalculatorInteractions from "@/components/CalculatorInteractions";

export const dynamic = "force-static";
export const metadata = staticPageMetadata("/kalkulator");

export default function Page() {
  return (
    <main>
      <article className="post">
        <p className="eyebrow">{"Kalkulator"}</p>
        <h1>{"Kalkulator teknik kimia."}</h1>
        <p className="lead">{"Empat kalkulator untuk konsep yang berulang kali dibahas di situs ini. Setiap kalkulator menggunakan persamaan standar, mencantumkan asumsinya secara eksplisit, dan menautkan artikel yang menjelaskan konsepnya. Hasil perhitungan merupakan titik awal analisis, bukan pengganti simulasi proses."}</p>
        <section className="calc-card">
          <h2>{"Derajat polimerisasi Carothers (step-growth)"}</h2>
          <p>{"Xn = (1 + r) / (1 + r − 2rp). Pada stoikiometri sempurna (r = 1) persamaan menyederhana menjadi Xn = 1 / (1 − p). Asumsi: polimerisasi step-growth tanpa reaksi samping."}</p>
          <div className="calc-grid">
            <div>
              <label>{"Konversi p"}</label>
              <input id="car-p" type="number" step="0.001" min="0" max="0.9999" defaultValue="0.99" />
            </div>
            <div>
              <label>{"Rasio stoikiometri r (1 = sempurna)"}</label>
              <input id="car-r" type="number" step="0.001" min="0.1" max="1" defaultValue="1" />
            </div>
          </div>
          <div className="calc-out" id="car-out"></div>
          <p>
            <a className="btn ghost" href="/artikel/polimerisasi-konversi-carothers/">{"Konsepnya: polimerisasi dan persamaan Carothers"}</a>
            {" "}
            <a className="btn ghost" href="/artikel/cs01-step-growth-carothers-dp-runtuh/">{"Cheat sheet: DP runtuh"}</a>
          </p>
        </section>
        <section className="calc-card">
          <h2>{"LMTD heat exchanger"}</h2>
          <p>{"LMTD = (ΔT1 − ΔT2) / ln(ΔT1 / ΔT2). Asumsi: aliran murni berlawanan arah atau searah sesuai pilihan, tanpa faktor koreksi konfigurasi shell-and-tube."}</p>
          <div className="calc-grid">
            <div>
              <label>{"Panas masuk (°C)"}</label>
              <input id="lm-thi" type="number" step="any" defaultValue="150" />
            </div>
            <div>
              <label>{"Panas keluar (°C)"}</label>
              <input id="lm-tho" type="number" step="any" defaultValue="100" />
            </div>
            <div>
              <label>{"Dingin masuk (°C)"}</label>
              <input id="lm-tci" type="number" step="any" defaultValue="30" />
            </div>
            <div>
              <label>{"Dingin keluar (°C)"}</label>
              <input id="lm-tco" type="number" step="any" defaultValue="80" />
            </div>
            <div>
              <label>{"Susunan aliran"}</label>
              <select id="lm-mode">
                <option value="counter">{"Berlawanan arah"}</option>
                <option value="co">{"Searah"}</option>
              </select>
            </div>
          </div>
          <div className="calc-out" id="lm-out"></div>
          <p>
            <a className="btn ghost" href="/artikel/heat-exchanger-bikin-shutdown/">{"Konsepnya: heat exchanger"}</a>
          </p>
        </section>
        <section className="calc-card">
          <h2>{"McCabe-Thiele distilasi biner"}</h2>
          <p>{"Metode grafis McCabe-Thiele untuk campuran biner. Asumsi: volatilitas relatif konstan, kondensor total, luapan molar konstan, dan garis umpan sesuai nilai q. Contoh baku di bawah adalah pola benzena-toluena."}</p>
          <div className="calc-grid">
            <div>
              <label>{"Volatilitas relatif α"}</label>
              <input id="mt-alpha" type="number" step="0.01" min="1.01" defaultValue="2.45" />
            </div>
            <div>
              <label>{"Fraksi umpan zF"}</label>
              <input id="mt-zf" type="number" step="0.01" min="0.01" max="0.99" defaultValue="0.44" />
            </div>
            <div>
              <label>{"Fraksi distilat xD"}</label>
              <input id="mt-xd" type="number" step="0.01" min="0.01" max="0.999" defaultValue="0.97" />
            </div>
            <div>
              <label>{"Fraksi bottoms xB"}</label>
              <input id="mt-xb" type="number" step="0.001" min="0.001" max="0.99" defaultValue="0.02" />
            </div>
            <div>
              <label>{"q umpan (1 = cair jenuh)"}</label>
              <input id="mt-q" type="number" step="0.05" min="-1" max="2" defaultValue="1" />
            </div>
            <div>
              <label>{"Faktor R / R minimum"}</label>
              <input id="mt-f" type="number" step="0.05" min="1.01" max="5" defaultValue="1.3" />
            </div>
          </div>
          <div className="calc-out" id="mt-out"></div>
          <canvas id="mt-canvas" width="520" height="520"></canvas>
          <p>
            <a className="btn ghost" href="/artikel/distilasi-bertingkat-minyak-mentah/">{"Konsepnya: distilasi bertingkat"}</a>
            {" "}
            <a className="btn ghost" href="/artikel/reflux-optimum-kolom-distilasi/">{"Konsep reflux optimum"}</a>
          </p>
        </section>
        <section className="calc-card">
          <h2>{"Konversi satuan proses"}</h2>
          <p>{"Suhu, tekanan, dan aliran volumetrik yang paling sering dipakai di pabrik."}</p>
          <div className="calc-grid">
            <div>
              <label>{"Suhu"}</label>
              <input id="cv-tv" type="number" step="any" defaultValue="100" />
            </div>
            <div>
              <label>{"Satuan suhu"}</label>
              <select id="cv-tu">
                <option value="C">{"°C"}</option>
                <option value="F">{"°F"}</option>
                <option value="K">{"K"}</option>
              </select>
            </div>
            <div>
              <label>{"Tekanan"}</label>
              <input id="cv-pv" type="number" step="any" defaultValue="1" />
            </div>
            <div>
              <label>{"Satuan tekanan"}</label>
              <select id="cv-pu">
                <option value="atm">{"atm"}</option>
                <option value="bar">{"bar"}</option>
                <option value="kPa">{"kPa"}</option>
                <option value="Pa">{"Pa"}</option>
                <option value="psi">{"psi"}</option>
              </select>
            </div>
            <div>
              <label>{"Aliran"}</label>
              <input id="cv-fv" type="number" step="any" defaultValue="10" />
            </div>
            <div>
              <label>{"Satuan aliran"}</label>
              <select id="cv-fu">
                <option value="m3/h">{"m³/jam"}</option>
                <option value="m3/s">{"m³/s"}</option>
                <option value="L/s">{"L/s"}</option>
                <option value="gpm (US)">{"gpm (US)"}</option>
              </select>
            </div>
          </div>
          <div className="calc-out" id="cv-out"></div>
          <p>
            <a className="btn ghost" href="/artikel/utilitas-pabrik-steam-air-nitrogen/">{"Konsepnya: utilitas pabrik"}</a>
          </p>
        </section>
      </article>
      {"\n"}{"\n\n"}
      <CalculatorInteractions />
    </main>
    );
}
