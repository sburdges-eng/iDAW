# iDAWi - intelligent Digital Audio Workstation

> "Interrogate Before Generate" - The tool shouldn't finish art for people. It should make them braver.

iDAWi is a dual-interface DAW that combines professional audio production (Side A) with emotion-driven AI composition (Side B).

## Features

### Side A: Professional DAW
- Timeline with multi-track editing
- 8-channel mixer with real-time VU meters
- Transport controls (Play, Pause, Stop, Record)
- Tempo and time signature control
- Pan knobs with smooth drag interaction

### Side B: Emotion Interface
- Emotion Wheel with 15+ categorized emotions
- 3-Phase Interrogation System:
  - Phase 0: Core Wound/Desire
  - Phase 1: Emotional Intent
  - Phase 2: Technical Constraints
- Ghost Writer AI suggestions
- Rule-breaking recommendations with justifications

## Tech Stack

- **Frontend**: Tauri 2.0 + React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS (Ableton-style dark theme)
- **State**: Zustand with persistence
- **Animation**: Framer Motion
- **Backend**: Rust (audio engine) + Python (Music Brain)
- **IPC**: Tauri commands bridge all systems

## Architecture

```
┌─────────────────────────────────────────┐
│  Tauri Window (Press Cmd+E to flip)     │
│                                         │
│  SIDE A (DAW)          SIDE B (Emotion) │
│  ├── Timeline          ├── Interrogator │
│  ├── Mixer             ├── Emotion Wheel│
│  │   ├── VU Meters     ├── Ghost Writer │
│  │   ├── Pan Knobs     └── Rule Breaker │
│  │   └── Faders                         │
│  └── Transport                          │
│         ↕                      ↕         │
│    Tauri IPC           Tauri IPC        │
│         ↕                      ↕         │
│  Rust Audio Engine    Python Music Brain│
└─────────────────────────────────────────┘
```

## Quick Start

```bash
# Install dependencies
npm install

# Install Rust dependencies
cd src-tauri && cargo build && cd ..

# Run development server (web only)
npm run dev

# Run with Tauri (native app)
npm run tauri dev

# Build for production
npm run tauri build
```

## Project Structure

```
iDAWi/
├── src/                       # React TypeScript frontend
│   ├── components/
│   │   ├── SideA/            # DAW interface components
│   │   │   ├── Timeline.tsx  # Track arrangement view
│   │   │   ├── Mixer.tsx     # Channel mixer with VU meters
│   │   │   ├── VUMeter.tsx   # Real-time level meters
│   │   │   ├── Knob.tsx      # Draggable pan/parameter knobs
│   │   │   ├── Transport.tsx # Play/Stop/Record controls
│   │   │   └── Toolbar.tsx   # Top toolbar
│   │   ├── SideB/            # Emotion interface components
│   │   │   ├── EmotionWheel.tsx
│   │   │   ├── Interrogator.tsx
│   │   │   ├── GhostWriter.tsx
│   │   │   └── RuleBreaker.tsx
│   │   └── shared/           # Shared components
│   ├── hooks/                # Custom React hooks
│   │   ├── useMusicBrain.ts  # Music Brain API integration
│   │   └── useTauriAudio.ts  # Tauri audio bridge
│   ├── store/                # Zustand state management
│   │   └── useStore.ts       # Central app state
│   └── index.css             # Tailwind + custom styles
├── src-tauri/                # Rust backend
│   └── src/
│       ├── main.rs           # Tauri entry point
│       ├── lib.rs            # Tauri commands
│       └── audio_engine.rs   # Audio processing
├── music-brain/              # Python Music Brain bridge
│   ├── bridge.py             # IPC bridge script
│   └── music_brain/          # Extracted modules
├── public/                   # Static assets
├── index.html                # Entry HTML
├── tailwind.config.js        # Tailwind configuration
├── vite.config.ts            # Vite configuration
└── package.json              # Node dependencies
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+E` / `Ctrl+E` | Flip between Side A and Side B |
| `Space` | Play/Pause |
| `Cmd+N` | New project |
| `Cmd+S` | Save project |
| `Cmd+Z` | Undo |
| `Cmd+Shift+Z` | Redo |

## Component Features

### VU Meter
- Real-time level visualization
- Stereo left/right channels
- Peak hold indicator (1 second decay)
- Gradient coloring (green → yellow → red)
- Scale marks for reference

### Knob
- Drag up/down to adjust value
- Double-click to reset to center
- Size variants (sm, md, lg)
- Optional value display
- Custom formatters

### Mixer
- Collapsible panel
- Per-track: name, pan, VU meters, fader, mute/solo
- Master channel with summed levels
- Color-coded track indicators
- dB readout per channel

## Philosophy

Unlike traditional DAWs:
1. ❌ Pick plugin → Tweak knobs → Hope it sounds good
2. ✅ Describe emotion → AI suggests rules to break → Generate with intent

**Every parameter has emotional justification.**

> "The audience doesn't hear 'borrowed from Dorian.' They hear 'that part made me cry.'"

## Development

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Preview production build
npm run preview
```

## License

MIT License - Sean Burdges

## Credits

Built by Sean Burdges
Part of the iDAW ecosystem
