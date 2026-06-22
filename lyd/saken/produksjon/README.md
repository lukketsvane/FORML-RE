# SAKEN — høyrespelproduksjon (OpenAI TTS + pro miks/master)

Ferdig, køyrbar produksjonspakke for å lage høyrespelet **SAKEN** med OpenAI
TTS og deretter mikse/mastre det til eit ferdig høyrespel.

Manuset ligg i [`SAKEN_hoyrespel_script.txt`](SAKEN_hoyrespel_script.txt).
Tidslina (replikkar + lydeffektar) ligg i
[`saken_segments.json`](saken_segments.json), og røystregien i
[`voice_profiles.json`](voice_profiles.json).

## ⚠️ Tryggleik først

API-nøkkelen som vart limt inn i chatten **må roterast/slettast** i OpenAI
Platform før du brukar denne pakka. Lag ein ny prosjektnøkkel og hald han
berre lokalt som miljøvariabel — han skal **aldri** sjekkast inn i git.

## Status

Pipelinen er verifisert i dette miljøet: `ffmpeg` + `pydub` byggjer heile
tidslina (~11,6 min) og loudnorm-mastringa køyrer. Sjølve røyst-renderinga
er **ikkje** køyrd, fordi den oppgjevne OpenAI-nøkkelen autentiserer (HTTP
200) men manglar kvote (`429 insufficient_quota`). Legg til kreditt/billing
på ein ny nøkkel, så er pakka klar til å køyre rett ut av boksen.

## Beste oppsett

- Modell: `gpt-4o-mini-tts`
- Format frå TTS: `wav`
- Røyster: `cedar` (Forteljar/Klumpen/Litani) og `marin` (Glenn)
- Master: WAV 48 kHz + FLAC + MP3 320k
- Loudness: ffmpeg `loudnorm` til ca. −16 LUFS / −1,0 dBTP når ffmpeg finst

## Køyr

```bash
cd lyd/saken/produksjon
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# ffmpeg må vere installert (mac: brew install ffmpeg, debian/ubuntu: apt-get install ffmpeg)

export OPENAI_API_KEY="NY_SIKKER_NØKKEL_HER"
python make_tts.py        # renderar røyst-stems til voices/
python mix_master.py      # miksar + mastrar til build/
```

## Output

- `build/SAKEN_hoyrespel_MASTER_BEST_48k.wav`
- `build/SAKEN_hoyrespel_MASTER_BEST_48k.flac`
- `build/SAKEN_hoyrespel_MASTER_BEST_320k.mp3`
- `stems/SAKEN_dialogue_stem_48k.wav`
- `stems/SAKEN_sfx_stem_48k.wav`

## Regi

Sjå [`MIX_REGI_NOTAT.md`](MIX_REGI_NOTAT.md).

- **Forteljar** (`cedar`): eldgamal, 90–120 år, treig, knirkete, dramatisk, Voss/Bergen.
- **Glenn** (`marin`): rask, flat, tørr, byråkratisk embetsrøyst.
- **Klumpen** (`cedar`): mjuk, nysgjerrig, lys, litt svolten.
- **Litani** (`cedar`): rituell, hypnotisk, gravalvorleg.
- **Lydrom**: fuktig arkivkjellar, drypp kvart 17. sekund, svak svevande stol-tone.
