import { AppShell } from "../../features/navigation/AppShell";
import { OpportunityList } from "../../features/opportunities/OpportunityList";

export default function IdeasPage() { return <AppShell title="Content opportunities" description="Relative opportunity scores combine available audience, trend, novelty, and feasibility evidence."><OpportunityList /></AppShell>; }
