import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./styles.css";
import "./workspace-theme.css";
import { ThemeProvider } from "../features/theme/ThemeProvider";

export const metadata: Metadata = {
  title: "Verdict — creator intelligence",
  description: "Evidence-backed, pre-publication Instagram creator strategy. Never automatic publishing.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body><a className="skip-link" href="#main-content">Skip to main content</a><ThemeProvider>{children}</ThemeProvider></body>
    </html>
  );
}
