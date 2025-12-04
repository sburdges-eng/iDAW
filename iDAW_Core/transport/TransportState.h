/**
 * TransportState.h - DAW Transport State Machine
 *
 * Manages playback state, tempo, time signature, and position.
 * Thread-safe for audio thread access.
 */

#pragma once

#include <JuceHeader.h>
#include <atomic>

namespace iDAW {

/**
 * @brief Time signature representation
 */
struct TimeSignature {
    int numerator = 4;
    int denominator = 4;

    bool operator==(const TimeSignature& other) const {
        return numerator == other.numerator && denominator == other.denominator;
    }
};

/**
 * @brief Position in project time
 */
struct PlayheadPosition {
    double samplePosition = 0.0;   ///< Current sample position
    double beatsPosition = 0.0;    ///< Position in beats
    int bar = 1;                   ///< Current bar number (1-indexed)
    int beat = 1;                  ///< Current beat within bar (1-indexed)
    double subBeat = 0.0;          ///< Fractional beat position

    /** Format as "BAR.BEAT.TICKS" */
    juce::String toString() const {
        int ticks = static_cast<int>(subBeat * 960);  // 960 PPQN
        return juce::String(bar) + "." +
               juce::String(beat) + "." +
               juce::String(ticks).paddedLeft('0', 3);
    }

    /** Format as "HH:MM:SS:FF" timecode */
    juce::String toTimecode(double sampleRate, int fps = 30) const {
        double seconds = samplePosition / sampleRate;
        int h = static_cast<int>(seconds / 3600);
        int m = static_cast<int>((seconds - h * 3600) / 60);
        int s = static_cast<int>(seconds) % 60;
        int f = static_cast<int>((seconds - static_cast<int>(seconds)) * fps);

        return juce::String(h).paddedLeft('0', 2) + ":" +
               juce::String(m).paddedLeft('0', 2) + ":" +
               juce::String(s).paddedLeft('0', 2) + ":" +
               juce::String(f).paddedLeft('0', 2);
    }
};

/**
 * @brief Transport state manager
 *
 * Thread-safe state management for DAW transport.
 */
class TransportState : public juce::ChangeBroadcaster {
public:
    TransportState();
    ~TransportState() override = default;

    //==========================================================================
    // Playback state
    //==========================================================================

    enum class State { Stopped, Playing, Recording, Paused };

    State getState() const { return state.load(); }
    bool isPlaying() const { return state.load() == State::Playing || state.load() == State::Recording; }
    bool isRecording() const { return state.load() == State::Recording; }
    bool isStopped() const { return state.load() == State::Stopped; }
    bool isPaused() const { return state.load() == State::Paused; }

    void play();
    void pause();
    void stop();
    void startRecording();
    void stopRecording();

    //==========================================================================
    // Position
    //==========================================================================

    double getSamplePosition() const { return samplePosition.load(); }
    void setSamplePosition(double position);

    PlayheadPosition getPosition() const;
    void setPositionInBeats(double beats);
    void setPositionToBar(int bar);

    //==========================================================================
    // Tempo and time signature
    //==========================================================================

    double getTempo() const { return tempo.load(); }
    void setTempo(double bpm);

    TimeSignature getTimeSignature() const;
    void setTimeSignature(int numerator, int denominator);

    double getSampleRate() const { return sampleRate.load(); }
    void setSampleRate(double rate);

    //==========================================================================
    // Loop
    //==========================================================================

    bool isLooping() const { return loopEnabled.load(); }
    void setLooping(bool enabled);

    double getLoopStartSamples() const { return loopStartSamples.load(); }
    double getLoopEndSamples() const { return loopEndSamples.load(); }
    void setLoopRange(double startSamples, double endSamples);
    void setLoopRangeInBeats(double startBeats, double endBeats);

    //==========================================================================
    // Conversion utilities
    //==========================================================================

    double beatsToSamples(double beats) const;
    double samplesToBeats(double samples) const;
    double barsToSamples(int bars) const;
    int samplesToBar(double samples) const;

    //==========================================================================
    // Audio processing
    //==========================================================================

    /** Advance position by given number of samples (call from audio thread) */
    void advancePosition(int numSamples) noexcept;

    /** Check if we need to loop (call from audio thread) */
    bool shouldLoop() const noexcept;

    /** Perform loop if needed, returns true if looped */
    bool performLoopIfNeeded() noexcept;

    //==========================================================================
    // Listeners
    //==========================================================================

    class Listener {
    public:
        virtual ~Listener() = default;
        virtual void transportStateChanged(State newState) {}
        virtual void tempoChanged(double newTempo) {}
        virtual void positionChanged(double newPosition) {}
        virtual void loopChanged(bool enabled, double start, double end) {}
    };

    void addListener(Listener* listener) { listeners.add(listener); }
    void removeListener(Listener* listener) { listeners.remove(listener); }

private:
    std::atomic<State> state{State::Stopped};
    std::atomic<double> samplePosition{0.0};
    std::atomic<double> tempo{120.0};
    std::atomic<double> sampleRate{44100.0};

    // Time signature (not atomic, protected by lock)
    TimeSignature timeSignature;
    mutable juce::SpinLock timeSignatureLock;

    // Loop
    std::atomic<bool> loopEnabled{false};
    std::atomic<double> loopStartSamples{0.0};
    std::atomic<double> loopEndSamples{0.0};

    juce::ListenerList<Listener> listeners;

    void notifyStateChanged();
    void notifyTempoChanged();
    void notifyPositionChanged();
    void notifyLoopChanged();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TransportState)
};

} // namespace iDAW
