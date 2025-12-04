/**
 * TransportBar.cpp - Transport Control UI Implementation
 */

#include "TransportBar.h"
#include "../tracks/TrackList.h"

namespace iDAW {

// Simple SVG icon data
const char* TransportBar::playIconSvg = R"(<svg viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21" fill="currentColor"/></svg>)";
const char* TransportBar::pauseIconSvg = R"(<svg viewBox="0 0 24 24"><rect x="5" y="3" width="4" height="18" fill="currentColor"/><rect x="15" y="3" width="4" height="18" fill="currentColor"/></svg>)";
const char* TransportBar::stopIconSvg = R"(<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="currentColor"/></svg>)";
const char* TransportBar::recordIconSvg = R"(<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="currentColor"/></svg>)";
const char* TransportBar::rewindIconSvg = R"(<svg viewBox="0 0 24 24"><polygon points="11,12 1,3 1,21" fill="currentColor"/><polygon points="22,12 12,3 12,21" fill="currentColor"/></svg>)";
const char* TransportBar::loopIconSvg = R"(<svg viewBox="0 0 24 24"><path d="M12,4V1L8,5l4,4V6a6,6,0,0,1,6,6,5.87,5.87,0,0,1-.94,3.19l1.45,1.45A8,8,0,0,0,12,4Zm0,14a6,6,0,0,1-6-6,5.87,5.87,0,0,1,.94-3.19L5.49,7.36A8,8,0,0,0,12,20v3l4-4-4-4Z" fill="currentColor"/></svg>)";

TransportBar::TransportBar(TrackList& tracks)
    : trackList(tracks) {

    transportState.addListener(this);

    // Create transport buttons
    auto createButton = [this](const char* svg) -> std::unique_ptr<juce::DrawableButton> {
        auto btn = std::make_unique<juce::DrawableButton>("", juce::DrawableButton::ImageFitted);
        auto drawable = juce::Drawable::createFromSVG(*juce::parseXML(svg));
        if (drawable) {
            drawable->replaceColour(juce::Colours::black, juce::Colour(0xFF00D4FF));
            btn->setImages(drawable.get());
        }
        return btn;
    };

    rewindButton = createButton(rewindIconSvg);
    playButton = createButton(playIconSvg);
    stopButton = createButton(stopIconSvg);
    recordButton = createButton(recordIconSvg);
    loopButton = createButton(loopIconSvg);

    rewindButton->onClick = [this] { rewind(); };
    playButton->onClick = [this] { togglePlay(); };
    stopButton->onClick = [this] { stop(); };
    recordButton->onClick = [this] { toggleRecord(); };
    loopButton->onClick = [this] { toggleLoop(); };

    addAndMakeVisible(*rewindButton);
    addAndMakeVisible(*playButton);
    addAndMakeVisible(*stopButton);
    addAndMakeVisible(*recordButton);
    addAndMakeVisible(*loopButton);

    // Position display
    positionLabel = std::make_unique<juce::Label>();
    positionLabel->setFont(juce::Font(juce::Font::getDefaultMonospacedFontName(), 18, juce::Font::bold));
    positionLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF00D4FF));
    positionLabel->setJustificationType(juce::Justification::centred);
    positionLabel->setText("1.1.000", juce::dontSendNotification);
    addAndMakeVisible(*positionLabel);

    timecodeLabel = std::make_unique<juce::Label>();
    timecodeLabel->setFont(juce::Font(juce::Font::getDefaultMonospacedFontName(), 12, juce::Font::plain));
    timecodeLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF888888));
    timecodeLabel->setJustificationType(juce::Justification::centred);
    timecodeLabel->setText("00:00:00:00", juce::dontSendNotification);
    addAndMakeVisible(*timecodeLabel);

    // Tempo slider
    tempoSlider = std::make_unique<juce::Slider>(juce::Slider::LinearHorizontal, juce::Slider::TextBoxLeft);
    tempoSlider->setRange(20.0, 300.0, 0.1);
    tempoSlider->setValue(transportState.getTempo());
    tempoSlider->setTextBoxStyle(juce::Slider::TextBoxLeft, false, 55, 20);
    tempoSlider->setColour(juce::Slider::textBoxTextColourId, juce::Colour(0xFF00D4FF));
    tempoSlider->setColour(juce::Slider::trackColourId, juce::Colour(0xFF00D4FF));
    tempoSlider->onValueChange = [this] {
        transportState.setTempo(tempoSlider->getValue());
    };
    addAndMakeVisible(*tempoSlider);

    tempoLabel = std::make_unique<juce::Label>();
    tempoLabel->setText("BPM", juce::dontSendNotification);
    tempoLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF888888));
    addAndMakeVisible(*tempoLabel);

    // Tap tempo
    tapTempoButton = std::make_unique<juce::TextButton>("TAP");
    tapTempoButton->onClick = [this] { onTapTempo(); };
    addAndMakeVisible(*tapTempoButton);

    // Time signature
    timeSignatureCombo = std::make_unique<juce::ComboBox>();
    timeSignatureCombo->addItem("4/4", 1);
    timeSignatureCombo->addItem("3/4", 2);
    timeSignatureCombo->addItem("6/8", 3);
    timeSignatureCombo->addItem("2/4", 4);
    timeSignatureCombo->addItem("5/4", 5);
    timeSignatureCombo->addItem("7/8", 6);
    timeSignatureCombo->setSelectedId(1);
    timeSignatureCombo->onChange = [this] {
        switch (timeSignatureCombo->getSelectedId()) {
            case 1: transportState.setTimeSignature(4, 4); break;
            case 2: transportState.setTimeSignature(3, 4); break;
            case 3: transportState.setTimeSignature(6, 8); break;
            case 4: transportState.setTimeSignature(2, 4); break;
            case 5: transportState.setTimeSignature(5, 4); break;
            case 6: transportState.setTimeSignature(7, 8); break;
        }
    };
    addAndMakeVisible(*timeSignatureCombo);

    // CPU meter
    cpuLabel = std::make_unique<juce::Label>();
    cpuLabel->setText("CPU: 0%", juce::dontSendNotification);
    cpuLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF00FF88));
    cpuLabel->setFont(juce::Font(11));
    addAndMakeVisible(*cpuLabel);

    // Start timer for display updates
    startTimerHz(30);

    updateButtonStates();
}

