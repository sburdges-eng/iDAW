/**
 * TrackList.cpp - Track Collection Implementation
 */

#include "TrackList.h"
#include "../session/Project.h"

namespace iDAW {

TrackList::TrackList() {
    masterTrack = std::make_unique<MasterTrack>();
}

Track* TrackList::getTrack(int index) {
    if (index >= 0 && index < static_cast<int>(tracks.size())) {
        return tracks[index].get();
    }
    return nullptr;
}

const Track* TrackList::getTrack(int index) const {
    if (index >= 0 && index < static_cast<int>(tracks.size())) {
        return tracks[index].get();
    }
    return nullptr;
}

Track* TrackList::getTrackById(juce::Uuid id) {
    for (auto& track : tracks) {
        if (track->getId() == id) {
            return track.get();
        }
    }
    return nullptr;
}

Track* TrackList::getSelectedTrack() {
    return getTrack(selectedTrackIndex);
}

AudioTrack* TrackList::addAudioTrack(const juce::String& name) {
    auto trackName = name.isEmpty() ? generateTrackName("Audio") : name;
    auto track = std::make_unique<AudioTrack>(trackName);
    auto* ptr = track.get();

    int index = static_cast<int>(tracks.size());
    track->setIndex(index);
    tracks.push_back(std::move(track));

    listeners.call([ptr, index](Listener& l) { l.trackAdded(ptr, index); });
    sendChangeMessage();

    return ptr;
}

MidiTrack* TrackList::addMidiTrack(const juce::String& name) {
    auto trackName = name.isEmpty() ? generateTrackName("MIDI") : name;
    auto track = std::make_unique<MidiTrack>(trackName);
    auto* ptr = track.get();

    int index = static_cast<int>(tracks.size());
    track->setIndex(index);
    tracks.push_back(std::move(track));

    listeners.call([ptr, index](Listener& l) { l.trackAdded(ptr, index); });
    sendChangeMessage();

    return ptr;
}

GroupTrack* TrackList::addGroupTrack(const juce::String& name) {
    auto trackName = name.isEmpty() ? generateTrackName("Group") : name;
    auto track = std::make_unique<GroupTrack>(trackName);
    auto* ptr = track.get();

    int index = static_cast<int>(tracks.size());
    track->setIndex(index);
    tracks.push_back(std::move(track));

    listeners.call([ptr, index](Listener& l) { l.trackAdded(ptr, index); });
    sendChangeMessage();

    return ptr;
}

void TrackList::removeTrack(int index) {
    if (index >= 0 && index < static_cast<int>(tracks.size())) {
        tracks.erase(tracks.begin() + index);
        updateTrackIndices();

        if (selectedTrackIndex >= static_cast<int>(tracks.size())) {
            selectedTrackIndex = static_cast<int>(tracks.size()) - 1;
        }

        listeners.call([index](Listener& l) { l.trackRemoved(index); });
        sendChangeMessage();
    }
}

void TrackList::removeTrack(Track* track) {
    for (int i = 0; i < static_cast<int>(tracks.size()); ++i) {
        if (tracks[i].get() == track) {
            removeTrack(i);
            return;
        }
    }
}

void TrackList::moveTrack(int fromIndex, int toIndex) {
    if (fromIndex >= 0 && fromIndex < static_cast<int>(tracks.size()) &&
        toIndex >= 0 && toIndex < static_cast<int>(tracks.size()) &&
        fromIndex != toIndex) {

        auto track = std::move(tracks[fromIndex]);
        tracks.erase(tracks.begin() + fromIndex);
        tracks.insert(tracks.begin() + toIndex, std::move(track));
        updateTrackIndices();

        // Update selection
        if (selectedTrackIndex == fromIndex) {
            selectedTrackIndex = toIndex;
        } else if (fromIndex < selectedTrackIndex && toIndex >= selectedTrackIndex) {
            selectedTrackIndex--;
        } else if (fromIndex > selectedTrackIndex && toIndex <= selectedTrackIndex) {
            selectedTrackIndex++;
        }

        listeners.call([fromIndex, toIndex](Listener& l) { l.trackMoved(fromIndex, toIndex); });
        sendChangeMessage();
    }
}

void TrackList::duplicateTrack(int index) {
    if (index >= 0 && index < static_cast<int>(tracks.size())) {
        auto* original = tracks[index].get();
        auto data = original->toVar();

        std::unique_ptr<Track> newTrack;

        switch (original->getType()) {
            case TrackType::Audio:
                newTrack = std::make_unique<AudioTrack>(original->getName() + " Copy");
                break;
            case TrackType::Midi:
                newTrack = std::make_unique<MidiTrack>(original->getName() + " Copy");
                break;
            case TrackType::Group:
                newTrack = std::make_unique<GroupTrack>(original->getName() + " Copy");
                break;
            default:
                return;
        }

        newTrack->fromVar(data);
        newTrack->setName(original->getName() + " Copy");

        int newIndex = index + 1;
        newTrack->setIndex(newIndex);
        tracks.insert(tracks.begin() + newIndex, std::move(newTrack));
        updateTrackIndices();

        listeners.call([this, newIndex](Listener& l) {
            l.trackAdded(tracks[newIndex].get(), newIndex);
        });
        sendChangeMessage();
    }
}

void TrackList::clear() {
    tracks.clear();
    selectedTrackIndex = -1;
    nextTrackNumber = 1;
    sendChangeMessage();
}

void TrackList::setSelectedTrackIndex(int index) {
    if (index >= -1 && index < static_cast<int>(tracks.size()) && index != selectedTrackIndex) {
        selectedTrackIndex = index;
        listeners.call([index](Listener& l) { l.selectionChanged(index); });
        sendChangeMessage();
    }
}

void TrackList::selectNextTrack() {
    if (selectedTrackIndex < static_cast<int>(tracks.size()) - 1) {
        setSelectedTrackIndex(selectedTrackIndex + 1);
    }
}

void TrackList::selectPreviousTrack() {
    if (selectedTrackIndex > 0) {
        setSelectedTrackIndex(selectedTrackIndex - 1);
    }
}

bool TrackList::hasAnySolo() const {
    for (const auto& track : tracks) {
        if (track->isSolo()) {
            return true;
        }
    }
    return false;
}

bool TrackList::isTrackAudible(int index) const {
    if (index < 0 || index >= static_cast<int>(tracks.size())) {
        return false;
    }

    const auto* track = tracks[index].get();

    if (track->isMuted()) {
        return false;
    }

    if (hasAnySolo()) {
        return track->isSolo();
    }

    return true;
}

void TrackList::prepareToPlay(double sampleRate, int samplesPerBlock) {
    for (auto& track : tracks) {
        track->prepareToPlay(sampleRate, samplesPerBlock);
    }
    masterTrack->prepareToPlay(sampleRate, samplesPerBlock);
}

void TrackList::releaseResources() {
    for (auto& track : tracks) {
        track->releaseResources();
    }
    masterTrack->releaseResources();
}

void TrackList::loadFromProject(Project& project) {
    clear();

    auto data = project.getTrackData();
    if (auto* arr = data.getArray()) {
        for (const auto& trackVar : *arr) {
            if (auto* obj = trackVar.getDynamicObject()) {
                auto type = static_cast<TrackType>(static_cast<int>(obj->getProperty("type")));

                std::unique_ptr<Track> track;
                switch (type) {
                    case TrackType::Audio:
                        track = std::make_unique<AudioTrack>();
                        break;
                    case TrackType::Midi:
                        track = std::make_unique<MidiTrack>();
                        break;
                    case TrackType::Group:
                        track = std::make_unique<GroupTrack>();
                        break;
                    default:
                        continue;
                }

                track->fromVar(trackVar);
                track->setIndex(static_cast<int>(tracks.size()));
                tracks.push_back(std::move(track));
            }
        }
    }

    // Load master track
    auto masterData = project.getMasterTrackData();
    if (masterData.isObject()) {
        masterTrack->fromVar(masterData);
    }

    sendChangeMessage();
}

void TrackList::saveToProject(Project& project) {
    juce::Array<juce::var> trackArray;
    for (const auto& track : tracks) {
        trackArray.add(track->toVar());
    }
    project.setTrackData(trackArray);
    project.setMasterTrackData(masterTrack->toVar());
}

juce::String TrackList::generateTrackName(const juce::String& baseName) {
    return baseName + " " + juce::String(nextTrackNumber++);
}

void TrackList::updateTrackIndices() {
    for (int i = 0; i < static_cast<int>(tracks.size()); ++i) {
        tracks[i]->setIndex(i);
    }
}

} // namespace iDAW
