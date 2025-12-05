# iDAWi - intelligent Digital Audio Workstation (interface)

> Professional DAW UI with emotion-driven music production
>
> **Philosophy: "Interrogate Before Generate"**

## What is iDAWi?

iDAWi (lowercase 'i' = intelligent) is a standalone DAW interface that combines:

- **Side A**: Professional timeline, mixer, and transport (like Ableton)
- **Side B**: Emotion-driven interrogation and AI Ghost Writer
- **Flip Toggle**: Press `⌘E` (Mac) or `Ctrl+E` (Windows/Linux) to switch between sides

## Tech Stack

- **Frontend**: Tauri 2.0 + React 18 + TypeScript
- **Styling**: Tailwind CSS (Ableton dark theme)
- **Backend**: Rust (audio engine) + Python (Music Brain)
- **IPC**: Tauri commands bridge all systems

## Architecture

```
┌─────────────────────────────────────────┐
│  Tauri Window (Press ⌘E to flip)       │
│                                         │
│  SIDE A (DAW)          SIDE B (Emotion) │
│  ├── Timeline          ├── Interrogator │
│  ├── Mixer             ├── Emotion Wheel│
│  ├── Transport         ├── Ghost Writer │
│  └── Plugin Rack       └── Rule Breaker │
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
cd src-tauri && cargo build && cd ..

# Run development server
npm run tauri dev

# Build for production
npm run tauri build
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘E / Ctrl+E` | Flip between Side A and Side B |
| `Space` | Play/Pause |
| `⌘N` | New project |
| `⌘S` | Save project |
| `⌘Z` | Undo |
| `⌘⇧Z` | Redo |

## Philosophy

Unlike traditional DAWs:

1. ❌ Pick plugin → Tweak knobs → Hope it sounds good
2. ✅ Describe emotion → AI suggests rules to break → Generate with intent

**Every parameter has emotional justification.**

## Project Structure

```
iDAWi/
├── src/                    # React TypeScript frontend
│   ├── components/
│   │   ├── SideA/         # DAW interface components
│   │   ├── SideB/         # Emotion interface components
│   │   └── shared/        # Shared components
│   ├── hooks/             # Custom React hooks
│   ├── store/             # Zustand state management
│   └── styles/            # CSS and Tailwind config
├── src-tauri/             # Rust backend
│   └── src/
│       ├── main.rs        # Tauri entry point
│       └── audio_engine.rs # Audio processing
├── music-brain/           # Python Music Brain bridge
│   ├── bridge.py          # IPC bridge script
│   └── music_brain/       # Extracted modules
└── public/                # Static assets
```

## License

MIT

## Credits

Built by Sean Burdges
Part of the iDAW ecosystem
