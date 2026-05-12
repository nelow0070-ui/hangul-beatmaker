from dataclasses import dataclass

from config import (
    DEFAULT_VELOCITY,
    INSTRUMENT_MAP,
    PITCH_MAP,
    SILENT_INITIAL,
    VOWEL_NORMALIZE,
)
from hangul import split_syllable


@dataclass(frozen=True)
class BeatToken:
    raw: str
    initial: str
    vowel: str
    normalized_vowel: str
    final: str
    instrument: str | None
    pitch: int | None
    velocity: float
    is_rest: bool


def tokenize_text(text: str) -> list[BeatToken]:
    tokens = []

    for char in text:
        token = tokenize_char(char)
        if token is not None:
            tokens.append(token)

    return tokens


def tokenize_char(char: str) -> BeatToken | None:
    parts = split_syllable(char)
    if parts is None:
        return None

    normalized_vowel = VOWEL_NORMALIZE.get(parts.vowel, parts.vowel)
    instrument = INSTRUMENT_MAP.get(normalized_vowel)
    is_rest = parts.initial == SILENT_INITIAL or instrument is None

    return BeatToken(
        raw=parts.syllable,
        initial=parts.initial,
        vowel=parts.vowel,
        normalized_vowel=normalized_vowel,
        final=parts.final,
        instrument=None if is_rest else instrument,
        pitch=None if is_rest else PITCH_MAP.get(parts.initial),
        velocity=DEFAULT_VELOCITY,
        is_rest=is_rest,
    )
