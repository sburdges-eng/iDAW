/**
 * IntentPanel.cpp - Intent Panel Implementation
 */

#include "IntentPanel.h"

namespace iDAW {

//==============================================================================
// Rule Breaking Options
//==============================================================================

std::vector<IntentPanel::RuleBreakingOption> IntentPanel::getRuleBreakingOptions() {
    return {
        // Harmony rules
        {"HARMONY_AvoidTonicResolution", "Avoid Tonic Resolution",
         "Unresolved yearning, endless seeking",
         "Never resolve to the I chord; use deceptive cadences"},

        {"HARMONY_ParallelFifths", "Parallel Fifths",
         "Raw, medieval power; primal connection",
         "Use parallel perfect fifths between voices"},

        {"HARMONY_ChordToneClusters", "Chord Tone Clusters",
         "Dense emotional complexity; anxiety",
         "Stack adjacent chord tones in close position"},

        {"HARMONY_ModeModulation", "Sudden Mode Changes",
         "Emotional whiplash; transformation",
         "Shift between parallel major/minor unexpectedly"},

        // Rhythm rules
        {"RHYTHM_ConstantDisplacement", "Constant Displacement",
         "Anxiety, restlessness, anticipation",
         "Shift rhythmic accents off the grid continuously"},

        {"RHYTHM_AsymmetricGroove", "Asymmetric Time",
         "Unpredictability, controlled chaos",
         "Use odd time signatures or irregular groupings"},

        {"RHYTHM_RubatoEverywhere", "Excessive Rubato",
         "Dreamlike, unmoored from reality",
         "Constantly fluctuate tempo for emotional effect"},

        // Arrangement rules
        {"ARRANGEMENT_BuriedVocals", "Buried Vocals",
         "Dissociation, distance from emotion",
         "Mix vocals below instruments, as if heard underwater"},

        {"ARRANGEMENT_NoDynamics", "Flat Dynamics",
         "Emotional numbness, depression",
         "Keep everything at the same level; no crescendos"},

        {"ARRANGEMENT_SuddenSilence", "Sudden Silence",
         "Shock, loss, the void",
         "Cut to complete silence unexpectedly"},

        // Production rules
        {"PRODUCTION_PitchImperfection", "Pitch Imperfection",
         "Emotional honesty, vulnerability",
         "Leave pitch slightly off; avoid auto-tune"},

        {"PRODUCTION_DistortEverything", "Distort Everything",
         "Rage, overwhelming emotion, catharsis",
         "Apply saturation/distortion to all elements"},

        {"PRODUCTION_LoFiDegradation", "Lo-Fi Degradation",
         "Nostalgia, memory, loss of clarity",
         "Add tape hiss, bit reduction, filter highs"},

        // Structural rules
        {"STRUCTURE_NoChorus", "No Chorus",
         "Refusal of easy satisfaction",
         "Never repeat the obvious hook; continuous development"},

        {"STRUCTURE_EndUnresolved", "Unfinished Ending",
         "Life continues; story incomplete",
         "End mid-phrase without resolution"},
    };
}

//==============================================================================
// Phase0Component
//==============================================================================

IntentPanel::Phase0Component::Phase0Component() {
    auto setupEditor = [](juce::TextEditor& editor, const juce::String& placeholder) {
        editor.setMultiLine(true);
        editor.setReturnKeyStartsNewLine(true);
        editor.setColour(juce::TextEditor::backgroundColourId, juce::Colour(0xFF0D3050));
        editor.setColour(juce::TextEditor::textColourId, juce::Colour(0xFF00D4FF));
        editor.setColour(juce::TextEditor::outlineColourId, juce::Colour(0xFF00D4FF).withAlpha(0.5f));
        editor.setTextToShowWhenEmpty(placeholder, juce::Colour(0xFF557788));
    };

    auto setupLabel = [](juce::Label& label) {
        label.setColour(juce::Label::textColourId, juce::Colour(0xFF00D4FF));
        label.setFont(juce::Font(13, juce::Font::bold));
    };

    setupLabel(eventLabel);
    setupLabel(resistanceLabel);
    setupLabel(longingLabel);

    setupEditor(coreEventEditor, "A moment that changed everything...");
    setupEditor(coreResistanceEditor, "What I can't accept...");
    setupEditor(coreLongingEditor, "What I ache for...");

    addAndMakeVisible(eventLabel);
    addAndMakeVisible(coreEventEditor);
    addAndMakeVisible(resistanceLabel);
    addAndMakeVisible(coreResistanceEditor);
    addAndMakeVisible(longingLabel);
    addAndMakeVisible(coreLongingEditor);
}

void IntentPanel::Phase0Component::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF0A2540));
}

