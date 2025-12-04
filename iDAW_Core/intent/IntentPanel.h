/**
 * IntentPanel.h - AI Intent-Driven Composition Panel
 *
 * The unique iDAW feature: Intent-driven composition with AI collaboration.
 * Three-phase intent schema:
 * - Phase 0: Core Wound/Desire (why)
 * - Phase 1: Emotional Intent (what feeling)
 * - Phase 2: Technical Constraints (how)
 *
 * "The tool shouldn't finish art for people. It should make them braver."
 */

#pragma once

#include <JuceHeader.h>
#include <memory>

namespace iDAW {

/**
 * @brief Intent-driven composition panel
 */
class IntentPanel : public juce::Component {
public:
    IntentPanel();
    ~IntentPanel() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

    //==========================================================================
    // Intent phases
    //==========================================================================

    // Phase 0: Core
    juce::String getCoreEvent() const;
    juce::String getCoreResistance() const;
    juce::String getCoreLonging() const;

    // Phase 1: Emotional
    juce::String getPrimaryMood() const;
    float getVulnerabilityScale() const;  // 0.0 - 1.0
    juce::String getNarrativeArc() const;

    // Phase 2: Technical
    juce::String getTechnicalGenre() const;
    juce::String getTechnicalKey() const;
    juce::String getRuleToBreak() const;

    //==========================================================================
    // AI suggestions
    //==========================================================================

    void requestAISuggestions();
    void onSuggestionReceived(const juce::String& category, const juce::String& suggestion);

    //==========================================================================
    // Rule breaking effects
    //==========================================================================

    struct RuleBreakingOption {
        juce::String id;
        juce::String name;
        juce::String emotionalEffect;
        juce::String technicalDescription;
    };

    static std::vector<RuleBreakingOption> getRuleBreakingOptions();

private:
    // Phase tabs
    std::unique_ptr<juce::TabbedComponent> phaseTabs;

    // Phase 0 components
    std::unique_ptr<juce::TextEditor> coreEventEditor;
    std::unique_ptr<juce::TextEditor> coreResistanceEditor;
    std::unique_ptr<juce::TextEditor> coreLongingEditor;

    // Phase 1 components
    std::unique_ptr<juce::ComboBox> moodSelector;
    std::unique_ptr<juce::Slider> vulnerabilitySlider;
    std::unique_ptr<juce::ComboBox> narrativeArcSelector;

    // Phase 2 components
    std::unique_ptr<juce::ComboBox> genreSelector;
    std::unique_ptr<juce::ComboBox> keySelector;
    std::unique_ptr<juce::ComboBox> ruleBreakingSelector;
    std::unique_ptr<juce::Label> ruleEffectLabel;

    // AI suggestion button
    std::unique_ptr<juce::TextButton> suggestButton;

    // Ghost Hands toggle
    std::unique_ptr<juce::ToggleButton> ghostHandsToggle;

    void createPhase0Tab(juce::Component* parent);
    void createPhase1Tab(juce::Component* parent);
    void createPhase2Tab(juce::Component* parent);
    void updateRuleEffect();

    class Phase0Component;
    class Phase1Component;
    class Phase2Component;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(IntentPanel)
};

/**
 * @brief Phase 0: Core Wound/Desire
 */
class IntentPanel::Phase0Component : public juce::Component {
public:
    Phase0Component();
    void resized() override;
    void paint(juce::Graphics& g) override;

    juce::TextEditor coreEventEditor;
    juce::TextEditor coreResistanceEditor;
    juce::TextEditor coreLongingEditor;

private:
    juce::Label eventLabel{"", "What happened? (The core event)"};
    juce::Label resistanceLabel{"", "What are you resisting?"};
    juce::Label longingLabel{"", "What do you long for?"};
};

/**
 * @brief Phase 1: Emotional Intent
 */
class IntentPanel::Phase1Component : public juce::Component {
public:
    Phase1Component();
    void resized() override;
    void paint(juce::Graphics& g) override;

    juce::ComboBox moodSelector;
    juce::Slider vulnerabilitySlider;
    juce::ComboBox narrativeArcSelector;

private:
    juce::Label moodLabel{"", "Primary Mood"};
    juce::Label vulnerabilityLabel{"", "Vulnerability (how exposed?)"};
    juce::Label narrativeLabel{"", "Narrative Arc"};
};

/**
 * @brief Phase 2: Technical Constraints
 */
class IntentPanel::Phase2Component : public juce::Component {
public:
    Phase2Component();
    void resized() override;
    void paint(juce::Graphics& g) override;

    juce::ComboBox genreSelector;
    juce::ComboBox keySelector;
    juce::ComboBox ruleBreakingSelector;
    juce::Label ruleEffectLabel;

private:
    juce::Label genreLabel{"", "Genre"};
    juce::Label keyLabel{"", "Key"};
    juce::Label ruleLabel{"", "Rule to Break"};
};

} // namespace iDAW
