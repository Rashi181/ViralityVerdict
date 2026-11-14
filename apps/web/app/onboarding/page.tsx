import { OnboardingForm } from "../../features/auth/OnboardingForm";
import { DemoImportButton } from "../../features/imports/DemoImportButton";
import { CsvImportForm } from "../../features/imports/CsvImportForm";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { CreatorSummary } from "../../features/creator/CreatorSummary";
import { AudiencePersonaPanel } from "../../features/audience/AudiencePersonaPanel";
import { TrendFeed } from "../../features/trends/TrendFeed";
import { OpportunityList } from "../../features/opportunities/OpportunityList";
export default function OnboardingPage() { return <main><OnboardingForm /><InstagramStatus /><CsvImportForm /><DemoImportButton /><CreatorSummary /><AudiencePersonaPanel /><TrendFeed /><OpportunityList /></main>; }
