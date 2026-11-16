import React, { useMemo } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  Edge,
  Node,
  BackgroundVariant
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { DeviceNode } from './DeviceNode'
import { TopologyConfig } from '../../types'
import { useNetLabStore } from '../../stores/useNetLabStore'

const nodeTypes = {
  deviceNode: DeviceNode
}

interface NetworkTopologyCanvasProps {
  topology: TopologyConfig
  activeNodeId?: string
}

export const NetworkTopologyCanvas: React.FC<NetworkTopologyCanvasProps> = ({
  topology,
  activeNodeId
}) => {
  const { selectedEvent } = useNetLabStore()

  const currentActiveNode = selectedEvent?.destination_node || selectedEvent?.source_node || activeNodeId

  // Transform topology devices to React Flow nodes
  const nodes: Node[] = useMemo(() => {
    return topology.devices.map((device, idx) => {
      const isHere = device.id === currentActiveNode
      const ip = device.interfaces[0]?.ip_address || 'No IP'
      const mac = device.interfaces[0]?.mac_address || 'No MAC'

      return {
        id: device.id,
        type: 'deviceNode',
        position: device.position || { x: 100 + idx * 220, y: 150 },
        data: {
          id: device.id,
          label: device.label,
          type: device.type,
          ip,
          mac,
          isPacketHere: isHere,
          natEnabled: device.nat_enabled
        }
      }
    })
  }, [topology, currentActiveNode])

  // Transform topology links to React Flow edges
  const edges: Edge[] = useMemo(() => {
    return topology.links.map((link) => {
      const isLinkActive =
        selectedEvent &&
        ((selectedEvent.source_node === link.source_id && selectedEvent.destination_node === link.target_id) ||
         (selectedEvent.source_node === link.target_id && selectedEvent.destination_node === link.source_id))

      return {
        id: link.id,
        source: link.source_id,
        target: link.target_id,
        animated: !!isLinkActive,
        label: `${link.medium} • ${link.latency_ms}ms`,
        labelStyle: { fill: '#6B7280', fontSize: 10, fontWeight: 500 },
        labelBgStyle: { fill: '#FFFFFF', fillOpacity: 0.9, rx: 4, ry: 4 },
        labelBgBorderRadius: 4,
        style: {
          stroke: isLinkActive ? '#4F6BED' : '#D1D5DB',
          strokeWidth: isLinkActive ? 2.5 : 1.5
        }
      }
    })
  }, [topology, selectedEvent])

  return (
    <div className="h-full w-full bg-[#FAFAFA] rounded-xl overflow-hidden border border-[#E8E8E5]">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="#E5E7EB" />
        <Controls showInteractive={false} className="!bg-white !border !border-[#E8E8E5] !shadow-xs" />
      </ReactFlow>
    </div>
  )
}

