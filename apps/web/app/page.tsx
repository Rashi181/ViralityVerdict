import { HealthPanel } from "../features/system/HealthPanel";

export default function HomePage() {
  return (
    <main>
      <p className="eyebrow">Verdict · foundation</p>
      <h1>Create the next Reel with evidence, not guesswork.</h1>
      <p className="intro">
        This foundation checks the real API connection. Creator intelligence, analytics, and
        recommendations are not available yet.
      </p>
      <HealthPanel />
    </main>
  );
}
