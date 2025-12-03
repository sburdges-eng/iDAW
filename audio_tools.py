"""
Audio Analysis Tools - MCP tools for audio file analysis.

Provides 9 tools:
- detect_bpm
- detect_key
- analyze_audio_feel
- extract_chords
- detect_scale
- analyze_theory
- compare_audio_files
- batch_analyze_audio
- export_audio_features
"""

from typing import Any, Dict, List
import json
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# Import DAiW audio modules
try:
    from music_brain.audio import (
        analyze_feel,
        AudioFeatures,
        AudioAnalyzer,
        ChordDetector,
        TheoryAnalyzer,
        detect_chords_from_audio,
    )
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Try to import audio cataloger for BPM/key detection
try:
    from tools.audio_cataloger.audio_cataloger import detect_bpm_key
    AUDIO_CATALOGER_AVAILABLE = True
except ImportError:
    AUDIO_CATALOGER_AVAILABLE = False


def register_tools(server: Server) -> None:
    """Register all audio analysis tools with the MCP server."""
    if not MCP_AVAILABLE:
        return
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available audio analysis tools."""
        return [
            Tool(
                name="detect_bpm",
                description="Detect tempo (BPM) from an audio file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file (WAV, MP3, AIFF, etc.)"
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="detect_key",
                description="Detect musical key and mode from an audio file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="analyze_audio_feel",
                description="Analyze groove feel and energy characteristics from audio.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="extract_chords",
                description="Extract chord progression from audio file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        },
                        "window_size": {
                            "type": "number",
                            "description": "Chord detection window in seconds",
                            "default": 0.5
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="detect_scale",
                description="Detect scales/modes from audio file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="analyze_theory",
                description="Complete music theory analysis (scales, modes, harmonic complexity).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
            Tool(
                name="compare_audio_files",
                description="Compare two audio files for BPM, key, feel, and feature differences.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file1": {
                            "type": "string",
                            "description": "Path to first audio file"
                        },
                        "file2": {
                            "type": "string",
                            "description": "Path to second audio file"
                        },
                        "detailed": {
                            "type": "boolean",
                            "description": "Include detailed feature comparison",
                            "default": False
                        }
                    },
                    "required": ["file1", "file2"]
                }
            ),
            Tool(
                name="batch_analyze_audio",
                description="Batch analyze multiple audio files. Returns BPM, key, and features for each file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of audio file paths to analyze"
                        },
                        "max_duration": {
                            "type": "number",
                            "description": "Maximum duration per file in seconds (optional)"
                        }
                    },
                    "required": ["files"]
                }
            ),
            Tool(
                name="export_audio_features",
                description="Export comprehensive audio features to JSON format.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_file": {
                            "type": "string",
                            "description": "Path to audio file"
                        },
                        "include_segments": {
                            "type": "boolean",
                            "description": "Include structural segment analysis",
                            "default": False
                        },
                        "include_chords": {
                            "type": "boolean",
                            "description": "Include chord detection",
                            "default": False
                        }
                    },
                    "required": ["audio_file"]
                }
            ),
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle tool calls."""
        try:
            audio_file = arguments.get("audio_file", "")
            
            if not Path(audio_file).exists():
                return [TextContent(type="text", text=f"Error: Audio file not found: {audio_file}")]
            
            if name == "detect_bpm":
                if AUDIO_AVAILABLE:
                    try:
                        analyzer = AudioAnalyzer()
                        analysis = analyzer.analyze_file(
                            audio_file,
                            detect_key=False,
                            detect_bpm=True,
                            extract_features_flag=False,
                            analyze_segments=False,
                        )
                        bpm_result = analysis.bpm_result
                        result = {
                            "audio_file": audio_file,
                            "bpm": bpm_result.bpm if bpm_result else None,
                            "confidence": bpm_result.confidence if bpm_result else 0.0,
                            "alternatives": bpm_result.tempo_alternatives[:3] if bpm_result else [],
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "BPM detection requires librosa. Install with: pip install librosa",
                        }
                elif AUDIO_CATALOGER_AVAILABLE:
                    try:
                        bpm, _ = detect_bpm_key(audio_file)
                        # Convert string confidence to float for consistency (0.0-1.0)
                        confidence_val = 0.8 if bpm else 0.3
                        result = {
                            "audio_file": audio_file,
                            "bpm": float(bpm) if bpm else None,
                            "confidence": confidence_val,
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "BPM detection requires librosa. Install with: pip install librosa",
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis modules not available",
                        "note": "Install librosa and optional audio_cataloger helpers",
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "detect_key":
                if AUDIO_AVAILABLE:
                    try:
                        analyzer = AudioAnalyzer()
                        analysis = analyzer.analyze_file(
                            audio_file,
                            detect_key=True,
                            detect_bpm=False,
                            extract_features_flag=False,
                            analyze_segments=False,
                        )
                        key_result = analysis.key_result
                        result = {
                            "audio_file": audio_file,
                            "key": key_result.key if key_result else None,
                            "mode": key_result.mode.value if key_result else None,
                            "confidence": key_result.confidence if key_result else 0.0,
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Key detection requires librosa. Install with: pip install librosa",
                        }
                elif AUDIO_CATALOGER_AVAILABLE:
                    try:
                        _, key_info = detect_bpm_key(audio_file)
                        if key_info:
                            key, mode = key_info.split() if " " in key_info else (key_info, "major")
                            # Convert string confidence to float for consistency (0.0-1.0)
                            result = {
                                "audio_file": audio_file,
                                "key": key,
                                "mode": mode,
                                "confidence": 0.8,
                            }
                        else:
                            result = {
                                "audio_file": audio_file,
                                "key": None,
                                "mode": None,
                                "confidence": 0.3,
                            }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Key detection requires librosa. Install with: pip install librosa",
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis modules not available",
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "analyze_audio_feel":
                if AUDIO_AVAILABLE:
                    try:
                        features = analyze_feel(audio_file)
                        result = {
                            "audio_file": audio_file,
                            "tempo_bpm": features.tempo_bpm,
                            "energy_curve": features.energy_curve[:10] if len(features.energy_curve) > 10 else features.energy_curve,
                            "dynamic_range_db": features.dynamic_range_db,
                            "rms_mean": features.rms_mean
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Audio analysis requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis module not available",
                        "note": "Install librosa and ensure music_brain.audio is accessible"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "extract_chords":
                if AUDIO_AVAILABLE:
                    try:
                        window_size = arguments.get("window_size", 0.5)
                        detection = detect_chords_from_audio(audio_file, window_size=window_size)
                        result = {
                            "audio_file": audio_file,
                            "chords": detection.chord_sequence,
                            "unique_chords": detection.unique_chords,
                            "estimated_key": detection.estimated_key,
                            "confidence": detection.confidence,
                            "chord_count": len(detection.chords)
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Chord detection requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis module not available",
                        "note": "Install librosa: pip install librosa"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "detect_scale":
                if AUDIO_AVAILABLE:
                    try:
                        analyzer = TheoryAnalyzer()
                        analysis = analyzer.analyze_audio(audio_file)
                        
                        scales = []
                        for scale in analysis.detected_scales[:5]:
                            scales.append({
                                "scale": scale.full_name,
                                "confidence": scale.confidence,
                                "is_mode": scale.is_mode,
                                "characteristics": scale.characteristics
                            })
                        
                        result = {
                            "audio_file": audio_file,
                            "primary_scale": analysis.primary_scale.full_name if analysis.primary_scale else None,
                            "mode": analysis.mode,
                            "detected_scales": scales
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Scale detection requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis module not available"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "analyze_theory":
                if AUDIO_AVAILABLE:
                    try:
                        analyzer = TheoryAnalyzer()
                        analysis = analyzer.analyze_audio(audio_file)
                        
                        result = {
                            "audio_file": audio_file,
                            "key_center": analysis.key_center,
                            "mode": analysis.mode,
                            "harmonic_complexity": analysis.harmonic_complexity,
                            "primary_scale": analysis.primary_scale.to_dict() if analysis.primary_scale else None,
                            "detected_scales": [s.to_dict() for s in analysis.detected_scales[:3]]
                        }
                    except Exception as e:
                        result = {
                            "audio_file": audio_file,
                            "error": str(e),
                            "note": "Theory analysis requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "audio_file": audio_file,
                        "error": "Audio analysis module not available"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "compare_audio_files":
                if AUDIO_AVAILABLE:
                    try:
                        from music_brain.audio.feel import compare_feel
                        file1 = arguments.get("file1", "")
                        file2 = arguments.get("file2", "")
                        detailed = arguments.get("detailed", False)
                        
                        if not Path(file1).exists():
                            return [TextContent(type="text", text=f"Error: File not found: {file1}")]
                        if not Path(file2).exists():
                            return [TextContent(type="text", text=f"Error: File not found: {file2}")]
                        
                        analyzer = AudioAnalyzer()
                        analysis1 = analyzer.analyze_file(str(file1))
                        analysis2 = analyzer.analyze_file(str(file2))
                        
                        comparison = {
                            "file1": file1,
                            "file2": file2,
                            "duration": {
                                "file1": analysis1.duration_seconds,
                                "file2": analysis2.duration_seconds,
                                "difference": abs(analysis1.duration_seconds - analysis2.duration_seconds)
                            }
                        }
                        
                        if analysis1.bpm_result and analysis2.bpm_result:
                            comparison["bpm"] = {
                                "file1": analysis1.bpm_result.bpm,
                                "file2": analysis2.bpm_result.bpm,
                                "difference": abs(analysis1.bpm_result.bpm - analysis2.bpm_result.bpm),
                                "file1_confidence": analysis1.bpm_result.confidence,
                                "file2_confidence": analysis2.bpm_result.confidence
                            }
                        
                        if analysis1.key_result and analysis2.key_result:
                            comparison["key"] = {
                                "file1": analysis1.key_result.full_key,
                                "file2": analysis2.key_result.full_key,
                                "match": analysis1.key_result.full_key == analysis2.key_result.full_key,
                                "file1_confidence": analysis1.key_result.confidence,
                                "file2_confidence": analysis2.key_result.confidence
                            }
                        
                        if analysis1.features and analysis2.features:
                            try:
                                feel_comparison = compare_feel(file1, file2)
                                comparison["feel"] = feel_comparison
                            except Exception as e:
                                comparison["feel"] = {"error": str(e)}
                        
                        if detailed and analysis1.feature_summary and analysis2.feature_summary:
                            feature_comparison = {}
                            all_keys = set(analysis1.feature_summary.keys()) | set(analysis2.feature_summary.keys())
                            for key in sorted(all_keys):
                                val1 = analysis1.feature_summary.get(key, 0)
                                val2 = analysis2.feature_summary.get(key, 0)
                                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                                    feature_comparison[key] = {
                                        "file1": val1,
                                        "file2": val2,
                                        "difference": abs(val1 - val2)
                                    }
                            comparison["features"] = feature_comparison
                        
                        result = comparison
                    except Exception as e:
                        result = {
                            "error": str(e),
                            "note": "Audio comparison requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "error": "Audio analysis modules not available",
                        "note": "Install librosa: pip install librosa"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "batch_analyze_audio":
                if AUDIO_AVAILABLE:
                    try:
                        files = arguments.get("files", [])
                        max_duration = arguments.get("max_duration")
                        
                        if not files:
                            return [TextContent(type="text", text='{"error": "No files provided"}')]
                        
                        analyzer = AudioAnalyzer()
                        results = []
                        
                        for file_path in files:
                            if not Path(file_path).exists():
                                results.append({
                                    "file": file_path,
                                    "error": "File not found"
                                })
                                continue
                            
                            try:
                                analysis = analyzer.analyze_file(
                                    str(file_path),
                                    max_duration=max_duration
                                )
                                
                                result = {
                                    "file": file_path,
                                    "filename": Path(file_path).name,
                                    "duration_seconds": analysis.duration_seconds,
                                    "sample_rate": analysis.sample_rate,
                                }
                                
                                if analysis.bpm_result:
                                    result["bpm"] = analysis.bpm_result.bpm
                                    result["bpm_confidence"] = analysis.bpm_result.confidence
                                
                                if analysis.key_result:
                                    result["key"] = analysis.key_result.full_key
                                    result["key_confidence"] = analysis.key_result.confidence
                                
                                if analysis.features:
                                    result["feel_tempo"] = analysis.features.tempo_bpm
                                    result["dynamic_range_db"] = analysis.features.dynamic_range_db
                                    result["swing_estimate"] = analysis.features.swing_estimate
                                
                                if analysis.feature_summary:
                                    result.update(analysis.feature_summary)
                                
                                results.append(result)
                            except Exception as e:
                                results.append({
                                    "file": file_path,
                                    "error": str(e)
                                })
                        
                        result = {
                            "total_files": len(files),
                            "successful": len([r for r in results if "error" not in r]),
                            "results": results
                        }
                    except Exception as e:
                        result = {
                            "error": str(e),
                            "note": "Batch analysis requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "error": "Audio analysis modules not available",
                        "note": "Install librosa: pip install librosa"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "export_audio_features":
                if AUDIO_AVAILABLE:
                    try:
                        audio_file = arguments.get("audio_file", "")
                        include_segments = arguments.get("include_segments", False)
                        include_chords = arguments.get("include_chords", False)
                        
                        if not Path(audio_file).exists():
                            return [TextContent(type="text", text=f'{{"error": "File not found: {audio_file}"}}')]
                        
                        analyzer = AudioAnalyzer()
                        analysis = analyzer.analyze_file(
                            str(audio_file),
                            analyze_segments=include_segments
                        )
                        
                        export_data = {
                            "file": audio_file,
                            "filename": Path(audio_file).name,
                            "duration_seconds": analysis.duration_seconds,
                            "sample_rate": analysis.sample_rate,
                        }
                        
                        if analysis.bpm_result:
                            export_data["bpm"] = {
                                "value": analysis.bpm_result.bpm,
                                "confidence": analysis.bpm_result.confidence,
                                "alternatives": analysis.bpm_result.tempo_alternatives[:5]
                            }
                        
                        if analysis.key_result:
                            export_data["key"] = {
                                "key": analysis.key_result.key,
                                "mode": analysis.key_result.mode.value if hasattr(analysis.key_result.mode, 'value') else str(analysis.key_result.mode),
                                "full_key": analysis.key_result.full_key,
                                "confidence": analysis.key_result.confidence
                            }
                        
                        if analysis.features:
                            export_data["feel"] = analysis.features.to_dict()
                        
                        if analysis.feature_summary:
                            export_data["features"] = analysis.feature_summary
                        
                        if include_segments and analysis.segments:
                            export_data["segments"] = [
                                {
                                    "start_time": seg.start_time,
                                    "end_time": seg.end_time,
                                    "duration": seg.duration,
                                    "energy": seg.energy,
                                    "label": seg.label
                                }
                                for seg in analysis.segments
                            ]
                        
                        if include_chords:
                            try:
                                detector = ChordDetector()
                                progression = detector.detect_progression(str(audio_file))
                                export_data["chords"] = progression.to_dict()
                            except Exception as e:
                                export_data["chords"] = {"error": str(e)}
                        
                        result = export_data
                    except Exception as e:
                        result = {
                            "error": str(e),
                            "note": "Feature export requires librosa. Install with: pip install librosa"
                        }
                else:
                    result = {
                        "error": "Audio analysis modules not available",
                        "note": "Install librosa: pip install librosa"
                    }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

