"""Minimal Vosk WebSocket backend for InterviewCoach English transcription.

Run after downloading and extracting an English Vosk model into ./model, or set
VOSK_MODEL_PATH to the model directory.
"""
import json
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000
MODEL_PATH = os.getenv("VOSK_MODEL_PATH", str(Path(__file__).parent / "model"))

app = FastAPI(title="InterviewCoach Vosk English ASR")
model = None

@app.on_event("startup")
def load_model():
    global model
    if not Path(MODEL_PATH).exists():
        raise RuntimeError(
            f"Vosk model directory not found: {MODEL_PATH}. Download an English Vosk model and set VOSK_MODEL_PATH."
        )
    model = Model(MODEL_PATH)

@app.get("/health")
def health():
    return {"ok": model is not None, "model_path": MODEL_PATH}

@app.websocket("/ws/en")
async def english_asr(websocket: WebSocket):
    await websocket.accept()
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)
    await websocket.send_text(json.dumps({"type": "ready", "language": "en-US"}))
    try:
        while True:
            message = await websocket.receive()
            if message.get("type") == "websocket.disconnect":
                break
            audio = message.get("bytes")
            text_frame = message.get("text")
            if text_frame:
                try:
                    control = json.loads(text_frame)
                except json.JSONDecodeError:
                    control = {}
                if control.get("type") == "flush":
                    final = json.loads(recognizer.FinalResult())
                    final_text = (final.get("text") or "").strip()
                    if final_text:
                        await websocket.send_text(json.dumps({"type": "final", "text": final_text}))
                    recognizer.Reset()
                continue
            if not audio:
                # Ignore non-binary/empty frames.
                continue
            if recognizer.AcceptWaveform(audio):
                result = json.loads(recognizer.Result())
                final_text = (result.get("text") or "").strip()
                if final_text:
                    await websocket.send_text(json.dumps({"type": "final", "text": final_text}))
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "").strip()
                if partial:
                    await websocket.send_text(json.dumps({"type": "partial", "text": partial}))
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        try:
            await websocket.send_text(json.dumps({"type": "error", "message": str(exc)}))
        except Exception:
            pass
    finally:
        try:
            final = json.loads(recognizer.FinalResult())
            text = (final.get("text") or "").strip()
            if text:
                await websocket.send_text(json.dumps({"type": "final", "text": text}))
        except Exception:
            pass
