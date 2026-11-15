import { AppShell } from "../../features/navigation/AppShell";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { InstagramSafety } from "../../features/imports/InstagramSafety";
import { DemoFixtureControl } from "../../features/demo/DemoFixtureControl";

export default function ConnectPage() { return <AppShell title="Connect Instagram" description="Connect your professional account through Meta. Verdict reads only eligible creator data and cannot publish or change your account."><InstagramStatus /><InstagramSafety /><DemoFixtureControl /></AppShell>; }
