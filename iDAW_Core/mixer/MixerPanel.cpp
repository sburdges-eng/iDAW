/**
 * MixerPanel.cpp - Mixer Implementation
 */

#include "MixerPanel.h"
#include "ChannelStrip.h"

namespace iDAW {

//==============================================================================
// MixerPanel
//==============================================================================

MixerPanel::MixerPanel(TrackList& tracks)
    : trackList(tracks) {

    trackList.addChangeListener(this);
    trackList.addListener(this);

    viewport = std::make_unique<juce::Viewport>();
    channelContainer = std::make_unique<juce::Component>();

    viewport->setViewedComponent(channelContainer.get(), false);
    viewport->setScrollBarsShown(false, true);
    addAndMakeVisible(*viewport);

    // Master strip
    masterStrip = std::make_unique<ChannelStrip>(*trackList.getMasterTrack(), true);
    addAndMakeVisible(*masterStrip);

    rebuildChannelStrips();
}

MixerPanel::~MixerPanel() {
    trackList.removeChangeListener(this);
    trackList.removeListener(this);
}

void MixerPanel::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF1A1A2E));

    // Border
    g.setColour(juce::Colour(0xFF333355));
    g.drawRect(getLocalBounds(), 1);

    // Separator before master
    int masterX = getWidth() - 100;
    g.setColour(juce::Colour(0xFF00D4FF).withAlpha(0.3f));
    g.drawVerticalLine(masterX - 5, 0.0f, static_cast<float>(getHeight()));
}

void MixerPanel::resized() {
    auto area = getLocalBounds();

    // Master strip on the right
    int masterWidth = 90;
    masterStrip->setBounds(area.removeFromRight(masterWidth).reduced(2));

    area.removeFromRight(10);  // Separator space

    // Viewport for channel strips
    viewport->setBounds(area);

    // Calculate container width
    int stripWidth = 80;
    int numStrips = static_cast<int>(channelStrips.size());
    int containerWidth = juce::jmax(area.getWidth(), numStrips * stripWidth);

    channelContainer->setSize(containerWidth, area.getHeight());

    // Layout channel strips
    int x = 0;
    for (auto& strip : channelStrips) {
        strip->setBounds(x, 0, stripWidth, area.getHeight());
        x += stripWidth;
    }
}

void MixerPanel::projectChanged() {
    rebuildChannelStrips();
}

void MixerPanel::updateChannelStrips() {
    for (auto& strip : channelStrips) {
        strip->repaint();
    }
    masterStrip->repaint();
}

void MixerPanel::rebuildChannelStrips() {
    channelStrips.clear();

    for (int i = 0; i < trackList.getNumTracks(); ++i) {
        auto* track = trackList.getTrack(i);
        auto strip = std::make_unique<ChannelStrip>(*track);
        strip->setSelected(i == trackList.getSelectedTrackIndex());
        channelContainer->addAndMakeVisible(*strip);
        channelStrips.push_back(std::move(strip));
    }

    resized();
}

void MixerPanel::changeListenerCallback(juce::ChangeBroadcaster* source) {
    juce::ignoreUnused(source);
    updateChannelStrips();
}

void MixerPanel::trackAdded(Track* track, int index) {
    juce::ignoreUnused(track, index);
    rebuildChannelStrips();
}

void MixerPanel::trackRemoved(int index) {
    juce::ignoreUnused(index);
    rebuildChannelStrips();
}

void MixerPanel::trackMoved(int fromIndex, int toIndex) {
    juce::ignoreUnused(fromIndex, toIndex);
    rebuildChannelStrips();
}

void MixerPanel::selectionChanged(int newSelectedIndex) {
    for (int i = 0; i < static_cast<int>(channelStrips.size()); ++i) {
        channelStrips[i]->setSelected(i == newSelectedIndex);
    }
}

//==============================================================================
// ChannelStrip
//==============================================================================

ChannelStrip::ChannelStrip(Track& t, bool master)
    : track(t), isMaster(master) {

    track.addChangeListener(this);
    setupComponents();
    updateFromTrack();
}

