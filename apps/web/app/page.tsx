import { HealthPanel } from "../features/system/HealthPanel";
import Link from "next/link";

export default function HomePage() {
  return (
    <main id="main-content" tabIndex={-1}>
      <p className="eyebrow">Verdict · creator intelligence</p>
      <h1>Create the next Reel with evidence, not guesswork.</h1>
      <p className="intro">
        Plan, inspect, and improve your next Reel using clearly labeled creator evidence,
        hypotheses, and manual publishing handoff. Verdict never posts automatically.
      </p>
      <p><Link href="/sign-up">Create an account</Link> or <Link href="/sign-in">sign in</Link>.</p>
      <HealthPanel />
    </main>
  );
}
