# 🎯 START HERE - Cursor Workflow Quick Start

> **New to working on iDAW/miDiKompanion in Cursor? Read this first!**

---

## ⚡ 30-Second Quick Start

1. **Read** `CURSOR_WORKFLOW_GUIDE.md` (20 min read, saves hours of confusion)
2. **Bookmark** `PROJECT_NAVIGATION.md` (quick reference map)
3. **Copy** `SESSION_TEMPLATE.md` for your first session
4. **Choose** ONE component to work on today
5. **Start** coding with confidence!

---

## 📚 The 4 Essential Documents

### 1. 🎯 [CURSOR_WORKFLOW_GUIDE.md](CURSOR_WORKFLOW_GUIDE.md)
**Read this first! (~20 min)**

Complete guide for working in Cursor without getting lost:
- Daily workflow step-by-step
- How to use Cursor's AI features effectively
- What to do when stuck (CRITICAL!)
- Emergency procedures
- Example session flow
- Best practices and anti-patterns

**When to use:** Beginning of every session, when feeling overwhelmed

---

### 2. 🗺️ [PROJECT_NAVIGATION.md](PROJECT_NAVIGATION.md)
**Bookmark this! (Quick reference)**

One-page map of the entire project:
- "I want to work on X" → "Go here"
- Directory structure overview
- Common commands cheat sheet
- Quick file location lookup
- Testing commands

**When to use:** Finding files, understanding structure, quick lookups

---

### 3. 📋 [SESSION_TEMPLATE.md](SESSION_TEMPLATE.md)
**Copy for each session!**

Template for tracking your work sessions:
- Session goals
- Files to modify
- Success criteria
- Work log
- Testing checklist
- Stuck detection

**When to use:** Start of every Cursor session (copy → fill out → follow)

---

### 4. 🚨 [STUCK_LOG.md](STUCK_LOG.md)
**Use when stuck!**

Log for documenting when you get stuck:
- What went wrong
- What you tried
- How to recover
- Lessons learned

**When to use:** Same error 3+ times, undoing changes, can't remember goal, >2 hours on one issue

---

## 🎓 Learning Path

