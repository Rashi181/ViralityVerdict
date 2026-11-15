import Link from "next/link";
import { CreatorJourney } from "./CreatorJourney";

const features = [
  ["Understand", "See creator-history patterns, caption keywords, hashtags, and clear limits."],
  ["Discover", "Prioritize personalized Reel opportunities with transparent reasoning."],
  ["Review", "Upload a private draft and improve it before you publish manually."],
  ["Write", "Explore relevant captions and hashtag directions that fit your content."],
  ["Plan", "Save ideas and drafts, compare experiments, and organize what comes next."],
  ["Learn", "Later, compare actual accessible performance with what Verdict suggested."],
];

export function LandingOverview() {
  return <>
    <section className="landing-overview" aria-labelledby="overview-heading">
      <header><p>What Verdict does</p><h2 id="overview-heading">A creator strategy workspace, before you publish.</h2><span>Verdict turns authorized creator context into ideas, private draft feedback, and a clearer next move.</span></header>
      <ol className="landing-flow"><li><b>01</b><strong>Connect</strong><span>Use official, read-only access when available—or your own permitted import.</span></li><li><b>02</b><strong>Understand</strong><span>Separate observed history from inferences and simulations.</span></li><li><b>03</b><strong>Create</strong><span>Choose an idea, review a private draft, then publish yourself.</span></li></ol>
      <div className="landing-feature-grid">{features.map(([title, copy], index) => <article key={title}><i>{String(index + 1).padStart(2, "0")}</i><h3>{title}</h3><p>{copy}</p></article>)}</div>
    </section>
    <section className="landing-safety"><div><p>Creator control</p><h2>Your account stays yours.</h2><span>Verdict is designed for read-only analysis. It does not publish, delete, comment, message, or edit an Instagram account.</span></div><Link href="/connect">See connection safety</Link></section>
    <CreatorJourney />
  </>;
}
