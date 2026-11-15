"use client";

import { createContext, type ReactNode, useCallback, useContext, useEffect, useRef, useState } from "react";

type Theme = "light" | "dark";
type ThemeOrigin = { x: number; y: number };
type ThemeContextValue = { theme: Theme; toggleTheme: (origin?: ThemeOrigin) => void };
type ViewTransitionHandle = { finished: Promise<void> };
type ViewTransitionDocument = Document & {
  startViewTransition?: (update: () => void) => ViewTransitionHandle;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);
const storageKey = "verdict-theme";

function preferredTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

function applyTheme(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  window.localStorage.setItem(storageKey, theme);
}

/**
 * The browser owns the outgoing-page snapshot. This is substantially more
 * reliable than serialising the entire document into a canvas: long pages,
 * media previews, and cross-origin images no longer make the theme switch fail.
 * The custom properties place the CSS ink-spill at the pressed toggle.
 */
function prepareInkOrigin(origin: ThemeOrigin) {
  const root = document.documentElement;
  const x = (origin.x / window.innerWidth) * 100;
  const y = (origin.y / window.innerHeight) * 100;
  const seed = (Math.sin(origin.x * 12.9898 + origin.y * 78.233) * 43758.5453) % 1;
  const polygon = (radius: number, phase: number) => {
    const points = Array.from({ length: 28 }, (_, index) => {
      const angle = (index / 28) * Math.PI * 2;
      const wobble = 1 + Math.sin(angle * 5 + phase + seed * 9) * .14 + Math.sin(angle * 9 - phase * .7) * .06;
      return `${(x + Math.cos(angle) * radius * wobble).toFixed(2)}% ${(y + Math.sin(angle) * radius * wobble).toFixed(2)}%`;
    });
    return `polygon(${points.join(",")})`;
  };

  root.style.setProperty("--ink-origin-x", `${x.toFixed(2)}%`);
  root.style.setProperty("--ink-origin-y", `${y.toFixed(2)}%`);
  // Matching polygon point counts let the browser interpolate a fluid,
  // irregular contour instead of falling back to a circular reveal.
  root.style.setProperty("--ink-spill-start", polygon(220, .2));
  root.style.setProperty("--ink-spill-wide", polygon(112, 1.1));
  root.style.setProperty("--ink-spill-near", polygon(44, 2.4));
  root.style.setProperty("--ink-spill-end", polygon(.15, 3.6));
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("dark");
  const transitioning = useRef(false);

  useEffect(() => {
    const saved = window.localStorage.getItem(storageKey);
    const next = saved === "light" || saved === "dark" ? saved : preferredTheme();
    applyTheme(next);
    const frame = window.requestAnimationFrame(() => setTheme(next));
    return () => window.cancelAnimationFrame(frame);
  }, []);

  const toggleTheme = useCallback((origin?: ThemeOrigin) => {
    if (transitioning.current) return;

    const root = document.documentElement;
    const next: Theme = root.dataset.theme === "light" ? "dark" : "light";
    const change = () => {
      applyTheme(next);
      setTheme(next);
    };

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      change();
      return;
    }

    const point = origin ?? { x: window.innerWidth - 56, y: 40 };
    prepareInkOrigin(point);
    root.dataset.inkTransition = "spill";
    transitioning.current = true;

    const startViewTransition = (document as ViewTransitionDocument).startViewTransition;
    if (!startViewTransition) {
      // A no-motion fallback is preferable to a partially applied theme.
      change();
      root.removeAttribute("data-ink-transition");
      transitioning.current = false;
      return;
    }

    const transition = startViewTransition.call(document, change);
    void transition.finished.catch(() => undefined).finally(() => {
      root.removeAttribute("data-ink-transition");
      transitioning.current = false;
    });
  }, []);

  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error("useTheme must be used inside ThemeProvider");
  return value;
}
