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
}
.header-text p {
  font-size: 0.8rem;
  color: rgba(255,255,255,.75);
  font-weight: 400;
  letter-spacing: 0.2px;
  margin-top: 3px;
}
.header-right { display: flex; align-items: center; gap: 12px; z-index: 1; }

/* Language Toggle */
.lang-toggle {
  display: flex;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 99px;
  padding: 3px;
  gap: 2px;
}
.lang-btn {
  padding: 6px 16px;
  border-radius: 99px;
  border: none;
  font-family: var(--font-body);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  color: rgba(255,255,255,.75);
  background: transparent;
  letter-spacing: 0.3px;
}
.lang-btn.active {
  background: rgba(255,255,255,.25);
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.lang-btn:hover:not(.active) { color: #fff; background: rgba(255,255,255,.1); }

/* (browser badge removed) */

/* ═══════════════════════════════════════════════════════
   MAIN LAYOUT
═══════════════════════════════════════════════════════ */
.main { padding: 32px 40px; max-width: 1400px; margin: 0 auto; }

.grid-top { display: grid; grid-template-columns: 340px 1fr; gap: 24px; margin-bottom: 24px; }
.grid-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }

/* ═══════════════════════════════════════════════════════
   GLASS CARD
═══════════════════════════════════════════════════════ */
.card {
  background: var(--clr-glass);
  border: 1px solid var(--clr-glass-border);
  border-radius: var(--radius-xl);
  padding: 28px;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}
.card:hover { box-shadow: var(--shadow-lg); transform: translateY(-1px); }
.card-title {
  font-family: var(--font-head);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--clr-dark);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-title .icon { font-size: 1rem; }

/* ═══════════════════════════════════════════════════════
   MODE SELECTOR
═══════════════════════════════════════════════════════ */
.mode-list { display: flex; flex-direction: column; gap: 10px; }
.mode-card {
  display: flex; align-items: center; gap: 14px;
  padding: 16px 18px;
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  background: rgba(255,255,255,.55);
  cursor: pointer;
  transition: var(--transition);
  position: relative;
}
.mode-card:hover, .mode-card.active {
  background: #fff;
  border-color: var(--clr-primary);
  box-shadow: 0 4px 18px rgba(33,150,243,.18);
}
.mode-card:hover .mode-icon, .mode-card.active .mode-icon {
  background: rgba(33,150,243,.12);
}
.mode-card:hover .mode-text strong, .mode-card.active .mode-text strong {
  color: var(--clr-primary);
}
.mode-icon {
  width: 44px; height: 44px; border-radius: var(--radius-sm);
  background: var(--clr-lightest);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  transition: var(--transition);
  flex-shrink: 0;
}
.mode-text {}
.mode-text strong {
  display: block;
  font-family: var(--font-head);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--clr-dark);
  transition: var(--transition);
}
.mode-text span {
  font-size: 0.75rem;
  color: #5c7099;
}

/* Question Panel */
.question-panel {
  margin-top: 16px;
  padding: 16px;
  background: rgba(255,255,255,.6);
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-glass-border);
  display: none;
}
.question-panel.visible { display: block; }

.q-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--clr-light);
  background: #fff;
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--clr-dark);
  cursor: pointer;
  outline: none;
  transition: var(--transition);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%230D47A1' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}
.q-select:focus { border-color: var(--clr-primary); box-shadow: 0 0 0 3px rgba(33,150,243,.15); }

.q-display {
  margin-top: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, var(--clr-lightest), #fff);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--clr-primary);
  font-size: 0.9rem;
  color: var(--clr-dark);
  font-weight: 500;
  line-height: 1.5;
  min-height: 52px;
  display: flex;
  align-items: center;
}
.q-display.empty { color: #90a4ae; font-weight: 400; font-style: italic; }

.btn-random {
  width: 100%;
  margin-top: 10px;
  padding: 12px;
  background: linear-gradient(135deg, var(--clr-primary), var(--clr-dark));
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-head);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  display: flex; align-items: center; justify-content: center; gap: 8px;
  letter-spacing: 0.3px;
}
.btn-random:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(33,150,243,.4); }
.btn-random:active { transform: translateY(0); }

/* ═══════════════════════════════════════════════════════
   STATUS INDICATOR
═══════════════════════════════════════════════════════ */
.status-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md);
  margin-bottom: 20px;
  font-family: var(--font-head);
  font-size: 0.85rem;
  font-weight: 600;
  transition: var(--transition);
}
.status-bar.idle { background: rgba(144,202,249,.2); border: 1.5px solid var(--clr-light); color: var(--clr-dark); }
.status-bar.listening { background: rgba(33,150,243,.1); border: 1.5px solid var(--clr-primary); color: var(--clr-primary); }
.status-bar.recording { background: rgba(244,67,54,.08); border: 1.5px solid #ef5350; color: #c62828; }
.status-bar.analyzing { background: rgba(156,39,176,.08); border: 1.5px solid #ab47bc; color: #6a1b9a; }
.status-bar.done { background: rgba(76,175,80,.1); border: 1.5px solid #66bb6a; color: #2e7d32; }

.status-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.status-bar.idle .status-dot { background: var(--clr-light); }
.status-bar.listening .status-dot {
  background: var(--clr-primary);
  animation: pulse-blue 1.4s ease infinite;
}
.status-bar.recording .status-dot {
  background: #ef5350;
  animation: pulse-red 0.8s ease infinite;
}
.status-bar.analyzing .status-dot {
  background: #ab47bc;
  animation: pulse-purple 1s ease infinite;
}
.status-bar.done .status-dot { background: #66bb6a; }

@keyframes pulse-blue {
  0%, 100% { box-shadow: 0 0 0 0 rgba(33,150,243,.5); }
  50% { box-shadow: 0 0 0 6px rgba(33,150,243,0); }
}
@keyframes pulse-red {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239,83,80,.6); }
  50% { box-shadow: 0 0 0 8px rgba(239,83,80,0); }
}
@keyframes pulse-purple {
  0%, 100% { box-shadow: 0 0 0 0 rgba(171,71,188,.5); }
  50% { box-shadow: 0 0 0 6px rgba(171,71,188,0); }
}

.status-meta { margin-left: auto; font-size: 0.8rem; font-weight: 500; opacity: 0.8; }

/* ═══════════════════════════════════════════════════════
   CONTROLS
═══════════════════════════════════════════════════════ */
.controls { display: flex; gap: 12px; margin-bottom: 20px; }
.btn {
  flex: 1;
  padding: 14px 20px;
  border-radius: var(--radius-md);
  border: none;
  font-family: var(--font-head);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  display: flex; align-items: center; justify-content: center; gap: 8px;
  letter-spacing: 0.2px;
}
.btn-start {
  background: linear-gradient(135deg, var(--clr-primary), var(--clr-dark));
  color: #fff;
  box-shadow: 0 4px 16px rgba(33,150,243,.35);
}
.btn-start:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(33,150,243,.45); }
.btn-start:active:not(:disabled) { transform: translateY(0); }
.btn-stop {
  background: rgba(239,83,80,.1);
  color: #c62828;
  border: 1.5px solid rgba(239,83,80,.4);
}
.btn-stop:hover:not(:disabled) { background: rgba(239,83,80,.18); transform: translateY(-1px); }
.btn-reset {
  background: rgba(144,202,249,.25);
  color: var(--clr-dark);
  border: 1.5px solid var(--clr-light);
  flex: 0; padding: 14px 18px;
}
.btn-reset:hover:not(:disabled) { background: rgba(144,202,249,.45); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

/* ═══════════════════════════════════════════════════════
   LIVE TRANSCRIPT
═══════════════════════════════════════════════════════ */
.transcript-area {
  min-height: 220px;
  max-height: 320px;
  overflow-y: auto;
  padding: 20px;
  background: rgba(255,255,255,.55);
  border-radius: var(--radius-md);
  border: 1.5px solid var(--clr-glass-border);
  font-size: 1rem;
  line-height: 1.8;
  color: #1a237e;
  position: relative;
}
.transcript-area .placeholder {
  position: absolute;
  inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 12px;
  color: #90a4ae;
  font-size: 0.9rem;
  pointer-events: none;
}
.transcript-area .placeholder .ph-icon { font-size: 2.5rem; opacity: 0.5; }
.transcript-final { color: #1a237e; }
.transcript-interim {
  color: var(--clr-interim);
  font-style: italic;
  background: rgba(33,150,243,.06);
  border-radius: 4px;
  padding: 1px 4px;
}

/* Live metrics strip */
.live-metrics {
  display: flex; gap: 12px;
  margin-top: 12px;
}
.live-metric {
  flex: 1;
  padding: 10px 14px;
  background: rgba(255,255,255,.5);
  border-radius: var(--radius-sm);
  border: 1px solid var(--clr-glass-border);
  text-align: center;
}
.live-metric .lm-val {
  font-family: var(--font-head);
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--clr-dark);
  display: block;
}
.live-metric .lm-lbl {
  font-size: 0.7rem;
  font-weight: 500;
  color: #5c7099;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* ═══════════════════════════════════════════════════════
   REPORT SECTION
═══════════════════════════════════════════════════════ */
.report-section { display: none; }
.report-section.visible { display: block; }

.report-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.stat-card {
  padding: 20px 18px;
  background: rgba(255,255,255,.65);
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-glass-border);
  text-align: center;
  transition: var(--transition);
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.stat-card .stat-icon { font-size: 1.8rem; margin-bottom: 8px; display: block; }
.stat-card .stat-val {
  font-family: var(--font-head);
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--clr-dark);
  display: block;
  line-height: 1;
}
.stat-card .stat-lbl {
  font-size: 0.72rem;
  font-weight: 600;
  color: #5c7099;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 4px;
  display: block;
}
.stat-card .stat-sub {
  font-size: 0.8rem;
  color: var(--clr-primary);
  margin-top: 4px;
  display: block;
}

/* Filler list */
.filler-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.filler-tag {
  padding: 4px 12px;
  background: #FFF3E0;
  border: 1px solid #FFCC80;
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #E65100;
}

/* Keywords */
.keyword-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.keyword-tag {
  padding: 5px 12px;
  background: rgba(33,150,243,.1);
  border: 1px solid rgba(33,150,243,.25);
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--clr-dark);
}

/* Pause list */
.pause-list { margin-top: 10px; display: flex; flex-direction: column; gap: 6px; }
.pause-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 12px;
  background: rgba(255,255,255,.5);
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  color: var(--clr-dark);
}
.pause-bar {
  height: 6px;
  background: linear-gradient(90deg, var(--clr-light), var(--clr-primary));
  border-radius: 99px;
  min-width: 20px;
}

