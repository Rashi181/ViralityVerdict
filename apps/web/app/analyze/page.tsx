import { AppShell } from "../../features/navigation/AppShell";
import { VideoUpload } from "../../features/videos/VideoUpload";
import { ReelReadiness } from "../../features/videos/ReelReadiness";

export default function AnalyzePage() { return <AppShell title="Analyze a Reel draft" description="Upload a private draft, inspect real extraction evidence, then add AI analysis when a provider is authorized."><VideoUpload /><ReelReadiness /></AppShell>; }
