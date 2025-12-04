/**
 * Project.cpp - Project Implementation
 */

#include "Project.h"

namespace iDAW {

const char* const Project::FILE_EXTENSION = ".idaw";

Project::Project() = default;

bool Project::loadFromFile(const juce::File& file) {
    if (!file.existsAsFile()) {
        return false;
    }

    auto jsonString = file.loadFileAsString();
    auto json = juce::JSON::parse(jsonString);

    if (!json.isObject()) {
        return false;
    }

    if (!fromJson(json)) {
        return false;
    }

    projectFile = file;
    unsavedChanges = false;
    return true;
}

bool Project::saveToFile(const juce::File& file) {
    auto json = toJson();
    auto jsonString = juce::JSON::toString(json, true);

    if (file.replaceWithText(jsonString)) {
        projectFile = file;
        unsavedChanges = false;
        return true;
    }

    return false;
}

bool Project::save() {
    if (projectFile.existsAsFile()) {
        return saveToFile(projectFile);
    }
    return false;
}

juce::File Project::getProjectDirectory() const {
    if (projectFile.existsAsFile()) {
        return projectFile.getParentDirectory();
    }
    return juce::File();
}

void Project::setName(const juce::String& n) {
    if (name != n) {
        name = n;
        markAsModified();
    }
}

void Project::setAuthor(const juce::String& a) {
    if (author != a) {
        author = a;
        markAsModified();
    }
}

void Project::setTempo(double bpm) {
    if (tempo != bpm) {
        tempo = juce::jlimit(20.0, 999.0, bpm);
        markAsModified();
    }
}

void Project::setTimeSignature(int num, int denom) {
    if (timeSignatureNum != num || timeSignatureDenom != denom) {
        timeSignatureNum = juce::jlimit(1, 32, num);
        timeSignatureDenom = juce::jlimit(1, 32, denom);
        markAsModified();
    }
}

void Project::setSampleRate(double rate) {
    if (sampleRate != rate) {
        sampleRate = rate;
        markAsModified();
    }
}

void Project::setTrackData(const juce::var& data) {
    trackData = data;
    markAsModified();
}

void Project::setMasterTrackData(const juce::var& data) {
    masterTrackData = data;
    markAsModified();
}

void Project::setIntentData(const juce::var& data) {
    intentData = data;
    markAsModified();
}

juce::File Project::getAudioDirectory() const {
    auto projectDir = getProjectDirectory();
    if (projectDir.isDirectory()) {
        auto audioDir = projectDir.getChildFile("Audio Files");
        if (!audioDir.exists()) {
            audioDir.createDirectory();
        }
        return audioDir;
    }
    return juce::File();
}

juce::File Project::copyAudioFileToProject(const juce::File& sourceFile) {
    auto audioDir = getAudioDirectory();
    if (!audioDir.isDirectory()) {
        return juce::File();
    }

    auto destFile = audioDir.getChildFile(sourceFile.getFileName());

    // Handle duplicate names
    int counter = 1;
    while (destFile.existsAsFile()) {
        destFile = audioDir.getChildFile(
            sourceFile.getFileNameWithoutExtension() +
            "_" + juce::String(counter++) +
            sourceFile.getFileExtension()
        );
    }

    if (sourceFile.copyFileTo(destFile)) {
        return destFile;
    }

    return juce::File();
}

juce::String Project::getRelativePath(const juce::File& file) const {
    auto projectDir = getProjectDirectory();
    if (projectDir.isDirectory() && file.isAChildOf(projectDir)) {
        return file.getRelativePathFrom(projectDir);
    }
    return file.getFullPathName();
}

juce::File Project::resolveRelativePath(const juce::String& relativePath) const {
    auto projectDir = getProjectDirectory();
    if (projectDir.isDirectory()) {
        return projectDir.getChildFile(relativePath);
    }
    return juce::File(relativePath);
}

juce::var Project::toJson() const {
    auto obj = new juce::DynamicObject();

    // File format version
    obj->setProperty("formatVersion", FILE_FORMAT_VERSION);
    obj->setProperty("application", "iDAW");

    // Metadata
    obj->setProperty("name", name);
    obj->setProperty("author", author);
    obj->setProperty("tempo", tempo);
    obj->setProperty("timeSignatureNumerator", timeSignatureNum);
    obj->setProperty("timeSignatureDenominator", timeSignatureDenom);
    obj->setProperty("sampleRate", sampleRate);

    // Timestamps
    obj->setProperty("createdAt", juce::Time::getCurrentTime().toISO8601(true));
    obj->setProperty("modifiedAt", juce::Time::getCurrentTime().toISO8601(true));

    // Track data
    obj->setProperty("tracks", trackData);
    obj->setProperty("masterTrack", masterTrackData);

    // Intent data
    obj->setProperty("intent", intentData);

    return juce::var(obj);
}

bool Project::fromJson(const juce::var& json) {
    if (!json.isObject()) {
        return false;
    }

    auto* obj = json.getDynamicObject();
    if (!obj) {
        return false;
    }

    // Check version
    int version = obj->getProperty("formatVersion");
    if (version > FILE_FORMAT_VERSION) {
        // File is from a newer version
        DBG("Warning: Project file is from a newer version of iDAW");
    }

    // Metadata
    name = obj->getProperty("name").toString();
    author = obj->getProperty("author").toString();
    tempo = obj->getProperty("tempo");
    timeSignatureNum = obj->getProperty("timeSignatureNumerator");
    timeSignatureDenom = obj->getProperty("timeSignatureDenominator");
    sampleRate = obj->getProperty("sampleRate");

    // Validate
    if (tempo <= 0) tempo = 120.0;
    if (timeSignatureNum <= 0) timeSignatureNum = 4;
    if (timeSignatureDenom <= 0) timeSignatureDenom = 4;
    if (sampleRate <= 0) sampleRate = 44100.0;

    // Track data
    trackData = obj->getProperty("tracks");
    masterTrackData = obj->getProperty("masterTrack");

    // Intent data
    intentData = obj->getProperty("intent");

    return true;
}

} // namespace iDAW
