/**
 * MainWindow.cpp - iDAW Main Window Implementation
 */

#include "MainWindow.h"
#include "../transport/TransportBar.h"
#include "../arrangement/ArrangementView.h"
#include "../mixer/MixerPanel.h"
#include "../intent/IntentPanel.h"
#include "../tracks/TrackList.h"
#include "../session/Project.h"

namespace iDAW {

//==============================================================================
// MainWindow
//==============================================================================

MainWindow::MainWindow(const juce::String& name,
                       juce::AudioDeviceManager& deviceManager)
    : DocumentWindow(name,
                    juce::Colour(0xFF1A1A2E),  // Dark background
                    DocumentWindow::allButtons),
      audioDeviceManager(deviceManager) {

    setUsingNativeTitleBar(true);

    // Initialize command manager
    commandManager.registerAllCommandsForTarget(this);

#if JUCE_MAC
    setMacMainMenu(this);
#else
    setMenuBar(this);
#endif

    // Create components
    trackList = std::make_unique<TrackList>();
    transportBar = std::make_unique<TransportBar>(*trackList);
    arrangementView = std::make_unique<ArrangementView>(*trackList, *transportBar);
    mixerPanel = std::make_unique<MixerPanel>(*trackList);
    intentPanel = std::make_unique<IntentPanel>();

    // Create content component
    contentComponent = std::make_unique<MainContentComponent>(
        *this,
        *transportBar,
        *arrangementView,
        *mixerPanel,
        *intentPanel
    );

    setContentOwned(contentComponent.release(), true);

    // Status bar
    statusLabel = std::make_unique<juce::Label>();
    statusLabel->setText("Ready", juce::dontSendNotification);

    cpuMeter = std::make_unique<juce::Label>();
    cpuMeter->setText("CPU: 0%", juce::dontSendNotification);

    // Window settings
    setResizable(true, true);
    setResizeLimits(800, 600, 4096, 2160);
    centreWithSize(1400, 900);
    setVisible(true);

    // Start with new project
    newProject();
}

MainWindow::~MainWindow() {
#if JUCE_MAC
    juce::MenuBarModel::setMacMainMenu(nullptr);
#else
    setMenuBar(nullptr);
#endif
}

void MainWindow::closeButtonPressed() {
    juce::JUCEApplication::getInstance()->systemRequestedQuit();
}

bool MainWindow::canCloseWindow() {
    return confirmSaveIfNeeded();
}

bool MainWindow::confirmSaveIfNeeded() {
    if (!hasUnsavedChanges()) {
        return true;
    }

    auto result = juce::AlertWindow::showYesNoCancelBox(
        juce::MessageBoxIconType::QuestionIcon,
        "Save Changes?",
        "Do you want to save changes to the current project?",
        "Save",
        "Don't Save",
        "Cancel"
    );

    if (result == 1) { // Save
        return saveProject();
    } else if (result == 2) { // Don't Save
        return true;
    }

    return false; // Cancel
}

bool MainWindow::hasUnsavedChanges() const {
    return currentProject && currentProject->hasUnsavedChanges();
}

//==============================================================================
// Project Management
//==============================================================================

void MainWindow::newProject() {
    if (!confirmSaveIfNeeded()) return;

    currentProject = std::make_unique<Project>();
    trackList->clear();

    // Add a default audio track and MIDI track
    trackList->addAudioTrack("Audio 1");
    trackList->addMidiTrack("MIDI 1");

    arrangementView->projectChanged();
    mixerPanel->projectChanged();

    setName("iDAW - Untitled");
}

void MainWindow::openProject() {
    if (!confirmSaveIfNeeded()) return;

    juce::FileChooser chooser("Open Project",
                              juce::File::getSpecialLocation(juce::File::userMusicDirectory),
                              "*.idaw");

    if (chooser.browseForFileToOpen()) {
        openProject(chooser.getResult());
    }
}

void MainWindow::openProject(const juce::File& file) {
    if (!confirmSaveIfNeeded()) return;

    currentProject = std::make_unique<Project>();
    if (currentProject->loadFromFile(file)) {
        trackList->loadFromProject(*currentProject);
        arrangementView->projectChanged();
        mixerPanel->projectChanged();
        setName("iDAW - " + file.getFileNameWithoutExtension());
    } else {
        juce::AlertWindow::showMessageBoxAsync(
            juce::MessageBoxIconType::WarningIcon,
            "Error",
            "Failed to open project: " + file.getFullPathName()
        );
        newProject();
    }
}

bool MainWindow::saveProject() {
    if (!currentProject) return false;

    if (currentProject->getProjectFile().existsAsFile()) {
        return currentProject->save();
    }

    return saveProjectAs();
}

bool MainWindow::saveProjectAs() {
    if (!currentProject) return false;

    juce::FileChooser chooser("Save Project As",
                              juce::File::getSpecialLocation(juce::File::userMusicDirectory),
                              "*.idaw");

    if (chooser.browseForFileToSave(true)) {
        auto file = chooser.getResult();
        if (!file.hasFileExtension(".idaw")) {
            file = file.withFileExtension(".idaw");
        }

        trackList->saveToProject(*currentProject);
        if (currentProject->saveToFile(file)) {
            setName("iDAW - " + file.getFileNameWithoutExtension());
            return true;
        }
    }

    return false;
}

void MainWindow::closeProject() {
    if (!confirmSaveIfNeeded()) return;

    currentProject.reset();
    trackList->clear();
    arrangementView->projectChanged();
    mixerPanel->projectChanged();
    setName("iDAW");
}

//==============================================================================
// MenuBarModel
//==============================================================================

juce::StringArray MainWindow::getMenuBarNames() {
    return {"File", "Edit", "View", "Track", "Transport", "Window", "Help"};
}

juce::PopupMenu MainWindow::getMenuForIndex(int menuIndex, const juce::String& menuName) {
    juce::PopupMenu menu;
    juce::ignoreUnused(menuName);

    if (menuIndex == 0) { // File
        menu.addCommandItem(&commandManager, cmdNewProject);
        menu.addCommandItem(&commandManager, cmdOpenProject);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdSaveProject);
        menu.addCommandItem(&commandManager, cmdSaveProjectAs);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdCloseProject);
#if !JUCE_MAC
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdQuit);
#endif
    }
    else if (menuIndex == 1) { // Edit
        menu.addCommandItem(&commandManager, cmdUndo);
        menu.addCommandItem(&commandManager, cmdRedo);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdCut);
        menu.addCommandItem(&commandManager, cmdCopy);
        menu.addCommandItem(&commandManager, cmdPaste);
        menu.addCommandItem(&commandManager, cmdDelete);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdSelectAll);
    }
    else if (menuIndex == 2) { // View
        menu.addCommandItem(&commandManager, cmdShowArrangement);
        menu.addCommandItem(&commandManager, cmdShowMixer);
        menu.addCommandItem(&commandManager, cmdShowIntentPanel);
        menu.addCommandItem(&commandManager, cmdShowBrowser);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdShowPerformanceMetrics);
    }
    else if (menuIndex == 3) { // Track
        menu.addCommandItem(&commandManager, cmdAddAudioTrack);
        menu.addCommandItem(&commandManager, cmdAddMidiTrack);
        menu.addCommandItem(&commandManager, cmdAddGroupTrack);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdDeleteTrack);
    }
    else if (menuIndex == 4) { // Transport
        menu.addCommandItem(&commandManager, cmdPlay);
        menu.addCommandItem(&commandManager, cmdStop);
        menu.addCommandItem(&commandManager, cmdRecord);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdRewind);
        menu.addCommandItem(&commandManager, cmdFastForward);
        menu.addSeparator();
        menu.addCommandItem(&commandManager, cmdLoop);
    }
    else if (menuIndex == 5) { // Window
        menu.addCommandItem(&commandManager, cmdAudioSettings);
        menu.addCommandItem(&commandManager, cmdPreferences);
    }
    else if (menuIndex == 6) { // Help
        menu.addCommandItem(&commandManager, cmdAbout);
        menu.addCommandItem(&commandManager, cmdDocumentation);
    }

    return menu;
}

