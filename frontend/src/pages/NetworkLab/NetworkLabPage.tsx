import React, { useState, useEffect } from 'react'
import {
  FlaskConical,
  Play,
  Layers,
  Clock,
  Eye,
  Sliders,
  Send,
  Sparkles,
  BarChart3
} from 'lucide-react'
import { useNetLabStore } from '../../stores/useNetLabStore'
import { runSimulation, fetchScenarios, fetchScenarioDetail } from '../../services/api'
import { NetworkTopologyCanvas } from '../../components/topology/NetworkTopologyCanvas'
import { SimulationControls } from '../../components/simulation/SimulationControls'
import { EventTimeline } from '../../components/simulation/EventTimeline'
import { PacketInspector } from '../../components/inspector/PacketInspector'
import { ExplanationCard } from '../../components/simulation/ExplanationCard'
import { CwndChart } from '../../components/charts/CwndChart'
import { NetworkStatsSummary } from '../../components/charts/NetworkStatsSummary'

export const NetworkLabPage: React.FC = () => {
  const {
    activeSimulation,
    setActiveSimulation,
    selectedEvent,
    selectedPacket,
    currentStepIndex
  } = useNetLabStore()

  // New Simulation Form State
  const [senderId, setSenderId] = useState<string>('')
  const [receiverId, setReceiverId] = useState<string>('')
  const [appProtocol, setAppProtocol] = useState<string>('HTTP')
  const [transportProtocol, setTransportProtocol] = useState<string>('TCP')
  const [payload, setPayload] = useState<string>('GET /index.html HTTP/1.1\r\nHost: example.com')
  const [lossRate, setLossRate] = useState<number>(0.0)
  const [bitErrorRate, setBitErrorRate] = useState<number>(0.0)
  const [mtu, setMtu] = useState<number>(1500)
  const [isRunning, setIsRunning] = useState<boolean>(false)

  // Ensure default simulation is loaded if none is active
  useEffect(() => {
    if (!activeSimulation) {
      fetchScenarios().then((scenarios) => {
        if (scenarios.length > 0) {
          fetchScenarioDetail(scenarios[0].id).then((detail) => {
            const src = detail.topology.devices[0].id
            const dst = detail.topology.devices[detail.topology.devices.length - 1].id
            setSenderId(src)
            setReceiverId(dst)
            runSimulation({
              topology_id: detail.id,
              sender_id: src,
              receiver_id: dst
            }).then((res) => setActiveSimulation(res))
          })
        }
      })
    } else {
      setSenderId(activeSimulation.topology.devices[0]?.id || '')
      setReceiverId(activeSimulation.topology.devices[activeSimulation.topology.devices.length - 1]?.id || '')
    }
  }, [activeSimulation, setActiveSimulation])

  const handleStartSimulation = async () => {
    if (!activeSimulation || !senderId || !receiverId) return
    setIsRunning(true)
    try {
      const res = await runSimulation({
        topology_id: activeSimulation.topology.id,
        custom_topology: activeSimulation.topology,
        sender_id: senderId,
        receiver_id: receiverId,
        app_protocol: appProtocol,
        transport_protocol: transportProtocol,
        payload: payload,
        override_loss_rate: lossRate > 0 ? lossRate : undefined,
        override_bit_error_rate: bitErrorRate > 0 ? bitErrorRate : undefined,
        override_mtu: mtu
      })
      setActiveSimulation(res)
    } catch (err) {
      alert(`Simulation error: ${err}`)
    } finally {
      setIsRunning(false)
    }
  }

  if (!activeSimulation) {
    return (
      <div className="flex h-[80vh] items-center justify-center text-xs text-[#6B7280]">
        Loading Network Simulation Engine...
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4 space-y-4">
      {/* Simulation Controls Toolbar */}
      <SimulationControls />

      {/* THREE SYNCHRONIZED PANELS */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* PANEL 1: Visual Network Topology (Left 7 cols) */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          <div className="h-[460px] w-full relative">
            <NetworkTopologyCanvas
              topology={activeSimulation.topology}
              activeNodeId={selectedEvent?.destination_node || selectedEvent?.source_node}
            />
          </div>

          {/* Quick Transmission Config Form */}
          <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
            <div className="flex items-center justify-between border-b border-[#E8E8E5] pb-2">
              <div className="flex items-center space-x-1.5 text-xs font-bold text-[#202124]">
                <Send className="h-3.5 w-3.5 text-[#4F6BED]" />
                <span>Transmit New Message Across Topology</span>
              </div>
              <button
                onClick={handleStartSimulation}
                disabled={isRunning}
                className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6] disabled:opacity-50 transition-colors"
              >
                <Play className="h-3 w-3" />
                <span>{isRunning ? 'Transmitting...' : 'Send Message'}</span>
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              <div>
                <label className="text-[11px] text-[#6B7280]">Sender Node</label>
                <select
                  value={senderId}
                  onChange={(e) => setSenderId(e.target.value)}
                  className="w-full mt-0.5 px-2 py-1 text-xs rounded border border-[#E8E8E5] bg-[#F7F7F5]"
                >
                  {activeSimulation.topology.devices.map((d) => (
                    <option key={d.id} value={d.id}>{d.label} ({d.id})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-[11px] text-[#6B7280]">Receiver Node</label>
                <select
                  value={receiverId}
                  onChange={(e) => setReceiverId(e.target.value)}
                  className="w-full mt-0.5 px-2 py-1 text-xs rounded border border-[#E8E8E5] bg-[#F7F7F5]"
                >
                  {activeSimulation.topology.devices.map((d) => (
                    <option key={d.id} value={d.id}>{d.label} ({d.id})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-[11px] text-[#6B7280]">Transport Layer</label>
                <select
                  value={transportProtocol}
                  onChange={(e) => setTransportProtocol(e.target.value)}
                  className="w-full mt-0.5 px-2 py-1 text-xs rounded border border-[#E8E8E5] bg-[#F7F7F5]"
                >
                  <option value="TCP">TCP (Handshake & Reliability)</option>
                  <option value="UDP">UDP (Stateless & Fast)</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] text-[#6B7280]">Simulated Loss Rate</label>
                <select
                  value={lossRate}
                  onChange={(e) => setLossRate(Number(e.target.value))}
                  className="w-full mt-0.5 px-2 py-1 text-xs rounded border border-[#E8E8E5] bg-[#F7F7F5]"
                >
                  <option value={0.0}>0% Loss (Clean)</option>
                  <option value={0.2}>20% Loss (Drops & Retries)</option>
                  <option value={0.4}>40% Loss (High Congestion)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Performance & Congestion Window Graph */}
          {activeSimulation.stats.tcp_cwnd_history && activeSimulation.stats.tcp_cwnd_history.length > 0 && (
            <CwndChart data={activeSimulation.stats.tcp_cwnd_history} />
          )}
        </div>

        {/* RIGHT PANELS (Right 5 cols) */}
        <div className="lg:col-span-5 flex flex-col space-y-4">
          {/* PANEL 2: Synchronized Event Timeline (Height 230px) */}
          <div className="h-[240px]">
            <EventTimeline />
          </div>

          {/* "WHY DID THIS HAPPEN?" Explanation Engine */}
          <div>
            <ExplanationCard />
          </div>

          {/* PANEL 3: Packet & Header Inspector (Height 340px) */}
          <div className="h-[360px]">
            <PacketInspector packet={selectedPacket} />
          </div>
        </div>
      </div>

      {/* Network Stats Summary Bar */}
      <div className="pt-2">
        <NetworkStatsSummary stats={activeSimulation.stats} />
      </div>
    </div>
  )
}