ChannelStrip::~ChannelStrip() {
    track.removeChangeListener(this);
}

void ChannelStrip::setupComponents() {
    // Name label
    nameLabel = std::make_unique<juce::Label>();
    nameLabel->setFont(juce::Font(11));
    nameLabel->setJustificationType(juce::Justification::centred);
    nameLabel->setColour(juce::Label::textColourId, juce::Colours::white);
    nameLabel->setEditable(true);
    nameLabel->onTextChange = [this] {
        track.setName(nameLabel->getText());
    };
    addAndMakeVisible(*nameLabel);

    // Solo/Mute/Arm buttons
    if (!isMaster) {
        soloButton = std::make_unique<juce::TextButton>("S");
        soloButton->setClickingTogglesState(true);
        soloButton->onClick = [this] {
            track.setSolo(soloButton->getToggleState());
        };
        addAndMakeVisible(*soloButton);

        muteButton = std::make_unique<juce::TextButton>("M");
        muteButton->setClickingTogglesState(true);
        muteButton->onClick = [this] {
            track.setMuted(muteButton->getToggleState());
        };
        addAndMakeVisible(*muteButton);

        if (track.getType() == TrackType::Audio || track.getType() == TrackType::Midi) {
            armButton = std::make_unique<juce::TextButton>("R");
            armButton->setClickingTogglesState(true);
            armButton->onClick = [this] {
                track.setArmed(armButton->getToggleState());
            };
            addAndMakeVisible(*armButton);
        }
    }

    // Pan knob (not on master)
    if (!isMaster) {
        panKnob = std::make_unique<juce::Slider>(juce::Slider::RotaryHorizontalVerticalDrag,
                                                  juce::Slider::NoTextBox);
        panKnob->setRange(-1.0, 1.0, 0.01);
        panKnob->setValue(0.0);
        panKnob->onValueChange = [this] {
            track.setPan(static_cast<float>(panKnob->getValue()));
        };
        addAndMakeVisible(*panKnob);
    }

    // Meter
    meter = std::make_unique<MeterComponent>(track);
    addAndMakeVisible(*meter);

    // Fader
    fader = std::make_unique<juce::Slider>(juce::Slider::LinearVertical,
                                           juce::Slider::NoTextBox);
    fader->setRange(0.0, 2.0, 0.001);
    fader->setSkewFactorFromMidPoint(1.0);
    fader->setValue(1.0);
    fader->onValueChange = [this] {
        track.setVolume(static_cast<float>(fader->getValue()));
    };
    addAndMakeVisible(*fader);

    // dB label
    dbLabel = std::make_unique<juce::Label>();
    dbLabel->setFont(juce::Font(10));
    dbLabel->setJustificationType(juce::Justification::centred);
    dbLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF888888));
    addAndMakeVisible(*dbLabel);

    // Plugin insert button
    insertButton = std::make_unique<juce::TextButton>("+");
    insertButton->onClick = [this] {
        // TODO: Open plugin browser
    };
    addAndMakeVisible(*insertButton);
}

void ChannelStrip::paint(juce::Graphics& g) {
    // Background
    juce::Colour bgColour = selected ? juce::Colour(0xFF2A2A4E) : juce::Colour(0xFF202038);
    g.fillAll(bgColour);

    // Border
    g.setColour(selected ? juce::Colour(0xFF00D4FF) : juce::Colour(0xFF333355));
    g.drawRect(getLocalBounds(), 1);

    // Track type indicator
    juce::Colour typeColour = track.getColour();
    g.setColour(typeColour);
    g.fillRect(0, 0, getWidth(), 3);
}

