# app.py - InterviewCoach Streamlit Application
# 2 languages, 50 questions each, live transcription (Vosk), final analysis (Whisper)

import os
import io
import json
import time
import wave
import random
import tempfile
import threading
import queue
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
# Audio library detection
# OSError is raised when PortAudio system library is missing (e.g. Streamlit Cloud)
# ImportError is raised when the Python package itself is not installed
# ---------------------------------------------------------------------------
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except (ImportError, OSError):
    sd = None
    SOUNDDEVICE_AVAILABLE = False

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except (ImportError, OSError):
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# Cloud/server environment: no mic → offer WAV file upload fallback
MIC_AVAILABLE = SOUNDDEVICE_AVAILABLE or PYAUDIO_AVAILABLE

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
        "recording": False,
        "recorded_frames": [],
        "live_text": "",
        "final_text": "",
        "analysis_result": None,
        "start_time": None,
        "audio_path": None,
        "model_manager": None,
        "audio_thread": None,
        "audio_queue": None,
        "stop_event": None,
        # For upload tab: store processed wav bytes so it survives st.rerun()
        "upload_wav_bytes": None,
        "upload_filename": None,
        "whisper_loading": False,
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
# Audio recording helpers
# ===========================================================================
SAMPLE_RATE = 16000
CHUNK_SIZE  = 1024

def _record_sounddevice(frames_list, stop_event, live_q, vosk_lang, mm):
    import sounddevice as _sd
    live_parts = []

    def callback(indata, frames, t, status):
        if stop_event.is_set():
            raise _sd.CallbackStop()
        pcm = (indata[:, 0] * 32767).astype(np.int16).tobytes()
        frames_list.append(indata[:, 0].copy())
        if mm.vosk_en or mm.vosk_id:
            txt, is_final = mm.transcribe_live_chunk(pcm, vosk_lang)
            if txt:
                if is_final:
                    live_parts.append(txt)
                live_q.put((" ".join(live_parts) + " " + txt).strip())

    with _sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                         dtype="float32", blocksize=CHUNK_SIZE,
                         callback=callback):
        stop_event.wait()

    # Flush
    if mm.vosk_en or mm.vosk_id:
        v = mm.vosk_en if vosk_lang == "en" else mm.vosk_id
        if v and v.recognizer:
            res = json.loads(v.recognizer.FinalResult())
            last = res.get("text", "")
            if last:
                live_parts.append(last)
            live_q.put(" ".join(live_parts).strip())


def _record_pyaudio(frames_list, stop_event, live_q, vosk_lang, mm):
    import pyaudio as _pa
    pa = _pa.PyAudio()
    stream = pa.open(format=_pa.paInt16, channels=1, rate=SAMPLE_RATE,
                     input=True, frames_per_buffer=CHUNK_SIZE)
    live_parts = []
    try:
        while not stop_event.is_set():
            pcm = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            arr = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
            frames_list.append(arr)
            if mm.vosk_en or mm.vosk_id:
                txt, is_final = mm.transcribe_live_chunk(pcm, vosk_lang)
                if txt:
                    if is_final:
                        live_parts.append(txt)
                    live_q.put((" ".join(live_parts) + " " + txt).strip())
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

    # Flush
    if mm.vosk_en or mm.vosk_id:
        v = mm.vosk_en if vosk_lang == "en" else mm.vosk_id
        if v and v.recognizer:
            res = json.loads(v.recognizer.FinalResult())
            last = res.get("text", "")
            if last:
                live_parts.append(last)
            live_q.put(" ".join(live_parts).strip())


