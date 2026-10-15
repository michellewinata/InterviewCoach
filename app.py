import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="InterviewCoach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default chrome for a full custom UI experience
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    .stApp { background: #E3F2FD; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  FULL APP HTML / CSS / JS
# ─────────────────────────────────────────────────────────────────────────────
HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="InterviewCoach - Practice interviews with local open-source Whisper transcription, filler word detection and performance reports." />
<title>InterviewCoach</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
<style>
/* ═══════════════════════════════════════════════════════
   DESIGN SYSTEM
═══════════════════════════════════════════════════════ */
:root {
  --clr-lightest:  #E3F2FD;
  --clr-light:     #90CAF9;
  --clr-mid:       #42A5F5;
  --clr-primary:   #2196F3;
  --clr-dark:      #0D47A1;
  --clr-darker:    #082f7a;
  --clr-white:     #ffffff;
  --clr-glass:     rgba(255,255,255,0.60);
  --clr-glass-border: rgba(145,202,249,0.45);
  --clr-filler-bg: #FFF3E0;
  --clr-filler:    #E65100;
  --clr-interim:   rgba(33,150,243,0.45);
  --radius-sm:     8px;
  --radius-md:     14px;
  --radius-lg:     20px;
  --radius-xl:     28px;
  --shadow-sm:     0 2px 8px rgba(13,71,161,.08);
  --shadow-md:     0 6px 24px rgba(13,71,161,.12);
  --shadow-lg:     0 16px 48px rgba(13,71,161,.18);
  --transition:    0.25s cubic-bezier(.4,0,.2,1);
  --font-head:     'Plus Jakarta Sans', sans-serif;
  --font-body:     'Inter', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  font-family: var(--font-body);
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%, #E3F2FD 100%);
  min-height: 100vh;
  color: #1a237e;
  overflow-x: hidden;
}

/* ───── Scrollbar ───── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--clr-lightest); }
::-webkit-scrollbar-thumb { background: var(--clr-light); border-radius: 99px; }

/* ═══════════════════════════════════════════════════════
   HEADER
═══════════════════════════════════════════════════════ */
.header {
  background: linear-gradient(135deg, var(--clr-dark) 0%, #1565C0 60%, var(--clr-primary) 100%);
  padding: 24px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}
.header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(144,202,249,.2) 0%, transparent 70%);
  border-radius: 50%;
}
.header::after {
  content: '';
  position: absolute;
  bottom: -60%;
  left: 10%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255,255,255,.08) 0%, transparent 70%);
  border-radius: 50%;
}
.header-left { display: flex; align-items: center; gap: 16px; z-index: 1; }
.logo-icon {
  width: 52px; height: 52px;
  background: rgba(255,255,255,.15);
  border: 2px solid rgba(255,255,255,.3);
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(0,0,0,.2);
}
.header-text h1 {
  font-family: var(--font-head);
  font-size: 1.7rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.5px;
  line-height: 1.1;
