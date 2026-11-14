import { AppShell } from "../../features/navigation/AppShell";
import { Strategist } from "../../features/strategist/Strategist";

export default function StrategistPage() { return <AppShell title="AI strategist" description="A scoped assistant that can only use your Verdict data when its provider is configured."><Strategist /></AppShell>; }
