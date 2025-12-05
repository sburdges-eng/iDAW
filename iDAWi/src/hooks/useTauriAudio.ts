import { useEffect, useCallback } from 'react';
import { useStore } from '../store/useStore';

// Tauri API - optional, will fallback if not available
// Use a dynamic loader for Tauri's invoke API in a RT-safe, ESM-friendly way

let invoke: ((cmd: string, args?: Record<string, unknown>) => Promise<unknown>) | null = null;

// Attempt to dynamically load Tauri's invoke API at runtime (non-crashing fallback)
async function loadTauriInvoke() {
  try {
    // Note: Some Tauri setups use '@tauri-apps/api/tauri' for invoke, others use '@tauri-apps/api/core'
    let tauriApi;
    try {
      tauriApi = await import('@tauri-apps/api/core');
    } catch {
      tauriApi = await import('@tauri-apps/api/tauri'); // fallback for some Tauri scaffolds
    }
    if (typeof tauriApi.invoke === 'function') {
      invoke = tauriApi.invoke;
    } else {
      invoke = null;
    }
  } catch {
    // Tauri not available; fallback to null (no crash)
    invoke = null;
  }
}

loadTauriInvoke(); // Fire and forget; set invoke if/when tauri loads

interface AudioEngineState {
  is_playing: boolean;
  position_samples: number;
  tempo_bpm: number;
  sample_rate: number;
}

export function useTauriAudio() {
  const {
    play,
    stop,
    pause,
    setTempo,
    setPosition,
    isPlaying,
    tempo,
  } = useStore();

  const handlePlay = useCallback(async () => {
    try {
      if (invoke) {
        await invoke('audio_play');
      }
      play();
    } catch (error) {
      console.error('Failed to play:', error);
      play();
    }
  }, [play]);

  const handleStop = useCallback(async () => {
    try {
      if (invoke) {
        await invoke('audio_stop');
      }
      stop();
    } catch (error) {
      console.error('Failed to stop:', error);
      stop();
    }
  }, [stop]);

  const handlePause = useCallback(async () => {
    try {
      if (invoke) {
        await invoke('audio_pause');
      }
      pause();
    } catch (error) {
      console.error('Failed to pause:', error);
      pause();
    }
  }, [pause]);

  const handleSetTempo = useCallback(async (bpm: number) => {
    try {
      if (invoke) {
        await invoke('audio_set_tempo', { bpm });
      }
      setTempo(bpm);
    } catch (error) {
      console.error('Failed to set tempo:', error);
      setTempo(bpm);
    }
  }, [setTempo]);

  const togglePlayPause = useCallback(async () => {
    if (isPlaying) {
      await handlePause();
    } else {
      await handlePlay();
    }
  }, [isPlaying, handlePlay, handlePause]);

  // Poll audio state every 100ms when playing
  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(async () => {
      try {
        if (invoke) {
          const state = await invoke('audio_get_state') as AudioEngineState;
          setPosition(state.position_samples);
        } else {
          // Fallback: simulate position advancement
          setPosition((prev: number) => prev + (tempo / 60) * 44100 * 0.1);
        }
      } catch {
        // Fallback: simulate position advancement
        const currentPosition = useStore.getState().position;
        setPosition(currentPosition + (tempo / 60) * 44100 * 0.1);
      }
    }, 100);

    return () => clearInterval(interval);
  }, [isPlaying, setPosition, tempo]);

  return {
    play: handlePlay,
    stop: handleStop,
    pause: handlePause,
    setTempo: handleSetTempo,
    togglePlayPause,
  };
}
