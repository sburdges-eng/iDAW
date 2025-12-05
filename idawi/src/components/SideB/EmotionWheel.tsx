import React, { useEffect, useState } from 'react';
import { useMusicBrain } from '../../hooks/useMusicBrain';

// Category color mappings with standard Tailwind-safe class tokens.
export const categoryColors = {
  grief: "bg-[color:var(--emotion-grief)]",
  joy: "bg-[color:var(--emotion-joy)]",
  anger: "bg-[color:var(--emotion-anger)]",
  fear: "bg-[color:var(--emotion-fear)]",
  love: "bg-[color:var(--emotion-love)]",
} as const;

export const categoryHoverColors = {
  grief: "hover:bg-[color:var(--emotion-grief)] hover:bg-opacity-10",
  joy: "hover:bg-[color:var(--emotion-joy)] hover:bg-opacity-10",
  anger: "hover:bg-[color:var(--emotion-anger)] hover:bg-opacity-10",
  fear: "hover:bg-[color:var(--emotion-fear)] hover:bg-opacity-10",
  love: "hover:bg-[color:var(--emotion-love)] hover:bg-opacity-10",
} as const;

export type EmotionCategory = keyof typeof categoryColors;

export type Emotion = {
  name: string;
  category: EmotionCategory;
  intensity: number; // 0.0 - 1.0
};

interface EmotionWheelProps {
  onSelectEmotion: (emotion: string) => void;
  selectedEmotion?: string | null;
}

export const EmotionWheel = ({ onSelectEmotion, selectedEmotion: selectedEmotionProp }: EmotionWheelProps): JSX.Element => {
  const [emotions, setEmotions] = useState<Emotion[]>([]);
  const [internalSelectedEmotion, setInternalSelectedEmotion] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { getEmotions } = useMusicBrain();

  // Use prop if provided, otherwise use internal state
  const selectedEmotion = selectedEmotionProp !== undefined ? selectedEmotionProp : internalSelectedEmotion;

  useEffect(() => {
    setIsLoading(true);
    getEmotions()
      .then(setEmotions)
      .finally(() => setIsLoading(false));
  }, [getEmotions]);

  const handleSelect = (emotion: string) => {
    // Only update internal state if not controlled by prop
    if (selectedEmotionProp === undefined) {
      setInternalSelectedEmotion(emotion);
    }
    onSelectEmotion(emotion);
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-bold mb-4">What are you feeling?</h2>
        <div className="grid grid-cols-3 gap-3">
          {[...Array(9)].map((_, i) => (
            <div
              key={i}
              className="p-4 rounded border border-ableton-border animate-pulse bg-ableton-surface"
            >
              <div className="w-3 h-3 rounded-full bg-ableton-border mb-2" />
              <div className="h-4 bg-ableton-border rounded w-3/4 mb-1" />
              <div className="h-3 bg-ableton-border rounded w-1/2" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">What are you feeling?</h2>
      <p className="text-ableton-text-dim text-sm mb-6">
        Select an emotion to begin the interrogation process
      </p>

      <div className="grid grid-cols-3 gap-3">
        {emotions.map((emotion: Emotion) => (
          <button
            key={emotion.name}
            onClick={() => handleSelect(emotion.name)}
            className={`
              p-4 rounded border transition-all text-left
              ${selectedEmotion === emotion.name
                ? 'border-ableton-accent bg-ableton-accent bg-opacity-20 scale-105'
                : `border-ableton-border hover:bg-ableton-surface ${categoryHoverColors[emotion.category] || ''}`
              }
            `}
          >
            <div
              className={`w-3 h-3 rounded-full mb-2 ${categoryColors[emotion.category] || 'bg-ableton-text-dim'}`}
              style={{ opacity: 0.5 + emotion.intensity * 0.5 }}
            />
            <div className="text-sm font-medium">{emotion.name}</div>
            <div className="text-xs text-ableton-text-dim">{emotion.category}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

