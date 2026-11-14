import type { ReactNode } from "react";
import Link from "next/link";

const navigation = [
  ["Dashboard", "/dashboard"],
  ["Connect & import", "/connect"],
  ["Insights", "/insights"],
  ["Ideas", "/ideas"],
  ["Analyze Reel", "/analyze"],
  ["Caption & Hashtag Studio", "/studio"],
  ["Planner", "/planner"],
  ["Strategist", "/strategist"],
  ["Publish & learn", "/publish"],
] as const;

export function AppShell({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  return <div className="app-shell"><aside className="sidebar"><Link className="brand" href="/dashboard">Verdict</Link><p>Creator intelligence, before you publish.</p><nav aria-label="Product navigation">{navigation.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}</nav></aside><main id="main-content" tabIndex={-1}><p className="eyebrow">Verdict workspace</p><h1>{title}</h1><p className="intro">{description}</p>{children}</main></div>;
}
