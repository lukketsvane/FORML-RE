#!/usr/bin/env python3
"""
BESTE TTS-KØYRING FOR SAKEN

Brukar OpenAI sitt nyaste og mest pålitelege TTS-oppsett i Speech API:
- model: gpt-4o-mini-tts
- response_format: wav
- voices: berre marin + cedar, som OpenAI tilrår for best kvalitet

Køyr:
  pip install -r requirements.txt
  export OPENAI_API_KEY="NY_SIKKER_NØKKEL_HER"
  python make_tts_BEST.py
"""
from pathlib import Path
import json, re, time
from openai import OpenAI

BASE = Path(__file__).resolve().parent
SEGMENTS = json.loads((BASE / "saken_segments.json").read_text(encoding="utf-8"))
PROFILES = json.loads((BASE / "voice_profiles.json").read_text(encoding="utf-8"))
OUT = BASE / "voices"
OUT.mkdir(exist_ok=True)

MODEL = "gpt-4o-mini-tts"
RESPONSE_FORMAT = "wav"

client = OpenAI()

def safe(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s)

for seg in SEGMENTS:
    if seg.get("type") != "voice":
        continue

    role = seg["role"]
    profile = PROFILES[role]
    out = OUT / f'{seg["id"]}_{safe(role)}.wav'

    if out.exists() and out.stat().st_size > 2048:
        print("skip", out.name)
        continue

    print(f"TTS BEST: {out.name} | {MODEL} | {profile['voice']}")
    with client.audio.speech.with_streaming_response.create(
        model=MODEL,
        voice=profile["voice"],
        input=seg["text"],
        instructions=profile["instructions"],
        response_format=RESPONSE_FORMAT,
    ) as response:
        response.stream_to_file(out)

    # Liten pause for å vere snill mot rate limits ved store manus.
    time.sleep(0.12)

print("Ferdig. Køyr: python mix_master_BEST.py")
