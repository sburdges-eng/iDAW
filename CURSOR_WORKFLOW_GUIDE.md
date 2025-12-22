# 🎯 Cursor Workflow Guide for iDAW/miDiKompanion

> **How to Work in Cursor Without Getting Lost or Overwhelmed**
> 
> Last Updated: 2025-12-22 | For: iDAW/miDiKompanion Project

---

## 🚨 START HERE - The Golden Rules

### 1. **ONE TASK AT A TIME**
   - Pick ONE specific feature/bug from your TODO
   - Complete it fully before moving to next
   - Resist the urge to "quickly fix" unrelated things

### 2. **SESSION BOUNDARIES**
   - Each Cursor session = 1-3 hours max
   - Start with a clear goal
   - End with documentation of what you did
   - Use the SESSION_TEMPLATE.md (see below)

### 3. **ALWAYS KNOW WHERE YOU ARE**
   - Use the Project Map (see below) at session start
   - Check which component you're working on
   - Understand dependencies before making changes

---

## 📍 Quick Project Map - Where Am I?

Your project has **4 MAJOR COMPONENTS**:

```
┌──────────────────────────────────────────────────────────────────┐
│                    iDAW/miDiKompanion PROJECT                    │
└──────────────────────────────────────────────────────────────────┘

1️⃣  MUSIC BRAIN (Python Intelligence Layer)
    📁 Location: /music_brain/
    🎯 Purpose: Music theory, emotion mapping, MIDI generation
    🔧 Tools: Python, pytest
    📚 Docs: CLAUDE_AGENT_GUIDE.md, MAIN_DOCUMENTATION.md
    ✅ When to work here: Theory logic, intent processing, chord analysis
    
2️⃣  PENTA-CORE (C++ Real-Time Audio Processing)
    📁 Location: /src_penta-core/, /penta_core_music-brain/
    🎯 Purpose: Low-latency audio/MIDI processing, groove engine
    🔧 Tools: C++, CMake, clang
    📚 Docs: docs_penta-core/
    ✅ When to work here: Performance-critical audio, real-time MIDI
    
3️⃣  iDAW CORE (JUCE DAW Framework)
    📁 Location: /iDAW_Core/
    🎯 Purpose: Full DAW application, UI, plugin hosting
    🔧 Tools: C++, JUCE, CMake
    📚 Docs: COMPREHENSIVE_TODO_IDAW.md, BUILD.md
    ✅ When to work here: DAW features, UI, audio engine
    
4️⃣  MCP SERVERS (AI Integration Layer)
    📁 Location: /mcp_todo/, /mcp_workstation/
    🎯 Purpose: Model Context Protocol for AI assistants
    🔧 Tools: Python, Node.js
    📚 Docs: mcp_*/README.md
    ✅ When to work here: Claude/AI tool integration

🗄️  VAULT (Knowledge Base)
    📁 Location: /vault/
    🎯 Purpose: Obsidian-compatible docs, guides, theory
    ✅ When to work here: Documentation, writing guides
```

---

## 🎯 Daily Workflow - Step by Step

### **BEFORE YOU START CODING**

#### Step 1: Choose Your Component (2 min)
```bash
# Ask yourself: "What am I working on today?"
# Answer should be ONE of:
# - Music Brain (Python theory/MIDI)
# - Penta-Core (C++ audio engine)
# - iDAW Core (JUCE DAW)
# - MCP Servers (AI tools)
# - Documentation/Vault
```

#### Step 2: Set Your Session Goal (3 min)
Create a file: `SESSION_NOTES_YYYY-MM-DD.md` (template below)
```markdown
# Session: [Date] [Component]

## Goal (ONE sentence)
Fix chord progression analyzer to handle diminished chords

## Files I Expect to Touch
- music_brain/structure/progression.py
- tests/test_progression.py

## Success Criteria
- [ ] Diminished chords parse correctly
- [ ] Tests pass
- [ ] Committed and pushed
```

#### Step 3: Check Dependencies (2 min)
```bash
# For Music Brain (Python)
cd /home/runner/work/iDAW/iDAW
source venv/bin/activate || python -m venv venv && source venv/bin/activate
pip install -e .

# For Penta-Core (C++)
cd src_penta-core && cmake . && make

# For iDAW Core (JUCE)
cd iDAW_Core && cmake -B build && cmake --build build
```

