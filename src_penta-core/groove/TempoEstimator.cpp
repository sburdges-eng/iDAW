#include "penta/groove/TempoEstimator.h"
#include <algorithm>
#include <cmath>

namespace penta::groove {

TempoEstimator::TempoEstimator(const Config& config)
    : config_(config)
    , currentTempo_(120.0f)
    , confidence_(0.0f)
    , lastOnsetPosition_(0)
{
    onsetHistory_.reserve(config.historySize);
    // TODO: Week 10 implementation - autocorrelation-based tempo estimation
}

void TempoEstimator::addOnset(uint64_t samplePosition) noexcept {
    onsetHistory_.push_back(samplePosition);
    
    // Keep only recent history
    if (onsetHistory_.size() > config_.historySize) {
        onsetHistory_.erase(onsetHistory_.begin());
    }
    
    lastOnsetPosition_ = samplePosition;
    
    // Estimate tempo if we have enough onsets
    if (onsetHistory_.size() >= 4) {
        estimateTempo();
    }
}

uint64_t TempoEstimator::getSamplesPerBeat() const noexcept {
    if (currentTempo_ <= 0.0f) return 0;
    return static_cast<uint64_t>((60.0 * config_.sampleRate) / currentTempo_);
}

void TempoEstimator::updateConfig(const Config& config) noexcept {
    config_ = config;
    onsetHistory_.reserve(config.historySize);
}

void TempoEstimator::reset() noexcept {
    onsetHistory_.clear();
    currentTempo_ = 120.0f;
    confidence_ = 0.0f;
    lastOnsetPosition_ = 0;
}

void TempoEstimator::estimateTempo() noexcept {
    if (onsetHistory_.size() < 4) {
        return;  // Need at least 4 onsets
    }
    
    // Calculate inter-onset intervals (IOI)
    std::vector<float> intervals;
    intervals.reserve(onsetHistory_.size() - 1);
    
    for (size_t i = 1; i < onsetHistory_.size(); ++i) {
        uint64_t ioi = onsetHistory_[i] - onsetHistory_[i - 1];
        // Convert to seconds
        float ioiSeconds = static_cast<float>(ioi) / static_cast<float>(config_.sampleRate);
        intervals.push_back(ioiSeconds);
    }
    
    // Find most common interval using autocorrelation
    float bestInterval = autocorrelate(intervals);
    
    if (bestInterval > 0.0f) {
        // Convert interval to BPM
        float estimatedTempo = 60.0f / bestInterval;
        
        // Clamp to valid range
        estimatedTempo = std::max(config_.minTempo, std::min(config_.maxTempo, estimatedTempo));
        
        // Apply adaptive filtering
        currentTempo_ = currentTempo_ * (1.0f - config_.adaptationRate) + 
                        estimatedTempo * config_.adaptationRate;
        
        // Update confidence based on consistency of intervals
        float variance = 0.0f;
        float mean = bestInterval;
        for (float interval : intervals) {
            float diff = interval - mean;
            variance += diff * diff;
        }
        variance /= intervals.size();
        
        // Higher confidence for lower variance
        confidence_ = 1.0f / (1.0f + variance * 10.0f);
        confidence_ = std::min(1.0f, confidence_);
    }
}

float TempoEstimator::autocorrelate(const std::vector<float>& intervals) const noexcept {
    if (intervals.empty()) {
        return 0.0f;
    }
    
    // Simple approach: find the median interval as the most stable tempo indicator
    std::vector<float> sortedIntervals = intervals;
    std::sort(sortedIntervals.begin(), sortedIntervals.end());
    
    // Return median interval
    size_t medianIdx = sortedIntervals.size() / 2;
    if (sortedIntervals.size() % 2 == 0 && sortedIntervals.size() > 1) {
        return (sortedIntervals[medianIdx - 1] + sortedIntervals[medianIdx]) / 2.0f;
    } else {
        return sortedIntervals[medianIdx];
    }
}

} // namespace penta::groove
