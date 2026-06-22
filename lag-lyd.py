#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lag-lyd.py — lydbok/høyrespel frå tekst med Gemini TTS (nyaste modell).

Deler teksten i bitar, kallar TTS parallelt (med backoff på rate limit),
skøyter PCM-en saman til éi WAV-fil og ein MP3 per tekst. Køyr med
GEMINI_API_KEY i miljøet:  GEMINI_API_KEY=... python3 lag-lyd.py
"""
import os, re, time, wave, threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from google import genai
from google.genai import types

MODELL = os.environ.get("TTS_MODELL", "gemini-3.1-flash-tts-preview")
JOBS = int(os.environ.get("TTS_JOBS", "3"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
try:
    import lameenc
    HAR_MP3 = True
except Exception:
    HAR_MP3 = False


def del_tekst(t, maks=1000):
    """Del i bitar <= ~maks teikn, på avsnitts- og setningsgrenser."""
    bitar, bunke = [], ""
    for a in [x.strip() for x in re.split(r"\n\s*\n", t) if x.strip()]:
        if len(a) > maks:
            for s in re.split(r"(?<=[.!?…])\s+", a):
                if bunke and len(bunke) + len(s) > maks:
                    bitar.append(bunke); bunke = ""
                bunke = (bunke + " " + s).strip()
        else:
            if bunke and len(bunke) + len(a) > maks:
                bitar.append(bunke); bunke = ""
            bunke = (bunke + "\n\n" + a).strip()
    if bunke:
        bitar.append(bunke)
    return bitar


def tts(tekst, voice, stil):
    innhald = f"{stil}\n\n{tekst}"
    siste = None
    for forsok in range(8):
        try:
            r = client.models.generate_content(
                model=MODELL, contents=innhald,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)))))
            cand = (r.candidates or [None])[0]
            parts = getattr(getattr(cand, "content", None), "parts", None) or []
            for p in parts:
                inl = getattr(p, "inline_data", None)
                if inl and inl.data:
                    return inl.data
            siste = RuntimeError("tomt audiosvar")        # prøv på nytt
            time.sleep(min(30, 5 * (forsok + 1)))
            continue
        except Exception as e:
            siste = e
            msg = str(e)
            if any(x in msg for x in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE",
                                      "500", "INTERNAL", "RemoteProtocol")):
                m = re.search(r"(\d+(?:\.\d+)?)s", msg)
                time.sleep(min(60, float(m.group(1)) + 1) if m else min(60, 8 * (forsok + 1)))
                continue
            raise
    raise siste


def lag(namn, voice, stil):
    tekst = (Path("lyd") / namn / "tekst.txt").read_text(encoding="utf-8")
    bitar = del_tekst(tekst)
    print(f"[{namn}] {len(bitar)} bitar · modell {MODELL} · voice {voice}", flush=True)
    pcm = [None] * len(bitar)
    feil = []
    lock = threading.Lock()

    def one(i):
        try:
            pcm[i] = tts(bitar[i], voice, stil)
            print(f"  [{namn}] {i + 1}/{len(bitar)} ok ({len(pcm[i]) // 1024} KB)", flush=True)
        except Exception as e:
            with lock:
                feil.append(i)
            print(f"  [{namn}] {i + 1} FEILA: {type(e).__name__}: {str(e)[:120]}", flush=True)

    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        list(ex.map(one, range(len(bitar))))

    data = b"".join(p for p in pcm if p)
    ut = Path("lyd") / namn
    wavp = ut / f"{namn}.wav"
    with wave.open(str(wavp), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(data)
    sek = len(data) / 2 / 24000
    print(f"[{namn}] WAV {wavp}  {wavp.stat().st_size // 1024} KB  ~{sek / 60:.1f} min", flush=True)
    if HAR_MP3 and data:
        enc = lameenc.Encoder()
        enc.set_bit_rate(128); enc.set_in_sample_rate(24000); enc.set_channels(1); enc.set_quality(2)
        mp3 = enc.encode(data) + enc.flush()
        mp3p = ut / f"{namn}.mp3"
        mp3p.write_bytes(mp3)
        print(f"[{namn}] MP3 {mp3p}  {mp3p.stat().st_size // 1024} KB", flush=True)
    if feil:
        print(f"[{namn}] ÅTVARING: {len(feil)} bitar feila: {sorted(i + 1 for i in feil)}", flush=True)


NARRATOR = ("Les den følgjande teksten som ei vakker, roleg lydbok — varm og ettertenksam "
            "forteljarstemme, god tid, naturlege pausar. Les berre sjølve teksten, ikkje denne instruksen:")
HOYRESPEL = ("Framfør den følgjande teksten som eit innleva høyrespel — roleg, nøktern forteljar "
             "for skildringane, og levande replikkar: Klumpen lett, liten og litt fortvila, Glenn "
             "tørr, roleg og byråkratisk. Les berre sjølve teksten, ikkje denne instruksen:")
MORK = ("Les den følgjande teksten langsamt og alvorleg, som eit mørkt prosadikt — låg, dempa, "
        "intens forteljarstemme med lange pausar. Les berre sjølve teksten, ikkje denne instruksen:")

KOMITE = ("Framfør den følgjande teksten som eit satirisk høyrespel — eit komitémøte som har "
          "vart i hundre år. Tørr, roleg forteljar for skildringane; Lederen pompøs og "
          "byråkratisk; forslagsstillarane ivrige og litt patetiske; gjer stemmene tydeleg "
          "ulike og timinga komisk. Les berre sjølve teksten, ikkje denne instruksen:")

TEKSTAR = {
    "gravgaaver": ("Charon", NARRATOR),
    "saken": ("Puck", HOYRESPEL),
    "oneida": ("Charon", MORK),
    "grunnlaget": ("Puck", KOMITE),
}

if __name__ == "__main__":
    import sys
    valde = [a for a in sys.argv[1:] if a in TEKSTAR] or list(TEKSTAR)
    for namn in valde:
        voice, stil = TEKSTAR[namn]
        lag(namn, voice, stil)
    print("FERDIG")
