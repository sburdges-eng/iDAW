/**
 * MixerPanel.h - DAW Mixer View
 *
 * Displays channel strips for all tracks with:
 * - Fader and pan
 * - Solo/Mute/Arm buttons
 * - VU meter
 * - Insert plugin slots
 * - Send knobs
 */

#pragma once

#include <JuceHeader.h>
#include "../tracks/TrackList.h"
#include <memory>
#include <vector>

namespace iDAW {

class ChannelStrip;

/**
 * @brief Main mixer panel containing channel strips
 */
class MixerPanel : public juce::Component,
                   public juce::ChangeListener,
                   public TrackList::Listener {
public:
    explicit MixerPanel(TrackList& tracks);
    ~MixerPanel() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

    void projectChanged();
    void updateChannelStrips();

    // ChangeListener (from TrackList)
    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

    // TrackList::Listener
    void trackAdded(Track* track, int index) override;
    void trackRemoved(int index) override;
    void trackMoved(int fromIndex, int toIndex) override;
    void selectionChanged(int newSelectedIndex) override;

private:
    TrackList& trackList;

    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> channelContainer;

    std::vector<std::unique_ptr<ChannelStrip>> channelStrips;
    std::unique_ptr<ChannelStrip> masterStrip;

    void rebuildChannelStrips();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MixerPanel)
};

/**
 * @brief Single channel strip in the mixer
 */
class ChannelStrip : public juce::Component,
                     public juce::ChangeListener {
public:
    ChannelStrip(Track& track, bool isMaster = false);
    ~ChannelStrip() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

    Track& getTrack() { return track; }

    void setSelected(bool selected);
    bool isSelected() const { return selected; }

    // ChangeListener (from Track)
    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

private:
    Track& track;
    bool isMaster;
    bool selected = false;

    // Header
    std::unique_ptr<juce::Label> nameLabel;
    std::unique_ptr<juce::TextButton> colourButton;

    // Solo/Mute/Arm
    std::unique_ptr<juce::TextButton> soloButton;
    std::unique_ptr<juce::TextButton> muteButton;
    std::unique_ptr<juce::TextButton> armButton;

    // Fader and pan
    std::unique_ptr<juce::Slider> fader;
    std::unique_ptr<juce::Slider> panKnob;
    std::unique_ptr<juce::Label> dbLabel;

    // Meter
    class MeterComponent;
    std::unique_ptr<MeterComponent> meter;

    // Plugin slots (simplified view)
    std::unique_ptr<juce::TextButton> insertButton;

    void updateFromTrack();
    void setupComponents();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ChannelStrip)
};

/**
 * @brief VU Meter component for channel strips
 */
class ChannelStrip::MeterComponent : public juce::Component,
                                      public juce::Timer {
public:
    explicit MeterComponent(Track& t);

    void paint(juce::Graphics& g) override;
    void timerCallback() override;

private:
    Track& track;
    float leftLevel = 0.0f;
    float rightLevel = 0.0f;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MeterComponent)
};

} // namespace iDAW
