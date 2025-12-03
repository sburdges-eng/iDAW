"""
Audio Analyzer - Comprehensive audio analysis for music production.

Provides unified interface for analyzing audio files:
- Tempo detection
- Key detection
- Spectral analysis
- Chord detection
- Dynamics analysis
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    import numpy as np

# Optional imports
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    librosa = None
    np = None
    LIBROSA_AVAILABLE = False

from music_brain.audio.feel import AudioFeatures, analyze_feel


# Krumhansl-Kessler key profiles for key detection
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


@dataclass
class AudioAnalysis:
    """
    Complete audio analysis results.

    Combines tempo, key, spectral, and dynamic analysis.
    """
    # File info
    filepath: str = ""
    duration_seconds: float = 0.0
    sample_rate: int = 44100
    num_channels: int = 1

    # Tempo analysis
    tempo_bpm: float = 120.0
    tempo_confidence: float = 0.0
    beat_positions: List[float] = field(default_factory=list)
    downbeat_positions: List[float] = field(default_factory=list)

    # Key analysis
    key: str = "C"
    mode: str = "major"
    key_confidence: float = 0.0
    chroma_mean: List[float] = field(default_factory=list)

    # Spectral analysis
    spectral_centroid: float = 0.0
    spectral_bandwidth: float = 0.0
    spectral_rolloff: float = 0.0
    spectral_flatness: float = 0.0
    zero_crossing_rate: float = 0.0

    # Dynamics
    rms_mean: float = 0.0
    rms_max: float = 0.0
    dynamic_range_db: float = 0.0
    loudness_lufs: float = -14.0
    peak_db: float = 0.0

    # Energy
    energy_curve: List[float] = field(default_factory=list)

    # Groove
    swing_estimate: float = 0.0
    groove_regularity: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "filepath": self.filepath,
            "duration_seconds": self.duration_seconds,
            "sample_rate": self.sample_rate,
            "num_channels": self.num_channels,
            "tempo": {
                "bpm": self.tempo_bpm,
                "confidence": self.tempo_confidence,
                "beat_count": len(self.beat_positions),
            },
            "key": {
                "key": self.key,
                "mode": self.mode,
                "confidence": self.key_confidence,
            },
            "spectral": {
                "centroid": self.spectral_centroid,
                "bandwidth": self.spectral_bandwidth,
                "rolloff": self.spectral_rolloff,
                "flatness": self.spectral_flatness,
                "zero_crossing_rate": self.zero_crossing_rate,
            },
            "dynamics": {
                "rms_mean": self.rms_mean,
                "rms_max": self.rms_max,
                "dynamic_range_db": self.dynamic_range_db,
                "peak_db": self.peak_db,
            },
            "groove": {
                "swing_estimate": self.swing_estimate,
                "regularity": self.groove_regularity,
            },
        }


class AudioAnalyzer:
    """
    Comprehensive audio analyzer.

    Provides unified analysis of audio files including tempo, key,
    spectral characteristics, and dynamics.
    """

    def __init__(
        self,
        sample_rate: int = 44100,
        hop_length: int = 512,
        n_fft: int = 2048,
    ):
        """
        Initialize audio analyzer.

        Args:
            sample_rate: Target sample rate for analysis
            hop_length: Analysis hop length in samples
            n_fft: FFT window size
        """
        if not LIBROSA_AVAILABLE:
            raise ImportError(
                "librosa and numpy required for AudioAnalyzer. "
                "Install with: pip install librosa numpy"
            )

        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.n_fft = n_fft

    def analyze_file(
        self,
        filepath: str,
        max_duration: Optional[float] = None,
    ) -> AudioAnalysis:
        """
        Analyze an audio file comprehensively.

        Args:
            filepath: Path to audio file
            max_duration: Maximum duration to analyze (seconds)

        Returns:
            AudioAnalysis with all extracted features
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Audio file not found: {filepath}")

        # Load audio
        y, sr = librosa.load(
            str(filepath),
            sr=self.sample_rate,
            mono=True,
            duration=max_duration
        )

        return self.analyze_waveform(y, sr, str(filepath))

    def analyze_waveform(
        self,
        samples: "np.ndarray",
        sample_rate: int,
        filepath: str = "",
    ) -> AudioAnalysis:
        """
        Analyze audio waveform.

        Args:
            samples: Audio samples (mono)
            sample_rate: Sample rate
            filepath: Optional filepath for reference

        Returns:
            AudioAnalysis results
        """
        duration = len(samples) / sample_rate

        # Tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )
        beat_times = librosa.frames_to_time(
            beat_frames, sr=sample_rate, hop_length=self.hop_length
        )

        # Key detection
        key, mode, key_confidence, chroma_mean = self._detect_key(samples, sample_rate)

        # Spectral features
        spectral = self._analyze_spectral(samples, sample_rate)

        # Dynamics
        dynamics = self._analyze_dynamics(samples, sample_rate)

        # Energy curve
        energy_curve = self._compute_energy_curve(
            samples, sample_rate, beat_frames
        )

        # Groove analysis
        swing = self._estimate_swing(beat_times)
        regularity = self._estimate_regularity(beat_times)

        return AudioAnalysis(
            filepath=filepath,
            duration_seconds=duration,
            sample_rate=sample_rate,
            num_channels=1,
            tempo_bpm=float(tempo),
            tempo_confidence=self._estimate_tempo_confidence(samples, tempo, sample_rate),
            beat_positions=beat_times.tolist(),
            key=key,
            mode=mode,
            key_confidence=key_confidence,
            chroma_mean=chroma_mean,
            spectral_centroid=spectral["centroid"],
            spectral_bandwidth=spectral["bandwidth"],
            spectral_rolloff=spectral["rolloff"],
            spectral_flatness=spectral["flatness"],
            zero_crossing_rate=spectral["zcr"],
            rms_mean=dynamics["rms_mean"],
            rms_max=dynamics["rms_max"],
            dynamic_range_db=dynamics["dynamic_range"],
            peak_db=dynamics["peak_db"],
            energy_curve=energy_curve,
            swing_estimate=swing,
            groove_regularity=regularity,
        )

    def detect_bpm(
        self,
        samples: "np.ndarray",
        sample_rate: int,
    ) -> Tuple[float, float]:
        """
        Detect tempo (BPM) from audio samples.

        Args:
            samples: Audio samples
            sample_rate: Sample rate

        Returns:
            Tuple of (bpm, confidence)
        """
        tempo, _ = librosa.beat.beat_track(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )
        confidence = self._estimate_tempo_confidence(samples, tempo, sample_rate)
        return float(tempo), confidence

    def detect_key(
        self,
        samples: "np.ndarray",
        sample_rate: int,
    ) -> Tuple[str, str]:
        """
        Detect musical key from audio samples.

        Args:
            samples: Audio samples
            sample_rate: Sample rate

        Returns:
            Tuple of (key, mode) e.g., ("C", "major")
        """
        key, mode, _, _ = self._detect_key(samples, sample_rate)
        return key, mode

    def _detect_key(
        self,
        samples: "np.ndarray",
        sample_rate: int,
    ) -> Tuple[str, str, float, List[float]]:
        """
        Detect key using Krumhansl-Kessler algorithm.

        Returns:
            Tuple of (key, mode, confidence, chroma_mean)
        """
        # Compute chromagram
        chroma = librosa.feature.chroma_cqt(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )
        chroma_mean = np.mean(chroma, axis=1)

        # Normalize
        chroma_norm = chroma_mean / (np.sum(chroma_mean) + 1e-6)

        # Correlate with key profiles for all rotations
        best_key = "C"
        best_mode = "major"
        best_score = -1.0

        for rotation in range(12):
            # Rotate chroma
            rotated = np.roll(chroma_norm, -rotation)

            # Correlate with major profile
            major_score = np.corrcoef(rotated, MAJOR_PROFILE)[0, 1]
            if major_score > best_score:
                best_score = major_score
                best_key = NOTE_NAMES[rotation]
                best_mode = "major"

            # Correlate with minor profile
            minor_score = np.corrcoef(rotated, MINOR_PROFILE)[0, 1]
            if minor_score > best_score:
                best_score = minor_score
                best_key = NOTE_NAMES[rotation]
                best_mode = "minor"

        confidence = max(0.0, min(1.0, (best_score + 1) / 2))
        return best_key, best_mode, confidence, chroma_mean.tolist()

    def _analyze_spectral(
        self,
        samples: "np.ndarray",
        sample_rate: int,
    ) -> Dict[str, float]:
        """Analyze spectral characteristics."""
        centroid = librosa.feature.spectral_centroid(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )[0]
        bandwidth = librosa.feature.spectral_bandwidth(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )[0]
        rolloff = librosa.feature.spectral_rolloff(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )[0]
        flatness = librosa.feature.spectral_flatness(
            y=samples, hop_length=self.hop_length
        )[0]
        zcr = librosa.feature.zero_crossing_rate(
            y=samples, hop_length=self.hop_length
        )[0]

        return {
            "centroid": float(np.mean(centroid)),
            "bandwidth": float(np.mean(bandwidth)),
            "rolloff": float(np.mean(rolloff)),
            "flatness": float(np.mean(flatness)),
            "zcr": float(np.mean(zcr)),
        }

    def _analyze_dynamics(
        self,
        samples: "np.ndarray",
        sample_rate: int,
    ) -> Dict[str, float]:
        """Analyze dynamics and loudness."""
        rms = librosa.feature.rms(y=samples, hop_length=self.hop_length)[0]
        rms_db = librosa.amplitude_to_db(rms)

        # Filter out silence for dynamic range calculation
        rms_db_active = rms_db[rms_db > -60]
        if len(rms_db_active) > 0:
            dynamic_range = float(np.max(rms_db_active) - np.min(rms_db_active))
        else:
            dynamic_range = 0.0

        # Peak level
        peak = float(np.max(np.abs(samples)))
        peak_db = float(20 * np.log10(peak + 1e-6))

        return {
            "rms_mean": float(np.mean(rms)),
            "rms_max": float(np.max(rms)),
            "dynamic_range": dynamic_range,
            "peak_db": peak_db,
        }

    def _compute_energy_curve(
        self,
        samples: "np.ndarray",
        sample_rate: int,
        beat_frames: "np.ndarray",
    ) -> List[float]:
        """Compute per-beat energy curve."""
        rms = librosa.feature.rms(y=samples, hop_length=self.hop_length)[0]

        energy_curve = []
        for i in range(len(beat_frames) - 1):
            start_frame = beat_frames[i]
            end_frame = beat_frames[i + 1]
            if end_frame <= len(rms):
                beat_energy = float(np.mean(rms[start_frame:end_frame]))
                energy_curve.append(beat_energy)

        return energy_curve

    def _estimate_tempo_confidence(
        self,
        samples: "np.ndarray",
        tempo: float,
        sample_rate: int,
    ) -> float:
        """Estimate confidence in tempo detection."""
        onset_env = librosa.onset.onset_strength(
            y=samples, sr=sample_rate, hop_length=self.hop_length
        )

        # Autocorrelation
        autocorr = np.correlate(onset_env, onset_env, mode='full')
        autocorr = autocorr[len(autocorr)//2:]

        # Find lag for detected tempo
        frames_per_beat = (60.0 / tempo) * sample_rate / self.hop_length
        tempo_lag = int(frames_per_beat)

        if tempo_lag >= len(autocorr):
            return 0.5

        peak_value = autocorr[tempo_lag]
        max_value = np.max(autocorr[1:])

        if max_value > 0:
            confidence = min(1.0, peak_value / max_value)
        else:
            confidence = 0.5

        return float(confidence)

    def _estimate_swing(self, beat_times: "np.ndarray") -> float:
        """Estimate swing amount from beat timing."""
        if len(beat_times) < 4:
            return 0.0

        intervals = np.diff(beat_times)
        if len(intervals) < 2:
            return 0.0

        even_intervals = intervals[0::2]
        odd_intervals = intervals[1::2]

        min_len = min(len(even_intervals), len(odd_intervals))
        if min_len < 2:
            return 0.0

        even_mean = np.mean(even_intervals[:min_len])
        odd_mean = np.mean(odd_intervals[:min_len])

        if even_mean == 0:
            return 0.0

        ratio = odd_mean / even_mean
        swing = max(0.0, min(1.0, (1.0 - ratio) * 3))
        return float(swing)

    def _estimate_regularity(self, beat_times: "np.ndarray") -> float:
        """Estimate groove regularity."""
        if len(beat_times) < 3:
            return 1.0

        intervals = np.diff(beat_times)
        if len(intervals) < 2:
            return 1.0

        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)

        if mean_interval == 0:
            return 1.0

        cv = std_interval / mean_interval
        regularity = max(0.0, 1.0 - cv * 5)
        return float(regularity)
