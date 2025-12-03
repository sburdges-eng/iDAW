# iDAW Comprehensive To-Do List

> Generated: 2025-12-03 | Version: 0.2.0 (Alpha)

This document provides a complete roadmap of tasks for the iDAW project, organized by priority and component.

---

## 📊 Project Status Overview

| Component | Status | Completion |
|-----------|--------|------------|
| DAiW-Music-Brain (Python) | ✅ Functional | ~90% |
| Penta-Core (C++ RT Engines) | ✅ Functional | ~85% |
| iDAW_Core (JUCE Plugins) | 🔄 In Progress | ~40% |
| MCP Workstation | ✅ Functional | ~95% |
| Test Suite | ✅ Comprehensive | ~85% |
| Documentation | ✅ Extensive | ~90% |

---

## 🔴 HIGH PRIORITY - Core Functionality

### 1. JUCE Plugin DSP Implementations
**Status**: Only Pencil plugin fully implemented; 6 plugins need DSP work

| Plugin | Priority | Required DSP Work |
|--------|----------|-------------------|
| **Eraser** | HIGH | Spectral subtraction, noise gate, audio cleanup algorithms |
| **Press** | HIGH | Compressor/limiter, knee curves, attack/release envelopes |
| **Palette** | MEDIUM | Tonal coloring, EQ curves, saturation variations |
| **Smudge** | MEDIUM | Blending algorithms, crossfade, morphing |
| **Trace** | LOW | Envelope follower, pattern automation |
| **Parrot** | LOW | Sample playback engine, pitch shifting |

**Location**: `iDAW_Core/plugins/*/`

**Tasks**:
- [ ] Implement Eraser DSP (spectral subtraction, noise profiling)
- [ ] Implement Press DSP (compressor curves, gain reduction)
- [ ] Implement Palette DSP (multi-band EQ, saturation)
- [ ] Implement Smudge DSP (audio morphing, crossfade)
- [ ] Implement Trace DSP (envelope follower, automation)
- [ ] Implement Parrot DSP (sample engine, pitch detection)
- [ ] Add JUCE parameter automation for all plugins
- [ ] Create shader effects for each plugin's visual identity

---

### 2. FFT Library Integration for Production
**Status**: Penta-core uses simplified filterbank; production needs real FFT

**Tasks**:
- [ ] Choose FFT library: FFTW3 (Linux), vDSP (macOS), or header-only (KissFFT/PocketFFT)
- [ ] Integrate FFT into CMake build system
- [ ] Update OnsetDetector to use real FFT for spectral flux
- [ ] Implement proper Hann windowing with FFT
- [ ] Benchmark FFT performance (target: < 150μs per 512-sample block)
- [ ] Add fallback for systems without SIMD

---

### 3. Test Suite Gaps
**Status**: 519 tests passing, 25 failing (require optional deps), 5 errors

**Tasks**:
- [ ] Fix 5 bridge integration test errors
- [ ] Add mock implementations for optional API tests (openai, anthropic, google-generativeai)
- [ ] Add C++ unit tests for OSCHub pattern matching
- [ ] Add integration tests for JUCE plugin audio processing
- [ ] Add memory leak tests with Valgrind/AddressSanitizer
- [ ] Add RT-safety verification tests (no allocations in audio thread)

---

## 🟡 MEDIUM PRIORITY - Enhancement & Integration

### 4. Python/C++ Bridge Completion
**Status**: Framework exists, some functionality incomplete

**Tasks**:
- [ ] Complete Python bindings for all penta-core modules
- [ ] Add pybind11 wrappers for GrooveEngine
- [ ] Add pybind11 wrappers for HarmonyEngine
- [ ] Add pybind11 wrappers for DiagnosticsEngine
- [ ] Add pybind11 wrappers for OSCHub
- [ ] Create integration tests for Python bindings
- [ ] Document Python API with examples

---

### 5. Therapy/Chatbot Integration
**Status**: Infrastructure ready, NLP service pending

