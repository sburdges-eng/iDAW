# iDAW 18-Month Implementation Roadmap

> **Start Date:** December 2024
> **End Date:** May 2026
> **Philosophy:** "Interrogate Before Generate" - The tool shouldn't finish art for people. It should make them braver.

---

## Executive Summary

This document provides a comprehensive 18-month implementation plan for the iDAW project, organized by quarter with specific deliverables, tasks, and acceptance criteria.

| Quarter | Focus | Key Deliverables |
|---------|-------|------------------|
| Q1 2025 | Core Foundation | CLI complete, Penta-Core harmony/groove |
| Q2 2025 | Audio Engine | Audio analysis, JUCE plugins, MCP tools |
| Q3 2025 | Desktop & DAW | Desktop app, Logic/Ableton integration |
| Q4 2025 | Polish & Scale | Optimization, testing, documentation |
| H1 2026 | Future Features | ML integration, mobile/web, collaboration |

---

## Q1 2025: Core Foundation (Months 1-3)

### Month 1: CLI & Python Core Completion

#### Week 1-2: Phase 1 CLI Completion
- [ ] Complete CLI wrapper commands in `music_brain/cli/commands.py`
  - [ ] `daiw generate` - Harmony generation from intent
  - [ ] `daiw diagnose` - Chord progression diagnosis
  - [ ] `daiw reharm` - Reharmonization suggestions
  - [ ] `daiw intent new|process|validate|suggest` - Intent subcommands
  - [ ] `daiw teach` - Interactive teaching mode
- [ ] Move `data/harmony_generator.py` → `music_brain/harmony/harmony_generator.py`
- [ ] Move `data/groove_applicator.py` → `music_brain/groove/groove_applicator.py`
- [ ] Create comprehensive test suite `tests/test_cli.py`
- [ ] Achieve ≥80% test coverage for CLI commands
- [ ] Update `__init__.py` exports

**Acceptance Criteria:**
- All CLI commands functional and documented
- `daiw --help` shows all commands
- Test coverage ≥80%
- Examples run without errors

#### Week 3-4: Brain Server & OSC Foundation
- [ ] Implement `brain_server.py` - Standalone Python OSC server
  - [ ] Listen on UDP port 9000
  - [ ] Respond on UDP port 9001
  - [ ] Handle `/daiw/generate` requests
  - [ ] Return JSON-serializable results
- [ ] Create `generate_session()` stable API
- [ ] Test client for brain server (no C++ needed)
- [ ] Validate JSON response format
- [ ] Document OSC message protocol

**Acceptance Criteria:**
- Brain server starts without errors
- Test client can send/receive messages
- Response is valid JSON
- Latency < 100ms for simple requests

---

### Month 2: Penta-Core Harmony Module (Phase 3.2)

#### Week 1: Chord Analysis Implementation
- [ ] Implement full chord template database (30+ templates)
  - [ ] Triads: Major, Minor, Diminished, Augmented
  - [ ] 7th chords: Maj7, Min7, Dom7, Half-dim7, Dim7
  - [ ] Extensions: 9th, 11th, 13th chords
  - [ ] Suspended: Sus2, Sus4
  - [ ] Add6, Add9 variations
- [ ] Optimize pattern matching with SIMD
  - [ ] AVX2-optimized bit operations
  - [ ] Parallel template evaluation
  - [ ] Early exit for perfect matches
- [ ] Implement temporal smoothing
  - [ ] Exponential moving average
  - [ ] Confidence decay over time
  - [ ] Chord change detection threshold
- [ ] Unit tests for all chord types, inversions, ambiguous cases

**Performance Target:** < 50μs for all template matching

#### Week 2: Scale Detection & Voice Leading
- [ ] Implement Krumhansl-Schmuckler key detection algorithm
  - [ ] Major/Minor key profiles
  - [ ] Modal profiles (7 modes)
  - [ ] Correlation calculation
  - [ ] Pitch class histogram with decay
