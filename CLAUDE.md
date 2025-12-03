# CLAUDE.md - AI Assistant Guide for iDAW

> Comprehensive guide for AI assistants working with the iDAW (Intelligent Digital Audio Workstation) monorepo.

## Project Philosophy

**"Interrogate Before Generate"** - The tool shouldn't finish art for people. It should make them braver.

iDAW is a multi-component music production platform that combines:
- Real-time C++ audio processing (JUCE-based)
- Python-based music intelligence and AI-assisted composition
- Multi-AI collaboration orchestration
- Intent-driven creative workflows

---

## Repository Architecture

This is a **monorepo** containing four major subsystems:

```
iDAW/
├── [Root Level]           # MCP Multi-AI Workstation
├── DAiW-Music-Brain/      # Python Music Intelligence Toolkit
├── iDAW_Core/             # JUCE Plugin Suite (C++)
├── src_penta-core/        # Penta-Core Real-time Engines (C++)
├── include/penta/         # Penta-Core Headers
├── src/                   # Core C++ DSP/MIDI modules
├── Python_Tools/          # Additional Python utilities
├── vault/                 # Obsidian Knowledge Base
└── tests*/                # Test suites
```

---

## 1. MCP Multi-AI Workstation (Root Level)

Orchestration system for multi-AI collaboration on iDAW development.

### Key Files
| File | Purpose |
|------|---------|
| `__init__.py` | Package exports, version 1.0.0 |
| `cli.py` | CLI entry point for workstation commands |
| `orchestrator.py` | Central coordinator (`Workstation` class) |
| `models.py` | Data models (AIAgent, Proposal, Phase, etc.) |
| `proposals.py` | Proposal management system |
| `phases.py` | Phase tracking for iDAW development |
| `cpp_planner.py` | C++ transition planning |
| `ai_specializations.py` | AI agent capabilities and task assignment |
| `server.py` | MCP server implementation |
| `debug.py` | Debug protocol and logging |

### CLI Commands
```bash
# From project root
python -m cli status              # Show workstation dashboard
python -m cli register claude     # Register as Claude
python -m cli propose claude "Title" "Desc" architecture
python -m cli vote claude PROP_ID 1
python -m cli phases              # Show phase progress
python -m cli cpp                 # Show C++ transition plan
python -m cli ai                  # Show AI specializations
python -m cli server              # Run MCP server
```

### AI Agents
- `claude` - Code architecture, real-time safety, complex debugging
- `chatgpt` - Theory analysis, explanations, documentation
- `gemini` - Cross-language patterns, multi-modal analysis
- `github_copilot` - Code completion, boilerplate generation

---

## 2. DAiW-Music-Brain (Python Toolkit)

Music production intelligence library for groove extraction, chord analysis, and intent-based generation.

### Directory Structure
```
DAiW-Music-Brain/
├── music_brain/
│   ├── __init__.py           # Public API (v0.2.0)
│   ├── cli.py                # `daiw` CLI command
│   ├── data/                 # JSON/YAML data files
│   ├── groove/               # Groove extraction/application
│   ├── structure/            # Chord/progression analysis
│   ├── session/              # Intent schema, teaching, interrogation
│   ├── audio/                # Audio feel analysis
│   └── daw/                  # DAW integration (Logic Pro)
├── tests/
└── pyproject.toml
```

### CLI Commands (`daiw`)
```bash
daiw extract drums.mid            # Extract groove from MIDI
daiw apply --genre funk track.mid # Apply genre groove template
daiw analyze --chords song.mid    # Analyze chord progression
daiw diagnose "F-C-Am-Dm"         # Diagnose harmonic issues
daiw intent new --title "My Song" # Create intent template
daiw intent suggest grief         # Suggest rules to break
daiw teach rulebreaking           # Interactive teaching mode
```

### Three-Phase Intent Schema
1. **Phase 0: Core Wound/Desire** - `core_event`, `core_resistance`, `core_longing`
2. **Phase 1: Emotional Intent** - `mood_primary`, `vulnerability_scale`, `narrative_arc`
3. **Phase 2: Technical Constraints** - `technical_genre`, `technical_key`, `technical_rule_to_break`

### Rule-Breaking Categories
| Category | Examples | Effect |
|----------|----------|--------|
| Harmony | `HARMONY_AvoidTonicResolution` | Unresolved yearning |
| Rhythm | `RHYTHM_ConstantDisplacement` | Anxiety, restlessness |
| Arrangement | `ARRANGEMENT_BuriedVocals` | Dissociation |
| Production | `PRODUCTION_PitchImperfection` | Emotional honesty |

