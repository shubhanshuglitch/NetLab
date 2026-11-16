import React from 'react'
import {
  HelpCircle,
  Cpu,
  RefreshCw,
  GitFork,
  Globe2,
  Info
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const ExplanationCard: React.FC = () => {
  const { selectedEvent } = useNetLabStore()

  if (!selectedEvent || !selectedEvent.explanation) {
    return (
      <div className="flex flex-col items-center justify-center p-6 text-center text-[#9CA3AF] border border-[#E8E8E5] rounded-xl bg-white h-full">
        <HelpCircle className="h-8 w-8 mb-2 stroke-1 text-[#D1D5DB]" />
        <p className="text-xs font-medium text-[#6B7280]">Why Did This Happen?</p>
        <p className="text-[11px] text-[#9CA3AF] mt-0.5">
          Select any event in the timeline to see protocol-grounded causal explanations.
        </p>
      </div>
    )
  }

  const { what, why, protocol, data_changed, counterfactual, real_world } = selectedEvent.explanation

  return (
    <div className="flex flex-col rounded-xl border border-[#E8E8E5] bg-white overflow-hidden shadow-xs">
      {/* Title */}
      <div className="flex items-center space-x-2 px-4 py-2.5 border-b border-[#E8E8E5] bg-[#FAFAFA]">
        <Info className="h-4 w-4 text-[#4F6BED]" />
        <span className="text-xs font-bold text-[#202124] tracking-tight uppercase">
          Why Did This Happen?
        </span>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-blue-50 text-[#4F6BED] font-semibold ml-auto">
          {protocol}
        </span>
      </div>

      {/* Structured Sections */}
      <div className="p-4 space-y-3 overflow-y-auto">
        {/* 1. What Happened */}
        <div>
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#202124] mb-1">
            <span className="h-2 w-2 rounded-full bg-[#4F6BED]" />
            <span>What Happened?</span>
          </div>
          <p className="text-xs text-[#4B5563] pl-3.5 leading-relaxed bg-[#F7F7F5] p-2 rounded-md border border-[#E8E8E5]">
            {what}
          </p>
        </div>

        {/* 2. Why Did It Happen? */}
        <div>
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#202124] mb-1">
            <Cpu className="h-3.5 w-3.5 text-[#25845A]" />
            <span>Why Did It Happen? (Protocol Mechanics)</span>
          </div>
          <p className="text-xs text-[#4B5563] pl-3.5 leading-relaxed">
            {why}
          </p>
        </div>

        {/* 3. What Data Changed */}
        {data_changed && (
          <div>
            <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#202124] mb-1">
              <RefreshCw className="h-3.5 w-3.5 text-[#D89A38]" />
              <span>State & Data Changed</span>
            </div>
            <p className="text-xs font-mono text-[#D89A38] bg-amber-50/50 p-2 rounded-md border border-amber-200">
              {data_changed}
            </p>
          </div>
        )}

        {/* 4. Counterfactual Question */}
        {counterfactual && (
          <div className="rounded-lg border border-indigo-100 bg-indigo-50/40 p-2.5">
            <div className="flex items-center space-x-1.5 text-xs font-semibold text-indigo-900 mb-1">
              <GitFork className="h-3.5 w-3.5 text-indigo-600" />
              <span>What if the configuration was different?</span>
            </div>
            <p className="text-xs text-indigo-800 leading-relaxed">
              {counterfactual}
            </p>
          </div>
        )}

        {/* 5. Real-World Context */}
        {real_world && (
          <div className="rounded-lg border border-[#E8E8E5] bg-[#FAFAFA] p-2.5">
            <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#202124] mb-1">
              <Globe2 className="h-3.5 w-3.5 text-[#25845A]" />
              <span>Real-World Engineering Context</span>
            </div>
            <p className="text-xs text-[#6B7280] leading-relaxed">
              {real_world}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

