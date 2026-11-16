import { create } from 'zustand'
import {
  SimulationResponse,
  SimulationEventModel,
  PacketModel,
  TopologyConfig
} from '../types'

interface NetLabStore {
  activeTab: string
  setActiveTab: (tab: string) => void

  // Global search modal
  isSearchOpen: boolean
  setSearchOpen: (open: boolean) => void

  // Active Simulation State
  activeSimulation: SimulationResponse | null
  currentStepIndex: number
  selectedEvent: SimulationEventModel | null
  selectedPacket: PacketModel | null
  isPlaying: boolean
  playbackSpeedMs: number

  setActiveSimulation: (sim: SimulationResponse | null) => void
  setCurrentStepIndex: (index: number) => void
  setSelectedEvent: (event: SimulationEventModel | null) => void
  setSelectedPacket: (packet: PacketModel | null) => void
  setIsPlaying: (playing: boolean) => void
  setPlaybackSpeedMs: (speed: number) => void

  // Step controls
  stepForward: () => void
  stepBackward: () => void
  resetSimulation: () => void

  // Progress & Bookmarks (persisted in localStorage)
  completedConcepts: string[]
  completedScenarios: string[]
  answeredQuestions: Record<string, boolean> // questionId -> isCorrect
  bookmarkedQuestions: string[]

  markConceptComplete: (id: string) => void
  markScenarioComplete: (id: string) => void
  recordQuestionAnswer: (id: string, isCorrect: boolean) => void
  toggleBookmarkQuestion: (id: string) => void
}

export const useNetLabStore = create<NetLabStore>((set, get) => ({
  activeTab: 'home',
  setActiveTab: (tab) => set({ activeTab: tab }),

  isSearchOpen: false,
  setSearchOpen: (open) => set({ isSearchOpen: open }),

  activeSimulation: null,
  currentStepIndex: 0,
  selectedEvent: null,
  selectedPacket: null,
  isPlaying: false,
  playbackSpeedMs: 700,

  setActiveSimulation: (sim) => {
    const firstEvent = sim?.events?.[0] || null
    set({
      activeSimulation: sim,
      currentStepIndex: 0,
      selectedEvent: firstEvent,
      selectedPacket: firstEvent?.packet_snapshot || sim?.packets?.[0] || null,
      isPlaying: false
    })
  },

  setCurrentStepIndex: (index) => {
    const sim = get().activeSimulation
    if (!sim) return
    const clamped = Math.max(0, Math.min(index, sim.events.length - 1))
    const event = sim.events[clamped] || null
    set({
      currentStepIndex: clamped,
      selectedEvent: event,
      selectedPacket: event?.packet_snapshot || get().selectedPacket
    })
  },

  setSelectedEvent: (event) => set({
    selectedEvent: event,
    selectedPacket: event?.packet_snapshot || get().selectedPacket
  }),

  setSelectedPacket: (packet) => set({ selectedPacket: packet }),

  setIsPlaying: (playing) => set({ isPlaying: playing }),

  setPlaybackSpeedMs: (speed) => set({ playbackSpeedMs: speed }),

  stepForward: () => {
    const { currentStepIndex, activeSimulation } = get()
    if (!activeSimulation) return
    if (currentStepIndex < activeSimulation.events.length - 1) {
      get().setCurrentStepIndex(currentStepIndex + 1)
    } else {
      set({ isPlaying: false })
    }
  },

  stepBackward: () => {
    const { currentStepIndex } = get()
    if (currentStepIndex > 0) {
      get().setCurrentStepIndex(currentStepIndex - 1)
    }
  },

  resetSimulation: () => {
    get().setCurrentStepIndex(0)
    set({ isPlaying: false })
  },

  // Progress state
  completedConcepts: JSON.parse(localStorage.getItem('netlab_concepts') || '[]'),
  completedScenarios: JSON.parse(localStorage.getItem('netlab_scenarios') || '[]'),
  answeredQuestions: JSON.parse(localStorage.getItem('netlab_answers') || '{}'),
  bookmarkedQuestions: JSON.parse(localStorage.getItem('netlab_bookmarks') || '[]'),

  markConceptComplete: (id) => {
    const updated = Array.from(new Set([...get().completedConcepts, id]))
    localStorage.setItem('netlab_concepts', JSON.stringify(updated))
    set({ completedConcepts: updated })
  },

  markScenarioComplete: (id) => {
    const updated = Array.from(new Set([...get().completedScenarios, id]))
    localStorage.setItem('netlab_scenarios', JSON.stringify(updated))
    set({ completedScenarios: updated })
  },

  recordQuestionAnswer: (id, isCorrect) => {
    const updated = { ...get().answeredQuestions, [id]: isCorrect }
    localStorage.setItem('netlab_answers', JSON.stringify(updated))
    set({ answeredQuestions: updated })
  },

  toggleBookmarkQuestion: (id) => {
    const current = get().bookmarkedQuestions
    const updated = current.includes(id) ? current.filter((q) => q !== id) : [...current, id]
    localStorage.setItem('netlab_bookmarks', JSON.stringify(updated))
    set({ bookmarkedQuestions: updated })
  }
}))