/* Final transcript with highlights */
.final-transcript {
  padding: 20px;
  background: rgba(255,255,255,.65);
  border-radius: var(--radius-md);
  border: 1.5px solid var(--clr-glass-border);
  font-size: 0.95rem;
  line-height: 1.9;
  color: #1a237e;
  max-height: 280px;
  overflow-y: auto;
}
.filler-highlight {
  background: #FFF3E0;
  color: var(--clr-filler);
  border-radius: 4px;
  padding: 1px 5px;
  font-weight: 600;
  border-bottom: 2px solid #FFCC80;
}

/* Pause markers in transcript */
.pause-marker {
  display: inline-block;
  font-family: 'Courier New', monospace;
  font-weight: 800;
  font-size: 0.88em;
  border-radius: 4px;
  padding: 1px 6px;
  margin: 0 3px;
  vertical-align: middle;
  letter-spacing: 1px;
}
.pause-marker.short {
  color: #1565C0;
  background: rgba(33,150,243,.12);
  border: 1px solid rgba(33,150,243,.25);
  title: 'Short pause';
}
.pause-marker.long {
  color: #6a1b9a;
  background: rgba(156,39,176,.1);
  border: 1px solid rgba(156,39,176,.25);
}

/* ═══════════════════════════════════════════════════════
   BROWSER WARNING
═══════════════════════════════════════════════════════ */
.browser-warning {
  display: none;
  padding: 20px 28px;
  background: #fff3e0;
  border: 2px solid #ffcc80;
  border-radius: var(--radius-md);
  color: #e65100;
  font-weight: 500;
  text-align: center;
  margin: 24px 40px;
}
.browser-warning .bw-icon { font-size: 2rem; display: block; margin-bottom: 8px; }

/* ═══════════════════════════════════════════════════════
   SECTION LABELS & DIVIDERS
═══════════════════════════════════════════════════════ */
.section-label {
  font-family: var(--font-head);
  font-size: 1rem;
  font-weight: 700;
  color: var(--clr-dark);
  margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}
.section-divider {
  height: 1px;
  background: linear-gradient(90deg, var(--clr-light), transparent);
  margin: 20px 0;
}

/* ═══════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════ */
@media (max-width: 900px) {
  .main { padding: 20px; }
  .grid-top { grid-template-columns: 1fr; }
  .grid-bottom { grid-template-columns: 1fr; }
  .header { padding: 16px 20px; }
  .header-text h1 { font-size: 1.3rem; }
  .report-grid { grid-template-columns: repeat(2, 1fr); }
  .header-right { display: none; }
}
@media (max-width: 560px) {
  .report-grid { grid-template-columns: 1fr 1fr; }
  .controls { flex-wrap: wrap; }
}
</style>
</head>
<body>

<!-- ════════════════════════════════════════════════
     HEADER
════════════════════════════════════════════════ -->
<header class="header">
  <div class="header-left">
    <div class="logo-icon">🎙️</div>
    <div class="header-text">
      <h1>InterviewCoach</h1>
      <p>Practice Interviews. Improve Your Answers. Build Confidence.</p>
    </div>
  </div>
  <div class="header-right">
    <div class="lang-toggle">
      <button class="lang-btn active" id="lang-en" onclick="setLang('en')" aria-label="Switch to English">🇬🇧 English</button>
      <button class="lang-btn" id="lang-id" onclick="setLang('id')" aria-label="Switch to Bahasa Indonesia">🇮🇩 Indonesia</button>
    </div>
  </div>
</header>

<!-- Browser warning (shown if Web Speech API not supported) -->
<div class="browser-warning" id="browser-warning">
  <span class="bw-icon">⚠️</span>
  <strong>Browser Not Supported</strong><br/>
  This browser cannot record audio (needs microphone access). Please use a recent Chrome, Edge or Firefox and open the app via <strong>localhost</strong> or HTTPS.
</div>

<!-- ════════════════════════════════════════════════
     MAIN
════════════════════════════════════════════════ -->
<main class="main" id="app-main">

  <div class="grid-top">

    <!-- ── LEFT: Mode Selector ── -->
    <div>
      <div class="card">
        <div class="card-title"><span class="icon">⚙️</span> <span id="label-practice-mode">Practice Mode</span></div>
        <div class="mode-list">

          <div class="mode-card active" id="mode-free" onclick="selectMode('free')" role="button" tabindex="0" aria-pressed="true">
            <div class="mode-icon">🗣️</div>
            <div class="mode-text">
              <strong id="label-mode-free">Free Speak</strong>
              <span id="label-mode-free-sub">Talk freely, no question</span>
            </div>
          </div>

          <div class="mode-card" id="mode-choose" onclick="selectMode('choose')" role="button" tabindex="0" aria-pressed="false">
            <div class="mode-icon">📋</div>
            <div class="mode-text">
              <strong id="label-mode-choose">Choose Question</strong>
              <span id="label-mode-choose-sub">Pick from 50 questions</span>
            </div>
          </div>

          <div class="mode-card" id="mode-random" onclick="selectMode('random')" role="button" tabindex="0" aria-pressed="false">
            <div class="mode-icon">🎲</div>
            <div class="mode-text">
              <strong id="label-mode-random">Random Question</strong>
              <span id="label-mode-random-sub">Surprise me!</span>
            </div>
          </div>

        </div>

        <!-- Choose Mode Panel -->
        <div class="question-panel" id="choose-panel">
          <select class="q-select" id="question-select" onchange="onQuestionSelect()" aria-label="Select interview question">
            <option value="">— Select a question —</option>
          </select>
          <div class="q-display empty" id="q-display" aria-live="polite">No question selected</div>
        </div>

        <!-- Random Mode Panel -->
        <div class="question-panel" id="random-panel">
          <div class="q-display" id="random-display" aria-live="polite">Click below to generate a question</div>
          <button class="btn-random" id="btn-randomize" onclick="randomizeQuestion()">
            🎲 <span id="label-roll">Roll a Question</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ── RIGHT: Session Panel ── -->
    <div>
      <div class="card">
        <div class="card-title"><span class="icon">🎙️</span> <span id="label-live-session">Live Session</span></div>

        <!-- Status Indicator -->
        <div class="status-bar idle" id="status-bar" role="status" aria-live="polite">
          <div class="status-dot"></div>
          <span id="status-text">Ready to start</span>
          <div class="status-meta" id="status-meta"></div>
        </div>

        <!-- Controls -->
        <div class="controls">
          <button class="btn btn-start" id="btn-start" onclick="startSession()" aria-label="Start recording">
            ▶ <span id="label-start">Start Recording</span>
          </button>
          <button class="btn btn-stop" id="btn-stop" onclick="stopSession()" disabled aria-label="Stop recording">
            ■ <span id="label-stop">Stop</span>
          </button>
          <button class="btn btn-reset" id="btn-reset" onclick="resetSession()" aria-label="Reset session">↺</button>
        </div>

        <!-- Live Transcript -->
        <div class="section-label">
          <span>📝</span> <span id="label-live-transcript">Live Transcript</span>
        </div>
        <div class="transcript-area" id="transcript-area" aria-live="polite" aria-label="Live transcript">
          <div class="placeholder" id="transcript-placeholder">
            <span class="ph-icon">🎤</span>
            <span id="label-placeholder">Press Start and begin speaking…</span>
          </div>
          <span class="transcript-final" id="final-text"></span>
          <span class="transcript-interim" id="interim-text"></span>
        </div>

        <!-- Live Metrics -->
        <div class="live-metrics">
          <div class="live-metric">
            <span class="lm-val" id="live-wpm">—</span>
            <span class="lm-lbl" id="label-wpm">WPM</span>
          </div>
          <div class="live-metric">
            <span class="lm-val" id="live-duration">0:00</span>
            <span class="lm-lbl" id="label-duration">Duration</span>
          </div>
          <div class="live-metric">
            <span class="lm-val" id="live-words">0</span>
            <span class="lm-lbl" id="label-words">Words</span>
          </div>
          <div class="live-metric">
            <span class="lm-val" id="live-fillers">0</span>
            <span class="lm-lbl" id="label-fillers">Fillers</span>
          </div>
        </div>
      </div>
    </div>
  </div><!-- /grid-top -->

  <!-- ════════ REPORT SECTION ════════ -->
  <div class="report-section" id="report-section">

    <div class="section-label" style="margin-bottom:20px; font-size:1.1rem;">
      📊 <span id="label-session-report">Session Report</span>
    </div>

    <!-- Stats Grid -->
    <div class="report-grid" id="report-stats-grid">
      <!-- dynamically filled -->
    </div>

    <div class="grid-bottom">

      <!-- ── Filler Words & Keywords ── -->
      <div>
        <div class="card">
          <div class="card-title"><span class="icon">🔴</span> <span id="label-filler-analysis">Filler Word Analysis</span></div>
          <p id="filler-summary" style="font-size:.85rem; color:#5c7099; margin-bottom:10px;"></p>
          <div class="filler-tags" id="filler-tags"></div>

          <div class="section-divider"></div>

          <div class="card-title"><span class="icon">🔑</span> <span id="label-top-keywords">Top Keywords</span></div>
          <div class="keyword-tags" id="keyword-tags"></div>

          <div class="section-divider"></div>

          <div class="card-title"><span class="icon">⏸️</span> <span id="label-pauses">Detected Pauses</span></div>
          <p id="pause-summary" style="font-size:.85rem; color:#5c7099; margin-bottom:10px;"></p>
          <div class="pause-list" id="pause-list"></div>
        </div>
      </div>

      <!-- ── Final Transcript ── -->
      <div>
        <div class="card">
          <div class="card-title"><span class="icon">📄</span> <span id="label-final-transcript">Final Transcript</span>
            <span style="margin-left:auto; font-size:0.72rem; color:#5c7099; font-weight:400; text-transform:none; letter-spacing:0;">
              <span style="background:#FFF3E0;border:1px solid #FFCC80;border-radius:4px;padding:2px 8px;color:#E65100;font-weight:600;" id="label-legend-filler">filler</span>
              <span id="label-legend-highlighted"> = highlighted</span>
            </span>
          </div>
          <div class="final-transcript" id="final-transcript-display" aria-label="Final transcript with filler words highlighted"></div>
        </div>
      </div>
    </div><!-- /grid-bottom -->

  </div><!-- /report-section -->