void MainWindow::menuItemSelected(int menuItemID, int topLevelMenuIndex) {
    juce::ignoreUnused(menuItemID, topLevelMenuIndex);
}

//==============================================================================
// ApplicationCommandTarget
//==============================================================================

void MainWindow::getAllCommands(juce::Array<juce::CommandID>& commands) {
    commands.addArray({
        cmdNewProject, cmdOpenProject, cmdSaveProject, cmdSaveProjectAs,
        cmdCloseProject, cmdQuit,
        cmdUndo, cmdRedo, cmdCut, cmdCopy, cmdPaste, cmdDelete, cmdSelectAll,
        cmdShowMixer, cmdShowArrangement, cmdShowIntentPanel, cmdShowBrowser,
        cmdShowPerformanceMetrics,
        cmdAddAudioTrack, cmdAddMidiTrack, cmdAddGroupTrack, cmdDeleteTrack,
        cmdPlay, cmdStop, cmdRecord, cmdRewind, cmdFastForward, cmdLoop,
        cmdAudioSettings, cmdPreferences,
        cmdAbout, cmdDocumentation
    });
}

void MainWindow::getCommandInfo(juce::CommandID commandID, juce::ApplicationCommandInfo& result) {
    switch (commandID) {
        case cmdNewProject:
            result.setInfo("New Project", "Create a new project", "File", 0);
            result.addDefaultKeypress('n', juce::ModifierKeys::commandModifier);
            break;
        case cmdOpenProject:
            result.setInfo("Open Project...", "Open an existing project", "File", 0);
            result.addDefaultKeypress('o', juce::ModifierKeys::commandModifier);
            break;
        case cmdSaveProject:
            result.setInfo("Save Project", "Save the current project", "File", 0);
            result.addDefaultKeypress('s', juce::ModifierKeys::commandModifier);
            break;
        case cmdSaveProjectAs:
            result.setInfo("Save Project As...", "Save project with a new name", "File", 0);
            result.addDefaultKeypress('s', juce::ModifierKeys::commandModifier | juce::ModifierKeys::shiftModifier);
            break;
        case cmdCloseProject:
            result.setInfo("Close Project", "Close the current project", "File", 0);
            result.addDefaultKeypress('w', juce::ModifierKeys::commandModifier);
            break;
        case cmdQuit:
            result.setInfo("Quit", "Quit iDAW", "File", 0);
            result.addDefaultKeypress('q', juce::ModifierKeys::commandModifier);
            break;

        case cmdUndo:
            result.setInfo("Undo", "Undo last action", "Edit", 0);
            result.addDefaultKeypress('z', juce::ModifierKeys::commandModifier);
            break;
        case cmdRedo:
            result.setInfo("Redo", "Redo last undone action", "Edit", 0);
            result.addDefaultKeypress('z', juce::ModifierKeys::commandModifier | juce::ModifierKeys::shiftModifier);
            break;
        case cmdCut:
            result.setInfo("Cut", "Cut selection", "Edit", 0);
            result.addDefaultKeypress('x', juce::ModifierKeys::commandModifier);
            break;
        case cmdCopy:
            result.setInfo("Copy", "Copy selection", "Edit", 0);
            result.addDefaultKeypress('c', juce::ModifierKeys::commandModifier);
            break;
        case cmdPaste:
            result.setInfo("Paste", "Paste from clipboard", "Edit", 0);
            result.addDefaultKeypress('v', juce::ModifierKeys::commandModifier);
            break;
        case cmdDelete:
            result.setInfo("Delete", "Delete selection", "Edit", 0);
            result.addDefaultKeypress(juce::KeyPress::deleteKey, 0);
            break;
        case cmdSelectAll:
            result.setInfo("Select All", "Select all items", "Edit", 0);
            result.addDefaultKeypress('a', juce::ModifierKeys::commandModifier);
            break;

        case cmdShowMixer:
            result.setInfo("Show Mixer", "Toggle mixer panel", "View", 0);
            result.addDefaultKeypress('m', juce::ModifierKeys::commandModifier);
            break;
        case cmdShowArrangement:
            result.setInfo("Show Arrangement", "Toggle arrangement view", "View", 0);
            break;
        case cmdShowIntentPanel:
            result.setInfo("Show Intent Panel", "Toggle AI intent panel", "View", 0);
            result.addDefaultKeypress('i', juce::ModifierKeys::commandModifier);
            break;
        case cmdShowBrowser:
            result.setInfo("Show Browser", "Toggle file browser", "View", 0);
            break;
        case cmdShowPerformanceMetrics:
            result.setInfo("Performance Metrics", "Show CPU and memory usage", "View", 0);
            break;

        case cmdAddAudioTrack:
            result.setInfo("Add Audio Track", "Create a new audio track", "Track", 0);
            result.addDefaultKeypress('t', juce::ModifierKeys::commandModifier | juce::ModifierKeys::shiftModifier);
            break;
        case cmdAddMidiTrack:
            result.setInfo("Add MIDI Track", "Create a new MIDI track", "Track", 0);
            break;
        case cmdAddGroupTrack:
            result.setInfo("Add Group Track", "Create a new group track", "Track", 0);
            break;
        case cmdDeleteTrack:
            result.setInfo("Delete Track", "Delete selected track", "Track", 0);
            break;

        case cmdPlay:
            result.setInfo("Play", "Start playback", "Transport", 0);
            result.addDefaultKeypress(juce::KeyPress::spaceKey, 0);
            break;
        case cmdStop:
            result.setInfo("Stop", "Stop playback", "Transport", 0);
            break;
        case cmdRecord:
            result.setInfo("Record", "Start recording", "Transport", 0);
            result.addDefaultKeypress('r', juce::ModifierKeys::commandModifier);
            break;
        case cmdRewind:
            result.setInfo("Rewind", "Go to beginning", "Transport", 0);
            result.addDefaultKeypress(juce::KeyPress::returnKey, 0);
            break;
        case cmdFastForward:
            result.setInfo("Fast Forward", "Skip forward", "Transport", 0);
            break;
        case cmdLoop:
            result.setInfo("Loop", "Toggle loop mode", "Transport", 0);
            result.addDefaultKeypress('l', juce::ModifierKeys::commandModifier);
            break;

        case cmdAudioSettings:
            result.setInfo("Audio Settings...", "Configure audio device", "Window", 0);
            break;
        case cmdPreferences:
            result.setInfo("Preferences...", "Edit preferences", "Window", 0);
            result.addDefaultKeypress(',', juce::ModifierKeys::commandModifier);
            break;

        case cmdAbout:
            result.setInfo("About iDAW", "About this application", "Help", 0);
            break;
        case cmdDocumentation:
            result.setInfo("Documentation", "Open documentation", "Help", 0);
            break;
    }
}

