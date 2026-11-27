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

    # Browser recording controls
    mm = st.session_state.model_manager
    if mm is None:
        st.warning("Model Manager is not initialized.")
        return

    st.markdown("### 🎙️ Record Your Answer")
    st.caption(
        f"Selected transcription model: **{mm.best_model.capitalize()}**. "
        "Record in your browser, then analyze the audio."
    )

    audio_file = st.audio_input(
        "Start recording your interview answer",
        sample_rate=SAMPLE_RATE,
        key="answer_audio"
    )

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        if st.button(
            "Analyze Recording",
            type="primary",
            use_container_width=True
        ):
            process_recording(audio_file)

    if st.button("🗑️ Clear", use_container_width=True):
        for key in ("analysis_result", "final_text", "audio_path"):
            st.session_state[key] = None if key != "final_text" else ""
        st.rerun()

    if st.session_state.final_text:
        st.markdown("### 📝 Final Transcription")
        st.text_area(
            "Transcribed answer",
            st.session_state.final_text,
            height=120,
            key="final_transcript_display"
        )

    st.divider()

    # Results
    if st.session_state.analysis_result:
        st.divider()
        render_results()


# Entry point
render_sidebar()
render_main()