</main>

<!-- ════════════════════════════════════════════════
     JAVASCRIPT
════════════════════════════════════════════════ -->
<script>
// ═══════════════════════════════════════════════════
//  INTERVIEW QUESTIONS — 50 questions, 5 categories
// ═══════════════════════════════════════════════════
const QUESTIONS = {
  en: {
    "General & About You": [
      "Tell me about yourself.",
      "What are your greatest strengths?",
      "What is your biggest weakness?",
      "Where do you see yourself in five years?",
      "Why are you interested in this position?",
      "Why do you want to work for this company?",
      "What are you passionate about outside of work?",
      "How would your colleagues describe you?",
      "What motivates you to do your best work?",
      "Describe your ideal work environment."
    ],
    "Teamwork & Collaboration": [
      "Tell me about a time you worked successfully in a team.",
      "How do you handle conflict with a coworker?",
      "Describe a situation where you had to work with a difficult team member.",
      "How do you prioritize tasks when working on a team project?",
      "Give an example of when you went above and beyond for a teammate.",
      "How do you give and receive constructive feedback?",
      "Describe a time you led a team through a challenging project.",
      "How do you ensure clear communication in a remote team?",
      "Tell me about a time you influenced others to adopt your idea.",
      "How do you handle disagreements with your manager?"
    ],
    "Problem Solving & Critical Thinking": [
      "Describe a difficult problem you solved at work.",
      "Tell me about a time you made a mistake and how you handled it.",
      "How do you approach a task you've never done before?",
      "Give an example of a creative solution you came up with.",
      "Describe a time you had to make a decision without enough information.",
      "How do you handle multiple deadlines at the same time?",
      "Tell me about a time you failed and what you learned.",
      "Describe a situation where you had to adapt quickly to a change.",
      "How do you stay calm under pressure?",
      "Give an example of how you improved a process or workflow."
    ],
    "Leadership & Initiative": [
      "Tell me about a time you took initiative without being asked.",
      "Describe a project you led from start to finish.",
      "How do you motivate others during a difficult period?",
      "Tell me about a time you mentored or coached a colleague.",
      "How do you handle underperforming team members?",
      "Describe a situation where you had to make an unpopular decision.",
      "How do you set goals and track your progress?",
      "Tell me about a time you successfully managed competing priorities.",
      "Describe how you build trust with a new team.",
      "What's your approach to delegating tasks?"
    ],
    "Career & Role-Specific": [
      "Why should we hire you over other candidates?",
      "What unique skills do you bring to this role?",
      "How does this position align with your career goals?",
      "What do you know about our company and industry?",
      "Where did you hear about this job opening?",
      "What salary range are you expecting?",
      "Are you comfortable with travel or relocation?",
      "Do you have any questions for us?",
      "How soon can you start if offered the position?",
      "Describe your biggest professional achievement."
    ]
  },
  id: {
    "Umum & Tentang Diri": [
      "Ceritakan tentang diri Anda.",
      "Apa kekuatan terbesar Anda?",
      "Apa kelemahan terbesar Anda?",
      "Di mana Anda melihat diri Anda dalam lima tahun ke depan?",
      "Mengapa Anda tertarik dengan posisi ini?",
      "Mengapa Anda ingin bekerja di perusahaan ini?",
      "Apa yang Anda sukai di luar pekerjaan?",
      "Bagaimana rekan kerja Anda menggambarkan Anda?",
      "Apa yang memotivasi Anda untuk bekerja sebaik mungkin?",
      "Deskripsikan lingkungan kerja ideal Anda."
    ],
    "Kerja Tim & Kolaborasi": [
      "Ceritakan saat Anda berhasil bekerja dalam tim.",
      "Bagaimana Anda menangani konflik dengan rekan kerja?",
      "Ceritakan situasi di mana Anda harus bekerja dengan anggota tim yang sulit.",
      "Bagaimana Anda memprioritaskan tugas dalam proyek tim?",
      "Berikan contoh ketika Anda melakukan lebih dari yang diharapkan untuk rekan tim.",
      "Bagaimana Anda memberikan dan menerima umpan balik konstruktif?",
      "Ceritakan saat Anda memimpin tim melalui proyek yang menantang.",
      "Bagaimana Anda memastikan komunikasi yang jelas dalam tim jarak jauh?",
      "Ceritakan saat Anda memengaruhi orang lain untuk menerima ide Anda.",
      "Bagaimana Anda menangani ketidaksepakatan dengan manajer Anda?"
    ],
    "Pemecahan Masalah & Berpikir Kritis": [
      "Deskripsikan masalah sulit yang pernah Anda selesaikan di tempat kerja.",
      "Ceritakan saat Anda membuat kesalahan dan bagaimana Anda mengatasinya.",
      "Bagaimana Anda mendekati tugas yang belum pernah Anda lakukan?",
      "Berikan contoh solusi kreatif yang Anda temukan.",
      "Ceritakan saat Anda harus membuat keputusan tanpa informasi yang cukup.",
      "Bagaimana Anda menangani banyak tenggat waktu sekaligus?",
      "Ceritakan saat Anda gagal dan pelajaran yang Anda petik.",
      "Deskripsikan situasi di mana Anda harus beradaptasi dengan cepat terhadap perubahan.",
      "Bagaimana Anda tetap tenang di bawah tekanan?",
      "Berikan contoh bagaimana Anda meningkatkan proses atau alur kerja."
    ],
    "Kepemimpinan & Inisiatif": [
      "Ceritakan saat Anda mengambil inisiatif tanpa diminta.",
      "Deskripsikan proyek yang Anda pimpin dari awal hingga akhir.",
      "Bagaimana Anda memotivasi orang lain di saat sulit?",
      "Ceritakan saat Anda membimbing atau melatih rekan kerja.",
      "Bagaimana Anda menangani anggota tim yang berkinerja rendah?",
      "Deskripsikan situasi di mana Anda harus membuat keputusan yang tidak populer.",
      "Bagaimana Anda menetapkan tujuan dan melacak kemajuan Anda?",
      "Ceritakan saat Anda berhasil mengelola prioritas yang bersaing.",
      "Deskripsikan cara Anda membangun kepercayaan dengan tim baru.",
      "Bagaimana pendekatan Anda dalam mendelegasikan tugas?"
    ],
    "Karier & Spesifik Posisi": [
      "Mengapa kami harus mempekerjakan Anda daripada kandidat lain?",
      "Keterampilan unik apa yang Anda bawa ke peran ini?",
      "Bagaimana posisi ini sesuai dengan tujuan karier Anda?",
      "Apa yang Anda ketahui tentang perusahaan dan industri kami?",
      "Dari mana Anda mendengar tentang lowongan kerja ini?",
      "Berapa ekspektasi gaji Anda?",
      "Apakah Anda nyaman dengan perjalanan atau relokasi?",
      "Apakah Anda memiliki pertanyaan untuk kami?",
      "Seberapa cepat Anda bisa mulai jika ditawari posisi ini?",
      "Deskripsikan pencapaian profesional terbesar Anda."
    ]
  }
};

// ═══════════════════════════════════════════════════
//  FILLER WORDS — per language
// ═══════════════════════════════════════════════════
const FILLERS = {
  en: ["um", "uh", "like", "you know", "basically", "literally", "right", "actually",
       "kind of", "sort of", "honestly", "okay", "i mean", "anyway", "you see",
       "well", "so yeah", "and stuff", "or whatever", "you know what i mean"],
  id: ["ee", "eee", "anu", "gitu", "kan", "tuh", "ya", "jadi", "soalnya", "terus",
       "nah", "intinya", "maksudnya", "gimana", "kayak", "emang", "sebenarnya",
       "begitu", "yah", "loh", "deh", "nih", "sih"]
};