- [ ] Implement voice leading optimizer
  - [ ] Generate voicing candidates
  - [ ] Cost function (voice distance, parallel motion, crossing)
  - [ ] Branch and bound search
  - [ ] Caching for common progressions
- [ ] Integration testing with real MIDI
- [ ] Python bindings for HarmonyEngine

**Performance Target:** < 100μs total latency, > 90% chord detection accuracy

#### Week 3-4: Integration & Testing
- [ ] Test harmony engine with real MIDI files
- [ ] Benchmark performance on various hardware
- [ ] Document API with Doxygen
- [ ] Create Python wrapper tests
- [ ] Validate RT-safety (no allocations in audio path)

---

### Month 3: Penta-Core Groove Module (Phase 3.3)

#### Week 1: FFT Integration & Onset Detection
- [ ] Choose and integrate FFT library
  - [ ] FFTW3 (Linux), vDSP (macOS), or KissFFT/PocketFFT (header-only)
  - [ ] CMake integration
  - [ ] RT-safe buffer management
- [ ] Implement onset detector
  - [ ] Spectral flux calculation
  - [ ] Hann window function
  - [ ] Peak picking with adaptive threshold
  - [ ] Median filtering for noise rejection
- [ ] Implement tempo estimator
  - [ ] Inter-onset interval calculation
  - [ ] Autocorrelation of IOI sequence
  - [ ] Peak detection in autocorrelation
  - [ ] BPM calculation and smoothing

**Performance Target:** < 150μs per 512-sample block

#### Week 2: Rhythm Quantization
- [ ] Implement grid quantization
  - [ ] Sample-accurate grid calculation
  - [ ] Multi-resolution grids (whole to 32nd notes)
  - [ ] Triplet support
  - [ ] Strength parameter (0-100%)
- [ ] Implement swing timing
  - [ ] Swing amount calculation
  - [ ] 8th note and 16th note swing
  - [ ] Non-uniform swing patterns
- [ ] Time signature detection
  - [ ] Beat strength analysis
  - [ ] Common time signatures (4/4, 3/4, 6/8, etc.)
  - [ ] Confidence scoring

**Performance Target:** < 200μs total latency, < 2 BPM tempo error

#### Week 3-4: Python Bindings & Testing
- [ ] Complete pybind11 wrappers for GrooveEngine
- [ ] Integration tests for Python bindings
- [ ] Benchmark against music_brain Python implementations
- [ ] Document Python API with examples
- [ ] Verify real-time quantization works

---

## Q2 2025: Audio Engine & Tools (Months 4-6)

### Month 4: Audio Analysis & MCP Tools

#### Week 1-2: Audio Analysis Module
- [ ] Expand `music_brain/audio/analyzer.py` with full AudioAnalyzer class
- [ ] Implement `chord_detection.py` with ChordDetector
  - [ ] Detect chords from audio
  - [ ] Detect progression from file
  - [ ] Confidence scoring
- [ ] Implement `frequency.py` with FrequencyAnalyzer
  - [ ] FFT analysis
  - [ ] Pitch detection
  - [ ] Harmonic content analysis
- [ ] Integrate with existing audio_cataloger patterns
- [ ] Add CLI command: `daiw analyze-audio <file>`

**Dependencies:** librosa>=0.10.0, soundfile>=0.12.0, numpy>=1.24.0, scipy>=1.10.0

#### Week 3-4: MCP Tool Coverage Expansion (3 → 22 tools)
- [ ] Create `tools/intent.py` (4 tools)
  - [ ] `create_intent` - Create song intent template
  - [ ] `process_intent` - Process intent → music
  - [ ] `validate_intent` - Validate intent schema
  - [ ] `suggest_rulebreaks` - Suggest emotional rule-breaks
- [ ] Expand `tools/harmony.py` (6 tools total)
  - [ ] `generate_harmony` - Generate harmony from intent
  - [ ] `diagnose_chords` - Diagnose harmonic issues
  - [ ] `suggest_reharmonization` - Suggest chord substitutions
  - [ ] `find_key` - Detect key from progression
  - [ ] `voice_leading` - Optimize voice leading
