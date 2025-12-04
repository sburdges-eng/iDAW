/**
 * Clip.h - Audio and MIDI Clip Classes
 */

#pragma once

#include <JuceHeader.h>

namespace iDAW {

/**
 * @brief Base class for clips on tracks
 */
class Clip {
public:
    Clip();
    virtual ~Clip() = default;

    //==========================================================================
    // Position and length (in samples)
    //==========================================================================

    double getStartPosition() const { return startPosition; }
    void setStartPosition(double pos);

    double getLength() const { return length; }
    void setLength(double len);

    double getEndPosition() const { return startPosition + length; }

    double getOffset() const { return offset; }  // Start offset within source
    void setOffset(double off);

    bool containsPosition(double position) const;

    //==========================================================================
    // Display
    //==========================================================================

    juce::String getName() const { return name; }
    void setName(const juce::String& n);

    juce::Colour getColour() const { return colour; }
    void setColour(juce::Colour c);

    //==========================================================================
    // Audio/MIDI access
    //==========================================================================

    virtual void getAudio(juce::AudioBuffer<float>& buffer,
                         double playPosition,
                         double sampleRate);

    virtual void getMidi(juce::MidiBuffer& buffer,
                        double playPosition,
                        int numSamples,
                        double sampleRate);

    //==========================================================================
    // Serialization
    //==========================================================================

    virtual juce::var toVar() const;
    virtual void fromVar(const juce::var& data);

protected:
    juce::String name = "Clip";
    juce::Colour colour{juce::Colour(0xFF00D4FF)};

    double startPosition = 0.0;  // In samples
    double length = 0.0;         // In samples
    double offset = 0.0;         // Offset into source

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Clip)
};

/**
 * @brief Audio clip referencing an audio file
 */
class AudioClip : public Clip {
public:
    AudioClip();

    void setAudioFile(const juce::File& file);
    juce::File getAudioFile() const { return audioFile; }

    void getAudio(juce::AudioBuffer<float>& buffer,
                 double playPosition,
                 double sampleRate) override;

    // Waveform cache for display
    juce::AudioThumbnail* getThumbnail() { return thumbnail.get(); }

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    juce::File audioFile;
    std::unique_ptr<juce::AudioFormatManager> formatManager;
    std::unique_ptr<juce::AudioFormatReaderSource> readerSource;
    std::unique_ptr<juce::AudioThumbnailCache> thumbnailCache;
    std::unique_ptr<juce::AudioThumbnail> thumbnail;

    void loadAudioFile();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AudioClip)
};

/**
 * @brief MIDI clip containing MIDI data
 */
class MidiClip : public Clip {
public:
    MidiClip();

    juce::MidiMessageSequence& getMidiSequence() { return midiData; }
    const juce::MidiMessageSequence& getMidiSequence() const { return midiData; }

    void setMidiSequence(const juce::MidiMessageSequence& seq);

    void getMidi(juce::MidiBuffer& buffer,
                double playPosition,
                int numSamples,
                double sampleRate) override;

    // Editing
    void addNote(int noteNumber, double startBeat, double lengthBeats,
                float velocity, int channel = 1);
    void removeNote(int index);
    void clearNotes();

    juce::var toVar() const override;
    void fromVar(const juce::var& data) override;

private:
    juce::MidiMessageSequence midiData;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MidiClip)
};

} // namespace iDAW
