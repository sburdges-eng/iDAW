/**
 * MainApplication.h - iDAW Desktop Application Entry Point
 *
 * Intent-Driven Digital Audio Workstation with AI Collaboration
 * "The tool shouldn't finish art for people. It should make them braver."
 */

#pragma once

#include <JuceHeader.h>
#include <memory>

namespace iDAW {

// Forward declarations
class MainWindow;
class PreferencesManager;

/**
 * @brief Main application class for iDAW Desktop
 *
 * Manages application lifecycle, audio device configuration,
 * and global state.
 */
class MainApplication : public juce::JUCEApplication {
public:
    MainApplication() = default;

    //==========================================================================
    // JUCEApplication overrides
    //==========================================================================

    const juce::String getApplicationName() override {
        return "iDAW";
    }

    const juce::String getApplicationVersion() override {
        return "1.0.0";
    }

    bool moreThanOneInstanceAllowed() override {
        return false;
    }

    void initialise(const juce::String& commandLine) override;
    void shutdown() override;
    void systemRequestedQuit() override;
    void anotherInstanceStarted(const juce::String& commandLine) override;

    //==========================================================================
    // Menu bar (macOS)
    //==========================================================================

    juce::MenuBarModel* getMenuModel();

    //==========================================================================
    // Global accessors
    //==========================================================================

    static MainApplication& getInstance() {
        return *dynamic_cast<MainApplication*>(JUCEApplication::getInstance());
    }

    juce::AudioDeviceManager& getAudioDeviceManager() {
        return audioDeviceManager;
    }

    PreferencesManager& getPreferences();

    /** Get the application data directory */
    juce::File getAppDataDirectory() const;

    /** Get recent projects list */
    juce::RecentlyOpenedFilesList& getRecentProjects() {
        return recentProjects;
    }

private:
    std::unique_ptr<MainWindow> mainWindow;
    std::unique_ptr<PreferencesManager> preferences;

    juce::AudioDeviceManager audioDeviceManager;
    juce::RecentlyOpenedFilesList recentProjects;

    /** Initialize audio device with saved settings or defaults */
    void initializeAudioDevice();

    /** Load application preferences */
    void loadPreferences();

    /** Save application preferences on shutdown */
    void savePreferences();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainApplication)
};

} // namespace iDAW
