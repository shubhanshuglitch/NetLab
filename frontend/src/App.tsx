import React from 'react'
import { Navbar } from './components/layout/Navbar'
import { GlobalSearchModal } from './components/layout/GlobalSearchModal'
import { HomePage } from './pages/Home/HomePage'
import { LearnPage } from './pages/Learn/LearnPage'
import { ScenariosPage } from './pages/Scenarios/ScenariosPage'
import { NetworkLabPage } from './pages/NetworkLab/NetworkLabPage'
import { InterviewLabPage } from './pages/InterviewLab/InterviewLabPage'
import { ProgressPage } from './pages/Progress/ProgressPage'
import { useNetLabStore } from './stores/useNetLabStore'
import { Network, Heart } from 'lucide-react'

export const App: React.FC = () => {
  const { activeTab, setActiveTab } = useNetLabStore()

  const renderActivePage = () => {
    switch (activeTab) {
      case 'home':
        return <HomePage />
      case 'learn':
        return <LearnPage />
      case 'scenarios':
        return <ScenariosPage />
      case 'network-lab':
        return <NetworkLabPage />
      case 'interview-lab':
        return <InterviewLabPage />
      case 'progress':
        return <ProgressPage />
      default:
        return <HomePage />
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#F7F7F5] text-[#202124]">
      {/* Top Navbar */}
      <Navbar />

      {/* Global Search Modal */}
      <GlobalSearchModal />

      {/* Main Page Content */}
      <main className="flex-1 pb-12">
        {renderActivePage()}
      </main>

      {/* Footer */}
      <footer className="border-t border-[#E8E8E5] bg-[#FFFFFF] py-6 px-4">
        <div className="mx-auto max-w-7xl flex flex-col sm:flex-row items-center justify-between text-xs text-[#6B7280] gap-3">
          <div className="flex items-center space-x-2">
            <div className="flex h-5 w-5 items-center justify-center rounded bg-[#4F6BED] text-white">
              <Network className="h-3 w-3" />
            </div>
            <span className="font-semibold text-[#202124]">NetLab</span>
            <span>— Understand Networks. See Every Packet. Learn by Experimenting.</span>
          </div>

          <div className="flex items-center space-x-4">
            <button onClick={() => setActiveTab('learn')} className="hover:text-[#202124]">Concepts</button>
            <button onClick={() => setActiveTab('scenarios')} className="hover:text-[#202124]">Scenarios</button>
            <button onClick={() => setActiveTab('network-lab')} className="hover:text-[#202124]">Network Lab</button>
            <button onClick={() => setActiveTab('interview-lab')} className="hover:text-[#202124]">Interview Prep</button>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