// ═══════════════════════════════════════════════════
//  STOP WORDS (for keyword extraction)
// ═══════════════════════════════════════════════════
const STOP_WORDS_EN = new Set(["i","me","my","we","our","you","your","he","she","it","they","them",
  "the","a","an","is","are","was","were","be","been","being","have","has","had",
  "do","does","did","will","would","could","should","may","might","shall","can",
  "to","of","in","on","at","for","with","about","by","from","up","out","as",
  "and","or","but","if","then","than","so","yet","both","either","not","no",
  "that","this","these","those","what","which","who","when","where","how","why",
  "there","here","just","also","very","really","more","most","some","any","all"]);

const STOP_WORDS_ID = new Set(["saya","aku","kita","kami","kamu","anda","dia","mereka","nya",
  "yang","dan","atau","tapi","juga","ke","di","dari","untuk","dengan","pada","ini",
  "itu","ada","tidak","bisa","akan","sudah","belum","jika","kalau","karena","oleh",
  "lebih","banyak","sangat","saat","ketika","selalu","sering","pernah","dalam","lagi",
  "harus","perlu","bagi","hal","cara","agar","maka","serta","maupun","bahwa","tentang"]);

// ═══════════════════════════════════════════════════
//  UI LABELS (i18n)
// ═══════════════════════════════════════════════════
const LABELS = {
  en: {
    practiceMode: "Practice Mode",
    modeFree: "Free Speak", modeFreeSub: "Talk freely, no question",
    modeChoose: "Choose Question", modeChooseSub: "Pick from 50 questions",
    modeRandom: "Random Question", modeRandomSub: "Surprise me!",
    liveSession: "Live Session",
    liveTranscript: "Live Transcript",
    placeholder: "Press Start and begin speaking…",
    wpm: "WPM", duration: "Duration", words: "Words", fillers: "Fillers",
    start: "Start Recording", stop: "Stop",
    sessionReport: "Session Report",
    fillerAnalysis: "Filler Word Analysis",
    topKeywords: "Top Keywords",
    pauses: "Detected Pauses",
    finalTranscript: "Final Transcript",
    legendFiller: "filler", legendHighlighted: " = highlighted · / pause 1.5–3s · // pause >3s",
    roll: "Roll a Question",
    statusReady: "Ready to start",
    statusListening: "Listening…",
    statusRecording: "Recording",
    statusAnalyzing: "Analyzing…",
    statusDone: "Session complete",
    noFillers: "No filler words detected. Excellent!",
    noKeywords: "No keywords found.",
    noPauses: "No significant pauses detected.",
    fillerSummary: (n,w) => `${n} filler word${n!==1?'s':''} detected (${w}% of total words)`,
    pauseSummary: (n, total, longest) => n
      ? `${n} pause${n!==1?'s':''} detected (>1.5s) · total ${total}s · longest ${longest}s`
      : '0 pauses detected (>1.5s)',
  },
  id: {
    practiceMode: "Mode Latihan",
    modeFree: "Bicara Bebas", modeFreeSub: "Bicara bebas, tanpa pertanyaan",
    modeChoose: "Pilih Pertanyaan", modeChooseSub: "Pilih dari 50 pertanyaan",
    modeRandom: "Pertanyaan Acak", modeRandomSub: "Kejutkan saya!",
    liveSession: "Sesi Langsung",
    liveTranscript: "Transkrip Langsung",
    placeholder: "Tekan Mulai dan mulailah berbicara…",
    wpm: "KPM", duration: "Durasi", words: "Kata", fillers: "Filler",
    start: "Mulai Rekam", stop: "Stop",
    sessionReport: "Laporan Sesi",
    fillerAnalysis: "Analisis Kata Filler",
    topKeywords: "Kata Kunci Utama",
    pauses: "Jeda Terdeteksi",
    finalTranscript: "Transkrip Akhir",
    legendFiller: "filler", legendHighlighted: " = disorot · / jeda 1,5–3s · // jeda >3s",
    roll: "Pilihkan Pertanyaan",
    statusReady: "Siap untuk memulai",
    statusListening: "Mendengarkan…",
    statusRecording: "Merekam",
    statusAnalyzing: "Menganalisis…",
    statusDone: "Sesi selesai",
    noFillers: "Tidak ada kata filler terdeteksi. Hebat!",
    noKeywords: "Tidak ada kata kunci ditemukan.",
    noPauses: "Tidak ada jeda signifikan terdeteksi.",
    fillerSummary: (n,w) => `${n} kata filler terdeteksi (${w}% dari total kata)`,
    pauseSummary: (n, total, longest) => n
      ? `${n} jeda terdeteksi (>1,5s) · total ${total}s · terlama ${longest}s`
      : '0 jeda terdeteksi (>1,5s)',
  }
};

// ═══════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════
let currentLang = 'en';
let currentMode = 'free';
let currentQuestion = '';
let sessionStartTime = null;
let sessionTimerInterval = null;
let finalTranscript = '';       // text with pause markers: ' / ' (1.5–3s) and ' // ' (>3s)
let fillerCountLive = 0;
let pauses = [];                // [{time:'m:ss', duration:s}] measured from the audio
let sessionDuration = 0;        // seconds of audio recorded
let articulationTime = 0;       // seconds of actual talking (pauses removed)
let sessionActive = false;

// ═══════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════
async function init() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    document.getElementById('browser-warning').style.display = 'block';
    document.getElementById('app-main').style.display = 'none';
    return;
  }
  populateQuestions();
  applyLabels();
  updateUI();
  warmupAsr();   // download + warm up the local Whisper model now, so Start is instant
}

// ═══════════════════════════════════════════════════
//  LANGUAGE
// ═══════════════════════════════════════════════════
function setLang(lang) {
  if (lang === currentLang) return;
  if (sessionActive) resetSession();
  currentLang = lang;
  document.getElementById('lang-en').classList.toggle('active', lang === 'en');
  document.getElementById('lang-id').classList.toggle('active', lang === 'id');

  populateQuestions();
  applyLabels();
  // Reset question display
  currentQuestion = '';
  document.getElementById('q-display').textContent = L('modeFree');
  document.getElementById('q-display').classList.add('empty');
  document.getElementById('random-display').textContent = L('modeRandomSub');
  updateQuestionDisplay();
  warmupAsr();
}

function L(key) { return LABELS[currentLang][key] || LABELS.en[key] || key; }

