"use client";

import { useRef } from "react";
import { useTheme } from "./ThemeProvider";

export function ThemeToggle() {
  const button = useRef<HTMLButtonElement>(null);
  const { theme, toggleTheme } = useTheme();
  return <button ref={button} type="button" className="theme-toggle" aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`} onClick={() => {
    const rect = button.current?.getBoundingClientRect();
    toggleTheme(rect ? { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 } : undefined);
  }}><span aria-hidden="true">{theme === "dark" ? "☼" : "☾"}</span><i>{theme === "dark" ? "Light" : "Dark"}</i></button>;
}
