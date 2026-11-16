import React from 'react'
import {
  Send,
  CheckCircle,
  AlertOctagon,
  RotateCcw,
  Gauge,
  Timer
} from 'lucide-react'
import { SimulationStats } from '../../types'

interface NetworkStatsSummaryProps {
  stats: SimulationStats
}

export const NetworkStatsSummary: React.FC<NetworkStatsSummaryProps> = ({ stats }) => {
  const statCards = [
    {
      label: 'Transmitted',
      value: stats.packets_transmitted,
      unit: 'packets',
      icon: Send,
      color: 'text-blue-600',
      bg: 'bg-blue-50'
    },
    {
      label: 'Delivered',
      value: stats.packets_received,
      unit: 'packets',
      icon: CheckCircle,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50'
    },
    {
      label: 'Lost / Corrupted',
      value: stats.packets_lost + stats.frames_corrupted,
      unit: 'packets',
      icon: AlertOctagon,
      color: stats.packets_lost > 0 ? 'text-red-600' : 'text-gray-600',
      bg: stats.packets_lost > 0 ? 'bg-red-50' : 'bg-gray-50'
    },
    {
      label: 'Retransmissions',
      value: stats.retransmissions,
      unit: 'events',
      icon: RotateCcw,
      color: stats.retransmissions > 0 ? 'text-amber-600' : 'text-gray-600',
      bg: stats.retransmissions > 0 ? 'bg-amber-50' : 'bg-gray-50'
    },
    {
      label: 'Throughput',
      value: stats.throughput_kbps,
      unit: 'Kbps',
      icon: Gauge,
      color: 'text-indigo-600',
      bg: 'bg-indigo-50'
    },
    {
      label: 'Round Trip Latency',
      value: stats.average_latency_ms,
      unit: 'ms',
      icon: Timer,
      color: 'text-purple-600',
      bg: 'bg-purple-50'
    }
  ]

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
      {statCards.map((card, i) => {
        const Icon = card.icon
        return (
          <div
            key={i}
            className="flex flex-col p-2.5 rounded-xl border border-[#E8E8E5] bg-white shadow-xs"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-medium text-[#6B7280]">{card.label}</span>
              <div className={`p-1 rounded-md ${card.bg}`}>
                <Icon className={`h-3 w-3 ${card.color}`} />
              </div>
            </div>
            <div className="flex items-baseline space-x-1">
              <span className="text-base font-bold text-[#202124]">{card.value}</span>
              <span className="text-[10px] text-[#9CA3AF]">{card.unit}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

