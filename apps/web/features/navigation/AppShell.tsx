"use client";

import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "../theme/ThemeToggle";
import { request } from "../../lib/api";
import { useRouter } from "next/navigation";

const navigation = [
  ["Dashboard", "/dashboard", "◉"],
  ["Connect", "/connect", "⌁"],
  ["Creator intelligence", "/insights", "◌"],
  ["Ideas", "/ideas", "✦"],
  ["Reel analyzer", "/analyze", "▷"],
] as const;

export function AppShell({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const navigationRef = useRef<HTMLElement>(null);
  const [spotlitHref, setSpotlitHref] = useState<string | null>(null);
  const [lamp, setLamp] = useState({ left: 0, width: 0, visible: false });
  const moveLamp = useCallback((href: string) => {
    const navigation = navigationRef.current;
    const target = navigation?.querySelector<HTMLAnchorElement>(`a[data-nav-href="${href}"]`);
    if (!navigation || !target) return;
    const navigationBounds = navigation.getBoundingClientRect();
    const targetBounds = target.getBoundingClientRect();
    setLamp({ left: targetBounds.left - navigationBounds.left, width: targetBounds.width, visible: true });
  }, []);
  useEffect(() => {
    const frame = window.requestAnimationFrame(() => moveLamp(pathname));
    const resize = () => moveLamp(pathname);
    window.addEventListener("resize", resize);
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener("resize", resize);
    };
  }, [moveLamp, pathname]);
  const signOut = async () => { await request("/auth/sign-out", { method: "POST" }).catch(() => undefined); router.push("/"); router.refresh(); };
  return <div className="app-shell app-shell-limelight"><main id="main-content" tabIndex={-1}><header className="workspace-topbar"><Link className="brand" href="/dashboard"><span>V</span>Verdict</Link><nav ref={navigationRef} className="limelight-nav" aria-label="Product navigation" onMouseLeave={() => { setSpotlitHref(null); moveLamp(pathname); }}><span className="limelight-lamp" aria-hidden="true" style={{ width: lamp.width, transform: `translateX(${lamp.left}px)`, opacity: lamp.visible ? 1 : 0 }} />{navigation.map(([label, href, icon]) => <Link key={href} data-nav-href={href} href={href} className={`${pathname === href ? "is-active" : ""} ${spotlitHref === href ? "is-spotlit" : ""}`} aria-current={pathname === href ? "page" : undefined} onMouseEnter={() => { setSpotlitHref(href); moveLamp(href); }} onFocus={() => { setSpotlitHref(href); moveLamp(href); }} onBlur={() => setSpotlitHref(null)}><i aria-hidden="true">{icon}</i><span>{label}</span></Link>)}</nav><div className="workspace-actions"><ThemeToggle /><button className="sign-out-button" type="button" onClick={signOut}>Sign out</button></div></header><header className="workspace-heading"><div><p className="eyebrow">Verdict workspace</p><h1>{title}</h1><p className="intro">{description}</p></div></header><section className="workspace-content">{children}</section></main></div>;
}
