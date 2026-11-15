"use client";

/* eslint-disable @next/next/no-img-element */

import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  motion,
  useMotionValue,
  useReducedMotion,
  useSpring,
  useTransform,
  type MotionValue,
} from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { PersonaLanyardRail } from "./PersonaLanyardRail";
import { LandingOverview } from "./LandingOverview";
import { ThemeToggle } from "../theme/ThemeToggle";
import { request, type User } from "../../lib/api";

const cards = [
  { src: "/hero/pop-art-portrait.jpeg", title: "Creator insight" },
  { src: "/hero/coffee-aesthetic.jpeg", title: "Audience context" },
  { src: "/hero/city-day.jpeg", title: "Brand voice" },
  { src: "/hero/ootd-ugc.jpeg", title: "Reel opportunity" },
  { src: "/hero/playful-duo.jpeg", title: "Trend context" },
  { src: "/hero/speaker.jpeg", title: "Hook review" },
  { src: "/hero/costume-creator.jpeg", title: "Caption studio" },
  { src: "/hero/comic-art.jpeg", title: "Creative direction" },
  { src: "/hero/gameplay.jpeg", title: "Content plan" },
];

const spring = { stiffness: 60, damping: 25, mass: 0.5 };

type Stage = { width: number; height: number; mobile: boolean };
type TunnelCard = (typeof cards)[number] & { index: number; cos: number; sin: number; x: number; y: number; rotation: number };

const tunnelCards: TunnelCard[] = cards.map((card, index) => {
  const angle = index * 137.5 * (Math.PI / 180);
  return {
    ...card,
    index,
    cos: Math.cos(angle),
    sin: Math.sin(angle),
    x: 0.28 + (index % 3) * 0.08,
    y: 0.26 + (index % 2) * 0.09,
    rotation: (index % 2 === 0 ? 1 : -1) * (3 + (index % 5) * 2),
  };
});

function useParallax(enabled: boolean) {
  const rawX = useMotionValue(0);
  const rawY = useMotionValue(0);
  const x = useSpring(rawX, spring);
  const y = useSpring(rawY, spring);

  useEffect(() => {
    if (!enabled) return;
    const move = (event: PointerEvent) => {
      rawX.set((event.clientX / window.innerWidth - 0.5) * 2);
      rawY.set((event.clientY / window.innerHeight - 0.5) * 2);
    };
    window.addEventListener("pointermove", move, { passive: true });
    return () => window.removeEventListener("pointermove", move);
  }, [enabled, rawX, rawY]);

  return { x, y };
}

function Card({ card, progress, pointer, stage }: { card: TunnelCard; progress: MotionValue<number>; pointer: { x: MotionValue<number>; y: MotionValue<number> }; stage: Stage }) {
  const span = 0.55;
  const start = (card.index / tunnelCards.length) * (1 - span);
  const localProgress = useTransform(progress, [start, start + span], [0, 1]);
  const z = useTransform(localProgress, [0, 1], [stage.mobile ? -1200 : -1700, stage.mobile ? 350 : 500]);
  const opacity = useTransform(localProgress, [0, 0.18, 0.82, 0.98], [0, 1, 1, 0]);
  const transform = useTransform([z, pointer.x, pointer.y], ([currentZ, px, py]: number[]) =>
    `translate3d(calc(-50% + ${card.cos * stage.width * card.x - px * (stage.mobile ? 20 : 45)}px), calc(-50% + ${card.sin * stage.height * card.y - py * (stage.mobile ? 20 : 45)}px), ${currentZ}px) rotateZ(${card.rotation}deg)`,
  );
  const width = stage.mobile ? Math.max(150, Math.min(210, stage.width * 0.48)) : Math.max(250, Math.min(360, stage.width * 0.24));

  return <motion.div aria-hidden="true" className="tunnel-card" style={{ width, transform, opacity, zIndex: card.index + 1 }}>
    <div className="tunnel-card-frame">
      <img src={card.src} alt="" draggable={false} />
      <span>{card.title}</span>
    </div>
  </motion.div>;
}

