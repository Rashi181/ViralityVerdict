import { AppShell } from "../../features/navigation/AppShell";
import { CreatorSummary } from "../../features/creator/CreatorSummary";
import { AudiencePersonaPanel } from "../../features/audience/AudiencePersonaPanel";

export default function InsightsPage() { return <AppShell title="Creator intelligence" description="A focused view of the real creator and audience evidence Verdict can access today."><CreatorSummary /><AudiencePersonaPanel /></AppShell>; }
