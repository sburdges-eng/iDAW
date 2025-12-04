/**
 * PreferencesManager.h - User Preferences and Settings
 */

#pragma once

#include <JuceHeader.h>

namespace iDAW {

/**
 * @brief Manages user preferences and application settings
 */
class PreferencesManager {
public:
    PreferencesManager();

    //==========================================================================
    // File operations
    //==========================================================================

    void loadFromFile(const juce::File& file);
    void saveToFile(const juce::File& file) const;

    //==========================================================================
    // Audio settings
    //==========================================================================

    int getDefaultBufferSize() const { return defaultBufferSize; }
    void setDefaultBufferSize(int size) { defaultBufferSize = size; }

    double getDefaultSampleRate() const { return defaultSampleRate; }
    void setDefaultSampleRate(double rate) { defaultSampleRate = rate; }

    //==========================================================================
    // Plugin paths
    //==========================================================================

    juce::StringArray getPluginSearchPaths() const { return pluginSearchPaths; }
    void setPluginSearchPaths(const juce::StringArray& paths) { pluginSearchPaths = paths; }
    void addPluginSearchPath(const juce::String& path);

    //==========================================================================
    // UI settings
    //==========================================================================

    enum class Theme { Dark, Light, Blueprint };

    Theme getTheme() const { return theme; }
    void setTheme(Theme t) { theme = t; }

    bool getShowTooltips() const { return showTooltips; }
    void setShowTooltips(bool show) { showTooltips = show; }

    //==========================================================================
    // Project settings
    //==========================================================================

    juce::File getDefaultProjectLocation() const { return defaultProjectLocation; }
    void setDefaultProjectLocation(const juce::File& dir) { defaultProjectLocation = dir; }

    bool getAutoSaveEnabled() const { return autoSaveEnabled; }
    void setAutoSaveEnabled(bool enabled) { autoSaveEnabled = enabled; }

    int getAutoSaveIntervalMinutes() const { return autoSaveIntervalMinutes; }
    void setAutoSaveIntervalMinutes(int minutes) { autoSaveIntervalMinutes = minutes; }

    //==========================================================================
    // AI/Intent settings
    //==========================================================================

    bool getGhostHandsEnabled() const { return ghostHandsEnabled; }
    void setGhostHandsEnabled(bool enabled) { ghostHandsEnabled = enabled; }

    bool getIntentAssistantEnabled() const { return intentAssistantEnabled; }
    void setIntentAssistantEnabled(bool enabled) { intentAssistantEnabled = enabled; }

private:
    // Audio
    int defaultBufferSize = 512;
    double defaultSampleRate = 44100.0;

    // Plugins
    juce::StringArray pluginSearchPaths;

    // UI
    Theme theme = Theme::Blueprint;
    bool showTooltips = true;

    // Project
    juce::File defaultProjectLocation;
    bool autoSaveEnabled = true;
    int autoSaveIntervalMinutes = 5;

    // AI
    bool ghostHandsEnabled = true;
    bool intentAssistantEnabled = true;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PreferencesManager)
};

} // namespace iDAW