export function PerspectiveTunnelHero() {
  const router = useRouter();
  const container = useRef<HTMLElement>(null);
  const reducedMotion = useReducedMotion();
  const [stage, setStage] = useState<Stage>({ width: 1440, height: 900, mobile: false });
  const [user, setUser] = useState<User | null>();
  const rawProgress = useMotionValue(0);
  const progress = useSpring(rawProgress, { stiffness: 80, damping: 30, restDelta: 0.0001 });
  const pointer = useParallax(!reducedMotion);
  const titleScale = useTransform(progress, [0, 0.5, 1], [0.7, 1, 1.35]);
  const titleOpacity = useTransform(progress, [0, 0.12, 0.85, 1], [0.25, 1, 1, 0]);
  const promptOpacity = useTransform(progress, [0, 0.12], [1, 0]);

  useEffect(() => {
    const resize = () => setStage({ width: window.innerWidth, height: window.innerHeight, mobile: window.innerWidth < 768 });
    resize();
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, []);

  useEffect(() => {
    const element = container.current;
    if (!element || reducedMotion) return;
    const wheel = (event: WheelEvent) => {
      if (rawProgress.get() === 1 && event.deltaY > 0) return;
      if (rawProgress.get() === 0 && event.deltaY < 0) return;
      event.preventDefault();
      rawProgress.set(Math.min(1, Math.max(0, rawProgress.get() + event.deltaY * 0.0008)));
    };
    element.addEventListener("wheel", wheel, { passive: false });
    return () => element.removeEventListener("wheel", wheel);
  }, [rawProgress, reducedMotion]);

  useEffect(() => {
    // The tunnel is an exploration at the top of the landing page. Returning there must
    // restore its opening frame rather than leave visitors on an empty end frame.
    const resetAtTop = () => {
      if (window.scrollY <= 8 && rawProgress.get() > 0) rawProgress.set(0);
    };
    window.addEventListener("scroll", resetAtTop, { passive: true });
    return () => window.removeEventListener("scroll", resetAtTop);
  }, [rawProgress]);

  useEffect(() => {
    request<User>("/auth/me").then(setUser).catch(() => setUser(null));
  }, []);

  const isSignedIn = Boolean(user);

  return <main id="main-content" className="landing-page">
    <div className="landing-theme-control"><button type="button" aria-label="Go to Verdict home" className="landing-wordmark landing-control-button" onClick={() => router.push("/")}><b>V</b><span>Verdict</span></button><div className="landing-account-links">{isSignedIn ? <button type="button" className="landing-workspace-button" onClick={() => router.push("/dashboard")}>Open workspace <span aria-hidden="true">→</span></button> : <><button type="button" className="landing-control-button" onClick={() => router.push("/sign-in?next=/dashboard")}>Log in</button><button type="button" className="landing-workspace-button" onClick={() => router.push("/sign-up?next=/onboarding")}>Get started <span aria-hidden="true">→</span></button></>}</div><ThemeToggle /></div>
    <section className="tunnel-hero" ref={container} style={{ perspective: stage.mobile ? "900px" : "1200px" }}>
    <div className="tunnel-grid" />
    <div className="tunnel-glow" />
    <div className="tunnel-ring tunnel-ring-near" />
    <div className="tunnel-ring tunnel-ring-far" />
    <motion.section className="tunnel-copy" style={{ scale: titleScale, opacity: titleOpacity }}>
      <p>Verdict · creator intelligence</p>
      <h1>Create with<br />context.</h1>
      <span>Move from authorized history to your next better Reel—without giving up control of your account.</span>
      <div className="tunnel-actions">{isSignedIn ? <><Link href="/connect">Connect safely</Link><Link href="/dashboard">Open workspace</Link></> : <><Link href="/sign-up?next=/onboarding">Create your workspace</Link><Link href="/sign-in?next=/dashboard">Log in</Link></>}</div>
    </motion.section>
    <motion.div className="tunnel-prompt" style={{ opacity: promptOpacity }}><span>Scroll to explore</span><i /></motion.div>
    <div className="tunnel-plane" style={{ transformStyle: "preserve-3d" }}>{tunnelCards.map((card) => <Card key={card.title} card={card} progress={progress} pointer={pointer} stage={stage} />)}</div>
    </section>
    <LandingOverview />
    <PersonaLanyardRail />
  </main>;
}
