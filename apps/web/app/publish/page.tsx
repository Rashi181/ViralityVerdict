import { AppShell } from "../../features/navigation/AppShell";
import { PublishingEligibility } from "../../features/publishing/PublishingEligibility";

export default function PublishPage() { return <AppShell title="Publish and learn" description="You always publish manually. Later, authorized performance sync can improve future recommendations."><PublishingEligibility /></AppShell>; }
