import React, { useState, useEffect } from 'react';
import { useStore } from '../../store/useStore';
import { VUMeter } from './VUMeter';
import { Knob } from './Knob';

export const Mixer: React.FC = () => {
  const { tracks, updateTrack } = useStore();
  const [levels, setLevels] = useState<Record<string, number>>({});

  // Simulate audio levels (would come from audio engine in production)
  useEffect(() => {
    const interval = setInterval(() => {
      const newLevels: Record<string, number> = {};
      tracks.forEach(track => {
        if (!track.muted) {
          newLevels[track.id] = Math.random() * 0.8; // Random level for demo
        } else {
          newLevels[track.id] = 0;
        }
      });
      setLevels(newLevels);
    }, 100);

    return () => clearInterval(interval);
  }, [tracks]);

  return (
    <div className="h-full bg-ableton-surface border-l border-ableton-border flex overflow-x-auto">
      {tracks.map((track) => (
        <div key={track.id} className="mixer-channel">
          {/* Track Name */}
          <div className="text-xs text-center mb-2 truncate w-full">
            {track.name}
          </div>

          {/* Pan Knob */}
          <Knob
            value={track.pan}
            onChange={(val) => updateTrack(track.id, { pan: val })}
            label="Pan"
            min={-1}
            max={1}
          />

          {/* VU Meter */}
          <div className="my-4 flex justify-center">
            <VUMeter level={levels[track.id] || 0} />
          </div>

          {/* Fader */}
          <div className="flex-1 flex items-center justify-center">
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={track.volume}
              onChange={(e) => updateTrack(track.id, { volume: parseFloat(e.target.value) })}
              className="fader-vertical"
            />
          </div>

          {/* Mute/Solo Buttons */}
          <div className="flex gap-1 mt-2">
            <button
              className={`px-2 py-1 text-xs rounded ${
                track.muted ? 'btn-ableton-active' : 'btn-ableton'
              }`}
              onClick={() => updateTrack(track.id, { muted: !track.muted })}
            >
              M
            </button>
            <button
              className={`px-2 py-1 text-xs rounded ${
                track.solo ? 'btn-ableton-active' : 'btn-ableton'
              }`}
              onClick={() => updateTrack(track.id, { solo: !track.solo })}
            >
              S
            </button>
          </div>

          {/* Volume Display */}
          <div className="text-xs text-ableton-text-dim mt-2">
            {Math.round(track.volume * 100)}%
          </div>
        </div>
      ))}

      {/* Master Channel */}
      <div className="mixer-channel border-l-2 border-ableton-accent">
        <div className="text-xs text-center mb-2 font-bold">Master</div>
        <VUMeter level={Math.max(...Object.values(levels), 0)} />
        <div className="flex-1 flex items-center justify-center mt-4">
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            defaultValue="0.8"
            className="fader-vertical"
          />
        </div>
      </div>
    </div>
  );
};
