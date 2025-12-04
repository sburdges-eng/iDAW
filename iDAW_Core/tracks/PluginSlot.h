/**
 * PluginSlot.h - Plugin Insert Slot
 */

#pragma once

#include <JuceHeader.h>
#include <memory>

namespace iDAW {

/**
 * @brief A slot for an audio plugin in the track's processing chain
 */
class PluginSlot {
public:
    PluginSlot();
    ~PluginSlot() = default;

    //==========================================================================
    // Plugin instance
    //==========================================================================

    bool hasPlugin() const { return plugin != nullptr; }
    juce::AudioPluginInstance* getPlugin() { return plugin.get(); }

    bool loadPlugin(const juce::PluginDescription& description,
                   juce::AudioPluginFormatManager& formatManager,
                   double sampleRate, int blockSize);

    void clearPlugin();

    juce::String getPluginName() const;
    juce::PluginDescription getPluginDescription() const;

    //==========================================================================
    // Bypass
    //==========================================================================

    bool isEnabled() const { return enabled; }
    void setEnabled(bool e) { enabled = e; }
    void toggleEnabled() { enabled = !enabled; }

    //==========================================================================
    // Processing
    //==========================================================================

    void prepareToPlay(double sampleRate, int samplesPerBlock);
    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages);
    void releaseResources();

    //==========================================================================
    // State
    //==========================================================================

    juce::MemoryBlock getState() const;
    void setState(const juce::MemoryBlock& state);

    //==========================================================================
    // Editor
    //==========================================================================

    juce::AudioProcessorEditor* createEditor();
    bool hasEditor() const;

private:
    std::unique_ptr<juce::AudioPluginInstance> plugin;
    juce::PluginDescription description;
    bool enabled = true;

    double currentSampleRate = 44100.0;
    int currentBlockSize = 512;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PluginSlot)
};

} // namespace iDAW
