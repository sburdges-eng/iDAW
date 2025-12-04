/**
 * ArrangementView.h - Timeline and Track Lane View
 *
 * The main arrangement/timeline view with:
 * - Timeline ruler (bars/beats)
 * - Track lanes with clips
 * - Playhead indicator
 * - Selection and editing
 */

#pragma once

#include <JuceHeader.h>
#include "../tracks/TrackList.h"
#include "../transport/TransportState.h"
#include <memory>
#include <vector>

namespace iDAW {

class TransportBar;
class TrackLane;
class TimelineRuler;
class PlayheadComponent;

/**
 * @brief Main arrangement/timeline view
 */
class ArrangementView : public juce::Component,
                        public juce::ChangeListener,
                        public TrackList::Listener,
                        public TransportState::Listener {
public:
    ArrangementView(TrackList& tracks, TransportBar& transport);
    ~ArrangementView() override;

    void paint(juce::Graphics& g) override;
    void resized() override;
    void mouseDown(const juce::MouseEvent& e) override;
    void mouseDrag(const juce::MouseEvent& e) override;

    void projectChanged();

    // Zoom and scroll
    double getPixelsPerBeat() const { return pixelsPerBeat; }
    void setPixelsPerBeat(double ppb);
    void zoomIn();
    void zoomOut();

    double getScrollPosition() const;
    void setScrollPosition(double beats);

    // Time to pixel conversion
    int beatsToPixels(double beats) const;
    double pixelsToBeats(int pixels) const;

    // ChangeListener
    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

    // TrackList::Listener
    void trackAdded(Track* track, int index) override;
    void trackRemoved(int index) override;
    void trackMoved(int fromIndex, int toIndex) override;
    void selectionChanged(int newSelectedIndex) override;

    // TransportState::Listener
    void transportStateChanged(TransportState::State newState) override;
    void positionChanged(double newPosition) override;

private:
    TrackList& trackList;
    TransportBar& transportBar;

    double pixelsPerBeat = 40.0;
    int trackHeight = 80;

    // Components
    std::unique_ptr<TimelineRuler> timelineRuler;
    std::unique_ptr<juce::Viewport> trackViewport;
    std::unique_ptr<juce::Component> trackContainer;
    std::vector<std::unique_ptr<TrackLane>> trackLanes;
    std::unique_ptr<PlayheadComponent> playhead;

    // Track headers
    std::unique_ptr<juce::Viewport> headerViewport;
    std::unique_ptr<juce::Component> headerContainer;

    void rebuildTrackLanes();
    void updatePlayheadPosition();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ArrangementView)
};

/**
 * @brief Timeline ruler showing bars and beats
 */
class TimelineRuler : public juce::Component {
public:
    TimelineRuler(ArrangementView& view, TransportBar& transport);

    void paint(juce::Graphics& g) override;
    void mouseDown(const juce::MouseEvent& e) override;

private:
    ArrangementView& arrangementView;
    TransportBar& transportBar;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TimelineRuler)
};

/**
 * @brief Single track lane showing clips
 */
class TrackLane : public juce::Component,
                  public juce::ChangeListener {
public:
    TrackLane(Track& track, ArrangementView& view);
    ~TrackLane() override;

    void paint(juce::Graphics& g) override;
    void resized() override;
    void mouseDown(const juce::MouseEvent& e) override;
    void mouseDrag(const juce::MouseEvent& e) override;
    void mouseUp(const juce::MouseEvent& e) override;

    Track& getTrack() { return track; }

    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

private:
    Track& track;
    ArrangementView& arrangementView;

    void paintClips(juce::Graphics& g);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TrackLane)
};

/**
 * @brief Track header showing name, solo/mute, etc.
 */
class TrackHeader : public juce::Component {
public:
    TrackHeader(Track& track, TrackList& trackList);

    void paint(juce::Graphics& g) override;
    void resized() override;
    void mouseDown(const juce::MouseEvent& e) override;

private:
    Track& track;
    TrackList& trackList;

    std::unique_ptr<juce::Label> nameLabel;
    std::unique_ptr<juce::TextButton> soloButton;
    std::unique_ptr<juce::TextButton> muteButton;
    std::unique_ptr<juce::TextButton> armButton;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TrackHeader)
};

/**
 * @brief Playhead position indicator
 */
class PlayheadComponent : public juce::Component,
                          public juce::Timer {
public:
    PlayheadComponent(ArrangementView& view, TransportBar& transport);

    void paint(juce::Graphics& g) override;
    void timerCallback() override;

    void updatePosition();

private:
    ArrangementView& arrangementView;
    TransportBar& transportBar;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PlayheadComponent)
};

} // namespace iDAW
