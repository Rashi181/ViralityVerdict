"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Summary = {
  sample_size: number;
  date_start: string | null;
  date_end: string | null;
  total_views: number;
  average_engagement_rate: number | null;
  recurring_formats: Record<string, number>;
  observed_hashtags: string[];
  observed_caption_keywords: string[];
  hook_samples: string[];
  data_source: "none" | "instagram_api" | "user_import" | "synthetic_demo";
};

export function CreatorSummary() {
  const [summary, setSummary] = useState<Summary>();
  useEffect(() => { void request<Summary>("/creator/profile").then(setSummary).catch(() => undefined); }, []);
  if (!summary) return null;

  if (summary.sample_size === 0) {
    return <section className="panel insights-empty-state">
      <p className="insight-kicker">Creator history</p>
      <h2>Nothing to analyze yet.</h2>
      <p>Verdict has not received eligible post or Reel history from your connected account. It will not fill this page with made-up performance data.</p>
      <Link className="button" href="/connect">Check connection</Link>
    </section>;
  }

  const dateRange = summary.date_start && summary.date_end
    ? `${new Date(summary.date_start).toLocaleDateString()} – ${new Date(summary.date_end).toLocaleDateString()}`
    : "Available history";
  const formats = Object.entries(summary.recurring_formats).map(([format, count]) => `${format} (${count})`).join(" · ");
  const synthetic = summary.data_source === "synthetic_demo";

  return <section className="panel creator-insights-panel">
    <header><div><p className="insight-kicker">Creator history</p><h2>{synthetic ? "Synthetic creator-history demonstration" : "What your published content shows"}</h2><span>{dateRange}</span></div></header>
    {synthetic && <p className="demo-source-label">Synthetic demonstration data — fictional posts and metrics, not Meta OAuth observations.</p>}
    <div className="insight-metrics">
      <article><strong>{summary.sample_size}</strong><span>observed posts</span></article>
      <article><strong>{summary.total_views.toLocaleString()}</strong><span>total views</span></article>
      <article><strong>{summary.average_engagement_rate === null ? "—" : `${summary.average_engagement_rate}%`}</strong><span>average engagement</span></article>
    </div>
    <div className="insight-signals">
      {formats && <article><b>Formats</b><span>{formats}</span></article>}
      {summary.observed_hashtags.length > 0 && <article><b>Hashtags used</b><span>{summary.observed_hashtags.slice(0, 8).join(" · ")}</span></article>}
      {summary.observed_caption_keywords.length > 0 && <article><b>Caption themes</b><span>{summary.observed_caption_keywords.slice(0, 8).join(" · ")}</span></article>}
      {summary.hook_samples.length > 0 && <article><b>Opening patterns</b><span>{summary.hook_samples.slice(0, 3).join(" · ")}</span></article>}
    </div>
  </section>;
}