void IntentPanel::Phase0Component::resized() {
    auto area = getLocalBounds().reduced(10);

    int labelHeight = 20;
    int editorHeight = 60;
    int spacing = 10;

    eventLabel.setBounds(area.removeFromTop(labelHeight));
    coreEventEditor.setBounds(area.removeFromTop(editorHeight));
    area.removeFromTop(spacing);

    resistanceLabel.setBounds(area.removeFromTop(labelHeight));
    coreResistanceEditor.setBounds(area.removeFromTop(editorHeight));
    area.removeFromTop(spacing);

    longingLabel.setBounds(area.removeFromTop(labelHeight));
    coreLongingEditor.setBounds(area.removeFromTop(editorHeight));
}

//==============================================================================
// Phase1Component
//==============================================================================

IntentPanel::Phase1Component::Phase1Component() {
    auto setupLabel = [](juce::Label& label) {
        label.setColour(juce::Label::textColourId, juce::Colour(0xFF00D4FF));
        label.setFont(juce::Font(13, juce::Font::bold));
    };

    setupLabel(moodLabel);
    setupLabel(vulnerabilityLabel);
    setupLabel(narrativeLabel);

    // Mood options
    moodSelector.addItem("Grief", 1);
    moodSelector.addItem("Rage", 2);
    moodSelector.addItem("Longing", 3);
    moodSelector.addItem("Joy", 4);
    moodSelector.addItem("Fear", 5);
    moodSelector.addItem("Hope", 6);
    moodSelector.addItem("Defiance", 7);
    moodSelector.addItem("Acceptance", 8);
    moodSelector.addItem("Confusion", 9);
    moodSelector.addItem("Peace", 10);
    moodSelector.setSelectedId(1);

    // Vulnerability slider
    vulnerabilitySlider.setRange(0.0, 1.0, 0.01);
    vulnerabilitySlider.setValue(0.5);
    vulnerabilitySlider.setSliderStyle(juce::Slider::LinearHorizontal);
    vulnerabilitySlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 50, 20);
    vulnerabilitySlider.setColour(juce::Slider::trackColourId, juce::Colour(0xFF00D4FF));

    // Narrative arc options
    narrativeArcSelector.addItem("Descent into Darkness", 1);
    narrativeArcSelector.addItem("Climbing Out", 2);
    narrativeArcSelector.addItem("Stuck in the Middle", 3);
    narrativeArcSelector.addItem("Transformation", 4);
    narrativeArcSelector.addItem("Circular / Returning", 5);
    narrativeArcSelector.addItem("Fragmented", 6);
    narrativeArcSelector.setSelectedId(1);

    addAndMakeVisible(moodLabel);
    addAndMakeVisible(moodSelector);
    addAndMakeVisible(vulnerabilityLabel);
    addAndMakeVisible(vulnerabilitySlider);
    addAndMakeVisible(narrativeLabel);
    addAndMakeVisible(narrativeArcSelector);
}

void IntentPanel::Phase1Component::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF0A2540));
}

void IntentPanel::Phase1Component::resized() {
    auto area = getLocalBounds().reduced(10);

    int labelHeight = 20;
    int controlHeight = 30;
    int spacing = 15;

    moodLabel.setBounds(area.removeFromTop(labelHeight));
    moodSelector.setBounds(area.removeFromTop(controlHeight));
    area.removeFromTop(spacing);

    vulnerabilityLabel.setBounds(area.removeFromTop(labelHeight));
    vulnerabilitySlider.setBounds(area.removeFromTop(controlHeight));
    area.removeFromTop(spacing);

    narrativeLabel.setBounds(area.removeFromTop(labelHeight));
    narrativeArcSelector.setBounds(area.removeFromTop(controlHeight));
}

//==============================================================================
// Phase2Component
//==============================================================================

