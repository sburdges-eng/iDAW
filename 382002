# 🎹 Auto Emotion-Instrument Sampler

**Intelligent sample downloader that systematically organizes FREE samples by emotion and instrument.**

## 🎯 What It Does

Downloads and organizes **25MB** of samples for each combination:

### Emotion Hierarchy (Music-Brain):
1. **Base Emotions** (6): HAPPY, SAD, ANGRY, FEAR, SURPRISE, DISGUST
2. **Sub-Emotions** (36): contentment, joy, grief, despair, rage, frustration, etc.
3. **Sub-Sub-Emotions** (216): satisfied, peaceful, melancholy, nostalgic, etc.

### Instruments (4):
- Piano
- Guitar
- Drums
- Vocals

### Total Combinations:
- **Base**: 6 emotions × 4 instruments = 24 combinations × 25MB = **600MB**
- **Sub**: 36 emotions × 4 instruments = 144 combinations × 25MB = **3.6GB**
- **Sub-Sub**: 216 emotions × 4 instruments = 864 combinations × 25MB = **21.6GB**

**Maximum library size**: ~25GB (if all filled)

## 🚀 Quick Start (3 Steps)

### Step 1: Get Free API Key (2 minutes)

1. Visit: https://freesound.org/
2. Create free account
3. Go to: https://freesound.org/apiv2/apply/
4. Create API app:
   - Name: "iDAW Sample Fetcher"
   - Description: "Personal sample library"
5. Copy API key

### Step 2: Run Setup

```bash
cd ~/Applications/iDAW
./setup_and_start.sh
```

Paste your API key when prompted.

### Step 3: Start Downloading

The script will automatically:
1. Download 5 samples for each base emotion × instrument (24 combos)
2. Move to sub-emotions (36 combos)
3. Sync everything to Google Drive
4. Show progress and statistics

## 📊 Download Order

### Phase 1: Base Emotions (6 × 4 = 24 combinations)

```
1. HAPPY + piano     → 5 files (~25MB)
2. HAPPY + guitar    → 5 files (~25MB)
3. HAPPY + drums     → 5 files (~25MB)
4. HAPPY + vocals    → 5 files (~25MB)

5. SAD + piano       → 5 files (~25MB)
6. SAD + guitar      → 5 files (~25MB)
7. SAD + drums       → 5 files (~25MB)
8. SAD + vocals      → 5 files (~25MB)

9. ANGRY + piano     → 5 files (~25MB)
10. ANGRY + guitar   → 5 files (~25MB)
11. ANGRY + drums    → 5 files (~25MB)
12. ANGRY + vocals   → 5 files (~25MB)

13. FEAR + piano     → 5 files (~25MB)
14. FEAR + guitar    → 5 files (~25MB)
15. FEAR + drums     → 5 files (~25MB)
16. FEAR + vocals    → 5 files (~25MB)

17. SURPRISE + piano → 5 files (~25MB)
18. SURPRISE + guitar→ 5 files (~25MB)
19. SURPRISE + drums → 5 files (~25MB)
20. SURPRISE + vocals→ 5 files (~25MB)

21. DISGUST + piano  → 5 files (~25MB)
22. DISGUST + guitar → 5 files (~25MB)
23. DISGUST + drums  → 5 files (~25MB)
24. DISGUST + vocals → 5 files (~25MB)
```

**Total Phase 1**: 120 files, ~600MB

### Phase 2: Sub-Emotions (First 20)

```
CONTENTMENT, JOY, HOPEFUL, GRATEFUL, LOVE, PRIDE (from HAPPY)
GRIEF, DESPAIR, LONELINESS, HURT, DISAPPOINTED, SHAME (from SAD)
RAGE, FRUSTRATED, ANNOYED, BITTER (from ANGRY)
... etc
```

Each × 4 instruments = 5 files per combo

## 📁 File Organization

### Local Staging:
```
~/Applications/iDAW/emotion_instrument_staging/
├── base/
│   ├── HAPPY/
│   │   ├── piano/
│   │   │   ├── 12345_happy_piano.mp3
│   │   │   ├── 67890_joyful_keys.mp3
│   │   │   └── ...
│   │   ├── guitar/
│   │   ├── drums/
│   │   └── vocals/
│   ├── SAD/
│   ├── ANGRY/
│   ├── FEAR/
│   ├── SURPRISE/
│   └── DISGUST/
└── sub/
    ├── CONTENTMENT/
    ├── JOY/
    └── ...
```

### Google Drive (Permanent):
```
~/sburdges@gmail.com - Google Drive/My Drive/iDAW_Samples/Emotion_Instrument_Library/
├── base/
│   ├── HAPPY/
│   │   ├── piano/ (25MB)
│   │   ├── guitar/ (25MB)
│   │   ├── drums/ (25MB)
│   │   └── vocals/ (25MB)
│   └── ...
└── sub/
    └── ...
```

## 🎵 Sample Use Cases

