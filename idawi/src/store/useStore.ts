import { create } from 'zustand';

export interface Clip {
  id: string;
  name: string;
  startTime: number;
  duration: number;
  color?: string;
}

export interface Track {
  id: string;
  name: string;
  type: 'audio' | 'midi' | 'aux';
  color: string;
  volume: number;
  pan: number;
  muted: boolean;
  solo: boolean;
  armed: boolean;
  clips: Clip[];
}

interface StoreState {
  // Playback state
  isPlaying: boolean;
  isRecording: boolean;
  currentTime: number;
  tempo: number;
  timeSignature: [number, number];

  // Project state
  projectName: string;
  tracks: Track[];

  // UI state
  currentSide: 'A' | 'B';
  selectedTrackId: string | null;

  // Actions
  setPlaying: (playing: boolean) => void;
  setRecording: (recording: boolean) => void;
  setCurrentTime: (time: number) => void;
  setTempo: (tempo: number) => void;
  toggleSide: () => void;
  addTrack: (track: Omit<Track, 'id'>) => void;
  updateTrack: (id: string, updates: Partial<Track>) => void;
  removeTrack: (id: string) => void;
  selectTrack: (id: string | null) => void;
}

const defaultTracks: Track[] = [
  {
    id: '1',
    name: 'Drums',
    type: 'audio',
    color: '#ff5500',
    volume: 0.8,
    pan: 0,
    muted: false,
    solo: false,
    armed: false,
    clips: [
      { id: 'c1', name: 'Beat 1', startTime: 0, duration: 4 },
      { id: 'c2', name: 'Beat 2', startTime: 4, duration: 4 },
    ],
  },
  {
    id: '2',
    name: 'Bass',
    type: 'midi',
    color: '#00aaff',
    volume: 0.7,
    pan: 0,
    muted: false,
    solo: false,
    armed: false,
    clips: [
      { id: 'c3', name: 'Bass Line', startTime: 0, duration: 8 },
    ],
  },
  {
    id: '3',
    name: 'Synth Lead',
    type: 'midi',
    color: '#aa00ff',
    volume: 0.6,
    pan: 0.2,
    muted: false,
    solo: false,
    armed: false,
    clips: [
      { id: 'c4', name: 'Melody', startTime: 4, duration: 4 },
    ],
  },
  {
    id: '4',
    name: 'Pad',
    type: 'midi',
    color: '#00ff88',
    volume: 0.5,
    pan: -0.2,
    muted: false,
    solo: false,
    armed: false,
    clips: [
      { id: 'c5', name: 'Atmosphere', startTime: 0, duration: 8 },
    ],
  },
  {
    id: '5',
    name: 'Vocals',
    type: 'audio',
    color: '#ffaa00',
    volume: 0.9,
    pan: 0,
    muted: false,
    solo: false,
    armed: false,
    clips: [],
  },
  {
    id: '6',
    name: 'FX',
    type: 'aux',
    color: '#ff00aa',
    volume: 0.4,
    pan: 0,
    muted: false,
    solo: false,
    armed: false,
    clips: [],
  },
];

export const useStore = create<StoreState>((set) => ({
  // Initial state
  isPlaying: false,
  isRecording: false,
  currentTime: 0,
  tempo: 120,
  timeSignature: [4, 4],
  projectName: 'Untitled Project',
  tracks: defaultTracks,
  currentSide: 'A',
  selectedTrackId: null,

  // Actions
  setPlaying: (playing) => set({ isPlaying: playing }),
  setRecording: (recording) => set({ isRecording: recording }),
  setCurrentTime: (time) => set({ currentTime: time }),
  setTempo: (tempo) => set({ tempo }),

  toggleSide: () => set((state) => ({
    currentSide: state.currentSide === 'A' ? 'B' : 'A'
  })),

  addTrack: (track) => set((state) => ({
    tracks: [...state.tracks, { ...track, id: `track-${Date.now()}` }]
  })),

  updateTrack: (id, updates) => set((state) => ({
    tracks: state.tracks.map((t) =>
      t.id === id ? { ...t, ...updates } : t
    )
  })),

  removeTrack: (id) => set((state) => ({
    tracks: state.tracks.filter((t) => t.id !== id)
  })),

  selectTrack: (id) => set({ selectedTrackId: id }),
}));
