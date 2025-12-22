# 🗺️ iDAW/miDiKompanion - Quick Navigation Map

> One-page reference for finding anything in the project

Last Updated: 2025-12-22

---

## 🎯 "I want to work on..." → "Go here"

| I want to... | Component | Files to Check |
|--------------|-----------|----------------|
| **Music theory logic** | Music Brain | `music_brain/structure/chord.py`<br>`music_brain/structure/progression.py` |
| **Emotion → music mapping** | Music Brain | `music_brain/data/emotional_mapping.py`<br>`music_brain/session/intent_schema.py` |
| **MIDI file generation** | Music Brain | `music_brain/harmony/harmony_generator.py`<br>`music_brain/utils/midi_io.py` |
| **Groove/timing feel** | Music Brain | `music_brain/groove/extractor.py`<br>`music_brain/groove/templates.py` |
| **Command-line interface** | Music Brain | `music_brain/cli.py` |
| **Real-time audio processing** | Penta-Core | `src_penta-core/audio/` |
| **C++ performance code** | Penta-Core | `src_penta-core/groove/groove_engine.cpp` |
| **DAW application** | iDAW Core | `iDAW_Core/src/` |
| **UI/interface** | iDAW Core | `iDAW_Core/src/ui/` |
| **Plugin hosting** | iDAW Core | `iDAW_Core/src/plugins/` |
| **Claude/AI integration** | MCP Servers | `mcp_todo/`, `mcp_workstation/` |
| **Documentation** | Vault | `vault/Songwriting_Guides/`<br>`vault/Theory_Reference/` |
| **Production guides** | Vault | `vault/Production_Workflows/` |
| **Tests** | Tests | `tests/`, `tests_music-brain/`, `tests_penta-core/` |

---

## 📂 Directory Structure (Top Level)

```
iDAW/
├── 🧠 music_brain/          # Python music intelligence toolkit
├── ⚙️  src_penta-core/       # C++ real-time audio engine
├── 🎛️  iDAW_Core/            # JUCE-based DAW application
├── 🤖 mcp_todo/             # MCP server for task management
├── 🤖 mcp_workstation/      # MCP server for workstation tools
├── 📚 vault/                # Knowledge base (Obsidian)
├── 🧪 tests/                # Python tests
├── 📖 docs/                 # General documentation
├── 🎼 examples/             # Example MIDI files and scripts
└── 🔧 tools/                # Utility scripts
```

---

## 🧠 Music Brain Deep Dive

```
music_brain/
├── __init__.py
├── cli.py                   # 👈 START: Command-line interface
│
├── 🎵 structure/            # Harmony & chord analysis
│   ├── chord.py             # Chord parsing, intervals
│   ├── progression.py       # Roman numeral analysis, diagnostics
│   └── sections.py          # Song structure detection
│
├── 🎹 groove/               # Timing & feel
│   ├── extractor.py         # Extract groove from MIDI
│   ├── applicator.py        # Apply groove to MIDI
│   ├── templates.py         # Genre templates (funk, jazz, etc.)
│   └── groove_engine.py     # Humanization logic
│
├── 🧘 session/              # Intent & teaching
│   ├── intent_schema.py     # 3-phase intent system
│   ├── intent_processor.py  # Process intent → music
│   ├── interrogator.py      # Question system
│   └── teaching.py          # Rule-breaking lessons
│
├── 🎼 harmony/              # Chord voicing & generation
│   └── harmony_generator.py # Generate MIDI from intent
│
├── 🎧 audio/                # Audio analysis (Phase 2)
│   ├── analyzer.py          # BPM, key detection
│   ├── feel.py              # Timing feel analysis
│   └── frequency.py         # FFT, spectral analysis
│
├── 🛠️ utils/                # Utilities
│   ├── midi_io.py           # Read/write MIDI files
│   ├── instruments.py       # GM instrument mappings
│   └── ppq.py               # Timing utilities
│
└── 📊 data/                 # JSON/YAML data files
    ├── chord_progressions.json
    ├── emotional_mapping.py
    ├── genre_pocket_maps.json
    ├── scales_database.json
    └── song_intent_schema.yaml
```

---

## ⚙️ Penta-Core Deep Dive

```
src_penta-core/
├── CMakeLists.txt           # 👈 BUILD: C++ build config
│
├── 🎚️ audio/                # Real-time audio processing
│   ├── audio_engine.cpp     # Core audio engine
│   ├── buffer.cpp           # Audio buffer management
│   └── dsp/                 # DSP algorithms
│
├── 🎹 midi/                 # MIDI processing
│   ├── midi_processor.cpp   # Real-time MIDI handling
│   └── midi_buffer.cpp      # MIDI event buffering
│
├── 🎵 groove/               # C++ groove engine
│   └── groove_engine.cpp    # Performance-critical groove
│
├── 🔌 effects/              # Audio effects
│   └── guitar_fx.cpp        # Guitar effects chain
│
└── 🧪 tests/                # C++ unit tests
    └── test_*.cpp
```

