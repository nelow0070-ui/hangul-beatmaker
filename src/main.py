from dataclasses import dataclass
import time

from config import pitch_to_semitones
from hangul import split_syllable
from playback import PygameSamplePlayer
from tokenizer import tokenize_text


JAMO_NUMBER_MAP = {
    "ㄱ": 1,
    "ㄴ": 2,
    "ㄷ": 3,
    "ㄹ": 4,
    "ㅁ": 5,
    "ㅂ": 6,
    "ㅅ": 7,
    "ㅇ": 8,
    "ㅈ": 9,
    "ㅊ": 10,
    "ㅋ": 11,
    "ㅌ": 12,
    "ㅍ": 13,
    "ㅎ": 14,
    "ㅏ": 1,
    "ㅑ": 2,
    "ㅐ": 3,
    "ㅓ": 4,
    "ㅕ": 5,
    "ㅔ": 6,
    "ㅗ": 7,
    "ㅛ": 8,
    "ㅜ": 9,
    "ㅠ": 10,
    "ㅡ": 11,
    "ㅣ": 12,
    "": 0,
}


@dataclass(frozen=True)
class PlaybackSettings:
    beats_per_measure: int
    beat_unit: int
    bpm: float

    @property
    def seconds_per_beat(self) -> float:
        return 60 / self.bpm


def main() -> None:
    print("한글 808 비트메이커 시작")
    print("초성은 pitch, 중성은 808 샘플을 고릅니다. 받침은 현재 무시합니다.")
    print("입력 형식: 첫 음절은 박자표, 두 번째 음절은 BPM, 나머지는 한글 비트")
    print("예: 러휴가나다라")
    print("종료하려면 빈 줄을 입력하세요.")

    player = PygameSamplePlayer()

    while True:
        line = input("입력: ").strip()
        if not line:
            return

        parsed_input = parse_input_line(line)
        if parsed_input is None:
            print("입력은 한글 음절로 박자표, BPM, 비트를 작성하세요. 예: 러휴가나다라")
            continue

        settings, text = parsed_input
        print(
            f"{settings.beat_unit}분의 {settings.beats_per_measure}박자, "
            f"{settings.bpm:g} BPM으로 재생합니다."
        )

        tokens = tokenize_text(text)
        if not tokens:
            print("음악으로 변환할 수 있는 한글 음절이 없습니다.")
            continue

        for index, token in enumerate(tokens):
            measure = (index // settings.beats_per_measure) + 1
            beat = (index % settings.beats_per_measure) + 1
            if token.is_rest:
                print(f"{token.raw}: {measure}마디 {beat}박, 재생 안 함")
            else:
                semitones = None if token.pitch is None else pitch_to_semitones(token.pitch)
                print(
                    f"{token.raw}: {measure}마디 {beat}박, "
                    f"{token.initial} -> pitch {token.pitch} ({semitones:.1f}반음), "
                    f"{token.vowel}/{token.normalized_vowel} -> {token.instrument}"
                )

            player.play_token(token)
            if index < len(tokens) - 1:
                time.sleep(settings.seconds_per_beat)


def parse_input_line(line: str) -> tuple[PlaybackSettings, str] | None:
    compact = "".join(line.split())
    if len(compact) < 3:
        return None

    parsed_time_signature = parse_meter_syllable(compact[0])
    parsed_bpm = parse_bpm_syllable(compact[1])
    if parsed_time_signature is None or parsed_bpm is None:
        return None

    beats_per_measure, beat_unit = parsed_time_signature
    return (
        PlaybackSettings(
            beats_per_measure=beats_per_measure,
            beat_unit=beat_unit,
            bpm=parsed_bpm,
        ),
        compact[2:],
    )


def parse_meter_syllable(value: str) -> tuple[int, int] | None:
    parts = split_syllable(value)
    if parts is None:
        return None

    beats_per_measure = JAMO_NUMBER_MAP.get(parts.initial)
    beat_unit = JAMO_NUMBER_MAP.get(parts.vowel)
    if beats_per_measure is None or beat_unit is None:
        return None

    return validate_time_signature(beats_per_measure, beat_unit)


def parse_bpm_syllable(value: str) -> float | None:
    parts = split_syllable(value)
    if parts is None:
        return None

    numbers = [
        JAMO_NUMBER_MAP.get(parts.initial),
        JAMO_NUMBER_MAP.get(parts.vowel),
        JAMO_NUMBER_MAP.get(parts.final),
    ]
    if any(number is None for number in numbers):
        return None

    bpm = sum(numbers) * 5
    if bpm <= 0:
        return None

    return float(bpm)


def validate_time_signature(
    beats_per_measure: int,
    beat_unit: int,
) -> tuple[int, int] | None:
    if beats_per_measure <= 0 or beat_unit <= 0:
        return None
    return beats_per_measure, beat_unit


if __name__ == "__main__":
    main()