bool MainWindow::perform(const juce::ApplicationCommandTarget::InvocationInfo& info) {
    switch (info.commandID) {
        case cmdNewProject: newProject(); return true;
        case cmdOpenProject: openProject(); return true;
        case cmdSaveProject: saveProject(); return true;
        case cmdSaveProjectAs: saveProjectAs(); return true;
        case cmdCloseProject: closeProject(); return true;
        case cmdQuit: juce::JUCEApplication::getInstance()->systemRequestedQuit(); return true;

        case cmdPlay: transportBar->play(); return true;
        case cmdStop: transportBar->stop(); return true;
        case cmdRecord: transportBar->toggleRecord(); return true;
        case cmdRewind: transportBar->rewind(); return true;
        case cmdLoop: transportBar->toggleLoop(); return true;

        case cmdAddAudioTrack: trackList->addAudioTrack(); return true;
        case cmdAddMidiTrack: trackList->addMidiTrack(); return true;
        case cmdAddGroupTrack: trackList->addGroupTrack(); return true;

        case cmdAudioSettings: {
            juce::DialogWindow::LaunchOptions options;
            auto* selector = new juce::AudioDeviceSelectorComponent(
                audioDeviceManager, 0, 2, 0, 2, true, true, true, false);
            selector->setSize(500, 400);
            options.content.setOwned(selector);
            options.dialogTitle = "Audio Settings";
            options.dialogBackgroundColour = juce::Colour(0xFF1A1A2E);
            options.escapeKeyTriggersCloseButton = true;
            options.useNativeTitleBar = true;
            options.resizable = false;
            options.launchAsync();
            return true;
        }

        case cmdAbout: {
            juce::AlertWindow::showMessageBoxAsync(
                juce::MessageBoxIconType::InfoIcon,
                "About iDAW",
                "iDAW - Intent-Driven Digital Audio Workstation\n\n"
                "Version 1.0.0\n\n"
                "\"The tool shouldn't finish art for people.\n"
                "It should make them braver.\""
            );
            return true;
        }

        default:
            return false;
    }
}

