import { useEffect, useCallback } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { useStore } from '../store/useStore';

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
      await invoke('audio_play');
      play();
    } catch (error) {
      console.error('Failed to play:', error);
      // Fallback to local state if Tauri is not available
      play();
    }
  }, [play]);

  const handleStop = useCallback(async () => {
    try {
      await invoke('audio_stop');
      stop();
    } catch (error) {
      console.error('Failed to stop:', error);
      stop();
    }
  }, [stop]);

  const handlePause = useCallback(async () => {
    try {
      await invoke('audio_pause');
      pause();
    } catch (error) {
      console.error('Failed to pause:', error);
      pause();
    }
  }, [pause]);

  const handleSetTempo = useCallback(async (bpm: number) => {
    try {
      await invoke('audio_set_tempo', { bpm });
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
        const state = await invoke<AudioEngineState>('audio_get_state');
        setPosition(state.position_samples);
      } catch {
        // Fallback: simulate position advancement
        setPosition((prev: number) => prev + (tempo / 60) * 44100 * 0.1);
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
