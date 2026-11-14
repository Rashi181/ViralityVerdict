"use client";
import { useEffect, useState } from "react";
import { request } from "../../lib/api";
type Plan = { id: string; title: string; status: string; planned_at: string | null };
export function Planner() {
  const [plans, setPlans] = useState<Plan[]>(); const [message, setMessage] = useState<string>();
  const reload = () => request<Plan[]>("/plans").then(setPlans).catch(() => {});
  useEffect(() => { void reload(); }, []); if (!plans) return null;
  return <><section className="panel"><h2>Content planner</h2><p>Statuses describe your plan only; they never mean Verdict published anything.</p>{plans.length ? plans.map((plan) => <p key={plan.id}><strong>{plan.title}</strong> — {plan.status}{plan.planned_at ? ` · ${new Date(plan.planned_at).toLocaleString()}` : ""}</p>) : <p>No planned items.</p>}</section><form className="panel" action={async (data) => { try { await request("/plans", { method: "POST", body: JSON.stringify({ title: data.get("title"), status: data.get("status"), planned_at: data.get("planned_at") ? new Date(String(data.get("planned_at"))).toISOString() : null }) }); setMessage("Plan saved."); reload(); } catch (error) { setMessage(error instanceof Error ? error.message : "Save failed"); } }}><h2>Save a plan</h2><label>Title<input name="title" required /></label><label>Status<select name="status"><option>idea</option><option>draft</option><option>ready</option><option>scheduled</option><option>published</option><option>archived</option></select></label><label>Planned date<input name="planned_at" type="datetime-local" /></label><button type="submit">Save plan</button>{message && <p role="status">{message}</p>}</form></>;
}