function applyLabels() {
  const l = LABELS[currentLang];
  setText('label-practice-mode', l.practiceMode);
  setText('label-mode-free', l.modeFree);
  setText('label-mode-free-sub', l.modeFreeSub);
  setText('label-mode-choose', l.modeChoose);
  setText('label-mode-choose-sub', l.modeChooseSub);
  setText('label-mode-random', l.modeRandom);
  setText('label-mode-random-sub', l.modeRandomSub);
  setText('label-live-session', l.liveSession);
  setText('label-live-transcript', l.liveTranscript);
  setText('label-placeholder', l.placeholder);
  setText('label-wpm', l.wpm);
  setText('label-duration', l.duration);
  setText('label-words', l.words);
  setText('label-fillers', l.fillers);
  setText('label-start', l.start);
  setText('label-stop', l.stop);
  setText('label-session-report', l.sessionReport);
  setText('label-filler-analysis', l.fillerAnalysis);
  setText('label-top-keywords', l.topKeywords);
  setText('label-pauses', l.pauses);
  setText('label-final-transcript', l.finalTranscript);
  setText('label-legend-filler', l.legendFiller);
  setText('label-legend-highlighted', l.legendHighlighted);
  setText('label-roll', l.roll);
  if (!sessionActive) setStatus('idle');
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

// ═══════════════════════════════════════════════════
//  QUESTION MANAGEMENT
// ═══════════════════════════════════════════════════
function populateQuestions() {
  const sel = document.getElementById('question-select');
  sel.innerHTML = `<option value="">— ${currentLang==='en'?'Select a question':'Pilih pertanyaan'} —</option>`;
  const cats = QUESTIONS[currentLang];
  for (const [cat, qs] of Object.entries(cats)) {
    const og = document.createElement('optgroup');
    og.label = cat;
    qs.forEach(q => {
      const opt = document.createElement('option');
      opt.value = q;
      opt.textContent = q;
      og.appendChild(opt);
    });
    sel.appendChild(og);
  }
}

function getAllQuestions() {
  const all = [];
  for (const qs of Object.values(QUESTIONS[currentLang])) all.push(...qs);
  return all;
}

function selectMode(mode) {
  currentMode = mode;
  ['free','choose','random'].forEach(m => {
    const el = document.getElementById(`mode-${m}`);
    el.classList.toggle('active', m === mode);
    el.setAttribute('aria-pressed', m === mode ? 'true' : 'false');
  });
  document.getElementById('choose-panel').classList.toggle('visible', mode === 'choose');
  document.getElementById('random-panel').classList.toggle('visible', mode === 'random');

  if (mode === 'free') { currentQuestion = ''; updateQuestionDisplay(); }
  if (mode === 'random') updateQuestionDisplay();
}

function onQuestionSelect() {
  const sel = document.getElementById('question-select');
  currentQuestion = sel.value;
  const disp = document.getElementById('q-display');
  if (currentQuestion) {
    disp.textContent = currentQuestion;
    disp.classList.remove('empty');
  } else {
    disp.textContent = currentLang === 'en' ? 'No question selected' : 'Belum dipilih';
    disp.classList.add('empty');
  }
}

function randomizeQuestion() {
  const all = getAllQuestions();
  currentQuestion = all[Math.floor(Math.random() * all.length)];
  document.getElementById('random-display').textContent = currentQuestion;
  document.getElementById('random-display').classList.remove('empty');
  // Bounce animation
  const btn = document.getElementById('btn-randomize');
  btn.style.transform = 'scale(0.95)';
  setTimeout(() => btn.style.transform = '', 150);
}

function updateQuestionDisplay() {
  if (currentMode === 'choose') {
    const disp = document.getElementById('q-display');
    disp.textContent = currentQuestion || (currentLang==='en'?'No question selected':'Belum dipilih');
    disp.classList.toggle('empty', !currentQuestion);
  } else if (currentMode === 'random') {
    document.getElementById('random-display').textContent = currentQuestion || L('modeRandomSub');
  }
}

// ═══════════════════════════════════════════════════
//  STATUS
// ═══════════════════════════════════════════════════
function setStatus(state, meta = '') {
  const bar = document.getElementById('status-bar');
  bar.className = `status-bar ${state}`;
  const labels = {
    idle: L('statusReady'),
    listening: L('statusListening'),
    recording: L('statusRecording'),
    analyzing: L('statusAnalyzing'),
    done: L('statusDone')
  };
  document.getElementById('status-text').textContent = labels[state] || state;
  document.getElementById('status-meta').textContent = meta;
}

// ═══════════════════════════════════════════════════
//  SESSION CONTROL + LOCAL ASR (open-source Whisper, runs on this device)
// ═══════════════════════════════════════════════════
// ═══════════════════════════════════════════════════
//  LOCAL SPEECH ENGINE — CORE (pure logic, no DOM)
//  1. StreamResampler : mic rate → 16 kHz (box filter, no drift between chunks)
//  2. Segmenter       : adaptive-energy VAD → cuts audio at natural pauses,
//                       measures every pause from the REAL audio timeline
//  3. cleanAsrText    : removes Whisper hallucinations / repetition loops
// ═══════════════════════════════════════════════════
const ASR_SR = 16000;
const FRAME = 320;                    // 20 ms @ 16 kHz
const FRAME_SEC = FRAME / ASR_SR;
const MIN_RUN_FRAMES = 5;             // 100 ms continuous energy = real speech (ignores clicks)
const HANGOVER_SEC = 0.35;            // short dips inside a word/phrase are still "speaking"
const SILENCE_COMMIT_SEC = 0.6;       // this much silence = end of a phrase → transcribe it
const TAIL_SEC = 0.3;                 // silence kept after the last word
const PREROLL_SEC = 0.4;              // silence kept before the first word (no clipped consonants)
const MAX_SEG_SEC = 12;               // continuous speech is force-cut (at the quietest point)
const MIN_COMMIT_FRAMES = 6;          // < 120 ms of speech = noise, discard
const PAUSE_MIN_SEC = 1.5;            // gap counted as a pause
const PAUSE_LONG_SEC = 3.0;           // "//" marker above this

function rmsOf(x) {
  const n = x.length;
  if (!n) return 0;
  let s = 0;
  for (let i = 0; i < n; i++) s += x[i] * x[i];
  return Math.sqrt(s / n);
}

function concatF32(a, b) {
  if (!a.length) return b;
  const o = new Float32Array(a.length + b.length);
  o.set(a); o.set(b, a.length);
  return o;
}

// ─── Streaming resampler (area-average; keeps fractional phase across chunks) ───
class StreamResampler {
  constructor(srcRate, dstRate = ASR_SR) {
    this.ratio = srcRate / dstRate;
    this.left = new Float32Array(0);
    this.t = 0;
  }
  process(inp) {
    if (this.ratio === 1) return new Float32Array(inp);
    const data = concatF32(this.left, inp);
    const ratio = this.ratio;
    const out = [];
    let t = this.t;
    while (t + ratio <= data.length) {
      const b = t + ratio;
      let s = 0;
      for (let j = Math.floor(t), e = Math.ceil(b); j < e; j++) {
        s += data[j] * (Math.min(j + 1, b) - Math.max(j, t));
      }
      out.push(s / ratio);
      t = b;
    }
    const used = Math.floor(t);
    this.left = data.slice(used);
    this.t = t - used;
    return Float32Array.from(out);
  }
}

// ─── Segmenter: VAD + phrase cutting + pause measurement ───
class Segmenter {
  constructor() { this.reset(); }

  reset() {
    this.buf = new Float32Array(0);   // audio not yet sent to ASR
    this.bufStartT = 0;               // absolute time (s) of buf[0]
    this.rem = new Float32Array(0);
    this.samples = 0;
    this.nFrames = 0;
    this.noise = 0.003;               // adaptive noise floor (RMS)
    this.voicedRun = 0;
    this.runStartT = 0;
    this.speaking = false;
    this.everSpoke = false;
    this.lastSpeechEndT = 0;
    this.firstSpeechT = 0;
    this.pauses = [];                 // [{time, duration}]  (time = when silence began)
    this.commits = [];
    this.segCounter = 0;
    this.curId = 0;
    this.cur = this._newSeg();
  }

  _newSeg() {
    this.curId++;
    return { hasSpeech: false, voicedFrames: 0, pauseBefore: 0, startT: 0 };
  }

  get totalSec() { return this.samples / ASR_SR; }
  threshold() { return Math.min(0.06, Math.max(0.009, this.noise * 3)); }

  push(x) {
    if (!x || !x.length) return;
    this.buf = concatF32(this.buf, x);
    this.samples += x.length;
    const data = this.rem.length ? concatF32(this.rem, x) : x;
    let i = 0;
    for (; i + FRAME <= data.length; i += FRAME) {
      this._frame(rmsOf(data.subarray(i, i + FRAME)));
    }
    this.rem = data.slice(i);
    this._maybeCommit();
  }

  _frame(rms) {
    this.nFrames++;
    const tEnd = this.nFrames * FRAME_SEC;
    const tStart = tEnd - FRAME_SEC;
    if (rms > this.threshold()) {
      if (this.voicedRun === 0) this.runStartT = tStart;
      this.voicedRun++;
      if (this.voicedRun >= MIN_RUN_FRAMES) {
        if (!this.speaking) { this.speaking = true; this._onset(this.runStartT); }
        this.lastSpeechEndT = tEnd;
        this.cur.voicedFrames += (this.voicedRun === MIN_RUN_FRAMES) ? MIN_RUN_FRAMES : 1;
      }
    } else {
      this.voicedRun = 0;
      this.noise += (rms - this.noise) * (rms < this.noise ? 0.2 : 0.01);
      this.noise = Math.min(0.03, Math.max(0.0005, this.noise));
      if (this.speaking && tEnd - this.lastSpeechEndT > HANGOVER_SEC) this.speaking = false;
    }
  }

  _onset(startT) {
    let gap = this.everSpoke ? startT - this.lastSpeechEndT : 0;
    if (gap >= PAUSE_MIN_SEC) {
      this.pauses.push({ time: this.lastSpeechEndT, duration: Math.round(gap * 10) / 10 });
    } else {
      gap = 0;
    }
    if (!this.everSpoke) { this.everSpoke = true; this.firstSpeechT = startT; }
    if (!this.cur.hasSpeech) {
      this.cur.hasSpeech = true;
      this.cur.pauseBefore = gap;
      this.cur.startT = startT;
    }
  }

  _maybeCommit() {
    const dur = this.buf.length / ASR_SR;
    if (!this.cur.hasSpeech) {
      // nothing worth transcribing yet: keep only a short pre-roll
      const keep = Math.round(PREROLL_SEC * ASR_SR);
      if (this.buf.length > keep * 2) this._dropFront(this.buf.length - keep);
      return;
    }
    const silence = this.nFrames * FRAME_SEC - this.lastSpeechEndT;
    if (silence >= SILENCE_COMMIT_SEC) {
      this._emit(Math.min(this.lastSpeechEndT + TAIL_SEC, this.bufStartT + dur), 'pause');
    } else if (dur >= MAX_SEG_SEC) {
      this._emit(this._quietestPoint(), 'max');
    }
  }

  _quietestPoint() {
    const total = this.buf.length;
    const lo = Math.max(Math.round(0.5 * ASR_SR), total - 3 * ASR_SR);
    const hi = total - Math.round(0.3 * ASR_SR);
    let best = hi, bestE = Infinity;
    for (let s = lo; s + FRAME <= hi; s += FRAME / 2) {
      const e = rmsOf(this.buf.subarray(s, s + FRAME));
      if (e < bestE) { bestE = e; best = s + FRAME / 2; }
    }
    return this.bufStartT + best / ASR_SR;
  }

  _emit(cutT, reason) {
    const c = this.cur;
    let idx = Math.round((cutT - this.bufStartT) * ASR_SR);
    idx = Math.max(0, Math.min(idx, this.buf.length));
    if (c.voicedFrames >= MIN_COMMIT_FRAMES && idx > 0.15 * ASR_SR) {
      this.commits.push({
        id: ++this.segCounter,
        audio: this.buf.slice(0, idx),
        pauseBefore: c.pauseBefore,
        startT: c.startT,
        endT: cutT,
        voicedSec: c.voicedFrames * FRAME_SEC,
        reason
      });
    }
    this._dropFront(idx);
    if (reason === 'max') {
      this.curId++;
      this.cur = { hasSpeech: true, voicedFrames: MIN_RUN_FRAMES, pauseBefore: 0, startT: cutT };
    } else {
      this.cur = this._newSeg();
    }
  }

  _dropFront(n) {
    this.buf = this.buf.slice(n);
    this.bufStartT += n / ASR_SR;
  }

  takeCommits() { const o = this.commits; this.commits = []; return o; }

  // call when the user presses Stop: emits whatever speech is still buffered
  flush() {
    if (this.cur.hasSpeech) {
      this._emit(Math.min(this.lastSpeechEndT + TAIL_SEC, this.bufStartT + this.buf.length / ASR_SR), 'stop');
    }
    return this.takeCommits();
  }

  // snapshot of the phrase currently being spoken (for the live "interim" text)
  peekInterim() {
    const c = this.cur;
    if (!c.hasSpeech || c.voicedFrames < 30) return null;
    return { key: this.curId, audio: this.buf.slice(0), voicedSec: c.voicedFrames * FRAME_SEC };
  }

  // seconds of silence since the last word (live pause indicator)
  currentSilence() {
    if (!this.everSpoke || this.speaking) return 0;
    return Math.max(0, this.nFrames * FRAME_SEC - this.lastSpeechEndT);
  }

  // time actually spent talking = speaking span minus the long pauses
  articulationSec() {
    if (!this.everSpoke) return 0;
    const span = this.lastSpeechEndT - this.firstSpeechT;
    const paused = this.pauses.reduce((a, p) => a + p.duration, 0);
    return Math.max(0, span - paused);
  }
}

// ─── Whisper output clean-up ───
const HALLUCINATION_RE = /thanks? for watching|thank you for watching|please subscribe|don'?t forget to (like|subscribe)|subtitles? by[^.]*|transcribed by[^.]*|amara\.org[^.]*|terima kasih (telah|sudah) menonton|subtitle oleh[^.]*|terjemahan oleh[^.]*|jangan lupa (subscribe|like)[^.]*/gi;

function cleanAsrText(raw) {
  let t = (raw || '').replace(/\s+/g, ' ').trim();
  t = t.replace(/[\[\(][^\]\)]*[\]\)]/g, ' ');         // [Music] (applause) [BLANK_AUDIO]
  t = t.replace(HALLUCINATION_RE, ' ');
  // the same 1–4 word phrase repeated 4+ times = decoder loop → keep one
  t = t.replace(/\b((?:[\w']+\s+){0,3}[\w']+)(?:[\s,.!?]+\1\b){3,}/gi, '$1');
  t = t.replace(/(^|\s)[.!?,]+(?=\s|$)/g, ' ');          // punctuation left behind by the removals
  t = t.replace(/\s+/g, ' ').trim();
  if (!/[A-Za-zÀ-ÿ0-9]/.test(t)) return '';
  return t;
}

