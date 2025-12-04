/**
 * Clip.cpp - Clip Implementation
 */

#include "Clip.h"

namespace iDAW {

//==============================================================================
// Clip (base class)
//==============================================================================

Clip::Clip() = default;

void Clip::setStartPosition(double pos) {
    startPosition = std::max(0.0, pos);
}

void Clip::setLength(double len) {
    length = std::max(0.0, len);
}

void Clip::setOffset(double off) {
    offset = std::max(0.0, off);
}

bool Clip::containsPosition(double position) const {
    return position >= startPosition && position < getEndPosition();
}

void Clip::setName(const juce::String& n) {
    name = n;
}

void Clip::setColour(juce::Colour c) {
    colour = c;
}

void Clip::getAudio(juce::AudioBuffer<float>& buffer,
                    double playPosition,
                    double sampleRate) {
    juce::ignoreUnused(buffer, playPosition, sampleRate);
    // Base implementation does nothing
}

void Clip::getMidi(juce::MidiBuffer& buffer,
                   double playPosition,
                   int numSamples,
                   double sampleRate) {
    juce::ignoreUnused(buffer, playPosition, numSamples, sampleRate);
    // Base implementation does nothing
}

juce::var Clip::toVar() const {
    auto obj = new juce::DynamicObject();
    obj->setProperty("name", name);
    obj->setProperty("colour", colour.toString());
    obj->setProperty("startPosition", startPosition);
    obj->setProperty("length", length);
    obj->setProperty("offset", offset);
    return juce::var(obj);
}

void Clip::fromVar(const juce::var& data) {
    if (auto* obj = data.getDynamicObject()) {
        name = obj->getProperty("name").toString();
        colour = juce::Colour::fromString(obj->getProperty("colour").toString());
        startPosition = obj->getProperty("startPosition");
        length = obj->getProperty("length");
        offset = obj->getProperty("offset");
    }
}

//==============================================================================
// AudioClip
//==============================================================================

AudioClip::AudioClip() {
    formatManager = std::make_unique<juce::AudioFormatManager>();
    formatManager->registerBasicFormats();

    thumbnailCache = std::make_unique<juce::AudioThumbnailCache>(5);
    thumbnail = std::make_unique<juce::AudioThumbnail>(512, *formatManager, *thumbnailCache);
}

void AudioClip::setAudioFile(const juce::File& file) {
    audioFile = file;
    loadAudioFile();
}

void AudioClip::loadAudioFile() {
    if (!audioFile.existsAsFile()) return;

    auto* reader = formatManager->createReaderFor(audioFile);
    if (reader) {
        readerSource = std::make_unique<juce::AudioFormatReaderSource>(reader, true);
        length = static_cast<double>(reader->lengthInSamples);
        name = audioFile.getFileNameWithoutExtension();

        thumbnail->setSource(new juce::FileInputSource(audioFile));
    }
}

void AudioClip::getAudio(juce::AudioBuffer<float>& buffer,
                         double playPosition,
                         double sampleRate) {
    juce::ignoreUnused(sampleRate);

    if (!readerSource) return;
    if (!containsPosition(playPosition)) return;

    // Calculate position within clip
    double positionInClip = playPosition - startPosition + offset;
    readerSource->setNextReadPosition(static_cast<juce::int64>(positionInClip));

    // Read audio
    juce::AudioSourceChannelInfo info(&buffer, 0, buffer.getNumSamples());
    readerSource->getNextAudioBlock(info);
}

juce::var AudioClip::toVar() const {
    auto base = Clip::toVar();
    if (auto* obj = base.getDynamicObject()) {
        obj->setProperty("type", "audio");
        obj->setProperty("audioFile", audioFile.getFullPathName());
    }
    return base;
}

void AudioClip::fromVar(const juce::var& data) {
    Clip::fromVar(data);
    if (auto* obj = data.getDynamicObject()) {
        audioFile = juce::File(obj->getProperty("audioFile").toString());
        loadAudioFile();
    }
}

//==============================================================================
// MidiClip
//==============================================================================

MidiClip::MidiClip() = default;

void MidiClip::setMidiSequence(const juce::MidiMessageSequence& seq) {
    midiData = seq;
}

void MidiClip::getMidi(juce::MidiBuffer& buffer,
                       double playPosition,
                       int numSamples,
                       double sampleRate) {
    if (!containsPosition(playPosition)) return;

    // Calculate time range within clip
    double startTimeInClip = playPosition - startPosition + offset;
    double endTimeInClip = startTimeInClip + (numSamples / sampleRate * 1000.0);  // ms

    // Convert to seconds for MIDI sequence
    double startSec = startTimeInClip / sampleRate;
    double endSec = endTimeInClip / sampleRate;

    for (int i = 0; i < midiData.getNumEvents(); ++i) {
        auto* event = midiData.getEventPointer(i);
        double eventTime = event->message.getTimeStamp();

        if (eventTime >= startSec && eventTime < endSec) {
            int sampleOffset = static_cast<int>((eventTime - startSec) * sampleRate);
            buffer.addEvent(event->message, sampleOffset);
        }
    }
}

void MidiClip::addNote(int noteNumber, double startBeat, double lengthBeats,
                       float velocity, int channel) {
    // Convert beats to seconds (assuming 120 BPM for now, should use transport)
    double bpm = 120.0;
    double startSec = startBeat * 60.0 / bpm;
    double endSec = (startBeat + lengthBeats) * 60.0 / bpm;

    int vel = static_cast<int>(velocity * 127);

    midiData.addEvent(juce::MidiMessage::noteOn(channel, noteNumber, static_cast<juce::uint8>(vel)), startSec);
    midiData.addEvent(juce::MidiMessage::noteOff(channel, noteNumber), endSec);
    midiData.updateMatchedPairs();
}

void MidiClip::removeNote(int index) {
    if (index >= 0 && index < midiData.getNumEvents()) {
        // Find matching note off
        auto* noteOn = midiData.getEventPointer(index);
        if (noteOn && noteOn->message.isNoteOn() && noteOn->noteOffObject) {
            midiData.deleteEvent(midiData.getIndexOf(noteOn->noteOffObject), true);
        }
        midiData.deleteEvent(index, true);
    }
}

void MidiClip::clearNotes() {
    midiData.clear();
}

juce::var MidiClip::toVar() const {
    auto base = Clip::toVar();
    if (auto* obj = base.getDynamicObject()) {
        obj->setProperty("type", "midi");

        // Serialize MIDI data
        juce::Array<juce::var> events;
        for (int i = 0; i < midiData.getNumEvents(); ++i) {
            auto* event = midiData.getEventPointer(i);
            auto eventObj = new juce::DynamicObject();
            eventObj->setProperty("time", event->message.getTimeStamp());

            juce::MemoryBlock block;
            block.append(event->message.getRawData(), static_cast<size_t>(event->message.getRawDataSize()));
            eventObj->setProperty("data", block.toBase64Encoding());

            events.add(juce::var(eventObj));
        }
        obj->setProperty("midiEvents", events);
    }
    return base;
}

void MidiClip::fromVar(const juce::var& data) {
    Clip::fromVar(data);
    if (auto* obj = data.getDynamicObject()) {
        midiData.clear();

        if (auto* events = obj->getProperty("midiEvents").getArray()) {
            for (const auto& eventVar : *events) {
                if (auto* eventObj = eventVar.getDynamicObject()) {
                    double time = eventObj->getProperty("time");
                    juce::String dataStr = eventObj->getProperty("data").toString();

                    juce::MemoryBlock block;
                    block.fromBase64Encoding(dataStr);

                    auto msg = juce::MidiMessage(block.getData(), static_cast<int>(block.getSize()), time);
                    midiData.addEvent(msg);
                }
            }
            midiData.updateMatchedPairs();
        }
    }
}

} // namespace iDAW
