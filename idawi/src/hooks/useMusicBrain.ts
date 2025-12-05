// Music Brain integration hook
// In production, this would use Tauri's invoke to call Python
import { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import type { Emotion, EmotionCategory } from '../components/SideB/EmotionWheel';

interface RuleBreakSuggestion {
  rule: string;
  effect: string;
  use_when: string;
  justification: string;
}

interface ProcessIntentResult {
  harmony: string[];
  tempo: number;
  key: string;
  mixer_params: Record<string, number | string>;
}

// Default emotions matching backend intent_schema.py (lowercase categories)
const defaultEmotions: Emotion[] = [
  // Grief category (maps to backend AffectState: grief, longing, melancholy)
  { name: 'Grief', category: 'grief', intensity: 0.9 },
  { name: 'Melancholy', category: 'grief', intensity: 0.6 },
  { name: 'Longing', category: 'grief', intensity: 0.7 },
  
  // Joy category (maps to backend AffectState: hope, euphoria)
  { name: 'Joy', category: 'joy', intensity: 0.8 },
  { name: 'Euphoria', category: 'joy', intensity: 1.0 },
  { name: 'Hope', category: 'joy', intensity: 0.6 },
  
  // Anger category (maps to backend AffectState: rage, defiance)
  { name: 'Rage', category: 'anger', intensity: 1.0 },
  { name: 'Frustration', category: 'anger', intensity: 0.6 },
  { name: 'Defiance', category: 'anger', intensity: 0.8 },
  
  // Fear category (maps to backend AffectState: anxiety, dissociation)
  { name: 'Terror', category: 'fear', intensity: 1.0 },
  { name: 'Anxiety', category: 'fear', intensity: 0.6 },
  { name: 'Dread', category: 'fear', intensity: 0.8 },
  
  // Love category (maps to backend AffectState: tenderness, nostalgia)
  { name: 'Passion', category: 'love', intensity: 0.9 },
  { name: 'Tenderness', category: 'love', intensity: 0.5 },
  { name: 'Devotion', category: 'love', intensity: 0.8 },
];

// Rule-breaking suggestions based on emotions (keys match emotion names)
const ruleBreakingDatabase: Record<string, RuleBreakSuggestion[]> = {
  Grief: [
    {
      rule: 'HARMONY_AvoidTonicResolution',
      effect: 'Creates unresolved yearning that mirrors emotional state',
      use_when: 'The listener should feel the loss is still unprocessed',
      justification: 'Grief rarely resolves cleanly. Music that refuses resolution honors that truth.',
    },
    {
      rule: 'ARRANGEMENT_BuriedVocals',
      effect: 'Creates dissociation, words half-heard like fading memories',
      use_when: 'The subject is too painful to confront directly',
      justification: 'Sometimes the truth is easier to bear when obscured.',
    },
  ],
  Anxiety: [
    {
      rule: 'RHYTHM_ConstantDisplacement',
      effect: 'Never lets listener settle into comfortable expectation',
      use_when: 'Representing intrusive thoughts or restlessness',
      justification: 'Anxiety never follows a predictable pattern.',
    },
    {
      rule: 'HARMONY_UnresolvedDissonance',
      effect: 'Creates tension that never fully releases',
      use_when: 'Showing the impossibility of finding peace',
      justification: 'The anxious mind cannot find resolution.',
    },
  ],
  Rage: [
    {
      rule: 'ARRANGEMENT_ExtremeDynamicRange',
      effect: 'Jarring shifts that mirror emotional volatility',
      use_when: 'The anger comes in unpredictable waves',
      justification: 'Rage rarely announces itself politely.',
    },
    {
      rule: 'PRODUCTION_Distortion',
      effect: 'Traditional form breaks down as control is lost',
      use_when: 'Representing loss of composure',
      justification: 'Anger destroys structure by nature.',
    },
  ],
  Joy: [
    {
      rule: 'HARMONY_ModalInterchange',
      effect: 'Unexpected brightness from borrowed chords',
      use_when: 'Joy that contains complexity and depth',
      justification: 'Real joy often comes from unexpected places.',
    },
  ],
  Passion: [
    {
      rule: 'PRODUCTION_PitchImperfection',
      effect: 'Vulnerability through imperfect tuning',
      use_when: 'Love that is honest and unpolished',
      justification: 'Perfect pitch is a lie we tell ourselves.',
    },
  ],
  Longing: [
    {
      rule: 'HARMONY_AvoidTonicResolution',
      effect: 'Creates unresolved yearning',
      use_when: 'The desire remains unfulfilled',
      justification: 'Longing by definition never arrives.',
    },
    {
      rule: 'MELODY_AvoidResolution',
      effect: 'Melodic phrases that never complete',
      use_when: 'Representing reaching for something just out of grasp',
      justification: 'The melody mirrors the emotional incompleteness.',
    },
  ],
  Defiance: [
    {
      rule: 'HARMONY_ParallelMotion',
      effect: 'Bold parallel fifths that break classical rules',
      use_when: 'Representing rebellion against norms',
      justification: 'Defiance means breaking the rules on purpose.',
    },
  ],
};

export function useMusicBrain() {
  const [isLoading, setIsLoading] = useState(false);
  const isMountedRef = useRef(true);

  // Track mount status to prevent state updates after unmount
  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  // Safe state setter that checks if component is still mounted
  const safeSetIsLoading = useCallback((value: boolean) => {
    if (isMountedRef.current) {
      setIsLoading(value);
    }
  }, []);

  const getEmotions = useCallback(async (): Promise<Emotion[]> => {
    safeSetIsLoading(true);
    try {
      // In production: return invoke('music_brain_command', { command: 'get_emotions', args: {} });
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            safeSetIsLoading(false);
            resolve(defaultEmotions);
          } catch (error) {
            safeSetIsLoading(false);
            reject(error);
          }
        }, 300);
      });
    } catch (error) {
      safeSetIsLoading(false);
      throw error;
    }
  }, [safeSetIsLoading]);

  const suggestRuleBreak = useCallback(async (emotion: string): Promise<RuleBreakSuggestion[]> => {
    safeSetIsLoading(true);
    try {
      // In production: return invoke('music_brain_command', { command: 'suggest_rule_break', args: { emotion } });
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            const suggestions = ruleBreakingDatabase[emotion] || [
              {
                rule: 'HARMONY_ModalInterchange',
                effect: 'Unexpected harmonic color',
                use_when: 'You want to surprise the listener',
                justification: 'Breaking expectations creates emotional impact.',
              },
            ];
            safeSetIsLoading(false);
            resolve(suggestions);
          } catch (error) {
            safeSetIsLoading(false);
            reject(error);
          }
        }, 500);
      });
    } catch (error) {
      safeSetIsLoading(false);
      throw error;
    }
  }, [safeSetIsLoading]);

  const processIntent = useCallback(async (intent?: Record<string, unknown>): Promise<ProcessIntentResult> => {
    safeSetIsLoading(true);
    try {
      // In production: return invoke('music_brain_command', { command: 'process_intent', args: { intent } });
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            // Generate contextual results based on intent
            const intentData = intent || {};
            const emotion = (intentData.song_intent as Record<string, string>)?.mood_primary || 'neutral';
            const key = (intentData.technical_constraints as Record<string, string>)?.technical_key || 'C';

            // Harmony progressions by emotion (matches backend AFFECT_MODE_MAP)
            const harmonyByEmotion: Record<string, string[]> = {
              Grief: ['Am', 'F', 'C', 'G'],
              Anxiety: ['Dm', 'Am/E', 'Bb', 'F/A'],
              Rage: ['Em', 'C', 'G', 'D'],
              Joy: ['C', 'G', 'Am', 'F'],
              Passion: ['F', 'Am', 'Dm', 'C'],
              Longing: ['Am', 'Em', 'F', 'G'],
              Defiance: ['Em', 'G', 'D', 'C'],
              Hope: ['C', 'F', 'Am', 'G'],
            };

            // Tempo ranges by emotion (matches backend AFFECT_MODE_MAP)
            const tempoByEmotion: Record<string, number> = {
              Grief: 72,
              Anxiety: 140,
              Rage: 160,
              Joy: 120,
              Passion: 90,
              Longing: 75,
              Defiance: 130,
              Hope: 110,
            };

            safeSetIsLoading(false);
            resolve({
              harmony: harmonyByEmotion[emotion] || ['C', 'Am', 'F', 'G'],
              tempo: tempoByEmotion[emotion] || 120,
              key,
              mixer_params: {
                reverb: emotion === 'Grief' || emotion === 'Longing' ? 0.7 : 0.3,
                delay: emotion === 'Anxiety' ? 0.5 : 0.2,
                compression: emotion === 'Rage' || emotion === 'Defiance' ? 0.8 : 0.4,
                warmth: emotion === 'Passion' || emotion === 'Hope' ? 0.6 : 0.3,
              },
            });
          } catch (error) {
            safeSetIsLoading(false);
            reject(error);
          }
        }, 800);
      });
    } catch (error) {
      safeSetIsLoading(false);
      throw error;
    }
  }, [safeSetIsLoading]);

  // Memoize the return object to prevent unnecessary re-renders
  return useMemo(
    () => ({
      getEmotions,
      suggestRuleBreak,
      processIntent,
      isLoading,
    }),
    [getEmotions, suggestRuleBreak, processIntent, isLoading]
  );
}
