/**
 * Project.h - iDAW Project File Management
 *
 * Handles saving and loading of .idaw project files.
 * Project format is JSON-based with references to audio files.
 */

#pragma once

#include <JuceHeader.h>

namespace iDAW {

/**
 * @brief Represents an iDAW project file
 */
class Project {
public:
    Project();
    ~Project() = default;

    //==========================================================================
    // File operations
    //==========================================================================

    bool loadFromFile(const juce::File& file);
    bool saveToFile(const juce::File& file);
    bool save();

    juce::File getProjectFile() const { return projectFile; }
    juce::File getProjectDirectory() const;

    bool hasUnsavedChanges() const { return unsavedChanges; }
    void markAsModified() { unsavedChanges = true; }
    void clearModifiedFlag() { unsavedChanges = false; }

    //==========================================================================
    // Project metadata
    //==========================================================================

    juce::String getName() const { return name; }
    void setName(const juce::String& n);

    juce::String getAuthor() const { return author; }
    void setAuthor(const juce::String& a);

    double getTempo() const { return tempo; }
    void setTempo(double bpm);

    int getTimeSignatureNumerator() const { return timeSignatureNum; }
    int getTimeSignatureDenominator() const { return timeSignatureDenom; }
    void setTimeSignature(int num, int denom);

    double getSampleRate() const { return sampleRate; }
    void setSampleRate(double rate);

    //==========================================================================
    // Track data (serialized from TrackList)
    //==========================================================================

    juce::var getTrackData() const { return trackData; }
    void setTrackData(const juce::var& data);

    juce::var getMasterTrackData() const { return masterTrackData; }
    void setMasterTrackData(const juce::var& data);

    //==========================================================================
    // Intent data
    //==========================================================================

    juce::var getIntentData() const { return intentData; }
    void setIntentData(const juce::var& data);

    //==========================================================================
    // Audio file management
    //==========================================================================

    juce::File getAudioDirectory() const;
    juce::File copyAudioFileToProject(const juce::File& sourceFile);
    juce::String getRelativePath(const juce::File& file) const;
    juce::File resolveRelativePath(const juce::String& relativePath) const;

    //==========================================================================
    // Undo/Redo (placeholder)
    //==========================================================================

    void undo() { /* TODO */ }
    void redo() { /* TODO */ }
    bool canUndo() const { return false; }
    bool canRedo() const { return false; }

    //==========================================================================
    // Version info
    //==========================================================================

    static constexpr int FILE_FORMAT_VERSION = 1;
    static const char* const FILE_EXTENSION;

private:
    juce::File projectFile;
    bool unsavedChanges = false;

    // Metadata
    juce::String name = "Untitled";
    juce::String author;
    double tempo = 120.0;
    int timeSignatureNum = 4;
    int timeSignatureDenom = 4;
    double sampleRate = 44100.0;

    // Data
    juce::var trackData;
    juce::var masterTrackData;
    juce::var intentData;

    juce::var toJson() const;
    bool fromJson(const juce::var& json);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Project)
};

} // namespace iDAW