def start_recording():
    mm = st.session_state.model_manager
    lang = st.session_state.language
    if mm is None:
        st.error("Load models first from sidebar.")
        return

    frames = []
    q = queue.Queue()
    stop_ev = threading.Event()
    mm.reset_live(lang)

    if SOUNDDEVICE_AVAILABLE:
        t = threading.Thread(target=_record_sounddevice,
                             args=(frames, stop_ev, q, lang, mm), daemon=True)
    elif PYAUDIO_AVAILABLE:
        t = threading.Thread(target=_record_pyaudio,
                             args=(frames, stop_ev, q, lang, mm), daemon=True)
    else:
        st.error("❌ No microphone library available (PortAudio not found). Use the **📂 Upload WAV** tab instead.")
        return

    st.session_state.recorded_frames = frames
    st.session_state.audio_queue     = q
    st.session_state.stop_event      = stop_ev
    st.session_state.audio_thread    = t
    st.session_state.start_time      = time.time()
    st.session_state.live_text       = ""
    st.session_state.recording       = True
    st.session_state.analysis_result = None
    t.start()


def stop_recording():
    if st.session_state.stop_event:
        st.session_state.stop_event.set()
    if st.session_state.audio_thread:
        st.session_state.audio_thread.join(timeout=5)
    st.session_state.recording = False

    frames   = st.session_state.recorded_frames
    duration = time.time() - (st.session_state.start_time or time.time())

    if not frames:
        st.warning("No audio recorded.")
        return

    audio_data = np.concatenate(frames).astype(np.float32)
    wav_path   = numpy_to_wav(audio_data, SAMPLE_RATE)
    st.session_state.audio_path = wav_path

    # Final transcription
    mm   = st.session_state.model_manager
    lang = st.session_state.language

    # Auto-load Whisper if not loaded
    if mm.whisper is None or mm.whisper.model is None:
        with st.spinner("Loading Whisper for final transcription…"):
            mm.load_whisper("base")

    result     = mm.transcribe_final(wav_path, lang)
    final_text = result.get("text", "") or st.session_state.live_text

    st.session_state.final_text = final_text

    # Analysis
    analyzer = SpeechAnalyzer(lang)
    analysis = analyzer.analyze_full(final_text, audio_data, duration, SAMPLE_RATE)
    st.session_state.analysis_result = analysis


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
            st.session_state.live_text = ""
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
                st.session_state.live_text        = ""
            st.caption(f"Q#{st.session_state.selected_q_idx + 1} selected")

        st.divider()

        # Models
        st.markdown("### ⚙️ ASR Models")
        mm = get_model_manager()
        st.session_state.model_manager = mm
        avail = mm.availability_report()
        for name, ok in avail.items():
            st.markdown(f"{'✅' if ok else '❌'} **{name.capitalize()}**")

        # Show loaded status
        st.markdown("**Loaded:**")
        vosk_loaded = (mm.vosk_en is not None and mm.vosk_en.model is not None) or \
                      (mm.vosk_id is not None and mm.vosk_id.model is not None)
        whisper_loaded = mm.whisper is not None and mm.whisper.model is not None
        st.markdown(f"{'🟢' if vosk_loaded else '🔴'} Vosk  |  {'🟢' if whisper_loaded else '🔴'} Whisper")

        st.divider()
        if st.button("▶ Load Vosk (live)", use_container_width=True):
            with st.spinner("Downloading / loading Vosk…"):
                ok = mm.load_vosk(st.session_state.language)
            st.success("Vosk loaded ✅") if ok else st.error("Vosk failed ❌")

        if st.button("▶ Load Whisper (final)", use_container_width=True):
            with st.spinner("Loading Whisper-base…"):
                ok = mm.load_whisper("base")
            st.success("Whisper loaded ✅") if ok else st.error("Whisper failed ❌")

        st.divider()
        st.caption(f"Best model: **{mm.best_model}**")
        st.caption("Run notebook to compare & auto-select best model.")


