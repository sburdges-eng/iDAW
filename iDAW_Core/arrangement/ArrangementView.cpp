/**
 * ArrangementView.cpp - Arrangement View Implementation
 */

#include "ArrangementView.h"
#include "../transport/TransportBar.h"
#include "../tracks/Clip.h"

namespace iDAW {

//==============================================================================
// ArrangementView
//==============================================================================

ArrangementView::ArrangementView(TrackList& tracks, TransportBar& transport)
    : trackList(tracks), transportBar(transport) {

    trackList.addChangeListener(this);
    trackList.addListener(this);
    transportBar.getTransportState().addListener(this);

    // Timeline ruler
    timelineRuler = std::make_unique<TimelineRuler>(*this, transportBar);
    addAndMakeVisible(*timelineRuler);

    // Track headers viewport
    headerViewport = std::make_unique<juce::Viewport>();
    headerContainer = std::make_unique<juce::Component>();
    headerViewport->setViewedComponent(headerContainer.get(), false);
    headerViewport->setScrollBarsShown(false, false);
    addAndMakeVisible(*headerViewport);

    // Track lanes viewport
    trackViewport = std::make_unique<juce::Viewport>();
    trackContainer = std::make_unique<juce::Component>();
    trackViewport->setViewedComponent(trackContainer.get(), false);
    trackViewport->setScrollBarsShown(true, true);
    addAndMakeVisible(*trackViewport);

    // Sync scroll between headers and track lanes
    trackViewport->getVerticalScrollBar().addListener([this](juce::ScrollBar& bar, double newValue) {
        juce::ignoreUnused(bar, newValue);
        headerViewport->setViewPosition(0, trackViewport->getViewPositionY());
    });

    // Playhead
    playhead = std::make_unique<PlayheadComponent>(*this, transportBar);
    addAndMakeVisible(*playhead);

    rebuildTrackLanes();
}

ArrangementView::~ArrangementView() {
    trackList.removeChangeListener(this);
    trackList.removeListener(this);
    transportBar.getTransportState().removeListener(this);
}

void ArrangementView::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF1A1A2E));
}

void ArrangementView::resized() {
    auto area = getLocalBounds();

    int rulerHeight = 30;
    int headerWidth = 150;

    // Timeline ruler (top, spans headers + tracks)
    timelineRuler->setBounds(area.removeFromTop(rulerHeight));

    // Headers (left side)
    auto headerArea = area.removeFromLeft(headerWidth);
    headerViewport->setBounds(headerArea);

    // Track lanes (right side)
    trackViewport->setBounds(area);

    // Calculate content sizes
    int numTracks = trackList.getNumTracks();
    int contentHeight = juce::jmax(area.getHeight(), numTracks * trackHeight);
    int contentWidth = beatsToPixels(200);  // 200 beats visible width

    headerContainer->setSize(headerWidth, contentHeight);
    trackContainer->setSize(contentWidth, contentHeight);

    // Layout track lanes
    int y = 0;
    for (auto& lane : trackLanes) {
        lane->setBounds(0, y, contentWidth, trackHeight);
        y += trackHeight;
    }

    // Playhead spans timeline + tracks
    playhead->setBounds(headerWidth, 0, area.getWidth(), area.getHeight() + rulerHeight);
    playhead->toFront(false);
}

void ArrangementView::mouseDown(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
}

void ArrangementView::mouseDrag(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
}

void ArrangementView::projectChanged() {
    rebuildTrackLanes();
}

void ArrangementView::setPixelsPerBeat(double ppb) {
    pixelsPerBeat = juce::jlimit(5.0, 200.0, ppb);
    resized();
    repaint();
}

void ArrangementView::zoomIn() {
    setPixelsPerBeat(pixelsPerBeat * 1.5);
}

void ArrangementView::zoomOut() {
    setPixelsPerBeat(pixelsPerBeat / 1.5);
}

double ArrangementView::getScrollPosition() const {
    return pixelsToBeats(trackViewport->getViewPositionX());
}

void ArrangementView::setScrollPosition(double beats) {
    trackViewport->setViewPosition(beatsToPixels(beats), trackViewport->getViewPositionY());
}

int ArrangementView::beatsToPixels(double beats) const {
    return static_cast<int>(beats * pixelsPerBeat);
}

double ArrangementView::pixelsToBeats(int pixels) const {
    return static_cast<double>(pixels) / pixelsPerBeat;
}

void ArrangementView::rebuildTrackLanes() {
    trackLanes.clear();

    for (int i = 0; i < trackList.getNumTracks(); ++i) {
        auto* track = trackList.getTrack(i);
        auto lane = std::make_unique<TrackLane>(*track, *this);
        trackContainer->addAndMakeVisible(*lane);
        trackLanes.push_back(std::move(lane));
    }

    resized();
}