IntentPanel::Phase2Component::Phase2Component() {
    auto setupLabel = [](juce::Label& label) {
        label.setColour(juce::Label::textColourId, juce::Colour(0xFF00D4FF));
        label.setFont(juce::Font(13, juce::Font::bold));
    };

    setupLabel(genreLabel);
    setupLabel(keyLabel);
    setupLabel(ruleLabel);

    // Genre options
    genreSelector.addItem("Ambient", 1);
    genreSelector.addItem("Electronic", 2);
    genreSelector.addItem("Indie Folk", 3);
    genreSelector.addItem("Art Pop", 4);
    genreSelector.addItem("Post-Rock", 5);
    genreSelector.addItem("Neo-Soul", 6);
    genreSelector.addItem("Experimental", 7);
    genreSelector.addItem("Orchestral", 8);
    genreSelector.setSelectedId(1);

    // Key options
    keySelector.addItem("C Major", 1);
    keySelector.addItem("A Minor", 2);
    keySelector.addItem("G Major", 3);
    keySelector.addItem("E Minor", 4);
    keySelector.addItem("D Major", 5);
    keySelector.addItem("B Minor", 6);
    keySelector.addItem("F Major", 7);
    keySelector.addItem("D Minor", 8);
    keySelector.addItem("Bb Major", 9);
    keySelector.addItem("G Minor", 10);
    keySelector.addItem("Eb Major", 11);
    keySelector.addItem("C Minor", 12);
    keySelector.setSelectedId(2);

    // Rule breaking options
    auto options = IntentPanel::getRuleBreakingOptions();
    int id = 1;
    for (const auto& opt : options) {
        ruleBreakingSelector.addItem(opt.name, id++);
    }
    ruleBreakingSelector.setSelectedId(1);

    ruleBreakingSelector.onChange = [this] {
        int idx = ruleBreakingSelector.getSelectedId() - 1;
        auto options = IntentPanel::getRuleBreakingOptions();
        if (idx >= 0 && idx < static_cast<int>(options.size())) {
            ruleEffectLabel.setText(options[idx].emotionalEffect, juce::dontSendNotification);
        }
    };

    // Effect label
    ruleEffectLabel.setColour(juce::Label::textColourId, juce::Colour(0xFFFFAA00));
    ruleEffectLabel.setFont(juce::Font(12, juce::Font::italic));
    ruleEffectLabel.setText("Unresolved yearning, endless seeking", juce::dontSendNotification);

    addAndMakeVisible(genreLabel);
    addAndMakeVisible(genreSelector);
    addAndMakeVisible(keyLabel);
    addAndMakeVisible(keySelector);
    addAndMakeVisible(ruleLabel);
    addAndMakeVisible(ruleBreakingSelector);
    addAndMakeVisible(ruleEffectLabel);
}

void IntentPanel::Phase2Component::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF0A2540));
}

void IntentPanel::Phase2Component::resized() {
    auto area = getLocalBounds().reduced(10);

    int labelHeight = 20;
    int controlHeight = 30;
    int spacing = 15;

    genreLabel.setBounds(area.removeFromTop(labelHeight));
    genreSelector.setBounds(area.removeFromTop(controlHeight));
    area.removeFromTop(spacing);

    keyLabel.setBounds(area.removeFromTop(labelHeight));
    keySelector.setBounds(area.removeFromTop(controlHeight));
    area.removeFromTop(spacing);

    ruleLabel.setBounds(area.removeFromTop(labelHeight));
    ruleBreakingSelector.setBounds(area.removeFromTop(controlHeight));
    area.removeFromTop(5);
    ruleEffectLabel.setBounds(area.removeFromTop(20));
}

//==============================================================================
// IntentPanel
//==============================================================================

IntentPanel::IntentPanel() {
    // Title
    auto titleLabel = std::make_unique<juce::Label>();
    titleLabel->setText("Intent", juce::dontSendNotification);
    titleLabel->setFont(juce::Font(18, juce::Font::bold));
    titleLabel->setColour(juce::Label::textColourId, juce::Colour(0xFF00D4FF));
    addAndMakeVisible(*titleLabel);

    // Tabs for phases
    phaseTabs = std::make_unique<juce::TabbedComponent>(juce::TabbedButtonBar::TabsAtTop);
    phaseTabs->setColour(juce::TabbedComponent::backgroundColourId, juce::Colour(0xFF0A2540));
    phaseTabs->setTabBarDepth(30);

    // Add phase tabs
    phaseTabs->addTab("Why", juce::Colour(0xFF0A2540), new Phase0Component(), true);
    phaseTabs->addTab("Feeling", juce::Colour(0xFF0A2540), new Phase1Component(), true);
    phaseTabs->addTab("How", juce::Colour(0xFF0A2540), new Phase2Component(), true);

    addAndMakeVisible(*phaseTabs);

    // Ghost Hands toggle
    ghostHandsToggle = std::make_unique<juce::ToggleButton>("Ghost Hands");
    ghostHandsToggle->setToggleState(true, juce::dontSendNotification);
    ghostHandsToggle->setColour(juce::ToggleButton::textColourId, juce::Colour(0xFF00D4FF));
    addAndMakeVisible(*ghostHandsToggle);

    // Suggest button
    suggestButton = std::make_unique<juce::TextButton>("Ask AI");
    suggestButton->setColour(juce::TextButton::buttonColourId, juce::Colour(0xFF00D4FF));
    suggestButton->setColour(juce::TextButton::textColourOffId, juce::Colour(0xFF0A2540));
    suggestButton->onClick = [this] { requestAISuggestions(); };
    addAndMakeVisible(*suggestButton);
}

