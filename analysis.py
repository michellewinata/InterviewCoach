# analysis.py - Speech Analysis Module for InterviewCoach
# Analyzes transcribed speech: WPM, keywords, pauses, fluency score

import re
import time
import numpy as np
from typing import List, Tuple, Dict, Optional


class SpeechAnalyzer:
    """Analyzes speech for interview coaching metrics."""

    # English interview keywords
    KEYWORDS_EN = [
        "experience", "team", "project", "leadership", "challenge",
        "solution", "achievement", "responsibility", "collaborate", "collaboration",
        "innovation", "strategy", "result", "results", "impact",
        "growth", "communication", "deadline", "priority", "initiative",
        "problem", "success", "failure", "learned", "improved",
        "managed", "developed", "implemented", "designed", "led",
        "deliver", "delivered", "goal", "goals", "stakeholder",
        "feedback", "performance", "skills", "technical", "analytical",
        "creative", "motivated", "passionate", "driven", "organized",
        "efficient", "effective", "process", "quality", "mentor",
    ]

    # Indonesian interview keywords
    KEYWORDS_ID = [
        "pengalaman", "tim", "proyek", "kepemimpinan", "tantangan",
        "solusi", "pencapaian", "tanggung jawab", "kolaborasi", "kerja sama",
        "inovasi", "strategi", "hasil", "dampak", "pertumbuhan",
        "komunikasi", "tenggat", "prioritas", "inisiatif", "masalah",
        "sukses", "gagal", "kegagalan", "belajar", "meningkat",
        "mengelola", "mengembangkan", "menerapkan", "merancang", "memimpin",
        "mencapai", "tujuan", "pemangku kepentingan", "umpan balik",
        "kinerja", "keahlian", "teknis", "analitis", "kreatif",
        "motivasi", "semangat", "disiplin", "terorganisir", "efisien",
        "efektif", "proses", "kualitas", "membimbing", "mentor",
    ]

    def __init__(self, language: str = "en"):
        self.language = language
        self.keywords = self.KEYWORDS_EN if language == "en" else self.KEYWORDS_ID

    # ------------------------------------------------------------------
    # WPM
    # ------------------------------------------------------------------
    def calculate_wpm(self, transcript: str, duration_seconds: float) -> float:
        """Calculate words per minute."""
        if duration_seconds <= 0:
            return 0.0
        words = transcript.strip().split()
        word_count = len([w for w in words if w.strip()])
        minutes = duration_seconds / 60.0
        return round(word_count / minutes, 1) if minutes > 0 else 0.0

    # ------------------------------------------------------------------
    # Keywords
    # ------------------------------------------------------------------
    def detect_keywords(self, transcript: str) -> List[str]:
        """Find matching interview keywords in transcript (case-insensitive)."""
        transcript_lower = transcript.lower()
        found = []
        for kw in self.keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, transcript_lower):
                found.append(kw)
        return found

    # ------------------------------------------------------------------
    # Pause detection (energy-based VAD)
    # ------------------------------------------------------------------
    def detect_pauses(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        short_pause_ms: int = 500,
        long_pause_ms: int = 1500,
        frame_ms: int = 20,
        energy_threshold_percentile: int = 15,
    ) -> List[Tuple[float, str]]:
        """
        Detect pauses in audio using energy-based VAD.
        Returns list of (start_time_sec, pause_type) where pause_type is '|' or '||'.
        """
        if audio_data is None or len(audio_data) == 0:
            return []

        frame_size = int(sample_rate * frame_ms / 1000)
        num_frames = len(audio_data) // frame_size

        if num_frames == 0:
            return []

        # Compute RMS energy per frame
        energies = []
        for i in range(num_frames):
            frame = audio_data[i * frame_size: (i + 1) * frame_size]
            rms = np.sqrt(np.mean(frame.astype(np.float64) ** 2) + 1e-10)
            energies.append(rms)

        energies = np.array(energies)
        threshold = np.percentile(energies, energy_threshold_percentile) * 1.5

        is_silent = energies < threshold

        pauses: List[Tuple[float, str]] = []
        in_pause = False
        pause_start = 0

        for i, silent in enumerate(is_silent):
            if silent and not in_pause:
                in_pause = True
                pause_start = i
            elif not silent and in_pause:
                in_pause = False
                pause_len_frames = i - pause_start
                pause_ms = pause_len_frames * frame_ms
                start_sec = pause_start * frame_ms / 1000.0

                if pause_ms >= long_pause_ms:
                    pauses.append((start_sec, "||"))
                elif pause_ms >= short_pause_ms:
                    pauses.append((start_sec, "|"))

        if in_pause:
            pause_len_frames = num_frames - pause_start
            pause_ms = pause_len_frames * frame_ms
            start_sec = pause_start * frame_ms / 1000.0
            if pause_ms >= long_pause_ms:
                pauses.append((start_sec, "||"))
            elif pause_ms >= short_pause_ms:
                pauses.append((start_sec, "|"))

        return pauses

    # ------------------------------------------------------------------
    # Insert pauses into transcript text
    # ------------------------------------------------------------------
    def insert_pauses_in_transcript(
        self,
        transcript: str,
        pauses: List[Tuple[float, str]],
        duration: float = 0.0,
    ) -> str:
        """Insert pause markers proportionally into the transcript text."""
        if not pauses or not transcript.strip():
            return transcript

        words = transcript.strip().split()
        if len(words) == 0 or duration <= 0:
            return transcript

        result_tokens = list(words)
        sorted_pauses = sorted(pauses, key=lambda x: x[0])

        for pause_time, pause_type in reversed(sorted_pauses):
            ratio = pause_time / duration
            insert_idx = int(ratio * len(words))
            insert_idx = max(0, min(insert_idx, len(result_tokens)))
            result_tokens.insert(insert_idx, pause_type)

        return " ".join(result_tokens)

    # ------------------------------------------------------------------
    # Fluency score
    # ------------------------------------------------------------------
    def calculate_fluency_score(
        self,
        wpm: float,
        short_pauses: int,
        long_pauses: int,
        duration: float,
    ) -> float:
        """Score 0-100. Ideal interview WPM: 120-160."""
        # WPM score (0-50 pts)
        if 120 <= wpm <= 160:
            wpm_score = 50.0
        elif wpm < 60 or wpm > 220:
            wpm_score = 10.0
        elif wpm < 120:
            wpm_score = 50.0 * (wpm - 60) / 60.0
        else:
            wpm_score = 50.0 - 20.0 * (wpm - 160) / 60.0

        # Pause score (0-50 pts base, deductions per pause)
        minutes = max(duration / 60.0, 0.1)
        short_rate = short_pauses / minutes
        long_rate  = long_pauses  / minutes
        short_penalty = max(0, (short_rate - 2) * 3)
        long_penalty  = max(0, (long_rate  - 0.5) * 10)
        pause_score = max(0, 50.0 - short_penalty - long_penalty)

        return min(100.0, max(0.0, round(wpm_score + pause_score, 1)))

    # ------------------------------------------------------------------
    # Full analysis
    # ------------------------------------------------------------------
    def analyze_full(
        self,
        transcript: str,
        audio_data: Optional[np.ndarray],
        duration: float,
        sample_rate: int = 16000,
    ) -> Dict:
        """Run all analyses and return a summary dict."""
        final_transcript = transcript.strip()
        words = final_transcript.split()
        total_words = len([w for w in words if w.strip()])

        wpm = self.calculate_wpm(final_transcript, duration)
        keywords_found = self.detect_keywords(final_transcript)

        pauses: List[Tuple[float, str]] = []
        if audio_data is not None and len(audio_data) > 0:
            pauses = self.detect_pauses(audio_data, sample_rate)

        short_pauses = sum(1 for _, t in pauses if t == "|")
        long_pauses  = sum(1 for _, t in pauses if t == "||")

        transcript_with_pauses = self.insert_pauses_in_transcript(
            final_transcript, pauses, duration
        )

        fluency_score = self.calculate_fluency_score(
            wpm, short_pauses, long_pauses, duration
        )

        return {
            "wpm": wpm,
            "keywords_found": keywords_found,
            "keywords_count": len(keywords_found),
            "pauses_short": short_pauses,
            "pauses_long": long_pauses,
            "transcript_with_pauses": transcript_with_pauses,
            "duration": round(duration, 1),
            "total_words": total_words,
            "final_transcript": final_transcript,
            "fluency_score": fluency_score,
        }