// ═══════════════════════════════════════════════════
//  LOCAL SPEECH ENGINE — GLUE (mic, Whisper Web Worker, UI updates)
//  Everything runs on this device: Whisper (Hugging Face / ONNX) executes in a
//  Web Worker via WebGPU (fast) or WASM (fallback). No external speech API.
// ═══════════════════════════════════════════════════
const TRANSFORMERS_CDN = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.2';

// Runs inside the worker (serialised with .toString()), so inference never blocks the UI.
function __asrWorkerMain() {
  let asr = null, fast = null, tf = null, attempts = [], cur = null, lang = 'en';
  let chain = Promise.resolve();
  const post = (m) => self.postMessage(m);

  async function loadFrom(start, loadId) {
    const { pipeline, env } = tf;
    env.allowLocalModels = false;
    env.useBrowserCache = true;
    for (let i = start; i < attempts.length; i++) {
      const a = attempts[i];
      const files = {};
      try {
        post({ type: 'status', text: 'Loading ' + a.label + '…' });
        asr = await pipeline('automatic-speech-recognition', a.model, {
          device: a.device,
          dtype: a.dtype,
          progress_callback: (p) => {
            if (!p || !p.file) return;
            if (p.status === 'progress' && p.total) files[p.file] = { l: p.loaded, t: p.total };
            else if (p.status === 'done' && files[p.file]) files[p.file].l = files[p.file].t;
            else return;
            let l = 0, t = 0;
            for (const k in files) { l += files[k].l; t += files[k].t; }
            if (t) post({ type: 'progress', pct: Math.round(100 * l / t), label: a.label });
          }
        });
        // warm-up: compiles WebGPU shaders / WASM kernels so the first phrase isn't slow
        post({ type: 'status', text: 'Warming up ' + a.label + '…' });
        await asr(new Float32Array(16000), Object.assign({ max_new_tokens: 4 }, a.english ? {} : { language: lang === 'id' ? 'indonesian' : 'english', task: 'transcribe' }));
        cur = Object.assign({ i }, a);
        post({ type: 'ready', loadId, lang, info: { label: a.label, device: a.device, english: a.english } });
        if (a.device !== 'webgpu') loadFast(a.english);        // background: small model for instant live preview
        return true;
      } catch (err) {
        console.warn('ASR attempt failed:', a.label, err);
        asr = null;
      }
    }
    return false;
  }

  async function loadFast(english) {
    const myLang = lang;
    try {
      const model = english ? 'onnx-community/whisper-tiny.en' : 'onnx-community/whisper-base';
      const p = await tf.pipeline('automatic-speech-recognition', model, { device: 'wasm', dtype: 'q8' });
      if (myLang !== lang) return;                                   // language changed meanwhile
      await p(new Float32Array(16000), Object.assign({ max_new_tokens: 4 }, english ? {} : { language: lang === 'id' ? 'indonesian' : 'english', task: 'transcribe' }));
      fast = p;
      post({ type: 'fastready', label: model.split('/').pop() });
    } catch (err) { console.warn('fast preview model unavailable:', err); fast = null; }
  }

  self.onmessage = (e) => {
    const m = e.data;
    if (m.type === 'load') {
      chain = chain.then(async () => {
        try {
          if (!tf) tf = await import(m.cdn);
          attempts = m.attempts; lang = m.lang; fast = null;
          const ok = await loadFrom(0, m.loadId);
          if (!ok) post({ type: 'loaderror', loadId: m.loadId, message: 'No speech model could be loaded (check internet for the first download).' });
        } catch (err) {
          post({ type: 'loaderror', loadId: m.loadId, message: String((err && err.message) || err) });
        }
      });
    } else if (m.type === 'run') {
      chain = chain.then(async () => {
        const go = () => ((m.fast && fast) ? fast : asr)(m.audio, m.opts);
        try {
          let out;
          try { out = await go(); }
          catch (err) {
            // WebGPU can fail at inference time on some drivers → fall back to the next model/device once
            if (cur && cur.device === 'webgpu' && await loadFrom(cur.i + 1, null)) out = await go();
            else throw err;
          }
          post({ type: 'result', id: m.id, text: (out && out.text) || '' });
        } catch (err) {
          post({ type: 'result', id: m.id, error: String((err && err.message) || err) });
        }
      });
    }
  };
}

// ─── model choice: biggest/fastest that this device can run ───
async function detectWebGPU() {
  try {
    if (!navigator.gpu) return false;
    return !!(await navigator.gpu.requestAdapter());
  } catch (e) { return false; }
}

function buildAttempts(lang, gpu) {
  const gpuDtype = { encoder_model: 'fp32', decoder_model_merged: 'q4' };
  const mk = (model, device, dtype, english) => ({
    model, device, dtype, english,
    label: 'Whisper ' + model.split('/').pop().replace(/^whisper-|^distil-/, (m) => m === 'distil-' ? 'distil ' : '') +
           (device === 'webgpu' ? ' · WebGPU' : ' · CPU')
  });
  const list = [];
  if (lang === 'en') {
    if (gpu) {
      list.push(mk('onnx-community/distil-small.en', 'webgpu', gpuDtype, true));   // ≈ small.en accuracy, much faster
      list.push(mk('onnx-community/whisper-small.en', 'webgpu', gpuDtype, true));
    }
    list.push(mk('onnx-community/whisper-base.en', 'wasm', 'q8', true));
  } else {
    if (gpu) list.push(mk('onnx-community/whisper-small', 'webgpu', gpuDtype, false));
    list.push(mk('onnx-community/whisper-small', 'wasm', 'q8', false));
  }
  return list;
}

// ─── worker plumbing ───
let asrWorker = null, asrReadyLang = null, asrInfo = null, asrLoadLang = null, asrLoadPromise = null;
let asrGpu = null, asrLoadSeq = 0, asrRunSeq = 0;
const asrPendingLoads = {};
const asrRunWaiters = {};

function setMeta(t) {
  const el = document.getElementById('status-meta');
  if (el) el.textContent = t || '';
}
function modelMeta() { return asrInfo ? asrInfo.label + (asrInfo.fast ? ' · live: ' + asrInfo.fast : '') : ''; }

function onAsrMessage(e) {
  const m = e.data;
  if (m.type === 'progress') {
    if (!sessionActive) setMeta('Downloading ' + m.label + ' ' + m.pct + '%');
  } else if (m.type === 'status') {
    if (!sessionActive) setMeta(m.text);
  } else if (m.type === 'ready') {
    asrInfo = m.info; asrReadyLang = m.lang;
    const p = asrPendingLoads[m.loadId];
    if (p) { delete asrPendingLoads[m.loadId]; p.resolve(); }
    if (!sessionActive) setMeta('✓ ' + modelMeta());
  } else if (m.type === 'fastready') {
    if (asrInfo) asrInfo.fast = m.label;
    if (!sessionActive) setMeta('✓ ' + modelMeta());
  } else if (m.type === 'loaderror') {
    const p = asrPendingLoads[m.loadId];
    if (p) { delete asrPendingLoads[m.loadId]; p.reject(new Error(m.message)); }
  } else if (m.type === 'result') {
    const w = asrRunWaiters[m.id];
    if (w) { delete asrRunWaiters[m.id]; w(m); }
  }
}