---

### **WHILE YOU'RE CODING**

#### ✅ DO:
1. **Use Cursor's Composer** for multi-file edits
   - `Cmd+I` (Mac) or `Ctrl+I` (Windows)
   - Clearly describe the change
   - Review ALL suggested changes before accepting

2. **Use Cursor Chat** for understanding
   - `Cmd+L` - Ask "What does this function do?"
   - Reference specific files with `@filename`
   - Ask "Show me where this is used" before deleting

3. **Git Commit Frequently**
   ```bash
   # After every logical change (every 15-30 min)
   git add .
   git commit -m "feat: [component] brief description"
   git push origin dev
   ```

4. **Run Tests After Each Change**
   ```bash
   # Music Brain
   pytest tests/test_basic.py -v
   
   # Penta-Core
   cd src_penta-core && ./run_tests.sh
   
   # iDAW Core
   cd iDAW_Core/build && ctest
   ```

#### ❌ DON'T:
1. **DON'T** jump between components in one session
2. **DON'T** make "quick fixes" to unrelated code
3. **DON'T** delete files without checking git history
4. **DON'T** skip tests because "it looks right"
5. **DON'T** work for more than 3 hours without a break

---

### **WHEN YOU GET STUCK** (CRITICAL SECTION)

#### 🔴 STUCK DETECTION RULES
If you experience any of these, **STOP IMMEDIATELY**:
- Same error 3 times in a row
- Undoing your own change from <1 hour ago
- Can't remember what you were trying to fix
- Breaking tests you didn't touch
- Googling the same question twice

#### 🛠️ UNSTUCK PROTOCOL

1. **STOP CODING** - Step away from keyboard
2. **DOCUMENT THE PROBLEM**
   ```bash
   # Create: STUCK_LOG.md (if doesn't exist)
   echo "## [Date] - Stuck on: [Brief description]" >> STUCK_LOG.md
   echo "Files: [list]" >> STUCK_LOG.md
   echo "Error: [paste error]" >> STUCK_LOG.md
   echo "Attempts: [what I tried]" >> STUCK_LOG.md
   echo "---" >> STUCK_LOG.md
   ```

3. **RESET YOUR WORKSPACE**
   ```bash
   # Save your changes to a branch
   git checkout -b stuck/YYYY-MM-DD-description
   git add . && git commit -m "WIP: stuck on [issue]"
   git push origin stuck/YYYY-MM-DD-description
   
   # Go back to clean state
   git checkout dev
   git pull
   ```

4. **SWITCH TASKS**
   - Pick a DIFFERENT component
   - Do something easy (docs, tests, cleanup)
   - Come back tomorrow with fresh eyes

5. **ASK FOR HELP**
   - Create GitHub Issue with:
     - Link to stuck branch
     - STUCK_LOG.md contents
     - What you tried
     - What you expected vs. got

---

## 📋 Cursor-Specific Best Practices

### 1. **Using Cursor's AI Features Effectively**

#### Composer (Cmd+I) - For Making Changes
```
✅ GOOD PROMPT:
"Update music_brain/structure/chord.py to add support for 
diminished 7th chords. The parse_chord() function should 
recognize 'dim7' suffix and set quality='dim7'. Add a test 
in tests/test_chord.py."

❌ BAD PROMPT:
"fix the chords"
```

#### Chat (Cmd+L) - For Understanding
```
✅ GOOD QUESTIONS:
- "@progression.py What does diagnose_progression() return?"
- "Show me all places where GrooveTemplate is instantiated"
- "Explain the intent schema data flow from CLI to MIDI output"

❌ BAD QUESTIONS:
- "How does this work?" (too vague)
- "Fix this" (use Composer instead)
```

### 2. **Using @ Mentions**
```
@filename.py          - Reference specific file
@folder/              - Reference directory
@#symbol              - Reference function/class
@docs/                - Reference documentation folder

Example:
"Compare @music_brain/groove/extractor.py with 
@src_penta-core/groove/groove_engine.cpp - which 
should I modify for adding swing quantization?"
```

