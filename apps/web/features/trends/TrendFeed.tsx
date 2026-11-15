"use client";

import { useEffect, useState } from "react";

import { request } from "../../lib/api";

type Signal = { id: string; title: string; source_url: string; observed_at: string; niche_relevance: string; geographic_relevance: string; source_type: string; retrieved_at: string; freshness: string };
type Feed = { status: string; signals: Signal[]; fallback: string | null; limitations: string[] };

export function TrendFeed() {
  const [feed, setFeed] = useState<Feed>();
  useEffect(() => { void request<Feed>("/trends").then(setFeed).catch(() => undefined); }, []);
  if (!feed) return null;
  return <section className="panel trend-panel"><h2>Trend intelligence</h2><p>Status: <strong>{feed.status}</strong></p>{feed.fallback && <p className="error">{feed.fallback}</p>}{feed.signals.map((signal) => <article key={signal.id}><h3>{signal.title} · {signal.freshness}</h3><p>{signal.niche_relevance} Geographic relevance: {signal.geographic_relevance}.</p><p>Observed: {new Date(signal.observed_at).toLocaleString()} · Retrieved: {new Date(signal.retrieved_at).toLocaleString()}</p><a href={signal.source_url} target="_blank" rel="noreferrer">View documented source</a></article>)}{feed.limitations.map((limit) => <p key={limit} className="error">Limit: {limit.startsWith("Import an attributable") ? "A documented, authorized source connection is required before Verdict can show live trend intelligence." : limit}</p>)}</section>;
}
