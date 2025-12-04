/**
 * MainWindow.h - iDAW Main Window with Docking Panels
 *
 * The primary DAW interface featuring:
 * - Menu bar with file, edit, view, track, transport, window, help menus
 * - Toolbar with transport controls
 * - Dockable panels (arrangement, mixer, browser, intent)
 * - Status bar with audio engine info
 */

#pragma once

#include <JuceHeader.h>
#include <memory>

namespace iDAW {

// Forward declarations
class TransportBar;
class ArrangementView;
class MixerPanel;
class IntentPanel;
class TrackList;
class Project;

/**
 * @brief Main DAW window with panel layout
 */
class MainWindow : public juce::DocumentWindow,
                   public juce::MenuBarModel,
                   public juce::ApplicationCommandTarget {
public:
    MainWindow(const juce::String& name,
               juce::AudioDeviceManager& deviceManager);
    ~MainWindow() override;

    void closeButtonPressed() override;
    bool canCloseWindow();

    juce::MenuBarModel* getMenuBarModel() { return this; }

    //==========================================================================
    // Project management
    //==========================================================================

    void newProject();
    void openProject();
    void openProject(const juce::File& file);
    bool saveProject();
    bool saveProjectAs();
    void closeProject();

    bool hasUnsavedChanges() const;

    //==========================================================================
    // MenuBarModel
    //==========================================================================

    juce::StringArray getMenuBarNames() override;
    juce::PopupMenu getMenuForIndex(int menuIndex, const juce::String& menuName) override;
    void menuItemSelected(int menuItemID, int topLevelMenuIndex) override;

    //==========================================================================
    // ApplicationCommandTarget
    //==========================================================================

    juce::ApplicationCommandTarget* getNextCommandTarget() override { return nullptr; }
    void getAllCommands(juce::Array<juce::CommandID>& commands) override;
    void getCommandInfo(juce::CommandID commandID, juce::ApplicationCommandInfo& result) override;
    bool perform(const juce::ApplicationCommandTarget::InvocationInfo& info) override;

    //==========================================================================
    // Command IDs
    //==========================================================================

    enum CommandIDs {
        cmdNewProject = 1,
        cmdOpenProject,
        cmdSaveProject,
        cmdSaveProjectAs,
        cmdCloseProject,
        cmdQuit,

        cmdUndo,
        cmdRedo,
        cmdCut,
        cmdCopy,
        cmdPaste,
        cmdDelete,
        cmdSelectAll,

        cmdShowMixer,
        cmdShowArrangement,
        cmdShowIntentPanel,
        cmdShowBrowser,
        cmdShowPerformanceMetrics,

        cmdAddAudioTrack,
        cmdAddMidiTrack,
        cmdAddGroupTrack,
        cmdDeleteTrack,

        cmdPlay,
        cmdStop,
        cmdRecord,
        cmdRewind,
        cmdFastForward,
        cmdLoop,

        cmdAudioSettings,
        cmdPreferences,

        cmdAbout,
        cmdDocumentation
    };

private:
    juce::AudioDeviceManager& audioDeviceManager;

    // Core components
    std::unique_ptr<Project> currentProject;
    std::unique_ptr<TrackList> trackList;

    // Panels
    std::unique_ptr<TransportBar> transportBar;
    std::unique_ptr<ArrangementView> arrangementView;
    std::unique_ptr<MixerPanel> mixerPanel;
    std::unique_ptr<IntentPanel> intentPanel;

    // Commands
    juce::ApplicationCommandManager commandManager;

    // Status bar
    std::unique_ptr<juce::Label> statusLabel;
    std::unique_ptr<juce::Label> cpuMeter;

    // Layout
    void setupLayout();
    void updateStatusBar();

    // Save/load helpers
    bool confirmSaveIfNeeded();

    class MainContentComponent;
    std::unique_ptr<MainContentComponent> contentComponent;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainWindow)
};

/**
 * @brief Main content area with resizable panels
 */
class MainWindow::MainContentComponent : public juce::Component {
public:
    MainContentComponent(MainWindow& owner,
                        TransportBar& transport,
                        ArrangementView& arrangement,
                        MixerPanel& mixer,
                        IntentPanel& intent);

    void resized() override;
    void paint(juce::Graphics& g) override;

    void setMixerVisible(bool visible);
    void setIntentPanelVisible(bool visible);
    bool isMixerVisible() const { return mixerVisible; }
    bool isIntentPanelVisible() const { return intentVisible; }

private:
    MainWindow& owner;
    TransportBar& transportBar;
    ArrangementView& arrangementView;
    MixerPanel& mixerPanel;
    IntentPanel& intentPanel;

    bool mixerVisible = true;
    bool intentVisible = true;

    std::unique_ptr<juce::StretchableLayoutManager> layoutManager;
    std::unique_ptr<juce::StretchableLayoutResizerBar> resizer1;
    std::unique_ptr<juce::StretchableLayoutResizerBar> resizer2;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainContentComponent)
};

} // namespace iDAW
