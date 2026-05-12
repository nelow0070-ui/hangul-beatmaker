from pathlib import Path

import numpy as np
import pygame

from config import SAMPLE_FILES, SAMPLE_RATE, SOUNDS_DIR, pitch_to_semitones
from tokenizer import BeatToken


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PITCHED_INSTRUMENTS = set(SAMPLE_FILES)


class PygameSamplePlayer:
    def __init__(
        self,
        sounds_dir: str | Path = SOUNDS_DIR,
        sample_rate: int = SAMPLE_RATE,
    ) -> None:
        self.sample_rate = sample_rate
        self.sounds_dir = self._resolve_sounds_dir(sounds_dir)
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2, buffer=256)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
        self.samples = self._load_samples()
        self.pitched_samples: dict[tuple[str, int], pygame.mixer.Sound] = {}
        self.reported_missing_instruments: set[str] = set()

    def play_token(self, token: BeatToken) -> None:
        if token.is_rest or token.instrument is None:
            return

        sample = self._get_sample(token.instrument, token.pitch)
        if sample is None:
            self._report_missing_instrument(token.instrument)
            return

        channel = sample.play()
        if channel is not None:
            channel.set_volume(token.velocity)

    def _load_samples(self) -> dict[str, pygame.mixer.Sound]:
        samples = {}

        for instrument, filename in SAMPLE_FILES.items():
            path = self.sounds_dir / filename
            if not path.exists():
                print(f"샘플 파일 없음: {path} ({instrument} 재생에 필요)")
                continue

            samples[instrument] = pygame.mixer.Sound(str(path))

        return samples

    def _resolve_sounds_dir(self, sounds_dir: str | Path) -> Path:
        path = Path(sounds_dir)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def _get_sample(
        self,
        instrument: str,
        pitch: int | None,
    ) -> pygame.mixer.Sound | None:
        sample = self.samples.get(instrument)
        if (
            sample is None
            or pitch is None
            or pitch == 0
            or instrument not in PITCHED_INSTRUMENTS
        ):
            return sample

        semitones = pitch_to_semitones(pitch)
        cache_key = (instrument, semitones)
        if cache_key not in self.pitched_samples:
            self.pitched_samples[cache_key] = self._pitch_shift(sample, semitones)

        return self.pitched_samples[cache_key]

    def _report_missing_instrument(self, instrument: str) -> None:
        if instrument in self.reported_missing_instruments:
            return

        self.reported_missing_instruments.add(instrument)
        filename = SAMPLE_FILES.get(instrument)
        if filename is None:
            print(f"샘플 매핑 없음: {instrument}")
            return

        print(f"샘플 없음: {instrument} (필요 파일: {self.sounds_dir / filename})")

    def _pitch_shift(
        self,
        sample: pygame.mixer.Sound,
        semitones: int,
    ) -> pygame.mixer.Sound:
        ratio = 2 ** (semitones / 12)
        source = pygame.sndarray.array(sample)
        source_length = len(source)
        target_length = max(1, int(source_length / ratio))

        source_positions = np.arange(source_length)
        target_positions = np.linspace(0, source_length - 1, target_length)

        if source.ndim == 1:
            shifted = np.interp(target_positions, source_positions, source)
        else:
            channels = [
                np.interp(target_positions, source_positions, source[:, channel])
                for channel in range(source.shape[1])
            ]
            shifted = np.stack(channels, axis=1)

        return pygame.sndarray.make_sound(shifted.astype(source.dtype))


PygamePlayer = PygameSamplePlayer
