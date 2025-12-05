import React, { useRef, useEffect, useCallback, useMemo } from 'react';
import { useStore } from '../../store/useStore';

export const Timeline: React.FC = () => {
  const { tracks, currentTime, isPlaying, tempo, timeSignature } = useStore();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const staticCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const lastStaticDrawRef = useRef<string>('');

  // Calculate grid based on tempo and time signature
  const beatsPerBar = timeSignature[0];
  const pixelsPerBeat = 50;
  const pixelsPerBar = pixelsPerBeat * beatsPerBar;

  // Memoize track data for comparison
  const trackKey = useMemo(() => {
    return JSON.stringify(tracks.map(t => ({
      name: t.name,
      color: t.color,
      clips: t.clips.map(c => ({ name: c.name, startTime: c.startTime, duration: c.duration }))
    })));
  }, [tracks]);

  // Draw static content (grid and tracks) - only when tracks/tempo/timeSignature change
  const drawStaticContent = useCallback((ctx: CanvasRenderingContext2D, width: number, height: number) => {
    // Clear and draw background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    // Draw grid lines
    const bars = Math.ceil(width / pixelsPerBar);
    for (let i = 0; i <= bars * beatsPerBar; i++) {
      const x = i * pixelsPerBeat;
      const isBar = i % beatsPerBar === 0;

      ctx.strokeStyle = isBar ? '#444' : '#2a2a2a';
      ctx.lineWidth = isBar ? 2 : 1;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();

      // Bar numbers
      if (isBar) {
        ctx.fillStyle = '#666';
        ctx.font = '10px monospace';
        ctx.fillText(`${Math.floor(i / beatsPerBar) + 1}`, x + 4, 12);
      }
    }

    // Draw tracks
    const trackHeight = Math.min(80, (height - 20) / Math.max(tracks.length, 1));
    tracks.forEach((track, index) => {
      const y = 20 + index * trackHeight;

      // Track background
      ctx.fillStyle = track.color + '40';
      ctx.fillRect(0, y, width, trackHeight - 2);

      // Track name
      ctx.fillStyle = '#fff';
      ctx.font = '11px sans-serif';
      ctx.fillText(track.name, 8, y + 16);

      // Draw clips
      track.clips.forEach(clip => {
        const clipX = clip.startTime * pixelsPerBeat;
        const clipWidth = clip.duration * pixelsPerBeat;

        ctx.fillStyle = track.color;
        ctx.fillRect(clipX, y + 4, clipWidth, trackHeight - 10);

        ctx.fillStyle = '#fff';
        ctx.font = '10px sans-serif';
        ctx.fillText(clip.name, clipX + 4, y + 18);
      });
    });
  }, [tracks, beatsPerBar, pixelsPerBeat, pixelsPerBar]);

  // Draw playhead only - called frequently during playback
  const drawPlayhead = useCallback((ctx: CanvasRenderingContext2D, height: number) => {
    const playheadX = (currentTime / 60) * tempo * pixelsPerBeat;
    ctx.strokeStyle = '#ff5500';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(playheadX, 0);
    ctx.lineTo(playheadX, height);
    ctx.stroke();
  }, [currentTime, tempo, pixelsPerBeat]);

  // Static content effect - only redraws when tracks/settings change
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const width = canvas.offsetWidth;
    const height = canvas.offsetHeight;
    
    // Create a unique key for the current static state
    const staticKey = `${width}-${height}-${trackKey}-${beatsPerBar}-${tempo}`;
    
    // Only redraw static content if it changed
    if (staticKey !== lastStaticDrawRef.current) {
      // Create or resize offscreen canvas for static content
      if (!staticCanvasRef.current || 
          staticCanvasRef.current.width !== width || 
          staticCanvasRef.current.height !== height) {
        staticCanvasRef.current = document.createElement('canvas');
        staticCanvasRef.current.width = width;
        staticCanvasRef.current.height = height;
      }
      
      const staticCtx = staticCanvasRef.current.getContext('2d');
      if (staticCtx) {
        drawStaticContent(staticCtx, width, height);
        lastStaticDrawRef.current = staticKey;
      }
    }
  }, [trackKey, beatsPerBar, tempo, drawStaticContent]);

  // Main render effect - composites static content + playhead
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Draw static content from offscreen canvas (or draw directly if not cached)
    if (staticCanvasRef.current) {
      ctx.drawImage(staticCanvasRef.current, 0, 0);
    } else {
      drawStaticContent(ctx, canvas.width, canvas.height);
    }

    // Draw playhead on top
    drawPlayhead(ctx, canvas.height);
  }, [currentTime, drawStaticContent, drawPlayhead]);

  // Use requestAnimationFrame for smooth playhead updates during playback
  useEffect(() => {
    if (!isPlaying) return;

    let animationId: number;
    const canvas = canvasRef.current;
    
    const animate = () => {
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx && staticCanvasRef.current) {
          // Redraw static content
          ctx.drawImage(staticCanvasRef.current, 0, 0);
          // Draw updated playhead
          drawPlayhead(ctx, canvas.height);
        }
      }
      animationId = requestAnimationFrame(animate);
    };

    animationId = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animationId);
    };
  }, [isPlaying, drawPlayhead]);

  return (
    <div className="flex-1 bg-ableton-bg overflow-hidden">
      <canvas
        ref={canvasRef}
        className="w-full h-full"
        style={{ display: 'block' }}
      />
    </div>
  );
};
