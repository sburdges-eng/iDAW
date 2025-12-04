/**
 * Track.cpp - Track Implementation
 */

#include "Track.h"
#include "Clip.h"
#include "PluginSlot.h"

namespace iDAW {

//==============================================================================
// Track (base class)
//==============================================================================

Track::Track(TrackType type, const juce::String& name)
    : type(type), name(name), id(juce::Uuid()) {
}

void Track::setName(const juce::String& newName) {
    name = newName;
    sendChangeMessage();
}

void Track::setColour(juce::Colour c) {
    colour = c;
    sendChangeMessage();
}

void Track::setSolo(bool s) {
    solo = s;
    sendChangeMessage();
}

void Track::setMuted(bool m) {
    muted = m;
    sendChangeMessage();
}

void Track::setArmed(bool a) {
    armed = a;
    sendChangeMessage();
}

void Track::setVolume(float v) {
    volume = juce::jlimit(0.0f, 2.0f, v);
    sendChangeMessage();
}

float Track::getVolumeDb() const {
    return juce::Decibels::gainToDecibels(volume);
}

void Track::setVolumeDb(float db) {
    setVolume(juce::Decibels::decibelsToGain(db));
}

void Track::setPan(float p) {
    pan = juce::jlimit(-1.0f, 1.0f, p);
    sendChangeMessage();
}

void Track::setOutputBus(juce::Uuid busId) {
    outputBus = busId;
    sendChangeMessage();
}

PluginSlot* Track::getPluginSlot(int index) {
    if (index >= 0 && index < static_cast<int>(pluginSlots.size())) {
        return pluginSlots[index].get();
    }
    return nullptr;
}

void Track::addPluginSlot() {
    pluginSlots.push_back(std::make_unique<PluginSlot>());
    sendChangeMessage();
}

void Track::removePluginSlot(int index) {
    if (index >= 0 && index < static_cast<int>(pluginSlots.size())) {
        pluginSlots.erase(pluginSlots.begin() + index);
        sendChangeMessage();
    }
}

void Track::movePluginSlot(int fromIndex, int toIndex) {
    if (fromIndex >= 0 && fromIndex < static_cast<int>(pluginSlots.size()) &&
        toIndex >= 0 && toIndex < static_cast<int>(pluginSlots.size()) &&
        fromIndex != toIndex) {
        auto slot = std::move(pluginSlots[fromIndex]);
        pluginSlots.erase(pluginSlots.begin() + fromIndex);
        pluginSlots.insert(pluginSlots.begin() + toIndex, std::move(slot));
        sendChangeMessage();
    }
}

Clip* Track::getClip(int index) {
    if (index >= 0 && index < static_cast<int>(clips.size())) {
        return clips[index].get();
    }
    return nullptr;
}

void Track::addClip(std::unique_ptr<Clip> clip) {
    clips.push_back(std::move(clip));
    sendChangeMessage();
}

void Track::removeClip(int index) {
    if (index >= 0 && index < static_cast<int>(clips.size())) {
        clips.erase(clips.begin() + index);
        sendChangeMessage();
    }
}

Clip* Track::getClipAtPosition(double samplePosition) {
    for (auto& clip : clips) {
        if (clip->containsPosition(samplePosition)) {
            return clip.get();
        }
    }
    return nullptr;
}

float Track::getPeakLevel(int channel) const {
    if (channel >= 0 && channel < 2) {
        return peakLevels[channel].load();
    }
    return 0.0f;
}

void Track::resetPeaks() {
    peakLevels[0].store(0.0f);
    peakLevels[1].store(0.0f);
}

void Track::updatePeakLevels(const juce::AudioBuffer<float>& buffer) {
    for (int ch = 0; ch < juce::jmin(buffer.getNumChannels(), 2); ++ch) {
        float peak = buffer.getMagnitude(ch, 0, buffer.getNumSamples());
        float current = peakLevels[ch].load();
        if (peak > current) {
            peakLevels[ch].store(peak);
        } else {
            // Decay
            peakLevels[ch].store(current * 0.99f);
        }
    }
}

juce::var Track::toVar() const {
    auto obj = new juce::DynamicObject();
    obj->setProperty("type", static_cast<int>(type));
    obj->setProperty("name", name);
    obj->setProperty("colour", colour.toString());
    obj->setProperty("id", id.toString());
    obj->setProperty("solo", solo);
    obj->setProperty("muted", muted);
    obj->setProperty("armed", armed);
    obj->setProperty("volume", volume);
    obj->setProperty("pan", pan);
    obj->setProperty("outputBus", outputBus.toString());

    // Clips
    juce::Array<juce::var> clipArray;
    for (const auto& clip : clips) {
        clipArray.add(clip->toVar());
    }
    obj->setProperty("clips", clipArray);

    return juce::var(obj);
}

void Track::fromVar(const juce::var& data) {
    if (auto* obj = data.getDynamicObject()) {
        name = obj->getProperty("name").toString();
        colour = juce::Colour::fromString(obj->getProperty("colour").toString());
        id = juce::Uuid(obj->getProperty("id").toString());
        solo = obj->getProperty("solo");
        muted = obj->getProperty("muted");
        armed = obj->getProperty("armed");
        volume = static_cast<float>(obj->getProperty("volume"));
        pan = static_cast<float>(obj->getProperty("pan"));
        outputBus = juce::Uuid(obj->getProperty("outputBus").toString());

        // Clips
        clips.clear();
        if (auto* clipArray = obj->getProperty("clips").getArray()) {
            for (const auto& clipVar : *clipArray) {
                auto clip = std::make_unique<Clip>();
                clip->fromVar(clipVar);
                clips.push_back(std::move(clip));
            }
        }
    }
}

//==============================================================================
// AudioTrack
//==============================================================================

AudioTrack::AudioTrack(const juce::String& name)
    : Track(TrackType::Audio, name) {
}

void AudioTrack::prepareToPlay(double sampleRate, int samplesPerBlock) {
    currentSampleRate = sampleRate;
    currentBlockSize = samplesPerBlock;

    for (auto& slot : pluginSlots) {
        slot->prepareToPlay(sampleRate, samplesPerBlock);
    }
}

void AudioTrack::processBlock(juce::AudioBuffer<float>& buffer,
                               juce::MidiBuffer& midiMessages,
                               const TransportState& transport) {
    juce::ignoreUnused(midiMessages, transport);

    if (muted && !solo) {
        buffer.clear();
        return;
    }

    // Get audio from active clip at current position
    double position = transport.getSamplePosition();
    if (Clip* clip = getClipAtPosition(position)) {
        clip->getAudio(buffer, position, currentSampleRate);
    }

    // Process through plugin chain
    for (auto& slot : pluginSlots) {
        if (slot->isEnabled()) {
            slot->processBlock(buffer, midiMessages);
        }
    }

    // Apply volume and pan
    for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
        float gain = volume;
        if (ch == 0) gain *= (1.0f - juce::jmax(0.0f, pan));  // Left
        if (ch == 1) gain *= (1.0f + juce::jmin(0.0f, pan));  // Right
        buffer.applyGain(ch, 0, buffer.getNumSamples(), gain);
    }