# ===========================================================================
# RESULTS
# ===========================================================================
def render_results():
    r    = st.session_state.analysis_result
    lang = st.session_state.language

    if r is None:
        return

    st.markdown("## 📊 Analysis Results")

    # Metrics row
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
| Short pause (0.5–1.5s) | **{r['pauses_short']}** | `\|` |
| Long pause  (>1.5s)    | **{r['pauses_long']}**  | `\|\|` |
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
def _run_analysis_on_wav(wav_path: str, audio_data: np.ndarray, duration: float):
    """
    Transcribe WAV + run full analysis. Populates session_state.
    audio_data  : already-loaded float32 numpy array at SAMPLE_RATE
    duration    : audio duration in seconds
    """
    mm   = st.session_state.model_manager
    lang = st.session_state.language

    # 1. Auto-load Whisper if not ready
    if mm.whisper is None or mm.whisper.model is None:
        with st.spinner("⏳ Loading Whisper (first time ~30 s)…"):
            ok = mm.load_whisper("base")
        if not ok:
            st.warning("⚠️ Whisper failed to load — will try Vosk fallback for transcript.")

    # 2. Transcribe
    with st.spinner("🔍 Transcribing audio…"):
        result     = mm.transcribe_final(wav_path, lang)
        final_text = result.get("text", "").strip()
        model_used = result.get("model_used", "none")

    if not final_text:
        st.warning(
            f"⚠️ Transcription returned empty text (model used: **{model_used}**).  \n"
            "Make sure the audio is clear and in the selected language.  \n"
            "Analysis will still run using audio features only."
        )

    st.session_state.final_text = final_text

    # 3. Analyse
    with st.spinner("📊 Analysing speech…"):
        analyzer = SpeechAnalyzer(lang)
        analysis = analyzer.analyze_full(final_text, audio_data, duration, SAMPLE_RATE)

    st.session_state.analysis_result = analysis
    return analysis


