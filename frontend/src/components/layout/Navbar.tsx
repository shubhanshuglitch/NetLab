import React from 'react'
import {
  Network,
  BookOpen,
  Layers,
  FlaskConical,
  HelpCircle,
  Award,
  Search,
  Activity
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const Navbar: React.FC = () => {
  const { activeTab, setActiveTab, setSearchOpen, activeSimulation } = useNetLabStore()

  const navItems = [
    { id: 'home', label: 'Home', icon: Network },
    { id: 'learn', label: 'Learn', icon: BookOpen },
    { id: 'scenarios', label: 'Scenarios', icon: Layers },
    { id: 'network-lab', label: 'Network Lab', icon: FlaskConical },
    { id: 'interview-lab', label: 'Interview Lab', icon: HelpCircle },
    { id: 'progress', label: 'My Progress', icon: Award }
  ]

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#E8E8E5] bg-[#FFFFFF]/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
        {/* Brand */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('home')}>
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#4F6BED] text-white shadow-sm">
            <Network className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-semibold text-base text-[#202124] tracking-tight">NetLab</span>
              <span className="text-[10px] font-medium uppercase tracking-wider px-1.5 py-0.5 rounded bg-[#4F6BED]/10 text-[#4F6BED]">
                v1.0
              </span>
            </div>
            <p className="text-[11px] text-[#6B7280] leading-none hidden sm:block">Interactive Network Simulator</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = activeTab === item.id
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                  isActive
                    ? 'bg-[#4F6BED]/10 text-[#4F6BED] font-semibold'
                    : 'text-[#6B7280] hover:text-[#202124] hover:bg-[#F7F7F5]'
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? 'text-[#4F6BED]' : 'text-[#6B7280]'}`} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>

        {/* Right side actions: Global Search & Active Sim status */}
        <div className="flex items-center space-x-2">
          {activeSimulation && (
            <div
              onClick={() => setActiveTab('network-lab')}
              className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-[#25845A]/10 text-[#25845A] cursor-pointer hover:bg-[#25845A]/20 transition-colors"
            >
              <Activity className="h-3.5 w-3.5 animate-pulse" />
              <span>Sim Active ({activeSimulation.events.length} events)</span>
            </div>
          )}

          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center space-x-2 rounded-md border border-[#E8E8E5] bg-[#F7F7F5] px-2.5 py-1.5 text-xs text-[#6B7280] hover:border-[#D1D5DB] hover:text-[#202124] transition-all"
          >
            <Search className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Search concepts, protocols...</span>
            <kbd className="hidden sm:inline-block rounded border border-[#D1D5DB] bg-white px-1.5 text-[10px] text-[#9CA3AF]">
              Ctrl+K
            </kbd>
          </button>
        </div>
      </div>
    </header>
  )
}