### 3. **Using Terminal in Cursor**
```bash
# Keep 2-3 terminal tabs open:

Tab 1: Git operations
git status
git diff
git commit -m "..."

Tab 2: Testing
pytest tests/ -v --tb=short

Tab 3: Running the app
daiw diagnose "F-C-Am-Dm"
python app.py
```

---

## 🗂️ File Organization Tips

### **NEVER TOUCH THESE FILES** (Unless you're SURE)
```
❌ .git/
❌ .github/workflows/
❌ venv/, node_modules/
❌ build/, cmake-build-*/
❌ *.pyc, __pycache__/
❌ LICENSE files
❌ README.md (without good reason)
```

### **FREQUENTLY MODIFIED FILES**
```
✅ music_brain/**/*.py        (Python logic)
✅ src_penta-core/**/*.cpp    (C++ audio engine)
✅ tests/**/*.py              (Tests)
✅ vault/**/*.md              (Documentation)
✅ SESSION_NOTES_*.md         (Your notes)
```

### **UNDERSTAND BEFORE MODIFYING**
```
⚠️  pyproject.toml            (Dependencies)
⚠️  CMakeLists.txt            (Build config)
⚠️  music_brain/cli.py        (CLI interface)
⚠️  **/intent_schema.py       (Core data structures)
```

---

## 🎓 Learning the Codebase

### Week 1: Orientation
- [ ] Read START_HERE.txt
- [ ] Read MAIN_DOCUMENTATION.md
- [ ] Read CLAUDE_AGENT_GUIDE.md
- [ ] Run `daiw --help` and try each command
- [ ] Run `pytest tests/test_basic.py -v`

### Week 2: Music Brain Deep Dive
- [ ] Study `music_brain/session/intent_schema.py`
- [ ] Study `music_brain/structure/chord.py`
- [ ] Study `music_brain/groove/templates.py`
- [ ] Trace a command: `daiw diagnose "F-C-Am-Dm"` from CLI to output

### Week 3: Choose Your Path
- **Path A (Python Developer):** Deep dive into music_brain
- **Path B (C++ Developer):** Deep dive into penta-core/iDAW_Core
- **Path C (Documentation):** Vault, guides, examples
- **Path D (Integration):** MCP servers, DAW integrations

---

## 📊 Progress Tracking

### Daily Checklist (End of Session)
```markdown
## [Date] Session Summary

Component: [Music Brain / Penta-Core / iDAW Core / MCP / Docs]

✅ Completed:
- [x] Fixed chord diminished parsing
- [x] Added 3 new tests
- [x] All tests passing

🔄 In Progress:
- [ ] Documenting the new chord types

🚫 Blocked/Stuck:
- None (or describe and log in STUCK_LOG.md)

📝 Notes:
- Discovered that progression.py has duplicate code (refactor later)

⏰ Time Spent: 2h 15min

🔗 Commits: 
- abc123f feat: add diminished chord parsing
- def456g test: add diminished chord tests
```

### Weekly Review (Every Friday)
```markdown
## Week of [Date Range]

Sessions: 5
Total Time: 10h 30min

Major Accomplishments:
1. Completed chord analyzer improvements
2. Fixed 3 bugs in groove extractor
3. Updated documentation

Stuck Items Resolved: 1
Stuck Items Remaining: 0

Next Week Focus:
- Start on tempo detection feature
- Review penta-core integration
```

---

## 🎯 Example Session Flow

### Scenario: "Add support for augmented chords"

