export type DeviceType =
  | 'laptop'
  | 'desktop'
  | 'mobile'
  | 'router'
  | 'switch'
  | 'server'
  | 'dns_server'
  | 'firewall'
  | 'access_point'
  | 'load_balancer'
  | 'cdn_server'
  | 'cloud'

export type LinkMedium = 'ethernet' | 'wifi' | 'wan' | 'fiber'
export type LayerType = 'physical' | 'datalink' | 'network' | 'transport' | 'application'

export interface InterfaceConfig {
  name: string
  ip_address: string
  subnet_mask: string
  mac_address: string
  is_up?: boolean
}

export interface DeviceConfig {
  id: string
  label: string
  type: DeviceType
  position: { x: number; y: number }
  interfaces: InterfaceConfig[]
  default_gateway?: string
  dns_server?: string
  open_ports?: number[]
  nat_enabled?: boolean
  services?: string[]
}

export interface LinkConfig {
  id: string
  source_id: string
  target_id: string
  medium: LinkMedium
  bandwidth_mbps: number
  latency_ms: number
  mtu_bytes: number
  loss_rate: number
  bit_error_rate: number
  is_active: boolean
}

export interface TopologyConfig {
  id: string
  name: string
  description?: string
  devices: DeviceConfig[]
  links: LinkConfig[]
}

export interface TCPFlags {
  syn: boolean
  ack: boolean
  fin: boolean
  rst: boolean
  psh: boolean
  urg: boolean
}

export interface DataLinkHeader {
  src_mac: string
  dst_mac: string
  ethertype: string
  crc32: string
  is_corrupted: boolean
  frame_type: string
  frame_status: string
}

export interface NetworkHeader {
  version: number
  ihl: number
  tos_dscp: number
  total_length: number
  identification: number
  flags_df: boolean
  flags_mf: boolean
  fragment_offset: number
  ttl: number
  protocol: string
  header_checksum: string
  src_ip: string
  dst_ip: string
}

export interface TransportHeader {
  protocol: string
  src_port: number
  dst_port: number
  seq_num: number
  ack_num: number
  flags: TCPFlags
  window_size: number
  checksum: string
  urgent_pointer: number
}

export interface ApplicationHeader {
  protocol: string
  message_type: string
  method_or_status: string
  url_or_path: string
  headers: Record<string, string>
  payload: string
  dns_query_domain?: string
  dns_record_type?: string
  dns_answers?: any[]
}

export interface PacketModel {
  id: string
  size_bytes: number
  app_header?: ApplicationHeader
  transport_header?: TransportHeader
  network_header?: NetworkHeader
  datalink_header?: DataLinkHeader
  raw_payload: string
  status: 'CREATED' | 'IN_TRANSIT' | 'DELIVERED' | 'DROPPED' | 'CORRUPTED'
  current_node: string
  next_node?: string
  creation_time: number
}

export interface EventExplanation {
  what: string
  why: string
  protocol: string
  data_changed: string
  counterfactual: string
  real_world: string
}

export interface SimulationEventModel {
  event_id: string
  timestamp_ms: number
  event_type: string
  source_node: string
  destination_node?: string
  packet_id?: string
  packet_summary?: string
  layer: LayerType
  details: Record<string, any>
  explanation: EventExplanation
  packet_snapshot?: PacketModel
}

export interface SimulationStats {
  packets_transmitted: number
  packets_received: number
  packets_lost: number
  frames_corrupted: number
  retransmissions: number
  average_latency_ms: number
  throughput_kbps: number
  packet_delivery_ratio: number
  tcp_cwnd_history: Array<{ step: number; cwnd: number; ssthresh: number; state: string }>
  fragment_count: number
  connection_establishment_time_ms?: number
}

export interface SimulationResponse {
  simulation_id: string
  status: string
  current_step: number
  total_steps: number
  events: SimulationEventModel[]
  packets: PacketModel[]
  stats: SimulationStats
  topology: TopologyConfig
}

export interface ScenarioMeta {
  id: string
  category: string
  title: string
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced'
  summary: string
  core_concept: string
  key_question: string
  node_count: number
  link_count: number
}

export interface ScenarioDetail extends ScenarioMeta {
  topology: TopologyConfig
  walkthrough: Array<{ step: number; actor: string; action: string }>
  explanation: string
}

export interface ConceptItem {
  id: string
  name: string
  layer: string
  difficulty: string
  summary: string
  simple_explanation: string
  technical_explanation: string
  common_mistakes: string
  real_world_application: string
  interactive_type?: string
}

export interface InterviewQuestion {
  id: string
  category: string
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced'
  question: string
  options: string[]
  related_concept?: string
  scenario_link?: string
}

export interface VerifyAnswerResponse {
  question_id: string
  is_correct: boolean
  selected_option_index: number
  correct_option_index: number
  explanation: string
  why_incorrect: string[]
  follow_up?: string
  follow_up_answer?: string
  related_concept?: string
  scenario_link?: string
}

