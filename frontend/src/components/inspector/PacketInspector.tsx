import React, { useState } from 'react'
import {
  Layers,
  FileCode,
  Binary,
  ShieldAlert,
  ShieldCheck,
  Eye,
  CheckCircle,
  Copy
} from 'lucide-react'
import { PacketModel } from '../../types'

interface PacketInspectorProps {
  packet: PacketModel | null
}

export const PacketInspector: React.FC<PacketInspectorProps> = ({ packet }) => {
  const [activeTab, setActiveTab] = useState<'structured' | 'encapsulation' | 'hexdump'>('structured')
  const [copied, setCopied] = useState(false)

  if (!packet) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center text-[#9CA3AF] border border-[#E8E8E5] rounded-xl bg-white">
        <Layers className="h-10 w-10 mb-2 stroke-1 text-[#D1D5DB]" />
        <p className="text-sm font-medium text-[#6B7280]">No Packet Selected</p>
        <p className="text-xs text-[#9CA3AF] mt-1">
          Click on any packet or timeline event to inspect multi-layer headers, CRC checksums, and hex bytes.
        </p>
      </div>
    )
  }

  const { app_header, transport_header, network_header, datalink_header } = packet

  // Generate realistic hex dump representation of packet bytes
  const generateHexDump = () => {
    const lines = []
    const rawStr = `ETH[${datalink_header?.src_mac || 'SRC'}->${datalink_header?.dst_mac || 'DST'}] IP[${network_header?.src_ip || '192.168.1.1'}->${network_header?.dst_ip || '10.0.0.1'}] ${transport_header?.protocol || 'TCP'}[${transport_header?.src_port}->${transport_header?.dst_port}] PAYLOAD[${packet.raw_payload || 'DATA'}] CRC[${datalink_header?.crc32 || '0x0000'}]`
    const bytes = new TextEncoder().encode(rawStr)

    for (let i = 0; i < bytes.length; i += 16) {
      const slice = bytes.slice(i, i + 16)
      const hex = Array.from(slice)
        .map((b) => b.toString(16).padStart(2, '0').toUpperCase())
        .join(' ')
      const ascii = Array.from(slice)
        .map((b) => (b >= 32 && b <= 126 ? String.fromCharCode(b) : '.'))
        .join('')
      const offset = i.toString(16).padStart(4, '0').toUpperCase()
      lines.push(`${offset}   ${hex.padEnd(48, ' ')}   |${ascii}|`)
    }
    return lines.join('\n')
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(packet, null, 2))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-[#E8E8E5] bg-white overflow-hidden shadow-xs">
      {/* Inspector Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-[#E8E8E5] bg-[#FAFAFA]">
        <div className="flex items-center space-x-2">
          <Eye className="h-4 w-4 text-[#4F6BED]" />
          <span className="text-xs font-semibold text-[#202124]">Packet Inspector</span>
          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-200 text-[#4B5563]">
            ID: {packet.id}
          </span>
          <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-blue-50 text-[#4F6BED]">
            {packet.size_bytes} Bytes
          </span>
        </div>

        {/* View mode toggle */}
        <div className="flex items-center space-x-1">
          <div className="flex rounded-md border border-[#E8E8E5] bg-white p-0.5 text-xs">
            <button
              onClick={() => setActiveTab('structured')}
              className={`px-2 py-0.5 rounded ${
                activeTab === 'structured' ? 'bg-[#4F6BED] text-white font-medium' : 'text-[#6B7280] hover:text-[#202124]'
              }`}
            >
              Headers
            </button>
            <button
              onClick={() => setActiveTab('encapsulation')}
              className={`px-2 py-0.5 rounded ${
                activeTab === 'encapsulation' ? 'bg-[#4F6BED] text-white font-medium' : 'text-[#6B7280] hover:text-[#202124]'
              }`}
            >
              Encapsulation
            </button>
            <button
              onClick={() => setActiveTab('hexdump')}
              className={`px-2 py-0.5 rounded ${
                activeTab === 'hexdump' ? 'bg-[#4F6BED] text-white font-medium' : 'text-[#6B7280] hover:text-[#202124]'
              }`}
            >
              Hex Dump
            </button>
          </div>

          <button
            onClick={handleCopy}
            className="p-1 text-[#6B7280] hover:text-[#202124] rounded hover:bg-gray-100"
            title="Copy packet JSON"
          >
            {copied ? <CheckCircle className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* STRUCTURED HEADERS VIEW */}
        {activeTab === 'structured' && (
          <div className="space-y-3">
            {/* 1. Application Layer */}
            {app_header && (
              <div className="rounded-lg border border-purple-200 bg-purple-50/30 p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-purple-700">
                    Application Layer ({app_header.protocol})
                  </span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-100 text-purple-800">
                    {app_header.message_type}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-[#6B7280]">Method / Status:</span>{' '}
                    <span className="font-semibold text-[#202124]">{app_header.method_or_status}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">URL / Path:</span>{' '}
                    <span className="font-mono text-[#202124]">{app_header.url_or_path || '/'}</span>
                  </div>
                </div>
                {app_header.dns_query_domain && (
                  <div className="mt-2 text-xs">
                    <span className="text-[#6B7280]">DNS Query:</span>{' '}
                    <span className="font-mono font-medium text-purple-900">{app_header.dns_query_domain}</span>
                  </div>
                )}
                {app_header.payload && (
                  <div className="mt-2 text-[11px] font-mono bg-white p-2 rounded border border-purple-100 text-purple-950 overflow-x-auto whitespace-pre-wrap">
                    {app_header.payload}
                  </div>
                )}
              </div>
            )}

            {/* 2. Transport Layer */}
            {transport_header && (
              <div className="rounded-lg border border-blue-200 bg-blue-50/30 p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-blue-700">
                    Transport Layer ({transport_header.protocol})
                  </span>
                  <div className="flex items-center space-x-1">
                    {transport_header.flags && (
                      <span className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-blue-100 text-blue-800">
                        Flags: {[
                          transport_header.flags.syn && 'SYN',
                          transport_header.flags.ack && 'ACK',
                          transport_header.flags.fin && 'FIN',
                          transport_header.flags.rst && 'RST'
                        ].filter(Boolean).join(',') || 'NONE'}
                      </span>
                    )}
                  </div>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div>
                    <span className="text-[#6B7280]">Src Port:</span>{' '}
                    <span className="font-mono font-semibold">{transport_header.src_port}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Dst Port:</span>{' '}
                    <span className="font-mono font-semibold">{transport_header.dst_port}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Seq Num:</span>{' '}
                    <span className="font-mono font-semibold">{transport_header.seq_num}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Ack Num:</span>{' '}
                    <span className="font-mono font-semibold">{transport_header.ack_num}</span>
                  </div>
                </div>
                <div className="mt-2 flex items-center justify-between text-xs text-[#6B7280] pt-2 border-t border-blue-100">
                  <span>Window Size: <strong className="text-[#202124]">{transport_header.window_size}</strong></span>
                  <span>Checksum: <strong className="text-[#202124] font-mono">{transport_header.checksum}</strong></span>
                </div>
              </div>
            )}

            {/* 3. Network Layer */}
            {network_header && (
              <div className="rounded-lg border border-emerald-200 bg-emerald-50/30 p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700">
                    Network Layer (IPv{network_header.version})
                  </span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                    TTL: {network_header.ttl}
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-[#6B7280]">Source IP:</span>{' '}
                    <span className="font-mono font-bold text-emerald-900">{network_header.src_ip}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Destination IP:</span>{' '}
                    <span className="font-mono font-bold text-emerald-900">{network_header.dst_ip}</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs mt-2 pt-2 border-t border-emerald-100">
                  <div>
                    <span className="text-[#6B7280]">Total Length:</span>{' '}
                    <span className="font-mono">{network_header.total_length} B</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Identification:</span>{' '}
                    <span className="font-mono">{network_header.identification}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">MF Flag:</span>{' '}
                    <span className={`font-mono font-semibold ${network_header.flags_mf ? 'text-amber-600' : 'text-gray-600'}`}>
                      {network_header.flags_mf ? '1 (More Frags)' : '0 (Last)'}
                    </span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Frag Offset:</span>{' '}
                    <span className="font-mono">{network_header.fragment_offset} (×8 B)</span>
                  </div>
                </div>
                <div className="mt-1 text-xs text-[#6B7280]">
                  Checksum: <span className="font-mono text-[#202124]">{network_header.header_checksum}</span> (16-bit One's Complement)
                </div>
              </div>
            )}

            {/* 4. Data Link Layer */}
            {datalink_header && (
              <div className="rounded-lg border border-amber-200 bg-amber-50/30 p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-amber-700">
                    Data Link Layer ({datalink_header.frame_type})
                  </span>
                  <div className="flex items-center space-x-1">
                    {datalink_header.is_corrupted ? (
                      <span className="flex items-center space-x-1 text-[10px] font-semibold px-1.5 py-0.5 rounded bg-red-100 text-red-700">
                        <ShieldAlert className="h-3 w-3" />
                        <span>CRC CORRUPTED</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-1 text-[10px] font-semibold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-700">
                        <ShieldCheck className="h-3 w-3" />
                        <span>CRC VALID</span>
                      </span>
                    )}
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-[#6B7280]">Source MAC:</span>{' '}
                    <span className="font-mono font-bold text-amber-900">{datalink_header.src_mac}</span>
                  </div>
                  <div>
                    <span className="text-[#6B7280]">Destination MAC:</span>{' '}
                    <span className="font-mono font-bold text-amber-900">{datalink_header.dst_mac}</span>
                  </div>
                </div>
                <div className="mt-2 flex items-center justify-between text-xs pt-2 border-t border-amber-100">
                  <span>EtherType: <strong className="font-mono text-[#202124]">{datalink_header.ethertype}</strong></span>
                  <span>FCS / CRC-32: <strong className="font-mono text-[#202124]">{datalink_header.crc32}</strong></span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ENCAPSULATION VIEW */}
        {activeTab === 'encapsulation' && (
          <div className="space-y-2">
            <p className="text-xs text-[#6B7280] mb-3">
              Packet encapsulation from Layer 7 (Application payload) wrapped downward inside Transport, Network, and Data Link envelopes.
            </p>
            {/* Layer 2 Frame Wrapper */}
            <div className="rounded-lg border-2 border-amber-400 bg-amber-50/40 p-3">
              <div className="text-[10px] font-bold uppercase tracking-wider text-amber-800 mb-1">
                Ethernet Frame [Preamble | Dst MAC | Src MAC | Type: {datalink_header?.ethertype}]
              </div>

              {/* Layer 3 IP Packet Wrapper */}
              <div className="rounded-md border-2 border-emerald-400 bg-emerald-50/40 p-3 my-2">
                <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 mb-1">
                  IPv4 Datagram [Version: 4 | TTL: {network_header?.ttl} | {network_header?.src_ip} → {network_header?.dst_ip}]
                </div>

                {/* Layer 4 Segment Wrapper */}
                <div className="rounded-md border-2 border-blue-400 bg-blue-50/40 p-3 my-2">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-blue-800 mb-1">
                    {transport_header?.protocol || 'TCP'} Segment [Ports: {transport_header?.src_port} → {transport_header?.dst_port} | Seq: {transport_header?.seq_num}]
                  </div>

                  {/* Layer 7 Application Data */}
                  <div className="rounded border-2 border-purple-400 bg-purple-50 p-2.5 my-2">
                    <div className="text-[10px] font-bold uppercase tracking-wider text-purple-800 mb-1">
                      Application Payload ({app_header?.protocol || 'DATA'})
                    </div>
                    <div className="text-xs font-mono text-purple-950 bg-white p-2 rounded border border-purple-200">
                      {packet.raw_payload || 'No raw payload'}
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-[10px] font-mono text-right text-amber-800 mt-1 font-semibold">
                Frame Check Sequence: CRC-32 = {datalink_header?.crc32}
              </div>
            </div>
          </div>
        )}

        {/* HEX DUMP VIEW */}
        {activeTab === 'hexdump' && (
          <div>
            <p className="text-xs text-[#6B7280] mb-2">Raw serialized frame bytes and ASCII representation:</p>
            <pre className="text-[11px] font-mono bg-[#1E1E1E] text-[#D4D4D4] p-3 rounded-lg overflow-x-auto leading-relaxed shadow-inner">
              {generateHexDump()}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