def _process_audio_bytes(file_bytes: bytes, filename: str = "audio.wav"):
    """Decode raw audio bytes to 16 kHz mono WAV and run transcription + analysis."""
    suffix = "." + (filename or "audio.wav").rsplit(".", 1)[-1]
    raw_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            raw_path = tmp.name

        try:
            import librosa as _librosa
            audio_data, _ = _librosa.load(raw_path, sr=SAMPLE_RATE, mono=True)
        except Exception as lib_err:
            try:
                import soundfile as _sf
                audio_data, orig_sr = _sf.read(raw_path, dtype="float32", always_2d=False)
                if audio_data.ndim > 1:
                    audio_data = audio_data.mean(axis=1)
                if orig_sr != SAMPLE_RATE:
                    from scipy.signal import resample
                    target_len = int(len(audio_data) * SAMPLE_RATE / orig_sr)
                    audio_data = resample(audio_data, target_len).astype(np.float32)
            except Exception as sf_err:
                st.error(
                    f"❌ Could not load audio file.\n"
                    f"librosa error: {lib_err}\n"
                    f"soundfile error: {sf_err}"
                )
                return

        duration = len(audio_data) / SAMPLE_RATE
        wav_path = numpy_to_wav(audio_data, SAMPLE_RATE)
        st.session_state.audio_path = wav_path
        _run_analysis_on_wav(wav_path, audio_data, duration)
    except Exception as e:
        st.error(f"❌ Error processing audio: {e}")
        import traceback
        st.code(traceback.format_exc(), language="text")
    finally:
        if raw_path and os.path.exists(raw_path):
            try:
                os.remove(raw_path)
            except OSError:
                pass


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

    # Ensure model manager is set (always available via cache)
    mm = get_model_manager()
    st.session_state.model_manager = mm

    # ── Tab layout: Local Mic vs Browser Mic vs Upload ────────────────
    HAS_BROWSER_MIC = hasattr(st, "audio_input")

    if MIC_AVAILABLE:
        tab_mic, tab_upload = st.tabs(["🎙️ Microphone", "📂 Upload WAV"])
        tab_browser_mic = None
    elif HAS_BROWSER_MIC:
        tab_browser_mic, tab_upload = st.tabs(["🎙️ Browser Microphone", "📂 Upload WAV"])
        tab_mic = None
    else:
        st.info(
            "🖥️ **Server / Cloud environment detected** — microphone not available.  \n"
            "Upload a WAV recording below to analyze it."
        )
        tab_mic = None
        tab_browser_mic = None
        tab_upload = st.container()

    # ── TAB 1A: Local Microphone (sounddevice / pyaudio) ──────────────
    if tab_mic is not None:
        with tab_mic:
            c1, c2, _ = st.columns([2, 2, 4])
            with c1:
                if not st.session_state.recording:
                    if st.button("🔴 Start Recording", use_container_width=True, type="primary"):
                        start_recording()
                        st.rerun()
                else:
                    if st.button("⏹️ Stop & Analyze", use_container_width=True):
                        stop_recording()
                        st.rerun()
            with c2:
                if st.button("🗑️ Clear", use_container_width=True, key="clear_mic"):
                    for key in ("analysis_result", "live_text", "final_text", "recorded_frames", "audio_path"):
                        st.session_state[key] = (
                            None if key in ("analysis_result", "audio_path")
                            else [] if key == "recorded_frames"
                            else ""
                        )
                    st.rerun()

            if st.session_state.recording:
                elapsed = time.time() - (st.session_state.start_time or time.time())
                st.markdown(
                    f"<div style='color:#ef4444;font-weight:bold;padding:8px 0;'>"
                    f"🔴 Recording… {elapsed:.0f}s — speak now!</div>",
                    unsafe_allow_html=True,
                )
                q_obj = st.session_state.audio_queue
                if q_obj:
                    while not q_obj.empty():
                        st.session_state.live_text = q_obj.get_nowait()
                time.sleep(0.4)
                st.rerun()

            st.divider()
            st.markdown("### 📝 Live Transcription")
            live_txt = st.session_state.live_text or "_Transcription appears here as you speak…_"
            st.markdown(f"<div class='live-box'>{live_txt}</div>", unsafe_allow_html=True)

    # ── TAB 1B: Browser Microphone (Streamlit Cloud / Web) ────────────
    if tab_browser_mic is not None:
        with tab_browser_mic:
            st.markdown("### 🎙️ Record Directly in Browser")
            st.caption("Click the microphone icon below to start recording, click stop when finished, then click **Analyze Recording**.")

            browser_audio = st.audio_input("Record your answer", key="browser_mic_input")

            if browser_audio is not None:
                b_bytes = browser_audio.getvalue()
                if st.button("🔍 Analyze Recording", use_container_width=True, type="primary", key="analyze_browser_mic"):
                    _process_audio_bytes(b_bytes, "browser_recording.wav")

    # ── TAB 2: Upload WAV ─────────────────────────────────────────────
    with tab_upload:
        st.markdown("### 📂 Upload a WAV / Audio File")
        st.caption("Record yourself locally (Voice Memos, Audacity, etc.) then upload here.")

        uploaded = st.file_uploader(
            "Choose audio file",
            type=["wav", "mp3", "ogg", "flac", "m4a"],
            key="wav_uploader",
        )

        # When a new file is uploaded, cache the bytes into session_state
        if uploaded is not None:
            file_bytes = uploaded.read()
            # Only update if it's a new file (different name or new session)
            if (st.session_state.upload_filename != uploaded.name or
                    st.session_state.upload_wav_bytes is None):
                st.session_state.upload_wav_bytes = file_bytes
                st.session_state.upload_filename  = uploaded.name
                # Clear previous results when new file is selected
                st.session_state.analysis_result  = None
                st.session_state.final_text        = ""

        col_a, col_b = st.columns([2, 6])
        with col_a:
            analyze_btn = st.button(
                "🔍 Analyze Upload",
                use_container_width=True,
                type="primary",
                disabled=(st.session_state.upload_wav_bytes is None),
            )
        with col_b:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_upload"):
                st.session_state.analysis_result  = None
                st.session_state.live_text         = ""
                st.session_state.final_text        = ""
                st.session_state.upload_wav_bytes  = None
                st.session_state.upload_filename   = None
                st.session_state.audio_path        = None
                st.rerun()

        if analyze_btn and st.session_state.upload_wav_bytes:
            _process_audio_bytes(
                st.session_state.upload_wav_bytes,
                st.session_state.upload_filename or "audio.wav",
            )

        # Play audio preview (use cached bytes if available)
        if st.session_state.upload_wav_bytes is not None:
            st.audio(st.session_state.upload_wav_bytes, format="audio/wav")

    # ── Results (shared by both tabs) ─────────────────────────────────
    if st.session_state.analysis_result is not None:
        st.divider()
        render_results()


# Entry point
render_sidebar()
render_main()