void ArrangementView::updatePlayheadPosition() {
    playhead->updatePosition();
}

void ArrangementView::changeListenerCallback(juce::ChangeBroadcaster* source) {
    juce::ignoreUnused(source);
    repaint();
}

void ArrangementView::trackAdded(Track* track, int index) {
    juce::ignoreUnused(track, index);
    rebuildTrackLanes();
}

void ArrangementView::trackRemoved(int index) {
    juce::ignoreUnused(index);
    rebuildTrackLanes();
}

void ArrangementView::trackMoved(int fromIndex, int toIndex) {
    juce::ignoreUnused(fromIndex, toIndex);
    rebuildTrackLanes();
}

void ArrangementView::selectionChanged(int newSelectedIndex) {
    juce::ignoreUnused(newSelectedIndex);
    repaint();
}

void ArrangementView::transportStateChanged(TransportState::State newState) {
    juce::ignoreUnused(newState);
}

void ArrangementView::positionChanged(double newPosition) {
    juce::ignoreUnused(newPosition);
    updatePlayheadPosition();
}

//==============================================================================
// TimelineRuler
//==============================================================================

TimelineRuler::TimelineRuler(ArrangementView& view, TransportBar& transport)
    : arrangementView(view), transportBar(transport) {
}

void TimelineRuler::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF252540));

    auto& transport = transportBar.getTransportState();
    auto ts = transport.getTimeSignature();

    double ppb = arrangementView.getPixelsPerBeat();
    int headerWidth = 150;

    // Draw bar lines and numbers
    g.setFont(juce::Font(10));

    for (int bar = 1; bar < 100; ++bar) {
        double beat = (bar - 1) * ts.numerator;
        int x = headerWidth + arrangementView.beatsToPixels(beat);

        if (x > getWidth()) break;

        // Bar line
        g.setColour(juce::Colour(0xFF00D4FF).withAlpha(0.5f));
        g.drawVerticalLine(x, 0.0f, static_cast<float>(getHeight()));

        // Bar number
        g.setColour(juce::Colour(0xFF00D4FF));
        g.drawText(juce::String(bar), x + 2, 2, 30, 12, juce::Justification::left);

        // Beat lines
        if (ppb > 15) {
            g.setColour(juce::Colour(0xFF333355));
            for (int b = 1; b < ts.numerator; ++b) {
                int beatX = headerWidth + arrangementView.beatsToPixels(beat + b);
                g.drawVerticalLine(beatX, 15.0f, static_cast<float>(getHeight()));
            }
        }
    }

    // Bottom border
    g.setColour(juce::Colour(0xFF00D4FF).withAlpha(0.3f));
    g.drawHorizontalLine(getHeight() - 1, 0.0f, static_cast<float>(getWidth()));
}

void TimelineRuler::mouseDown(const juce::MouseEvent& e) {
    int headerWidth = 150;
    if (e.x > headerWidth) {
        double beats = arrangementView.pixelsToBeats(e.x - headerWidth);
        transportBar.getTransportState().setPositionInBeats(beats);
    }
}

//==============================================================================
// TrackLane
//==============================================================================

TrackLane::TrackLane(Track& t, ArrangementView& view)
    : track(t), arrangementView(view) {

    track.addChangeListener(this);
}

TrackLane::~TrackLane() {
    track.removeChangeListener(this);
}

void TrackLane::paint(juce::Graphics& g) {
    // Background
    bool selected = track.getIndex() == 0; // Simplified
    g.fillAll(selected ? juce::Colour(0xFF2A2A4E) : juce::Colour(0xFF1E1E38));

    // Track colour strip
    g.setColour(track.getColour());
    g.fillRect(0, 0, 3, getHeight());

    // Grid lines (beats)
    double ppb = arrangementView.getPixelsPerBeat();
    if (ppb > 15) {
        g.setColour(juce::Colour(0xFF333344));
        for (int beat = 0; beat < 200; ++beat) {
            int x = arrangementView.beatsToPixels(beat);
            if (x > getWidth()) break;
            g.drawVerticalLine(x, 0.0f, static_cast<float>(getHeight()));
        }
    }

    // Draw clips
    paintClips(g);

    // Bottom border
    g.setColour(juce::Colour(0xFF333355));
    g.drawHorizontalLine(getHeight() - 1, 0.0f, static_cast<float>(getWidth()));
}