---

## 🎛️ iDAW Core Deep Dive

```
iDAW_Core/
├── CMakeLists.txt           # 👈 BUILD: JUCE project config
│
├── src/
│   ├── 🖥️ ui/               # User interface
│   │   ├── MainWindow.cpp
│   │   ├── TrackView.cpp
│   │   └── MixerView.cpp
│   │
│   ├── 🎚️ audio/            # Audio engine integration
│   │   ├── AudioEngine.cpp
│   │   └── AudioGraph.cpp
│   │
│   ├── 🎵 tracks/           # Track management
│   │   ├── AudioTrack.cpp
│   │   └── MIDITrack.cpp
│   │
│   ├── 🔌 plugins/          # VST/AU plugin hosting
│   │   └── PluginHost.cpp
│   │
│   └── 💾 session/          # Project save/load
│       └── SessionManager.cpp
│
└── include/                 # Header files
    └── *.h
```

---

## 📚 Vault Deep Dive

```
vault/
├── 📖 Songwriting_Guides/   # Lyric writing, structure, etc.
│   ├── Hook Writing Guide.md
│   ├── Song Structure Guide.md
│   └── Lyric Writing Guide.md
│
├── 🎼 Theory_Reference/     # Music theory deep dives
│   ├── Chord Progressions for Songwriters.md
│   ├── Music Theory Vocabulary.md
│   └── Scales and Modes.md
│
├── 🎛️ Production_Workflows/ # Production techniques
│   ├── Mixing Workflow Checklist.md
│   ├── Mastering Checklist.md
│   └── [Genre] Production Guide.md (many)
│
└── 📋 Templates/            # Obsidian templates
    ├── Song Template.md
    ├── Session Notes Template.md
    └── Mix Notes Template.md
```

---

## 🔍 Finding Specific Features

### Chord Analysis
- **Parsing:** `music_brain/structure/chord.py` → `Chord.from_string()`
- **Progressions:** `music_brain/structure/progression.py` → `diagnose_progression()`
- **Roman Numerals:** `music_brain/structure/progression.py` → `to_roman_numerals()`

### Groove/Feel
- **Extract:** `music_brain/groove/extractor.py` → `extract_groove()`
- **Apply:** `music_brain/groove/applicator.py` → `apply_groove()`
- **Templates:** `music_brain/groove/templates.py` → `GENRE_TEMPLATES`

### Intent System
- **Schema:** `music_brain/session/intent_schema.py` → `CompleteSongIntent`
- **Processing:** `music_brain/session/intent_processor.py` → `process_intent()`
- **Questions:** `music_brain/session/interrogator.py` → `SongInterrogator`

### MIDI Generation
- **Harmony:** `music_brain/harmony/harmony_generator.py` → `HarmonyGenerator`
- **I/O:** `music_brain/utils/midi_io.py` → `save_midi()`, `load_midi()`

### Audio Analysis
- **BPM:** `music_brain/audio/analyzer.py` → `detect_bpm()`
- **Key:** `music_brain/audio/analyzer.py` → `detect_key()`
- **Feel:** `music_brain/audio/feel.py` → `analyze_feel()`

---

## 🧪 Testing

### Where Are Tests?
```
tests/                       # Music Brain Python tests
tests_music-brain/          # Music Brain specific tests
tests_penta-core/           # Penta-Core C++ tests
iDAW_Core/tests/            # iDAW Core tests
```

### Run Tests
```bash
# All Python tests
pytest tests/ -v

# Specific test file
pytest tests/test_chord.py -v

# Specific test
pytest tests/test_chord.py::test_parse_augmented -v

# With coverage
pytest tests/ --cov=music_brain --cov-report=html

# C++ tests (Penta-Core)
cd src_penta-core && ./run_tests.sh

# C++ tests (iDAW Core)
cd iDAW_Core/build && ctest
```

---

## 📖 Documentation Files

### Getting Started
- `START_HERE.txt` - Project overview, what to read first
- `README.md` - General info (currently shows JUCE framework)
- `MAIN_DOCUMENTATION.md` - Architecture and features

### Development
- `CURSOR_WORKFLOW_GUIDE.md` - **How to work without getting lost** ⭐
- `CLAUDE_AGENT_GUIDE.md` - AI assistant reference
- `PROJECT_ROADMAP.md` - Development timeline
- `COMPREHENSIVE_TODO_IDAW.md` - Task list for iDAW Core
- `DEVELOPMENT_ROADMAP_music-brain.md` - Task list for Music Brain

### Build & Deploy
- `BUILD.md` - Build instructions
- `INSTALL.md` - Installation guide
- `BUILD_COMPLETE.md` - Build status
- `TROUBLESHOOTING.md` - Common issues

