import React, { useState } from 'react';
import { useStore } from '../../store/useStore';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import clsx from 'clsx';

export const Mixer: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { tracks, updateTrack, selectedTrackId, selectTrack } = useStore();

  if (isCollapsed) {
    return (
      <div className="w-6 bg-ableton-surface border-l border-ableton-border flex flex-col items-center pt-2">
        <button
          className="p-1 hover:bg-ableton-surface-light rounded"
          onClick={() => setIsCollapsed(false)}
          title="Show Mixer"
        >
          <ChevronLeft size={16} />
        </button>
        <div
          className="mt-4 text-xs text-ableton-text-dim"
          style={{ writingMode: 'vertical-rl' }}
        >
          MIXER
        </div>
      </div>
    );
  }

  return (
    <div className="w-auto bg-ableton-surface border-l border-ableton-border flex flex-col">
      {/* Mixer Header */}
      <div className="h-8 border-b border-ableton-border flex items-center px-2 justify-between">
        <span className="text-xs text-ableton-text-dim uppercase tracking-wider">
          Mixer
        </span>
        <button
          className="p-1 hover:bg-ableton-surface-light rounded"
          onClick={() => setIsCollapsed(true)}
          title="Hide Mixer"
        >
          <ChevronRight size={14} />
        </button>
      </div>

      {/* Mixer Channels */}
      <div className="flex-1 flex overflow-x-auto p-2 gap-1">
        {tracks.map((track) => (
          <MixerChannel
            key={track.id}
            track={track}
            isSelected={track.id === selectedTrackId}
            onSelect={() => selectTrack(track.id)}
            onUpdate={(updates) => updateTrack(track.id, updates)}
          />
        ))}

        {/* Master Channel */}
        <MasterChannel />
      </div>
    </div>
  );
};

interface MixerChannelProps {
  track: {
    id: string;
    name: string;
    color: string;
    muted: boolean;
    solo: boolean;
    volume: number;
    pan: number;
  };
  isSelected: boolean;
  onSelect: () => void;
  onUpdate: (updates: { volume?: number; pan?: number }) => void;
}

const MixerChannel: React.FC<MixerChannelProps> = ({
  track,
  isSelected,
  onSelect,
  onUpdate,
}) => {
  // Simulate VU meter level (would come from audio engine)
  const [meterLevel] = useState(() => Math.random() * 0.7 + 0.1);

  return (
    <div
      className={clsx(
        'mixer-channel',
        isSelected && 'bg-ableton-surface-light'
      )}
      onClick={onSelect}
    >
      {/* Track name */}
      <div
        className="text-xs truncate w-full text-center mb-2"
        title={track.name}
      >
        {track.name}
      </div>

      {/* Pan knob */}
      <div className="relative mb-2">
        <div className="text-[10px] text-ableton-text-dim text-center mb-1">
          PAN
        </div>
        <input
          type="range"
          min={-1}
          max={1}
          step={0.01}
          value={track.pan}
          onChange={(e) => onUpdate({ pan: parseFloat(e.target.value) })}
          className="w-12"
          onClick={(e) => e.stopPropagation()}
        />
        <div className="text-[10px] text-ableton-text-dim text-center">
          {track.pan === 0 ? 'C' : track.pan < 0 ? `L${Math.abs(Math.round(track.pan * 50))}` : `R${Math.round(track.pan * 50)}`}
        </div>
      </div>

      {/* VU Meter + Fader */}
      <div className="flex-1 flex items-end gap-1 mb-2">
        {/* VU Meter */}
        <div className="vu-meter h-32">
          <div
            className="vu-meter-bar"
            style={{
              height: `${meterLevel * 100}%`,
              opacity: track.muted ? 0.3 : 1,
            }}
          />
        </div>

        {/* Fader */}
        <div className="h-32 flex flex-col items-center">
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={track.volume}
            onChange={(e) => onUpdate({ volume: parseFloat(e.target.value) })}
            className="h-28 w-4"
            style={{
              writingMode: 'vertical-lr',
              direction: 'rtl',
              WebkitAppearance: 'slider-vertical',
            }}
            onClick={(e) => e.stopPropagation()}
          />
        </div>

        {/* Second VU Meter (stereo) */}
        <div className="vu-meter h-32">
          <div
            className="vu-meter-bar"
            style={{
              height: `${meterLevel * 0.9 * 100}%`,
              opacity: track.muted ? 0.3 : 1,
            }}
          />
        </div>
      </div>

      {/* dB reading */}
      <div className="text-[10px] font-mono text-ableton-text-dim text-center mb-2">
        {track.volume === 0 ? '-∞' : `${Math.round((track.volume - 1) * 40)}dB`}
      </div>

      {/* Color indicator */}
      <div
        className="w-full h-2 rounded-sm"
        style={{ backgroundColor: track.color }}
      />
    </div>
  );
};

const MasterChannel: React.FC = () => {
  const [masterVolume, setMasterVolume] = useState(0.85);
  const meterLevel = 0.75;

  return (
    <div className="mixer-channel bg-ableton-surface-light border-l-2 border-ableton-accent">
      {/* Track name */}
      <div className="text-xs truncate w-full text-center mb-2 font-medium text-ableton-accent">
        MASTER
      </div>

      {/* Spacer for pan area */}
      <div className="h-12 mb-2" />

      {/* VU Meter + Fader */}
      <div className="flex-1 flex items-end gap-1 mb-2">
        {/* VU Meter L */}
        <div className="vu-meter h-32">
          <div
            className="vu-meter-bar"
            style={{ height: `${meterLevel * 100}%` }}
          />
        </div>

        {/* Fader */}
        <div className="h-32 flex flex-col items-center">
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={masterVolume}
            onChange={(e) => setMasterVolume(parseFloat(e.target.value))}
            className="h-28 w-4"
            style={{
              writingMode: 'vertical-lr',
              direction: 'rtl',
              WebkitAppearance: 'slider-vertical',
            }}
          />
        </div>

        {/* VU Meter R */}
        <div className="vu-meter h-32">
          <div
            className="vu-meter-bar"
            style={{ height: `${meterLevel * 0.95 * 100}%` }}
          />
        </div>
      </div>

      {/* dB reading */}
      <div className="text-[10px] font-mono text-ableton-text-dim text-center mb-2">
        {masterVolume === 0 ? '-∞' : `${Math.round((masterVolume - 1) * 40)}dB`}
      </div>

      {/* Color indicator */}
      <div className="w-full h-2 rounded-sm bg-ableton-accent" />
    </div>
  );
};
