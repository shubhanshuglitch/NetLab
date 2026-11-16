import React from 'react'
import {
  Award,
  BookOpen,
  Layers,
  HelpCircle,
  Bookmark,
  CheckCircle2,
  RotateCcw,
  Sparkles,
  ArrowRight
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const ProgressPage: React.FC = () => {
  const {
    completedConcepts,
    completedScenarios,
    answeredQuestions,
    bookmarkedQuestions,
    setActiveTab
  } = useNetLabStore()

  const totalAnswered = Object.keys(answeredQuestions).length
  const totalCorrect = Object.values(answeredQuestions).filter(Boolean).length
  const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0

  const handleClearProgress = () => {
    if (confirm('Are you sure you want to reset all learning progress and bookmarks?')) {
      localStorage.removeItem('netlab_concepts')
      localStorage.removeItem('netlab_scenarios')
      localStorage.removeItem('netlab_answers')
      localStorage.removeItem('netlab_bookmarks')
      window.location.reload()
    }
  }

  const milestones = [
    {
      title: 'First Packet Transmitted',
      desc: 'Executed your first network simulation in NetLab',
      achieved: completedScenarios.length > 0
    },
    {
      title: 'Layer 2 Master',
      desc: 'Explored CRC-32 bit division and ARQ sliding windows',
      achieved: completedConcepts.includes('concept-crc') || completedConcepts.includes('concept-arq')
    },
    {
      title: 'IP Routing Specialist',
      desc: 'Computed Dijkstra shortest paths and MTU fragmentation',
      achieved: completedConcepts.includes('concept-dijkstra') || completedConcepts.includes('concept-fragmentation')
    },
    {
      title: 'Interview Ace',
      desc: 'Solved 10 or more technical interview questions',
      achieved: totalCorrect >= 10
    }
  ]

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E8E8E5] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[#202124]">Learning Progress & Mastery</h1>
          <p className="text-xs text-[#6B7280]">
            Track your journey through computer networking concepts, simulation experiments, and interview preparation.
          </p>
        </div>

        <button
          onClick={handleClearProgress}
          className="flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-[#E8E8E5] text-xs text-[#D9534F] hover:bg-red-50 transition-colors"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          <span>Reset Progress</span>
        </button>
      </div>

      {/* High-Level Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white shadow-xs">
          <div className="flex items-center justify-between text-xs text-[#6B7280] mb-1">
            <span>Concepts Mastered</span>
            <BookOpen className="h-4 w-4 text-[#4F6BED]" />
          </div>
          <div className="text-2xl font-bold text-[#202124]">{completedConcepts.length} / 6</div>
          <div className="mt-2 h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
            <div className="h-full bg-[#4F6BED]" style={{ width: `${(completedConcepts.length / 6) * 100}%` }} />
          </div>
        </div>

        <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white shadow-xs">
          <div className="flex items-center justify-between text-xs text-[#6B7280] mb-1">
            <span>Scenarios Simulated</span>
            <Layers className="h-4 w-4 text-[#25845A]" />
          </div>
          <div className="text-2xl font-bold text-[#202124]">{completedScenarios.length} / 7</div>
          <div className="mt-2 h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
            <div className="h-full bg-[#25845A]" style={{ width: `${(completedScenarios.length / 7) * 100}%` }} />
          </div>
        </div>

        <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white shadow-xs">
          <div className="flex items-center justify-between text-xs text-[#6B7280] mb-1">
            <span>Questions Solved</span>
            <HelpCircle className="h-4 w-4 text-[#D89A38]" />
          </div>
          <div className="text-2xl font-bold text-[#202124]">{totalCorrect} / {totalAnswered}</div>
          <div className="text-[11px] text-[#6B7280] mt-1">Accuracy: <strong className="text-[#202124]">{accuracy}%</strong></div>
        </div>

        <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white shadow-xs">
          <div className="flex items-center justify-between text-xs text-[#6B7280] mb-1">
            <span>Bookmarked Items</span>
            <Bookmark className="h-4 w-4 text-purple-600" />
          </div>
          <div className="text-2xl font-bold text-[#202124]">{bookmarkedQuestions.length}</div>
          <div className="text-[11px] text-[#6B7280] mt-1">Saved for review</div>
        </div>
      </div>

      {/* Milestones & Badges */}
      <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-4">
        <div className="flex items-center space-x-2">
          <Award className="h-5 w-5 text-[#D89A38]" />
          <h2 className="text-base font-bold text-[#202124]">Learning Milestones</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {milestones.map((m, i) => (
            <div
              key={i}
              className={`p-3.5 rounded-xl border transition-all ${
                m.achieved
                  ? 'bg-amber-50/40 border-amber-200 text-amber-950'
                  : 'bg-[#FAFAFA] border-[#E8E8E5] text-[#9CA3AF] opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold">{m.title}</span>
                {m.achieved ? (
                  <CheckCircle2 className="h-4 w-4 text-amber-600" />
                ) : (
                  <span className="text-[10px]">Locked</span>
                )}
              </div>
              <p className="text-[11px] leading-snug">{m.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Bookmarked Questions Quick List */}
      <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bookmark className="h-4 w-4 text-[#4F6BED]" />
            <h2 className="text-base font-bold text-[#202124]">Bookmarked Questions ({bookmarkedQuestions.length})</h2>
          </div>
          {bookmarkedQuestions.length > 0 && (
            <button
              onClick={() => setActiveTab('interview-lab')}
              className="flex items-center space-x-1 text-xs font-semibold text-[#4F6BED] hover:underline"
            >
              <span>Practice in Interview Lab</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          )}
        </div>

        {bookmarkedQuestions.length === 0 ? (
          <p className="text-xs text-[#9CA3AF] py-4 text-center">
            No questions bookmarked yet. Click the bookmark icon on any interview question to save it here.
          </p>
        ) : (
          <div className="space-y-2">
            {bookmarkedQuestions.map((qId) => (
              <div
                key={qId}
                onClick={() => setActiveTab('interview-lab')}
                className="flex items-center justify-between p-3 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] text-xs hover:border-[#4F6BED] cursor-pointer transition-colors"
              >
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-[10px] text-gray-500">{qId.toUpperCase()}</span>
                  <span className="font-semibold text-[#202124]">Saved Interview Question</span>
                </div>
                <ArrowRight className="h-3.5 w-3.5 text-[#9CA3AF]" />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

