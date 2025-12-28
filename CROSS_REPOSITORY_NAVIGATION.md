# Cross-Repository Navigation Guide

**Quick reference for navigating the 12-repository ecosystem**

Last Updated: 2025-12-28

---

## 🎯 "I want to..." Quick Links

| I want to... | Go here | Repository |
|--------------|---------|------------|
| **Start a new project** | [iDAW README](README.md) | iDAW (THIS REPO) |
| **Learn the intent schema** | [Song Intent Schema](vault/Songwriting_Guides/song_intent_schema.md) | iDAW |
| **Use Python API** | [Music Brain README](README_music-brain.md) | iDAW |
| **Build C++ engine** | [Penta-Core BUILD](BUILD.md) | iDAW |
| **Build Kelly desktop app** | [Kelly Project](https://github.com/sburdges-eng/kelly-project) | kelly-project |
| **Understand all repos** | [Repository Compilation](REPOSITORY_COMPILATION.md) | iDAW (THIS REPO) |
| **Build everything** | [Multi-Build Guide](MULTI_BUILD.md) | iDAW or miDiKompanion |
| **Learn music theory** | [Theory Reference](vault/Theory_Reference/) | iDAW |
| **Production guides** | [Production Workflows](vault/Production_Workflows/) | iDAW |
| **Rule-breaking reference** | [Rule Breaking Guide](vault/Songwriting_Guides/rule_breaking_practical.md) | iDAW |

---

## 📦 Repository Purposes

### Core Repositories (Use These)

#### 1. [iDAW](https://github.com/sburdges-eng/iDAW) ⭐ **PRIMARY**
**Use for**: Everything! Main integrated repository
- Python music intelligence (`music_brain/`)
- C++ real-time engine (`src_penta-core/`)
- Knowledge base (`vault/`)
- Examples and tools
- Complete documentation

#### 2. [DAiW-Music-Brain](https://github.com/sburdges-eng/DAiW-Music-Brain)
**Use for**: Reference Python implementation (mostly integrated into iDAW)
- Original intent schema development
- Standalone Python package
- Legacy examples

**Migration**: Most features now in `iDAW/music_brain/`

#### 3. [penta-core](https://github.com/sburdges-eng/penta-core)
**Use for**: Reference C++ implementation (mostly integrated into iDAW)
- Original C++ engine development
- Performance optimization research
- Real-time audio docs

**Migration**: Most code now in `iDAW/src_penta-core/`

#### 4. [kelly-project](https://github.com/sburdges-eng/kelly-project)
**Use for**: Desktop application development
- Tauri + React desktop app
- Music Brain API integration
- Therapeutic composition UI

**Status**: Standalone, planned integration into `iDAW/apps/kelly/`

---

### Support Repositories

#### 5. [miDiKompanion](https://github.com/sburdges-eng/miDiKompanion)
**Use for**: Build system and Git automation
- Multi-repo build scripts
- Git batch update tools
- Build profile management

**Migration**: Build scripts being consolidated into iDAW

#### 6. [iDAWi](https://github.com/sburdges-eng/iDAWi)
**Use for**: Integration reference
- PR automation scripts
- Repository management tools

**Status**: Reference implementation for iDAW features

---

### Kelly Variants (Consolidation Needed)

#### 7. [kelly-music-brain-clean](https://github.com/sburdges-eng/kelly-music-brain-clean)
**Use for**: Clean Kelly implementation reference
- Refined music brain code
- Stable API implementation

**Plan**: Merge into iDAW

#### 8. [Kelly](https://github.com/sburdges-eng/Kelly)
**Use for**: Alternative Kelly implementation

**Plan**: Consolidate with kelly-project

---

### Reference/Archive Repositories

#### 9. [Pentagon-core-100-things](https://github.com/sburdges-eng/Pentagon-core-100-things)
**Use for**: Swift/iOS implementation reference
- iOS/macOS native code
- DAW development documentation
- 100-topic guides

**Status**: Reference for future native implementations

#### 10. [1DAW1](https://github.com/sburdges-eng/1DAW1)
**Use for**: Alternative DAW implementation reference

**Status**: Reference/experimental

#### 11. [lariat-bible](https://github.com/sburdges-eng/lariat-bible)
**Use for**: Order of operations framework

**Status**: Reference for workflow organization

#### 12. [GitHub-all-repo](https://github.com/sburdges-eng/GitHub-all-repo)
**Use for**: Previous compilation attempt reference

**Status**: Archive

---

## 🔄 Migration Quick Reference

### From DAiW-Music-Brain to iDAW

```python
# Old import (DAiW-Music-Brain standalone)
from daiw_music_brain.session import process_intent

# New import (iDAW integrated)
from music_brain.session.intent_processor import process_intent
```

### From penta-core to iDAW

```python
# Old import (penta-core standalone)
from penta_core import PentaCore

# New import (iDAW integrated)
# Build from iDAW/src_penta-core/
from penta_core import PentaCore  # Same import, different source
```

### From miDiKompanion build to iDAW

```bash
# Old (miDiKompanion)
./build_all.sh --music-brain --penta-core

# New (iDAW)
pip install -e .  # Python
cd src_penta-core && mkdir build && cmake .. && cmake --build .  # C++
```

---

## 📚 Documentation Map

### Getting Started
- [iDAW README](README.md) - Start here
- [REPOSITORY_COMPILATION.md](REPOSITORY_COMPILATION.md) - Complete analysis
- [PROJECT_NAVIGATION.md](PROJECT_NAVIGATION.md) - File structure guide
- [WORKFLOW.md](WORKFLOW.md) - Development workflow

### Building & Installation
- [BUILD.md](BUILD.md) - C++ build instructions
- [MULTI_BUILD.md](MULTI_BUILD.md) - Multi-component builds
- [INSTALL.md](INSTALL.md) - Installation guide

### Development
- [CURSOR_WORKFLOW_GUIDE.md](CURSOR_WORKFLOW_GUIDE.md) - Cursor development workflow
- [DEVELOPMENT_ROADMAP_music-brain.md](DEVELOPMENT_ROADMAP_music-brain.md) - Roadmap
- [WORKFLOW_QUICK_REFERENCE.txt](WORKFLOW_QUICK_REFERENCE.txt) - Quick reference card

### Music & Theory
- [vault/Songwriting_Guides/song_intent_schema.md](vault/Songwriting_Guides/song_intent_schema.md) - Intent system
- [vault/Songwriting_Guides/rule_breaking_practical.md](vault/Songwriting_Guides/rule_breaking_practical.md) - Rule-breaking
- [vault/Theory_Reference/](vault/Theory_Reference/) - Music theory fundamentals
- [vault/Production_Workflows/](vault/Production_Workflows/) - Production guides

### API & Integration
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - Quick start
- [docs/ADVANCED.md](docs/ADVANCED.md) - Advanced usage
- [docs/LOGIC_PRO_INTEGRATION.md](docs/LOGIC_PRO_INTEGRATION.md) - DAW integration

---

## 🎼 Feature Location Map

### Where to find specific features:

| Feature | Location | Repository |
|---------|----------|------------|
| **Intent Schema** | `music_brain/session/intent_schema.py` | iDAW |
| **Intent Processor** | `music_brain/session/intent_processor.py` | iDAW |
| **Groove Extraction** | `music_brain/groove/extractor.py` | iDAW |
| **Groove Application** | `music_brain/groove/applicator.py` | iDAW |
| **Chord Analysis** | `music_brain/structure/chord.py` | iDAW |
| **Progression Analysis** | `music_brain/structure/progression.py` | iDAW |
| **C++ Harmony Engine** | `src_penta-core/include/penta/harmony/` | iDAW |
| **C++ Groove Engine** | `src_penta-core/include/penta/groove/` | iDAW |
| **Kelly Desktop App** | `src/` (React/Tauri) | kelly-project |
| **Music Brain API** | `api.py` or music_brain API server | iDAW or kelly-project |
| **CLI Tools** | `music_brain/cli.py` | iDAW |
| **Emotional Mapping** | `music_brain/data/emotional_mapping.py` | iDAW |
| **Genre Templates** | `music_brain/data/genre_pocket_maps.json` | iDAW |
| **Chord Progressions** | `music_brain/data/chord_progression_families.json` | iDAW |
| **MCP Servers** | `mcp_todo/`, `mcp_workstation/` | iDAW |
| **Build Scripts** | `build_all.sh`, `Makefile` | miDiKompanion or iDAW |

---

## 🚀 Quick Start Paths

### Path 1: Python Developer (Use Music Brain features)

```bash
# Clone iDAW
git clone https://github.com/sburdges-eng/iDAW.git
cd iDAW

# Install
pip install -e .

# Use CLI
daiw intent new --title "My Song"

# Or Python API
python -c "from music_brain.session import process_intent; print('Ready!')"
```

**Next**: Read [README_music-brain.md](README_music-brain.md)

---

### Path 2: C++ Developer (Build Real-Time Engine)

```bash
# Clone iDAW
git clone https://github.com/sburdges-eng/iDAW.git
cd iDAW/src_penta-core

# Build
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

# Test
./penta_core_tests
```

**Next**: Read [BUILD.md](BUILD.md), [docs/PHASE3_DESIGN.md](docs/PHASE3_DESIGN.md)

---

### Path 3: Desktop App User (Kelly Therapeutic Composer)

```bash
# Clone Kelly project
git clone https://github.com/sburdges-eng/kelly-project.git
cd kelly-project

# Install dependencies
npm install
python -m pip install -e ".[dev]"

# Start API server
./scripts/start_music_brain_api.sh

# Launch app
npm run tauri dev
```

**Next**: Read kelly-project README.md

---

### Path 4: Full Integration (Everything)

```bash
# Clone iDAW (main repo)
git clone https://github.com/sburdges-eng/iDAW.git
cd iDAW

# Python components
pip install -e ".[dev]"

# C++ components
cd src_penta-core && mkdir build && cd build
cmake .. && cmake --build .
cd ../..

# Run tests
pytest tests/

# Try CLI
daiw --help
```

**Next**: Read [WORKFLOW.md](WORKFLOW.md), [REPOSITORY_COMPILATION.md](REPOSITORY_COMPILATION.md)

---

## 🔍 Finding Help

### "Where do I find...?"

| Looking for | Check |
|-------------|-------|
| **How to build** | [BUILD.md](BUILD.md), [MULTI_BUILD.md](MULTI_BUILD.md) |
| **How to use Python API** | [README_music-brain.md](README_music-brain.md) |
| **How to use CLI** | `daiw --help` or [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| **Music theory help** | [vault/Theory_Reference/](vault/Theory_Reference/) |
| **Songwriting help** | [vault/Songwriting_Guides/](vault/Songwriting_Guides/) |
| **Production tips** | [vault/Production_Workflows/](vault/Production_Workflows/) |
| **Development workflow** | [WORKFLOW.md](WORKFLOW.md), [CURSOR_WORKFLOW_GUIDE.md](CURSOR_WORKFLOW_GUIDE.md) |
| **Architecture details** | [REPOSITORY_COMPILATION.md](REPOSITORY_COMPILATION.md) |
| **Which repo to use** | This guide! Start with iDAW |

---

## 📊 Repository Status Summary

| Repo | Status | Use |
|------|--------|-----|
| iDAW | 🟢 **PRIMARY** | Use for all development |
| DAiW-Music-Brain | 🟡 Reference | Mostly integrated into iDAW |
| penta-core | 🟡 Reference | Mostly integrated into iDAW |
| kelly-project | 🟢 Active | Desktop app development |
| miDiKompanion | 🟡 Reference | Build script reference |
| iDAWi | 🟡 Reference | Integration patterns |
| kelly-music-brain-clean | 🟡 Merge pending | Will consolidate |
| Kelly | 🟡 Merge pending | Will consolidate |
| Pentagon-core-100-things | 📚 Archive | iOS reference |
| 1DAW1 | 📚 Archive | Experimental |
| lariat-bible | 📚 Archive | Reference |
| GitHub-all-repo | 📚 Archive | Previous attempt |

**Legend**:
- 🟢 Active - Actively developed, use this
- 🟡 Reference - Contains useful code/docs, being integrated
- 📚 Archive - Reference only, not for new development

---

## 🎯 Decision Tree: Which Repo Should I Clone?

```
START: What do you want to do?
│
├─ Use Python API for music analysis
│  └─> Clone iDAW
│     └─> Read README_music-brain.md
│
├─ Build real-time C++ audio engine
│  └─> Clone iDAW
│     └─> Build src_penta-core/
│     └─> Read BUILD.md
│
├─ Build desktop therapeutic composer
│  └─> Clone kelly-project
│     └─> Read kelly-project README
│
├─ Develop/contribute to main project
│  └─> Clone iDAW
│     └─> Read WORKFLOW.md
│
├─ Learn about the ecosystem
│  └─> Read REPOSITORY_COMPILATION.md (in iDAW)
│
└─ Build automation/scripts
   └─> Clone miDiKompanion (or use iDAW build scripts)
      └─> Read MULTI_BUILD.md
```

---

## 🔗 External Links

### Main Repositories
- **iDAW**: https://github.com/sburdges-eng/iDAW ⭐ PRIMARY
- **DAiW-Music-Brain**: https://github.com/sburdges-eng/DAiW-Music-Brain
- **penta-core**: https://github.com/sburdges-eng/penta-core
- **kelly-project**: https://github.com/sburdges-eng/kelly-project

### Full List
See [REPOSITORY_COMPILATION.md](REPOSITORY_COMPILATION.md#appendix-quick-reference) for complete list

---

## 💡 Pro Tips

1. **Start with iDAW** - It contains 90% of all code
2. **Check REPOSITORY_COMPILATION.md** - Comprehensive analysis of all repos
3. **Use the Python API** - Easier than building C++ for most use cases
4. **Read vault/** - Contains valuable music knowledge beyond just code
5. **Follow WORKFLOW.md** - Structured development process
6. **Check examples/** - Working code examples for common tasks

---

## 📞 Getting Help

1. **Documentation first**: Check this guide, REPOSITORY_COMPILATION.md, README files
2. **Examples second**: Look in `iDAW/examples/` for working code
3. **Source code third**: Code is well-documented with comments
4. **Issues**: Open issue in relevant repository (preferably iDAW)

---

## 🎓 Learning Path

### Beginner
1. Clone iDAW
2. Read README.md
3. Run `daiw --help`
4. Try examples in examples/
5. Read vault/Songwriting_Guides/

### Intermediate
1. Read REPOSITORY_COMPILATION.md
2. Explore music_brain/ Python code
3. Try Python API examples
4. Read vault/Theory_Reference/
5. Experiment with intent schema

### Advanced
1. Read WORKFLOW.md
2. Build src_penta-core/
3. Read docs/PHASE3_DESIGN.md
4. Contribute to development
5. Build Kelly desktop app

---

*This navigation guide is maintained in the iDAW repository.*

**Last Updated**: 2025-12-28  
**Maintained By**: iDAW development team
