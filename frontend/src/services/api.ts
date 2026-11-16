import {
  ScenarioMeta,
  ScenarioDetail,
  ConceptItem,
  InterviewQuestion,
  VerifyAnswerResponse,
  SimulationResponse,
  TopologyConfig
} from '../types'

const BASE_URL = '/api'

export async function fetchScenarios(category?: string): Promise<ScenarioMeta[]> {
  const url = category ? `${BASE_URL}/scenarios?category=${encodeURIComponent(category)}` : `${BASE_URL}/scenarios`
  const res = await fetch(url)
  if (!res.ok) throw new Error('Failed to fetch scenarios')
  return res.json()
}

export async function fetchScenarioDetail(id: string): Promise<ScenarioDetail> {
  const res = await fetch(`${BASE_URL}/scenarios/${id}`)
  if (!res.ok) throw new Error(`Failed to fetch scenario ${id}`)
  return res.json()
}

export async function fetchConcepts(): Promise<ConceptItem[]> {
  const res = await fetch(`${BASE_URL}/concepts`)
  if (!res.ok) throw new Error('Failed to fetch concepts')
  return res.json()
}

export async function calculateCRC(dataBits: string, generatorBits: string) {
  const res = await fetch(`${BASE_URL}/concepts/crc/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data_bits: dataBits, generator_bits: generatorBits })
  })
  if (!res.ok) throw new Error('CRC calculation failed')
  return res.json()
}

export async function simulateARQ(protocol: string, totalFrames: number, windowSize: number, dropIndex?: number) {
  const res = await fetch(`${BASE_URL}/concepts/arq/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      protocol,
      total_frames: totalFrames,
      window_size: windowSize,
      drop_frame_index: dropIndex
    })
  })
  if (!res.ok) throw new Error('ARQ simulation failed')
  return res.json()
}

export async function calculateDijkstra(nodes: string[], links: any[], source: string) {
  const res = await fetch(`${BASE_URL}/concepts/routing/dijkstra`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nodes, links, source })
  })
  if (!res.ok) throw new Error('Dijkstra calculation failed')
  return res.json()
}

export async function calculateFragmentation(payloadSize: number, mtu: number, flagsDf: boolean = false) {
  const res = await fetch(`${BASE_URL}/concepts/fragmentation/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ payload_size_bytes: payloadSize, mtu, flags_df: flagsDf })
  })
  if (!res.ok) throw new Error('Fragmentation calculation failed')
  return res.json()
}

export async function resolveDNS(domain: string) {
  const res = await fetch(`${BASE_URL}/concepts/dns/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain })
  })
  if (!res.ok) throw new Error('DNS resolution failed')
  return res.json()
}

export async function simulateDHCP(clientMac: string) {
  const res = await fetch(`${BASE_URL}/concepts/dhcp/dora`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ client_mac: clientMac })
  })
  if (!res.ok) throw new Error('DHCP simulation failed')
  return res.json()
}

export async function fetchInterviewQuestions(category?: string, difficulty?: string): Promise<InterviewQuestion[]> {
  const params = new URLSearchParams()
  if (category) params.append('category', category)
  if (difficulty) params.append('difficulty', difficulty)
  const res = await fetch(`${BASE_URL}/interview/questions?${params.toString()}`)
  if (!res.ok) throw new Error('Failed to fetch interview questions')
  return res.json()
}

export async function fetchInterviewCategories(): Promise<string[]> {
  const res = await fetch(`${BASE_URL}/interview/categories`)
  if (!res.ok) throw new Error('Failed to fetch interview categories')
  return res.json()
}

export async function verifyInterviewAnswer(questionId: string, selectedIndex: number): Promise<VerifyAnswerResponse> {
  const res = await fetch(`${BASE_URL}/interview/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question_id: questionId, selected_option_index: selectedIndex })
  })
  if (!res.ok) throw new Error('Verification failed')
  return res.json()
}

export async function searchAll(query: string) {
  const res = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`)
  if (!res.ok) throw new Error('Search failed')
  return res.json()
}

export async function runSimulation(req: {
  topology_id?: string
  custom_topology?: TopologyConfig
  sender_id: string
  receiver_id: string
  app_protocol?: string
  transport_protocol?: string
  payload?: string
  packet_size_bytes?: number
  override_mtu?: number
  override_loss_rate?: number
  override_bit_error_rate?: number
  tcp_algorithm?: string
}): Promise<SimulationResponse> {
  const res = await fetch(`${BASE_URL}/simulations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req)
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Simulation execution failed')
  }
  return res.json()
}