function ensureModel(lang) {
  if (asrReadyLang === lang) return Promise.resolve();
  if (asrLoadPromise && asrLoadLang === lang) return asrLoadPromise;
  asrLoadLang = lang;
  asrLoadPromise = (async () => {
    if (asrGpu === null) asrGpu = await detectWebGPU();
    if (!asrWorker) {
      const blob = new Blob(['(' + __asrWorkerMain.toString() + ')();'], { type: 'text/javascript' });
      asrWorker = new Worker(URL.createObjectURL(blob), { type: 'module' });
      asrWorker.onmessage = onAsrMessage;
      asrWorker.onerror = (ev) => console.error('ASR worker error:', ev.message || ev);
    }
    await new Promise((resolve, reject) => {
      const loadId = ++asrLoadSeq;
      asrPendingLoads[loadId] = { resolve, reject };
      asrWorker.postMessage({ type: 'load', loadId, lang, cdn: TRANSFORMERS_CDN, attempts: buildAttempts(lang, asrGpu) });
    });
  })();
  asrLoadPromise.catch(() => { if (asrLoadLang === lang) asrLoadPromise = null; });
  return asrLoadPromise;
}

function warmupAsr() {
  ensureModel(currentLang).catch((e) => {
    console.error(e);
    if (!sessionActive) setStatus('idle', ('Model error: ' + (e.message || e)).slice(0, 200));
  });
}

function asrRun(audio, opts, fast) {
  return new Promise((resolve) => {
    const id = ++asrRunSeq;
    const timer = setTimeout(() => {                 // worker died / hung: don't freeze the session
      if (asrRunWaiters[id]) { delete asrRunWaiters[id]; resolve({ id, error: 'ASR timed out' }); }
    }, 90000);
    asrRunWaiters[id] = (m) => { clearTimeout(timer); resolve(m); };
    asrWorker.postMessage({ type: 'run', id, audio, opts, fast: !!fast }, [audio.buffer]);
  });
}

// Whisper behaves better when quiet recordings are brought to a normal level
function prepAudio(a) {
  let peak = 0;
  for (let i = 0; i < a.length; i++) { const v = Math.abs(a[i]); if (v > peak) peak = v; }
  const out = new Float32Array(a.length);
  const g = (peak > 0 && peak < 0.4) ? Math.min(0.6 / peak, 12) : 1;
  for (let i = 0; i < a.length; i++) out[i] = a[i] * g;
  return out;
}

function decodeOpts(sec) {
  // token cap ≈ speaking speed × duration: stops runaway repetition loops, saves time
  const o = { max_new_tokens: Math.min(400, Math.ceil(sec * 10) + 24) };
  if (!asrInfo || !asrInfo.english) { o.language = currentLang === 'id' ? 'indonesian' : 'english'; o.task = 'transcribe'; }
  return o;
}

// ─── session state ───
let seg = null, resampler = null;
let commitQueue = [], asrBusy = false, sessionEpoch = 0;
let interimText = '', pendingPause = 0, lastInferMs = 0, lastInterimMs = 0, lastInterimAt = 0;
let micStream = null, audioCtx = null, srcNode = null, procNode = null, muteNode = null;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function appendFinal(text, gap) {
  if (gap >= PAUSE_MIN_SEC && finalTranscript.trim()) finalTranscript += (gap >= PAUSE_LONG_SEC ? '// ' : '/ ');
  finalTranscript += text + ' ';
}

function interimDue() {
  if (!sessionActive) return null;
  // adaptive: never queue interim work faster than the device can finish it
  if (performance.now() - lastInterimAt < Math.max(600, lastInterimMs * 0.8)) return null;
  return seg.peekInterim();
}

async function runCommit(job, epoch) {
  const t0 = performance.now();
  const out = await asrRun(prepAudio(job.audio), decodeOpts(job.audio.length / ASR_SR));
  lastInferMs = performance.now() - t0;
  if (epoch !== sessionEpoch) return;
  if (out.error) throw new Error(out.error);
  const text = cleanAsrText(out.text);
  const gap = Math.max(job.pauseBefore, pendingPause);
  if (text) { appendFinal(text, gap); pendingPause = 0; }
  else if (gap) pendingPause = gap;            // segment was noise → keep its pause for the next phrase
  interimText = '';
  renderLive();
}

async function runInterim(it, epoch) {
  const t0 = performance.now();
  const out = await asrRun(prepAudio(it.audio), decodeOpts(it.audio.length / ASR_SR), true);   // small model → fast preview
  lastInterimMs = performance.now() - t0;
  lastInterimAt = performance.now();
  if (epoch !== sessionEpoch) return;
  if (out.error) throw new Error(out.error);
  if (it.key === seg.curId) { interimText = cleanAsrText(out.text); renderLive(); }
}

async function pump() {
  if (asrBusy) return;
  asrBusy = true;
  const epoch = sessionEpoch;
  try {
    while (epoch === sessionEpoch) {
      const job = commitQueue.shift();
      if (job) { await runCommit(job, epoch); continue; }
      const it = interimDue();
      if (it) { await runInterim(it, epoch); continue; }
      break;
    }
  } catch (e) {
    console.error('ASR error:', e);
    if (epoch === sessionEpoch) setMeta(('ASR error: ' + (e.message || e)).slice(0, 160));
  } finally {
    asrBusy = false;
  }
}

async function drainQueue() {
  while (commitQueue.length || asrBusy) { pump(); await sleep(60); }
}

function liveStats() {
  const clean = finalTranscript.replace(/\s*\/+\s*/g, ' ').trim();
  const text = (clean + ' ' + interimText).trim();
  const words = text ? text.split(/\s+/).filter(Boolean).length : 0;
  return { text, words };
}

function renderLive() {
  const has = finalTranscript || interimText;
  document.getElementById('transcript-placeholder').style.display = has ? 'none' : 'flex';
  document.getElementById('final-text').textContent = finalTranscript;
  document.getElementById('interim-text').textContent = interimText;
  const area = document.getElementById('transcript-area');
  area.scrollTop = area.scrollHeight;
  const { text, words } = liveStats();
  fillerCountLive = countFillers(text);
  const elapsed = seg ? seg.totalSec : 0;
  updateLiveMetrics(elapsed > 3 ? Math.round(words / elapsed * 60) : 0, words, fillerCountLive);
}

// ─── session control ───
function teardownAudio() {
  try { if (procNode) { procNode.onaudioprocess = null; procNode.disconnect(); } } catch (_) {}
  try { if (srcNode) srcNode.disconnect(); } catch (_) {}
  try { if (muteNode) muteNode.disconnect(); } catch (_) {}
  if (micStream) micStream.getTracks().forEach((t) => t.stop());
  if (audioCtx) { try { audioCtx.close(); } catch (_) {} }
  procNode = srcNode = muteNode = micStream = audioCtx = null;
}

async function startSession() {
  sessionEpoch++;
  seg = new Segmenter();
  commitQueue = []; interimText = ''; pendingPause = 0; lastInterimAt = 0;
  finalTranscript = ''; pauses = []; fillerCountLive = 0; sessionDuration = 0;
  document.getElementById('final-text').textContent = '';
  document.getElementById('interim-text').textContent = '';
  document.getElementById('transcript-placeholder').style.display = 'flex';
  document.getElementById('report-section').classList.remove('visible');
  updateLiveMetrics(0, 0, 0);
  document.getElementById('live-duration').textContent = '0:00';
  document.getElementById('btn-start').disabled = true;
  try {
    // create the AudioContext inside the click so the browser lets it run even if the model is still loading
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    audioCtx.resume();
    setStatus('analyzing', 'Loading speech model…');
    while (asrReadyLang !== currentLang) await ensureModel(currentLang);   // normally already preloaded
    micStream = await navigator.mediaDevices.getUserMedia({ audio: {
      channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true
    }});
    await audioCtx.resume();
    resampler = new StreamResampler(audioCtx.sampleRate);
    srcNode = audioCtx.createMediaStreamSource(micStream);
    procNode = audioCtx.createScriptProcessor(4096, 1, 1);
    procNode.onaudioprocess = (e) => {
      if (!sessionActive) return;
      seg.push(resampler.process(e.inputBuffer.getChannelData(0)));
      const c = seg.takeCommits();
      if (c.length) commitQueue.push(...c);
      pump();
    };
    muteNode = audioCtx.createGain(); muteNode.gain.value = 0;      // keep graph alive, no feedback
    srcNode.connect(procNode); procNode.connect(muteNode); muteNode.connect(audioCtx.destination);

    sessionActive = true;
    sessionStartTime = Date.now();
    sessionTimerInterval = setInterval(() => {
      document.getElementById('live-duration').textContent = formatTime(seg.totalSec);
      const sil = seg.currentSilence();
      setMeta(sil >= PAUSE_MIN_SEC ? '⏸ pause ' + sil.toFixed(1) + 's' : modelMeta());
      renderLive();
    }, 500);
    setStatus('recording', modelMeta());
    document.getElementById('btn-stop').disabled = false;
  } catch (e) {
    console.error(e);
    sessionActive = false;
    teardownAudio();
    document.getElementById('btn-start').disabled = false;
    setStatus('idle', 'Microphone permission / model download is required');
    alert('Please allow microphone access and make sure the speech model can be downloaded (needs internet only the first time), then try again.');
  }
}

