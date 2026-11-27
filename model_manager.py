# model_manager.py - ASR Model Manager for InterviewCoach
# Manages Vosk (live), Whisper (final), Wav2Vec2, SpeechBrain

import os
import io
import json
import time
import wave
import zipfile
import logging
import threading
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional, Dict, List, Tuple

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Availability flags
# ---------------------------------------------------------------------------
try:
    import vosk
    vosk.SetLogLevel(-1)
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    from faster_whisper import WhisperModel as FasterWhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False

try:
    import whisper as openai_whisper
    OPENAI_WHISPER_AVAILABLE = True
except ImportError:
    OPENAI_WHISPER_AVAILABLE = False

WHISPER_AVAILABLE = FASTER_WHISPER_AVAILABLE or OPENAI_WHISPER_AVAILABLE

try:
    from transformers import pipeline as hf_pipeline, Wav2Vec2ForCTC, Wav2Vec2Processor
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import speechbrain  # noqa
    from speechbrain.inference.ASR import EncoderDecoderASR
    SPEECHBRAIN_AVAILABLE = True
except ImportError:
    SPEECHBRAIN_AVAILABLE = False

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False


# ---------------------------------------------------------------------------
# Helper: save numpy array as 16-bit mono WAV
# ---------------------------------------------------------------------------
def numpy_to_wav(audio: np.ndarray, sample_rate: int = 16000) -> str:
    """Write audio array to a temporary WAV file; returns its path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp.name
    tmp.close()
    audio_int16 = (audio * 32767).astype(np.int16) if audio.dtype != np.int16 else audio
    with wave.open(tmp_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    return tmp_path


# ===========================================================================
# Model 1 – Vosk  (fast, offline, real-time capable)
# ===========================================================================
class VoskTranscriber:
    """Real-time speech recognition using Vosk."""

    MODEL_URLS = {
        "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "id": "https://alphacephei.com/vosk/models/vosk-model-id-0.21.zip",
    }
    MODEL_DIRS = {
        "en": "models/vosk-model-small-en-us-0.15",
        "id": "models/vosk-model-id-0.21",
    }

    def __init__(self, language: str = "en"):
        self.language = language
        self.model: Optional[vosk.Model] = None
        self.recognizer: Optional[vosk.KaldiRecognizer] = None
        self._lock = threading.Lock()

    def download_model_if_needed(self) -> bool:
        """Download and extract Vosk model if not present."""
        model_dir = Path(self.MODEL_DIRS[self.language])
        if model_dir.exists():
            return True
        model_dir.parent.mkdir(parents=True, exist_ok=True)
        url = self.MODEL_URLS[self.language]
        zip_path = str(model_dir.parent / (model_dir.name + ".zip"))
        try:
            logger.info(f"Downloading Vosk model from {url} ...")
            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(str(model_dir.parent))
            os.remove(zip_path)
            return True
        except Exception as e:
            logger.error(f"Failed to download Vosk model: {e}")
            return False

    def load(self) -> bool:
        if not VOSK_AVAILABLE:
            return False
        try:
            if not self.download_model_if_needed():
                return False
            model_dir = str(Path(self.MODEL_DIRS[self.language]))
            self.model = vosk.Model(model_dir)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
            self.recognizer.SetWords(True)
            return True
        except Exception as e:
            logger.error(f"Vosk load error: {e}")
            return False

    def transcribe_chunk(self, pcm_bytes: bytes) -> Tuple[str, bool]:
        """
        Feed a PCM chunk; returns (partial_text, is_final).
        is_final=True when Vosk returns a final result.
        """
        if self.recognizer is None:
            return "", False
        with self._lock:
            if self.recognizer.AcceptWaveform(pcm_bytes):
                res = json.loads(self.recognizer.Result())
                return res.get("text", ""), True
            else:
                res = json.loads(self.recognizer.PartialResult())
                return res.get("partial", ""), False

    def transcribe_file(self, wav_path: str) -> str:
        """Transcribe a complete WAV file."""
        if not VOSK_AVAILABLE or self.model is None:
            return ""
        try:
            rec = vosk.KaldiRecognizer(self.model, 16000)
            rec.SetWords(True)
            with wave.open(wav_path, "rb") as wf:
                while True:
                    data = wf.readframes(4000)
                    if not data:
                        break
                    rec.AcceptWaveform(data)
            res = json.loads(rec.FinalResult())
            return res.get("text", "")
        except Exception as e:
            logger.error(f"Vosk file transcribe error: {e}")
            return ""

    def reset(self):
        if self.model is not None:
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
            self.recognizer.SetWords(True)


# ===========================================================================
# Model 2 – Whisper  (accurate, offline, best for final transcript)
# ===========================================================================
class WhisperTranscriber:
    """High-accuracy ASR using Whisper.

    Uses faster-whisper (CTranslate2, int8, no PyTorch) when installed,
    otherwise falls back to openai-whisper.
    """

    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        self.backend: Optional[str] = None

    def load(self, model_size: Optional[str] = None) -> bool:
        if not WHISPER_AVAILABLE:
            return False
        size = model_size or self.model_size
        try:
            if FASTER_WHISPER_AVAILABLE:
                self.model = FasterWhisperModel(size, device="cpu", compute_type="int8")
                self.backend = "faster"
            else:
                self.model = openai_whisper.load_model(size)
                self.backend = "openai"
            return True
        except Exception as e:
            logger.error(f"Whisper load error: {e}")
            return False

    def transcribe(self, wav_path: str, language: Optional[str] = None) -> Dict:
        """Returns dict with keys: text, segments, language.
        segments: list of {start, end, text}
        """
        empty = {"text": "", "segments": [], "language": language or "en"}
        if self.model is None:
            return empty
        lang = language if language in ("en", "id") else None
        try:
            if self.backend == "faster":
                segs, info = self.model.transcribe(wav_path, language=lang, beam_size=1)
                segments = [{"start": g.start, "end": g.end, "text": g.text} for g in segs]
                text = " ".join(g["text"].strip() for g in segments).strip()
                return {"text": text, "segments": segments,
                        "language": getattr(info, "language", lang or "en")}
            opts = {"language": lang} if lang else {}
            result = self.model.transcribe(wav_path, **opts)
            return {
                "text": result.get("text", "").strip(),
                "segments": result.get("segments", []),
                "language": result.get("language", lang or "en"),
            }
        except Exception as e:
            logger.error(f"Whisper transcribe error: {e}")
            return empty


# ===========================================================================
# Model 3 – Wav2Vec2  (transformer-based, offline)
# ===========================================================================
class Wav2Vec2Transcriber:
    """ASR using HuggingFace Wav2Vec2."""

    MODELS = {
        "en": "facebook/wav2vec2-base-960h",
        "id": "indonesian-nlp/wav2vec2-indonesian-javanese-sundanese",
    }
    FALLBACK_MODEL = "facebook/wav2vec2-base-960h"

    def __init__(self, language: str = "en"):
        self.language = language
        self.pipe = None

    def load(self) -> bool:
        if not TRANSFORMERS_AVAILABLE:
            return False
        try:
            model_name = self.MODELS.get(self.language, self.FALLBACK_MODEL)
            device = 0 if (TRANSFORMERS_AVAILABLE and
                           __import__("torch").cuda.is_available()) else -1
            self.pipe = hf_pipeline(
                "automatic-speech-recognition",
                model=model_name,
                device=device,
            )
            return True
        except Exception as e:
            logger.warning(f"Wav2Vec2 ({self.language}) load error: {e}. Trying fallback.")
            try:
                self.pipe = hf_pipeline(
                    "automatic-speech-recognition",
                    model=self.FALLBACK_MODEL,
                    device=-1,
                )
                return True
            except Exception as e2:
                logger.error(f"Wav2Vec2 fallback load error: {e2}")
                return False

    def transcribe(self, wav_path: str) -> str:
        if self.pipe is None:
            return ""
        try:
            result = self.pipe(wav_path)
            if isinstance(result, dict):
                return result.get("text", "").strip()
            return ""
        except Exception as e:
            logger.error(f"Wav2Vec2 transcribe error: {e}")
            return ""


# ===========================================================================
# Model 4 – SpeechBrain  (end-to-end neural ASR)
# ===========================================================================
class SpeechBrainTranscriber:
    """ASR using SpeechBrain (EncoderDecoder)."""

    SAVE_DIR = "models/speechbrain"
    SOURCE = "speechbrain/asr-crdnn-rnnlm-librispeech"

    def __init__(self):
        self.asr_model = None

    def load(self) -> bool:
        if not SPEECHBRAIN_AVAILABLE:
            return False
        try:
            Path(self.SAVE_DIR).mkdir(parents=True, exist_ok=True)
            self.asr_model = EncoderDecoderASR.from_hparams(
                source=self.SOURCE,
                savedir=self.SAVE_DIR,
                run_opts={"device": "cpu"},
            )
            return True
        except Exception as e:
            logger.error(f"SpeechBrain load error: {e}")
            return False

    def transcribe(self, wav_path: str) -> str:
        if self.asr_model is None:
            return ""
        try:
            result = self.asr_model.transcribe_file(wav_path)
            return result.strip() if result else ""
        except Exception as e:
            logger.error(f"SpeechBrain transcribe error: {e}")
            return ""


# ===========================================================================
# Central ModelManager
# ===========================================================================
class ModelManager:
    """Central manager for all 4 ASR models used in InterviewCoach."""

    CONFIG_PATH = Path("model_config.json")

    def __init__(self):
        self.vosk_en: Optional[VoskTranscriber] = None
        self.vosk_id: Optional[VoskTranscriber] = None
        self.whisper: Optional[WhisperTranscriber] = None
        self.wav2vec2_en: Optional[Wav2Vec2Transcriber] = None
        self.wav2vec2_id: Optional[Wav2Vec2Transcriber] = None
        self.speechbrain: Optional[SpeechBrainTranscriber] = None
        self.best_model: str = "whisper"  # updated after comparison
        self._load_config()

    # ------------------------------------------------------------------
    def _load_config(self):
        if self.CONFIG_PATH.exists():
            try:
                with open(self.CONFIG_PATH) as f:
                    cfg = json.load(f)
                    self.best_model = cfg.get("best_model", "whisper")
            except Exception:
                pass

    def save_config(self, best_model: str):
        self.best_model = best_model
        with open(self.CONFIG_PATH, "w") as f:
            json.dump({"best_model": best_model}, f, indent=2)

    # ------------------------------------------------------------------
    # Load helpers
    # ------------------------------------------------------------------
    def load_vosk(self, language: str = "en") -> bool:
        """Load Vosk model for the given language."""
        if language == "en":
            if self.vosk_en is None:
                self.vosk_en = VoskTranscriber("en")
            return self.vosk_en.load()
        else:
            if self.vosk_id is None:
                self.vosk_id = VoskTranscriber("id")
            return self.vosk_id.load()

    def load_whisper(self, model_size: str = "base") -> bool:
        if self.whisper is None:
            self.whisper = WhisperTranscriber(model_size)
        if self.whisper.model is not None:
            return True
        return self.whisper.load(model_size)

    def load_wav2vec2(self, language: str = "en") -> bool:
        if language == "en":
            if self.wav2vec2_en is None:
                self.wav2vec2_en = Wav2Vec2Transcriber("en")
            return self.wav2vec2_en.load()
        else:
            if self.wav2vec2_id is None:
                self.wav2vec2_id = Wav2Vec2Transcriber("id")
            return self.wav2vec2_id.load()

    def load_speechbrain(self) -> bool:
        if self.speechbrain is None:
            self.speechbrain = SpeechBrainTranscriber()
        return self.speechbrain.load()

    # ------------------------------------------------------------------
    # Live transcription (Vosk – low latency)
    # ------------------------------------------------------------------
    def transcribe_live_chunk(self, pcm_bytes: bytes, language: str = "en") -> Tuple[str, bool]:
        """Feed PCM chunk to Vosk; returns (text, is_final)."""
        transcriber = self.vosk_en if language == "en" else self.vosk_id
        if transcriber is None:
            return "", False
        return transcriber.transcribe_chunk(pcm_bytes)

    def reset_live(self, language: str = "en"):
        transcriber = self.vosk_en if language == "en" else self.vosk_id
        if transcriber:
            transcriber.reset()

    # ------------------------------------------------------------------
    # Final transcription (best model)
    # ------------------------------------------------------------------
    def transcribe_final(self, wav_path: str, language: str = "en") -> Dict:
        """
        Transcribe with the best model (Whisper by default).
        Returns dict: {text, segments, model_used}
        """
        if self.best_model == "whisper" and self.whisper and self.whisper.model:
            result = self.whisper.transcribe(wav_path, language)
            result["model_used"] = "whisper"
            return result

        if self.best_model == "wav2vec2":
            t = self.wav2vec2_en if language == "en" else self.wav2vec2_id
            if t and t.pipe:
                return {"text": t.transcribe(wav_path), "segments": [], "model_used": "wav2vec2"}

        if self.best_model == "speechbrain" and self.speechbrain and self.speechbrain.asr_model:
            return {"text": self.speechbrain.transcribe(wav_path), "segments": [], "model_used": "speechbrain"}

        # Fallback to Vosk
        v = self.vosk_en if language == "en" else self.vosk_id
        if v and v.model:
            return {"text": v.transcribe_file(wav_path), "segments": [], "model_used": "vosk"}

        return {"text": "", "segments": [], "model_used": "none"}

    # ------------------------------------------------------------------
    # Availability report
    # ------------------------------------------------------------------
    def availability_report(self) -> Dict[str, bool]:
        return {
            "vosk": VOSK_AVAILABLE,
            "whisper": WHISPER_AVAILABLE,
            "wav2vec2": TRANSFORMERS_AVAILABLE,
            "speechbrain": SPEECHBRAIN_AVAILABLE,
        }
