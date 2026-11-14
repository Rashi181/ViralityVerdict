import { AppShell } from "../../features/navigation/AppShell";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { CreatorSummary } from "../../features/creator/CreatorSummary";

export default function DashboardPage() { return <AppShell title="Your creator dashboard" description="Start with what Verdict can actually observe. Empty states explain what data is needed next."><InstagramStatus /><CreatorSummary /></AppShell>; }
