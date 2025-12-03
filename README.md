# Sample Library Automation System
**Created:** 2025-11-25
**For:** DAiW Music Brain + Lo-Fi Production Workflow

---

## What This Is

A complete automated system for:
1. Downloading curated Freesound sample packs
2. Organizing samples into a standard folder structure
3. Building a searchable catalog
4. Creating Logic Pro drum kits

Perfect for lo-fi bedroom emo/indie folk production (Kelly song aesthetic).

---

## Quick Start

### 1. Set up Freesound API
```bash
# Get free API key from: https://freesound.org/apiv2/apply/
echo "YOUR_API_KEY_HERE" > ~/.freesound_api_key
chmod 600 ~/.freesound_api_key
```

### 2. Download Sample Packs
```bash
cd ~/Music/Samples
./freesound_downloader.py
```

Downloads 14 curated packs:
- Acoustic drums (kicks, snares, hi-hats)
- Brush drums
- Room ambiences
- Acoustic guitar (notes, harmonics, strums)
- Bass (jazz, upright)
- Vocal textures
- Tape/vinyl FX
- Forest ambience

**Download time:** ~10-15 minutes
**Total size:** ~2-3 GB

### 3. Organize Samples
```bash
./organize_samples.py
```

Sorts all downloads into:
```
~/Music/Samples/
├── Drums/
│   ├── Kicks/
│   ├── Snares/
│   ├── HiHats/
│   └── ...
├── Bass/
├── Guitars/
├── Vocals/
└── FX/
```

Renames files to standard format:
```
[BPM]_[Key]_[Type]_[Description]_[Number].wav
```

Example: `120_Dmin_Kick_Acoustic_01.wav`

### 4. Build Searchable Catalog
```bash
./sample_cataloger.py
```

Creates `sample_catalog.json` with:
- Full metadata for every sample
- BPM, key, type, description
- File paths and sizes
- MD5 hashes (for deduplication)

### 5. Build Your First Kit
```bash
./build_lofi_kit.py
```

Creates `LoFi_Bedroom_Kit_01` with:
- GM-standard MIDI mapping (C1-C2)
- Best quality samples auto-selected
- Logic Pro setup guide
- MPK mini 3 compatible

---

## Searching Samples

```bash
# Find all kicks
./search_samples.py --type Kick

# Find samples at 120 BPM in D minor
./search_samples.py --bpm 120 --key Dmin

# Find all drum samples
./search_samples.py --category Drums

# Find acoustic samples
./search_samples.py --description Acoustic
```

---

## File Structure

```
~/Music/Samples/
├── README.md                    # This file
├── FREESOUND_PACK_LIST.md      # Curated pack list with URLs
├── freesound_downloader.py     # Download automation
├── organize_samples.py         # Sample organizer
├── sample_cataloger.py         # Database builder
├── build_lofi_kit.py          # Kit builder
├── search_samples.py          # Search tool
├── sample_catalog.json         # Generated database
│
├── Drums/
│   ├── Kicks/
│   ├── Snares/
│   ├── HiHats/
│   ├── Cymbals/
│   ├── Toms/
│   ├── Percussion/
│   └── Loops/
│
├── Bass/{Synth,Acoustic,Loops}/
├── Synths/{Pads,Leads,Keys,Arps}/
├── Guitars/{Acoustic,Electric,Loops}/
├── Vocals/{Phrases,Chops,FX}/
├── FX/{Risers,Downlifters,Impacts,Atmosphere}/
└── Loops/{Full,Stems}/
```

---

## Logic Pro Integration

### Using the Generated Kit

1. Open mapping guide:
   ```bash
   open ~/Music/Audio\ Music\ Apps/Sampler\ Instruments/LoFi_Bedroom_Kit_01_MAPPING.txt
   ```

2. In Logic Pro:
   - Create Software Instrument track
   - Load "Sampler" or "Quick Sampler"
   - Drag samples onto MIDI notes (per mapping guide)
   - Save as preset: "LoFi Bedroom Kit 01"

3. Play with your MIDI keyboard!

### MIDI Mapping (GM Standard)

| MIDI Note | Note Name | Drum |
|-----------|-----------|------|
| 36 | C1 | Kick |
| 38 | D1 | Snare |
| 42 | F#1 | Hi-Hat Closed |
| 46 | A#1 | Hi-Hat Open |
| 49 | C#2 | Crash Cymbal |
| 51 | D#2 | Ride Cymbal |
| 41-48 | F1-C2 | Toms (low to high) |

---

## Workflow Examples

### For Kelly Song Production

```bash
# 1. Find acoustic guitar samples in D minor
./search_samples.py --key Dmin --category Guitars

# 2. Find room ambience for bedroom vibe
./search_samples.py --description Room

# 3. Find brush drums for intimate verses
./search_samples.py --description Brush

# 4. Build custom kit with these samples
./build_lofi_kit.py
```

### For Hip-Hop Production

```bash
# Find 90 BPM drum loops
./search_samples.py --bpm 90 --type Loop

# Find bass hits
./search_samples.py --type Bass

# Find vinyl crackle FX
./search_samples.py --description Vinyl
```

---

## Customization

### Add More Packs

Edit `freesound_downloader.py` and add to `PACK_LIST`:

```python
"my_pack": {
    "pack_id": 12345,
    "name": "My Custom Pack",
    "user": "username",
},
```

### Change Naming Convention

Edit `organize_samples.py` function `sanitize_description()`:

```python
# Current format: [BPM]_[Key]_[Type]_[Description]_[Number].wav
# Change to whatever you want
```

### Custom Kit Mappings

Edit `build_lofi_kit.py` function `build_lofi_drum_kit()`:

```python
drum_mapping = {
    36: ("C1", "Kick", "Kick"),
    # Add your own mappings
}
```

---

## Troubleshooting

### "API key not found"
```bash
# Create API key file
echo "YOUR_KEY_HERE" > ~/.freesound_api_key
chmod 600 ~/.freesound_api_key
```

### "No samples to organize"
```bash
# Run downloader first
./freesound_downloader.py
```

### "Catalog not found"
```bash
# Build catalog first
./sample_cataloger.py
```

### "No samples available to build kit"
```bash
# Complete the full workflow:
./freesound_downloader.py
./organize_samples.py
./sample_cataloger.py
./build_lofi_kit.py
```

---

## Tech Stack

- **Python 3:** All automation scripts
- **Freesound API:** Sample downloads
- **JSON:** Database format
- **Logic Pro:** Sampler/EXS24 integration

---

## Next Steps

1. ✅ Run `freesound_downloader.py` - Download packs
2. ✅ Run `organize_samples.py` - Sort into folders
3. ✅ Run `sample_cataloger.py` - Build database
4. ✅ Run `build_lofi_kit.py` - Create first kit
5. 🎹 Load kit in Logic Pro
6. 🎵 Make music!

---

## Integration with DAiW Music Brain

The sample catalog JSON can be used by DAiW for:
- Auto-suggesting samples based on song key/tempo
- Building genre-specific kits
- Sample-based groove templates
- Audio-to-MIDI extraction workflows

Future integration:
```python
from music_brain.audio import SampleLibrary

lib = SampleLibrary("~/Music/Samples/sample_catalog.json")
kicks = lib.find(type="Kick", key="Dmin", bpm=82)
```

---

## Credits

**Sample Packs:** Freesound.org contributors
**Scripts:** DAiW Music Brain project
**Created:** 2025-11-25 for Kelly song production

---

*Happy sampling! 🎵*
