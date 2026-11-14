import { AppShell } from "../../features/navigation/AppShell";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { CsvImportForm } from "../../features/imports/CsvImportForm";

export default function ConnectPage() { return <AppShell title="Connect and import" description="Use official Instagram authorization when it is ready, or import only data you are allowed to use."><InstagramStatus /><CsvImportForm /></AppShell>; }