void ChannelStrip::resized() {
    auto area = getLocalBounds().reduced(4);

    // Name at top
    nameLabel->setBounds(area.removeFromTop(20));

    // Plugin insert button
    insertButton->setBounds(area.removeFromTop(20).reduced(2));

    area.removeFromTop(5);

    // Solo/Mute/Arm buttons
    if (!isMaster) {
        auto buttonArea = area.removeFromTop(22);
        int buttonWidth = buttonArea.getWidth() / 3;

        if (soloButton) soloButton->setBounds(buttonArea.removeFromLeft(buttonWidth).reduced(1));
        if (muteButton) muteButton->setBounds(buttonArea.removeFromLeft(buttonWidth).reduced(1));
        if (armButton) armButton->setBounds(buttonArea.reduced(1));
    }

    area.removeFromTop(5);

    // Pan knob
    if (panKnob) {
        panKnob->setBounds(area.removeFromTop(40).reduced(5));
    }

    // dB label at bottom
    dbLabel->setBounds(area.removeFromBottom(15));

    // Meter and fader share remaining space
    int meterWidth = 12;
    int faderWidth = area.getWidth() - meterWidth - 5;

    meter->setBounds(area.removeFromLeft(meterWidth));
    area.removeFromLeft(5);
    fader->setBounds(area);
}

void ChannelStrip::setSelected(bool sel) {
    if (selected != sel) {
        selected = sel;
        repaint();
    }
}

void ChannelStrip::updateFromTrack() {
    nameLabel->setText(track.getName(), juce::dontSendNotification);

    if (soloButton) soloButton->setToggleState(track.isSolo(), juce::dontSendNotification);
    if (muteButton) muteButton->setToggleState(track.isMuted(), juce::dontSendNotification);
    if (armButton) armButton->setToggleState(track.isArmed(), juce::dontSendNotification);

    if (panKnob) panKnob->setValue(track.getPan(), juce::dontSendNotification);
    fader->setValue(track.getVolume(), juce::dontSendNotification);

    float db = track.getVolumeDb();
    if (db < -60.0f) {
        dbLabel->setText("-inf", juce::dontSendNotification);
    } else {
        dbLabel->setText(juce::String(db, 1) + " dB", juce::dontSendNotification);
    }

    // Update button colours
    if (soloButton) {
        soloButton->setColour(juce::TextButton::buttonOnColourId, juce::Colour(0xFFFFCC00));
    }
    if (muteButton) {
        muteButton->setColour(juce::TextButton::buttonOnColourId, juce::Colour(0xFFFF4444));
    }
    if (armButton) {
        armButton->setColour(juce::TextButton::buttonOnColourId, juce::Colour(0xFFFF0000));
    }
}

void ChannelStrip::changeListenerCallback(juce::ChangeBroadcaster* source) {
    juce::ignoreUnused(source);
    updateFromTrack();
}

//==============================================================================
// MeterComponent
//==============================================================================

ChannelStrip::MeterComponent::MeterComponent(Track& t) : track(t) {
    startTimerHz(30);
}

void ChannelStrip::MeterComponent::paint(juce::Graphics& g) {
    auto area = getLocalBounds();
    int halfWidth = area.getWidth() / 2;

    // Background
    g.setColour(juce::Colour(0xFF111122));
    g.fillRect(area);

    // Left channel
    auto leftArea = area.removeFromLeft(halfWidth - 1);
    float leftHeight = leftLevel * leftArea.getHeight();
    g.setColour(leftLevel > 0.9f ? juce::Colour(0xFFFF4444) :
                leftLevel > 0.7f ? juce::Colour(0xFFFFCC00) :
                juce::Colour(0xFF00FF88));
    g.fillRect(leftArea.getX(),
              leftArea.getBottom() - static_cast<int>(leftHeight),
              leftArea.getWidth(),
              static_cast<int>(leftHeight));

    // Right channel
    area.removeFromLeft(2);  // Gap
    float rightHeight = rightLevel * area.getHeight();
    g.setColour(rightLevel > 0.9f ? juce::Colour(0xFFFF4444) :
                rightLevel > 0.7f ? juce::Colour(0xFFFFCC00) :
                juce::Colour(0xFF00FF88));
    g.fillRect(area.getX(),
              area.getBottom() - static_cast<int>(rightHeight),
              area.getWidth(),
              static_cast<int>(rightHeight));
}

void ChannelStrip::MeterComponent::timerCallback() {
    leftLevel = track.getPeakLevel(0);
    rightLevel = track.getPeakLevel(1);
    repaint();
}

} // namespace iDAW