```bash
# ===== SESSION START =====
# Time: 9:00 AM | Expected Duration: 2 hours

# 1. CREATE SESSION NOTE
cat > SESSION_NOTES_2025-12-22_augmented-chords.md << EOF
# Session: 2025-12-22 - Music Brain

## Goal
Add augmented chord parsing to chord.py

## Files to Modify
- music_brain/structure/chord.py
- tests/test_chord.py
- docs_music-brain/chord_reference.md

## Success Criteria
- [x] Parse "Caug" and "C+" as augmented
- [x] Tests pass
- [x] Committed
EOF

# 2. CHECK OUT FEATURE BRANCH
git checkout -b feat/augmented-chords
git pull origin dev

# 3. ACTIVATE ENVIRONMENT
source venv/bin/activate

# 4. RUN EXISTING TESTS (baseline)
pytest tests/test_chord.py -v
# ✓ All pass (baseline established)

# 5. OPEN CURSOR, USE COMPOSER
# Cmd+I: "Add augmented chord support to @chord.py
#  - Recognize 'aug' and '+' suffixes
#  - Set quality='augmented'
#  - Intervals: [0, 4, 8]
#  Also update @test_chord.py with tests for 'Caug' and 'C+'"

# 6. REVIEW CHANGES IN CURSOR
# - Check chord.py diff
# - Check test_chord.py diff
# - Accept if looks good

# 7. RUN TESTS
pytest tests/test_chord.py -v
# ✓ New tests pass!

# 8. MANUAL VERIFICATION
python -c "
from music_brain.structure.chord import Chord
c = Chord.from_string('Caug')
print(f'Root: {c.root}, Quality: {c.quality}')
# Expected: Root: C, Quality: augmented
"
# ✓ Works!

# 9. COMMIT
git add music_brain/structure/chord.py tests/test_chord.py
git commit -m "feat(chord): add augmented chord parsing

- Recognize 'aug' and '+' suffixes
- Add chord.quality='augmented' 
- Add tests for Caug and C+
- All tests passing"

# 10. PUSH
git push origin feat/augmented-chords

# 11. UPDATE SESSION NOTES
cat >> SESSION_NOTES_2025-12-22_augmented-chords.md << EOF

## Completed ✅
- [x] Augmented parsing works
- [x] Tests passing
- [x] Committed and pushed

## Time: 1h 15min (under estimate!)

## Next: Create PR, then move to diminished chords
EOF

# ===== SESSION END =====
# Time: 10:15 AM | Actual Duration: 1h 15min
# Status: SUCCESS ✅
```

---

## 🆘 Emergency Procedures

### "I broke the build!"
```bash
# 1. DON'T PANIC
# 2. Check what changed
git status
git diff

# 3. If recent change (< 1 hour ago):
git checkout -- .  # Discard all changes

# OR if you want to save your work:
git stash
git stash list

# 4. Verify build works
pytest tests/test_basic.py
# or
cd iDAW_Core && cmake --build build

# 5. If still broken, reset to last known good commit
git log --oneline -10
git reset --hard abc123f  # Use commit hash from git log

# 6. Document what happened
echo "## [Date] Build Break" >> STUCK_LOG.md
echo "What I did: ..." >> STUCK_LOG.md
echo "How I fixed: git reset --hard abc123f" >> STUCK_LOG.md
```

### "I can't find the file I need!"
```bash
# Search by filename
find . -name "*chord*" -type f

# Search by content
grep -r "diagnose_progression" --include="*.py"

# Use Cursor's Cmd+P (Quick Open)
# Type filename and it appears

# Ask Cursor Chat
# "Where is the GrooveTemplate class defined?"
```

### "Tests are failing and I don't know why!"
```bash
# 1. Run just ONE test
pytest tests/test_chord.py::test_parse_major -v

# 2. See FULL error output
pytest tests/test_chord.py -v --tb=long

# 3. Add print debugging
# Edit test file, add: print(f"Value: {chord.quality}")
pytest tests/test_chord.py -v -s  # -s shows prints

# 4. Ask Cursor
# Cmd+L: "@test_chord.py This test is failing: [paste error]
#  What could cause this?"
```

---

## 📚 Reference Quick Links

### Key Documentation Files
```
START_HERE.txt                    # Project overview
MAIN_DOCUMENTATION.md             # Architecture
CLAUDE_AGENT_GUIDE.md             # AI assistant reference
PROJECT_ROADMAP.md                # What's complete, what's next
COMPREHENSIVE_TODO_IDAW.md        # Task list
DAiW_Cheat_Sheet.md              # Emotion → music parameters
WORKFLOW.md                       # Development workflow
BUILD.md                          # Build instructions
```

### Testing
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_chord.py -v

# Specific test function
pytest tests/test_chord.py::test_augmented -v

# With coverage
pytest tests/ --cov=music_brain --cov-report=html
```

### Git Workflow
```bash
# Daily workflow
git checkout dev
git pull
git checkout -b feat/my-feature
# ... make changes ...
git add .
git commit -m "feat: description"
git push origin feat/my-feature

