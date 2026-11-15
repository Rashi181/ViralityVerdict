"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { request, type User } from "../../lib/api";

export function OnboardingForm() {
  const router = useRouter();
  const [user, setUser] = useState<User>();
  const [message, setMessage] = useState<string>();
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    request<User>("/auth/me").then(setUser).catch(() => setMessage("Please sign in to personalise your workspace."));
  }, []);

  if (!user) return <section className="auth-shell onboarding-shell"><aside className="auth-intro"><Link className="auth-brand" href="/"><span>V</span> Verdict</Link><div><p>Set up your workspace</p><h1>One small step before the good part.</h1><strong>Verdict uses these preferences only to frame future recommendations. You can change them later.</strong></div></aside><section className="auth-card onboarding-loading"><p>{message ?? "Loading your session…"}</p>{message && <Link className="button" href="/sign-in">Sign in</Link>}</section></section>;

  const submit = async (data: FormData) => {
    setMessage(undefined);
    setIsSaving(true);
    try {
      await request("/onboarding", { method: "PUT", body: JSON.stringify({ niche: data.get("niche"), content_goals: [data.get("goal")], posting_constraints: data.get("constraints"), preferred_language: data.get("language"), preferred_tone: data.get("tone"), connection_preference: "instagram" }) });
      router.push("/dashboard");
      router.refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "We could not save your preferences. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  return <section className="auth-shell onboarding-shell"><aside className="auth-intro onboarding-intro"><Link className="auth-brand" href="/"><span>V</span> Verdict</Link><div><p>Step 2 of 2 · Personalize</p><h1>Make your next Reel more you.</h1><strong>Give Verdict a little context. Your Instagram remains separate until you choose to connect it with read-only access.</strong></div><ol className="onboarding-progress" aria-label="Onboarding progress"><li className="is-complete"><b>01</b><span>Account created</span></li><li className="is-current"><b>02</b><span>Creator context</span></li><li><b>03</b><span>Connect when ready</span></li></ol><small>You can edit every choice later. Verdict never publishes or changes your Instagram account.</small></aside><form action={submit} className="auth-card onboarding-card"><div className="auth-card-heading"><p>Your creator context</p><h2>What should Verdict keep in mind?</h2><span>These are planning preferences, not audience data. No account is connected by this form.</span></div><div className="onboarding-grid"><label>Your niche<input name="niche" required maxLength={100} placeholder="e.g. campus fashion, food, fitness" autoComplete="off" /></label><label>Primary goal<select name="goal" required defaultValue=""><option value="" disabled>Choose one</option><option value="grow_reach">Grow reach</option><option value="build_community">Build community</option><option value="drive_inquiries">Drive inquiries</option><option value="improve_consistency">Post more consistently</option></select></label><label>Preferred tone<select name="tone" required defaultValue=""><option value="" disabled>Choose one</option><option value="warm">Warm and conversational</option><option value="confident">Confident and direct</option><option value="playful">Playful</option><option value="educational">Educational</option></select></label><label>Language<select name="language" required defaultValue="en"><option value="en">English</option><option value="hi">Hindi</option><option value="hinglish">Hinglish</option><option value="other">Other</option></select></label></div><label className="onboarding-wide">Your posting reality<textarea name="constraints" required maxLength={500} placeholder="e.g. I can film twice a week, mostly on campus, and prefer short talking videos." /></label>{message && <p className="error" role="alert">{message}</p>}<button type="submit" disabled={isSaving}>{isSaving ? "Saving your workspace…" : "Open my workspace"}<span>→</span></button><p className="onboarding-note">Next, you can connect Instagram securely—or start by reviewing a private Reel draft.</p></form></section>;
}