- [ ] Expand `tools/groove.py` (5 tools total)
  - [ ] `analyze_pocket` - Analyze timing pocket
  - [ ] `humanize_midi` - Add human feel
  - [ ] `quantize_smart` - Smart quantization
- [ ] Create `tools/audio_analysis.py` (4 tools)
  - [ ] `detect_bpm` - Detect tempo from audio
  - [ ] `detect_key` - Detect key from audio
  - [ ] `analyze_audio_feel` - Analyze groove feel from audio
  - [ ] `extract_chords` - Extract chords from audio
- [ ] Create `tools/teaching.py` (3 tools)
  - [ ] `explain_rulebreak` - Explain rule-breaking technique
  - [ ] `get_progression_info` - Get progression details
  - [ ] `emotion_to_music` - Map emotion to musical parameters

---

### Month 5: JUCE Plugin DSP Implementation

#### Week 1-2: High Priority Plugins
- [ ] **Eraser Plugin DSP**
  - [ ] Spectral subtraction algorithm
  - [ ] Noise gate implementation
  - [ ] Audio cleanup algorithms
  - [ ] Noise profiling system
- [ ] **Press Plugin DSP**
  - [ ] Compressor/limiter implementation
  - [ ] Knee curves (soft/hard)
  - [ ] Attack/release envelopes
  - [ ] Gain reduction metering

#### Week 3-4: Medium Priority Plugins
- [ ] **Palette Plugin DSP**
  - [ ] Tonal coloring algorithms
  - [ ] Multi-band EQ curves
  - [ ] Saturation variations
  - [ ] Color presets
- [ ] **Smudge Plugin DSP**
  - [ ] Audio blending algorithms
  - [ ] Crossfade implementation
  - [ ] Morphing between audio sources
- [ ] Add JUCE parameter automation for all plugins
- [ ] Create shader effects for visual identity

---

### Month 6: Diagnostics, OSC & Optimization (Phase 3.4-3.5)

#### Week 1: Performance Monitoring
- [ ] Implement high-resolution timing
  - [ ] Platform-specific timers (RDTSC, mach_absolute_time, QPC)
  - [ ] Microsecond precision
  - [ ] Minimal overhead (< 1μs)
- [ ] Implement CPU usage calculation
  - [ ] Thread CPU time tracking
  - [ ] Percentage calculation relative to buffer duration
  - [ ] Peak and average tracking
- [ ] Implement audio analysis
  - [ ] RMS calculation (SIMD-optimized)
  - [ ] Peak hold with decay
  - [ ] True peak detection
  - [ ] Dynamic range estimation

#### Week 2: OSC Communication
- [ ] Implement OSC message encoding/decoding with oscpack
- [ ] RT-safe message construction
- [ ] Platform sockets (UDP, non-blocking I/O)
- [ ] Message routing with pattern matching
- [ ] Priority queues for message handling

**Performance Target:** < 50μs messaging latency

#### Week 3-4: SIMD Optimization
- [ ] Profile hot paths with Instruments (macOS) / perf (Linux)
- [ ] Implement SIMD kernels for:
  - [ ] Chord pattern matching (AVX2)
  - [ ] RMS calculation (AVX2)
  - [ ] FFT preprocessing (AVX2)
  - [ ] Autocorrelation (AVX2)
- [ ] Add scalar fallbacks for non-SIMD systems
- [ ] Verify performance targets met

---

## Q3 2025: Desktop & DAW Integration (Months 7-9)

### Month 7: Desktop Application (Phase 3 - Part 1)

#### Week 1-2: Framework Setup
- [ ] Choose framework: Electron, PyQt, or Streamlit + PyWebView
- [ ] Set up project structure
- [ ] Implement basic window management
- [ ] Create application skeleton
- [ ] Dark theme implementation

