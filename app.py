import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="InterviewCoach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sembunyikan default header/footer Streamlit
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    .stApp { background: #E3F2FD; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  APP HTML / CSS / JS WITH WHISPER-SMALL (ONNX Transformers.js)
# ─────────────────────────────────────────────────────────────────────────────
HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>InterviewCoach</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
<style>
:root {
  --clr-lightest:  #E3F2FD;
  --clr-light:     #90CAF9;
  --clr-mid:       #42A5F5;
  --clr-primary:   #2196F3;
  --clr-dark:      #0D47A1;
  --clr-darker:    #082f7a;
  --clr-white:     #ffffff;
  --clr-glass:     rgba(255,255,255,0.75);
  --clr-glass-border: rgba(145,202,249,0.45);
  --clr-filler-bg: #FFF3E0;
  --clr-filler:    #E65100;
  --clr-interim:   rgba(33,150,243,0.55);
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

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--clr-lightest); }
::-webkit-scrollbar-thumb { background: var(--clr-light); border-radius: 99px; }

/* HEADER */
.header {
  background: linear-gradient(135deg, var(--clr-dark) 0%, #1565C0 60%, var(--clr-primary) 100%);
  padding: 22px 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}
.header-left { display: flex; align-items: center; gap: 16px; z-index: 1; }
.logo-icon {
  width: 48px; height: 48px;
  background: rgba(255,255,255,.15);
  border: 2px solid rgba(255,255,255,.3);
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px;
  backdrop-filter: blur(8px);
}
.header-text h1 {
  font-family: var(--font-head);
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.5px;
  line-height: 1.1;
}
.header-text p {
  font-size: 0.8rem;
  color: rgba(255,255,255,.8);
  margin-top: 3px;
}
.header-right { display: flex; align-items: center; gap: 12px; z-index: 1; }

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
}
.lang-btn.active {
  background: rgba(255,255,255,.25);
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}

/* MAIN LAYOUT */
.main { padding: 28px 36px; max-width: 1400px; margin: 0 auto; }
.grid-top { display: grid; grid-template-columns: 340px 1fr; gap: 24px; margin-bottom: 24px; }
.grid-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }

/* CARD */
.card {
  background: var(--clr-glass);
  border: 1px solid var(--clr-glass-border);
  border-radius: var(--radius-xl);
  padding: 24px;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}
.card:hover { box-shadow: var(--shadow-lg); }
.card-title {
  font-family: var(--font-head);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--clr-dark);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* MODE CARDS */
.mode-list { display: flex; flex-direction: column; gap: 10px; }
.mode-card {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  background: rgba(255,255,255,.6);
  cursor: pointer;
  transition: var(--transition);
}
.mode-card:hover, .mode-card.active {
  background: #fff;
  border-color: var(--clr-primary);
  box-shadow: 0 4px 16px rgba(33,150,243,.15);
}
.mode-card:hover .mode-icon, .mode-card.active .mode-icon { background: rgba(33,150,243,.12); }
.mode-card:hover .mode-text strong, .mode-card.active .mode-text strong { color: var(--clr-primary); }
.mode-icon {
  width: 42px; height: 42px; border-radius: var(--radius-sm);
  background: var(--clr-lightest);
  display: flex; align-items: center; justify-content: center;
  font-size: 19px;
  flex-shrink: 0;
}
.mode-text strong {
  display: block;
  font-family: var(--font-head);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--clr-dark);
}
.mode-text span { font-size: 0.74rem; color: #5c7099; }

/* QUESTION PANEL */
.question-panel {
  margin-top: 16px;
  padding: 14px;
  background: rgba(255,255,255,.6);
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-glass-border);
  display: none;
}
.question-panel.visible { display: block; }
.q-select {
  width: 100%;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--clr-light);
  background: #fff;
  font-size: 0.82rem;
  color: var(--clr-dark);
  cursor: pointer;
  outline: none;
}
.q-display {
  margin-top: 10px;
  padding: 12px 14px;
  background: #fff;
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--clr-primary);
  font-size: 0.85rem;
  color: var(--clr-dark);
  font-weight: 500;
  line-height: 1.4;
  min-height: 48px;
  display: flex;
  align-items: center;
}
.q-display.empty { color: #90a4ae; font-style: italic; }

.btn-random {
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  background: linear-gradient(135deg, var(--clr-primary), var(--clr-dark));
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-head);
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
}