**Tasks**:
- [ ] Define chatbot service API specification
- [ ] Implement chatbot service client in BridgeClient
- [ ] Add async callback support for auto-tune RPC
- [ ] Create intent-to-chat translation layer
- [ ] Add conversation state management
- [ ] Test with local LLM (optional Ollama integration)

---

### 6. CI/CD Pipeline Improvements
**Status**: Basic CI working, could be enhanced

**Tasks**:
- [ ] Add C++ build to main CI workflow
- [ ] Add Valgrind memory testing stage
- [ ] Add performance regression testing
- [ ] Add code coverage reporting (lcov for C++, coverage.py for Python)
- [ ] Add automated release builds for all platforms
- [ ] Add JUCE plugin validation (auval for macOS)

---

### 7. Penta-Core Optimization (Phase 3.5)
**Status**: Functional but not fully optimized

**Tasks**:
- [ ] Profile hot paths with Instruments (macOS) / perf (Linux)
- [ ] Implement SIMD kernels for chord pattern matching (AVX2)
- [ ] Implement SIMD kernels for RMS calculation
- [ ] Implement SIMD kernels for FFT preprocessing
- [ ] Implement SIMD kernels for autocorrelation
- [ ] Add scalar fallbacks for non-SIMD systems
- [ ] Verify < 100μs harmony latency @ 48kHz/512 samples
- [ ] Verify < 200μs groove latency @ 48kHz/512 samples

---

## 🟢 LOW PRIORITY - Polish & Future Features

### 8. Documentation & Tutorials
**Status**: Extensive but could be enhanced

**Tasks**:
- [ ] Generate C++ API documentation with Doxygen
- [ ] Create video tutorials for DAiW CLI
- [ ] Write migration guide from v0.1 to v0.2
- [ ] Add more intent schema examples (beyond Kelly song)
- [ ] Document PythonBridge usage with examples
- [ ] Create "Getting Started" guide for contributors

---

### 9. Desktop Application
**Status**: Streamlit UI exists, native wrapper incomplete

**Tasks**:
- [ ] Complete PyWebView wrapper for native desktop
- [ ] Add system tray integration (daiw_menubar.py)
- [ ] Create macOS .app bundle with PyInstaller
- [ ] Create Windows .exe installer
- [ ] Create Linux AppImage
- [ ] Add auto-update mechanism

---

### 10. DAW Integration Testing
**Status**: Logic Pro integration exists, needs expansion

**Tasks**:
- [ ] Test Logic Pro integration with real projects
- [ ] Add Ableton Live integration (via OSC)
- [ ] Add Reaper integration (via OSC)
- [ ] Add Pro Tools integration (via AAX format)
- [ ] Document DAW-specific setup instructions
- [ ] Create DAW template projects

---

### 11. Mobile/Web Expansion
**Status**: Streamlit web UI works, mobile not started

**Tasks**:
- [ ] Deploy Streamlit app to cloud (Streamlit Cloud / Railway)
- [ ] Create PWA wrapper for mobile access
- [ ] Evaluate React Native or Flutter for native mobile
- [ ] Create iOS Audio Unit version of plugins
- [ ] Create Android AAP version of plugins

---

## 🔵 FUTURE ENHANCEMENTS (Nice to Have)

### 12. ML Model Integration
**Status**: Not started, architecture supports it

**Tasks**:
- [ ] Evaluate real-time ML inference frameworks (ONNX Runtime, TensorFlow Lite)
- [ ] Design ML model interface for penta-core
- [ ] Implement chord prediction model
- [ ] Implement style transfer model for groove
- [ ] Add GPU acceleration option (CUDA/Metal)

---

### 13. Advanced Harmony Features
**Status**: Basic implementation complete

**Tasks**:
- [ ] Add jazz voicing generation
- [ ] Implement neo-Riemannian transformations
- [ ] Add counterpoint generation
- [ ] Implement tension/release analysis
- [ ] Add microtonal support (24-TET, just intonation)

---

### 14. Advanced Groove Features
**Status**: Basic implementation complete