---

## 3. Penta-Core (C++ Real-time Engines)

High-performance, RT-safe audio analysis engines.

### Components
```
include/penta/
├── common/           # RTTypes, RTLogger, RTMemoryPool
├── groove/           # GrooveEngine, OnsetDetector, TempoEstimator, RhythmQuantizer
├── harmony/          # HarmonyEngine, ChordAnalyzer, ScaleDetector, VoiceLeading
├── diagnostics/      # DiagnosticsEngine, AudioAnalyzer, PerformanceMonitor
└── osc/              # OSCHub, OSCClient, OSCServer, RTMessageQueue
```

### Key Classes
- **GrooveEngine** - Combines onset detection, tempo estimation, rhythm quantization
- **HarmonyEngine** - Chord analysis, scale detection, voice leading suggestions
- **DiagnosticsEngine** - Audio analysis and performance monitoring
- **OSCHub** - Real-time OSC communication for DAW integration

### RT-Safety Rules
1. All `processAudio()` methods are marked `noexcept`
2. No memory allocation in audio callbacks
3. Use lock-free data structures for thread communication
4. `kDefaultSampleRate = 44100.0`

---

## 4. iDAW_Core (JUCE Plugin Suite)

Art-themed audio plugins built on JUCE 8.

### Plugins
| Plugin | Description | Shader |
|--------|-------------|--------|
| **Pencil** | Sketching/drafting audio ideas | Graphite |
| **Eraser** | Audio removal/cleanup | ChalkDust |
| **Palette** | Tonal coloring/mixing | Watercolor |
| **Smudge** | Audio blending/smoothing | Scrapbook |
| **Press** | Dynamics/compression | Heartbeat |
| **Trace** | Pattern following/automation | Spirograph |
| **Parrot** | Sample playback/mimicry | Feather |

### Dual-Heap Memory Architecture
```
Side A ("Work State"):
  - std::pmr::monotonic_buffer_resource
  - 4GB pre-allocated at startup
  - NO deallocation during runtime
  - Thread-safe for real-time audio

Side B ("Dream State"):
  - std::pmr::synchronized_pool_resource
  - Dynamic allocation allowed
  - Used for AI generation and UI
  - May block - NEVER use from audio thread

Communication: Lock-free ring buffer (Side B → Side A)
```

### PythonBridge
- Embeds Python interpreter in Side B (non-audio thread)
- `call_iMIDI()` - Pass knob state + text prompt, get MIDI buffer
- "Ghost Hands" - AI-suggested knob movements
- Fail-safe: Returns C Major chord on Python failure

---

## 5. Python Tools

Additional utilities in `Python_Tools/`:
```
Python_Tools/
├── audio/          # analyzer.py, audio_feel_extractor.py, audio_cataloger.py
├── groove/         # groove_extractor.py, groove_applicator.py, generator.py
├── structure/      # structure_extractor.py, structure_analyzer.py
└── utils/          # ppq.py, instruments.py, orchestral.py
```

---

## Development Setup

### Python Installation
```bash
# Core installation
pip install -e .

# With optional dependencies
pip install -e ".[dev]"      # pytest, black, flake8, mypy
pip install -e ".[audio]"    # librosa, soundfile
pip install -e ".[theory]"   # music21
pip install -e ".[ui]"       # streamlit
pip install -e ".[desktop]"  # streamlit + pywebview
pip install -e ".[build]"    # + pyinstaller
pip install -e ".[all]"      # Everything
```

### C++ Build
```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j
ctest --output-on-failure
```

### Requirements
- **Python**: 3.9+ (tested 3.9-3.13)
- **C++**: C++17 standard
- **CMake**: 3.22+
- **JUCE**: 8.0.10

---

## Running Tests

### Python Tests
```bash
# Music Brain tests
pytest tests_music-brain/ -v

# Penta-Core Python bindings tests
pytest tests_penta-core/ -v

# DAiW-Music-Brain internal tests
pytest DAiW-Music-Brain/tests/ -v

# All tests with coverage
pytest --cov=music_brain tests/
```

### C++ Tests
```bash
cd build
ctest --output-on-failure

# Run specific test suite
./tests/test_harmony
./tests/test_groove
./tests/test_simd
```

### Test Categories
- `test_harmony.cpp` - Chord analysis, scale detection
- `test_groove.cpp` - Onset detection, tempo estimation
- `test_simd.cpp` - SIMD optimizations
- `test_memory.cpp` - Memory pool tests

---

## CI/CD Workflows

