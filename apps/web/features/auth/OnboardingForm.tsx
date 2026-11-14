"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { request, type User } from "../../lib/api";

export function OnboardingForm() {
  const [user, setUser] = useState<User>(); const [message, setMessage] = useState<string>();
  useEffect(() => { request<User>("/auth/me").then(setUser).catch(() => setMessage("Please sign in to access onboarding.")); }, []);
  if (!user) return <section className="panel"><p>{message ?? "Loading your session…"}</p>{message && <Link href="/sign-in">Sign in</Link>}</section>;
  return <form className="panel" action={async (data) => { await request("/onboarding", { method: "PUT", body: JSON.stringify({ niche: data.get("niche"), content_goals: [data.get("goal")], posting_constraints: data.get("constraints"), preferred_language: data.get("language"), preferred_tone: data.get("tone"), connection_preference: data.get("connection") }) }); setMessage("Onboarding saved."); }}>
    <h1>Welcome, {user.display_name}</h1><p>Tell Verdict how to tailor future recommendations.</p>
    <label>Niche<input name="niche" required /></label><label>Primary goal<input name="goal" required /></label><label>Posting constraints<input name="constraints" required /></label><label>Language<input name="language" defaultValue="en" required /></label><label>Tone<input name="tone" required /></label><label>Data preference<select name="connection"><option value="manual_import">Manual import</option><option value="instagram">Instagram connection</option></select></label><button type="submit">Save onboarding</button>{message && <p>{message}</p>}
  </form>;
}