**Tasks**:
- [ ] Add polyrhythm detection
- [ ] Implement groove DNA extraction (like The Pocket Queen)
- [ ] Add humanization presets by artist/style
- [ ] Implement live performance timing analysis
- [ ] Add drum replacement with timing preservation

---

### 15. Collaboration Features
**Status**: MCP multi-AI exists, user collaboration not started

**Tasks**:
- [ ] Design real-time collaboration protocol
- [ ] Implement session sharing via WebSocket
- [ ] Add version control for song intents
- [ ] Create collaborative editing UI
- [ ] Add comment/annotation system

---

## 📋 Task Summary by Component

### Python (DAiW-Music-Brain)
| Task | Priority | Status |
|------|----------|--------|
| Complete Python bindings | MEDIUM | Pending |
| Chatbot integration | MEDIUM | Pending |
| Desktop app polish | LOW | Pending |
| More intent examples | LOW | Pending |

### C++ (Penta-Core)
| Task | Priority | Status |
|------|----------|--------|
| FFT library integration | HIGH | Pending |
| SIMD optimization | MEDIUM | Pending |
| Memory testing | MEDIUM | Pending |
| Performance benchmarks | MEDIUM | Pending |

### C++ (iDAW_Core - JUCE)
| Task | Priority | Status |
|------|----------|--------|
| Eraser DSP | HIGH | Pending |
| Press DSP | HIGH | Pending |
| Palette DSP | MEDIUM | Pending |
| Smudge DSP | MEDIUM | Pending |
| Trace DSP | LOW | Pending |
| Parrot DSP | LOW | Pending |

### Testing
| Task | Priority | Status |
|------|----------|--------|
| Fix bridge test errors | HIGH | Pending |
| RT-safety verification | MEDIUM | Pending |
| Integration tests | MEDIUM | Pending |
| Coverage reporting | LOW | Pending |

### DevOps
| Task | Priority | Status |
|------|----------|--------|
| C++ CI build | MEDIUM | Pending |
| Memory testing CI | MEDIUM | Pending |
| Release automation | LOW | Pending |

---

## 🎯 Recommended Sprint Plan

### Sprint A: Plugin Foundation (Weeks 1-2)
1. Implement Eraser DSP
2. Implement Press DSP
3. Add JUCE parameter automation

### Sprint B: Performance (Weeks 3-4)
1. Integrate FFT library
2. Profile and identify hotspots
3. Implement SIMD optimizations

### Sprint C: Integration (Weeks 5-6)
1. Complete Python bindings
2. Fix test suite gaps
3. Add memory/RT-safety tests

### Sprint D: Polish (Weeks 7-8)
1. Remaining plugin DSP (Palette, Smudge)
2. Desktop app packaging
3. Documentation and tutorials

### Sprint E: Future (Weeks 9+)
1. ML model integration research
2. Collaboration features
3. Mobile/web expansion

---

## 📝 Quick Reference: File Locations

| Component | Primary Location |
|-----------|------------------|
| Python Music Brain | `DAiW-Music-Brain/music_brain/` |
| Python CLI | `DAiW-Music-Brain/music_brain/cli.py` |
| C++ Penta-Core | `src_penta-core/` |
| C++ Headers | `include/penta/` |
| JUCE Plugins | `iDAW_Core/plugins/` |
| Python Tests | `tests_music-brain/` |
| C++ Tests | `tests_penta-core/` |
| CI Workflows | `.github/workflows/` |
| Documentation | `docs_music-brain/`, `vault/` |

---

## ✅ Recently Completed (For Reference)

- ✅ All code-level TODOs resolved
- ✅ Harmony/Scale history tracking in HarmonyEngine
- ✅ Lock-free RTMessageQueue
- ✅ OSC Client/Server/Hub implementation
- ✅ OnsetDetector spectral flux
- ✅ TempoEstimator with confidence
- ✅ RhythmQuantizer with swing
- ✅ Kelly intent JSON example
- ✅ 37 CLI commands tested
- ✅ Windows TTS support
- ✅ AudioAnalyzer implementation

---

*"Interrogate Before Generate" - The tool shouldn't finish art for people. It should make them braver.*

*Last updated: 2025-12-03*
