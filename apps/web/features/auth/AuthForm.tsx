"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { request } from "../../lib/api";

export function AuthForm({ mode }: { mode: "sign-up" | "sign-in" }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isSignUp = mode === "sign-up";
  const requestedNext = searchParams.get("next");
  const next = requestedNext?.startsWith("/") && !requestedNext.startsWith("//") ? requestedNext : undefined;
  const submit = async (data: FormData) => {
    setError(undefined);
    setIsSubmitting(true);
    try {
      await request(isSignUp ? "/auth/sign-up" : "/auth/sign-in", { method: "POST", body: JSON.stringify(Object.fromEntries(data)) });
      router.push(next ?? (isSignUp ? "/onboarding" : "/dashboard"));
      router.refresh();
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Something went wrong. Please try again."); }
    finally { setIsSubmitting(false); }
  };

  const otherAuthHref = `${isSignUp ? "/sign-in" : "/sign-up"}${next ? `?next=${encodeURIComponent(next)}` : ""}`;
  return <section className="auth-shell"><aside className="auth-intro"><Link className="auth-brand" href="/"><span>V</span> Verdict</Link><div><p>{isSignUp ? "Create with context" : "Welcome back"}</p><h1>{isSignUp ? "Build a sharper Reel strategy." : "Your next idea is waiting."}</h1><strong>Creator intelligence that stays read-only, evidence-aware, and firmly under your control.</strong></div><ul><li>Personalized opportunities—not generic prompts</li><li>Private draft review before you publish</li><li>Manual publishing only, always</li></ul><small>Verdict never asks for your Instagram password.</small></aside><form action={submit} className="auth-card"><div className="auth-card-heading"><p>{isSignUp ? "Start your workspace" : "Sign in to Verdict"}</p><h2>{isSignUp ? "Create account" : "Good to see you."}</h2><span>{isSignUp ? "Start with your email. You can connect authorized Instagram data later." : "Use the email and password for your Verdict account."}</span></div>{isSignUp && <label>Display name<input name="display_name" required maxLength={80} placeholder="How should we call you?" autoComplete="name" /></label>}<label>Email address<input name="email" type="email" required placeholder="you@example.com" autoComplete="email" /></label><label>Password<input name="password" type="password" minLength={isSignUp ? 12 : 1} required placeholder={isSignUp ? "At least 12 characters" : "Your password"} autoComplete={isSignUp ? "new-password" : "current-password"} /></label>{error && <p className="error" role="alert">{error}</p>}<button type="submit" disabled={isSubmitting}>{isSubmitting ? "Working…" : isSignUp ? "Create your strategy" : "Sign in"}<span>→</span></button><p className="auth-switch">{isSignUp ? "Already have an account?" : "New to Verdict?"} <Link href={otherAuthHref}>{isSignUp ? "Log in" : "Create an account"}</Link></p></form></section>;
}
