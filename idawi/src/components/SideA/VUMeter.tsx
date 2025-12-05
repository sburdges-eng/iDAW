import React, { useEffect, useState } from 'react';

interface VUMeterProps {
  level: number; // 0.0 to 1.0
  peak?: number;
}

export const VUMeter: React.FC<VUMeterProps> = ({ level, peak = 0 }) => {
  const [peakHold, setPeakHold] = useState(0);
  const timeoutRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  const peakHoldRef = React.useRef(0);

  // Keep ref in sync with state
  useEffect(() => {
    peakHoldRef.current = peakHold;
  }, [peakHold]);

  useEffect(() => {
    // Use ref to get current peakHold value without adding it to dependency array
    if (peak > peakHoldRef.current) {
      // Clear any existing timeout
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      setPeakHold(peak);
      // Reset peak after 1 second
      timeoutRef.current = setTimeout(() => {
        setPeakHold(0);
        timeoutRef.current = null;
      }, 1000);
    }
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    };
  }, [peak]);

  const getColor = (value: number) => {
    if (value > 0.9) return 'bg-ableton-red';
    if (value > 0.7) return 'bg-ableton-yellow';
    return 'bg-ableton-green';
  };

  return (
    <div className="relative h-32 w-4 bg-ableton-bg border border-ableton-border rounded overflow-hidden">
      {/* Level bar */}
      <div
        className={`absolute bottom-0 w-full transition-all duration-75 ${getColor(level)}`}
        style={{ height: `${level * 100}%` }}
      />

      {/* Peak indicator */}
      {peakHold > 0 && (
        <div
          className="absolute w-full h-1 bg-ableton-red"
          style={{ bottom: `${peakHold * 100}%` }}
        />
      )}

      {/* Scale marks */}
      {[0.9, 0.7, 0.5, 0.3].map((mark) => (
        <div
          key={mark}
          className="absolute w-full h-px bg-ableton-border opacity-50"
          style={{ bottom: `${mark * 100}%` }}
        />
      ))}
    </div>
  );
};
