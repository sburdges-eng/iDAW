# Session Notes: [YYYY-MM-DD] - [Component/Feature]

> **Copy this template for each Cursor session**
> 
> Save as: `SESSION_NOTES_YYYY-MM-DD_brief-description.md`

---

## 📅 Session Info

**Date:** YYYY-MM-DD  
**Start Time:** HH:MM  
**Expected Duration:** X hours  
**Component:** [ Music Brain / Penta-Core / iDAW Core / MCP / Docs / Other ]

---

## 🎯 Goal (ONE clear sentence)

<!-- Example: "Add support for diminished 7th chords in the chord parser" -->



---

## 📋 Files I Expect to Touch

<!-- List the files you think you'll modify -->

- [ ] `path/to/file1.py`
- [ ] `path/to/file2.cpp`
- [ ] `path/to/test_file.py`
- [ ] `path/to/docs.md`

---

## ✅ Success Criteria (How I know I'm done)

- [ ] Feature works as expected
- [ ] Tests pass (existing + new)
- [ ] Code is committed and pushed
- [ ] Documentation updated (if needed)
- [ ] Manual verification completed

---

## 🔗 Related Tasks/Issues

<!-- Link to GitHub issues, TODOs, or other session notes -->

- Related to: #123 (GitHub issue)
- Follow-up from: SESSION_NOTES_2025-12-21_...md
- Blocks: Feature X (needs this to proceed)

---

## 📝 Work Log (Update as you go)

### HH:MM - Session Start
- Pulled latest changes from dev
- Activated venv
- Ran baseline tests: ✅ All passing

### HH:MM - [Milestone 1]
- Did X
- Modified Y
- Result: ...

### HH:MM - [Milestone 2]
- ...

### HH:MM - Testing
- Ran tests: ...
- Manual test: ...

### HH:MM - Session End
- Committed and pushed
- Updated roadmap/TODO

---

## 🧪 Testing Performed

### Automated Tests
```bash
# Commands run
pytest tests/test_chord.py -v

# Results
✅ All tests passing
❌ Failed: test_xyz (describe why)
```

### Manual Testing
```bash
# Commands/scripts run
daiw diagnose "F-C-Am-Dm"
python examples/test_feature.py

# Results
✅ Works as expected
❌ Issue found: ...
```

---

## 🐛 Issues Encountered

### Issue 1: [Brief description]
- **What happened:** ...
- **What I tried:** ...
- **Solution:** ...
- **Time lost:** X minutes

### Issue 2: [If stuck, see STUCK section below]
- ...

---

## 🚫 STUCK? (If yes, fill this out)

### Am I Stuck?
- [ ] Same error 3+ times
- [ ] Undid my own change
- [ ] Can't remember what I'm fixing
- [ ] Breaking unrelated tests
- [ ] Been on this >2 hours

### Stuck Details
**Problem:** Clear description of what's not working

**Error Message:**
```
Paste full error here
```

**What I Tried:**
1. ...
2. ...
3. ...

**Current Hypothesis:** ...

**Action Taken:**
- [ ] Created STUCK_LOG.md entry
- [ ] Saved work to `stuck/YYYY-MM-DD-description` branch
- [ ] Switched to different task
- [ ] Created GitHub issue for help

---

## ✅ Completed Items (Check off as you go)

- [ ] Feature implemented
- [ ] Tests written and passing
- [ ] Manual verification done
- [ ] Code reviewed (by me)
- [ ] Committed with good message
- [ ] Pushed to remote
- [ ] Documentation updated
- [ ] Roadmap/TODO updated

---

## 📊 Session Summary (Fill at end)

### What Got Done ✅
- [x] Implemented X
- [x] Fixed bug Y
- [x] Added Z tests

### What's In Progress 🔄
- [ ] Need to document feature
- [ ] Need to add edge case tests

### What's Blocked 🚫
- None
<!-- or -->
- [ ] Blocked on: [describe blocker]

### Discoveries/Learnings 💡
<!-- Things you learned about the codebase -->
- Discovered that progression.py uses ...
- Found duplicate code in ...
- Learned that ...

### Technical Debt Created 🏦
<!-- Things you know should be refactored later -->
- TODO: Refactor duplicate code in file X
- TODO: Improve error handling in Y

---

## ⏱️ Time Tracking

**Actual Time Spent:** X hours Y minutes

**Breakdown:**
- Setup/environment: X min
- Coding: X min
- Testing: X min
- Debugging: X min
- Documentation: X min

**Productivity Assessment:**
- ⭐⭐⭐⭐⭐ Very productive
- ⭐⭐⭐⭐ Productive
- ⭐⭐⭐ Average
- ⭐⭐ Some progress
- ⭐ Struggled / Stuck

---

## 🔗 Commits Made

<!-- Paste commit hashes and messages -->

```
abc123f feat(chord): add diminished 7th parsing
def456g test(chord): add dim7 chord tests
ghi789j docs: update chord reference
```

---

## 📝 Notes for Next Session

<!-- What should you remember for next time? -->

- Start with: ...
- Remember that: ...
- Don't forget to: ...

---

## 🎯 Next Steps

<!-- What's the logical next task after this? -->

1. [ ] ...
2. [ ] ...
3. [ ] ...

---

**Session End Time:** HH:MM  
**Status:** ✅ Success / 🔄 Partial / ❌ Blocked  
**Overall Feeling:** 😊 Great / 😐 Okay / 😞 Frustrated

---

## 📎 Attachments/Links

<!-- Screenshots, diagrams, external references -->

- Screenshot: ...
- Reference: https://...
- Related docs: ...

---

**REMEMBER:**
- Commit frequently (every 15-30 min)
- Test after each change
- Update this file as you go (not just at the end!)
- If stuck for >30 min, take a break
- If stuck for >2 hours, switch tasks
