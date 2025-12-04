/**
 * PreferencesManager.cpp - User Preferences Implementation
 */

#include "PreferencesManager.h"

namespace iDAW {

PreferencesManager::PreferencesManager() {
    // Initialize default plugin paths
#if JUCE_MAC
    pluginSearchPaths.add("/Library/Audio/Plug-Ins/VST3");
    pluginSearchPaths.add("/Library/Audio/Plug-Ins/Components");
    pluginSearchPaths.add("~/Library/Audio/Plug-Ins/VST3");
    pluginSearchPaths.add("~/Library/Audio/Plug-Ins/Components");
#elif JUCE_WINDOWS
    pluginSearchPaths.add("C:\\Program Files\\Common Files\\VST3");
    pluginSearchPaths.add("C:\\Program Files\\VSTPlugins");
#else // Linux
    pluginSearchPaths.add("/usr/lib/vst3");
    pluginSearchPaths.add("/usr/local/lib/vst3");
    pluginSearchPaths.add("~/.vst3");
#endif

    // Default project location
    defaultProjectLocation = juce::File::getSpecialLocation(
        juce::File::userMusicDirectory
    ).getChildFile("iDAW Projects");
}

void PreferencesManager::loadFromFile(const juce::File& file) {
    auto xml = juce::parseXML(file);
    if (!xml) return;

    if (xml->hasTagName("iDAWPreferences")) {
        // Audio
        defaultBufferSize = xml->getIntAttribute("bufferSize", defaultBufferSize);
        defaultSampleRate = xml->getDoubleAttribute("sampleRate", defaultSampleRate);

        // Theme
        auto themeStr = xml->getStringAttribute("theme", "blueprint");
        if (themeStr == "dark") theme = Theme::Dark;
        else if (themeStr == "light") theme = Theme::Light;
        else theme = Theme::Blueprint;

        showTooltips = xml->getBoolAttribute("showTooltips", showTooltips);

        // Project
        auto projectDir = xml->getStringAttribute("defaultProjectLocation");
        if (projectDir.isNotEmpty()) {
            defaultProjectLocation = juce::File(projectDir);
        }

        autoSaveEnabled = xml->getBoolAttribute("autoSave", autoSaveEnabled);
        autoSaveIntervalMinutes = xml->getIntAttribute("autoSaveMinutes", autoSaveIntervalMinutes);

        // AI
        ghostHandsEnabled = xml->getBoolAttribute("ghostHands", ghostHandsEnabled);
        intentAssistantEnabled = xml->getBoolAttribute("intentAssistant", intentAssistantEnabled);

        // Plugin paths
        if (auto* pathsElement = xml->getChildByName("PluginPaths")) {
            pluginSearchPaths.clear();
            for (auto* pathElement : pathsElement->getChildIterator()) {
                pluginSearchPaths.add(pathElement->getAllSubText());
            }
        }
    }
}

void PreferencesManager::saveToFile(const juce::File& file) const {
    juce::XmlElement xml("iDAWPreferences");

    // Audio
    xml.setAttribute("bufferSize", defaultBufferSize);
    xml.setAttribute("sampleRate", defaultSampleRate);

    // Theme
    juce::String themeStr;
    switch (theme) {
        case Theme::Dark: themeStr = "dark"; break;
        case Theme::Light: themeStr = "light"; break;
        case Theme::Blueprint: themeStr = "blueprint"; break;
    }
    xml.setAttribute("theme", themeStr);
    xml.setAttribute("showTooltips", showTooltips);

    // Project
    xml.setAttribute("defaultProjectLocation", defaultProjectLocation.getFullPathName());
    xml.setAttribute("autoSave", autoSaveEnabled);
    xml.setAttribute("autoSaveMinutes", autoSaveIntervalMinutes);

    // AI
    xml.setAttribute("ghostHands", ghostHandsEnabled);
    xml.setAttribute("intentAssistant", intentAssistantEnabled);

    // Plugin paths
    auto* pathsElement = xml.createNewChildElement("PluginPaths");
    for (const auto& path : pluginSearchPaths) {
        auto* pathElement = pathsElement->createNewChildElement("Path");
        pathElement->addTextElement(path);
    }

    file.replaceWithText(xml.toString());
}

void PreferencesManager::addPluginSearchPath(const juce::String& path) {
    if (!pluginSearchPaths.contains(path)) {
        pluginSearchPaths.add(path);
    }
}

} // namespace iDAW
