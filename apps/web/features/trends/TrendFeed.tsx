"use client";

import { useEffect, useState } from "react";

import { request } from "../../lib/api";

type Signal = { id: string; title: string; source_url: string; observed_at: string; niche_relevance: string; geographic_relevance: string; source_type: string; retrieved_at: string; freshness: string };
type Feed = { status: string; signals: Signal[]; fallback: string | null; limitations: string[] };

export function TrendFeed() {
  const [feed, setFeed] = useState<Feed>(); const [message, setMessage] = useState<string>();
  const reload = () => request<Feed>("/trends").then(setFeed).catch((error) => setMessage(error.message));
  useEffect(() => { void reload(); }, []);
  if (!feed) return null;
  return <><section className="panel"><h2>Trend intelligence</h2><p>Status: <strong>{feed.status}</strong></p>{feed.fallback && <p className="error">{feed.fallback}</p>}{feed.signals.map((signal) => <article key={signal.id}><h3>{signal.title} · {signal.freshness}</h3><p>{signal.niche_relevance} Geographic relevance: {signal.geographic_relevance}.</p><p>Observed: {new Date(signal.observed_at).toLocaleString()} · Retrieved: {new Date(signal.retrieved_at).toLocaleString()}</p><a href={signal.source_url} target="_blank" rel="noreferrer">View documented source</a></article>)}{feed.limitations.map((limit) => <p key={limit} className="error">Limit: {limit}</p>)}</section><form className="panel" action={async (data) => { try { await request("/trends/import", { method: "POST", body: JSON.stringify({ consent_confirmed: data.get("consent") === "on", signals: [{ title: data.get("title"), source_url: data.get("source_url"), observed_at: new Date(String(data.get("observed_at"))).toISOString(), niche_relevance: data.get("relevance"), geographic_relevance: data.get("geography"), source_type: data.get("source_type") }] }) }); setMessage("Source observation saved with attribution."); reload(); } catch (error) { setMessage(error instanceof Error ? error.message : "Trend import failed"); } }}><h2>Import attributable trend observation</h2><p>Use a documented, authorized source. This is an observation, not an Instagram performance claim.</p><label>Title<input name="title" required /></label><label>Source URL<input name="source_url" type="url" required /></label><label>Observed date<input name="observed_at" type="date" required /></label><label>Niche relevance<input name="relevance" required /></label><label>Geographic relevance<input name="geography" defaultValue="US" required /></label><label>Source type<select name="source_type"><option value="google_trends">Google Trends</option><option value="youtube">YouTube</option><option value="other_documented_source">Other documented source</option></select></label><label><input name="consent" type="checkbox" required /> I am authorized to import and attribute this source observation.</label><button type="submit">Save trend source</button>{message && <p role="status">{message}</p>}</form></>;
}
