# Stuck Log - iDAW/miDiKompanion

> **Purpose:** Document when you get stuck to help debug and prevent future issues
> 
> **When to use:** Same error 3+ times, undoing your own changes, can't remember goal, stuck >2 hours

---

## How to Use This Log

### When You Get Stuck:
1. **STOP CODING** immediately
2. Add entry below with date and description
3. Save your work to a `stuck/YYYY-MM-DD-description` branch
4. Switch to a different task or component
5. Come back later with fresh eyes

### Entry Template:
```markdown
## [YYYY-MM-DD] - Brief Description

**Component:** [Music Brain / Penta-Core / iDAW Core / MCP / Docs]

**What I Was Trying to Do:**
Clear description of the feature/fix

**The Problem:**
What's not working, error message, unexpected behavior

**Error Message:**
\```
Paste full error/traceback here
\```

**What I Tried:**
1. Attempted solution 1 - Result: ...
2. Attempted solution 2 - Result: ...
3. Attempted solution 3 - Result: ...

**Files Involved:**
- path/to/file1.py
- path/to/file2.cpp

**Current Hypothesis:**
What I think might be causing the issue

**Stuck Branch:**
`stuck/YYYY-MM-DD-brief-description`

**Status:**
- [ ] Unresolved
- [ ] Resolved (see solution below)
- [ ] Deferred (not critical, will revisit)
- [ ] Created GitHub Issue: #123

**Solution (if found):**
How the issue was eventually resolved

**Lessons Learned:**
What to avoid or remember for next time

**Time Lost:**
~X hours

---
```

---

## 🚨 ACTIVE STUCK ITEMS

<!-- Move items here when actively stuck, move to Resolved when done -->

### NONE - All clear! 🎉

<!-- When you add an item, move it here from the template above -->

---

## ✅ RESOLVED STUCK ITEMS

<!-- Move items here once resolved, keeping for reference -->

### Example Entry (DELETE THIS)

## [2025-12-22] - Chord Parser Not Recognizing Diminished 7ths

**Component:** Music Brain

**What I Was Trying to Do:**
Add support for "dim7" suffix in chord parser to recognize diminished 7th chords

**The Problem:**
Parser throws KeyError when encountering "dim7", falling back to treating it as an unknown chord

**Error Message:**
```
KeyError: 'dim7'
  File "music_brain/structure/chord.py", line 145, in from_string
    quality = QUALITY_MAP[quality_str]
```

**What I Tried:**
1. Added "dim7" to QUALITY_MAP - Result: Still errored (used wrong key)
2. Changed key to "diminished7" - Result: Still errored (need to update intervals too)
3. Updated intervals and tests - Result: Tests pass but manual test shows wrong notes

**Files Involved:**
- music_brain/structure/chord.py
- tests/test_chord.py

**Current Hypothesis:**
The interval mapping for diminished 7th is [0, 3, 6, 9] but I might have the enharmonic wrong

**Stuck Branch:**
`stuck/2025-12-22-dim7-chords`

**Status:**
- [x] Resolved (see solution below)

**Solution (if found):**
The issue was that I was using [0, 3, 6, 9] but diminished 7th needs [0, 3, 6, 9] AND the 7th needs to be a diminished 7th (9 semitones), not a minor 7th (10). The intervals were correct, but I was testing with C-Eb-Gb-A instead of C-Eb-Gb-Bbb (enharmonically A). Fixed by updating the test expectations.

**Lessons Learned:**
- Always check music theory reference before assuming interval math
- Diminished 7th is symmetrical (all minor 3rds)
- Test with multiple root notes to catch enharmonic issues

**Time Lost:**
~1.5 hours

---

<!-- END EXAMPLE - DELETE ABOVE THIS LINE -->

---

## 📋 DEFERRED ITEMS

<!-- Items that aren't critical and can be revisited later -->

### NONE

---

## 📊 Statistics

**Total Stuck Incidents:** 0  
**Total Resolved:** 0  
**Total Time Lost:** 0 hours  
**Average Time Per Incident:** N/A

**Most Common Issues:**
- N/A (no data yet)

**Components Most Affected:**
- N/A (no data yet)

---

## 💡 Stuck Prevention Tips

Based on past stuck incidents, remember to:

1. ✅ **Run baseline tests BEFORE making changes**
   - Ensures you know what breaks and what was already broken
   
2. ✅ **Make small, testable changes**
   - Easier to debug 10 lines than 100 lines
   
3. ✅ **Check music theory reference FIRST**
   - vault/Theory_Reference/ has the answers
   
4. ✅ **Read existing code before copying patterns**
   - Understand WHY it works that way
   
5. ✅ **Ask Cursor/Claude for explanation BEFORE attempting fix**
   - "Explain how this works" > "Fix this for me"
   
6. ✅ **Take breaks every 90 minutes**
   - Fresh eyes spot obvious issues
   
7. ✅ **One component at a time**
   - Don't mix Python and C++ changes in same session
   
8. ✅ **Document assumptions**
   - Wrong assumptions are easier to spot when written down

---

## 🆘 When to Create GitHub Issue

Create an issue if:
- Stuck for >4 hours total
- Impacts core functionality
- Might affect other developers
- Need architectural guidance
- Security concern
- Breaking change required

**Issue Template:**
```markdown
## Stuck on: [Brief Description]

**Component:** [Music Brain / Penta-Core / iDAW Core / MCP]

**Problem Summary:**
[1-2 sentences]

**Full Context:**
[Copy from STUCK_LOG.md entry]

**Stuck Branch:**
`stuck/YYYY-MM-DD-description`

**Help Needed:**
[ ] Architectural decision
[ ] Debugging assistance
[ ] Code review
[ ] Documentation clarification
[ ] Other: ...

**Priority:**
[ ] Blocking (can't proceed)
[ ] High (impacting progress)
[ ] Medium (can work around)
[ ] Low (nice to fix)
```

---

**Remember:** Getting stuck is NORMAL. This log helps you:
- Learn from mistakes
- Avoid repeating errors
- Know when to ask for help
- Track time spent debugging
- Identify patterns in issues

Every entry makes you a better developer! 🚀
