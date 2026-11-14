import { OnboardingForm } from "../../features/auth/OnboardingForm";
import { DemoImportButton } from "../../features/imports/DemoImportButton";
import { CsvImportForm } from "../../features/imports/CsvImportForm";
import { InstagramStatus } from "../../features/imports/InstagramStatus";
import { CreatorSummary } from "../../features/creator/CreatorSummary";
import { AudiencePersonaPanel } from "../../features/audience/AudiencePersonaPanel";
import { TrendFeed } from "../../features/trends/TrendFeed";
import { OpportunityList } from "../../features/opportunities/OpportunityList";
import { VideoUpload } from "../../features/videos/VideoUpload";
import { Optimizer } from "../../features/optimization/Optimizer";
import { Planner } from "../../features/planner/Planner";
import { Strategist } from "../../features/strategist/Strategist";
import { PublishingEligibility } from "../../features/publishing/PublishingEligibility";
export default function OnboardingPage() { return <main id="main-content" tabIndex={-1}><OnboardingForm /><InstagramStatus /><CsvImportForm /><DemoImportButton /><CreatorSummary /><AudiencePersonaPanel /><TrendFeed /><OpportunityList /><VideoUpload /><Optimizer /><Planner /><Strategist /><PublishingEligibility /></main>; }
