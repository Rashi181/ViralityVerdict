"use client";

import { useEffect, useState } from "react";
import { request } from "../../lib/api";

type Video = { id: string; filename: string; status: string };
type Readiness = { status: string; score: number | null; label: string; evidence: { duration_seconds: number; width: number; height: number; sampled_frame_count: number; sampling_strategy: string; source: string }[]; attention_risks: string[]; persona_reactions: string[]; cumulative_recommendation: string; limitations: string[] };

export function ReelReadiness() {
  const [videos, setVideos] = useState<Video[]>([]); const [selected, setSelected] = useState<string>(); const [result, setResult] = useState<Readiness>(); const [message, setMessage] = useState("Loading your private drafts…");
  useEffect(() => { request<Video[]>("/videos").then((items) => { setVideos(items); setSelected(items[0]?.id); setMessage(items.length ? "Choose a draft to inspect its available evidence." : "Upload a private Reel draft to begin analysis."); }).catch((error: unknown) => setMessage(error instanceof Error ? error.message : "Unable to load drafts.")); }, []);
  const inspect = async () => { if (!selected) return; try { setResult(await request<Readiness>(`/videos/${selected}/analysis`)); } catch (error) { setMessage(error instanceof Error ? error.message : "Unable to load analysis."); } };
  return <section className="panel"><h2>Reel Readiness</h2><p>{message}</p>{videos.length > 0 && <><label>Private draft<select value={selected} onChange={(event) => setSelected(event.target.value)}>{videos.map((video) => <option key={video.id} value={video.id}>{video.filename} — {video.status}</option>)}</select></label><button type="button" onClick={inspect}>Inspect available evidence</button></>}{result && <div className="analysis-result"><h3>{result.label}</h3><p>{result.cumulative_recommendation}</p><h4>Measured evidence</h4>{result.evidence.map((item, index) => <article key={`${item.source}-${index}`}><p>{item.source.replaceAll("_", " ")}: {item.duration_seconds}s · {item.width}×{item.height}{item.sampled_frame_count ? ` · ${item.sampled_frame_count} private frames selected` : ""}</p><small>{item.sampling_strategy}</small></article>)}<h4>Attention and personas</h4><p>{result.attention_risks.length || result.persona_reactions.length ? "Results will appear here when evidence-backed analysis is configured." : "No attention-risk or persona claim has been generated."}</p>{result.limitations.map((limitation) => <p className="error" key={limitation}>Limit: {limitation}</p>)}</div>}</section>;
}
