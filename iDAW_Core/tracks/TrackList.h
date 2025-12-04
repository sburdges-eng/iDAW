/**
 * TrackList.h - Track Collection Manager
 *
 * Manages the collection of tracks in a project.
 */

#pragma once

#include <JuceHeader.h>
#include "Track.h"
#include <memory>
#include <vector>

namespace iDAW {

class Project;

/**
 * @brief Manages the collection of tracks in a project
 */
class TrackList : public juce::ChangeBroadcaster {
public:
    TrackList();
    ~TrackList() override = default;

    //==========================================================================
    // Track access
    //==========================================================================

    int getNumTracks() const { return static_cast<int>(tracks.size()); }
    Track* getTrack(int index);
    const Track* getTrack(int index) const;
    Track* getTrackById(juce::Uuid id);
    Track* getSelectedTrack();

    MasterTrack* getMasterTrack() { return masterTrack.get(); }
    const MasterTrack* getMasterTrack() const { return masterTrack.get(); }

    //==========================================================================
    // Track creation
    //==========================================================================

    AudioTrack* addAudioTrack(const juce::String& name = "");
    MidiTrack* addMidiTrack(const juce::String& name = "");
    GroupTrack* addGroupTrack(const juce::String& name = "");

    //==========================================================================
    // Track management
    //==========================================================================

    void removeTrack(int index);
    void removeTrack(Track* track);
    void moveTrack(int fromIndex, int toIndex);
    void duplicateTrack(int index);
    void clear();

    //==========================================================================
    // Selection
    //==========================================================================

    int getSelectedTrackIndex() const { return selectedTrackIndex; }
    void setSelectedTrackIndex(int index);
    void selectNextTrack();
    void selectPreviousTrack();

    //==========================================================================
    // Solo handling
    //==========================================================================

    bool hasAnySolo() const;
    bool isTrackAudible(int index) const;

    //==========================================================================
    // Audio preparation
    //==========================================================================

    void prepareToPlay(double sampleRate, int samplesPerBlock);
    void releaseResources();

    //==========================================================================
    // Project integration
    //==========================================================================

    void loadFromProject(Project& project);
    void saveToProject(Project& project);

    //==========================================================================
    // Listeners
    //==========================================================================

    class Listener {
    public:
        virtual ~Listener() = default;
        virtual void trackAdded(Track* track, int index) {}
        virtual void trackRemoved(int index) {}
        virtual void trackMoved(int fromIndex, int toIndex) {}
        virtual void selectionChanged(int newSelectedIndex) {}
    };

    void addListener(Listener* listener) { listeners.add(listener); }
    void removeListener(Listener* listener) { listeners.remove(listener); }

private:
    std::vector<std::unique_ptr<Track>> tracks;
    std::unique_ptr<MasterTrack> masterTrack;

    int selectedTrackIndex = -1;
    int nextTrackNumber = 1;

    juce::ListenerList<Listener> listeners;

    juce::String generateTrackName(const juce::String& baseName);
    void updateTrackIndices();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(TrackList)
};

} // namespace iDAW
