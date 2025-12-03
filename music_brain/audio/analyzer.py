"""
AudioAnalyzer - Comprehensive audio analysis for tempo, key, spectrum, and chords.

This module provides high-level audio analysis capabilities that combine
tempo detection, key detection, spectral analysis, and chord detection
into a unified interface.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import numpy as np


@dataclass
class AudioAnalysis:
    """Complete analysis results for an audio file or waveform."""

    # Basic properties
    duration_seconds: float = 0.0
    sample_rate: int = 44100
    num_channels: int = 2

    # Tempo analysis
    tempo_bpm: float = 120.0
    tempo_confidence: float = 0.0
    beat_positions: List[float] = field(default_factory=list)

    # Key analysis
    key: str = "C"
    mode: str = "major"
    key_confidence: float = 0.0

    # Spectral analysis
    spectral_centroid: float = 0.0
    spectral_bandwidth: float = 0.0
    spectral_rolloff: float = 0.0

    # Frequency band energies (8 bands)
    frequency_bands: List[float] = field(default_factory=lambda: [0.0] * 8)

    # Chord detection
    detected_chords: List[Dict[str, Any]] = field(default_factory=list)
    chord_progression: List[str] = field(default_factory=list)

    # Energy/dynamics
    rms_energy: float = 0.0
    peak_amplitude: float = 0.0
    dynamic_range: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "duration_seconds": self.duration_seconds,
            "sample_rate": self.sample_rate,
            "num_channels": self.num_channels,
            "tempo": {
                "bpm": self.tempo_bpm,
                "confidence": self.tempo_confidence,
                "beat_positions": self.beat_positions,
            },
            "key": {
                "root": self.key,
                "mode": self.mode,
                "confidence": self.key_confidence,
            },
            "spectral": {
                "centroid": self.spectral_centroid,
                "bandwidth": self.spectral_bandwidth,
                "rolloff": self.spectral_rolloff,
            },
            "frequency_bands": self.frequency_bands,
            "chords": {
                "detected": self.detected_chords,
                "progression": self.chord_progression,
            },
            "dynamics": {
                "rms_energy": self.rms_energy,
                "peak_amplitude": self.peak_amplitude,
                "dynamic_range": self.dynamic_range,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AudioAnalysis":
        """Create from dictionary."""
        return cls(
            duration_seconds=data.get("duration_seconds", 0.0),
            sample_rate=data.get("sample_rate", 44100),
            num_channels=data.get("num_channels", 2),
            tempo_bpm=data.get("tempo", {}).get("bpm", 120.0),
            tempo_confidence=data.get("tempo", {}).get("confidence", 0.0),
            beat_positions=data.get("tempo", {}).get("beat_positions", []),
            key=data.get("key", {}).get("root", "C"),
            mode=data.get("key", {}).get("mode", "major"),
            key_confidence=data.get("key", {}).get("confidence", 0.0),
            spectral_centroid=data.get("spectral", {}).get("centroid", 0.0),
            spectral_bandwidth=data.get("spectral", {}).get("bandwidth", 0.0),
            spectral_rolloff=data.get("spectral", {}).get("rolloff", 0.0),
            frequency_bands=data.get("frequency_bands", [0.0] * 8),
            detected_chords=data.get("chords", {}).get("detected", []),
            chord_progression=data.get("chords", {}).get("progression", []),
            rms_energy=data.get("dynamics", {}).get("rms_energy", 0.0),
            peak_amplitude=data.get("dynamics", {}).get("peak_amplitude", 0.0),
            dynamic_range=data.get("dynamics", {}).get("dynamic_range", 0.0),
        )


class AudioAnalyzer:
    """
    Comprehensive audio analyzer that combines tempo, key, spectral,
    and chord analysis into a unified interface.

    Example:
        >>> analyzer = AudioAnalyzer()
        >>> analysis = analyzer.analyze_file("song.wav")
        >>> print(f"BPM: {analysis.tempo_bpm}, Key: {analysis.key} {analysis.mode}")
    """

    # Pitch class names for key detection
    PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Major and minor key profiles (Krumhansl-Schmuckler)
    MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    # Frequency band edges (Hz) for 8-band analysis
    BAND_EDGES = [20, 60, 250, 500, 2000, 4000, 6000, 12000, 20000]

    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the audio analyzer.

        Args:
            sample_rate: Default sample rate for analysis
        """
        self.sample_rate = sample_rate

    def analyze_file(self, audio_path: str) -> AudioAnalysis:
        """
        Analyze an audio file.

        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)

        Returns:
            AudioAnalysis with all detected features
        """
        try:
            import soundfile as sf
            samples, sr = sf.read(audio_path)
        except ImportError:
            # Fallback: try librosa
            try:
                import librosa
                samples, sr = librosa.load(audio_path, sr=None, mono=False)
                if samples.ndim == 1:
                    samples = samples.reshape(-1, 1)
                else:
                    samples = samples.T  # librosa returns (channels, samples)
            except ImportError:
                raise ImportError(
                    "Audio file reading requires 'soundfile' or 'librosa'. "
                    "Install with: pip install soundfile or pip install librosa"
                )

        # Convert to mono for analysis
        if samples.ndim > 1:
            num_channels = samples.shape[1]
            samples_mono = np.mean(samples, axis=1)
        else:
            num_channels = 1
            samples_mono = samples

        # Run analysis
        analysis = self.analyze_waveform(samples_mono, sr)
        analysis.num_channels = num_channels

        return analysis

    def analyze_waveform(self, samples: np.ndarray, sample_rate: int) -> AudioAnalysis:
        """
        Analyze a waveform array.

        Args:
            samples: Audio samples (mono)
            sample_rate: Sample rate in Hz

        Returns:
            AudioAnalysis with all detected features
        """
        analysis = AudioAnalysis()
        analysis.sample_rate = sample_rate
        analysis.duration_seconds = len(samples) / sample_rate

        # Tempo detection
        bpm, confidence = self.detect_bpm(samples, sample_rate)
        analysis.tempo_bpm = bpm
        analysis.tempo_confidence = confidence
        analysis.beat_positions = self._detect_beat_positions(samples, sample_rate, bpm)

        # Key detection
        key, mode = self.detect_key(samples, sample_rate)
        analysis.key = key
        analysis.mode = mode
        analysis.key_confidence = 0.8  # Estimated confidence

        # Spectral analysis
        spectral = self._analyze_spectral(samples, sample_rate)
        analysis.spectral_centroid = spectral["centroid"]
        analysis.spectral_bandwidth = spectral["bandwidth"]
        analysis.spectral_rolloff = spectral["rolloff"]

        # Frequency band analysis
        analysis.frequency_bands = self._analyze_frequency_bands(samples, sample_rate)

        # Dynamics analysis
        dynamics = self._analyze_dynamics(samples)
        analysis.rms_energy = dynamics["rms"]
        analysis.peak_amplitude = dynamics["peak"]
        analysis.dynamic_range = dynamics["range"]

        # Chord detection (if available)
        try:
            from music_brain.audio.chord_detection import ChordDetector
            detector = ChordDetector(sample_rate=sample_rate)
            chord_result = detector.detect_progression(samples, sample_rate)
            analysis.detected_chords = [
                {"time": c.time, "chord": c.chord, "confidence": c.confidence}
                for c in chord_result.chords
            ]
            analysis.chord_progression = chord_result.simplified_progression
        except Exception:
            pass  # Chord detection optional

        return analysis

    def detect_bpm(self, samples: np.ndarray, sample_rate: int) -> Tuple[float, float]:
        """
        Detect tempo (BPM) from audio samples.

        Args:
            samples: Audio samples (mono)
            sample_rate: Sample rate in Hz

        Returns:
            Tuple of (bpm, confidence)
        """
        try:
            import librosa
            tempo, beat_frames = librosa.beat.beat_track(y=samples, sr=sample_rate)
            # Handle both scalar and array returns (librosa version differences)
            if hasattr(tempo, '__iter__'):
                tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
            confidence = min(1.0, len(beat_frames) / (len(samples) / sample_rate / 0.5))
            return float(tempo), confidence
        except ImportError:
            pass

        # Fallback: autocorrelation-based tempo detection
        return self._detect_bpm_autocorrelation(samples, sample_rate)

    def _detect_bpm_autocorrelation(self, samples: np.ndarray, sample_rate: int) -> Tuple[float, float]:
        """Simple autocorrelation-based tempo detection."""
        # Onset detection using energy envelope
        hop_length = 512
        frame_length = 2048

        # Calculate energy envelope
        energy = np.array([
            np.sum(samples[i:i + frame_length] ** 2)
            for i in range(0, len(samples) - frame_length, hop_length)
        ])

        # Normalize
        if energy.max() > 0:
            energy = energy / energy.max()

        # Onset detection (difference of energy)
        onset_env = np.diff(energy)
        onset_env = np.maximum(0, onset_env)

        if len(onset_env) < 100:
            return 120.0, 0.0

        # Autocorrelation
        corr = np.correlate(onset_env, onset_env, mode='full')
        corr = corr[len(corr) // 2:]

        # Find peaks in BPM range (60-200 BPM)
        min_lag = int(60 * sample_rate / hop_length / 200)  # 200 BPM
        max_lag = int(60 * sample_rate / hop_length / 60)   # 60 BPM

        if max_lag > len(corr):
            max_lag = len(corr) - 1
        if min_lag >= max_lag:
            return 120.0, 0.0

        search_range = corr[min_lag:max_lag]
        peak_idx = np.argmax(search_range) + min_lag

        # Convert lag to BPM
        bpm = 60 * sample_rate / hop_length / peak_idx

        # Estimate confidence
        confidence = float(corr[peak_idx] / corr[0]) if corr[0] > 0 else 0.0

        return float(bpm), min(1.0, confidence)

    def detect_key(self, samples: np.ndarray, sample_rate: int) -> Tuple[str, str]:
        """
        Detect musical key from audio samples.

        Args:
            samples: Audio samples (mono)
            sample_rate: Sample rate in Hz

        Returns:
            Tuple of (key_name, mode) e.g., ("C", "major")
        """
        try:
            import librosa
            # Use librosa's chroma features
            chroma = librosa.feature.chroma_cqt(y=samples, sr=sample_rate)
            chroma_mean = np.mean(chroma, axis=1)
        except ImportError:
            # Fallback: simple FFT-based pitch class detection
            chroma_mean = self._compute_simple_chroma(samples, sample_rate)

        # Correlate with major and minor profiles for all keys
        best_key = "C"
        best_mode = "major"
        best_corr = -1

        for i in range(12):
            # Rotate chroma to align with key
            rotated_chroma = np.roll(chroma_mean, -i)

            # Correlate with major profile
            major_corr = np.corrcoef(rotated_chroma, self.MAJOR_PROFILE)[0, 1]
            if major_corr > best_corr:
                best_corr = major_corr
                best_key = self.PITCH_CLASSES[i]
                best_mode = "major"

            # Correlate with minor profile
            minor_corr = np.corrcoef(rotated_chroma, self.MINOR_PROFILE)[0, 1]
            if minor_corr > best_corr:
                best_corr = minor_corr
                best_key = self.PITCH_CLASSES[i]
                best_mode = "minor"

        return best_key, best_mode

    def _compute_simple_chroma(self, samples: np.ndarray, sample_rate: int) -> np.ndarray:
        """Simple FFT-based chroma feature extraction."""
        # Use FFT to get frequency content
        n_fft = 4096
        hop = n_fft // 2

        chroma = np.zeros(12)

        for i in range(0, len(samples) - n_fft, hop):
            frame = samples[i:i + n_fft]
            spectrum = np.abs(np.fft.rfft(frame))
            freqs = np.fft.rfftfreq(n_fft, 1 / sample_rate)

            # Map frequencies to pitch classes
            for j, (freq, mag) in enumerate(zip(freqs[1:], spectrum[1:])):
                if freq > 0 and mag > 0:
                    # Convert frequency to MIDI note, then to pitch class
                    midi_note = 12 * np.log2(freq / 440) + 69
                    pitch_class = int(round(midi_note)) % 12
                    if 0 <= pitch_class < 12:
                        chroma[pitch_class] += mag

        # Normalize
        if chroma.max() > 0:
            chroma = chroma / chroma.max()

        return chroma

    def _detect_beat_positions(
        self, samples: np.ndarray, sample_rate: int, bpm: float
    ) -> List[float]:
        """Detect beat positions in seconds."""
        try:
            import librosa
            _, beat_frames = librosa.beat.beat_track(y=samples, sr=sample_rate)
            return [float(librosa.frames_to_time(f, sr=sample_rate)) for f in beat_frames]
        except ImportError:
            pass

        # Fallback: estimate beats from BPM
        beat_interval = 60.0 / bpm
        duration = len(samples) / sample_rate
        return [i * beat_interval for i in range(int(duration / beat_interval))]

    def _analyze_spectral(self, samples: np.ndarray, sample_rate: int) -> Dict[str, float]:
        """Analyze spectral characteristics."""
        try:
            import librosa
            centroid = float(np.mean(librosa.feature.spectral_centroid(y=samples, sr=sample_rate)))
            bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=samples, sr=sample_rate)))
            rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=samples, sr=sample_rate)))
            return {"centroid": centroid, "bandwidth": bandwidth, "rolloff": rolloff}
        except ImportError:
            pass

        # Fallback: simple FFT-based analysis
        n_fft = 2048
        spectrum = np.abs(np.fft.rfft(samples[:n_fft]))
        freqs = np.fft.rfftfreq(n_fft, 1 / sample_rate)

        # Spectral centroid
        centroid = float(np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-10))

        # Spectral bandwidth (standard deviation around centroid)
        bandwidth = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * spectrum) / (np.sum(spectrum) + 1e-10)))

        # Spectral rolloff (frequency below which 85% of energy is contained)
        cumsum = np.cumsum(spectrum)
        rolloff_idx = np.searchsorted(cumsum, 0.85 * cumsum[-1])
        rolloff = float(freqs[min(rolloff_idx, len(freqs) - 1)])

        return {"centroid": centroid, "bandwidth": bandwidth, "rolloff": rolloff}

    def _analyze_frequency_bands(self, samples: np.ndarray, sample_rate: int) -> List[float]:
        """Analyze energy in 8 frequency bands."""
        n_fft = 4096
        spectrum = np.abs(np.fft.rfft(samples[:min(len(samples), n_fft * 10)]))
        freqs = np.fft.rfftfreq(min(len(samples), n_fft * 10), 1 / sample_rate)

        band_energies = []
        for i in range(len(self.BAND_EDGES) - 1):
            low = self.BAND_EDGES[i]
            high = self.BAND_EDGES[i + 1]
            mask = (freqs >= low) & (freqs < high)
            energy = float(np.sum(spectrum[mask] ** 2))
            band_energies.append(energy)

        # Normalize
        max_energy = max(band_energies) if band_energies else 1.0
        if max_energy > 0:
            band_energies = [e / max_energy for e in band_energies]

        return band_energies

    def _analyze_dynamics(self, samples: np.ndarray) -> Dict[str, float]:
        """Analyze dynamic characteristics."""
        rms = float(np.sqrt(np.mean(samples ** 2)))
        peak = float(np.max(np.abs(samples)))

        # Dynamic range in dB
        if rms > 0 and peak > 0:
            dynamic_range = float(20 * np.log10(peak / rms))
        else:
            dynamic_range = 0.0

        return {"rms": rms, "peak": peak, "range": dynamic_range}
