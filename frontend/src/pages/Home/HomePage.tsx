import React, { useState } from 'react'
import {
  Network,
  Search,
  BookOpen,
  Layers,
  HelpCircle,
  ArrowRight,
  Zap,
  ShieldCheck,
  Activity,
  Award,
  Sparkles
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const HomePage: React.FC = () => {
  const {
    setActiveTab,
    setSearchOpen,
    completedConcepts,
    completedScenarios,
    answeredQuestions
  } = useNetLabStore()

  const [searchVal, setSearchVal] = useState('')

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSearchOpen(true)
  }

  const featuredScenarios = [
    {
      id: 'scenario-youtube-tabs',
      title: 'Two YouTube Tabs on One Laptop',
      subtitle: 'Ephemeral Ports & Socket Multiplexing',
      category: 'Browser & Web',
      difficulty: 'Beginner',
      question: 'How does your OS know which audio belongs to which video tab?'
    },
    {
      id: 'scenario-two-laptops-wifi',
      title: 'Two Laptops Sharing One Wi-Fi',
      subtitle: 'NAT & Port Address Translation (PAT)',
      category: 'Infrastructure',
      difficulty: 'Intermediate',
      question: 'How do multiple home devices share a single public IPv4 address without collision?'
    },
    {
      id: 'scenario-url-journey',
      title: 'What Happens When You Enter google.com?',
      subtitle: 'Full 5-Layer Stack Protocol Flow',
      category: 'Browser & Web',
      difficulty: 'Intermediate',
      question: 'DNS → ARP → TCP Handshake → TLS → HTTP: the complete journey.'
    },
    {
      id: 'scenario-webrtc-videocall',
      title: 'Video Calling (UDP) vs File Download (TCP)',
      subtitle: 'Head-of-Line Blocking vs Real-Time Flow',
      category: 'Real Apps',
      difficulty: 'Intermediate',
      question: 'Why does Zoom use UDP while Google Drive downloads use TCP?'
    }
  ]

  const solvedCount = Object.values(answeredQuestions).filter(Boolean).length

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8 space-y-10">
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-[#E8E8E5] bg-white text-xs text-[#6B7280] shadow-xs">
          <Sparkles className="h-3.5 w-3.5 text-[#4F6BED]" />
          <span>No static diagrams. Realistic, packet-level interactive simulation.</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-[#202124] tracking-tight leading-tight">
          Understand Networks. <br className="hidden sm:inline" />
          <span className="text-[#4F6BED]">See Every Packet.</span> Learn by Experimenting.
        </h1>

        <p className="text-sm sm:text-base text-[#6B7280] leading-relaxed">
          Computer Networks is best understood when you can watch packets move, change router configurations,
          intentionally introduce packet drops, inspect headers, and understand exactly why something happens.
        </p>

        {/* Prominent Search Bar */}
        <form onSubmit={handleSearchSubmit} className="pt-2 max-w-xl mx-auto">
          <div className="relative flex items-center shadow-sm">
            <Search className="absolute left-4 h-5 w-5 text-[#9CA3AF]" />
            <input
              type="text"
              value={searchVal}
              onChange={(e) => setSearchVal(e.target.value)}
              onClick={() => setSearchOpen(true)}
              placeholder="What networking concept are you confused about? (e.g. NAT, TCP handshake, MTU)"
              className="w-full rounded-xl border border-[#E8E8E5] bg-white py-3.5 pl-11 pr-24 text-sm text-[#202124] placeholder-[#9CA3AF] focus:border-[#4F6BED] focus:outline-hidden focus:ring-4 focus:ring-[#4F6BED]/10 transition-all cursor-pointer"
            />
            <button
              type="submit"
              className="absolute right-2 px-3.5 py-2 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6] transition-colors"
            >
              Explore
            </button>
          </div>
        </form>

        {/* Quick query chips */}
        <div className="flex flex-wrap items-center justify-center gap-1.5 pt-1 text-xs text-[#6B7280]">
          <span className="text-[11px] text-[#9CA3AF]">Popular searches:</span>
          {['TCP Handshake', 'Why YouTube tabs differ', 'DHCP DORA', 'NAT table', 'CRC-32'].map((tag) => (
            <button
              key={tag}
              onClick={() => setSearchOpen(true)}
              className="px-2.5 py-0.5 rounded-full border border-[#E8E8E5] bg-white hover:border-[#4F6BED] hover:text-[#4F6BED] text-[11px] transition-colors"
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Progress & Quick Stats Banner */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs">
        <div className="flex items-center space-x-3.5 border-b md:border-b-0 md:border-r border-[#E8E8E5] pb-3 md:pb-0 md:pr-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-[#4F6BED]">
            <BookOpen className="h-5 w-5" />
          </div>
          <div>
            <div className="text-lg font-bold text-[#202124]">{completedConcepts.length} / 6</div>
            <div className="text-xs text-[#6B7280]">Concepts Mastered</div>
          </div>
        </div>

        <div className="flex items-center space-x-3.5 border-b md:border-b-0 md:border-r border-[#E8E8E5] pb-3 md:pb-0 md:pr-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-[#25845A]">
            <Layers className="h-5 w-5" />
          </div>
          <div>
            <div className="text-lg font-bold text-[#202124]">{completedScenarios.length} / 7</div>
            <div className="text-xs text-[#6B7280]">Scenarios Simulated</div>
          </div>
        </div>

        <div className="flex items-center space-x-3.5 border-b md:border-b-0 md:border-r border-[#E8E8E5] pb-3 md:pb-0 md:pr-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-[#D89A38]">
            <HelpCircle className="h-5 w-5" />
          </div>
          <div>
            <div className="text-lg font-bold text-[#202124]">{solvedCount} / 50+</div>
            <div className="text-xs text-[#6B7280]">Interview Questions Solved</div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-[#202124]">Launch Network Lab</div>
            <div className="text-[11px] text-[#6B7280]">Build custom topologies</div>
          </div>
          <button
            onClick={() => setActiveTab('network-lab')}
            className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-[#202124] text-xs font-medium text-white hover:bg-black transition-colors"
          >
            <span>Open Lab</span>
            <ArrowRight className="h-3 w-3" />
          </button>
        </div>
      </div>

      {/* Featured Real-World Scenarios */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-[#202124]">Featured Real-World Scenarios</h2>
            <p className="text-xs text-[#6B7280]">
              Experiment with everyday internet situations and observe the packet-level reality.
            </p>
          </div>
          <button
            onClick={() => setActiveTab('scenarios')}
            className="flex items-center space-x-1 text-xs font-semibold text-[#4F6BED] hover:underline"
          >
            <span>View All 7 Scenarios</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {featuredScenarios.map((sc) => (
            <div
              key={sc.id}
              onClick={() => setActiveTab('scenarios')}
              className="flex flex-col justify-between p-5 rounded-2xl border border-[#E8E8E5] bg-white hover:border-[#4F6BED] hover:shadow-md transition-all cursor-pointer group"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#F7F7F5] text-[#6B7280]">
                    {sc.category}
                  </span>
                  <span className="text-[10px] font-medium text-[#25845A] bg-emerald-50 px-2 py-0.5 rounded-full">
                    {sc.difficulty}
                  </span>
                </div>
                <h3 className="text-base font-bold text-[#202124] group-hover:text-[#4F6BED] transition-colors">
                  {sc.title}
                </h3>
                <p className="text-xs font-medium text-[#4F6BED] mt-0.5">{sc.subtitle}</p>
                <p className="text-xs text-[#6B7280] mt-2 leading-relaxed bg-[#F7F7F5] p-2.5 rounded-lg border border-[#E8E8E5]">
                  {sc.question}
                </p>
              </div>

              <div className="flex items-center justify-between mt-4 pt-3 border-t border-[#E8E8E5] text-xs">
                <span className="text-[#9CA3AF]">Interactive topology & packet inspection</span>
                <span className="flex items-center space-x-1 font-semibold text-[#202124] group-hover:translate-x-1 transition-transform">
                  <span>Start Simulation</span>
                  <ArrowRight className="h-3.5 w-3.5 text-[#4F6BED]" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Layer-by-Layer Concept Visualizer Highlights */}
      <div className="rounded-2xl border border-[#E8E8E5] bg-[#FFFFFF] p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-[#202124]">Interactive Concept Visualizers</h2>
            <p className="text-xs text-[#6B7280]">
              Direct algorithmic implementations you can tweak and execute step-by-step.
            </p>
          </div>
          <button
            onClick={() => setActiveTab('learn')}
            className="flex items-center space-x-1 text-xs font-semibold text-[#4F6BED] hover:underline"
          >
            <span>Explore Concept Library</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {[
            {
              name: 'CRC-32 Modulo-2 Division',
              layer: 'Data Link Layer',
              desc: 'Enter custom bits and watch step-by-step XOR division remainder computation.'
            },
            {
              name: 'ARQ Sliding Window Comparison',
              layer: 'Data Link Layer',
              desc: 'Compare Stop-and-Wait, Go-Back-N, and Selective Repeat under injected frame drops.'
            },
            {
              name: 'Dijkstra Link-State Algorithm',
              layer: 'Network Layer',
              desc: 'Step through tentative distance tables and shortest-path tree construction.'
            },
            {
              name: 'IPv4 MTU Fragmentation',
              layer: 'Network Layer',
              desc: 'Calculates 8-byte aligned offsets, MF flags, and destination reassembly.'
            },
            {
              name: 'Hierarchical DNS Resolution',
              layer: 'Application Layer',
              desc: 'Simulate recursive lookups from Root (.) to TLD (.com) and Authoritative zone.'
            },
            {
              name: 'DHCP DORA 4-Way Sequence',
              layer: 'Application / Network',
              desc: 'Discover broadcast, lease offer, formal request, and IP allocation ACK.'
            }
          ].map((item, i) => (
            <div
              key={i}
              onClick={() => setActiveTab('learn')}
              className="p-3.5 rounded-xl border border-[#E8E8E5] bg-[#FAFAFA] hover:bg-white hover:border-[#4F6BED] transition-all cursor-pointer"
            >
              <div className="text-[10px] font-semibold text-[#4F6BED] uppercase tracking-wider mb-1">
                {item.layer}
              </div>
              <div className="text-xs font-bold text-[#202124]">{item.name}</div>
              <p className="text-[11px] text-[#6B7280] mt-1 leading-snug">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Interview Lab CTA */}
      <div className="flex flex-col sm:flex-row items-center justify-between p-6 rounded-2xl bg-gradient-to-r from-[#4F6BED]/10 via-[#4F6BED]/5 to-transparent border border-[#4F6BED]/20 gap-4">
        <div className="space-y-1 text-center sm:text-left">
          <div className="inline-flex items-center space-x-1.5 text-xs font-bold text-[#4F6BED] uppercase tracking-wider">
            <Award className="h-4 w-4" />
            <span>Interview Lab — 50+ Questions</span>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-[#202124]">
            Preparing for SWE or Computer Networks Interviews?
          </h3>
          <p className="text-xs text-[#6B7280] max-w-xl">
            Practice real engineering interview questions with interactive simulations, why-wrong rationale,
            and follow-up system design challenges.
          </p>
        </div>

        <button
          onClick={() => setActiveTab('interview-lab')}
          className="px-5 py-2.5 rounded-xl bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6] shadow-sm transition-colors whitespace-nowrap shrink-0"
        >
          Practice Interview Questions
        </button>
      </div>
    </div>
  )
}

