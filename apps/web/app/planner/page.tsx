import { AppShell } from "../../features/navigation/AppShell";
import { Planner } from "../../features/planner/Planner";

export default function PlannerPage() { return <AppShell title="Planner and experiments" description="Organize ideas and drafts. A planned status never means Verdict published anything."><Planner /></AppShell>; }
