# iDAW_Core CMakeLists.txt
# Intent-Driven Digital Audio Workstation

cmake_minimum_required(VERSION 3.22)
project(iDAW VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find JUCE (assuming it's available via the main project or installed)
# If JUCE is not found, this will fail gracefully
find_package(JUCE CONFIG QUIET)

if(NOT JUCE_FOUND)
    message(STATUS "JUCE not found via find_package, looking for juce subdirectory...")
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../JUCE")
        add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../JUCE ${CMAKE_CURRENT_BINARY_DIR}/JUCE)
    elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/JUCE")
        add_subdirectory(JUCE)
    else()
        message(FATAL_ERROR "JUCE not found. Please install JUCE or set JUCE_DIR.")
    endif()
endif()

# ==============================================================================
# iDAW Desktop Application
# ==============================================================================

juce_add_gui_app(iDAW
    PRODUCT_NAME "iDAW"
    VERSION ${PROJECT_VERSION}
    COMPANY_NAME "iDAW"
    BUNDLE_ID "com.idaw.app"
    ICON_BIG ""
    ICON_SMALL ""
    DOCUMENT_EXTENSIONS idaw
    NEEDS_CURL FALSE
    NEEDS_WEB_BROWSER FALSE
)

# Source files
target_sources(iDAW PRIVATE
    # Application
    application/MainApplication.cpp
    application/MainWindow.cpp
    application/PreferencesManager.cpp

    # Transport
    transport/TransportState.cpp
    transport/TransportBar.cpp

    # Tracks
    tracks/Track.cpp
    tracks/TrackList.cpp
    tracks/Clip.cpp
    tracks/PluginSlot.cpp

    # Mixer
    mixer/MixerPanel.cpp

    # Arrangement
    arrangement/ArrangementView.cpp

    # Intent (AI features)
    intent/IntentPanel.cpp

    # Session
    session/Project.cpp

    # Existing iDAW components (if available)
    # include/DreamStateComponent.h
    # include/PythonBridge.h
    # include/MemoryManager.h
)

# Include directories
target_include_directories(iDAW PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/application
    ${CMAKE_CURRENT_SOURCE_DIR}/transport
    ${CMAKE_CURRENT_SOURCE_DIR}/tracks
    ${CMAKE_CURRENT_SOURCE_DIR}/mixer
    ${CMAKE_CURRENT_SOURCE_DIR}/arrangement
    ${CMAKE_CURRENT_SOURCE_DIR}/intent
    ${CMAKE_CURRENT_SOURCE_DIR}/session
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# JUCE modules
target_link_libraries(iDAW PRIVATE
    juce::juce_audio_basics
    juce::juce_audio_devices
    juce::juce_audio_formats
    juce::juce_audio_processors
    juce::juce_audio_utils
    juce::juce_core
    juce::juce_data_structures
    juce::juce_events
    juce::juce_graphics
    juce::juce_gui_basics
    juce::juce_gui_extra
    juce::juce_opengl
    juce::juce_recommended_config_flags
    juce::juce_recommended_warning_flags
)

# Compile definitions
target_compile_definitions(iDAW PRIVATE
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_DISPLAY_SPLASH_SCREEN=0
    JUCE_REPORT_APP_USAGE=0
    JUCE_PLUGINHOST_VST3=1
    JUCE_PLUGINHOST_AU=1
)

# ==============================================================================
# iDAW Plugins (existing art-themed plugins)
# ==============================================================================

# Add plugin subdirectories if they exist
set(PLUGIN_DIRS
    plugins/Pencil
    plugins/Eraser
    plugins/Palette
    plugins/Smudge
    plugins/Press
    plugins/Trace
    plugins/Parrot
    plugins/Stencil
    plugins/Chalk
    plugins/Brush
    plugins/Stamp
)

foreach(plugin_dir ${PLUGIN_DIRS})
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${plugin_dir}/CMakeLists.txt")
        add_subdirectory(${plugin_dir})
    endif()
endforeach()

# ==============================================================================
# Installation
# ==============================================================================

install(TARGETS iDAW
    RUNTIME DESTINATION bin
    BUNDLE DESTINATION .
)

# ==============================================================================
# Summary
# ==============================================================================

message(STATUS "")
message(STATUS "=== iDAW Build Configuration ===")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "")
