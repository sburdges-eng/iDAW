/**
 * TransportBar.h - Transport Control UI
 *
 * Visual transport controls with:
 * - Play/Stop/Record buttons
 * - Position display (bars.beats.ticks and timecode)
 * - Tempo control with tap tempo
 * - Time signature selector
 * - Loop toggle and markers
 */

#pragma once

#include <JuceHeader.h>
#include "TransportState.h"

namespace iDAW {

class TrackList;

/**
 * @brief Transport control bar UI component
 */
class TransportBar : public juce::Component,
                     public juce::Timer,
                     public TransportState::Listener {
public:
    explicit TransportBar(TrackList& tracks);
    ~TransportBar() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

    //==========================================================================
    // Transport controls
    //==========================================================================

    void play();
    void stop();
    void togglePlay();
    void toggleRecord();
    void rewind();
    void fastForward();
    void toggleLoop();

    TransportState& getTransportState() { return transportState; }
    const TransportState& getTransportState() const { return transportState; }

    //==========================================================================
    // Timer callback for display updates
    //==========================================================================

    void timerCallback() override;

    //==========================================================================
    // TransportState::Listener
    //==========================================================================

    void transportStateChanged(TransportState::State newState) override;
    void tempoChanged(double newTempo) override;
    void positionChanged(double newPosition) override;
    void loopChanged(bool enabled, double start, double end) override;

private:
    TrackList& trackList;
    TransportState transportState;

    // Transport buttons
    std::unique_ptr<juce::DrawableButton> rewindButton;
    std::unique_ptr<juce::DrawableButton> playButton;
    std::unique_ptr<juce::DrawableButton> stopButton;
    std::unique_ptr<juce::DrawableButton> recordButton;
    std::unique_ptr<juce::DrawableButton> loopButton;

    // Position display
    std::unique_ptr<juce::Label> positionLabel;
    std::unique_ptr<juce::Label> timecodeLabel;

    // Tempo control
    std::unique_ptr<juce::Slider> tempoSlider;
    std::unique_ptr<juce::Label> tempoLabel;
    std::unique_ptr<juce::TextButton> tapTempoButton;

    // Time signature
    std::unique_ptr<juce::ComboBox> timeSignatureCombo;

    // CPU meter
    std::unique_ptr<juce::Label> cpuLabel;

    // Tap tempo state
    juce::Array<double> tapTimes;
    double lastTapTime = 0.0;

    void updateButtonStates();
    void updatePositionDisplay();
    void onTapTempo();

    juce::Drawable* createTransportIcon(const juce::String& svgData);

    // SVG icons
    static const char* playIconSvg;
    static const char* pauseIconSvg;
    static const char* stopIconSvg;
    static const char* recordIconSvg;
    static const char* rewindIconSvg;
    static const char* loopIconSvg;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TransportBar)
};

} // namespace iDAW
