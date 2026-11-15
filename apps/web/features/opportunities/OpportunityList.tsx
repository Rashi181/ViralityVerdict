"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Opportunity = {
  id: string;
  title: string;
  angle?: string;
  hook?: string;
  format?: string;
  effort?: string;
  score: number;
  score_version: string;
  confidence: string;
  evidence: string[];
  score_inputs: Record<string, number | string[]>;
};

const imagery = ["/hero/ootd-ugc.jpeg", "/hero/coffee-aesthetic.jpeg", "/hero/speaker.jpeg", "/hero/comic-art.jpeg"];

export function OpportunityList() {
  const [items, setItems] = useState<Opportunity[]>();
  const [message, setMessage] = useState<string>();
  const reload = () => request<Opportunity[]>("/opportunities").then(setItems).catch(() => setItems([]));
  useEffect(() => { void reload(); }, []);
  if (!items) return null;

  return <>
    <section className="opportunity-gallery" aria-labelledby="opportunity-heading">
      <header><div><p>Evidence-backed suggestions</p><h2 id="opportunity-heading">Content opportunities</h2><span>Cards appear only after you save a real opportunity. Scores are prioritization heuristics, never virality predictions.</span></div><span className="workspace-avatar avatar-ideas" aria-hidden="true"><i /><b /></span></header>
      {items.length === 0 ? <div className="empty-opportunities"><strong>No opportunities yet.</strong><span>Connect history or add a researched idea below. Verdict will not invent ideas from missing account data.</span></div> : <div className="opportunity-grid">{items.map((item, index) => <article className="opportunity-card" key={item.id}><div className="opportunity-image" style={{ backgroundImage: `linear-gradient(180deg, transparent 35%, rgba(9,13,22,.92)), url(${imagery[index % imagery.length]})` }}><span>{item.score}<small>/100</small></span></div><div><small>{item.format ?? "reel"} · {item.effort ?? "planned"} effort · {item.confidence} confidence</small><h3>{item.title}</h3><p>{item.angle ?? "No angle was supplied."}</p>{item.hook && <blockquote>“{item.hook}”</blockquote>}<footer>Evidence: {item.evidence.join(", ") || "not recorded"}</footer></div></article>)}</div>}
    </section>
    <form className="opportunity-form" action={async (data) => { try { await request("/opportunities", { method: "POST", body: JSON.stringify({ title: data.get("title"), angle: data.get("angle"), hook: data.get("hook"), format: "reel", effort: "low", evidence: [data.get("evidence")], score_inputs: { audience_fit: Number(data.get("audience_fit")), trend_relevance: Number(data.get("trend_relevance")), novelty: Number(data.get("novelty")), feasibility: Number(data.get("feasibility")), missing_components: data.get("missing") ? [data.get("missing")] : [] } }) }); setMessage("Opportunity saved with a deterministic score."); reload(); } catch (error) { setMessage(error instanceof Error ? error.message : "Save failed"); } }}>
      <div><p>Make a grounded card</p><h2>Score an opportunity</h2><span>Only add evidence you are authorized to use. Missing information lowers confidence—it is not filled in.</span></div>
      <label>Title<input name="title" required /></label><label>Angle<input name="angle" required /></label><label>Hook<input name="hook" required /></label><label>Evidence ID or source<input name="evidence" required /></label>
      <div className="score-inputs"><label>Audience fit<input name="audience_fit" type="number" min="0" max="100" defaultValue="80" required /></label><label>Trend relevance<input name="trend_relevance" type="number" min="0" max="100" defaultValue="60" required /></label><label>Novelty<input name="novelty" type="number" min="0" max="100" defaultValue="50" required /></label><label>Feasibility<input name="feasibility" type="number" min="0" max="100" defaultValue="90" required /></label></div>
      <label>Missing input, if any<input name="missing" placeholder="e.g. current trend source" /></label><button type="submit">Save opportunity <span>→</span></button>{message && <p role="status">{message}</p>}
    </form>
  </>;
}
