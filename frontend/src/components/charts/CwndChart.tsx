import React from 'react'
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts'
import { TrendingUp } from 'lucide-react'

interface CwndChartProps {
  data: Array<{ step: number; cwnd: number; ssthresh: number; state: string }>
}

export const CwndChart: React.FC<CwndChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-6 text-center text-[#9CA3AF] border border-[#E8E8E5] rounded-xl bg-white h-48">
        <TrendingUp className="h-6 w-6 mb-1 text-[#D1D5DB]" />
        <p className="text-xs text-[#6B7280]">No Congestion Window Data</p>
        <p className="text-[10px] text-[#9CA3AF]">Run a TCP simulation with packet loss to observe cwnd growth and recovery.</p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-[#E8E8E5] bg-white p-3 shadow-xs">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-1.5">
          <TrendingUp className="h-4 w-4 text-[#4F6BED]" />
          <span className="text-xs font-semibold text-[#202124]">TCP Congestion Window (CWND) Dynamics</span>
        </div>
        <span className="text-[10px] text-[#6B7280] font-mono">Algorithm: Reno</span>
      </div>

      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 15, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F0F0EE" />
            <XAxis dataKey="step" tick={{ fontSize: 10, fill: '#6B7280' }} />
            <YAxis tick={{ fontSize: 10, fill: '#6B7280' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E8E8E5', borderRadius: '8px', fontSize: '11px' }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '4px' }} />
            <Line
              type="monotone"
              dataKey="cwnd"
              name="CWND (MSS)"
              stroke="#4F6BED"
              strokeWidth={2}
              dot={{ r: 3, fill: '#4F6BED' }}
            />
            <Line
              type="stepAfter"
              dataKey="ssthresh"
              name="ssthresh (MSS)"
              stroke="#D89A38"
              strokeWidth={1.5}
              strokeDasharray="4 4"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

