import React, { useEffect } from 'react'
import {
  Play,
  Pause,
  SkipForward,
  SkipBack,
  RotateCcw,
  Sliders,
  Gauge
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const SimulationControls: React.FC = () => {
  const {
    activeSimulation,
    currentStepIndex,
    isPlaying,
    playbackSpeedMs,
    setIsPlaying,
    stepForward,
    stepBackward,
    resetSimulation,
    setPlaybackSpeedMs
  } = useNetLabStore()

  // Auto-play interval timer
  useEffect(() => {
    let timer: any = null
    if (isPlaying) {
      timer = setInterval(() => {
        stepForward()
      }, playbackSpeedMs)
    }
    return () => {
      if (timer) clearInterval(timer)
    }
  }, [isPlaying, playbackSpeedMs, stepForward])

  if (!activeSimulation) return null

  const totalSteps = activeSimulation.events.length
  const progressPercent = totalSteps > 0 ? ((currentStepIndex + 1) / totalSteps) * 100 : 0

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-3 p-3 rounded-xl border border-[#E8E8E5] bg-white shadow-xs">
      {/* Playback Button Group */}
      <div className="flex items-center space-x-1.5">
        <button
          onClick={resetSimulation}
          className="p-2 rounded-lg border border-[#E8E8E5] bg-[#F7F7F5] hover:bg-[#E8E8E5] text-[#202124] transition-colors"
          title="Reset to beginning"
        >
          <RotateCcw className="h-4 w-4" />
        </button>

        <button
          onClick={stepBackward}
          disabled={currentStepIndex <= 0}
          className="p-2 rounded-lg border border-[#E8E8E5] bg-[#F7F7F5] hover:bg-[#E8E8E5] text-[#202124] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          title="Step Backward"
        >
          <SkipBack className="h-4 w-4" />
        </button>

        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg font-semibold text-xs transition-colors shadow-xs ${
            isPlaying
              ? 'bg-[#D9534F] text-white hover:bg-[#C9302C]'
              : 'bg-[#4F6BED] text-white hover:bg-[#3E58D6]'
          }`}
        >
          {isPlaying ? (
            <>
              <Pause className="h-4 w-4" />
              <span>Pause</span>
            </>
          ) : (
            <>
              <Play className="h-4 w-4" />
              <span>{currentStepIndex >= totalSteps - 1 ? 'Replay' : 'Play'}</span>
            </>
          )}
        </button>

        <button
          onClick={stepForward}
          disabled={currentStepIndex >= totalSteps - 1}
          className="p-2 rounded-lg border border-[#E8E8E5] bg-[#F7F7F5] hover:bg-[#E8E8E5] text-[#202124] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          title="Step Forward"
        >
          <SkipForward className="h-4 w-4" />
        </button>

        <span className="text-xs font-mono text-[#6B7280] ml-2">
          Step {currentStepIndex + 1} / {totalSteps}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full sm:w-48 flex items-center space-x-2">
        <div className="flex-1 h-2 bg-[#F0F0EE] rounded-full overflow-hidden">
          <div
            className="h-full bg-[#4F6BED] transition-all duration-200"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <span className="text-[11px] font-mono text-[#6B7280] w-9 text-right">
          {Math.round(progressPercent)}%
        </span>
      </div>

      {/* Speed Slider */}
      <div className="flex items-center space-x-2 text-xs text-[#6B7280]">
        <Gauge className="h-3.5 w-3.5" />
        <span>Speed:</span>
        <select
          value={playbackSpeedMs}
          onChange={(e) => setPlaybackSpeedMs(Number(e.target.value))}
          className="rounded border border-[#E8E8E5] bg-[#F7F7F5] px-2 py-1 text-xs text-[#202124] focus:outline-hidden"
        >
          <option value={1200}>0.5x (Slow)</option>
          <option value={700}>1.0x (Normal)</option>
          <option value={400}>1.5x (Fast)</option>
          <option value={200}>2.0x (Ultra)</option>
        </select>
      </div>
    </div>
  )
}