#### Week 3-4: Core UI Development
- [ ] Implement Ableton-style interface layout
- [ ] Visual arrangement editor
  - [ ] Timeline view
  - [ ] Section blocks (verse/chorus/bridge)
  - [ ] Drag-and-drop reordering
- [ ] Intent input panel
  - [ ] Emotional intent controls
  - [ ] Rule-breaking toggles
  - [ ] Genre selection

---

### Month 8: Desktop Application (Phase 3 - Part 2)

#### Week 1-2: MIDI Preview & Playback
- [ ] MIDI preview system
  - [ ] Internal MIDI playback
  - [ ] Waveform visualization
  - [ ] Transport controls (play/pause/stop)
- [ ] Project save/load
  - [ ] Save intent + generated content
  - [ ] Project file format (.daiw)
  - [ ] Recent projects list

#### Week 3-4: Integration & Export
- [ ] Connect to Phase 1 & 2 engines
- [ ] Real-time audio playback (if applicable)
- [ ] Export to DAW
  - [ ] MIDI export
  - [ ] Logic Pro project export
  - [ ] Ableton Live Set export
  - [ ] Generic MIDI + metadata
- [ ] User testing & feedback collection

---

### Month 9: DAW Integration (Phase 4 - Part 1)

#### Week 1-2: JUCE Plugin Skeleton
- [ ] Verify JUCE installed and Projucer works
- [ ] Build minimal plugin shell
  - [ ] Audio passthrough (no processing)
  - [ ] Placeholder UI elements
  - [ ] "Generate" button (test pattern)
- [ ] Build as AU and VST3
- [ ] AU validation passes
- [ ] Test in Logic Pro

#### Week 3-4: OSC Bridge Wiring
- [ ] Wire OSC sender/receiver in JUCE
- [ ] Connect C++ plugin to Python brain
- [ ] Implement complete flow:
  1. User types text, adjusts knobs
  2. User clicks "Generate"
  3. Plugin sends OSC to Python brain
  4. Python processes, returns note data
  5. Plugin parses JSON into MidiMessage
  6. Plugin schedules in MidiBuffer
  7. Logic receives MIDI, plays instruments
- [ ] End-to-end latency < 500ms

---

## Q4 2025: Polish & Scale (Months 10-12)

### Month 10: DAW Integration (Phase 4 - Part 2)

#### Week 1-2: Logic Pro X Plugin Completion
- [ ] Complete AU plugin development
- [ ] Direct integration with Logic
- [ ] Project templates for Logic
- [ ] Documentation for Logic users

#### Week 3-4: Ableton Live Integration
- [ ] Max for Live device
- [ ] Live integration via OSC
- [ ] Push controller support (if applicable)
- [ ] Live Set templates

---

### Month 11: Testing & Quality Assurance

#### Week 1-2: Comprehensive Testing
- [ ] Fix all test suite gaps
  - [ ] Bridge integration test errors
  - [ ] Mock implementations for optional API tests
  - [ ] C++ unit tests for OSCHub pattern matching
- [ ] Memory leak tests with Valgrind/AddressSanitizer
- [ ] RT-safety verification (no allocations in audio thread)
- [ ] 24-hour stress test (no crashes)

#### Week 3-4: CI/CD Pipeline Improvements
- [ ] Add C++ build to main CI workflow
- [ ] Add Valgrind memory testing stage
- [ ] Add performance regression testing
- [ ] Code coverage reporting (lcov for C++, coverage.py for Python)
- [ ] Automated release builds for all platforms
- [ ] JUCE plugin validation (auval for macOS)

---

### Month 12: Documentation & Packaging

#### Week 1-2: Documentation
- [ ] Generate C++ API documentation with Doxygen
- [ ] Create video tutorials for DAiW CLI
- [ ] Write migration guide from v0.1 to v0.2
- [ ] Add more intent schema examples
- [ ] Document PythonBridge usage
- [ ] Create "Getting Started" guide for contributors

