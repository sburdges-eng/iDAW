import { useEffect, useState } from 'react';
import { useMusicBrain } from '../../hooks/useMusicBrain';

// Category color mappings with standard Tailwind-safe class tokens.
// Uses lowercase keys to match backend intent_schema.py (AffectState enum)
export const categoryColors = {
  grief: "bg-blue-500",
  joy: "bg-yellow-500",
  anger: "bg-red-500",
  fear: "bg-purple-500",
  love: "bg-pink-500",
} as const;

export const categoryHoverColors = {
  grief: "hover:border-blue-500",
  joy: "hover:border-yellow-500",
  anger: "hover:border-red-500",
  fear: "hover:border-purple-500",
  love: "hover:border-pink-500",
} as const;

export type EmotionCategory = keyof typeof categoryColors;

export interface Emotion {
  name: string;
  category: EmotionCategory;
  intensity: number; // 0.0 - 1.0
}

// Default emotions matching backend schema
export const defaultEmotions: Emotion[] = [
  { name: "Grief", category: "grief", intensity: 0.7 },
  { name: "Longing", category: "grief", intensity: 0.6 },
  { name: "Melancholy", category: "grief", intensity: 0.5 },

  { name: "Joy", category: "joy", intensity: 0.9 },
  { name: "Hope", category: "joy", intensity: 0.7 },
  { name: "Peace", category: "joy", intensity: 0.6 },

  { name: "Anger", category: "anger", intensity: 0.85 },
  { name: "Restlessness", category: "anger", intensity: 0.5 },

  { name: "Fear", category: "fear", intensity: 0.8 },
  { name: "Anxiety", category: "fear", intensity: 0.5 },

  { name: "Love", category: "love", intensity: 0.8 },
  { name: "Tenderness", category: "love", intensity: 0.4 },
];

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
      .then((data) => setEmotions(data as Emotion[]))
      .finally(() => setIsLoading(false));
  }, [getEmotions]);

  const handleSelect = (emotion: string) => {
    // Only update internal state if not controlled by prop
    if (selectedEmotionProp === undefined) {
      setInternalSelectedEmotion(emotion);
    }
    onSelectEmotion(emotion);
  };

  const getCategoryColor = (category: string): string => {
    return categoryColors[category as EmotionCategory] || 'bg-ableton-text-dim';
  };

  const getCategoryHoverColor = (category: string): string => {
    return categoryHoverColors[category as EmotionCategory] || '';
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
        {emotions.map((emotion) => (
          <button
            key={emotion.name}
            type="button"
            onClick={() => handleSelect(emotion.name)}
            className={`
              p-4 rounded border transition-all text-left
              ${selectedEmotion === emotion.name
                ? 'border-ableton-accent bg-ableton-accent bg-opacity-20 scale-105'
                : `border-ableton-border hover:bg-ableton-surface ${getCategoryHoverColor(emotion.category)}`
              }
            `}
          >
            <div
              className={`w-3 h-3 rounded-full mb-2 ${getCategoryColor(emotion.category)}`}
              style={{ opacity: 0.5 + emotion.intensity * 0.5 }}
            />
            <div className="text-sm font-medium">{emotion.name}</div>
            <div className="text-xs text-ableton-text-dim capitalize">{emotion.category}</div>
          </button>
        ))}
      </div>
    </div>
  );
};