    updatePeakLevels(buffer);
}

void AudioTrack::releaseResources() {
    for (auto& slot : pluginSlots) {
        slot->releaseResources();
    }
}

void AudioTrack::setInputType(InputType type) {
    inputType = type;
    sendChangeMessage();
}

void AudioTrack::setInputChannels(int left, int right) {
    inputChannelLeft = left;
    inputChannelRight = right;
    sendChangeMessage();
}

void AudioTrack::setMonitoringInput(bool monitor) {
    monitorInput = monitor;
    sendChangeMessage();
}

juce::var AudioTrack::toVar() const {
    auto base = Track::toVar();
    if (auto* obj = base.getDynamicObject()) {
        obj->setProperty("inputType", static_cast<int>(inputType));
        obj->setProperty("inputChannelLeft", inputChannelLeft);
        obj->setProperty("inputChannelRight", inputChannelRight);
        obj->setProperty("monitorInput", monitorInput);
    }
    return base;
}

void AudioTrack::fromVar(const juce::var& data) {
    Track::fromVar(data);
    if (auto* obj = data.getDynamicObject()) {
        inputType = static_cast<InputType>(static_cast<int>(obj->getProperty("inputType")));
        inputChannelLeft = obj->getProperty("inputChannelLeft");
        inputChannelRight = obj->getProperty("inputChannelRight");
        monitorInput = obj->getProperty("monitorInput");
    }
}

//==============================================================================
// MidiTrack
//==============================================================================

MidiTrack::MidiTrack(const juce::String& name)
    : Track(TrackType::Midi, name) {
}

void MidiTrack::prepareToPlay(double sampleRate, int samplesPerBlock) {
    currentSampleRate = sampleRate;
    currentBlockSize = samplesPerBlock;

    for (auto& slot : pluginSlots) {
        slot->prepareToPlay(sampleRate, samplesPerBlock);
    }
}

void MidiTrack::processBlock(juce::AudioBuffer<float>& buffer,
                              juce::MidiBuffer& midiMessages,
                              const TransportState& transport) {
    if (muted && !solo) {
        buffer.clear();
        midiMessages.clear();
        return;
    }

    // Get MIDI from active clip at current position
    double position = transport.getSamplePosition();
    if (Clip* clip = getClipAtPosition(position)) {
        clip->getMidi(midiMessages, position, currentBlockSize, currentSampleRate);
    }

    // Filter by MIDI channel if specified
    if (midiChannel > 0) {
        juce::MidiBuffer filtered;
        for (const auto& metadata : midiMessages) {
            auto msg = metadata.getMessage();
            if (msg.getChannel() == midiChannel || !msg.isForChannel(midiChannel)) {
                filtered.addEvent(msg, metadata.samplePosition);
            }
        }
        midiMessages.swapWith(filtered);
    }

    // Process through plugin chain (instruments and effects)
    for (auto& slot : pluginSlots) {
        if (slot->isEnabled()) {
            slot->processBlock(buffer, midiMessages);
        }
    }

    // Apply volume
    buffer.applyGain(volume);

    updatePeakLevels(buffer);
}

