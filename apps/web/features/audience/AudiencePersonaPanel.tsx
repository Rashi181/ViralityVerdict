"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Evidence = { field: string; values: Record<string, string | number>; source: string; source_label: string; as_of: string };
type Persona = { status: "observed" | "provisional" | "synthetic_demo"; observed_evidence: Evidence[]; inferred_interests: string[]; likely_motivations: string[]; content_preferences: string[]; suggested_hooks: string[]; confidence: string; freshness: string | null };

const labelFor = (field: string) => field.replaceAll("_", " ");

export function AudiencePersonaPanel() {
  const [persona, setPersona] = useState<Persona>();
  useEffect(() => { void request<Persona>("/audience/personas/current").then(setPersona).catch(() => undefined); }, []);
  if (!persona) return null;

  const evidence = persona.observed_evidence;
  if (evidence.length === 0) {
    return <section className="panel audience-unavailable">
      <p className="insight-kicker">Audience snapshot</p>
      <h2>Audience demographics are not available yet.</h2>
      <p>Your connection is read-only. Verdict will show age, location, or audience patterns here only after Meta returns eligible aggregate data—it will not invent a persona from guesses.</p>
      <small>When data becomes available, it will be clearly dated and labeled as observed.</small>
    </section>;
  }

  const synthetic = persona.status === "synthetic_demo" || evidence.some((item) => item.source === "synthetic_demo");
  const hypotheses = [...persona.inferred_interests, ...persona.likely_motivations, ...persona.content_preferences, ...persona.suggested_hooks].slice(0, 4);
  return <section className="panel audience-persona-panel">
    <header><div><p className="insight-kicker">Audience snapshot</p><h2>{synthetic ? "Synthetic audience signals" : "Available audience signals"}</h2><span>{persona.freshness ? `Updated ${new Date(persona.freshness).toLocaleDateString()}` : "Observed data"} · {persona.confidence} confidence</span></div></header>
    {synthetic && <p className="demo-source-label">Synthetic demonstration data — not Meta OAuth data. Metrics are fictional and shown only to demonstrate Verdict’s analysis workflow.</p>}
    <div className="audience-evidence-grid">{evidence.map((item) => <article key={`${item.field}-${item.as_of}`}><b>{labelFor(item.field)}</b><strong>{Object.entries(item.values).map(([key, value]) => `${key}: ${value}`).join(" · ")}</strong><small>{item.source_label}</small></article>)}</div>
    {hypotheses.length > 0 && <div className="audience-next-step"><b>Planning hypotheses — not audience facts</b>{hypotheses.map((item) => <span key={item}>{item}</span>)}</div>}
  </section>;
}
