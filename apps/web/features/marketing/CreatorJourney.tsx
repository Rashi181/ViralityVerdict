"use client";

import { useState } from "react";

const stages = [
  ["Connect authorized history", "Official Meta read-only access or a creator-permitted import. Verdict never asks for an Instagram password.", "⌁"],
  ["Understand creator patterns", "Separate observed captions, hashtags, formats, and performance from hypotheses about what to test.", "◌"],
  ["Ground audience personas", "Use available aggregate audience evidence. Persona reactions remain simulated and clearly labeled.", "◎"],
  ["Find content opportunities", "Combine the creator’s history, audience context, and sourced trends where available.", "✦"],
  ["Review a private draft", "Inspect a creator-uploaded Reel before publishing. Missing analysis inputs stay visibly unavailable.", "◫"],
  ["Publish manually", "Verdict never posts, comments, messages, deletes, or edits an Instagram account.", "✓"],
];

export function CreatorJourney() {
  const [selected, setSelected] = useState(0);
  const [title, detail, icon] = stages[selected];
  return <section className="creator-journey" id="how-it-works" aria-labelledby="journey-heading"><header><p>How it works</p><h2 id="journey-heading">A deliberate path from context to a better Reel.</h2></header><div className="journey-layout"><div className="journey-orbit" aria-label="Six stages of the Verdict workflow"><div className="journey-core"><span>Creator context</span><strong>Your next Reel,<br />backed by context.</strong></div>{stages.map(([stageTitle, , stageIcon], index) => <button className={selected === index ? "is-active" : ""} type="button" key={stageTitle} aria-pressed={selected === index} onClick={() => setSelected(index)}><i>{stageIcon}</i><b>{String(index + 1).padStart(2, "0")}</b><span className="sr-only">{stageTitle}</span></button>)}</div><article className="journey-detail"><div><p>Stage {String(selected + 1).padStart(2, "0")} of 06</p><span>{selected === 0 ? "Read-only by design" : "Creator-controlled workflow"}</span></div><h3>{title}</h3><strong>{detail}</strong><footer>{stages.map(([stageTitle], index) => <button key={stageTitle} type="button" className={selected === index ? "is-active" : ""} onClick={() => setSelected(index)} aria-label={`Show stage ${index + 1}: ${stageTitle}`}>{String(index + 1).padStart(2, "0")}</button>)}</footer></article></div></section>;
}