TransportBar::~TransportBar() {
    transportState.removeListener(this);
}

void TransportBar::paint(juce::Graphics& g) {
    // Dark background with subtle gradient
    juce::ColourGradient gradient(
        juce::Colour(0xFF252540), 0, 0,
        juce::Colour(0xFF1A1A2E), 0, static_cast<float>(getHeight()),
        false
    );
    g.setGradientFill(gradient);
    g.fillAll();

    // Bottom border
    g.setColour(juce::Colour(0xFF00D4FF).withAlpha(0.3f));
    g.drawLine(0, getHeight() - 1.0f, getWidth(), getHeight() - 1.0f, 1.0f);

    // Section dividers
    g.setColour(juce::Colour(0xFF333355));
    g.drawVerticalLine(180, 5, getHeight() - 5);
    g.drawVerticalLine(380, 5, getHeight() - 5);
    g.drawVerticalLine(560, 5, getHeight() - 5);
}

void TransportBar::resized() {
    auto area = getLocalBounds().reduced(5);

    // Transport buttons (left section)
    auto buttonArea = area.removeFromLeft(170);
    int buttonSize = 36;
    int spacing = 4;

    rewindButton->setBounds(buttonArea.removeFromLeft(buttonSize).reduced(2));
    buttonArea.removeFromLeft(spacing);
    playButton->setBounds(buttonArea.removeFromLeft(buttonSize).reduced(2));
    buttonArea.removeFromLeft(spacing);
    stopButton->setBounds(buttonArea.removeFromLeft(buttonSize).reduced(2));
    buttonArea.removeFromLeft(spacing);
    recordButton->setBounds(buttonArea.removeFromLeft(buttonSize).reduced(2));

    area.removeFromLeft(15);

    // Position display
    auto posArea = area.removeFromLeft(150);
    positionLabel->setBounds(posArea.removeFromTop(25));
    timecodeLabel->setBounds(posArea);

    area.removeFromLeft(15);

    // Loop button
    loopButton->setBounds(area.removeFromLeft(36).reduced(2));

    area.removeFromLeft(15);

    // Tempo section
    auto tempoArea = area.removeFromLeft(180);
    tempoSlider->setBounds(tempoArea.removeFromLeft(130).reduced(0, 8));
    tempoLabel->setBounds(tempoArea.removeFromLeft(35).reduced(0, 12));

    // Tap tempo
    tapTempoButton->setBounds(area.removeFromLeft(50).reduced(2, 10));

    area.removeFromLeft(15);

    // Time signature
    timeSignatureCombo->setBounds(area.removeFromLeft(70).reduced(0, 10));

    // CPU meter (right side)
    cpuLabel->setBounds(area.removeFromRight(80).reduced(0, 12));
}