# Feature complete
# Create PR on GitHub
# Get review
# Merge to dev
```

---

## 🎨 Cursor Theme & Settings Recommendations

### Recommended Settings (Settings > Cursor Settings)
```json
{
  "cursor.ai.autoSuggest": true,
  "cursor.ai.modelProvider": "claude-3.5-sonnet",
  "cursor.chat.contextFiles": 5,
  "cursor.composer.enabled": true,
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "git.autofetch": true,
  "python.testing.pytestEnabled": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### Workspace Settings (.vscode/settings.json)
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.testing.pytestArgs": ["tests"],
  "python.analysis.extraPaths": ["${workspaceFolder}/music_brain"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/build": true,
    "**/.pytest_cache": true
  }
}
```

---

## ✅ Quick Start Checklist

### First Time Setup (Do Once)
- [ ] Read this entire guide (yes, all of it!)
- [ ] Bookmark this file in Cursor
- [ ] Install dependencies (Python venv, C++ tools)
- [ ] Run all tests to verify baseline
- [ ] Create your first SESSION_NOTES file
- [ ] Make a trivial change and commit it (practice workflow)

### Every Session (Do Every Time)
- [ ] Know which component you're working on
- [ ] Create SESSION_NOTES file with clear goal
- [ ] Pull latest changes (`git pull`)
- [ ] Run tests before starting (baseline)
- [ ] Work for 1-3 hours MAX
- [ ] Run tests after changes
- [ ] Commit and push
- [ ] Update SESSION_NOTES with results

### Every Week (Friday afternoon)
- [ ] Review all SESSION_NOTES from the week
- [ ] Update PROJECT_ROADMAP.md with progress
- [ ] Clear out STUCK_LOG.md (resolve or defer items)
- [ ] Plan next week's focus
- [ ] Push all branches
- [ ] Take a break! 🎉

---

## 🎯 Finishing Your Project

### How to Know When You're Done

Your project is complete when:
1. ✅ All tests pass
2. ✅ All TODO items marked complete
3. ✅ Documentation is updated
4. ✅ You can demo all features
5. ✅ No critical bugs in issue tracker
6. ✅ You've used it to make actual music!

### The Final Sprint (Last 10%)

The last 10% takes 50% of the time. Plan for:
- **Polish:** UI tweaks, better error messages
- **Documentation:** User guide, video tutorials
- **Testing:** Real-world usage, edge cases
- **Deployment:** Installers, release notes
- **Marketing:** Show it off, get feedback!

### Stay Motivated

- **Small wins:** Commit something every day
- **Visible progress:** Update roadmap weekly
- **Share progress:** Post demos, screenshots
- **Use your own tool:** Make music with it!
- **Remember why:** You're building something amazing

---

## 📞 When to Ask for Help

### Ask Cursor/Claude when:
- ✅ Understanding existing code
- ✅ Writing boilerplate
- ✅ Debugging specific errors
- ✅ Finding files or functions
- ✅ Generating tests

### Ask a human when:
- ❓ Major architecture decisions
- ❓ Stuck for more than 2 hours
- ❓ Security/safety concerns
- ❓ License/legal questions
- ❓ Project direction choices

### Community Resources
- GitHub Issues (your repo)
- Music production forums
- Python/C++ Discord servers
- /r/audioengineering, /r/WeAreTheMusicMakers

---

## 🎵 Final Words

> "The tool shouldn't finish art for people. It should make them braver."

You're building something that embodies this philosophy. The workflow in this guide is designed to keep you:

1. **Focused** - One component at a time
2. **Unblocked** - Clear stuck protocols
3. **Progressing** - Regular commits and tests
4. **Motivated** - Visible progress, small wins
5. **Finishing** - Clear completion criteria

Remember:
- **Slow and steady wins** - 2 hours/day > 12 hours/weekend
- **Perfect is the enemy of done** - Ship it, then improve it
- **Use your own tool** - Dogfooding reveals real issues
- **Take breaks** - Fresh eyes solve stuck problems
- **Celebrate progress** - Every commit is a win!

Now go make some music. 🎸🎹🎵

---

**Last Updated:** 2025-12-22  
**Version:** 1.0  
**Maintainer:** iDAW/miDiKompanion Team
