# CMakeLists.txt for DAiW Bridge Plugin Tests
# 
# This file provides an alternative build system for testing
# if you prefer CMake over Projucer-generated projects

cmake_minimum_required(VERSION 3.15)
project(DAiWBridgeTests)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find JUCE
find_package(JUCE CONFIG REQUIRED)

# Add Catch2 (optional, for testing framework)
# find_package(Catch2 3 REQUIRED)

# Source files
set(PLUGIN_SOURCES
    PluginProcessor.cpp
    PluginProcessor.h
    PluginEditor.cpp
    PluginEditor.h
)

set(TEST_SOURCES
    PluginProcessorTest.cpp
    PluginEditorTest.cpp
    OSCCommunicationTest.cpp
)

# Create test executable
add_executable(DAiWBridgeTests
    ${TEST_SOURCES}
    ${PLUGIN_SOURCES}
)

# Link JUCE modules
target_link_libraries(DAiWBridgeTests
    PRIVATE
    JUCE::juce_audio_basics
    JUCE::juce_audio_processors
    JUCE::juce_core
    JUCE::juce_data_structures
    JUCE::juce_events
    JUCE::juce_graphics
    JUCE::juce_gui_basics
    JUCE::juce_osc
)

# Optional: Link Catch2 if available
# target_link_libraries(DAiWBridgeTests PRIVATE Catch2::Catch2)

# Include directories
target_include_directories(DAiWBridgeTests
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Compiler options
if(MSVC)
    target_compile_options(DAiWBridgeTests PRIVATE /W4)
else()
    target_compile_options(DAiWBridgeTests PRIVATE -Wall -Wextra -Wpedantic)
endif()

# Optional: Add Catch2 test discovery
# include(Catch)
# catch_discover_tests(DAiWBridgeTests)