void TransportBar::timerCallback() {
    updatePositionDisplay();
}

void TransportBar::play() {
    transportState.play();
}

void TransportBar::stop() {
    transportState.stop();
}

void TransportBar::togglePlay() {
    if (transportState.isPlaying()) {
        transportState.pause();
    } else {
        transportState.play();
    }
}

void TransportBar::toggleRecord() {
    if (transportState.isRecording()) {
        transportState.stopRecording();
    } else {
        transportState.startRecording();
    }
}

void TransportBar::rewind() {
    transportState.setSamplePosition(0.0);
}

void TransportBar::fastForward() {
    // Skip forward by one bar
    auto pos = transportState.getPosition();
    transportState.setPositionToBar(pos.bar + 1);
}

void TransportBar::toggleLoop() {
    transportState.setLooping(!transportState.isLooping());
}

void TransportBar::updateButtonStates() {
    bool playing = transportState.isPlaying();
    bool recording = transportState.isRecording();
    bool looping = transportState.isLooping();

    // Update play button to show pause when playing
    auto drawable = juce::Drawable::createFromSVG(
        *juce::parseXML(playing ? pauseIconSvg : playIconSvg)
    );
    if (drawable) {
        drawable->replaceColour(juce::Colours::black, juce::Colour(0xFF00D4FF));
        playButton->setImages(drawable.get());
    }

    // Record button turns red when recording
    auto recordDrawable = juce::Drawable::createFromSVG(*juce::parseXML(recordIconSvg));
    if (recordDrawable) {
        recordDrawable->replaceColour(juce::Colours::black,
            recording ? juce::Colour(0xFFFF3344) : juce::Colour(0xFF00D4FF));
        recordButton->setImages(recordDrawable.get());
    }

    // Loop button highlight when active
    auto loopDrawable = juce::Drawable::createFromSVG(*juce::parseXML(loopIconSvg));
    if (loopDrawable) {
        loopDrawable->replaceColour(juce::Colours::black,
            looping ? juce::Colour(0xFFFFAA00) : juce::Colour(0xFF00D4FF));
        loopButton->setImages(loopDrawable.get());
    }
}

void TransportBar::updatePositionDisplay() {
    auto pos = transportState.getPosition();
    positionLabel->setText(pos.toString(), juce::dontSendNotification);
    timecodeLabel->setText(pos.toTimecode(transportState.getSampleRate()), juce::dontSendNotification);
}

void TransportBar::onTapTempo() {
    double now = juce::Time::getMillisecondCounterHiRes() / 1000.0;

    // Reset if more than 2 seconds since last tap
    if (now - lastTapTime > 2.0) {
        tapTimes.clear();
    }

    tapTimes.add(now);
    lastTapTime = now;

    // Keep only last 4 taps
    while (tapTimes.size() > 4) {
        tapTimes.remove(0);
    }

    // Calculate tempo from tap intervals
    if (tapTimes.size() >= 2) {
        double totalInterval = tapTimes.getLast() - tapTimes.getFirst();
        double avgInterval = totalInterval / (tapTimes.size() - 1);
        double bpm = 60.0 / avgInterval;
        bpm = juce::jlimit(20.0, 300.0, bpm);

        tempoSlider->setValue(bpm);
        transportState.setTempo(bpm);
    }
}

void TransportBar::transportStateChanged(TransportState::State newState) {
    juce::ignoreUnused(newState);
    juce::MessageManager::callAsync([this] {
        updateButtonStates();
    });
}

void TransportBar::tempoChanged(double newTempo) {
    juce::MessageManager::callAsync([this, newTempo] {
        tempoSlider->setValue(newTempo, juce::dontSendNotification);
    });
}

void TransportBar::positionChanged(double newPosition) {
    juce::ignoreUnused(newPosition);
    // Position updates handled by timer
}

void TransportBar::loopChanged(bool enabled, double start, double end) {
    juce::ignoreUnused(start, end);
    juce::MessageManager::callAsync([this, enabled] {
        juce::ignoreUnused(enabled);
        updateButtonStates();
    });
}

} // namespace iDAW
