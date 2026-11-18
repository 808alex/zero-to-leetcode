import { useMemo, useState } from "react";
import { LEVELS, MISTAKES, MISTAKE_CATEGORIES } from "../content";
import type { Mistake } from "../types";
import { CodeView, Out } from "../components/Bits";
import { Back, Warn } from "../components/Icons";
import { Pip } from "../components/Mascot";
import { play } from "../lib/sound";

function MistakeCard({ m }: { m: Mistake }) {
  const ran = m.wrongErr !== undefined;
  return (
    <article className="mistake" id={`mistake-${m.id}`}>
      <header className="mistake-head">
        <h3>{m.title}</h3>
        {LEVELS[m.level] && <span className="chip">Covered in {LEVELS[m.level].title}</span>}
      </header>
      <div className="mistake-cols">
        <div className="mistake-col bad">
          <div className="mistake-label">What people write</div>
          <CodeView code={m.wrong} />
          {ran && (
            m.wrongErr ? (
              <div className="py-says err"><span>Python says</span><code>{m.wrongErr}</code></div>
            ) : (
              <div className="py-says"><span>It prints</span><Out text={m.wrongOut} /></div>
            )
          )}
        </div>
        <div className="mistake-col good">
          <div className="mistake-label">What you meant</div>
          <CodeView code={m.right} />
          {ran && <div className="py-says ok"><span>It prints</span><Out text={m.rightOut} /></div>}
        </div>
      </div>
      <p className="mistake-why">{m.why}</p>
    </article>
  );
}

export function MistakesScreen({ onBack }: { onBack: () => void }) {
  const [cat, setCat] = useState<string>("All");
  const [q, setQ] = useState("");
  const list = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return MISTAKES.filter((m) => (cat === "All" || m.cat === cat) &&
      (!needle || [m.title, m.why, m.wrong, m.wrongErr || ""].some((t) => t.toLowerCase().includes(needle))));
  }, [cat, q]);

  return (
    <div className="page">
      <header className="page-top">
        <button className="btn ghost" onClick={onBack}><Back size={18} /> Path</button>
        <h1><Warn size={28} /> Common mistakes</h1>
      </header>
      <div className="page-body">
        <div className="page-intro">
          <Pip mood="think" size={80} />
          <p>The mistakes nearly everyone makes, each with the fix. Every message below is what Python really printed when we ran the code, so if you see it in your own work, you'll know what it means.</p>
        </div>
        <div className="filters">
          <input className="search" type="search" placeholder="Search, e.g. TypeError or index" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Search mistakes" />
          <div className="chips" role="tablist" aria-label="Categories">
            {["All", ...MISTAKE_CATEGORIES].map((c) => (
              <button key={c} role="tab" aria-selected={cat === c} className={`chip-btn ${cat === c ? "on" : ""}`} onClick={() => { setCat(c); play("click"); }}>
                {c}{c !== "All" && <small>{MISTAKES.filter((m) => m.cat === c).length}</small>}
              </button>
            ))}
          </div>
        </div>
        {list.length === 0 && <p className="muted">Nothing matches that search.</p>}
        <div className="mistake-list">{list.map((m) => <MistakeCard key={m.id} m={m} />)}</div>
      </div>
    </div>
  );
}
