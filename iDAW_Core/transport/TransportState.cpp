/**
 * TransportState.cpp - Transport State Implementation
 */

#include "TransportState.h"

namespace iDAW {

TransportState::TransportState() {
    timeSignature = {4, 4};
}

//==============================================================================
// Playback control
//==============================================================================

void TransportState::play() {
    auto prev = state.exchange(State::Playing);
    if (prev != State::Playing) {
        notifyStateChanged();
    }
}

void TransportState::pause() {
    auto prev = state.exchange(State::Paused);
    if (prev != State::Paused) {
        notifyStateChanged();
    }
}

void TransportState::stop() {
    state.store(State::Stopped);
    samplePosition.store(0.0);
    notifyStateChanged();
    notifyPositionChanged();
}

void TransportState::startRecording() {
    auto prev = state.exchange(State::Recording);
    if (prev != State::Recording) {
        notifyStateChanged();
    }
}

void TransportState::stopRecording() {
    if (state.load() == State::Recording) {
        state.store(State::Playing);
        notifyStateChanged();
    }
}

//==============================================================================
// Position
//==============================================================================

void TransportState::setSamplePosition(double position) {
    samplePosition.store(std::max(0.0, position));
    notifyPositionChanged();
}

PlayheadPosition TransportState::getPosition() const {
    PlayheadPosition pos;
    pos.samplePosition = samplePosition.load();

    double bpm = tempo.load();
    double sr = sampleRate.load();
    double samplesPerBeat = (sr * 60.0) / bpm;

    pos.beatsPosition = pos.samplePosition / samplesPerBeat;

    TimeSignature ts;
    {
        juce::SpinLock::ScopedLockType lock(timeSignatureLock);
        ts = timeSignature;
    }

    double beatsPerBar = static_cast<double>(ts.numerator);
    double totalBars = pos.beatsPosition / beatsPerBar;

    pos.bar = static_cast<int>(totalBars) + 1;
    double beatInBar = pos.beatsPosition - (pos.bar - 1) * beatsPerBar;
    pos.beat = static_cast<int>(beatInBar) + 1;
    pos.subBeat = beatInBar - static_cast<int>(beatInBar);

    return pos;
}

void TransportState::setPositionInBeats(double beats) {
    setSamplePosition(beatsToSamples(beats));
}

void TransportState::setPositionToBar(int bar) {
    TimeSignature ts;
    {
        juce::SpinLock::ScopedLockType lock(timeSignatureLock);
        ts = timeSignature;
    }

    double beatsPerBar = static_cast<double>(ts.numerator);
    double beats = (bar - 1) * beatsPerBar;
    setPositionInBeats(beats);
}

//==============================================================================
// Tempo and time signature
//==============================================================================

void TransportState::setTempo(double bpm) {
    bpm = juce::jlimit(20.0, 999.0, bpm);
    tempo.store(bpm);
    notifyTempoChanged();
}

TimeSignature TransportState::getTimeSignature() const {
    juce::SpinLock::ScopedLockType lock(timeSignatureLock);
    return timeSignature;
}

void TransportState::setTimeSignature(int numerator, int denominator) {
    juce::SpinLock::ScopedLockType lock(timeSignatureLock);
    timeSignature.numerator = juce::jlimit(1, 32, numerator);
    timeSignature.denominator = juce::jlimit(1, 32, denominator);
}

void TransportState::setSampleRate(double rate) {
    sampleRate.store(rate);
}

//==============================================================================
// Loop
//==============================================================================

void TransportState::setLooping(bool enabled) {
    loopEnabled.store(enabled);
    notifyLoopChanged();
}

void TransportState::setLoopRange(double startSamples, double endSamples) {
    loopStartSamples.store(std::max(0.0, startSamples));
    loopEndSamples.store(std::max(startSamples, endSamples));
    notifyLoopChanged();
}

void TransportState::setLoopRangeInBeats(double startBeats, double endBeats) {
    setLoopRange(beatsToSamples(startBeats), beatsToSamples(endBeats));
}

//==============================================================================
// Conversion utilities
//==============================================================================

double TransportState::beatsToSamples(double beats) const {
    double bpm = tempo.load();
    double sr = sampleRate.load();
    return beats * (sr * 60.0) / bpm;
}

double TransportState::samplesToBeats(double samples) const {
    double bpm = tempo.load();
    double sr = sampleRate.load();
    return samples * bpm / (sr * 60.0);
}

double TransportState::barsToSamples(int bars) const {
    TimeSignature ts;
    {
        juce::SpinLock::ScopedLockType lock(timeSignatureLock);
        ts = timeSignature;
    }

    double beatsPerBar = static_cast<double>(ts.numerator);
    return beatsToSamples(bars * beatsPerBar);
}

int TransportState::samplesToBar(double samples) const {
    TimeSignature ts;
    {
        juce::SpinLock::ScopedLockType lock(timeSignatureLock);
        ts = timeSignature;
    }

    double beatsPerBar = static_cast<double>(ts.numerator);
    double beats = samplesToBeats(samples);
    return static_cast<int>(beats / beatsPerBar) + 1;
}

//==============================================================================
// Audio processing
//==============================================================================

void TransportState::advancePosition(int numSamples) noexcept {
    if (isPlaying()) {
        samplePosition.fetch_add(static_cast<double>(numSamples));
    }
}

bool TransportState::shouldLoop() const noexcept {
    if (!loopEnabled.load()) return false;

    double pos = samplePosition.load();
    double end = loopEndSamples.load();

    return pos >= end;
}

bool TransportState::performLoopIfNeeded() noexcept {
    if (shouldLoop()) {
        samplePosition.store(loopStartSamples.load());
        return true;
    }
    return false;
}

//==============================================================================
// Notifications
//==============================================================================

void TransportState::notifyStateChanged() {
    sendChangeMessage();
    listeners.call([this](Listener& l) {
        l.transportStateChanged(state.load());
    });
}

void TransportState::notifyTempoChanged() {
    sendChangeMessage();
    listeners.call([this](Listener& l) {
        l.tempoChanged(tempo.load());
    });
}

void TransportState::notifyPositionChanged() {
    sendChangeMessage();
    listeners.call([this](Listener& l) {
        l.positionChanged(samplePosition.load());
    });
}

void TransportState::notifyLoopChanged() {
    sendChangeMessage();
    listeners.call([this](Listener& l) {
        l.loopChanged(loopEnabled.load(), loopStartSamples.load(), loopEndSamples.load());
    });
}

} // namespace iDAW
