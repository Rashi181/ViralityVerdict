"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { request } from "../../lib/api";

export function AuthForm({ mode }: { mode: "sign-up" | "sign-in" }) {
  const router = useRouter();
  const [error, setError] = useState<string>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const submit = async (formData: FormData) => {
    setError(undefined);
    setIsSubmitting(true);
    try {
      await request(`/auth/${mode}`, { method: "POST", body: JSON.stringify({
        email: formData.get("email"), password: formData.get("password"), display_name: formData.get("display_name"),
      }) });
      router.push("/onboarding");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to continue"); }
    finally { setIsSubmitting(false); }
  };
  return <form action={submit} className="panel"><h1>{mode === "sign-up" ? "Create your Verdict account" : "Sign in"}</h1>
    {mode === "sign-up" && <label>Display name<input name="display_name" required maxLength={80} /></label>}
    <label>Email<input name="email" type="email" required /></label>
    <label>Password<input name="password" type="password" minLength={mode === "sign-up" ? 12 : 1} required /></label>
    {error && <p className="error" role="alert">{error}</p>}<button type="submit" disabled={isSubmitting}>{isSubmitting ? "Working…" : mode === "sign-up" ? "Create account" : "Sign in"}</button>
  </form>;
}
