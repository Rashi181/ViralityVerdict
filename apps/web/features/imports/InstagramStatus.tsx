"use client";
import { useEffect, useState } from "react";
import { apiBaseUrl, request } from "../../lib/api";

type Status = { status: "not_configured" | "ready_for_connect" | "connected"; detail: string };

export function InstagramStatus() {
  const [connection, setConnection] = useState<Status | null>(null);
  const [message, setMessage] = useState("");
  const load = () => request<Status>("/instagram/status").then(setConnection).catch((error: Error) => setMessage(error.message));
  useEffect(() => { load(); }, []);
  const sync = async () => { try { const result = await request<{ media_count: number; username: string | null }>("/instagram/sync", { method: "POST" }); setMessage(`Synced ${result.media_count} observed media item${result.media_count === 1 ? "" : "s"}${result.username ? ` from @${result.username}` : ""}.`); } catch (error) { setMessage(error instanceof Error ? error.message : "Sync failed"); } };
  const isConnected = connection?.status === "connected";
  return <section className="connection-card"><header><div><p>Official Meta connection</p><h2>{isConnected ? "Your read-only connection is active." : "Connect only what Verdict needs."}</h2><span>{connection?.detail ?? "Checking Instagram connection…"}</span></div><span className="workspace-avatar avatar-connect" aria-hidden="true"><i /><b /></span></header><div className="connection-steps"><article><b>01</b><span>Authorize</span><small>Meta handles your sign-in. Verdict never sees your password.</small></article><article><b>02</b><span>Observe</span><small>Only eligible creator history is read with GET-only requests.</small></article><article><b>03</b><span>Stay in control</span><small>No posting, messages, comments, edits, or account changes.</small></article></div><footer>{connection?.status === "ready_for_connect" && <a className="button" href={`${apiBaseUrl}/instagram/connect`}>Continue to Meta’s read-only consent <span>→</span></a>}{isConnected && <button type="button" onClick={sync}>Sync authorized history <span>→</span></button>}{message && <p role="status">{message}</p>}<small>Access is purpose-limited: account connection and eligible observed history only.</small></footer></section>;
}
