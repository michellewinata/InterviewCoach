# app.py - InterviewCoach Streamlit Application
# 2 languages, 50 questions each, live transcription (Vosk), final analysis (Whisper)

import os
import io
import json
import time
import wave
import random
import tempfile
import logging
from pathlib import Path
from typing import Optional, List

import numpy as np
import streamlit as st

# Local modules
from analysis import SpeechAnalyzer
from model_manager import ModelManager, numpy_to_wav

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="InterviewCoach",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.main { background-color: #0e1117; }
.metric-card {
    background: linear-gradient(135deg, #1e2130, #252a3a);
    border-radius: 12px;
    padding: 16px 20px;
    border-left: 4px solid #4f8ef7;
    margin-bottom: 10px;
}
.live-box {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 16px;
    min-height: 100px;
    font-family: monospace;
    font-size: 15px;
    color: #d1fae5;
    white-space: pre-wrap;
}
.question-box {
    background: linear-gradient(135deg, #1a1f35, #232b45);
    border-radius: 14px;
    padding: 24px;
    border-left: 5px solid #6366f1;
    font-size: 20px;
    font-weight: 600;
    color: #e0e7ff;
    margin-bottom: 20px;
}
.pause-marker { color: #f59e0b; font-weight: bold; }
.keyword-badge {
    display: inline-block;
    background: #064e3b;
    color: #6ee7b7;
    border-radius: 6px;
    padding: 2px 8px;
    margin: 2px;
    font-size: 12px;
}
.score-ring { font-size: 48px; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# QUESTIONS DATABASE
# ===========================================================================
QUESTIONS_EN: List[str] = [
    "Tell me about yourself.",
    "What are your greatest strengths?",
    "What is your biggest weakness?",
    "Where do you see yourself in 5 years?",
    "Why do you want to work here?",
    "Tell me about a challenge you overcame.",
    "Describe your work style.",
    "How do you handle stress and pressure?",
    "What motivates you?",
    "Tell me about a time you worked in a team.",
    "How do you prioritize your work?",
    "Describe a project you're proud of.",
    "How do you handle conflict with a coworker?",
    "What are your career goals?",
    "Why are you leaving your current job?",
    "What do you know about our company?",
    "How do you stay updated in your field?",
    "Describe your leadership style.",
    "Tell me about a failure and what you learned.",
    "How do you manage multiple deadlines?",
    "What makes you unique compared to other candidates?",
    "Tell me about a time you showed initiative.",
    "How do you approach problem-solving?",
    "Describe a time you received constructive feedback.",
    "What technical skills do you bring to this role?",
    "Tell me about a time you influenced others without authority.",
    "How do you build relationships with stakeholders?",
    "Describe your biggest professional achievement.",
    "How do you adapt to change?",
    "Tell me about a time you had to make a difficult decision.",
    "What does success look like to you?",
    "How do you give feedback to others?",
    "Tell me about a time you went above and beyond.",
    "How do you approach learning new technologies?",
    "Describe a time you managed a tight budget.",
    "How do you handle ambiguity?",
    "Tell me about your communication style.",
    "What do you do when you disagree with your manager?",
    "How do you mentor junior team members?",
    "Describe a time you delivered results under pressure.",
    "What is your approach to work-life balance?",
    "Tell me about a time you built something from scratch.",
    "How do you handle repetitive tasks?",
    "What do you look for in a company culture?",
    "Describe a time you collaborated cross-functionally.",
    "How do you deal with underperforming team members?",
    "Tell me about your most complex technical challenge.",
    "How do you ensure quality in your work?",
    "What would your former colleagues say about you?",
    "Do you have any questions for us?",
]

QUESTIONS_ID: List[str] = [
    "Ceritakan tentang diri Anda.",
    "Apa kelebihan terbesar Anda?",
    "Apa kelemahan terbesar Anda?",
    "Di mana Anda melihat diri Anda dalam 5 tahun ke depan?",
    "Mengapa Anda ingin bekerja di sini?",
    "Ceritakan tentang tantangan yang pernah Anda hadapi.",
    "Bagaimana gaya kerja Anda?",
    "Bagaimana Anda menghadapi tekanan dan stres?",
    "Apa yang memotivasi Anda?",
    "Ceritakan tentang pengalaman bekerja dalam tim.",
    "Bagaimana Anda memprioritaskan pekerjaan Anda?",
    "Deskripsikan proyek yang Anda banggakan.",
    "Bagaimana Anda menangani konflik dengan rekan kerja?",
    "Apa tujuan karir Anda?",
    "Mengapa Anda meninggalkan pekerjaan Anda saat ini?",
    "Apa yang Anda ketahui tentang perusahaan kami?",
    "Bagaimana Anda tetap update di bidang Anda?",
    "Deskripsikan gaya kepemimpinan Anda.",
    "Ceritakan tentang kegagalan dan apa yang Anda pelajari.",
    "Bagaimana Anda mengelola beberapa deadline sekaligus?",
    "Apa yang membuat Anda unik dibanding kandidat lain?",
    "Ceritakan tentang saat Anda menunjukkan inisiatif.",
    "Bagaimana pendekatan Anda dalam memecahkan masalah?",
    "Deskripsikan saat Anda menerima umpan balik konstruktif.",
    "Keterampilan teknis apa yang Anda bawa untuk peran ini?",
    "Ceritakan tentang saat Anda mempengaruhi orang lain tanpa otoritas.",
    "Bagaimana Anda membangun hubungan dengan pemangku kepentingan?",
    "Deskripsikan pencapaian profesional terbesar Anda.",
    "Bagaimana Anda beradaptasi dengan perubahan?",
    "Ceritakan tentang saat Anda harus membuat keputusan sulit.",
    "Seperti apa kesuksesan bagi Anda?",
    "Bagaimana Anda memberikan umpan balik kepada orang lain?",
    "Ceritakan tentang saat Anda melampaui ekspektasi.",
    "Bagaimana Anda mendekati pembelajaran teknologi baru?",
    "Deskripsikan saat Anda mengelola anggaran yang ketat.",
    "Bagaimana Anda menghadapi ambiguitas?",
    "Ceritakan tentang gaya komunikasi Anda.",
    "Apa yang Anda lakukan saat tidak setuju dengan manajer Anda?",
    "Bagaimana Anda membimbing anggota tim junior?",
    "Deskripsikan saat Anda memberikan hasil di bawah tekanan.",
    "Bagaimana pendekatan Anda terhadap keseimbangan kerja-hidup?",
    "Ceritakan tentang saat Anda membangun sesuatu dari awal.",
    "Bagaimana Anda menangani tugas-tugas berulang?",
    "Apa yang Anda cari dalam budaya perusahaan?",
    "Deskripsikan saat Anda berkolaborasi lintas fungsi.",
    "Bagaimana Anda menangani anggota tim yang berkinerja rendah?",
    "Ceritakan tentang tantangan teknis paling kompleks Anda.",
    "Bagaimana Anda memastikan kualitas dalam pekerjaan Anda?",
    "Apa yang akan dikatakan mantan rekan kerja Anda tentang Anda?",
    "Apakah Anda memiliki pertanyaan untuk kami?",
]

# ===========================================================================
# Session State Init
# ===========================================================================
def init_session_state():
    defaults = {
        "language": "en",
        "session_mode": "Practice Mode",
        "selected_q_idx": 0,
        "current_question": QUESTIONS_EN[0],
        "final_text": "",
        "analysis_result": None,
        "audio_path": None,
        "model_manager": None,
        "audio_key": 0,            # bump to reset the st.audio_input widget
        "processed_hash": None,    # avoid re-analysing the same recording
        "used_model": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ===========================================================================
# Model loading (cached across reruns)
# ===========================================================================
@st.cache_resource(show_spinner=False)
def get_model_manager() -> ModelManager:
    return ModelManager()

# ===========================================================================
# Audio helpers (audio is recorded in the USER'S BROWSER via st.audio_input)
# ===========================================================================
SAMPLE_RATE = 16000


def wav_bytes_to_mono16k(data: bytes) -> np.ndarray:
    """Decode WAV bytes from st.audio_input -> float32 mono @ 16 kHz."""
    with wave.open(io.BytesIO(data), "rb") as wf:
        channels = wf.getnchannels()
        width    = wf.getsampwidth()
        rate     = wf.getframerate()
        raw      = wf.readframes(wf.getnframes())
    if width != 2:
        raise ValueError(f"Unsupported WAV sample width: {width * 8}-bit")
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        audio = audio[: len(audio) - len(audio) % channels].reshape(-1, channels).mean(axis=1)
    if rate != SAMPLE_RATE and len(audio) > 1:
        n_out = int(len(audio) * SAMPLE_RATE / rate)
        audio = np.interp(np.linspace(0, len(audio) - 1, n_out),
                          np.arange(len(audio)), audio).astype(np.float32)
    return audio


def process_recording(wav_bytes: bytes):
    """Transcribe + analyse one recording and store results in session state."""
    mm   = st.session_state.model_manager
    lang = st.session_state.language

    audio    = wav_bytes_to_mono16k(wav_bytes)
    duration = len(audio) / SAMPLE_RATE
    if duration < 1.0:
        st.warning("Recording too short - please speak for at least a few seconds.")
        return

    wav_path = numpy_to_wav(audio, SAMPLE_RATE)
    st.session_state.audio_path = wav_path

    # Prefer Whisper (works for EN + ID). Load it on demand.
    if not (mm.whisper and mm.whisper.model):
        with st.spinner("Loading Whisper model (first time only)..."):
            mm.load_whisper("base")

    with st.spinner("Transcribing..."):
        result = mm.transcribe_final(wav_path, lang)

    text = (result.get("text") or "").strip()
    st.session_state.used_model = result.get("model_used", "none")
    if not text:
        st.error("Could not transcribe the audio. Try again, speak closer to the mic, "
                 "or check that Whisper loaded in the sidebar.")
        return

    st.session_state.final_text = text
    analyzer = SpeechAnalyzer(lang)
    st.session_state.analysis_result = analyzer.analyze_full(text, audio, duration, SAMPLE_RATE)


# ===========================================================================
# SIDEBAR
# ===========================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎤 InterviewCoach")
        st.divider()

        # Language
        lang_choice = st.radio("🌐 Language", ["🇺🇸 English", "🇮🇩 Bahasa Indonesia"],
                                index=0 if st.session_state.language == "en" else 1)
        new_lang = "en" if "English" in lang_choice else "id"
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.session_state.selected_q_idx = 0
            st.session_state.analysis_result = None
            st.session_state.final_text = ""
            st.rerun()

        st.divider()

        # Session mode
        mode = st.selectbox("🗂️ Session Mode",
                            ["Practice Mode", "Random Mode", "Free Session"])
        st.session_state.session_mode = mode

        q_list = QUESTIONS_EN if st.session_state.language == "en" else QUESTIONS_ID

        if mode == "Practice Mode":
            labels = [f"{i+1}. {q[:48]}…" if len(q) > 50 else f"{i+1}. {q}"
                      for i, q in enumerate(q_list)]
            idx = st.selectbox("📋 Select Question", range(len(q_list)),
                               format_func=lambda i: labels[i],
                               index=st.session_state.selected_q_idx)
            st.session_state.selected_q_idx   = idx
            st.session_state.current_question = q_list[idx]

        elif mode == "Random Mode":
            if st.button("🎲 Random Question"):
                idx = random.randint(0, len(q_list) - 1)
                st.session_state.selected_q_idx   = idx
                st.session_state.current_question = q_list[idx]
                st.session_state.analysis_result  = None
            st.caption(f"Q#{st.session_state.selected_q_idx + 1} selected")

        st.divider()

        # Models
        st.markdown("### ⚙️ ASR Models")
        mm = get_model_manager()
        st.session_state.model_manager = mm
        avail = mm.availability_report()
        for name, ok in avail.items():
            st.markdown(f"{'✅' if ok else '❌'} **{name.capitalize()}**")

        st.divider()
        if st.button("▶ Load Whisper (recommended)", use_container_width=True):
            with st.spinner("Loading Whisper-base..."):
                ok = mm.load_whisper("base")
            st.success("Whisper loaded ✅") if ok else st.error("Whisper failed ❌")

        if st.session_state.language == "en":
            if st.button("▶ Load Vosk (EN fallback)", use_container_width=True):
                with st.spinner("Downloading / loading Vosk small..."):
                    ok = mm.load_vosk("en")
                st.success("Vosk loaded ✅") if ok else st.error("Vosk failed ❌")

        st.divider()
        st.caption(f"Best model: **{mm.best_model}**")
        st.caption("Run notebook to compare & auto-select best model.")


# ===========================================================================
# RESULTS
# ===========================================================================
def render_results():
    r    = st.session_state.analysis_result
    lang = st.session_state.language

    st.markdown("## 📊 Analysis Results")

    # Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("⏱️ Duration",    f"{r['duration']}s")
    c2.metric("📖 Words",       r['total_words'])
    c3.metric("💨 WPM",         r['wpm'])
    c4.metric("🔑 Keywords",    r['keywords_count'])
    c5.metric("🎯 Fluency",     f"{r['fluency_score']}/100")

    st.divider()

    colA, colB = st.columns(2)
    with colA:
        st.markdown("### ⏸️ Pauses")
        st.markdown(f"""
| Type | Count | Marker |
|------|-------|--------|
| Short pause (0.5–1.5s) | **{r['pauses_short']}** | `\\|` |
| Long pause  (>1.5s)    | **{r['pauses_long']}**  | `\\|\\|` |
""")
        st.markdown("### 🔑 Keywords Found")
        kw = r['keywords_found']
        if kw:
            st.markdown(" ".join(
                [f"<span class='keyword-badge'>{k}</span>" for k in kw]
            ), unsafe_allow_html=True)
        else:
            hint = "experience, leadership, team…" if lang == "en" else "pengalaman, kepemimpinan, tim…"
            st.caption(f"No keywords. Try using: {hint}")

    with colB:
        score = r['fluency_score']
        col   = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        label = ("Excellent 🌟" if score >= 80 else
                 "Good 👍"      if score >= 60 else
                 "Needs Work 💪")
        st.markdown(
            f"<div style='text-align:center;'>"
            f"<div class='score-ring' style='color:{col};'>{score}</div>"
            f"<div style='color:{col}; font-size:18px; margin-top:4px;'>{label}</div>"
            f"<div style='color:#9ca3af; font-size:13px;'>Fluency Score / 100</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.progress(int(score))

    st.divider()
    st.markdown("### 📄 Transcript with Pause Markers")
    marked = r['transcript_with_pauses'].replace(
        "||", "**||**").replace("|", "**|**")
    st.markdown(f"<div class='live-box'>{marked}</div>", unsafe_allow_html=True)

    st.markdown("### 📄 Clean Final Transcript")
    st.text_area("", r['final_transcript'], height=130, key="clean_ta")

    # Coaching tips
    st.divider()
    st.markdown("### 💡 Coaching Tips")
    wpm = r['wpm']
    if wpm == 0:
        st.warning("Could not calculate WPM — check transcription.")
    elif wpm < 100:
        st.info("🐢 Speak a bit faster. Aim for 120–160 WPM for a confident tone." if lang == "en"
                else "🐢 Coba bicara lebih cepat. Target 120–160 KPM.")
    elif wpm > 180:
        st.info("⚡ Slow down slightly — you're rushing. Let your ideas land." if lang == "en"
                else "⚡ Perlambat sedikit. Beri waktu ide Anda meresap.")
    else:
        st.success("✅ Speaking pace is excellent!" if lang == "en"
                   else "✅ Kecepatan bicara sudah bagus!")

    if r['pauses_long'] > 3:
        st.warning("⏸️ Many long pauses detected. Practice smoother delivery." if lang == "en"
                   else "⏸️ Banyak jeda panjang. Latih kelancaran bicara.")
    if r['keywords_count'] < 3:
        st.info("🔑 Use more impactful interview keywords." if lang == "en"
                else "🔑 Gunakan lebih banyak kata kunci interview.")
    if r['total_words'] < 50:
        st.info("📝 Aim for 1–2 minute answers (100–200 words)." if lang == "en"
                else "📝 Usahakan jawaban 1–2 menit (100–200 kata).")


# ===========================================================================
# MAIN
# ===========================================================================
def render_main():
    lang = st.session_state.language
    mode = st.session_state.session_mode

    st.markdown(
        "<h1 style='text-align:center; color:#6366f1;'>🎤 InterviewCoach</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#9ca3af;'>"
        "Practice interview answers · Real-time AI feedback · 2 Languages</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Question display
    if mode == "Free Session":
        st.markdown(
            "<div class='question-box'>🗣️ Free Session – speak about anything!</div>",
            unsafe_allow_html=True,
        )
    else:
        q   = st.session_state.current_question
        num = st.session_state.selected_q_idx + 1
        st.markdown(
            f"<div class='question-box'>Q{num}: {q}</div>",
            unsafe_allow_html=True,
        )

    # Recorder (runs in the browser, so it works on Streamlit Cloud)
    st.markdown("### 🎙️ Record your answer")
    st.caption("Click the mic, speak, then press stop. Analysis starts automatically.")
    audio = st.audio_input("Your answer", key=f"audio_{st.session_state.audio_key}",
                           label_visibility="collapsed")

    if audio is not None:
        data = audio.getvalue()
        h = hash(data)
        if h != st.session_state.processed_hash:
            st.session_state.processed_hash = h
            try:
                process_recording(data)
            except Exception as e:
                logger.exception("Processing failed")
                st.error(f"Could not process the recording: {e}")

    if st.button("🗑️ Clear", use_container_width=False):
        st.session_state.analysis_result = None
        st.session_state.final_text      = ""
        st.session_state.audio_path      = None
        st.session_state.processed_hash  = None
        st.session_state.audio_key      += 1
        st.rerun()

    # Results
    if st.session_state.analysis_result:
        st.divider()
        render_results()


# Entry point
render_sidebar()
render_main()
