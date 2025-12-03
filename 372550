#pragma once

#include <juce_core/juce_core.h>

/**
 * Thin wrapper that will communicate with the Python DAiW runtime.
 * For now it simply simulates a ping.
 */
class BridgeClient
{
public:
    BridgeClient();
    ~BridgeClient();

    /** Attempts to reach the DAiW runtime. */
    bool ping();

    /** TODO: Implement auto-tune request RPC. */
    bool requestAutoTune(const juce::File& inputFile, juce::File& outputFile);

    /** Placeholder chat endpoint. */
    juce::String sendChatMessage(const juce::String& message);

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(BridgeClient)
};

