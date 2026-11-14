"use client";

import { useEffect, useState } from "react";

import { request } from "../../lib/api";

type Evidence = { field: string; values: Record<string, string | number>; source: string; source_label: string; as_of: string };
type Persona = {
  status: "observed" | "provisional";
  label: string;
  intended_use: string;
  observed_evidence: Evidence[];
  content_preferences: string[];
  suggested_hooks: string[];
  pacing_considerations: string[];
  cta_preferences: string[];
  unknowns: string[];
  confidence: string;
  data_coverage: string;
  freshness: string | null;
  feedback_note: string | null;
};

export function AudiencePersonaPanel() {
  const [persona, setPersona] = useState<Persona>();
  const [message, setMessage] = useState<string>();
  const reload = () => request<Persona>("/audience/personas/current").then(setPersona).catch((error) => setMessage(error.message));
  useEffect(() => { void reload(); }, []);
  if (!persona) return null;

  return <>
    <section className="panel">
      <h2>Audience persona</h2>
      <p><strong>{persona.label}</strong> · <span className={persona.status === "provisional" ? "error" : ""}>{persona.status}</span> · confidence: {persona.confidence}</p>
      <p>{persona.intended_use}</p><p>Coverage: {persona.data_coverage}</p>
      <p>Freshness: {persona.freshness ? new Date(persona.freshness).toLocaleString() : "No audience aggregate data available"}</p>
      <h3>Observed evidence</h3>
      {persona.observed_evidence.length ? <ul>{persona.observed_evidence.map((item) => <li key={`${item.field}-${item.as_of}`}><strong>{item.field}</strong>: {Object.entries(item.values).map(([key, value]) => `${key}: ${value}`).join(", ")} — {item.source_label}, {new Date(item.as_of).toLocaleDateString()} ({item.source})</li>)}</ul> : <p>None. This persona is not validated by audience statistics.</p>}
      <h3>Hypotheses to test</h3>
      {[...persona.content_preferences, ...persona.suggested_hooks, ...persona.pacing_considerations, ...persona.cta_preferences].map((item) => <p key={item}>{item}</p>)}
      <h3>Unknowns</h3>{persona.unknowns.map((item) => <p className="error" key={item}>{item}</p>)}
      {persona.feedback_note && <p>Your saved feedback: {persona.feedback_note}</p>}
    </section>
    <form className="panel" action={async (data) => { try { await request("/audience/import", { method: "POST", body: JSON.stringify({ consent_confirmed: data.get("consent") === "on", aggregates: [{ field: data.get("field"), values: JSON.parse(String(data.get("values"))), source: "user_import", source_label: data.get("source_label"), as_of: new Date(String(data.get("as_of"))).toISOString() }] }) }); setMessage("Authorized aggregate audience data saved as user-imported, not API-verified."); reload(); } catch (error) { setMessage(error instanceof Error ? error.message : "Audience import failed"); } }}>
      <h2>Import aggregate audience evidence</h2><p>Only enter statistics you are authorized to use. Do not enter individual follower information.</p>
      <label>Aggregate field<select name="field" defaultValue="top_locations"><option value="top_locations">Top locations</option><option value="age_distribution">Age distribution</option><option value="gender_distribution">Gender distribution</option><option value="follower_count">Follower count</option><option value="other">Other aggregate</option></select></label>
      <label>Values as JSON object<input name="values" defaultValue='{"Example": 1}' required /></label><label>Source label<input name="source_label" defaultValue="Authorized audience export" required /></label><label>As-of date<input type="date" name="as_of" required /></label><label><input type="checkbox" name="consent" required /> I confirm I am authorized to import this aggregate audience data.</label><button type="submit">Save audience evidence</button>{message && <p role="status">{message}</p>}
    </form>
    <form className="panel" action={async (data) => { try { await request("/audience/personas/feedback", { method: "POST", body: JSON.stringify({ note: data.get("note") }) }); setMessage("Persona feedback saved."); reload(); } catch (error) { setMessage(error instanceof Error ? error.message : "Feedback failed"); } }}><h2>Persona feedback</h2><label>What should Verdict prioritize next?<input name="note" defaultValue={persona.feedback_note ?? ""} required /></label><button type="submit">Save feedback</button></form>
  </>;
}
