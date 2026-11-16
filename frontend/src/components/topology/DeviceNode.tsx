import React from 'react'
import { Handle, Position } from '@xyflow/react'
import {
  Laptop,
  Monitor,
  Smartphone,
  Router as RouterIcon,
  Server,
  Shield,
  Wifi,
  Cloud,
  Globe
} from 'lucide-react'
import { DeviceType } from '../../types'

interface DeviceNodeData {
  id: string
  label: string
  type: DeviceType
  ip: string
  mac: string
  isActive?: boolean
  isPacketHere?: boolean
  natEnabled?: boolean
}

const getDeviceIcon = (type: DeviceType) => {
  switch (type) {
    case 'laptop':
      return Laptop
    case 'desktop':
      return Monitor
    case 'mobile':
      return Smartphone
    case 'router':
      return RouterIcon
    case 'switch':
      return RouterIcon
    case 'server':
    case 'dns_server':
    case 'cdn_server':
      return Server
    case 'firewall':
      return Shield
    case 'access_point':
      return Wifi
    case 'cloud':
      return Cloud
    default:
      return Globe
  }
}

export const DeviceNode: React.FC<{ data: DeviceNodeData }> = ({ data }) => {
  const Icon = getDeviceIcon(data.type)

  return (
    <div
      className={`relative flex flex-col items-center justify-center p-3 rounded-xl border bg-white shadow-xs transition-all duration-200 min-w-[120px] ${
        data.isPacketHere
          ? 'border-[#4F6BED] ring-4 ring-[#4F6BED]/20 shadow-md scale-105'
          : 'border-[#E8E8E5] hover:border-[#D1D5DB]'
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-[#9CA3AF] !w-2 !h-2" />
      <Handle type="target" position={Position.Left} className="!bg-[#9CA3AF] !w-2 !h-2" />

      {/* Node Icon */}
      <div
        className={`flex h-10 w-10 items-center justify-center rounded-lg mb-1.5 transition-colors ${
          data.isPacketHere
            ? 'bg-[#4F6BED] text-white animate-pulse'
            : 'bg-[#F7F7F5] text-[#202124]'
        }`}
      >
        <Icon className="h-5 w-5" />
      </div>

      {/* Node Label */}
      <span className="text-xs font-semibold text-[#202124] text-center leading-tight">
        {data.label}
      </span>

      {/* Node IP Badge */}
      <div className="mt-1 flex flex-col items-center">
        <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#F7F7F5] text-[#6B7280] border border-[#E8E8E5]">
          {data.ip}
        </span>
        {data.natEnabled && (
          <span className="text-[9px] font-semibold text-[#25845A] bg-[#25845A]/10 px-1 rounded mt-0.5">
            NAT Active
          </span>
        )}
      </div>

      <Handle type="source" position={Position.Right} className="!bg-[#9CA3AF] !w-2 !h-2" />
      <Handle type="source" position={Position.Bottom} className="!bg-[#9CA3AF] !w-2 !h-2" />
    </div>
  )
}

