/**
 * Track.h - Base Track Class and Track Types
 *
 * Defines the track hierarchy:
 * - Track (abstract base)
 *   - AudioTrack (audio recording/playback)
 *   - MidiTrack (MIDI input/output)
 *   - GroupTrack (submix bus)
 *   - MasterTrack (master output)
 */

#pragma once

#include <JuceHeader.h>
#include <memory>
#include <vector>

namespace iDAW {

// Forward declarations
class Clip;
class PluginSlot;
class TransportState;

/**
 * @brief Track type enumeration
 */
enum class TrackType {
    Audio,
    Midi,
    Group,
    Master
};

/**
 * @brief Abstract base class for all track types
 */
class Track : public juce::ChangeBroadcaster {
public:
    Track(TrackType type, const juce::String& name);
    virtual ~Track() = default;

    //==========================================================================
    // Identity
    //==========================================================================

    TrackType getType() const { return type; }
    juce::String getName() const { return name; }
    void setName(const juce::String& newName);

    juce::Colour getColour() const { return colour; }
    void setColour(juce::Colour c);

    int getIndex() const { return index; }
    void setIndex(int i) { index = i; }

    juce::Uuid getId() const { return id; }

    //==========================================================================
    // Solo/Mute/Arm
    //==========================================================================

    bool isSolo() const { return solo; }
    void setSolo(bool s);

    bool isMuted() const { return muted; }
    void setMuted(bool m);

    bool isArmed() const { return armed; }
    void setArmed(bool a);

    //==========================================================================
    // Volume/Pan
    //==========================================================================

    float getVolume() const { return volume; }  // 0.0 to 1.0
    void setVolume(float v);

    float getVolumeDb() const;
    void setVolumeDb(float db);

    float getPan() const { return pan; }  // -1.0 to 1.0
    void setPan(float p);

    //==========================================================================
    // Output routing
    //==========================================================================

    juce::Uuid getOutputBus() const { return outputBus; }
    void setOutputBus(juce::Uuid busId);

    //==========================================================================
    // Plugin chain
    //==========================================================================

    int getNumPluginSlots() const { return static_cast<int>(pluginSlots.size()); }
    PluginSlot* getPluginSlot(int index);
    void addPluginSlot();
    void removePluginSlot(int index);
    void movePluginSlot(int fromIndex, int toIndex);

    //==========================================================================
    // Clips
    //==========================================================================

    int getNumClips() const { return static_cast<int>(clips.size()); }
    Clip* getClip(int index);
    void addClip(std::unique_ptr<Clip> clip);
    void removeClip(int index);
    Clip* getClipAtPosition(double samplePosition);

    //==========================================================================
    // Audio processing (pure virtual)
    //==========================================================================

    virtual void prepareToPlay(double sampleRate, int samplesPerBlock) = 0;
    virtual void processBlock(juce::AudioBuffer<float>& buffer,
                             juce::MidiBuffer& midiMessages,
                             const TransportState& transport) = 0;
    virtual void releaseResources() = 0;

    //==========================================================================
    // Metering
    //==========================================================================

    float getPeakLevel(int channel) const;
    void resetPeaks();

    //==========================================================================
    // Serialization
    //==========================================================================

    virtual juce::var toVar() const;
    virtual void fromVar(const juce::var& data);

protected:
    TrackType type;
    juce::String name;
    juce::Colour colour{juce::Colour(0xFF00D4FF)};
    juce::Uuid id;
    int index = 0;

    bool solo = false;
    bool muted = false;
    bool armed = false;

    float volume = 1.0f;
    float pan = 0.0f;

    juce::Uuid outputBus;

    std::vector<std::unique_ptr<PluginSlot>> pluginSlots;
    std::vector<std::unique_ptr<Clip>> clips;

    // Metering
    std::array<std::atomic<float>, 2> peakLevels{{0.0f, 0.0f}};

    void updatePeakLevels(const juce::AudioBuffer<float>& buffer);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Track)
};

/**
 * @brief Audio track for recording and playback of audio
 */
class AudioTrack : public Track {
public:
    explicit AudioTrack(const juce::String& name = "Audio");

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>& buffer,
                     juce::MidiBuffer& midiMessages,
                     const TransportState& transport) override;
    void releaseResources() override;

    //==========================================================================
    // Input configuration
    //==========================================================================

    enum class InputType { None, Mono, Stereo };

    InputType getInputType() const { return inputType; }
    void setInputType(InputType type);

    int getInputChannelLeft() const { return inputChannelLeft; }
    int getInputChannelRight() const { return inputChannelRight; }
    void setInputChannels(int left, int right);

    //==========================================================================
    // Recording
    //==========================================================================

    bool isMonitoringInput() const { return monitorInput; }
    void setMonitoringInput(bool monitor);

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    InputType inputType = InputType::Stereo;
    int inputChannelLeft = 0;
    int inputChannelRight = 1;
    bool monitorInput = false;

    double currentSampleRate = 44100.0;
    int currentBlockSize = 512;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AudioTrack)
};

/**
 * @brief MIDI track for sequencing and instrument plugins
 */
class MidiTrack : public Track {
public:
    explicit MidiTrack(const juce::String& name = "MIDI");

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>& buffer,
                     juce::MidiBuffer& midiMessages,
                     const TransportState& transport) override;
    void releaseResources() override;

    //==========================================================================
    // MIDI routing
    //==========================================================================

    int getMidiChannel() const { return midiChannel; }
    void setMidiChannel(int channel);

    bool acceptsAllMidiChannels() const { return midiChannel == 0; }

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    int midiChannel = 0;  // 0 = all channels, 1-16 = specific

    double currentSampleRate = 44100.0;
    int currentBlockSize = 512;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MidiTrack)
};

/**
 * @brief Group track for submixing multiple tracks
 */
class GroupTrack : public Track {
public:
    explicit GroupTrack(const juce::String& name = "Group");

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>& buffer,
                     juce::MidiBuffer& midiMessages,
                     const TransportState& transport) override;
    void releaseResources() override;

    //==========================================================================
    // Child tracks
    //==========================================================================

    void addChildTrack(juce::Uuid trackId);
    void removeChildTrack(juce::Uuid trackId);
    bool hasChildTrack(juce::Uuid trackId) const;
    const std::vector<juce::Uuid>& getChildTrackIds() const { return childTrackIds; }

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    std::vector<juce::Uuid> childTrackIds;

    double currentSampleRate = 44100.0;
    int currentBlockSize = 512;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(GroupTrack)
};

/**
 * @brief Master track - final output with master plugins
 */
class MasterTrack : public Track {
public:
    MasterTrack();

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>& buffer,
                     juce::MidiBuffer& midiMessages,
                     const TransportState& transport) override;
    void releaseResources() override;

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    double currentSampleRate = 44100.0;
    int currentBlockSize = 512;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MasterTrack)
};

} // namespace iDAW
