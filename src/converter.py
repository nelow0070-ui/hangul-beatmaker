from dataclasses import dataclass

from tokenizer import BeatToken, tokenize_text


@dataclass(frozen=True)
class BeatEvent:
    token: BeatToken
    step: int


@dataclass(frozen=True)
class BeatPattern:
    events: list[BeatEvent]


def text_to_pattern(text: str) -> BeatPattern:
    tokens = tokenize_text(text)
    events = [
        BeatEvent(token=token, step=index)
        for index, token in enumerate(tokens)
        if not token.is_rest
    ]
    return BeatPattern(events=events)


def text_to_events(text: str) -> list[BeatEvent]:
    return text_to_pattern(text).events
