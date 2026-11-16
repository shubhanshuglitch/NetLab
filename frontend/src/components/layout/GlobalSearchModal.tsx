import React, { useState, useEffect } from 'react'
import { Search, X, BookOpen, Layers, HelpCircle, ArrowRight } from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'
import { searchAll } from '../../services/api'

export const GlobalSearchModal: React.FC = () => {
  const { isSearchOpen, setSearchOpen, setActiveTab } = useNetLabStore()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<{
    concepts: any[]
    scenarios: any[]
    interview_questions: any[]
  }>({ concepts: [], scenarios: [], interview_questions: [] })
  const [loading, setLoading] = useState(false)

  // Listen for Ctrl+K keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        setSearchOpen(!isSearchOpen)
      }
      if (e.key === 'Escape' && isSearchOpen) {
        setSearchOpen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isSearchOpen, setSearchOpen])

  useEffect(() => {
    if (!query.trim()) {
      setResults({ concepts: [], scenarios: [], interview_questions: [] })
      return
    }
    const timer = setTimeout(async () => {
      setLoading(true)
      try {
        const data = await searchAll(query)
        setResults(data)
      } catch (err) {
        console.error('Search error:', err)
      } finally {
        setLoading(false)
      }
    }, 200)
    return () => clearTimeout(timer)
  }, [query])

  if (!isSearchOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-2xl rounded-xl border border-[#E8E8E5] bg-[#FFFFFF] shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3 border-b border-[#E8E8E5]">
          <Search className="h-5 w-5 text-[#6B7280] mr-2.5 shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search e.g. 'TCP handshake', 'Why YouTube tabs are different', 'NAT', 'ARP'..."
            className="w-full bg-transparent text-sm text-[#202124] placeholder-[#9CA3AF] focus:outline-hidden"
            autoFocus
          />
          {query && (
            <button onClick={() => setQuery('')} className="p-1 hover:text-[#202124] text-[#9CA3AF] mr-1">
              <X className="h-4 w-4" />
            </button>
          )}
          <button
            onClick={() => setSearchOpen(false)}
            className="rounded px-1.5 py-0.5 text-xs text-[#6B7280] hover:bg-[#F7F7F5]"
          >
            Esc
          </button>
        </div>

        {/* Results Area */}
        <div className="max-h-[60vh] overflow-y-auto p-4 space-y-4">
          {loading && (
            <div className="py-8 text-center text-xs text-[#6B7280]">Searching NetLab knowledge base...</div>
          )}

          {!loading && !query && (
            <div className="py-6 text-center text-xs text-[#9CA3AF]">
              Try searching for <span className="font-medium text-[#4F6BED]">"TCP Tahoe"</span>,{' '}
              <span className="font-medium text-[#4F6BED]">"Dijkstra"</span>,{' '}
              <span className="font-medium text-[#4F6BED]">"Fragment offset"</span>, or{' '}
              <span className="font-medium text-[#4F6BED]">"Why two laptops share an IP"</span>.
            </div>
          )}

          {!loading && query && results.concepts.length === 0 && results.scenarios.length === 0 && results.interview_questions.length === 0 && (
            <div className="py-8 text-center text-xs text-[#6B7280]">
              No exact matches found for "{query}". Try a broader networking term.
            </div>
          )}

          {/* Concepts Section */}
          {results.concepts.length > 0 && (
            <div>
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">
                <BookOpen className="h-3.5 w-3.5 text-[#4F6BED]" />
                <span>Concept Visualizers</span>
              </div>
              <div className="space-y-1.5">
                {results.concepts.map((c) => (
                  <div
                    key={c.id}
                    onClick={() => {
                      setSearchOpen(false)
                      setActiveTab('learn')
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-[#F7F7F5] cursor-pointer transition-colors border border-transparent hover:border-[#E8E8E5]"
                  >
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-semibold text-[#202124]">{c.name}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-50 text-blue-600 font-medium">
                          {c.layer}
                        </span>
                      </div>
                      <p className="text-[11px] text-[#6B7280] line-clamp-1">{c.summary}</p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-[#9CA3AF] shrink-0" />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Scenarios Section */}
          {results.scenarios.length > 0 && (
            <div>
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">
                <Layers className="h-3.5 w-3.5 text-[#25845A]" />
                <span>Real-World Scenarios</span>
              </div>
              <div className="space-y-1.5">
                {results.scenarios.map((s) => (
                  <div
                    key={s.id}
                    onClick={() => {
                      setSearchOpen(false)
                      setActiveTab('scenarios')
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-[#F7F7F5] cursor-pointer transition-colors border border-transparent hover:border-[#E8E8E5]"
                  >
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-semibold text-[#202124]">{s.title}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 font-medium">
                          {s.category}
                        </span>
                      </div>
                      <p className="text-[11px] text-[#6B7280] line-clamp-1">{s.summary}</p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-[#9CA3AF] shrink-0" />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Interview Questions Section */}
          {results.interview_questions.length > 0 && (
            <div>
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">
                <HelpCircle className="h-3.5 w-3.5 text-[#D89A38]" />
                <span>Interview Questions</span>
              </div>
              <div className="space-y-1.5">
                {results.interview_questions.map((q) => (
                  <div
                    key={q.id}
                    onClick={() => {
                      setSearchOpen(false)
                      setActiveTab('interview-lab')
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-[#F7F7F5] cursor-pointer transition-colors border border-transparent hover:border-[#E8E8E5]"
                  >
                    <div>
                      <span className="text-xs font-medium text-[#202124] line-clamp-1">{q.question}</span>
                      <div className="flex items-center space-x-2 mt-0.5">
                        <span className="text-[10px] text-[#D89A38] font-medium">{q.category}</span>
                        <span className="text-[10px] text-[#9CA3AF]">• {q.difficulty}</span>
                      </div>
                    </div>
                    <ArrowRight className="h-4 w-4 text-[#9CA3AF] shrink-0" />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

