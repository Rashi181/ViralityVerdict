import { AppShell } from "../../features/navigation/AppShell";
import { CreatorSummary } from "../../features/creator/CreatorSummary";
import { AudiencePersonaPanel } from "../../features/audience/AudiencePersonaPanel";
import { TrendFeed } from "../../features/trends/TrendFeed";

export default function InsightsPage() { return <AppShell title="Creator and audience insights" description="Separate observed creator evidence from inferred planning guidance and simulated personas."><CreatorSummary /><AudiencePersonaPanel /><TrendFeed /></AppShell>; }
