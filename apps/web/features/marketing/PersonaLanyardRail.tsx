"use client";

import { useState } from "react";

const personas = [
  { id: "practical", initials: "PL", name: "The Practical Learner", focus: "Save-worthy tutorials", use: "Actionable steps, templates, and calm walkthroughs.", preference: "Screen recordings with clear overlays and pause-to-read pacing.", tone: "amber" },
  { id: "curious", initials: "CS", name: "The Curious Scroller", focus: "Quick mental models", use: "Rapid hooks, surprising facts, and counter-intuitive comparisons.", preference: "Visual transitions, open loops, and a clear payoff by the end.", tone: "coral" },
  { id: "time", initials: "TC", name: "The Time-Pressed Creator", focus: "Efficiency and workflow", use: "Shortcuts, repeatable systems, and practical before-and-afters.", preference: "Fast breakdowns, templates, and concise editing cues.", tone: "violet" },
  { id: "visual", initials: "VE", name: "The Visual Explorer", focus: "Aesthetic process", use: "Strong opening frames and transformation-led ideas.", preference: "Texture, visual contrast, and process shown before explanation.", tone: "rose" },
  { id: "research", initials: "IR", name: "The Intentional Researcher", focus: "Evidence-first choices", use: "Clear comparisons with constraints and honest tradeoffs.", preference: "On-screen criteria, sources where available, and direct conclusions.", tone: "blue" },
];

export function PersonaLanyardRail() {
  const [selected, setSelected] = useState(0);
  const visible = [selected, (selected + 1) % personas.length, (selected + 2) % personas.length].map((index) => personas[index]);

  return <section className="persona-lanyards" id="personas" aria-labelledby="persona-heading">
    <header className="persona-heading"><p>Persona preview</p><h2 id="persona-heading">A strategic lens—not a claim about one follower.</h2><span>When authorized aggregate audience context is available, Verdict creates clearly labeled simulated personas to test content choices. These are polished examples only.</span></header>
    <div className="lanyard-stage" role="group" aria-label="Example simulated audience personas"><div className="lanyard-rail" aria-hidden="true"><i /></div><div className="lanyard-items">{visible.map((persona) => <article className={`lanyard-persona ${persona.tone}`} key={persona.id}><div className="lanyard-clip" aria-hidden="true" /><div className="lanyard-strap" aria-hidden="true" /><div className="lanyard-metal" aria-hidden="true" /><div className="persona-badge"><div className="persona-badge-top"><span /><i /></div><div className="persona-initials">{persona.initials}</div><h3>{persona.name}</h3><b>SIMULATED PERSONA</b><dl><div><dt>Strategic use</dt><dd>{persona.use}</dd></div><div><dt>Content preference</dt><dd>{persona.preference}</dd></div></dl><footer>Example model · not an individual follower</footer></div></article>)}</div></div>
    <div className="persona-controls"><button type="button" aria-label="Previous personas" onClick={() => setSelected((current) => (current + personas.length - 1) % personas.length)}>←</button><p>{visible[0].name} · {visible[0].focus}</p><button type="button" aria-label="Next personas" onClick={() => setSelected((current) => (current + 1) % personas.length)}>→</button></div>
    <p className="persona-hint">All personas are explicitly simulated from permitted aggregate evidence when it is available.</p>
  </section>;
}
