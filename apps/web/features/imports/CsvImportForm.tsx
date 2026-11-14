"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { request, type User } from "../../lib/api";
export function CsvImportForm() {
  const [message, setMessage] = useState<string>(); const [user, setUser] = useState<User | null>();
  useEffect(() => { request<User>("/auth/me").then(setUser).catch(() => setUser(null)); }, []);
  if (user === undefined) return <section className="panel"><h2>Import your CSV</h2><p>Checking your account…</p></section>;
  if (user === null) return <section className="panel"><h2>Import your CSV</h2><p>Sign in before importing creator data. This keeps every import private to your Verdict account.</p><Link href="/sign-in">Sign in to import</Link></section>;
  return <form className="panel" action={async (data) => { try { const body = new FormData(); body.set("file", data.get("file") as File); body.set("consent_confirmed", String(data.get("consent") === "on")); await request("/imports/csv", { method: "POST", body }); setMessage("Import saved as user-supplied data, not API-verified."); } catch (e) { setMessage(e instanceof Error ? e.message : "Import failed"); } }}><h2>Import your CSV</h2><p>Signed in as {user.email}. Required columns: media_id, published_at, caption, media_type, views, likes, comments.</p><label>CSV file<input type="file" name="file" accept=".csv,text/csv" required /></label><label><input type="checkbox" name="consent" required /> I confirm this is data I am authorized to import.</label><button type="submit">Import CSV</button>{message && <p role="status">{message}</p>}</form>;
}