void TrackLane::paintClips(juce::Graphics& g) {
    for (int i = 0; i < track.getNumClips(); ++i) {
        auto* clip = track.getClip(i);

        // Convert clip position to pixels
        // Note: clip positions are in samples, need to convert via transport
        // For now, simplified version assuming 44100 sample rate, 120 BPM
        double sampleRate = 44100.0;
        double bpm = 120.0;
        double samplesPerBeat = sampleRate * 60.0 / bpm;

        double startBeat = clip->getStartPosition() / samplesPerBeat;
        double lengthBeats = clip->getLength() / samplesPerBeat;

        int x = arrangementView.beatsToPixels(startBeat);
        int width = arrangementView.beatsToPixels(lengthBeats);
        int height = getHeight() - 10;

        // Clip background
        g.setColour(clip->getColour().withAlpha(0.7f));
        g.fillRoundedRectangle(static_cast<float>(x), 5.0f,
                               static_cast<float>(width), static_cast<float>(height), 4.0f);

        // Clip border
        g.setColour(clip->getColour());
        g.drawRoundedRectangle(static_cast<float>(x), 5.0f,
                               static_cast<float>(width), static_cast<float>(height), 4.0f, 1.0f);

        // Clip name
        g.setColour(juce::Colours::white);
        g.setFont(juce::Font(11));
        g.drawText(clip->getName(), x + 4, 7, width - 8, 16, juce::Justification::left, true);
    }
}

void TrackLane::resized() {
}

void TrackLane::mouseDown(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
}

void TrackLane::mouseDrag(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
}

void TrackLane::mouseUp(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
}

void TrackLane::changeListenerCallback(juce::ChangeBroadcaster* source) {
    juce::ignoreUnused(source);
    repaint();
}

//==============================================================================
// TrackHeader
//==============================================================================

TrackHeader::TrackHeader(Track& t, TrackList& tl)
    : track(t), trackList(tl) {

    nameLabel = std::make_unique<juce::Label>();
    nameLabel->setText(track.getName(), juce::dontSendNotification);
    nameLabel->setColour(juce::Label::textColourId, juce::Colours::white);
    nameLabel->setEditable(true);
    addAndMakeVisible(*nameLabel);

    soloButton = std::make_unique<juce::TextButton>("S");
    soloButton->setClickingTogglesState(true);
    addAndMakeVisible(*soloButton);

    muteButton = std::make_unique<juce::TextButton>("M");
    muteButton->setClickingTogglesState(true);
    addAndMakeVisible(*muteButton);

    armButton = std::make_unique<juce::TextButton>("R");
    armButton->setClickingTogglesState(true);
    addAndMakeVisible(*armButton);
}

void TrackHeader::paint(juce::Graphics& g) {
    bool selected = trackList.getSelectedTrackIndex() == track.getIndex();
    g.fillAll(selected ? juce::Colour(0xFF2A2A4E) : juce::Colour(0xFF202038));

    g.setColour(track.getColour());
    g.fillRect(0, 0, 4, getHeight());

    g.setColour(juce::Colour(0xFF333355));
    g.drawRect(getLocalBounds(), 1);
}

void TrackHeader::resized() {
    auto area = getLocalBounds().reduced(5);
    area.removeFromLeft(5);

    nameLabel->setBounds(area.removeFromTop(20));

    auto buttonArea = area.removeFromTop(22);
    int buttonWidth = buttonArea.getWidth() / 3;
    soloButton->setBounds(buttonArea.removeFromLeft(buttonWidth).reduced(1));
    muteButton->setBounds(buttonArea.removeFromLeft(buttonWidth).reduced(1));
    armButton->setBounds(buttonArea.reduced(1));
}

void TrackHeader::mouseDown(const juce::MouseEvent& e) {
    juce::ignoreUnused(e);
    trackList.setSelectedTrackIndex(track.getIndex());
}

//==============================================================================
// PlayheadComponent
//==============================================================================

PlayheadComponent::PlayheadComponent(ArrangementView& view, TransportBar& transport)
    : arrangementView(view), transportBar(transport) {

    setInterceptsMouseClicks(false, false);
    startTimerHz(30);
}

void PlayheadComponent::paint(juce::Graphics& g) {
    auto& transport = transportBar.getTransportState();
    double sampleRate = transport.getSampleRate();
    double bpm = transport.getTempo();
    double samplesPerBeat = sampleRate * 60.0 / bpm;

    double positionBeats = transport.getSamplePosition() / samplesPerBeat;
    int x = arrangementView.beatsToPixels(positionBeats);

    // Playhead line
    g.setColour(juce::Colour(0xFFFF4444));
    g.drawVerticalLine(x, 0.0f, static_cast<float>(getHeight()));

    // Playhead triangle at top
    juce::Path triangle;
    triangle.addTriangle(static_cast<float>(x - 6), 0.0f,
                         static_cast<float>(x + 6), 0.0f,
                         static_cast<float>(x), 10.0f);
    g.fillPath(triangle);
}

void PlayheadComponent::timerCallback() {
    if (transportBar.getTransportState().isPlaying()) {
        repaint();
    }
}

void PlayheadComponent::updatePosition() {
    repaint();
}

} // namespace iDAW
