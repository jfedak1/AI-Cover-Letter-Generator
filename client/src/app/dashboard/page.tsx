import Stats from './Stats'
import CoverLetterHistory from './CoverLetterHistory'
import GettingStarted from './GettingStarted'

export default function DashboardHome() {
  return (
    <div className="space-y-4 grid gap-10">
      <GettingStarted />
      <Stats />
      <CoverLetterHistory />
    </div>
  );
}