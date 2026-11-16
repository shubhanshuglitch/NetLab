import React from 'react'
import {
  Clock,
  ArrowRight,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  Send
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'
import { SimulationEventModel } from '../../types'

export const EventTimeline: React.FC = () => {
  const { activeSimulation, currentStepIndex, setCurrentStepIndex } = useNetLabStore()

  if (!activeSimulation || !activeSimulation.events.length) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-6 text-center text-[#9CA3AF] border border-[#E8E8E5] rounded-xl bg-white">
        <Clock className="h-8 w-8 mb-2 stroke-1 text-[#D1D5DB]" />
        <p className="text-xs font-medium text-[#6B7280]">No Events Recorded</p>
        <p className="text-[11px] text-[#9CA3AF] mt-0.5">Start a scenario or run a simulation to generate events.</p>
      </div>
    )
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'PACKET_DROPPED':
        return <AlertTriangle className="h-3.5 w-3.5 text-[#D9534F]" />
      case 'CRC_ERROR':
        return <ShieldAlert className="h-3.5 w-3.5 text-[#D9534F]" />
      case 'TCP_RETRANSMISSION':
        return <RefreshCw className="h-3.5 w-3.5 text-[#D89A38]" />
      case 'PACKET_DELIVERED':
        return <CheckCircle2 className="h-3.5 w-3.5 text-[#25845A]" />
      default:
        return <Send className="h-3.5 w-3.5 text-[#4F6BED]" />
    }
  }

  const getLayerBadgeColor = (layer: string) => {
    switch (layer) {
      case 'application':
        return 'bg-purple-50 text-purple-700 border-purple-200'
      case 'transport':
        return 'bg-blue-50 text-blue-700 border-blue-200'
      case 'network':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200'
      case 'datalink':
        return 'bg-amber-50 text-amber-700 border-amber-200'
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200'
    }
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-[#E8E8E5] bg-white overflow-hidden shadow-xs">
      <div className="flex items-center justify-between px-3.5 py-2.5 border-b border-[#E8E8E5] bg-[#FAFAFA]">
        <div className="flex items-center space-x-2">
          <Clock className="h-4 w-4 text-[#4F6BED]" />
          <span className="text-xs font-semibold text-[#202124]">Event Timeline</span>
        </div>
        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-200 text-[#4B5563]">
          {activeSimulation.events.length} Events
        </span>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {activeSimulation.events.map((event, idx) => {
          const isSelected = idx === currentStepIndex
          return (
            <div
              key={event.event_id || idx}
              onClick={() => setCurrentStepIndex(idx)}
              className={`flex items-start space-x-2.5 p-2 rounded-lg cursor-pointer transition-all border ${
                isSelected
                  ? 'bg-[#4F6BED]/5 border-[#4F6BED] shadow-xs'
                  : 'hover:bg-[#F7F7F5] border-transparent'
              }`}
            >
              {/* Step indicator */}
              <div className="flex flex-col items-center shrink-0 pt-0.5">
                <div
                  className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${
                    isSelected
                      ? 'bg-[#4F6BED] text-white'
                      : 'bg-[#F0F0EE] text-[#6B7280]'
                  }`}
                >
                  {idx + 1}
                </div>
              </div>

              {/* Event Body */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-0.5">
                  <div className="flex items-center space-x-1.5 truncate">
                    {getEventIcon(event.event_type)}
                    <span className="text-xs font-semibold text-[#202124] truncate">
                      {event.event_type.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-[#9CA3AF] shrink-0">
                    +{event.timestamp_ms.toFixed(1)}ms
                  </span>
                </div>

                <div className="flex items-center space-x-1.5 text-[11px] text-[#6B7280]">
                  <span className="font-medium text-[#202124]">{event.source_node}</span>
                  {event.destination_node && (
                    <>
                      <ArrowRight className="h-3 w-3 text-[#9CA3AF]" />
                      <span className="font-medium text-[#202124]">{event.destination_node}</span>
                    </>
                  )}
                  <span
                    className={`text-[9px] font-medium px-1 py-0.2 rounded border uppercase tracking-wider ml-auto ${getLayerBadgeColor(
                      event.layer
                    )}`}
                  >
                    {event.layer}
                  </span>
                </div>

                <p className="text-[11px] text-[#6B7280] line-clamp-1 mt-0.5">
                  {event.explanation?.what || 'Network transition occurred.'}
                </p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