### First Day (30 min)
1. ⏱️ 5 min: Read this file (you are here!)
2. ⏱️ 20 min: Read `CURSOR_WORKFLOW_GUIDE.md` (skim at minimum)
3. ⏱️ 5 min: Skim `PROJECT_NAVIGATION.md` (don't memorize, just know it exists)

### First Session (1-2 hours)
1. ⏱️ 5 min: Copy `SESSION_TEMPLATE.md` → `SESSION_NOTES_YYYY-MM-DD_first-session.md`
2. ⏱️ 10 min: Choose ONE component (Music Brain recommended for beginners)
3. ⏱️ 5 min: Set ONE simple goal (e.g., "Run existing tests and understand test structure")
4. ⏱️ 60 min: Work on goal using Cursor
5. ⏱️ 10 min: Fill out session summary
6. ⏱️ 5 min: Commit and push

### First Week (5-10 hours total)
- Day 1: Orientation + first session (above)
- Day 2: Read `MAIN_DOCUMENTATION.md`, explore component you chose
- Day 3: Make a small change (e.g., add a test, fix a typo, add docs)
- Day 4: Make a feature change in your component
- Day 5: Review week, plan next week

### Ongoing (Daily)
Every session:
1. Copy SESSION_TEMPLATE.md
2. Set ONE clear goal
3. Work 1-3 hours max
4. Fill out session notes
5. Commit and push

Every week:
1. Friday: Review all session notes
2. Update PROJECT_ROADMAP.md
3. Clear STUCK_LOG.md (resolve or defer)
4. Plan next week

---

## 🗂️ All Workflow Documents (Alphabetical)

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `.cursorrules` | Cursor AI behavior rules | Auto-loaded by Cursor |
| `CLAUDE_AGENT_GUIDE.md` | AI assistant reference | When using Claude/AI features |
| `CURSOR_WORKFLOW_GUIDE.md` | **Main workflow guide** | **Every session start** |
| `DAiW_Cheat_Sheet.md` | Emotion → music quick ref | When mapping emotions to music |
| `MAIN_DOCUMENTATION.md` | Architecture overview | Understanding codebase structure |
| `PROJECT_NAVIGATION.md` | **Quick file finder** | **Finding any file/feature** |
| `PROJECT_ROADMAP.md` | Development timeline | Checking project status |
| `SESSION_TEMPLATE.md` | **Session notes template** | **Every session** |
| `START_HERE.txt` | Project overview | First time orientation |
| `STUCK_LOG.md` | **Stuck issue tracker** | **When stuck >30 min** |

---

## 🎯 The Golden Rules (Never Forget These)

### 1. ONE COMPONENT AT A TIME
Pick Music Brain OR Penta-Core OR iDAW Core OR MCP OR Docs.  
Don't mix in one session.

**Why:** Context switching kills productivity and causes bugs.

### 2. SESSION BOUNDARIES
Max 3 hours per session. Set clear start/end.  
Use SESSION_TEMPLATE.md every time.

**Why:** Prevents burnout, maintains focus, tracks progress.

### 3. ALWAYS KNOW WHERE YOU ARE
Check PROJECT_NAVIGATION.md when unsure.  
Know which component, which files, which goal.

**Why:** Prevents "lost in codebase" feeling.

### 4. TEST BEFORE AND AFTER
Run tests before starting (baseline).  
Run tests after changes (validation).

**Why:** Know what you broke vs. what was already broken.

### 5. STUCK? STOP IMMEDIATELY
Same error 3 times = STOP.  
Log in STUCK_LOG.md.  
Switch tasks or take break.

**Why:** Digging deeper when stuck wastes time. Fresh eyes solve issues faster.

---

## 🆘 Emergency Quick Reference

### "I'm overwhelmed, where do I start?"
→ Read `CURSOR_WORKFLOW_GUIDE.md` section "🚨 START HERE - The Golden Rules"

### "I can't find file/feature X"
→ Open `PROJECT_NAVIGATION.md` and search (Cmd+F)

### "I'm stuck on same error"
→ Open `STUCK_LOG.md` and create entry, then switch tasks

### "I broke the build"
→ `git status` → `git diff` → `git checkout -- .` (see CURSOR_WORKFLOW_GUIDE.md "Emergency Procedures")

### "I don't know what to work on"
→ Check `PROJECT_ROADMAP.md` → Pick ONE task → Create SESSION_NOTES

### "Tests are failing"
→ Run `pytest tests/test_basic.py -v --tb=long` → Check CURSOR_WORKFLOW_GUIDE.md "Emergency Procedures"

---

## 📊 Workflow At A Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURSOR SESSION WORKFLOW                      │
└─────────────────────────────────────────────────────────────────┘

BEFORE SESSION (5 min)
├─ Copy SESSION_TEMPLATE.md → SESSION_NOTES_YYYY-MM-DD_topic.md
├─ Choose ONE component
├─ Set ONE clear goal
└─ List expected files to touch

DURING SESSION (1-3 hours)
├─ Pull latest: git pull
├─ Run baseline tests
├─ Make small changes (commit every 15-30 min)
├─ Test after each change
├─ Use Cursor Composer (Cmd+I) for edits
├─ Use Cursor Chat (Cmd+L) for understanding
└─ Update SESSION_NOTES as you go

STUCK? (If same error 3x)
├─ STOP coding
├─ Create STUCK_LOG.md entry
├─ Save work: git checkout -b stuck/YYYY-MM-DD-topic
├─ Commit: git add . && git commit -m "WIP: stuck on X"
├─ Push: git push origin stuck/YYYY-MM-DD-topic
└─ Switch tasks or take break

AFTER SESSION (10 min)
├─ Run all tests: pytest tests/ -v
├─ Commit final changes
├─ Push to remote
├─ Update SESSION_NOTES summary
└─ Update PROJECT_ROADMAP.md if major milestone

WEEKLY (30 min)
├─ Review all SESSION_NOTES
├─ Resolve or defer STUCK_LOG.md items
├─ Update PROJECT_ROADMAP.md progress
└─ Plan next week's focus
```

---

## 🎨 Cursor Setup (Optional but Recommended)

### Install Cursor Settings
Create `.vscode/settings.json` in project root:
```json
{
  "cursor.ai.autoSuggest": true,
  "cursor.ai.modelProvider": "claude-3.5-sonnet",
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.testing.pytestEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/build": true
  }
}
```

### Keyboard Shortcuts to Know
- `Cmd+I` (Mac) / `Ctrl+I` (Win) - **Composer** (multi-file edits)
- `Cmd+L` (Mac) / `Ctrl+L` (Win) - **Chat** (ask questions)
- `Cmd+P` - Quick open file
- `Cmd+Shift+F` - Search across files
- `Cmd+K` - Inline AI suggestions

---

## ✅ Pre-Session Checklist

Before starting ANY coding session, check:

- [ ] I've read CURSOR_WORKFLOW_GUIDE.md (at least once)
- [ ] I know which component I'm working on TODAY
- [ ] I've created a SESSION_NOTES file for this session
- [ ] I've set ONE clear goal
- [ ] I've pulled latest changes: `git pull`
- [ ] I've activated my environment (Python venv or C++ tools)
- [ ] I know where to find STUCK_LOG.md if I get stuck
- [ ] I have 1-3 hours available (not 30 min!)

**If you can't check ALL these boxes, STOP and set up first!**

---

## 🎯 Success Metrics

You're succeeding when:
- ✅ You commit code every session
- ✅ You don't feel lost in the codebase
- ✅ You know what component you're working on
- ✅ You recover from stuck situations quickly
- ✅ Your sessions have clear starts and ends
- ✅ You're making steady progress (not perfect progress!)

---

## 💬 Cursor AI Tips

### Using @ Mentions
```
@CURSOR_WORKFLOW_GUIDE.md - Workflow questions
@PROJECT_NAVIGATION.md - Find files
@filename.py - Reference specific file
@folder/ - Reference directory
```

### Good Prompts
```
✅ "Explain how @chord.py parses chord strings"
✅ "Show me all files that use GrooveTemplate"
✅ "Update @test_chord.py to add tests for augmented chords"

