#!/usr/bin/env python3
"""
BESTE MIX/MASTER FOR SAKEN

Mikser:
- dialog-stem
- SFX-stem
- full master WAV
- full master FLAC
- full master MP3 320k

Brukar ffmpeg loudnorm dersom ffmpeg finst:
- -16 LUFS integrert, eigna for tale/høyrespel
- -1.0 dB true peak
- 48 kHz
"""
from pathlib import Path
import json, re, shutil, subprocess
from pydub import AudioSegment, effects

BASE = Path(__file__).resolve().parent
SEGMENTS = json.loads((BASE / "saken_segments.json").read_text(encoding="utf-8"))
VOICES = BASE / "voices"
SFX = BASE / "sfx"
BUILD = BASE / "build"
STEMS = BASE / "stems"
BUILD.mkdir(exist_ok=True)
STEMS.mkdir(exist_ok=True)

def safe(s):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s)

def audio(path):
    return AudioSegment.from_file(path).set_frame_rate(48000).set_channels(2)

def sil(ms):
    return AudioSegment.silent(duration=ms, frame_rate=48000)

# Role balance.
role_gain = {
    "FORTELJAR": -1.2,
    "GLENN": 0.0,
    "KLUMPEN": -0.7,
    "KLUMPEN_LITANI": -1.0,
}
role_pause = {
    "FORTELJAR": 760,
    "GLENN": 440,
    "KLUMPEN": 560,
    "KLUMPEN_LITANI": 980,
}

# SFX er medvite lågt, så høyrespelet ikkje blir effekt-demo.
sfx_gain = {
    "room_tone": -28,
    "chair_hover": -27,
    "drypp": -8,
    "late_drypp": -8,
    "final_drypp": -10,
    "folder": -12,
    "stamp": -8,
    "postit_storm": -15,
    "chair_touch": -9,
    "knock": -8,
    "litany_drone": -23,
}

master = sil(0)
dialogue_stem = sil(0)
sfx_stem = sil(0)

def append(seg, kind, pause=0):
    global master, dialogue_stem, sfx_stem
    seg = seg.set_frame_rate(48000).set_channels(2)
    master += seg
    if kind == "dialogue":
        dialogue_stem += seg
        sfx_stem += sil(len(seg))
    else:
        sfx_stem += seg
        dialogue_stem += sil(len(seg))
    if pause:
        master += sil(pause)
        dialogue_stem += sil(pause)
        sfx_stem += sil(pause)

for seg in SEGMENTS:
    if seg["type"] == "sfx":
        cue = seg["cue"]
        path = SFX / f"{cue}.wav"
        if path.exists():
            a = audio(path).apply_gain(sfx_gain.get(cue, -12))
            append(a, "sfx", 270)
    else:
        role = seg["role"]
        path = VOICES / f'{seg["id"]}_{safe(role)}.wav'
        if not path.exists():
            raise FileNotFoundError(f"Manglar {path}. Køyr python make_tts_BEST.py først.")

        a = audio(path)
        # Dialog chain: lett kontroll, ikkje flat podkast.
        a = effects.normalize(a, headroom=2.0).apply_gain(role_gain.get(role, 0))
        a = effects.compress_dynamic_range(a, threshold=-18, ratio=2.15, attack=7, release=150)
        a = a.high_pass_filter(70).low_pass_filter(12500)
        append(a, "dialogue", role_pause.get(role, 520))

# Master chain før loudnorm.
master = master.fade_in(1000).fade_out(4000)
master = effects.compress_dynamic_range(master, threshold=-17, ratio=2.0, attack=10, release=190)
master = master.high_pass_filter(35).low_pass_filter(15000)
master = effects.normalize(master, headroom=1.2)

raw_wav = BUILD / "SAKEN_hoyrespel_MASTER_raw_48k.wav"
final_wav = BUILD / "SAKEN_hoyrespel_MASTER_BEST_48k.wav"
final_flac = BUILD / "SAKEN_hoyrespel_MASTER_BEST_48k.flac"
final_mp3 = BUILD / "SAKEN_hoyrespel_MASTER_BEST_320k.mp3"

master.export(raw_wav, format="wav")
dialogue_stem.export(STEMS / "SAKEN_dialogue_stem_48k.wav", format="wav")
sfx_stem.export(STEMS / "SAKEN_sfx_stem_48k.wav", format="wav")

if shutil.which("ffmpeg"):
    # Broadcast-ish loudness normalisering for tale/høyrespel.
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_wav),
        "-af", "loudnorm=I=-16:TP=-1.0:LRA=11,aresample=48000",
        str(final_wav)
    ], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(final_wav), str(final_flac)], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(final_wav), "-codec:a", "libmp3lame", "-b:a", "320k", str(final_mp3)], check=True)
else:
    # Fallback utan ffmpeg.
    master.export(final_wav, format="wav")
    master.export(final_mp3, format="mp3", bitrate="320k")

print("Ferdig BEST-master:")
print(final_wav)
print(final_flac)
print(final_mp3)
print(STEMS / "SAKEN_dialogue_stem_48k.wav")
print(STEMS / "SAKEN_sfx_stem_48k.wav")
