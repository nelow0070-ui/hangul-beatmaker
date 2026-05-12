# Hangul 808 Beatmaker

Hangul syllables trigger 808-style WAV samples in real time.

- Initial consonant: pitch value stored on the token
- Vowel: sample instrument selection
- Final consonant: parsed but ignored for now
- Playback: `pygame.mixer`

Expected sample files:

```text
sounds/
  808_kick.wav
  snare.wav
  hihat.wav
  clap.wav
  open_hihat.wav
```

Vowel mapping:

```text
ㅏ -> sounds/808_kick.wav
ㅓ -> sounds/clap.wav
ㅗ -> sounds/snare.wav
ㅜ -> sounds/open_hihat.wav
ㅣ -> sounds/hihat.wav
```

WAV samples are local assets and are ignored by git via `sounds/*.wav`.

Run:

```bash
python src/main.py
```

Web UI:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/web/
```

Each input line starts with two Hangul syllables:

- First syllable: time signature
- Second syllable: BPM
- Remaining syllables: beat text

For example, `러휴가나다라` means:

- `러`: `ㄹ(4)` + `ㅓ(4)` -> 4/4 time
- `휴`: `ㅎ(14)` + `ㅠ(10)` + no final `(0)` -> `(14 + 10 + 0) * 5 = 120 BPM`
- `가나다라`: played as measure 1, beats 1-4

```text
입력: 러휴가나다라
```

After that, each Hangul syllable is played one beat apart at the selected BPM.
