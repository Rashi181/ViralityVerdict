import { OnboardingForm } from "../../features/auth/OnboardingForm";
import { DemoImportButton } from "../../features/imports/DemoImportButton";
import { CsvImportForm } from "../../features/imports/CsvImportForm";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { CreatorSummary } from "../../features/creator/CreatorSummary";
import { AudiencePersonaPanel } from "../../features/audience/AudiencePersonaPanel";
export default function OnboardingPage() { return <main><OnboardingForm /><InstagramStatus /><CsvImportForm /><DemoImportButton /><CreatorSummary /><AudiencePersonaPanel /></main>; }