### Reference
- `DAiW_Cheat_Sheet.md` - Emotion → music quick lookup
- `AUTOMATION_GUIDE.md` - Automation features
- `PERFORMANCE_SUMMARY.md` - Performance optimizations

### User Guides
- `vault/` directory - Comprehensive guides and templates

---

## 🚀 Common Commands

### Music Brain CLI
```bash
# Activate environment
source venv/bin/activate

# Diagnose chords
daiw diagnose "F-C-Am-Dm"

# Generate MIDI
daiw generate --key F --mode major --pattern "I-V-vi-IV" -o output.mid

# Apply groove
daiw apply --genre funk input.mid output.mid

# Get help
daiw --help
daiw diagnose --help
```

### Development
```bash
# Install dependencies
pip install -e .

# Run tests
pytest tests/ -v

# Run linter
pylint music_brain/

# Run type checker
mypy music_brain/

# Build C++ (Penta-Core)
cd src_penta-core && cmake . && make

# Build C++ (iDAW Core)
cd iDAW_Core && cmake -B build && cmake --build build
```

### Git Workflow
```bash
# Start new feature
git checkout -b feat/my-feature

# Check status
git status

# Commit
git add .
git commit -m "feat: description"

# Push
git push origin feat/my-feature
```

---

## 🆘 "Where is...?"

### "Where is the chord parser?"
→ `music_brain/structure/chord.py` → `Chord.from_string()`

### "Where are the emotion presets?"
→ `music_brain/data/emotional_mapping.py` → `EMOTIONAL_PRESETS`

### "Where is the CLI defined?"
→ `music_brain/cli.py` → `@click.command()` decorators

### "Where are the tests?"
→ `tests/` and `tests_music-brain/`

### "Where is the groove extraction?"
→ `music_brain/groove/extractor.py` → `extract_groove()`

### "Where is the C++ audio engine?"
→ `src_penta-core/audio/audio_engine.cpp`

### "Where is the DAW UI?"
→ `iDAW_Core/src/ui/MainWindow.cpp`

### "Where are the genre templates?"
→ `music_brain/groove/templates.py` → `GENRE_TEMPLATES`

### "Where is the intent schema?"
→ `music_brain/session/intent_schema.py` → `CompleteSongIntent`

### "Where is the teaching system?"
→ `music_brain/session/teaching.py` → `RuleBreakingTeacher`

---

## 🎯 Quick Workflows

### Add a New Chord Type
1. Edit `music_brain/structure/chord.py`
2. Add to `Chord.from_string()` parsing logic
3. Add test in `tests/test_chord.py`
4. Run `pytest tests/test_chord.py -v`
5. Commit: `git commit -m "feat(chord): add [type] chord parsing"`

### Add a New Groove Template
1. Edit `music_brain/groove/templates.py`
2. Add to `GENRE_TEMPLATES` dictionary
3. Add test in `tests/test_groove.py`
4. Run `pytest tests/test_groove.py -v`
5. Commit: `git commit -m "feat(groove): add [genre] template"`

### Add a New CLI Command
1. Edit `music_brain/cli.py`
2. Add `@click.command()` function
3. Add to `cli.add_command()` at bottom
4. Test: `daiw [command] --help`
5. Add test in `tests/test_cli_commands.py`
6. Commit: `git commit -m "feat(cli): add [command] command"`

---

## 📞 Help Resources

### In This Repo
- `CURSOR_WORKFLOW_GUIDE.md` - Workflow guide
- `TROUBLESHOOTING.md` - Common issues
- `STUCK_LOG.md` - Document when stuck (create if needed)

### External
- GitHub Issues: `https://github.com/sburdges-eng/iDAW/issues`
- Music Brain: `https://github.com/sburdges-eng/DAiW-Music-Brain`
- JUCE Framework: `https://juce.com/learn/documentation`

---

## 🎓 Learning Path

### Day 1: Overview
1. Read `START_HERE.txt`
2. Read `MAIN_DOCUMENTATION.md`
3. Run `daiw --help` and try commands
4. Explore `vault/` docs

### Week 1: Music Brain
1. Study `music_brain/session/intent_schema.py`
2. Study `music_brain/structure/chord.py`
3. Trace `daiw diagnose` command through code
4. Make a small change and test

### Week 2: Choose Your Focus
- **Python Path:** Deep dive into music_brain
- **C++ Path:** Explore src_penta-core
- **DAW Path:** Study iDAW_Core
- **Docs Path:** Improve vault/ guides

---

**Navigation Tips:**
- Use Cursor's `Cmd+P` to quick-open files
- Use `Cmd+Shift+F` to search across files
- Use `@filename` in Cursor Chat to reference files
- Bookmark this file in Cursor for quick access

Happy coding! 🎵
