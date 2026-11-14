import { AppShell } from "../../features/navigation/AppShell";
import { VideoUpload } from "../../features/videos/VideoUpload";

export default function AnalyzePage() { return <AppShell title="Analyze a Reel draft" description="Upload a private draft. Verdict shows only extraction results it can actually measure."><VideoUpload /></AppShell>; }