void MidiTrack::releaseResources() {
    for (auto& slot : pluginSlots) {
        slot->releaseResources();
    }
}

void MidiTrack::setMidiChannel(int channel) {
    midiChannel = juce::jlimit(0, 16, channel);
    sendChangeMessage();
}

juce::var MidiTrack::toVar() const {
    auto base = Track::toVar();
    if (auto* obj = base.getDynamicObject()) {
        obj->setProperty("midiChannel", midiChannel);
    }
    return base;
}

void MidiTrack::fromVar(const juce::var& data) {
    Track::fromVar(data);
    if (auto* obj = data.getDynamicObject()) {
        midiChannel = obj->getProperty("midiChannel");
    }
}

//==============================================================================
// GroupTrack
//==============================================================================

GroupTrack::GroupTrack(const juce::String& name)
    : Track(TrackType::Group, name) {
}

void GroupTrack::prepareToPlay(double sampleRate, int samplesPerBlock) {
    currentSampleRate = sampleRate;
    currentBlockSize = samplesPerBlock;

    for (auto& slot : pluginSlots) {
        slot->prepareToPlay(sampleRate, samplesPerBlock);
    }
}

void GroupTrack::processBlock(juce::AudioBuffer<float>& buffer,
                               juce::MidiBuffer& midiMessages,
                               const TransportState& transport) {
    juce::ignoreUnused(transport);

    if (muted && !solo) {
        buffer.clear();
        return;
    }

    // Group receives mixed audio from child tracks (handled by audio engine)
    // Process through plugin chain
    for (auto& slot : pluginSlots) {
        if (slot->isEnabled()) {
            slot->processBlock(buffer, midiMessages);
        }
    }

    // Apply volume and pan
    for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
        float gain = volume;
        if (ch == 0) gain *= (1.0f - juce::jmax(0.0f, pan));
        if (ch == 1) gain *= (1.0f + juce::jmin(0.0f, pan));
        buffer.applyGain(ch, 0, buffer.getNumSamples(), gain);
    }

    updatePeakLevels(buffer);
}

void GroupTrack::releaseResources() {
    for (auto& slot : pluginSlots) {
        slot->releaseResources();
    }
}

void GroupTrack::addChildTrack(juce::Uuid trackId) {
    if (!hasChildTrack(trackId)) {
        childTrackIds.push_back(trackId);
        sendChangeMessage();
    }
}

void GroupTrack::removeChildTrack(juce::Uuid trackId) {
    auto it = std::find(childTrackIds.begin(), childTrackIds.end(), trackId);
    if (it != childTrackIds.end()) {
        childTrackIds.erase(it);
        sendChangeMessage();
    }
}

bool GroupTrack::hasChildTrack(juce::Uuid trackId) const {
    return std::find(childTrackIds.begin(), childTrackIds.end(), trackId) != childTrackIds.end();
}

juce::var GroupTrack::toVar() const {
    auto base = Track::toVar();
    if (auto* obj = base.getDynamicObject()) {
        juce::Array<juce::var> children;
        for (const auto& id : childTrackIds) {
            children.add(id.toString());
        }
        obj->setProperty("childTracks", children);
    }
    return base;
}

void GroupTrack::fromVar(const juce::var& data) {
    Track::fromVar(data);
    if (auto* obj = data.getDynamicObject()) {
        childTrackIds.clear();
        if (auto* arr = obj->getProperty("childTracks").getArray()) {
            for (const auto& item : *arr) {
                childTrackIds.push_back(juce::Uuid(item.toString()));
            }
        }
    }
}

//==============================================================================
// MasterTrack
//==============================================================================

MasterTrack::MasterTrack()
    : Track(TrackType::Master, "Master") {
}

void MasterTrack::prepareToPlay(double sampleRate, int samplesPerBlock) {
    currentSampleRate = sampleRate;
    currentBlockSize = samplesPerBlock;

    for (auto& slot : pluginSlots) {
        slot->prepareToPlay(sampleRate, samplesPerBlock);
    }
}

void MasterTrack::processBlock(juce::AudioBuffer<float>& buffer,
                                juce::MidiBuffer& midiMessages,
                                const TransportState& transport) {
    juce::ignoreUnused(transport);

    // Master track receives summed audio from all tracks
    // Process through plugin chain
    for (auto& slot : pluginSlots) {
        if (slot->isEnabled()) {
            slot->processBlock(buffer, midiMessages);
        }
    }

    // Apply master volume
    buffer.applyGain(volume);

    updatePeakLevels(buffer);
}

void MasterTrack::releaseResources() {
    for (auto& slot : pluginSlots) {
        slot->releaseResources();
    }
}

juce::var MasterTrack::toVar() const {
    return Track::toVar();
}

void MasterTrack::fromVar(const juce::var& data) {
    Track::fromVar(data);
}

} // namespace iDAW