### Base Emotions:
| Emotion | Instrument | Use Case |
|---------|-----------|----------|
| HAPPY | piano | Uplifting chord progressions |
| HAPPY | guitar | Bright strumming patterns |
| HAPPY | drums | Energetic rhythms |
| HAPPY | vocals | Joyful vocal samples |
| SAD | piano | Melancholic melodies |
| SAD | guitar | Somber fingerpicking |
| ANGRY | drums | Aggressive beats |
| FEAR | piano | Dissonant, tense chords |
| SURPRISE | vocals | Unexpected vocal textures |

### Sub-Emotions:
| Emotion | Instrument | Use Case |
|---------|-----------|----------|
| CONTENTMENT | piano | Peaceful ambient pads |
| GRIEF | strings | Mournful orchestral |
| RAGE | drums | Intense percussion |
| ANXIETY | synth | Tense soundscapes |

## 📈 Progress Tracking

The script automatically tracks:
- ✅ Total combinations downloaded
- ✅ Files per combination
- ✅ Size per combination (max 25MB)
- ✅ Last downloaded emotion/instrument
- ✅ Total library size

### View Progress:
```bash
./auto_emotion_sampler.py stats
```

Shows:
```
Statistics:
  Total Combinations: 24
  Total Files: 120
  Total Size: 600.00MB
  Google Drive: ~/sburdges@gmail.com.../Emotion_Instrument_Library/
```

## 🛠 Advanced Usage

### Manual Start (Skip Setup):
```bash
# If API key already configured
./auto_emotion_sampler.py start
```

### Sync Only (No Download):
```bash
./auto_emotion_sampler.py sync
```

### View Stats:
```bash
./auto_emotion_sampler.py stats
```

## 🔧 Configuration

### Change Files Per Combination:
Edit `auto_emotion_sampler.py`:
```python
sampler.auto_fetch_all(files_per_combo=10)  # Default is 5
```

### Change Size Limit:
Edit `auto_emotion_sampler.py`:
```python
MAX_SIZE_PER_COMBO_MB = 50  # Default is 25MB
```

### Add More Instruments:
Edit `auto_emotion_sampler.py`:
```python
INSTRUMENTS = ["piano", "guitar", "drums", "vocals", "bass", "synth"]
```

### Change Download Order:
The script downloads in this order:
1. Base emotions (all 6)
2. First 20 sub-emotions
3. (Can be extended to all 36 sub-emotions + 216 sub-sub-emotions)

## 📊 Expected Results

### After First Run (~30-60 minutes):
- **Phase 1 Complete**: 6 base emotions × 4 instruments = 24 combinations
- **~120 samples** downloaded
- **~600MB** total size
- All synced to Google Drive

### After Extended Run (~2-4 hours):
- **Phase 1 + Phase 2**: 26 emotions × 4 instruments = 104 combinations
- **~500 samples** downloaded
- **~2.5GB** total size

## ⚡ Performance Tips

### Faster Downloads:
- Good internet connection (downloads are ~5MB each)
- Run overnight for large libraries
- Freesound API has rate limits (1 download per second)

### Resume Interrupted Downloads:
Simply run again:
```bash
./auto_emotion_sampler.py start
```

The script automatically:
- ✅ Skips completed combinations (already at 25MB)
- ✅ Continues where it left off
- ✅ Doesn't re-download existing files

## 🎨 Integration

### With fetch_musical:
```bash
# Find scales for an emotion
./fetch_musical scale emotion grief

# Download samples for that emotion
./auto_emotion_sampler.py start
# (Will include grief samples)
```

### With DAiW-Music-Brain:
The emotion hierarchy comes from your Music-Brain taxonomy:
- `music_brain/happy.json` → HAPPY base emotion
- `music_brain/sad.json` → SAD base emotion
- etc.

## ❓ Troubleshooting

### "API key required" error:
```bash
./setup_and_start.sh
```
Re-enter your API key.

### No samples found:
- Freesound searches are hit-or-miss
- Some emotion-instrument combos have few results
- Script automatically tries multiple search queries

### Downloads are slow:
- Normal! Freesound has rate limiting
- 1 file per second = 120 files takes ~2 minutes
- 500 files takes ~10 minutes

### Google Drive not syncing:
Check the path in `auto_emotion_sampler.py`:
```python
GDRIVE_ROOT = Path.home() / "sburdges@gmail.com - Google Drive" / "My Drive"
```

Update if your Google Drive is in a different location.

## 📝 License

- Freesound samples: Check individual licenses (most are Creative Commons)
- Script: Free to use for personal projects
- Music-Brain taxonomy: Part of DAiW framework

## 🎯 Next Steps

After downloading:
1. ✅ Browse samples in Google Drive
2. ✅ Import into DAW (Ableton, Logic, etc.)
3. ✅ Create playlists by emotion
4. ✅ Build custom instrument racks
5. ✅ Generate emotion-driven compositions

Enjoy your emotion-organized sample library! 🎵