❌ "fix this"
❌ "make it better"
❌ "help"
```

### Composer vs Chat
- **Composer (Cmd+I):** Making changes, adding features
- **Chat (Cmd+L):** Understanding code, asking questions, planning

---

## 🎵 Remember the Project Philosophy

> **"Interrogate Before Generate"**

This applies to your workflow too:
- Interrogate: What am I working on? Why? What's the goal?
- Then Generate: Code, tests, commits

> **"The tool shouldn't finish art for people. It should make them braver."**

You're building this toolkit. Stay organized, stay brave, finish your project!

---

## 📞 Get Help

### In This Repo
- **Workflow questions:** Read CURSOR_WORKFLOW_GUIDE.md
- **Technical questions:** Read MAIN_DOCUMENTATION.md
- **File locations:** Read PROJECT_NAVIGATION.md
- **Stuck issues:** Use STUCK_LOG.md

### External
- GitHub Issues: https://github.com/sburdges-eng/iDAW/issues
- Create issue if stuck >4 hours

---

## 🚀 Ready to Start?

1. ✅ Read CURSOR_WORKFLOW_GUIDE.md (20 min) - **DO THIS NOW**
2. ✅ Copy SESSION_TEMPLATE.md
3. ✅ Choose your component
4. ✅ Set your goal
5. ✅ Start coding!

**Next:** Open `CURSOR_WORKFLOW_GUIDE.md` and start reading! 📖

---

**Last Updated:** 2025-12-22  
**Version:** 1.0  
**Maintainer:** iDAW/miDiKompanion Team

---

**You've got this! 🎸🎹🎵**