async function stopSession() {
  if (!sessionActive) return;
  sessionActive = false;
  clearInterval(sessionTimerInterval);
  document.getElementById('btn-stop').disabled = true;
  teardownAudio();
  setStatus('analyzing', 'Finishing local transcription…');
  commitQueue.push(...seg.flush());
  await drainQueue();
  interimText = '';
  renderLive();
  sessionDuration = seg.totalSec;
  document.getElementById('live-duration').textContent = formatTime(sessionDuration);
  buildReport();
  document.getElementById('btn-start').disabled = false;
}

function resetSession() {
  sessionActive = false; clearInterval(sessionTimerInterval);
  sessionEpoch++;                                   // any in-flight result is discarded
  teardownAudio();
  commitQueue = []; interimText = ''; pendingPause = 0;
  seg = null; finalTranscript = ''; pauses = []; fillerCountLive = 0; sessionDuration = 0;
  document.getElementById('final-text').textContent = '';
  document.getElementById('interim-text').textContent = '';
  document.getElementById('transcript-placeholder').style.display = 'flex';
  document.getElementById('report-section').classList.remove('visible');
  document.getElementById('live-duration').textContent = '0:00';
  document.getElementById('live-wpm').textContent = '—';
  document.getElementById('live-words').textContent = '0';
  document.getElementById('live-fillers').textContent = '0';
  document.getElementById('btn-start').disabled = false;
  document.getElementById('btn-stop').disabled = true;
  setStatus('idle', asrReadyLang === currentLang ? '✓ ' + modelMeta() : '');
}
function updateUI() { document.getElementById('btn-stop').disabled = true; }


// ═══════════════════════════════════════════════════
//  ANALYSIS ENGINE
// ═══════════════════════════════════════════════════
function countFillers(text) {
  if (!text) return 0;
  const lower = text.toLowerCase();
  let count = 0;
  FILLERS[currentLang].forEach(f => {
    const regex = new RegExp(`\\b${escapeRegex(f)}\\b`, 'gi');
    const matches = lower.match(regex);
    if (matches) count += matches.length;
  });
  return count;
}

function getFillerBreakdown(text) {
  const lower = text.toLowerCase();
  const result = {};
  FILLERS[currentLang].forEach(f => {
    const regex = new RegExp(`\\b${escapeRegex(f)}\\b`, 'gi');
    const matches = lower.match(regex);
    if (matches && matches.length > 0) result[f] = matches.length;
  });
  return result;
}

function extractKeywords(text) {
  const stops = currentLang === 'en' ? STOP_WORDS_EN : STOP_WORDS_ID;
  const words = text.toLowerCase().match(/\b[a-zA-ZÀ-ÿ]{4,}\b/g) || [];
  const freq = {};
  words.forEach(w => {
    if (!stops.has(w) && !FILLERS[currentLang].includes(w)) {
      freq[w] = (freq[w] || 0) + 1;
    }
  });
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([word, count]) => ({ word, count }));
}

function highlightFillers(text) {
  if (!text.trim()) return '';
  let result = escapeHtml(text);
  // Style pause markers FIRST (longest token first to avoid double-replacement)
  result = result.replace(/ \/{2} /g, '<span class="pause-marker long" title="Long pause (>3s)">//</span>');
  result = result.replace(/ \/ /g, '<span class="pause-marker short" title="Short pause (1.5–3s)">/</span>');
  // Sort fillers by length (longest first) to avoid partial replacements
  const sorted = [...FILLERS[currentLang]].sort((a, b) => b.length - a.length);
  sorted.forEach(f => {
    const regex = new RegExp(`\\b(${escapeRegex(f)})\\b`, 'gi');
    result = result.replace(regex, `<span class="filler-highlight">$1</span>`);
  });
  return result;
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function buildReport() {
  const duration = sessionDuration || (sessionStartTime ? (Date.now() - sessionStartTime) / 1000 : 0);
  const text = finalTranscript.trim();
  // pauses come from the audio timeline (VAD), not from the ASR text
  pauses = seg ? seg.pauses.map(p => ({ duration: p.duration, time: formatTime(p.time) })) : [];
  articulationTime = seg ? seg.articulationSec() : 0;
  const pauseTotal = Math.round(pauses.reduce((s, p) => s + p.duration, 0) * 10) / 10;
  const pauseLongest = pauses.reduce((m, p) => Math.max(m, p.duration), 0);
  // Strip pause markers before counting words / WPM
  const cleanText = text.replace(/\s*\/+\s*/g, ' ');
  const words = cleanText ? cleanText.split(/\s+/).filter(Boolean) : [];
  const totalWords = words.length;
  const wpm = duration > 0 ? Math.round((totalWords / duration) * 60) : 0;
  const fillerBreakdown = getFillerBreakdown(cleanText);
  const totalFillers = Object.values(fillerBreakdown).reduce((a, b) => a + b, 0);
  const fillerPct = totalWords > 0 ? Math.round((totalFillers / totalWords) * 100) : 0;
  const keywords = extractKeywords(cleanText);
  const highlighted = highlightFillers(text);

  // ─── Stats Grid ───
  const statsGrid = document.getElementById('report-stats-grid');
  const stats = [
    { icon: '⏱️', val: formatTime(duration), lbl: currentLang==='en'?'Duration':'Durasi', sub: '' },
    { icon: '💬', val: totalWords, lbl: currentLang==='en'?'Total Words':'Total Kata', sub: '' },
    { icon: '📈', val: wpm, lbl: currentLang==='en'?'Avg WPM':'Rata-rata KPM', sub: articulationTime > 3 ? Math.round(totalWords / articulationTime * 60) + (currentLang==='en'?' excl. pauses':' tanpa jeda') : (currentLang==='en'?'Words per minute':'Kata per menit') },
    { icon: '🔴', val: totalFillers, lbl: currentLang==='en'?'Filler Words':'Kata Filler', sub: `${fillerPct}% ${currentLang==='en'?'of words':'dari kata'}` },
    { icon: '⏸️', val: pauses.length, lbl: currentLang==='en'?'Pauses':'Jeda', sub: pauses.length ? (currentLang==='en'?'>1.5s · total ':'>1,5s · total ') + pauseTotal + 's' : (currentLang==='en'?'>1.5s gaps':'>1,5s jeda') },
    { icon: '🔑', val: keywords.length, lbl: currentLang==='en'?'Key Topics':'Topik Kunci', sub: '' },
  ];
  statsGrid.innerHTML = stats.map(s => `
    <div class="stat-card">
      <span class="stat-icon">${s.icon}</span>
      <span class="stat-val">${s.val}</span>
      <span class="stat-lbl">${s.lbl}</span>
      ${s.sub ? `<span class="stat-sub">${s.sub}</span>` : ''}
    </div>
  `).join('');

  // ─── Filler Tags ───
  const fillerTags = document.getElementById('filler-tags');
  document.getElementById('filler-summary').textContent = totalFillers > 0
    ? LABELS[currentLang].fillerSummary(totalFillers, fillerPct)
    : L('noFillers');
  fillerTags.innerHTML = Object.entries(fillerBreakdown).length > 0
    ? Object.entries(fillerBreakdown)
        .sort((a,b) => b[1]-a[1])
        .map(([w, c]) => `<span class="filler-tag">${w} ×${c}</span>`)
        .join('')
    : '';

  // ─── Keywords ───
  const kwTags = document.getElementById('keyword-tags');
  kwTags.innerHTML = keywords.length > 0
    ? keywords.map(k => `<span class="keyword-tag">${k.word} <small style="opacity:.6">×${k.count}</small></span>`).join('')
    : `<span style="color:#90a4ae;font-size:.85rem">${L('noKeywords')}</span>`;

  // ─── Pauses ───
  const pauseList = document.getElementById('pause-list');
  document.getElementById('pause-summary').textContent = LABELS[currentLang].pauseSummary(pauses.length, pauseTotal, pauseLongest);
  pauseList.innerHTML = pauses.length > 0
    ? pauses.map(p => `
        <div class="pause-item">
          <div class="pause-bar" style="width:${Math.min(p.duration*20, 120)}px"></div>
          <span>${currentLang==='en'?'At':'Pada'} ${p.time} — ${p.duration}s ${currentLang==='en'?'pause':'jeda'}</span>
        </div>`).join('')
    : `<span style="color:#90a4ae;font-size:.85rem">${L('noPauses')}</span>`;

  // ─── Final Transcript ───
  document.getElementById('final-transcript-display').innerHTML = highlighted || `<span style="color:#90a4ae;font-style:italic">${currentLang==='en'?'No transcript recorded.':'Tidak ada transkrip.'}</span>`;

  // ─── Show Report ───
  document.getElementById('report-section').classList.add('visible');
  setStatus('done');
  document.getElementById('report-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ═══════════════════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════════════════
function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${String(s).padStart(2,'0')}`;
}

function updateLiveMetrics(wpm, words, fillers) {
  document.getElementById('live-wpm').textContent = wpm || '—';
  document.getElementById('live-words').textContent = words;
  document.getElementById('live-fillers').textContent = fillers;
}

// Keyboard accessibility for mode cards
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.mode-card').forEach(card => {
    card.addEventListener('keypress', e => { if (e.key === 'Enter' || e.key === ' ') card.click(); });
  });
});

// ═══════════════════════════════════════════════════
//  BOOT
// ═══════════════════════════════════════════════════
init();
</script>
</body>
</html>
"""

components.html(HTML, height=1600, scrolling=True)