/* STATUS BAR */
.status-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  font-family: var(--font-head);
  font-size: 0.82rem;
  font-weight: 600;
}
.status-bar.idle { background: rgba(144,202,249,.25); border: 1.5px solid var(--clr-light); color: var(--clr-dark); }
.status-bar.listening { background: rgba(33,150,243,.12); border: 1.5px solid var(--clr-primary); color: var(--clr-primary); }
.status-bar.recording { background: rgba(244,67,54,.1); border: 1.5px solid #ef5350; color: #c62828; }
.status-bar.analyzing { background: rgba(156,39,176,.1); border: 1.5px solid #ab47bc; color: #6a1b9a; }
.status-bar.done { background: rgba(76,175,80,.12); border: 1.5px solid #66bb6a; color: #2e7d32; }
.status-dot { width: 9px; height: 9px; border-radius: 50%; }
.status-bar.idle .status-dot { background: var(--clr-light); }
.status-bar.listening .status-dot { background: var(--clr-primary); }
.status-bar.recording .status-dot { background: #ef5350; animation: pulse-red 0.8s infinite; }
.status-bar.analyzing .status-dot { background: #ab47bc; animation: pulse-purple 1s infinite; }
.status-bar.done .status-dot { background: #66bb6a; }

@keyframes pulse-red {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239,83,80,.6); }
  50% { box-shadow: 0 0 0 6px rgba(239,83,80,0); }
}
@keyframes pulse-purple {
  0%, 100% { box-shadow: 0 0 0 0 rgba(171,71,188,.5); }
  50% { box-shadow: 0 0 0 6px rgba(171,71,188,0); }
}
.status-meta { margin-left: auto; font-size: 0.78rem; font-weight: 500; opacity: 0.85; }

/* CONTROLS */
.controls { display: flex; gap: 10px; margin-bottom: 16px; }
.btn {
  flex: 1; padding: 12px 18px;
  border-radius: var(--radius-md);
  border: none;
  font-family: var(--font-head);
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-start { background: linear-gradient(135deg, var(--clr-primary), var(--clr-dark)); color: #fff; }
.btn-start:hover:not(:disabled) { box-shadow: 0 4px 14px rgba(33,150,243,.4); }
.btn-stop { background: rgba(239,83,80,.12); color: #c62828; border: 1.5px solid rgba(239,83,80,.4); }
.btn-reset { background: rgba(144,202,249,.3); color: var(--clr-dark); border: 1.5px solid var(--clr-light); flex: 0; padding: 12px 16px; }
.btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* LIVE TRANSCRIPT */
.transcript-area {
  min-height: 200px;
  max-height: 300px;
  overflow-y: auto;
  padding: 18px;
  background: rgba(255,255,255,.6);
  border-radius: var(--radius-md);
  border: 1.5px solid var(--clr-glass-border);
  font-size: 0.95rem;
  line-height: 1.8;
  color: #1a237e;
  position: relative;
}
.transcript-area .placeholder {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 10px; color: #90a4ae; font-size: 0.88rem; pointer-events: none;
}

.live-metrics { display: flex; gap: 10px; margin-top: 12px; }
.live-metric {
  flex: 1; padding: 8px 12px;
  background: rgba(255,255,255,.6);
  border-radius: var(--radius-sm);
  border: 1px solid var(--clr-glass-border);
  text-align: center;
}
.live-metric .lm-val {
  font-family: var(--font-head);
  font-size: 1.25rem; font-weight: 800; color: var(--clr-dark); display: block;
}
.live-metric .lm-lbl { font-size: 0.68rem; font-weight: 600; color: #5c7099; text-transform: uppercase; }

/* REPORT SECTION */
.report-section { display: none; margin-top: 24px; }
.report-section.visible { display: block; }
.report-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px;
}
.stat-card {
  padding: 16px 14px;
  background: rgba(255,255,255,.7);
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-glass-border);
  text-align: center;
}
.stat-card .stat-icon { font-size: 1.6rem; margin-bottom: 6px; display: block; }
.stat-card .stat-val { font-family: var(--font-head); font-size: 1.5rem; font-weight: 800; color: var(--clr-dark); }
.stat-card .stat-lbl { font-size: 0.72rem; font-weight: 600; color: #5c7099; text-transform: uppercase; margin-top: 4px; }

.filler-tags, .keyword-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.filler-tag {
  padding: 3px 10px; background: #FFF3E0; border: 1px solid #FFCC80; border-radius: 99px;
  font-size: 0.78rem; font-weight: 600; color: #E65100;
}
.keyword-tag {
  padding: 4px 10px; background: rgba(33,150,243,.1); border: 1px solid rgba(33,150,243,.25);
  border-radius: 99px; font-size: 0.78rem; font-weight: 600; color: var(--clr-dark);
}
.pause-list { margin-top: 10px; display: flex; flex-direction: column; gap: 6px; }
.pause-item {
  display: flex; align-items: center; gap: 10px; padding: 6px 10px;
  background: rgba(255,255,255,.6); border-radius: var(--radius-sm); font-size: 0.8rem; color: var(--clr-dark);
}
.pause-bar { height: 5px; background: linear-gradient(90deg, var(--clr-light), var(--clr-primary)); border-radius: 99px; min-width: 15px; }

.final-transcript {
  padding: 18px; background: rgba(255,255,255,.7);
  border-radius: var(--radius-md); border: 1.5px solid var(--clr-glass-border);
  font-size: 0.93rem; line-height: 1.9; color: #1a237e; max-height: 280px; overflow-y: auto;
}
.filler-highlight {
  background: #FFF3E0; color: var(--clr-filler); border-radius: 4px; padding: 1px 5px;
  font-weight: 600; border-bottom: 2px solid #FFCC80;
}
.pause-marker {
  display: inline-block; font-family: monospace; font-weight: 800; font-size: 0.88em;
  border-radius: 4px; padding: 1px 6px; margin: 0 3px; vertical-align: middle;
}
.pause-marker.short { color: #1565C0; background: rgba(33,150,243,.12); border: 1px solid rgba(33,150,243,.3); }
.pause-marker.long { color: #6a1b9a; background: rgba(156,39,176,.12); border: 1px solid rgba(156,39,176,.3); }

.browser-warning {
  display: none; padding: 16px 20px; background: #fff3e0; border: 2px solid #ffcc80;
  border-radius: var(--radius-md); color: #e65100; font-weight: 500; text-align: center; margin: 20px 36px;
}
.section-divider { height: 1px; background: linear-gradient(90deg, var(--clr-light), transparent); margin: 16px 0; }
</style>
</head>
<body>

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
      <button class="lang-btn active" id="lang-en" onclick="setLang('en')">🇬🇧 English</button>
      <button class="lang-btn" id="lang-id" onclick="setLang('id')">🇮🇩 Indonesia</button>
    </div>
  </div>
</header>

<div class="browser-warning" id="browser-warning">
  <strong>Microphone Not Available</strong><br/>
  Please allow microphone access in your browser settings to practice.
</div>

<main class="main" id="app-main">
  <div class="grid-top">
    <div>
      <div class="card">
        <div class="card-title"><span>⚙️</span> <span id="label-practice-mode">Practice Mode</span></div>
        <div class="mode-list">
          <div class="mode-card active" id="mode-free" onclick="selectMode('free')">
            <div class="mode-icon">🗣️</div>
            <div class="mode-text">
              <strong id="label-mode-free">Free Speak</strong>
              <span id="label-mode-free-sub">Talk freely, no question</span>
            </div>
          </div>
          <div class="mode-card" id="mode-choose" onclick="selectMode('choose')">
            <div class="mode-icon">📋</div>
            <div class="mode-text">
              <strong id="label-mode-choose">Choose Question</strong>
              <span id="label-mode-choose-sub">Pick from 50 questions</span>
            </div>
          </div>
          <div class="mode-card" id="mode-random" onclick="selectMode('random')">
            <div class="mode-icon">🎲</div>
            <div class="mode-text">
              <strong id="label-mode-random">Random Question</strong>
              <span id="label-mode-random-sub">Surprise me!</span>
            </div>
          </div>
        </div>

        <div class="question-panel" id="choose-panel">
          <select class="q-select" id="question-select" onchange="onQuestionSelect()">
            <option value="">— Select a question —</option>
          </select>
          <div class="q-display empty" id="q-display">No question selected</div>
        </div>

        <div class="question-panel" id="random-panel">
          <div class="q-display" id="random-display">Click below to generate a question</div>
          <button class="btn-random" id="btn-randomize" onclick="randomizeQuestion()">
            🎲 <span id="label-roll">Roll a Question</span>
          </button>
        </div>
      </div>
    </div>

    <div>
      <div class="card">
        <div class="card-title"><span>🎙️</span> <span id="label-live-session">Live Session</span></div>

        <div class="status-bar idle" id="status-bar">
          <div class="status-dot"></div>
          <span id="status-text">Ready to start</span>
          <div class="status-meta" id="status-meta"></div>
        </div>

        <div class="controls">
          <button class="btn btn-start" id="btn-start" onclick="startSession()">
            ▶ <span id="label-start">Start Recording</span>
          </button>
          <button class="btn btn-stop" id="btn-stop" onclick="stopSession()" disabled>
            ■ <span id="label-stop">Stop</span>
          </button>
          <button class="btn btn-reset" id="btn-reset" onclick="resetSession()">↺</button>
        </div>

        <div class="card-title" style="margin-bottom:8px;">
          <span>📝</span> <span id="label-live-transcript">Live Transcript</span>
        </div>
        <div class="transcript-area" id="transcript-area">
          <div class="placeholder" id="transcript-placeholder">
            <span style="font-size:2rem; opacity:.5;">🎤</span>
            <span id="label-placeholder">Press Start and begin speaking…</span>
          </div>
          <span id="final-text"></span>
        </div>

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
  </div>

  <div class="report-section" id="report-section">
    <div class="card-title" style="font-size:1.1rem; margin-bottom:16px;">
      📊 <span id="label-session-report">Session Report</span>
    </div>

    <div class="report-grid" id="report-stats-grid"></div>

    <div class="grid-bottom">
      <div>
        <div class="card">
          <div class="card-title"><span>🔴</span> <span id="label-filler-analysis">Filler Word Analysis</span></div>
          <p id="filler-summary" style="font-size:.82rem; color:#5c7099; margin-bottom:10px;"></p>
          <div class="filler-tags" id="filler-tags"></div>

          <div class="section-divider"></div>

          <div class="card-title"><span>🔑</span> <span id="label-top-keywords">Top Keywords</span></div>
          <div class="keyword-tags" id="keyword-tags"></div>

          <div class="section-divider"></div>

          <div class="card-title"><span>⏸️</span> <span id="label-pauses">Detected Pauses</span></div>
          <p id="pause-summary" style="font-size:.82rem; color:#5c7099; margin-bottom:10px;"></p>
          <div class="pause-list" id="pause-list"></div>
        </div>
      </div>

      <div>
        <div class="card">
          <div class="card-title">
            <span>📄</span> <span id="label-final-transcript">Final Transcript</span>
            <span style="margin-left:auto; font-size:0.72rem; color:#5c7099; font-weight:400; text-transform:none;">
              <span style="background:#FFF3E0;border:1px solid #FFCC80;border-radius:4px;padding:2px 6px;color:#E65100;font-weight:600;" id="label-legend-filler">filler</span>
              <span id="label-legend-highlighted"> = highlighted</span>
            </span>
          </div>
          <div class="final-transcript" id="final-transcript-display"></div>
        </div>
      </div>
    </div>
  </div>
</main>

<script>
const QUESTIONS = {
  en: {
    "General & About You": [
      "Tell me about yourself.", "What are your greatest strengths?", "What is your biggest weakness?",
      "Where do you see yourself in five years?", "Why are you interested in this position?",
      "Why do you want to work for this company?", "What are you passionate about outside of work?",
      "How would your colleagues describe you?", "What motivates you to do your best work?", "Describe your ideal work environment."
    ],
    "Teamwork & Collaboration": [
      "Tell me about a time you worked successfully in a team.", "How do you handle conflict with a coworker?",
      "Describe a situation where you had to work with a difficult team member.", "How do you prioritize tasks when working on a team project?",
      "Give an example of when you went above and beyond for a teammate.", "How do you give and receive constructive feedback?",
      "Describe a time you led a team through a challenging project.", "How do you ensure clear communication in a remote team?",
      "Tell me about a time you influenced others to adopt your idea.", "How do you handle disagreements with your manager?"
    ],
    "Problem Solving": [
      "Describe a difficult problem you solved at work.", "Tell me about a time you made a mistake and how you handled it.",
      "How do you approach a task you've never done before?", "Give an example of a creative solution you came up with.",
      "Describe a time you had to make a decision without enough information.", "How do you handle multiple deadlines at the same time?",
      "Tell me about a time you failed and what you learned.", "Describe a situation where you had to adapt quickly to a change.",
      "How do you stay calm under pressure?", "Give an example of how you improved a process or workflow."
    ],
    "Leadership & Initiative": [
      "Tell me about a time you took initiative without being asked.", "Describe a project you led from start to finish.",
      "How do you motivate others during a difficult period?", "Tell me about a time you mentored or coached a colleague.",
      "How do you handle underperforming team members?", "Describe a situation where you had to make an unpopular decision.",
      "How do you set goals and track your progress?", "Tell me about a time you successfully managed competing priorities.",
      "Describe how you build trust with a new team.", "What's your approach to delegating tasks?"
    ],
    "Career & Role": [
      "Why should we hire you over other candidates?", "What unique skills do you bring to this role?",
      "How does this position align with your career goals?", "What do you know about our company and industry?",
      "Where did you hear about this job opening?", "What salary range are you expecting?",
      "Are you comfortable with travel or relocation?", "Do you have any questions for us?",
      "How soon can you start if offered the position?", "Describe your biggest professional achievement."
    ]
  },
  id: {
    "Umum & Tentang Diri": [
      "Ceritakan tentang diri Anda.", "Apa kekuatan terbesar Anda?", "Apa kelemahan terbesar Anda?",
      "Di mana Anda melihat diri Anda dalam lima tahun ke depan?", "Mengapa Anda tertarik dengan posisi ini?",
      "Mengapa Anda ingin bekerja di perusahaan ini?", "Apa yang Anda sukai di luar pekerjaan?",
      "Bagaimana rekan kerja Anda menggambarkan Anda?", "Apa yang memotivasi Anda untuk bekerja sebaik mungkin?", "Deskripsikan lingkungan kerja ideal Anda."
    ],
    "Kerja Tim & Kolaborasi": [
      "Ceritakan saat Anda berhasil bekerja dalam tim.", "Bagaimana Anda menangani konflik dengan rekan kerja?",
      "Ceritakan situasi di mana Anda harus bekerja dengan anggota tim yang sulit.", "Bagaimana Anda memprioritaskan tugas dalam proyek tim?",
      "Berikan contoh ketika Anda melakukan lebih dari yang diharapkan untuk rekan tim.", "Bagaimana Anda memberikan dan menerima umpan balik konstruktif?",
      "Ceritakan saat Anda memimpin tim melalui proyek yang menantang.", "Bagaimana Anda memastikan komunikasi yang jelas dalam tim jarak jauh?",
      "Ceritakan saat Anda memengaruhi orang lain untuk menerima ide Anda.", "Bagaimana Anda menangani ketidaksepakatan dengan manajer Anda?"
    ],
    "Pemecahan Masalah": [
      "Deskripsikan masalah sulit yang pernah Anda selesaikan di tempat kerja.", "Ceritakan saat Anda membuat kesalahan dan bagaimana Anda mengatasinya.",
      "Bagaimana Anda mendekati tugas yang belum pernah Anda lakukan?", "Berikan contoh solusi kreatif yang Anda temukan.",
      "Ceritakan saat Anda harus membuat keputusan tanpa informasi yang cukup.", "Bagaimana Anda menangani banyak tenggat waktu sekaligus?",
      "Ceritakan saat Anda gagal dan pelajaran yang Anda petik.", "Deskripsikan situasi di mana Anda harus beradaptasi dengan cepat terhadap perubahan.",
      "Bagaimana Anda tetap tenang di bawah tekanan?", "Berikan contoh bagaimana Anda meningkatkan proses atau alur kerja."
    ],
    "Kepemimpinan & Inisiatif": [
      "Ceritakan saat Anda mengambil inisiatif tanpa diminta.", "Deskripsikan proyek yang Anda pimpin dari awal hingga akhir.",
      "Bagaimana Anda memotivasi orang lain di saat sulit?", "Ceritakan saat Anda membimbing atau melatih rekan kerja.",
      "Bagaimana Anda menangani anggota tim yang berkinerja rendah?", "Deskripsikan situasi di mana Anda harus membuat keputusan yang tidak populer.",
      "Bagaimana Anda menetapkan tujuan dan melacak kemajuan Anda?", "Ceritakan saat Anda berhasil mengelola prioritas yang bersaing.",
      "Deskripsikan cara Anda membangun kepercayaan dengan tim baru.", "Bagaimana pendekatan Anda dalam mendelegasikan tugas?"
    ],
    "Karier & Posisi": [
      "Mengapa kami harus mempekerjakan Anda daripada kandidat lain?", "Keterampilan unik apa yang Anda bawa ke peran ini?",
      "Bagaimana posisi ini sesuai dengan tujuan karier Anda?", "Apa yang Anda ketahui tentang perusahaan dan industri kami?",
      "Dari mana Anda mendengar tentang lowongan kerja ini?", "Berapa ekspektasi gaji Anda?",
      "Apakah Anda nyaman dengan perjalanan atau relokasi?", "Apakah Anda memiliki pertanyaan untuk kami?",
      "Seberapa cepat Anda bisa mulai jika ditawari posisi ini?", "Deskripsikan pencapaian profesional terbesar Anda."
    ]
  }
};

const FILLERS = {
  en: ["um", "uh", "like", "you know", "basically", "literally", "right", "actually",
       "kind of", "sort of", "honestly", "okay", "i mean", "anyway", "you see",
       "well", "so yeah", "and stuff", "or whatever"],
  id: ["ee", "eee", "anu", "gitu", "kan", "tuh", "ya", "jadi", "soalnya", "terus",
       "nah", "intinya", "maksudnya", "gimana", "kayak", "emang", "sebenarnya",
       "begitu", "yah", "loh", "deh", "nih", "sih"]
};

const STOP_WORDS_EN = new Set(["i","me","my","we","our","you","your","he","she","it","they","them",
  "the","a","an","is","are","was","were","be","been","being","have","has","had",
  "do","does","did","will","would","could","should","may","might","shall","can",
  "to","of","in","on","at","for","with","about","by","from","up","out","as",
  "and","or","but","if","then","than","so","yet","both","either","not","no",
  "that","this","these","those","what","which","who","when","where","how","why"]);

const STOP_WORDS_ID = new Set(["saya","aku","kita","kami","kamu","anda","dia","mereka","nya",
  "yang","dan","atau","tapi","juga","ke","di","dari","untuk","dengan","pada","ini",
  "itu","ada","tidak","bisa","akan","sudah","belum","jika","kalau","karena","oleh",
  "lebih","banyak","sangat","saat","ketika","selalu","sering","pernah","dalam","lagi"]);

const LABELS = {
  en: {
    practiceMode: "Practice Mode", modeFree: "Free Speak", modeFreeSub: "Talk freely, no question",
    modeChoose: "Choose Question", modeChooseSub: "Pick from 50 questions",
    modeRandom: "Random Question", modeRandomSub: "Surprise me!",
    liveSession: "Live Session", liveTranscript: "Live Transcript",
    placeholder: "Press Start and begin speaking…",
    wpm: "WPM", duration: "Duration", words: "Words", fillers: "Fillers",
    start: "Start Recording", stop: "Stop",
    sessionReport: "Session Report", fillerAnalysis: "Filler Word Analysis",
    topKeywords: "Top Keywords", pauses: "Detected Pauses",
    finalTranscript: "Final Transcript", legendFiller: "filler", legendHighlighted: " = highlighted",
    roll: "Roll a Question", statusReady: "Ready to start",
    statusListening: "Listening…", statusRecording: "Recording", statusAnalyzing: "Analyzing…", statusDone: "Session complete",
    noFillers: "No filler words detected. Great job!", noKeywords: "No keywords found.", noPauses: "No significant pauses detected.",
    fillerSummary: (n,w) => `${n} filler word${n!==1?'s':''} detected (${w}% of words)`,
    pauseSummary: (n, t) => `${n} pause${n!==1?'s':''} detected (>1.5s) · total ${t}s`,
  },
  id: {
    practiceMode: "Mode Latihan", modeFree: "Bicara Bebas", modeFreeSub: "Bicara bebas, tanpa pertanyaan",
    modeChoose: "Pilih Pertanyaan", modeChooseSub: "Pilih dari 50 pertanyaan",
    modeRandom: "Pertanyaan Acak", modeRandomSub: "Kejutkan saya!",
    liveSession: "Sesi Langsung", liveTranscript: "Transkrip Langsung",
    placeholder: "Tekan Mulai dan mulailah berbicara…",
    wpm: "KPM", duration: "Durasi", words: "Kata", fillers: "Filler",
    start: "Mulai Rekam", stop: "Stop",
    sessionReport: "Laporan Sesi", fillerAnalysis: "Analisis Kata Filler",
    topKeywords: "Kata Kunci Utama", pauses: "Jeda Terdeteksi",
    finalTranscript: "Transkrip Akhir", legendFiller: "filler", legendHighlighted: " = disorot",
    roll: "Pilihkan Pertanyaan", statusReady: "Siap untuk memulai",
    statusListening: "Mendengarkan…", statusRecording: "Merekam", statusAnalyzing: "Menganalisis…", statusDone: "Sesi selesai",
    noFillers: "Tidak ada kata filler terdeteksi. Hebat!", noKeywords: "Tidak ada kata kunci ditemukan.", noPauses: "Tidak ada jeda signifikan terdeteksi.",
    fillerSummary: (n,w) => `${n} kata filler terdeteksi (${w}% dari total kata)`,
    pauseSummary: (n, t) => `${n} jeda terdeteksi (>1,5s) · total ${t}s`,
  }
};

let currentLang = 'en';
let currentMode = 'free';
let currentQuestion = '';
let sessionStartTime = null;
let sessionTimerInterval = null;
let finalCleanTranscript = ''; 
let transcriptChunks = [];     
let fillerCountLive = 0;
let pauses = [];
let sessionDuration = 0;
let sessionActive = false;

const ASR_SR = 16000;
const FRAME = 320;
const FRAME_SEC = FRAME / ASR_SR;

function rmsOf(x) {
  let s = 0;
  for (let i = 0; i < x.length; i++) s += x[i] * x[i];
  return Math.sqrt(s / x.length);
}

function concatF32(a, b) {
  if (!a.length) return b;
  const o = new Float32Array(a.length + b.length);
  o.set(a); o.set(b, a.length);
  return o;
}

class StreamResampler {
  constructor(srcRate, dstRate = ASR_SR) {
    this.ratio = srcRate / dstRate;
    this.left = new Float32Array(0);
    this.t = 0;
  }
  process(inp) {
    if (this.ratio === 1) return new Float32Array(inp);
    const data = concatF32(this.left, inp);
    const out = [];
    let t = this.t;
    while (t + this.ratio <= data.length) {
      const b = t + this.ratio;
      let s = 0;
      for (let j = Math.floor(t), e = Math.ceil(b); j < e; j++) {
        s += data[j] * (Math.min(j + 1, b) - Math.max(j, t));
      }
      out.push(s / this.ratio);
      t = b;
    }
    const used = Math.floor(t);
    this.left = data.slice(used);
    this.t = t - used;
    return Float32Array.from(out);
  }
}

class Segmenter {
  constructor() { this.reset(); }
  reset() {
    this.buf = new Float32Array(0);
    this.bufStartT = 0;
    this.rem = new Float32Array(0);
    this.samples = 0;
    this.nFrames = 0;
    this.noise = 0.003;
    this.voicedRun = 0;
    this.speaking = false;
    this.everSpoke = false;
    this.lastSpeechEndT = 0;
    this.firstSpeechT = 0;
    this.pauses = [];
    this.commits = [];
    this.cur = { hasSpeech: false, voicedFrames: 0, pauseBefore: 0, startT: 0 };
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
    if (rms > this.threshold()) {
      this.voicedRun++;
      if (this.voicedRun >= 5) {
        if (!this.speaking) {
          this.speaking = true;
          let gap = this.everSpoke ? (tEnd - FRAME_SEC) - this.lastSpeechEndT : 0;
          if (gap >= 1.5) {
            this.pauses.push({ time: this.lastSpeechEndT, duration: Math.round(gap * 10) / 10 });
          } else { gap = 0; }
          if (!this.everSpoke) { this.everSpoke = true; this.firstSpeechT = tEnd - FRAME_SEC; }
          if (!this.cur.hasSpeech) {
            this.cur.hasSpeech = true;
            this.cur.pauseBefore = gap;
            this.cur.startT = tEnd - FRAME_SEC;
          }
        }
        this.lastSpeechEndT = tEnd;
        this.cur.voicedFrames++;
      }
    } else {
      this.voicedRun = 0;
      this.noise += (rms - this.noise) * 0.05;
      if (this.speaking && tEnd - this.lastSpeechEndT > 0.35) this.speaking = false;
    }
  }
  _maybeCommit() {
    const dur = this.buf.length / ASR_SR;
    if (!this.cur.hasSpeech) {
      const keep = Math.round(0.4 * ASR_SR);
      if (this.buf.length > keep * 2) this.buf = this.buf.slice(this.buf.length - keep);
      return;
    }
    const silence = this.nFrames * FRAME_SEC - this.lastSpeechEndT;
    if (silence >= 0.6 || dur >= 9.0) {
      this._emit();
    }
  }
  _emit() {
    if (this.cur.voicedFrames >= 6 && this.buf.length > 0.2 * ASR_SR) {
      this.commits.push({
        audio: this.buf.slice(0),
        pauseBefore: this.cur.pauseBefore,
      });
    }
    this.buf = new Float32Array(0);
    this.cur = { hasSpeech: false, voicedFrames: 0, pauseBefore: 0, startT: 0 };
  }
  takeCommits() { const o = this.commits; this.commits = []; return o; }
  flush() {
    if (this.cur.hasSpeech) this._emit();
    return this.takeCommits();
  }
}

// ── Web Worker for Whisper-Small ──
const TRANSFORMERS_CDN = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.3.3';

function __asrWorkerMain() {
  let asr = null, tf = null, curLang = 'en';
  self.onmessage = async (e) => {
    const m = e.data;
    if (m.type === 'load') {
      try {
        if (!tf) tf = await import(m.cdn);
        tf.env.allowLocalModels = false;
        tf.env.useBrowserCache = true;
        curLang = m.lang;
        self.postMessage({ type: 'status', text: 'Loading Whisper-Small (~240MB)...' });
        
        // Pilihan device: webgpu jika ada, jika tidak fallback ke wasm
        let device = 'wasm';
        try {
          if (navigator.gpu && await navigator.gpu.requestAdapter()) device = 'webgpu';
        } catch (_) {}

        asr = await tf.pipeline('automatic-speech-recognition', 'onnx-community/whisper-small', {
          device: device,
          dtype: device === 'webgpu' ? { encoder_model: 'fp32', decoder_model_merged: 'q4' } : 'q8'
        });
        self.postMessage({ type: 'ready', lang: m.lang, device: device });
      } catch (err) {
        self.postMessage({ type: 'loaderror', message: err.message });
      }
    } else if (m.type === 'run') {
      try {
        const out = await asr(m.audio, {
          language: m.lang === 'id' ? 'indonesian' : 'english',
          task: 'transcribe',
          max_new_tokens: 150
        });
        self.postMessage({ type: 'result', id: m.id, text: out.text || '' });
      } catch (err) {
        self.postMessage({ type: 'result', id: m.id, error: err.message });
      }
    }
  };
}

let asrWorker = null, asrReady = false, asrRunSeq = 0, asrWaiters = {};

function initAsrWorker(lang) {
  if (asrWorker) asrWorker.terminate();
  const blob = new Blob(['(' + __asrWorkerMain.toString() + ')();'], { type: 'text/javascript' });
  asrWorker = new Worker(URL.createObjectURL(blob), { type: 'module' });
  asrWorker.onmessage = (e) => {
    const m = e.data;
    if (m.type === 'ready') {
      asrReady = true;
      setStatus('idle', `Model ready (Whisper-Small · ${m.device.toUpperCase()})`);
    } else if (m.type === 'status') {
      setStatus('analyzing', m.text);
    } else if (m.type === 'result') {
      if (asrWaiters[m.id]) { asrWaiters[m.id](m); delete asrWaiters[m.id]; }
    } else if (m.type === 'loaderror') {
      setStatus('idle', 'Model load error');
    }
  };
  asrWorker.postMessage({ type: 'load', cdn: TRANSFORMERS_CDN, lang: lang });
}

function runAsr(audio, lang) {
  return new Promise((resolve) => {
    const id = ++asrRunSeq;
    asrWaiters[id] = resolve;
    asrWorker.postMessage({ type: 'run', id, audio, lang }, [audio.buffer]);
  });
}

let seg = null, resampler = null, audioCtx = null, micStream = null, procNode = null, muteNode = null;
let commitQueue = [], isProcessing = false;

async function startSession() {
  seg = new Segmenter();
  commitQueue = [];
  finalCleanTranscript = '';
  transcriptChunks = [];
  pauses = [];
  fillerCountLive = 0;
  sessionDuration = 0;

  document.getElementById('final-text').textContent = '';
  document.getElementById('transcript-placeholder').style.display = 'flex';
  document.getElementById('report-section').classList.remove('visible');
  document.getElementById('btn-start').disabled = true;

  try {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
    micStream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1 } });
    resampler = new StreamResampler(audioCtx.sampleRate);
    const srcNode = audioCtx.createMediaStreamSource(micStream);
    procNode = audioCtx.createScriptProcessor(4096, 1, 1);

    procNode.onaudioprocess = (e) => {
      if (!sessionActive) return;
      seg.push(resampler.process(e.inputBuffer.getChannelData(0)));
      const c = seg.takeCommits();
      if (c.length) {
        commitQueue.push(...c);
        processQueue();
      }
    };

    muteNode = audioCtx.createGain();
    muteNode.gain.value = 0;
    srcNode.connect(procNode);
    procNode.connect(muteNode);
    muteNode.connect(audioCtx.destination);

    sessionActive = true;
    sessionStartTime = Date.now();
    sessionTimerInterval = setInterval(() => {
      document.getElementById('live-duration').textContent = formatTime(seg.totalSec);
      updateLiveMetrics();
    }, 500);

    setStatus('recording', 'Listening...');
    document.getElementById('btn-stop').disabled = false;
  } catch (err) {
    console.error(err);
    document.getElementById('btn-start').disabled = false;
    alert('Microphone access is required.');
  }
}

async function processQueue() {
  if (isProcessing || !commitQueue.length) return;
  isProcessing = true;
  while (commitQueue.length) {
    const job = commitQueue.shift();
    setStatus('recording', 'Transcribing (Whisper-Small)...');
    const res = await runAsr(job.audio, currentLang);
    if (res && res.text) {
      let txt = res.text.trim();
      if (txt) {
        transcriptChunks.push({ text: txt, gapBefore: job.pauseBefore });
        finalCleanTranscript += (finalCleanTranscript ? ' ' : '') + txt;
        document.getElementById('transcript-placeholder').style.display = 'none';
        document.getElementById('final-text').textContent = finalCleanTranscript;
        const area = document.getElementById('transcript-area');
        area.scrollTop = area.scrollHeight;
        updateLiveMetrics();
      }
    }
  }
  isProcessing = false;
  if (sessionActive) setStatus('recording', 'Listening...');
}

async function stopSession() {
  sessionActive = false;
  clearInterval(sessionTimerInterval);
  document.getElementById('btn-stop').disabled = true;

  if (procNode) { procNode.disconnect(); procNode = null; }
  if (micStream) { micStream.getTracks().forEach(t => t.stop()); micStream = null; }
  if (audioCtx) { audioCtx.close(); audioCtx = null; }

  setStatus('analyzing', 'Finishing report...');
  if (seg) commitQueue.push(...seg.flush());
  await processQueue();

  sessionDuration = seg ? seg.totalSec : 0;
  pauses = seg ? seg.pauses.map(p => ({ duration: p.duration, time: formatTime(p.time) })) : [];
  buildReport();
  document.getElementById('btn-start').disabled = false;
}

function resetSession() {
  if (sessionActive) stopSession();
  finalCleanTranscript = '';
  transcriptChunks = [];
  pauses = [];
  document.getElementById('final-text').textContent = '';
  document.getElementById('transcript-placeholder').style.display = 'flex';
  document.getElementById('report-section').classList.remove('visible');
  document.getElementById('live-duration').textContent = '0:00';
  document.getElementById('live-wpm').textContent = '—';
  document.getElementById('live-words').textContent = '0';
  document.getElementById('live-fillers').textContent = '0';
  document.getElementById('btn-start').disabled = false;
  document.getElementById('btn-stop').disabled = true;
  setStatus('idle');
}

function updateLiveMetrics() {
  const words = finalCleanTranscript.trim().split(/\s+/).filter(Boolean).length;
  const elapsed = seg ? seg.totalSec : 0;
  const wpm = elapsed > 3 ? Math.round((words / elapsed) * 60) : 0;
  fillerCountLive = countFillers(finalCleanTranscript);
  document.getElementById('live-wpm').textContent = wpm || '—';
  document.getElementById('live-words').textContent = words;
  document.getElementById('live-fillers').textContent = fillerCountLive;
}

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
  return Object.entries(freq).sort((a,b) => b[1]-a[1]).slice(0, 10).map(([word, count]) => ({ word, count }));
}

function buildReport() {
  const duration = sessionDuration || 1;
  const cleanText = finalCleanTranscript.trim();
  const words = cleanText ? cleanText.split(/\s+/).filter(Boolean) : [];
  const totalWords = words.length;
  const wpm = duration > 0 ? Math.round((totalWords / duration) * 60) : 0;
  const fillerBreakdown = getFillerBreakdown(cleanText);
  const totalFillers = Object.values(fillerBreakdown).reduce((a,b)=>a+b, 0);
  const fillerPct = totalWords > 0 ? Math.round((totalFillers / totalWords) * 100) : 0;
  const keywords = extractKeywords(cleanText);
  const pauseTotal = Math.round(pauses.reduce((a,b)=>a+b.duration, 0) * 10)/10;

  // Pasang tanda jeda / dan // HANYA di Final Report
  let reportTranscript = '';
  transcriptChunks.forEach((c) => {
    if (c.gapBefore >= 3.0) reportTranscript += ' // ';
    else if (c.gapBefore >= 1.5) reportTranscript += ' / ';
    reportTranscript += c.text + ' ';
  });

  let highlighted = reportTranscript.trim();
  highlighted = highlighted.replace(/ \/{2} /g, ' <span class="pause-marker long" title="Long pause (>3s)">//</span> ');
  highlighted = highlighted.replace(/ \/ /g, ' <span class="pause-marker short" title="Short pause (1.5-3s)">/</span> ');
  const sortedFillers = [...FILLERS[currentLang]].sort((a,b) => b.length - a.length);
  sortedFillers.forEach(f => {
    const regex = new RegExp(`\\b(${escapeRegex(f)})\\b`, 'gi');
    highlighted = highlighted.replace(regex, `<span class="filler-highlight">$1</span>`);
  });

  const stats = [
    { icon: '⏱️', val: formatTime(duration), lbl: currentLang==='en'?'Duration':'Durasi' },
    { icon: '💬', val: totalWords, lbl: currentLang==='en'?'Words':'Kata' },
    { icon: '📈', val: wpm, lbl: currentLang==='en'?'WPM':'KPM' },
    { icon: '🔴', val: totalFillers, lbl: currentLang==='en'?'Fillers':'Filler' },
    { icon: '⏸️', val: pauses.length, lbl: currentLang==='en'?'Pauses':'Jeda' },
    { icon: '🔑', val: keywords.length, lbl: currentLang==='en'?'Keywords':'Kata Kunci' }
  ];
  document.getElementById('report-stats-grid').innerHTML = stats.map(s => `
    <div class="stat-card">
      <span class="stat-icon">${s.icon}</span>
      <span class="stat-val">${s.val}</span>
      <span class="stat-lbl">${s.lbl}</span>
    </div>
  `).join('');

  document.getElementById('filler-summary').textContent = LABELS[currentLang].fillerSummary(totalFillers, fillerPct);
  document.getElementById('filler-tags').innerHTML = Object.entries(fillerBreakdown).map(([w,c]) =>
    `<span class="filler-tag">${w} ×${c}</span>`
  ).join('') || `<span style="color:#90a4ae">${LABELS[currentLang].noFillers}</span>`;

  document.getElementById('keyword-tags').innerHTML = keywords.map(k =>
    `<span class="keyword-tag">${k.word} <small>×${k.count}</small></span>`
  ).join('') || `<span style="color:#90a4ae">${LABELS[currentLang].noKeywords}</span>`;

  document.getElementById('pause-summary').textContent = LABELS[currentLang].pauseSummary(pauses.length, pauseTotal);
  document.getElementById('pause-list').innerHTML = pauses.map(p => `
    <div class="pause-item">
      <div class="pause-bar" style="width:${Math.min(p.duration*15, 100)}px"></div>
      <span>${currentLang==='en'?'At':'Pada'} ${p.time} — ${p.duration}s</span>
    </div>
  `).join('') || `<span style="color:#90a4ae">${LABELS[currentLang].noPauses}</span>`;

  document.getElementById('final-transcript-display').innerHTML = highlighted || 'No speech recorded.';
  document.getElementById('report-section').classList.add('visible');
  setStatus('done');
}

function escapeRegex(str) { return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function formatTime(s) {
  const m = Math.floor(s/60);
  const sec = Math.floor(s%60);
  return `${m}:${String(sec).padStart(2,'0')}`;
}

function setLang(lang) {
  currentLang = lang;
  document.getElementById('lang-en').classList.toggle('active', lang==='en');
  document.getElementById('lang-id').classList.toggle('active', lang==='id');
  populateQuestions();
  applyLabels();
  initAsrWorker(lang);
}

function applyLabels() {
  const l = LABELS[currentLang];
  const set = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt; };
  set('label-practice-mode', l.practiceMode);
  set('label-mode-free', l.modeFree);
  set('label-mode-free-sub', l.modeFreeSub);
  set('label-mode-choose', l.modeChoose);
  set('label-mode-choose-sub', l.modeChooseSub);
  set('label-mode-random', l.modeRandom);
  set('label-mode-random-sub', l.modeRandomSub);
  set('label-live-session', l.liveSession);
  set('label-live-transcript', l.liveTranscript);
  set('label-placeholder', l.placeholder);
  set('label-wpm', l.wpm);
  set('label-duration', l.duration);
  set('label-words', l.words);
  set('label-fillers', l.fillers);
  set('label-start', l.start);
  set('label-stop', l.stop);
  set('label-session-report', l.sessionReport);
  set('label-filler-analysis', l.fillerAnalysis);
  set('label-top-keywords', l.topKeywords);
  set('label-pauses', l.pauses);
  set('label-final-transcript', l.finalTranscript);
  set('label-legend-filler', l.legendFiller);
  set('label-legend-highlighted', l.legendHighlighted);
  set('label-roll', l.roll);
}

function populateQuestions() {
  const sel = document.getElementById('question-select');
  sel.innerHTML = `<option value="">— ${currentLang==='en'?'Select a question':'Pilih pertanyaan'} —</option>`;
  for (const [cat, qs] of Object.entries(QUESTIONS[currentLang])) {
    const og = document.createElement('optgroup');
    og.label = cat;
    qs.forEach(q => {
      const opt = document.createElement('option');
      opt.value = q; opt.textContent = q;
      og.appendChild(opt);
    });
    sel.appendChild(og);
  }
}

function selectMode(m) {
  currentMode = m;
  ['free','choose','random'].forEach(x => {
    document.getElementById(`mode-${x}`).classList.toggle('active', x===m);
  });
  document.getElementById('choose-panel').classList.toggle('visible', m==='choose');
  document.getElementById('random-panel').classList.toggle('visible', m==='random');
}

function onQuestionSelect() {
  const q = document.getElementById('question-select').value;
  const disp = document.getElementById('q-display');
  disp.textContent = q || (currentLang==='en'?'No question selected':'Belum dipilih');
  disp.classList.toggle('empty', !q);
}

function randomizeQuestion() {
  const all = [];
  for (const qs of Object.values(QUESTIONS[currentLang])) all.push(...qs);
  const q = all[Math.floor(Math.random() * all.length)];
  document.getElementById('random-display').textContent = q;
}

function setStatus(st, meta='') {
  const bar = document.getElementById('status-bar');
  bar.className = `status-bar ${st}`;
  document.getElementById('status-text').textContent = LABELS[currentLang][`status${st.charAt(0).toUpperCase()+st.slice(1)}`] || st;
  document.getElementById('status-meta').textContent = meta;
}

// Start initial worker with English
populateQuestions();
applyLabels();
initAsrWorker('en');
</script>
</body>
</html>
"""

components.html(HTML, height=1500, scrolling=True)
