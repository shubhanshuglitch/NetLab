import React, { useState, useEffect } from 'react'
import {
  BookOpen,
  CheckCircle,
  HelpCircle,
  Play,
  RotateCcw,
  Sparkles,
  Layers,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Globe2
} from 'lucide-react'
import {
  fetchConcepts,
  calculateCRC,
  simulateARQ,
  calculateDijkstra,
  calculateFragmentation,
  resolveDNS,
  simulateDHCP
} from '../../services/api'
import { ConceptItem } from '../../types'
import { useNetLabStore } from '../../stores/useNetLabStore'

export const LearnPage: React.FC = () => {
  const { completedConcepts, markConceptComplete, setActiveTab } = useNetLabStore()
  const [concepts, setConcepts] = useState<ConceptItem[]>([])
  const [selectedConcept, setSelectedConcept] = useState<ConceptItem | null>(null)
  const [selectedLayer, setSelectedLayer] = useState<string>('All')
  const [loading, setLoading] = useState(true)

  // Interactive Concept Tool States
  // 1. CRC State
  const [crcData, setCrcData] = useState('1101011011')
  const [crcGen, setCrcGen] = useState('10011')
  const [crcResult, setCrcResult] = useState<any>(null)

  // 2. ARQ State
  const [arqProtocol, setArqProtocol] = useState('Go-Back-N')
  const [arqFrames, setArqFrames] = useState(6)
  const [arqWindow, setArqWindow] = useState(3)
  const [arqDrop, setArqDrop] = useState(1)
  const [arqResult, setArqResult] = useState<any>(null)

  // 3. Dijkstra State
  const [dijkstraSource, setDijkstraSource] = useState('R1')
  const [dijkstraResult, setDijkstraResult] = useState<any>(null)

  // 4. Fragmentation State
  const [fragPayload, setFragPayload] = useState(2400)
  const [fragMtu, setFragMtu] = useState(1000)
  const [fragResult, setFragResult] = useState<any>(null)

  // 5. DNS State
  const [dnsDomain, setDnsDomain] = useState('youtube.com')
  const [dnsResult, setDnsResult] = useState<any>(null)

  // 6. DHCP State
  const [dhcpMac, setDhcpMac] = useState('00:AA:22:33:44:55')
  const [dhcpResult, setDhcpResult] = useState<any>(null)

  useEffect(() => {
    fetchConcepts()
      .then((data) => {
        setConcepts(data)
        if (data.length > 0) {
          setSelectedConcept(data[0])
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false))
  }, [])

  // Auto-run initial interactive simulation when concept changes
  useEffect(() => {
    if (!selectedConcept) return
    if (selectedConcept.interactive_type === 'crc') handleRunCRC()
    if (selectedConcept.interactive_type === 'arq') handleRunARQ()
    if (selectedConcept.interactive_type === 'dijkstra') handleRunDijkstra()
    if (selectedConcept.interactive_type === 'fragmentation') handleRunFragmentation()
    if (selectedConcept.interactive_type === 'dns') handleRunDNS()
    if (selectedConcept.interactive_type === 'dhcp') handleRunDHCP()
  }, [selectedConcept])

  const handleRunCRC = async () => {
    try {
      const res = await calculateCRC(crcData, crcGen)
      setCrcResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleRunARQ = async () => {
    try {
      const res = await simulateARQ(arqProtocol, arqFrames, arqWindow, arqDrop)
      setArqResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleRunDijkstra = async () => {
    try {
      const nodes = ['R1', 'R2', 'R3', 'R4', 'R5']
      const links = [
        { source: 'R1', target: 'R2', cost: 3 },
        { source: 'R1', target: 'R3', cost: 5 },
        { source: 'R2', target: 'R3', cost: 1 },
        { source: 'R2', target: 'R4', cost: 7 },
        { source: 'R3', target: 'R4', cost: 2 },
        { source: 'R4', target: 'R5', cost: 4 },
        { source: 'R3', target: 'R5', cost: 8 }
      ]
      const res = await calculateDijkstra(nodes, links, dijkstraSource)
      setDijkstraResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleRunFragmentation = async () => {
    try {
      const res = await calculateFragmentation(fragPayload, fragMtu)
      setFragResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleRunDNS = async () => {
    try {
      const res = await resolveDNS(dnsDomain)
      setDnsResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleRunDHCP = async () => {
    try {
      const res = await simulateDHCP(dhcpMac)
      setDhcpResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  const layers = ['All', 'Application Layer', 'Network Layer', 'Data Link Layer']

  const filteredConcepts = concepts.filter(
    (c) => selectedLayer === 'All' || c.layer.toLowerCase().includes(selectedLayer.toLowerCase())
  )

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E8E8E5] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[#202124]">Concept Visualizer</h1>
          <p className="text-xs text-[#6B7280]">
            Interactive algorithmic implementations of core computer networking principles.
          </p>
        </div>

        {/* Layer Filters */}
        <div className="flex flex-wrap gap-1.5">
          {layers.map((layer) => (
            <button
              key={layer}
              onClick={() => setSelectedLayer(layer)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                selectedLayer === layer
                  ? 'bg-[#4F6BED] text-white shadow-xs'
                  : 'bg-white border border-[#E8E8E5] text-[#6B7280] hover:text-[#202124]'
              }`}
            >
              {layer}
            </button>
          ))}
        </div>
      </div>

      {/* Main 2-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Sidebar: Concept Selector */}
        <div className="lg:col-span-4 space-y-2">
          <div className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">
            Concepts ({filteredConcepts.length})
          </div>

          <div className="space-y-1.5">
            {filteredConcepts.map((c) => {
              const isSelected = selectedConcept?.id === c.id
              const isCompleted = completedConcepts.includes(c.id)

              return (
                <div
                  key={c.id}
                  onClick={() => setSelectedConcept(c)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-white border-[#4F6BED] shadow-sm ring-1 ring-[#4F6BED]'
                      : 'bg-white border-[#E8E8E5] hover:border-[#D1D5DB]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-[#4F6BED]">
                      {c.layer}
                    </span>
                    <div className="flex items-center space-x-1">
                      {isCompleted && <CheckCircle className="h-3.5 w-3.5 text-[#25845A]" />}
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-gray-100 text-[#4B5563]">
                        {c.difficulty}
                      </span>
                    </div>
                  </div>
                  <div className="text-xs font-bold text-[#202124]">{c.name}</div>
                  <p className="text-[11px] text-[#6B7280] line-clamp-1 mt-0.5">{c.summary}</p>
                </div>
              )
            })}
          </div>
        </div>

        {/* Right Content: Concept Details & Interactive Execution */}
        {selectedConcept && (
          <div className="lg:col-span-8 space-y-5">
            {/* Concept Header Card */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-50 text-[#4F6BED]">
                      {selectedConcept.layer}
                    </span>
                    <span className="text-xs font-medium text-[#6B7280]">• {selectedConcept.difficulty}</span>
                  </div>
                  <h2 className="text-xl font-bold text-[#202124] mt-1">{selectedConcept.name}</h2>
                </div>

                <button
                  onClick={() => markConceptComplete(selectedConcept.id)}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    completedConcepts.includes(selectedConcept.id)
                      ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      : 'bg-[#F7F7F5] border border-[#E8E8E5] text-[#202124] hover:bg-white'
                  }`}
                >
                  <CheckCircle className="h-3.5 w-3.5" />
                  <span>
                    {completedConcepts.includes(selectedConcept.id) ? 'Mastered' : 'Mark as Mastered'}
                  </span>
                </button>
              </div>

              {/* Explanations (Simple vs Technical) */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                <div className="p-3.5 rounded-xl bg-[#F7F7F5] border border-[#E8E8E5] space-y-1">
                  <div className="text-[11px] font-bold text-[#4F6BED] uppercase tracking-wider flex items-center space-x-1">
                    <Sparkles className="h-3 w-3" />
                    <span>Simple Explanation</span>
                  </div>
                  <p className="text-xs text-[#4B5563] leading-relaxed">
                    {selectedConcept.simple_explanation}
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-1">
                  <div className="text-[11px] font-bold text-[#25845A] uppercase tracking-wider flex items-center space-x-1">
                    <Cpu className="h-3 w-3" />
                    <span>Technical Protocol RFC Details</span>
                  </div>
                  <p className="text-xs text-[#4B5563] leading-relaxed">
                    {selectedConcept.technical_explanation}
                  </p>
                </div>
              </div>
            </div>

            {/* INTERACTIVE ALGORITHM WORKBENCH */}
            <div className="p-5 rounded-2xl border border-[#E8E8E5] bg-white shadow-xs space-y-4">
              <div className="flex items-center justify-between border-b border-[#E8E8E5] pb-3">
                <div className="flex items-center space-x-2">
                  <Play className="h-4 w-4 text-[#4F6BED]" />
                  <span className="text-sm font-bold text-[#202124]">Interactive Simulation & Parameters</span>
                </div>
                <span className="text-[11px] text-[#6B7280]">Live Deterministic Output</span>
              </div>

              {/* 1. CRC Interactive Tool */}
              {selectedConcept.interactive_type === 'crc' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Data Bits (Binary)</label>
                      <input
                        type="text"
                        value={crcData}
                        onChange={(e) => setCrcData(e.target.value.replace(/[^01]/g, ''))}
                        className="w-full mt-1 px-3 py-1.5 text-xs font-mono rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Generator Polynomial G(x) Bits</label>
                      <div className="flex items-center space-x-2 mt-1">
                        <input
                          type="text"
                          value={crcGen}
                          onChange={(e) => setCrcGen(e.target.value.replace(/[^01]/g, ''))}
                          className="w-full px-3 py-1.5 text-xs font-mono rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                        />
                        <button
                          onClick={handleRunCRC}
                          className="px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6]"
                        >
                          Calculate
                        </button>
                      </div>
                    </div>
                  </div>

                  {crcResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-3">
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                        <div>
                          <span className="text-[#6B7280]">Appended Dividend:</span>{' '}
                          <span className="font-mono font-bold text-[#202124]">{crcResult.appended_data_bits}</span>
                        </div>
                        <div>
                          <span className="text-[#6B7280]">Calculated Remainder (FCS):</span>{' '}
                          <span className="font-mono font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded">
                            {crcResult.remainder_crc_bits}
                          </span>
                        </div>
                        <div className="col-span-2 sm:col-span-1">
                          <span className="text-[#6B7280]">Transmitted Frame Codeword:</span>{' '}
                          <span className="font-mono font-bold text-blue-700">{crcResult.transmitted_codeword}</span>
                        </div>
                      </div>

                      <div className="text-[11px] font-semibold text-[#6B7280] mt-2">Modulo-2 Division Step Trace:</div>
                      <div className="max-h-48 overflow-y-auto space-y-1 font-mono text-[11px] bg-white p-2.5 rounded-lg border border-[#E8E8E5]">
                        {crcResult.steps.map((st: any) => (
                          <div key={st.step_index} className="flex items-center justify-between py-0.5 border-b border-gray-100 last:border-0">
                            <span>Step {st.step_index} [{st.action}]</span>
                            <span className="text-gray-500">{st.window_before} ⊕ {st.divisor} = <strong className="text-[#202124]">{st.window_after}</strong></span>
                            <span className="text-emerald-700">Rem: {st.current_remainder}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 2. ARQ Interactive Tool */}
              {selectedConcept.interactive_type === 'arq' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">ARQ Protocol</label>
                      <select
                        value={arqProtocol}
                        onChange={(e) => setArqProtocol(e.target.value)}
                        className="w-full mt-1 px-2 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      >
                        <option value="Stop-and-Wait">Stop-and-Wait</option>
                        <option value="Go-Back-N">Go-Back-N</option>
                        <option value="Selective-Repeat">Selective Repeat</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Window Size (N)</label>
                      <input
                        type="number"
                        min={1}
                        max={8}
                        value={arqWindow}
                        onChange={(e) => setArqWindow(Number(e.target.value))}
                        className="w-full mt-1 px-2 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Drop Frame #</label>
                      <input
                        type="number"
                        min={0}
                        max={7}
                        value={arqDrop}
                        onChange={(e) => setArqDrop(Number(e.target.value))}
                        className="w-full mt-1 px-2 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      />
                    </div>
                    <div className="flex items-end">
                      <button
                        onClick={handleRunARQ}
                        className="w-full px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6]"
                      >
                        Simulate ARQ
                      </button>
                    </div>
                  </div>

                  {arqResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-3">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-[#202124]">
                          {arqResult.protocol} Simulation (Window: {arqResult.window_size})
                        </span>
                        <span className="font-mono text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                          Retransmissions: {arqResult.retransmissions}
                        </span>
                      </div>

                      <div className="space-y-1.5 max-h-56 overflow-y-auto">
                        {arqResult.events.map((ev: any) => (
                          <div
                            key={ev.step}
                            className={`p-2 rounded-lg border text-xs ${
                              ev.is_dropped
                                ? 'bg-red-50/50 border-red-200 text-red-900'
                                : ev.is_timeout
                                ? 'bg-amber-50/50 border-amber-200 text-amber-900'
                                : 'bg-white border-[#E8E8E5] text-[#202124]'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-bold">Step {ev.step}: {ev.action}</span>
                              <span className="font-mono text-[10px] text-gray-500">
                                Sender Window: [{ev.sender_window.join(', ')}]
                              </span>
                            </div>
                            <p className="text-[11px] text-[#6B7280] mt-0.5">{ev.explanation}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 3. Dijkstra Interactive Tool */}
              {selectedConcept.interactive_type === 'dijkstra' && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <label className="text-xs font-semibold text-[#202124]">Source Router:</label>
                    <select
                      value={dijkstraSource}
                      onChange={(e) => setDijkstraSource(e.target.value)}
                      className="px-3 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                    >
                      {['R1', 'R2', 'R3', 'R4', 'R5'].map((r) => (
                        <option key={r} value={r}>{r}</option>
                      ))}
                    </select>
                    <button
                      onClick={handleRunDijkstra}
                      className="px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6]"
                    >
                      Run Dijkstra
                    </button>
                  </div>

                  {dijkstraResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-3">
                      <div className="text-xs font-bold text-[#202124]">Computed Forwarding Table for {dijkstraSource}:</div>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                        {dijkstraResult.routing_table.map((rt: any) => (
                          <div key={rt.destination} className="p-2 bg-white rounded-lg border border-[#E8E8E5]">
                            <div className="font-bold text-[#202124]">To {rt.destination}</div>
                            <div className="text-[11px] text-[#6B7280]">Metric Cost: <strong className="text-[#4F6BED]">{rt.cost}</strong></div>
                            <div className="text-[10px] text-[#9CA3AF]">Next Hop: <strong>{rt.next_hop}</strong></div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 4. Fragmentation Interactive Tool */}
              {selectedConcept.interactive_type === 'fragmentation' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Total Payload (Bytes)</label>
                      <input
                        type="number"
                        value={fragPayload}
                        onChange={(e) => setFragPayload(Number(e.target.value))}
                        className="w-full mt-1 px-3 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-[#202124]">Outgoing Link MTU (Bytes)</label>
                      <input
                        type="number"
                        value={fragMtu}
                        onChange={(e) => setFragMtu(Number(e.target.value))}
                        className="w-full mt-1 px-3 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                      />
                    </div>
                    <div className="flex items-end">
                      <button
                        onClick={handleRunFragmentation}
                        className="w-full px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6]"
                      >
                        Calculate Fragments
                      </button>
                    </div>
                  </div>

                  {fragResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-[#202124]">
                          Sliced into {fragResult.fragment_count} IPv4 Fragments
                        </span>
                        <span className="text-[11px] text-[#6B7280]">
                          Max Payload per Fragment: {((fragMtu - 20) >> 3) << 3} B (Multiple of 8)
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        {fragResult.fragments.map((fr: any) => (
                          <div key={fr.fragment_index} className="p-2 bg-white rounded-lg border border-[#E8E8E5] text-xs flex items-center justify-between">
                            <span className="font-bold text-emerald-900">Fragment #{fr.fragment_index + 1}</span>
                            <span className="font-mono">Payload: {fr.payload_bytes} B</span>
                            <span className="font-mono">Offset: {fr.offset_units_8b} ({fr.offset_bytes} B)</span>
                            <span className={`font-mono font-bold ${fr.mf_flag ? 'text-amber-600' : 'text-gray-600'}`}>
                              MF: {fr.mf_flag ? '1' : '0'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 5. DNS Interactive Tool */}
              {selectedConcept.interactive_type === 'dns' && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={dnsDomain}
                      onChange={(e) => setDnsDomain(e.target.value)}
                      placeholder="e.g. youtube.com or google.com"
                      className="w-full px-3 py-1.5 text-xs rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                    />
                    <button
                      onClick={handleRunDNS}
                      className="px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6] shrink-0"
                    >
                      Resolve Domain
                    </button>
                  </div>

                  {dnsResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-[#202124]">
                          Resolved: <strong className="text-emerald-700">{dnsResult.resolved_ip}</strong>
                        </span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${dnsResult.from_cache ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'}`}>
                          {dnsResult.from_cache ? 'Cache Hit' : 'Recursive Query'}
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        {dnsResult.steps.map((st: any) => (
                          <div key={st.step} className="p-2 bg-white rounded-lg border border-[#E8E8E5] text-xs">
                            <div className="flex items-center justify-between font-bold text-[#202124]">
                              <span>Step {st.step}: {st.server}</span>
                              <span className="text-blue-600 text-[10px]">{st.action}</span>
                            </div>
                            <p className="text-[11px] text-[#6B7280] mt-0.5">{st.explanation}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 6. DHCP Interactive Tool */}
              {selectedConcept.interactive_type === 'dhcp' && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={dhcpMac}
                      onChange={(e) => setDhcpMac(e.target.value)}
                      className="w-full px-3 py-1.5 text-xs font-mono rounded-lg border border-[#E8E8E5] bg-[#F7F7F5]"
                    />
                    <button
                      onClick={handleRunDHCP}
                      className="px-3 py-1.5 rounded-lg bg-[#4F6BED] text-xs font-semibold text-white hover:bg-[#3E58D6] shrink-0"
                    >
                      Simulate DORA
                    </button>
                  </div>

                  {dhcpResult && (
                    <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#E8E8E5] space-y-2">
                      <div className="space-y-1.5">
                        {dhcpResult.steps.map((st: any) => (
                          <div key={st.step} className="p-2.5 bg-white rounded-lg border border-[#E8E8E5] text-xs">
                            <div className="flex items-center justify-between font-bold text-[#202124]">
                              <span className="text-[#4F6BED]">Step {st.step}: {st.type}</span>
                              <span className="font-mono text-[10px] text-gray-500">{st.src_ip} → {st.dst_ip}</span>
                            </div>
                            <p className="text-[11px] text-[#202124] font-medium mt-1">{st.details}</p>
                            <p className="text-[10px] text-[#6B7280] mt-0.5">{st.explanation}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Bottom Insight Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl border border-red-200 bg-red-50/30 space-y-1">
                <span className="text-[11px] font-bold uppercase tracking-wider text-red-700">
                  Common Mistakes & Misconceptions
                </span>
                <p className="text-xs text-red-950 leading-relaxed">
                  {selectedConcept.common_mistakes}
                </p>
              </div>

              <div className="p-4 rounded-xl border border-[#E8E8E5] bg-white space-y-1">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#25845A]">
                  Real-World Production Engineering
                </span>
                <p className="text-xs text-[#4B5563] leading-relaxed">
                  {selectedConcept.real_world_application}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

