# Hangul 808 Beatmaker Design

## Goal

Turn Hangul input into real-time 808 sample playback.

- Initial consonant: pitch value
- Vowel: 808 sample type
- Initial consonant `ㅇ`: rest
- Final consonant: parsed but not used yet
- Future feature: MIDI export from tokenized beat events

## Current Structure

```text
src/
  main.py       # Program entry point
  config.py     # Pitch, vowel, and sample mappings
  hangul.py     # Hangul syllable splitting
  tokenizer.py  # Hangul text to BeatToken conversion
  converter.py  # BeatToken to future pattern/event data
  playback.py   # pygame sample playback
sounds/
  808_kick.wav
  808_bass.wav
  snare.wav
  hihat.wav
  clap.wav
docs/
  design.md     # Project design notes
```

## Mapping Rules

### Tokenization

Each Hangul syllable becomes one `BeatToken`.

- `raw`: original syllable
- `initial`: initial consonant
- `vowel`: original vowel
- `normalized_vowel`: reduced vowel set
- `final`: final consonant, currently ignored
- `instrument`: sample key
- `pitch`: pitch offset value

### Initial Consonants to Pitch

Each supported initial consonant maps to a pitch offset.
The first sample-based version stores this value on the token but plays the raw WAV sample.
Pitch-shifted playback can be added later behind the playback backend.

The initial consonant `ㅇ` creates a rest.

### Vowels to 808 Samples

Only a small vowel set is used directly.
Other vowels are normalized into this set when possible.

- ㅏ -> kick -> `sounds/808_kick.wav`
- ㅓ -> bass -> `sounds/808_bass.wav`
- ㅗ -> snare -> `sounds/snare.wav`
- ㅜ -> hihat -> `sounds/hihat.wav`
- ㅡ -> clap -> `sounds/clap.wav`
- ㅣ -> clap -> `sounds/clap.wav`

## Playback Choice

The first sample-based version uses `pygame.mixer`.
Samples are loaded once at startup and triggered immediately with `Sound.play()`.

## Next Steps

1. Add sample WAV files under `sounds/`.
2. Add tests for tokenization.
3. Add pitch-shifted sample playback if needed.
4. Add a `pretty_midi` exporter from `BeatPattern`.
