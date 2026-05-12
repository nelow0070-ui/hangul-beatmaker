PITCH_MAP = {
    "ㄱ": 0,
    "ㄲ": 1,
    "ㄴ": 2,
    "ㄷ": 3,
    "ㄸ": 4,
    "ㄹ": 5,
    "ㅁ": 6,
    "ㅂ": 7,
    "ㅃ": 8,
    "ㅅ": 9,
    "ㅆ": 10,
    "ㅈ": 11,
    "ㅉ": 12,
    "ㅊ": 13,
    "ㅋ": 14,
    "ㅌ": 15,
    "ㅍ": 16,
    "ㅎ": 17,
}

PITCH_MIN_SEMITONES = -6
PITCH_MAX_SEMITONES = 6
PITCH_MAX_STEP = max(PITCH_MAP.values())


def pitch_to_semitones(pitch: int) -> float:
    if PITCH_MAX_STEP == 0:
        return PITCH_MIN_SEMITONES

    pitch_range = PITCH_MAX_SEMITONES - PITCH_MIN_SEMITONES
    return PITCH_MIN_SEMITONES + (pitch / PITCH_MAX_STEP) * pitch_range


VOWEL_NORMALIZE = {
    "ㅑ": "ㅏ",
    "ㅐ": "ㅏ",
    "ㅒ": "ㅏ",
    "ㅕ": "ㅓ",
    "ㅔ": "ㅓ",
    "ㅖ": "ㅓ",
    "ㅛ": "ㅗ",
    "ㅘ": "ㅗ",
    "ㅙ": "ㅗ",
    "ㅚ": "ㅗ",
    "ㅠ": "ㅜ",
    "ㅝ": "ㅜ",
    "ㅞ": "ㅜ",
    "ㅟ": "ㅜ",
    "ㅢ": "ㅡ",
}

INSTRUMENT_MAP = {
    "ㅏ": "kick",
    "ㅓ": "clap",
    "ㅗ": "snare",
    "ㅜ": "open_hihat",
    "ㅡ": "clap",
    "ㅣ": "hihat",
}

SAMPLE_FILES = {
    "kick": "808_kick.wav",
    "snare": "snare.wav",
    "hihat": "hihat.wav",
    "open_hihat": "open_hihat.wav",
    "clap": "clap.wav",
}

SILENT_INITIAL = "ㅇ"
DEFAULT_VELOCITY = 1.0
SOUNDS_DIR = "sounds"

SAMPLE_RATE = 44100
