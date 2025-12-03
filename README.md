# DAiW Bridge JUCE Plugin

This is the JUCE plugin skeleton that connects your DAW to the Python DAiW brain server via OSC.

## Overview

The plugin provides:

- **UI**: Text input, parameter sliders, generate button
- **OSC Communication**: Sends requests to Python brain, receives MIDI events
- **MIDI Output**: Schedules MIDI events from brain server into your DAW

## Building

### Prerequisites

1. **JUCE Framework** - Download from <https://juce.com>
2. **Projucer** - JUCE's project management tool
3. **Xcode** (macOS) or **Visual Studio** (Windows)

### Setup

1. Open `DAiWBridge.jucer` in Projucer
2. Set JUCE modules path
3. Configure for your platform (macOS/Windows)
4. Open generated Xcode/Visual Studio project
5. Build the plugin

### Plugin Formats

The plugin builds as:

- **AU** (Audio Unit) - For Logic Pro, GarageBand
- **VST3** - For most DAWs (Ableton, Reaper, etc.)

## Usage

### 1. Start the Python Brain Server

```bash
python brain_server.py
```

The server listens on port 9000 and sends on port 9001.

### 2. Load Plugin in DAW

1. Build and install the plugin
2. Open your DAW (Logic Pro, Ableton, etc.)
3. Load DAiW Bridge on a MIDI track
4. Plugin UI should show "Connected" status

### 3. Generate MIDI

1. Type emotional text in the text area
2. Adjust sliders (motivation, chaos, vulnerability)
3. Click "Generate MIDI"
4. MIDI events will be scheduled and sent to your DAW

## Architecture

```
┌─────────────┐         OSC          ┌──────────────┐
│ JUCE Plugin │ ◄─────────────────► │ Python Brain │
│  (in DAW)   │   Port 9000/9001     │  (server)    │
└─────────────┘                       └──────────────┘
     │                                       │
     │                                       │
     └──────► MIDI to DAW ◄─────────────────┘
```

## OSC Protocol

### Plugin → Brain Server

- `/daiw/generate` - Send generation request
  - Arguments: text (string), motivation (float), chaos (float), vulnerability (float)
- `/daiw/ping` - Health check

### Brain Server → Plugin

- `/daiw/result` - Generation result with MIDI events (JSON)
- `/daiw/pong` - Response to ping
- `/daiw/error` - Error message (JSON)

## File Structure

```
cpp/DAiWBridge/
├── PluginProcessor.h      # Audio processing and OSC communication
├── PluginProcessor.cpp
├── PluginEditor.h         # UI components
├── PluginEditor.cpp
├── DAiWBridge.jucer      # Projucer project file (to be created)
└── README.md             # This file
```

## Testing

Comprehensive C++ unit tests are available in:

- `PluginProcessorTest.cpp` - Processor functionality tests
- `PluginEditorTest.cpp` - UI component tests
- `OSCCommunicationTest.cpp` - OSC and JSON parsing tests

See `TEST_README.md` for building and running tests.

## Next Steps

1. **Create Projucer Project** - Use Projucer to generate the `.jucer` file
2. **Build Tests** - Compile and run C++ test suite
3. **Test OSC Communication** - Verify plugin can communicate with brain server
4. **MIDI Scheduling** - Improve MIDI event timing and scheduling
5. **UI Enhancements** - Add more controls and visual feedback
6. **Error Handling** - Better error messages and recovery

## Troubleshooting

### Plugin doesn't connect

- Verify `brain_server.py` is running
- Check ports 9000 and 9001 are not blocked
- Check firewall settings

### MIDI not appearing

- Ensure plugin is on a MIDI track
- Check MIDI channel settings
- Verify JSON parsing is working (check console logs)

### Build errors

- Ensure JUCE is properly installed
- Check all modules are included (especially `juce_osc`)
- Verify C++ standard (C++17 or later)

## See Also

- `docs/OSC_SERVER_GUIDE.md` - Python brain server documentation
- `examples/test_osc_client.py` - Test client for OSC communication
- `brain_server.py` - Python brain server implementation
