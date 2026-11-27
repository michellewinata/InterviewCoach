## 🎤 InterviewCoach

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

> **Train your interview skills with real-time AI speech coaching — 100% offline, no API keys required.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌐 **2 Languages** | English 🇺🇸 and Bahasa Indonesia 🇮🇩 |
| 📋 **50 Questions** | Per language — practice, random, or free session |
| 🎲 **Random Mode** | Get a random interview question instantly |
| 🗣️ **Free Session** | Speak without a prompt to warm up |
| 📡 **Live Transcription** | Real-time transcript via Vosk while speaking |
| 📊 **Post-Session Analysis** | WPM, keywords, pauses, duration, word count, final transcript |
| ⏸️ **Pause Detection** | Short pauses `\|` (0.5–1.5s), long pauses `\|\|` (>1.5s) |
| 🎯 **Fluency Score** | 0–100 score based on WPM and pause patterns |
| 💡 **Coaching Tips** | Actionable feedback after each session |
| 🔒 **100% Offline** | No API calls — all models run locally |

---

## 🤖 ASR Models Used

| # | Model | Library | Role | Language |
|---|-------|---------|------|----------|
| 1 | **Vosk** | `vosk` | Live transcription (low-latency) | EN + ID |
| 2 | **Whisper** | `openai-whisper` | Final transcript (highest accuracy) | EN + ID |
| 3 | **Wav2Vec2** | `transformers` | Comparison / fallback | EN + ID |
| 4 | **SpeechBrain** | `speechbrain` | Comparison | EN |

Run the notebook to compare all 4 models and auto-select the best one.

---

## 📂 Project Structure

```
speechrecog/
├── app.py                    # Streamlit web application
├── analysis.py               # Speech analysis (WPM, pauses, keywords, fluency)
├── model_manager.py          # ASR model loader & transcriber
├── model_comparison.ipynb    # Model benchmarking + fine-tuning notebook
├── model_config.json         # Auto-generated: which model is best
├── requirements.txt          # Python dependencies
├── models/                   # Downloaded model weights (auto-created)
│   ├── vosk-model-en-us-0.22/
│   ├── vosk-model-id-0.21/
│   └── whisper-finetuned/
├── data/                     # Datasets (auto-created)
│   ├── english/
│   └── indonesian/
└── outputs/                  # Notebook outputs (charts, etc.)
```

---

## 🚀 Installation

### 1. Clone or place files

```bash
cd speechrecog
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> On Windows, PyAudio may need a pre-built wheel:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Download Vosk models

Place models in the `models/` directory:

| Language | Model | Download |
|----------|-------|----------|
| English | `vosk-model-en-us-0.22` | [Download (1.8GB)](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) |
| Indonesian | `vosk-model-id-0.21` | [Download (900MB)](https://alphacephei.com/vosk/models/vosk-model-id-0.21.zip) |

> Or click **▶ Load Vosk** in the app sidebar — it auto-downloads!

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📓 Notebook: Model Comparison & Fine-Tuning

```bash
jupyter notebook model_comparison.ipynb
```

The notebook will:
1. Download 10 EN + 10 ID speech samples
2. Run all 4 models on each sample
3. Compare WER, CER, Accuracy, RTF
4. Fine-tune Whisper on the combined dataset
5. Export `model_config.json` for the app

---

## 📊 Expected Model Performance

| Model | EN WER (expected) | ID WER (expected) | Avg RTF | Notes |
|-------|-------------------|-------------------|---------|-------|
| Vosk | ~15–25% | ~20–35% | ~0.1 | Fastest |
| **Whisper** | **~5–12%** | **~8–18%** | ~1.5 | **Best accuracy** |
| Wav2Vec2 | ~10–20% | ~25–40% | ~2.0 | GPU recommended |
| SpeechBrain | ~12–22% | ~40–60% | ~3.0 | EN only |

---

## 🗂️ Datasets

| Language | Dataset | Source |
|----------|---------|--------|
| English | `multispeak/hiring-accent-speech-human-voices` | [HuggingFace](https://huggingface.co/datasets/multispeak/hiring-accent-speech-human-voices) |
| Indonesian | `kambingbersayaphitam/speech-dataset-of-human-and-ai-generated-voices` | [Kaggle](https://www.kaggle.com/datasets/kambingbersayaphitam/speech-dataset-of-human-and-ai-generated-voices) |

---

## 🛠️ How to Use

1. **Open** `http://localhost:8501` after running `streamlit run app.py`
2. **Select** language in the sidebar (EN or ID)
3. **Choose** session mode: Practice / Random / Free
4. **Load** Vosk model (sidebar ▶ Load Vosk)
5. **Click** 🔴 Start Recording
6. **Speak** your answer
7. **Click** ⏹️ Stop & Analyze
8. **Review** WPM, pauses, keywords, fluency score, and coaching tips

---

## 📄 License

MIT License — free for personal and educational use.
