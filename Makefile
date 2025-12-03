# Makefile for building DAiW Bridge Plugin Tests
# 
# Usage:
#   make          - Build tests
#   make test     - Build and run tests
#   make clean    - Clean build files

CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -g
JUCE_PATH = /path/to/JUCE  # Update this path

# Source files
PLUGIN_SOURCES = PluginProcessor.cpp PluginEditor.cpp
TEST_SOURCES = PluginProcessorTest.cpp PluginEditorTest.cpp OSCCommunicationTest.cpp
ALL_SOURCES = $(PLUGIN_SOURCES) $(TEST_SOURCES) RunTests.cpp

# Object files
OBJECTS = $(ALL_SOURCES:.cpp=.o)

# Include directories
INCLUDES = -I$(JUCE_PATH)/modules

# Libraries (adjust for your platform)
LIBS = -framework CoreFoundation -framework CoreAudio

# Test executable
TARGET = DAiWBridgeTests

.PHONY: all test clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS) $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

test: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJECTS) $(TARGET)

