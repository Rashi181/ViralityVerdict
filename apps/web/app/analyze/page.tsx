import { AppShell } from "../../features/navigation/AppShell";
import { VideoUpload } from "../../features/videos/VideoUpload";
import { ReelReadiness } from "../../features/videos/ReelReadiness";
import { Optimizer } from "../../features/optimization/Optimizer";

export default function AnalyzePage() { return <AppShell title="Reel analyzer" description="Upload a private draft, inspect real extraction evidence, then improve the caption and hashtag direction in the same focused workflow."><VideoUpload /><ReelReadiness /><Optimizer /></AppShell>; }