### Main Workflows (`.github/workflows/`)

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Python tests, desktop builds (macOS/Linux/Windows) |
| `sprint_suite.yml` | Comprehensive sprint-based testing |
| `platform_support.yml` | Cross-platform Python testing |

### Sprint Suite Jobs
1. **Sprint 1** - Core testing & quality
2. **Sprint 2** - C++ build & integration
3. **Sprint 3** - Documentation checks
4. **Sprint 5** - Platform matrix (Linux/macOS/Windows × Python 3.9-3.13)
5. **Sprint 6** - Advanced theory and AI
6. **Sprint 7** - Mobile/Web (Streamlit)
7. **Sprint 8** - Enterprise tests

---

## Code Style & Conventions

### Python
```bash
# Format
black music_brain/ tests/

# Type check
mypy music_brain/

# Lint
flake8 music_brain/ tests/
```

- **Line length**: 100 characters
- **Formatter**: black
- **Type hints**: Required for public APIs

### C++
- **Standard**: C++17
- **Naming**: PascalCase for classes, camelCase for methods, snake_case for variables
- **RT-Safety**: Mark audio callbacks `noexcept`, no allocations
- **Memory**: Use `std::pmr` containers where possible

### Code Patterns

1. **Lazy imports** in Python CLI for fast startup
2. **Data classes** with `to_dict()`/`from_dict()` serialization
3. **Enums** for categorical values
4. **Singleton** pattern for managers (MemoryManager, Workstation)
5. **Lock-free ring buffers** for audio/UI communication

---

## Key Architecture Decisions

### 1. Dual-Engine Design
- **Side A (C++)**: Real-time audio, deterministic, lock-free
- **Side B (Python)**: AI generation, dynamic, may block

### 2. Intent-Driven Composition
- Emotional intent drives technical choices
- Phase 0 (why) must precede Phase 2 (how)
- Rule-breaking requires explicit justification

### 3. Multi-AI Collaboration
- Each AI has specializations and limitations
- Proposal system with voting
- Task assignment based on AI strengths

### 4. RT-Safety
- Audio thread never waits on UI/AI
- Lock-free communication via ring buffers
- Pre-allocated memory pools

---

## Common Development Tasks

### Adding a New Groove Genre
1. Add entry to `DAiW-Music-Brain/music_brain/data/genre_pocket_maps.json`
2. Add template in `music_brain/groove/templates.py`
3. Add to CLI choices in `music_brain/cli.py`

### Adding a Rule-Breaking Option
1. Add enum value in `music_brain/session/intent_schema.py`
2. Add entry in `RULE_BREAKING_EFFECTS` dict
3. Implement in `intent_processor.py`

### Adding a Penta-Core Engine
1. Create header in `include/penta/<subsystem>/`
2. Implement in `src_penta-core/<subsystem>/`
3. Add Python bindings in `bindings/`
4. Add tests in `tests_penta-core/`

### Adding an iDAW_Core Plugin
1. Create plugin directory in `iDAW_Core/plugins/<Name>/`
2. Add `include/<Name>Processor.h`, `src/<Name>Processor.cpp`
3. Add shader files in `shaders/`
4. Register in CMakeLists.txt

---

## Vault (Knowledge Base)

Obsidian-compatible markdown files in `vault/`:
```
vault/
├── Production_Guides/     # Compression, EQ, Dynamics guides
├── Songwriting_Guides/    # Intent schema, rule-breaking guides
├── Songs/                 # Song-specific project files
└── Templates/             # Task boards
```

Uses `[[wiki links]]` for cross-referencing.

---

## Troubleshooting

### Python Import Errors
```bash
pip install -e .
python --version  # Requires 3.9+
```

### C++ Build Failures
```bash
# Check CMake version
cmake --version  # Requires 3.22+

# Check compiler
g++ --version    # Requires C++17 support
```

### Audio Thread Issues
- Verify no allocations in `processBlock()`
- Check `isAudioThread()` assertions
- Use `assertNotAudioThread()` before blocking operations

### Test Failures
```bash
pytest -v --tb=long  # Verbose output with full tracebacks
```

---

## Data Flow

```
User Intent → Intent Schema → Intent Processor → Musical Elements
                                               ├── GeneratedProgression
                                               ├── GeneratedGroove
                                               └── GeneratedArrangement

Text Prompt → PythonBridge → Ring Buffer → Audio Engine
(Side B)                                    (Side A)

AI Proposal → Voting → Approved → Task Assignment → Implementation
```

---

## Meta Principle

> "The audience doesn't hear 'borrowed from Dorian.' They hear 'that part made me cry.'"

Technical implementation serves emotional expression. The tool educates and empowers - it doesn't just generate.
