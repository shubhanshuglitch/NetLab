import React, { useState, useEffect } from 'react'
import {
  Layers,
  Play,
  RotateCcw,
  Sliders,
  CheckCircle,
  HelpCircle,
  ArrowRight,
  ShieldAlert,
  Activity,
  Flame
} from 'lucide-react'
import { fetchScenarios, fetchScenarioDetail, runSimulation } from '../../services/api'
import { ScenarioMeta, ScenarioDetail } from '../../types'
import { useNetLabStore } from '../../stores/useNetLabStore'
import { NetworkTopologyCanvas } from '../../components/topology/NetworkTopologyCanvas'

export const ScenariosPage: React.FC = () => {
  const {
    setActiveSimulation,
    setActiveTab,
    completedScenarios,
    markScenarioComplete
  } = useNetLabStore()

  const [scenarios, setScenarios] = useState<ScenarioMeta[]>([])
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>('scenario-youtube-tabs')
  const [scenarioDetail, setScenarioDetail] = useState<ScenarioDetail | null>(null)
  const [activeCategory, setActiveCategory] = useState<string>('All')
  const [loading, setLoading] = useState(true)
  const [simulating, setSimulating] = useState(false)

  // Parameter Overrides
  const [lossRate, setLossRate] = useState<number>(0.0)
  const [bitErrorRate, setBitErrorRate] = useState<number>(0.0)
  const [mtuOverride, setMtuOverride] = useState<number>(1500)
  const [tcpAlgo, setTcpAlgo] = useState<string>('Reno')

  useEffect(() => {
    fetchScenarios()
      .then((data) => {
        setScenarios(data)
        if (data.length > 0) {
          setSelectedScenarioId(data[0].id)
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!selectedScenarioId) return
    fetchScenarioDetail(selectedScenarioId)
      .then((detail) => setScenarioDetail(detail))
      .catch((err) => console.error(err))
  }, [selectedScenarioId])

  const categories = ['All', 'Browser & Web', 'Network Infrastructure', 'Real Applications', 'Advanced Networking']

  const filteredScenarios = scenarios.filter(
    (s) => activeCategory === 'All' || s.category.toLowerCase().includes(activeCategory.toLowerCase().slice(0, 7))
  )

  const handleRunSimulation = async () => {
    if (!scenarioDetail) return
    setSimulating(true)
    try {
      const srcNode = scenarioDetail.topology.devices[0].id
      const dstNode = scenarioDetail.topology.devices[scenarioDetail.topology.devices.length - 1].id

      const res = await runSimulation({
        topology_id: scenarioDetail.id,
        sender_id: srcNode,
        receiver_id: dstNode,
        override_loss_rate: lossRate > 0 ? lossRate : undefined,
        override_bit_error_rate: bitErrorRate > 0 ? bitErrorRate : undefined,
        override_mtu: mtuOverride,
        tcp_algorithm: tcpAlgo
      })

      setActiveSimulation(res)
      markScenarioComplete(scenarioDetail.id)
      setActiveTab('network-lab')
    } catch (err) {
      alert(`Simulation failed: ${err}`)
    } finally {
      setSimulating(false)
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E8E8E5] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[#202124]">Real-World Scenario Simulator</h1>
          <p className="text-xs text-[#6B7280]">
            Experience how protocols interact in realistic multi-device environments.
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                activeCategory === cat
                  ? 'bg-[#4F6BED] text-white shadow-xs'
                  : 'bg-white border border-[#E8E8E5] text-[#6B7280] hover:text-[#202124]'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Scenario List */}
        <div className="lg:col-span-4 space-y-2">
          <div className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">
            Available Scenarios ({filteredScenarios.length})
          </div>

          <div className="space-y-2">
            {filteredScenarios.map((sc) => {
              const isSelected = sc.id === selectedScenarioId
              const isCompleted = completedScenarios.includes(sc.id)

              return (
                <div
                  key={sc.id}
                  onClick={() => setSelectedScenarioId(sc.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-white border-[#4F6BED] shadow-sm ring-1 ring-[#4F6BED]'
                      : 'bg-white border-[#E8E8E5] hover:border-[#D1D5DB]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-[#4F6BED]">
                      {sc.category}
                    </span>
                    <div className="flex items-center space-x-1">
                      {isCompleted && <CheckCircle className="h-3.5 w-3.5 text-[#25845A]" />}
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-gray-100 text-[#4B5563]">
                        {sc.difficulty}
                      </span>
                    </div>
                  </div>
                  <h4 className="text-xs font-bold text-[#202124]">{sc.title}</h4>
                  <p className="text-[11px] text-[#6B7280] line-clamp-2 mt-1">{sc.summary}</p>
                </div>
              )
            })}
          </div>
        </div>

        {/* Scenario Details & Topology Preview */}
        {scenarioDetail && (
          <div className="lg:col-span-8 space-y-5">
            {/* Scenario Header Banner */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold text-[#4F6BED]">{scenarioDetail.category}</span>
                  <h2 className="text-xl font-bold text-[#202124] mt-0.5">{scenarioDetail.title}</h2>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={handleRunSimulation}
                    disabled={simulating}
                    className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-[#4F6BED] text-xs font-bold text-white hover:bg-[#3E58D6] shadow-xs transition-colors disabled:opacity-50"
                  >
                    <Play className="h-4 w-4" />
                    <span>{simulating ? 'Simulating...' : 'Run Scenario'}</span>
                  </button>
                </div>
              </div>

              {/* Central Key Question */}
              <div className="p-3.5 rounded-xl bg-amber-50/50 border border-amber-200">
                <div className="flex items-center space-x-1.5 text-xs font-bold text-amber-900 mb-1">
                  <HelpCircle className="h-4 w-4 text-amber-700" />
                  <span>The Fundamental Question</span>
                </div>
                <p className="text-xs text-amber-950 font-medium">
                  {scenarioDetail.key_question}
                </p>
              </div>

              <p className="text-xs text-[#6B7280] leading-relaxed">
                {scenarioDetail.explanation}
              </p>
            </div>

            {/* Interactive Network Topology Preview */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Layers className="h-4 w-4 text-[#4F6BED]" />
                  <span className="text-xs font-bold text-[#202124] uppercase tracking-wide">
                    Scenario Topology
                  </span>
                </div>
                <span className="text-xs text-[#6B7280]">
                  {scenarioDetail.topology.devices.length} Devices • {scenarioDetail.topology.links.length} Links
                </span>
              </div>

              <div className="h-72 w-full">
                <NetworkTopologyCanvas topology={scenarioDetail.topology} />
              </div>
            </div>

            {/* Parameter Injection Workbench */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
              <div className="flex items-center justify-between border-b border-[#E8E8E5] pb-2">
                <div className="flex items-center space-x-2">
                  <Sliders className="h-4 w-4 text-[#D89A38]" />
                  <span className="text-xs font-bold text-[#202124] uppercase tracking-wide">
                    Experiment: Inject Failures & Parameters
                  </span>
                </div>
                <span className="text-[11px] text-[#6B7280]">Observe how protocols respond</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div>
                  <div className="flex justify-between text-[#6B7280] mb-1">
                    <span>Packet Loss Rate:</span>
                    <strong className="text-[#D9534F]">{(lossRate * 100).toFixed(0)}%</strong>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="0.4"
                    step="0.05"
                    value={lossRate}
                    onChange={(e) => setLossRate(Number(e.target.value))}
                    className="w-full accent-[#D9534F]"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-[#6B7280] mb-1">
                    <span>Link MTU:</span>
                    <strong className="text-[#4F6BED]">{mtuOverride} B</strong>
                  </div>
                  <input
                    type="range"
                    min="500"
                    max="1500"
                    step="100"
                    value={mtuOverride}
                    onChange={(e) => setMtuOverride(Number(e.target.value))}
                    className="w-full accent-[#4F6BED]"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-[#6B7280] mb-1">
                    <span>Bit Corruption (BER):</span>
                    <strong className="text-amber-600">{(bitErrorRate * 100).toFixed(0)}%</strong>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="0.3"
                    step="0.05"
                    value={bitErrorRate}
                    onChange={(e) => setBitErrorRate(Number(e.target.value))}
                    className="w-full accent-amber-600"
                  />
                </div>
              </div>
            </div>

            {/* Chronological Step-by-Step Walkthrough Preview */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-3">
              <div className="text-xs font-bold text-[#202124] uppercase tracking-wide">
                Protocol Walkthrough Steps
              </div>
              <div className="space-y-2">
                {scenarioDetail.walkthrough.map((step) => (
                  <div
                    key={step.step}
                    className="flex items-start space-x-3 p-2.5 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] text-xs"
                  >
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-[#4F6BED]/10 text-[#4F6BED] font-bold text-[10px] shrink-0 mt-0.5">
                      {step.step}
                    </div>
                    <div>
                      <span className="font-semibold text-[#202124]">[{step.actor}]: </span>
                      <span className="text-[#4B5563]">{step.action}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

