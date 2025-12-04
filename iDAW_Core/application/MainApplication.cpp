/**
 * MainApplication.cpp - iDAW Desktop Application Implementation
 */

#include "MainApplication.h"
#include "MainWindow.h"
#include "PreferencesManager.h"

namespace iDAW {

void MainApplication::initialise(const juce::String& commandLine) {
    juce::ignoreUnused(commandLine);

    // Initialize preferences first
    preferences = std::make_unique<PreferencesManager>();
    loadPreferences();

    // Initialize audio device
    initializeAudioDevice();

    // Create main window
    mainWindow = std::make_unique<MainWindow>(
        getApplicationName(),
        audioDeviceManager
    );

    // Load recent projects
    auto recentFile = getAppDataDirectory().getChildFile("recent_projects.txt");
    if (recentFile.existsAsFile()) {
        recentProjects.restoreFromString(recentFile.loadFileAsString());
    }
    recentProjects.setMaxNumberOfItems(10);
}

void MainApplication::shutdown() {
    savePreferences();

    // Save recent projects
    auto recentFile = getAppDataDirectory().getChildFile("recent_projects.txt");
    recentFile.replaceWithText(recentProjects.toString());

    mainWindow.reset();
    preferences.reset();
}

void MainApplication::systemRequestedQuit() {
    // Check for unsaved changes in main window
    if (mainWindow && !mainWindow->canCloseWindow()) {
        return; // User cancelled
    }

    quit();
}

void MainApplication::anotherInstanceStarted(const juce::String& commandLine) {
    // Could handle opening a project file passed as argument
    juce::ignoreUnused(commandLine);

    if (mainWindow) {
        mainWindow->toFront(true);
    }
}

juce::MenuBarModel* MainApplication::getMenuModel() {
    if (mainWindow) {
        return mainWindow->getMenuBarModel();
    }
    return nullptr;
}

PreferencesManager& MainApplication::getPreferences() {
    jassert(preferences != nullptr);
    return *preferences;
}

juce::File MainApplication::getAppDataDirectory() const {
    auto dir = juce::File::getSpecialLocation(
        juce::File::userApplicationDataDirectory
    ).getChildFile("iDAW");

    if (!dir.exists()) {
        dir.createDirectory();
    }

    return dir;
}

void MainApplication::initializeAudioDevice() {
    // Try to restore saved audio settings
    auto settingsFile = getAppDataDirectory().getChildFile("audio_settings.xml");

    if (settingsFile.existsAsFile()) {
        auto xml = juce::parseXML(settingsFile);
        if (xml) {
            audioDeviceManager.initialise(
                2,    // numInputChannels
                2,    // numOutputChannels
                xml.get(),
                true  // selectDefaultDeviceOnFailure
            );
            return;
        }
    }

    // Default initialization
    audioDeviceManager.initialiseWithDefaultDevices(2, 2);
}

void MainApplication::loadPreferences() {
    auto prefsFile = getAppDataDirectory().getChildFile("preferences.xml");
    if (prefsFile.existsAsFile()) {
        preferences->loadFromFile(prefsFile);
    }
}

void MainApplication::savePreferences() {
    // Save audio device state
    auto audioState = audioDeviceManager.createStateXml();
    if (audioState) {
        auto settingsFile = getAppDataDirectory().getChildFile("audio_settings.xml");
        settingsFile.replaceWithText(audioState->toString());
    }

    // Save preferences
    auto prefsFile = getAppDataDirectory().getChildFile("preferences.xml");
    preferences->saveToFile(prefsFile);
}

} // namespace iDAW

// Application entry point
START_JUCE_APPLICATION(iDAW::MainApplication)
