/**
 * PluginSlot.cpp - Plugin Slot Implementation
 */

#include "PluginSlot.h"

namespace iDAW {

PluginSlot::PluginSlot() = default;

bool PluginSlot::loadPlugin(const juce::PluginDescription& desc,
                            juce::AudioPluginFormatManager& formatManager,
                            double sampleRate, int blockSize) {
    juce::String errorMessage;

    plugin = formatManager.createPluginInstance(
        desc, sampleRate, blockSize, errorMessage);

    if (plugin) {
        description = desc;
        currentSampleRate = sampleRate;
        currentBlockSize = blockSize;
        plugin->prepareToPlay(sampleRate, blockSize);
        return true;
    }

    DBG("Failed to load plugin: " + errorMessage);
    return false;
}

void PluginSlot::clearPlugin() {
    if (plugin) {
        plugin->releaseResources();
        plugin.reset();
    }
    description = juce::PluginDescription();
}

juce::String PluginSlot::getPluginName() const {
    if (plugin) {
        return plugin->getName();
    }
    return "Empty";
}

juce::PluginDescription PluginSlot::getPluginDescription() const {
    return description;
}

void PluginSlot::prepareToPlay(double sampleRate, int samplesPerBlock) {
    currentSampleRate = sampleRate;
    currentBlockSize = samplesPerBlock;

    if (plugin) {
        plugin->prepareToPlay(sampleRate, samplesPerBlock);
    }
}

void PluginSlot::processBlock(juce::AudioBuffer<float>& buffer,
                              juce::MidiBuffer& midiMessages) {
    if (plugin && enabled) {
        plugin->processBlock(buffer, midiMessages);
    }
}

void PluginSlot::releaseResources() {
    if (plugin) {
        plugin->releaseResources();
    }
}

juce::MemoryBlock PluginSlot::getState() const {
    juce::MemoryBlock state;
    if (plugin) {
        plugin->getStateInformation(state);
    }
    return state;
}

void PluginSlot::setState(const juce::MemoryBlock& state) {
    if (plugin && state.getSize() > 0) {
        plugin->setStateInformation(state.getData(), static_cast<int>(state.getSize()));
    }
}

juce::AudioProcessorEditor* PluginSlot::createEditor() {
    if (plugin && plugin->hasEditor()) {
        return plugin->createEditor();
    }
    return nullptr;
}

bool PluginSlot::hasEditor() const {
    return plugin && plugin->hasEditor();
}

} // namespace iDAW