IntentPanel::~IntentPanel() = default;

void IntentPanel::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(0xFF0A2540));

    // Border
    g.setColour(juce::Colour(0xFF00D4FF).withAlpha(0.3f));
    g.drawRect(getLocalBounds(), 1);

    // Title background
    g.setColour(juce::Colour(0xFF0D3050));
    g.fillRect(0, 0, getWidth(), 35);
}

void IntentPanel::resized() {
    auto area = getLocalBounds();

    // Title area
    area.removeFromTop(35);

    // Ghost Hands toggle and suggest button at bottom
    auto bottomArea = area.removeFromBottom(40);
    ghostHandsToggle->setBounds(bottomArea.removeFromLeft(120).reduced(5));
    suggestButton->setBounds(bottomArea.removeFromRight(80).reduced(5));

    // Tabs fill remaining space
    phaseTabs->setBounds(area);
}

juce::String IntentPanel::getCoreEvent() const {
    if (auto* phase0 = dynamic_cast<Phase0Component*>(phaseTabs->getTabContentComponent(0))) {
        return phase0->coreEventEditor.getText();
    }
    return {};
}

juce::String IntentPanel::getCoreResistance() const {
    if (auto* phase0 = dynamic_cast<Phase0Component*>(phaseTabs->getTabContentComponent(0))) {
        return phase0->coreResistanceEditor.getText();
    }
    return {};
}

juce::String IntentPanel::getCoreLonging() const {
    if (auto* phase0 = dynamic_cast<Phase0Component*>(phaseTabs->getTabContentComponent(0))) {
        return phase0->coreLongingEditor.getText();
    }
    return {};
}

juce::String IntentPanel::getPrimaryMood() const {
    if (auto* phase1 = dynamic_cast<Phase1Component*>(phaseTabs->getTabContentComponent(1))) {
        return phase1->moodSelector.getText();
    }
    return {};
}

float IntentPanel::getVulnerabilityScale() const {
    if (auto* phase1 = dynamic_cast<Phase1Component*>(phaseTabs->getTabContentComponent(1))) {
        return static_cast<float>(phase1->vulnerabilitySlider.getValue());
    }
    return 0.5f;
}

juce::String IntentPanel::getNarrativeArc() const {
    if (auto* phase1 = dynamic_cast<Phase1Component*>(phaseTabs->getTabContentComponent(1))) {
        return phase1->narrativeArcSelector.getText();
    }
    return {};
}

juce::String IntentPanel::getTechnicalGenre() const {
    if (auto* phase2 = dynamic_cast<Phase2Component*>(phaseTabs->getTabContentComponent(2))) {
        return phase2->genreSelector.getText();
    }
    return {};
}

juce::String IntentPanel::getTechnicalKey() const {
    if (auto* phase2 = dynamic_cast<Phase2Component*>(phaseTabs->getTabContentComponent(2))) {
        return phase2->keySelector.getText();
    }
    return {};
}

juce::String IntentPanel::getRuleToBreak() const {
    if (auto* phase2 = dynamic_cast<Phase2Component*>(phaseTabs->getTabContentComponent(2))) {
        return phase2->ruleBreakingSelector.getText();
    }
    return {};
}

void IntentPanel::requestAISuggestions() {
    // TODO: Integrate with Python bridge / penta_core_music-brain
    // For now, just show a message
    juce::AlertWindow::showMessageBoxAsync(
        juce::MessageBoxIconType::InfoIcon,
        "AI Suggestions",
        "Based on your intent:\n\n"
        "Mood: " + getPrimaryMood() + "\n"
        "Vulnerability: " + juce::String(getVulnerabilityScale() * 100, 0) + "%\n\n"
        "Consider breaking: " + getRuleToBreak() + "\n\n"
        "This creates: " + [this]() {
            auto options = getRuleBreakingOptions();
            int idx = 0;
            if (auto* phase2 = dynamic_cast<Phase2Component*>(phaseTabs->getTabContentComponent(2))) {
                idx = phase2->ruleBreakingSelector.getSelectedId() - 1;
            }
            if (idx >= 0 && idx < static_cast<int>(options.size())) {
                return options[idx].emotionalEffect;
            }
            return juce::String("unknown effect");
        }()
    );
}

void IntentPanel::onSuggestionReceived(const juce::String& category, const juce::String& suggestion) {
    juce::ignoreUnused(category, suggestion);
    // TODO: Update UI with AI suggestions
}

} // namespace iDAW