//==============================================================================
// MainContentComponent
//==============================================================================

MainWindow::MainContentComponent::MainContentComponent(MainWindow& o,
                                                        TransportBar& transport,
                                                        ArrangementView& arrangement,
                                                        MixerPanel& mixer,
                                                        IntentPanel& intent)
    : owner(o),
      transportBar(transport),
      arrangementView(arrangement),
      mixerPanel(mixer),
      intentPanel(intent) {

    addAndMakeVisible(transportBar);
    addAndMakeVisible(arrangementView);
    addAndMakeVisible(mixerPanel);
    addAndMakeVisible(intentPanel);

    layoutManager = std::make_unique<juce::StretchableLayoutManager>();

    // Set up layout: arrangement | mixer | intent panel
    layoutManager->setItemLayout(0, 200, -1.0, -0.6);  // Arrangement (60%)
    layoutManager->setItemLayout(1, 5, 5, 5);          // Resizer
    layoutManager->setItemLayout(2, 150, 400, 250);    // Mixer
    layoutManager->setItemLayout(3, 5, 5, 5);          // Resizer
    layoutManager->setItemLayout(4, 150, 350, 250);    // Intent panel

    resizer1 = std::make_unique<juce::StretchableLayoutResizerBar>(
        layoutManager.get(), 1, true);
    resizer2 = std::make_unique<juce::StretchableLayoutResizerBar>(
        layoutManager.get(), 3, true);

    addAndMakeVisible(*resizer1);
    addAndMakeVisible(*resizer2);

    setSize(1400, 900);
}

void MainWindow::MainContentComponent::resized() {
    auto area = getLocalBounds();

    // Transport bar at top
    transportBar.setBounds(area.removeFromTop(50));

    // Main panels below
    juce::Component* comps[] = {
        &arrangementView, resizer1.get(), &mixerPanel, resizer2.get(), &intentPanel
    };

    layoutManager->layOutComponents(comps, 5,
                                    area.getX(), area.getY(),
                                    area.getWidth(), area.getHeight(),
                                    false, true);
}

void MainWindow::MainContentComponent::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF1A1A2E));
}

void MainWindow::MainContentComponent::setMixerVisible(bool visible) {
    mixerVisible = visible;
    mixerPanel.setVisible(visible);
    resizer1->setVisible(visible);
    resized();
}

void MainWindow::MainContentComponent::setIntentPanelVisible(bool visible) {
    intentVisible = visible;
    intentPanel.setVisible(visible);
    resizer2->setVisible(visible);
    resized();
}

} // namespace iDAW
