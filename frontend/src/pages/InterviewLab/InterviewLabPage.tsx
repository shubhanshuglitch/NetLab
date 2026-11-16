import React, { useState, useEffect } from 'react'
import {
  HelpCircle,
  CheckCircle,
  XCircle,
  Bookmark,
  BookmarkCheck,
  ChevronRight,
  ChevronLeft,
  ArrowRight,
  Flame,
  Award,
  BookOpen,
  Filter,
  Sparkles
} from 'lucide-react'
import {
  fetchInterviewQuestions,
  fetchInterviewCategories,
  verifyInterviewAnswer
} from '../../services/api'
import { InterviewQuestion, VerifyAnswerResponse } from '../../types'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const InterviewLabPage: React.FC = () => {
  const {
    answeredQuestions,
    bookmarkedQuestions,
    recordQuestionAnswer,
    toggleBookmarkQuestion,
    setActiveTab
  } = useNetLabStore()

  const [questions, setQuestions] = useState<InterviewQuestion[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All')
  const [currentIdx, setCurrentIdx] = useState<number>(0)
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [verifiedResult, setVerifiedResult] = useState<VerifyAnswerResponse | null>(null)
  const [showBookmarksOnly, setShowBookmarksOnly] = useState<boolean>(false)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    fetchInterviewCategories().then((cats) => setCategories(cats)).catch(console.error)
  }, [])

  useEffect(() => {
    setLoading(true)
    const cat = selectedCategory === 'All' ? undefined : selectedCategory
    const diff = selectedDifficulty === 'All' ? undefined : selectedDifficulty

    fetchInterviewQuestions(cat, diff)
      .then((qs) => {
        setQuestions(qs)
        setCurrentIdx(0)
        setSelectedOption(null)
        setVerifiedResult(null)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [selectedCategory, selectedDifficulty])

  const currentQ = questions[currentIdx]

  const handleSelectOption = (idx: number) => {
    if (verifiedResult) return // already submitted
    setSelectedOption(idx)
  }

  const handleSubmitAnswer = async () => {
    if (!currentQ || selectedOption === null) return
    try {
      const res = await verifyInterviewAnswer(currentQ.id, selectedOption)
      setVerifiedResult(res)
      recordQuestionAnswer(currentQ.id, res.is_correct)
    } catch (err) {
      console.error(err)
    }
  }

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1)
      setSelectedOption(null)
      setVerifiedResult(null)
    }
  }

  const handlePrev = () => {
    if (currentIdx > 0) {
      setCurrentIdx(currentIdx - 1)
      setSelectedOption(null)
      setVerifiedResult(null)
    }
  }

  const isBookmarked = currentQ && bookmarkedQuestions.includes(currentQ.id)
  const isAnswered = currentQ && currentQ.id in answeredQuestions

  const totalAnswered = Object.keys(answeredQuestions).length
  const totalCorrect = Object.values(answeredQuestions).filter(Boolean).length
  const accuracyRate = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6 space-y-6">
      {/* Header & Stats Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E8E8E5] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[#202124]">Computer Networks Interview Lab</h1>
          <p className="text-xs text-[#6B7280]">
            50+ Technical questions asked at Google, Amazon, Meta, and high-frequency network engineering interviews.
          </p>
        </div>

        {/* Stats Pill */}
        <div className="flex items-center space-x-3 text-xs bg-white p-2 px-3 rounded-xl border border-[#E8E8E5]">
          <div>
            <span className="text-[#6B7280]">Solved: </span>
            <strong className="text-[#202124]">{totalCorrect} / {totalAnswered}</strong>
          </div>
          <span className="text-[#D1D5DB]">|</span>
          <div>
            <span className="text-[#6B7280]">Accuracy: </span>
            <strong className={accuracyRate >= 70 ? 'text-[#25845A]' : 'text-[#D89A38]'}>{accuracyRate}%</strong>
          </div>
          <span className="text-[#D1D5DB]">|</span>
          <div className="flex items-center space-x-1">
            <Bookmark className="h-3.5 w-3.5 text-[#4F6BED]" />
            <strong className="text-[#202124]">{bookmarkedQuestions.length}</strong>
          </div>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-xl border border-[#E8E8E5]">
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <Filter className="h-3.5 w-3.5 text-[#6B7280]" />
          <span className="text-[#6B7280] font-medium">Category:</span>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="rounded-md border border-[#E8E8E5] bg-[#F7F7F5] px-2 py-1 text-xs text-[#202124]"
          >
            <option value="All">All Categories ({categories.length})</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <span className="text-[#6B7280] font-medium ml-2">Difficulty:</span>
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="rounded-md border border-[#E8E8E5] bg-[#F7F7F5] px-2 py-1 text-xs text-[#202124]"
          >
            <option value="All">All Levels</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>

        <span className="text-xs font-mono text-[#6B7280]">
          Question {currentIdx + 1} of {questions.length}
        </span>
      </div>

      {/* Question Card */}
      {loading ? (
        <div className="py-16 text-center text-xs text-[#6B7280]">Loading questions...</div>
      ) : currentQ ? (
        <div className="p-6 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-5">
          {/* Question Metadata & Bookmark */}
          <div className="flex items-center justify-between border-b border-[#E8E8E5] pb-3">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-50 text-[#4F6BED]">
                {currentQ.category}
              </span>
              <span className="text-xs font-medium text-[#6B7280]">• {currentQ.difficulty}</span>
              {isAnswered && (
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${answeredQuestions[currentQ.id] ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'}`}>
                  {answeredQuestions[currentQ.id] ? 'Previously Solved' : 'Previously Attempted'}
                </span>
              )}
            </div>

            <button
              onClick={() => toggleBookmarkQuestion(currentQ.id)}
              className={`p-1.5 rounded-lg border transition-colors ${
                isBookmarked
                  ? 'bg-amber-50 border-amber-300 text-[#D89A38]'
                  : 'border-[#E8E8E5] text-[#9CA3AF] hover:text-[#202124]'
              }`}
              title={isBookmarked ? 'Remove Bookmark' : 'Bookmark this question'}
            >
              {isBookmarked ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
            </button>
          </div>

          {/* Question Text */}
          <h2 className="text-lg font-bold text-[#202124] leading-snug">
            {currentQ.question}
          </h2>

          {/* Options List */}
          <div className="space-y-2.5 pt-2">
            {currentQ.options.map((opt, idx) => {
              const isSelected = selectedOption === idx
              const isVerified = verifiedResult !== null
              const isCorrectOpt = verifiedResult?.correct_option_index === idx
              const isChosenWrong = isVerified && isSelected && !verifiedResult.is_correct

              let btnStyle = 'border-[#E8E8E5] bg-[#FAFAFA] hover:bg-[#F7F7F5] text-[#202124]'
              if (isSelected && !isVerified) {
                btnStyle = 'border-[#4F6BED] bg-blue-50/50 text-[#4F6BED] font-semibold ring-1 ring-[#4F6BED]'
              }
              if (isVerified) {
                if (isCorrectOpt) {
                  btnStyle = 'border-[#25845A] bg-emerald-50 text-emerald-900 font-semibold'
                } else if (isChosenWrong) {
                  btnStyle = 'border-[#D9534F] bg-red-50 text-red-900 font-semibold'
                } else {
                  btnStyle = 'border-[#E8E8E5] opacity-50 text-gray-500'
                }
              }

              return (
                <div
                  key={idx}
                  onClick={() => handleSelectOption(idx)}
                  className={`flex items-start space-x-3 p-3.5 rounded-xl border text-xs cursor-pointer transition-all ${btnStyle}`}
                >
                  <div className="flex h-5 w-5 items-center justify-center rounded-full border border-current font-bold text-[10px] shrink-0 mt-0.5">
                    {String.fromCharCode(65 + idx)}
                  </div>
                  <div className="flex-1 leading-relaxed">{opt}</div>
                  {isVerified && isCorrectOpt && <CheckCircle className="h-4 w-4 text-[#25845A] shrink-0" />}
                  {isVerified && isChosenWrong && <XCircle className="h-4 w-4 text-[#D9534F] shrink-0" />}
                </div>
              )
            })}
          </div>

          {/* Action Row */}
          <div className="flex items-center justify-between pt-3 border-t border-[#E8E8E5]">
            <div className="flex items-center space-x-2">
              <button
                onClick={handlePrev}
                disabled={currentIdx === 0}
                className="flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-[#E8E8E5] text-xs text-[#6B7280] hover:text-[#202124] disabled:opacity-40"
              >
                <ChevronLeft className="h-4 w-4" />
                <span>Previous</span>
              </button>
              <button
                onClick={handleNext}
                disabled={currentIdx === questions.length - 1}
                className="flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-[#E8E8E5] text-xs text-[#6B7280] hover:text-[#202124] disabled:opacity-40"
              >
                <span>Next</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>

            {!verifiedResult ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={selectedOption === null}
                className="px-5 py-2 rounded-xl bg-[#4F6BED] text-xs font-bold text-white hover:bg-[#3E58D6] disabled:opacity-50 transition-colors"
              >
                Submit Answer
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={currentIdx === questions.length - 1}
                className="flex items-center space-x-1 px-5 py-2 rounded-xl bg-[#202124] text-xs font-bold text-white hover:bg-black transition-colors"
              >
                <span>Next Question</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            )}
          </div>

          {/* VERIFIED EVALUATION & EXPLANATION ACCORDION */}
          {verifiedResult && (
            <div className="pt-4 border-t border-[#E8E8E5] space-y-4 animate-in fade-in duration-200">
              {/* Correctness banner */}
              <div
                className={`flex items-center space-x-2.5 p-3 rounded-xl border ${
                  verifiedResult.is_correct
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                    : 'bg-red-50 border-red-200 text-red-900'
                }`}
              >
                {verifiedResult.is_correct ? (
                  <CheckCircle className="h-5 w-5 text-[#25845A]" />
                ) : (
                  <XCircle className="h-5 w-5 text-[#D9534F]" />
                )}
                <div className="text-xs">
                  <strong>{verifiedResult.is_correct ? 'Correct Answer!' : 'Incorrect Choice.'}</strong>{' '}
                  Option {String.fromCharCode(65 + verifiedResult.correct_option_index)} is the standard RFC protocol behavior.
                </div>
              </div>

              {/* In-depth explanation */}
              <div className="p-4 rounded-xl bg-[#F7F7F5] border border-[#E8E8E5] space-y-1.5 text-xs">
                <span className="font-bold text-[#202124]">Detailed Technical Explanation:</span>
                <p className="text-[#4B5563] leading-relaxed">{verifiedResult.explanation}</p>
              </div>

              {/* Why alternative options are wrong */}
              {verifiedResult.why_incorrect && (
                <div className="p-4 rounded-xl bg-white border border-[#E8E8E5] space-y-2 text-xs">
                  <span className="font-bold text-[#202124]">Why Alternative Answers Are Incorrect:</span>
                  <div className="space-y-1">
                    {verifiedResult.why_incorrect.map((why, i) => (
                      <div key={i} className="text-[#6B7280] leading-snug">
                        <strong className="text-[#202124]">Option {String.fromCharCode(65 + i)}:</strong> {why}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Follow-up question */}
              {verifiedResult.follow_up && (
                <div className="p-4 rounded-xl bg-purple-50/40 border border-purple-200 space-y-1.5 text-xs">
                  <span className="font-bold text-purple-900 flex items-center space-x-1.5">
                    <Sparkles className="h-3.5 w-3.5 text-purple-600" />
                    <span>Interviewer Follow-up Question:</span>
                  </span>
                  <p className="text-purple-950 font-medium">{verifiedResult.follow_up}</p>
                  <p className="text-[#4B5563] pt-1 leading-relaxed">{verifiedResult.follow_up_answer}</p>
                </div>
              )}

              {/* Cross link to scenario */}
              {verifiedResult.scenario_link && (
                <div className="flex items-center justify-between p-3 rounded-xl bg-blue-50/40 border border-blue-200 text-xs">
                  <span className="text-blue-900">
                    Want to see this protocol behavior in action?
                  </span>
                  <button
                    onClick={() => setActiveTab('scenarios')}
                    className="flex items-center space-x-1 font-semibold text-[#4F6BED] hover:underline"
                  >
                    <span>Run Visual Scenario</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="py-12 text-center text-xs text-[#6B7280]">
          No questions matching selected filters.
        </div>
      )}
    </div>
  )
}

