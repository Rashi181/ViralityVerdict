"use client";

import { useEffect, useState } from "react";

import { request } from "../../lib/api";

type Summary = {
  sample_size: number;
  date_start: string | null;
  date_end: string | null;
  total_views: number;
  average_engagement_rate: number | null;
  top_media_ids: string[];
  recurring_formats: Record<string, number>;
  observed_hashtags: string[];
  observed_caption_keywords: string[];
  hook_samples: string[];
  limitations: string[];
};

export function CreatorSummary() {
  const [summary, setSummary] = useState<Summary>();
  useEffect(() => { request<Summary>("/creator/profile").then(setSummary).catch(() => {}); }, []);
  if (!summary) return null;

  const window = summary.date_start && summary.date_end
    ? `${new Date(summary.date_start).toLocaleDateString()}–${new Date(summary.date_end).toLocaleDateString()}`
    : "not available";
  const formats = Object.entries(summary.recurring_formats)
    .map(([format, count]) => `${format} (${count})`).join(", ");

  return <section className="panel">
    <h2>Creator intelligence</h2>
    <p>Observed imported history: {summary.sample_size} unique items · {summary.total_views} total views</p>
    <p>Observation window: {window}</p>
    <p>Derived average engagement rate: {summary.average_engagement_rate ?? "unavailable"}{summary.average_engagement_rate !== null ? "%" : ""}</p>
    <p>Recurring formats: {formats || "none"}</p>
    <p>Observed hashtags: {summary.observed_hashtags.join(", ") || "none"}</p>
    <p>Observed caption keywords: {summary.observed_caption_keywords.join(", ") || "none"}</p>
    <p>Observed top-caption openings: {summary.hook_samples.join(" | ") || "none"}</p>
    <p>Top media IDs: {summary.top_media_ids.join(", ") || "none"}</p>
    {summary.limitations.map((limit) => <p key={limit} className="error">Limit: {limit}</p>)}
  </section>;
}