#### Week 3-4: Desktop Packaging
- [ ] Complete PyWebView wrapper for native desktop
- [ ] System tray integration
- [ ] macOS .app bundle with PyInstaller
- [ ] Windows .exe installer
- [ ] Linux AppImage
- [ ] Auto-update mechanism

---

## H1 2026: Future Enhancements (Months 13-18)

### Month 13-14: Additional DAW Support

- [ ] FL Studio support (VST3)
- [ ] Pro Tools support (AAX format)
- [ ] Reaper integration (via OSC)
- [ ] Create DAW-specific setup documentation
- [ ] Create DAW template projects

### Month 15-16: ML Model Integration

- [ ] Evaluate real-time ML inference frameworks
  - [ ] ONNX Runtime
  - [ ] TensorFlow Lite
  - [ ] CoreML (macOS/iOS)
- [ ] Design ML model interface for penta-core
- [ ] Implement chord prediction model
- [ ] Implement style transfer model for groove
- [ ] GPU acceleration option (CUDA/Metal)

### Month 17-18: Mobile, Web & Collaboration

#### Mobile/Web Expansion
- [ ] Deploy Streamlit app to cloud (Streamlit Cloud / Railway)
- [ ] Create PWA wrapper for mobile access
- [ ] Evaluate React Native or Flutter for native mobile
- [ ] iOS Audio Unit version of plugins
- [ ] Android AAP version of plugins

#### Collaboration Features
- [ ] Design real-time collaboration protocol
- [ ] Implement session sharing via WebSocket
- [ ] Version control for song intents
- [ ] Collaborative editing UI
- [ ] Comment/annotation system

---

## Advanced Features (Ongoing/Future)

### Advanced Harmony
- [ ] Jazz voicing generation
- [ ] Neo-Riemannian transformations
- [ ] Counterpoint generation
- [ ] Tension/release analysis
- [ ] Microtonal support (24-TET, just intonation)

### Advanced Groove
- [ ] Polyrhythm detection
- [ ] Groove DNA extraction
- [ ] Humanization presets by artist/style
- [ ] Live performance timing analysis
- [ ] Drum replacement with timing preservation

### Lower Priority Plugins
- [ ] **Trace Plugin DSP** - Envelope follower, pattern automation
- [ ] **Parrot Plugin DSP** - Sample playback engine, pitch shifting

---

## Success Metrics

### Performance Targets
| Module | Target Latency | CPU Usage |
|--------|---------------|-----------|
| Harmony Engine | < 100μs @ 48kHz/512 | < 2% |
| Groove Engine | < 200μs @ 48kHz/512 | < 2% |
| OSC Messaging | < 50μs | < 1% |
| Total Plugin | < 350μs | < 5% |

### Quality Targets
| Metric | Target |
|--------|--------|
| Chord Detection Accuracy | > 90% |
| Tempo Tracking Error | < 2 BPM |
| Scale Detection Accuracy | > 85% |
| Test Coverage (Python) | > 80% |
| Test Coverage (C++) | > 70% |

### Robustness Targets
- All unit tests passing
- No memory leaks (Valgrind clean)
- No crashes in 24-hour stress test
- Cross-platform validated (macOS, Linux, Windows)
- Graceful degradation under load

---

## Quick Reference: Key File Locations

| Component | Location |
|-----------|----------|
| Python Music Brain | `DAiW-Music-Brain/music_brain/` |
| Python CLI | `DAiW-Music-Brain/music_brain/cli.py` |
| C++ Penta-Core | `src_penta-core/` |
| C++ Headers | `include/penta/` |
| JUCE Plugins | `iDAW_Core/plugins/` |
| Python Tests | `tests_music-brain/` |
| C++ Tests | `tests_penta-core/` |
| CI Workflows | `.github/workflows/` |
| MCP Workstation | `mcp_workstation/` |
| MCP TODO Server | `mcp_todo/` |

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2024-12 | 1.0.0 | Initial 18-month roadmap |

---

*"The audience doesn't hear 'borrowed from Dorian.' They hear 'that part made me cry.'"*
