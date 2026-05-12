const INITIALS = [
  "ㄱ",
  "ㄲ",
  "ㄴ",
  "ㄷ",
  "ㄸ",
  "ㄹ",
  "ㅁ",
  "ㅂ",
  "ㅃ",
  "ㅅ",
  "ㅆ",
  "ㅇ",
  "ㅈ",
  "ㅉ",
  "ㅊ",
  "ㅋ",
  "ㅌ",
  "ㅍ",
  "ㅎ",
];

const VOWELS = [
  "ㅏ",
  "ㅐ",
  "ㅑ",
  "ㅒ",
  "ㅓ",
  "ㅔ",
  "ㅕ",
  "ㅖ",
  "ㅗ",
  "ㅘ",
  "ㅙ",
  "ㅚ",
  "ㅛ",
  "ㅜ",
  "ㅝ",
  "ㅞ",
  "ㅟ",
  "ㅠ",
  "ㅡ",
  "ㅢ",
  "ㅣ",
];

const FINALS = [
  "",
  "ㄱ",
  "ㄲ",
  "ㄳ",
  "ㄴ",
  "ㄵ",
  "ㄶ",
  "ㄷ",
  "ㄹ",
  "ㄺ",
  "ㄻ",
  "ㄼ",
  "ㄽ",
  "ㄾ",
  "ㄿ",
  "ㅀ",
  "ㅁ",
  "ㅂ",
  "ㅄ",
  "ㅅ",
  "ㅆ",
  "ㅇ",
  "ㅈ",
  "ㅊ",
  "ㅋ",
  "ㅌ",
  "ㅍ",
  "ㅎ",
];

const JAMO_NUMBER_MAP = {
  ㄱ: 1,
  ㄴ: 2,
  ㄷ: 3,
  ㄹ: 4,
  ㅁ: 5,
  ㅂ: 6,
  ㅅ: 7,
  ㅇ: 8,
  ㅈ: 9,
  ㅊ: 10,
  ㅋ: 11,
  ㅌ: 12,
  ㅍ: 13,
  ㅎ: 14,
  ㅏ: 1,
  ㅑ: 2,
  ㅐ: 3,
  ㅓ: 4,
  ㅕ: 5,
  ㅔ: 6,
  ㅗ: 7,
  ㅛ: 8,
  ㅜ: 9,
  ㅠ: 10,
  ㅡ: 11,
  ㅣ: 12,
  "": 0,
};

const PITCH_MAP = {
  ㄱ: 0,
  ㄲ: 1,
  ㄴ: 2,
  ㄷ: 3,
  ㄸ: 4,
  ㄹ: 5,
  ㅁ: 6,
  ㅂ: 7,
  ㅃ: 8,
  ㅅ: 9,
  ㅆ: 10,
  ㅈ: 11,
  ㅉ: 12,
  ㅊ: 13,
  ㅋ: 14,
  ㅌ: 15,
  ㅍ: 16,
  ㅎ: 17,
};

const VOWEL_NORMALIZE = {
  ㅑ: "ㅏ",
  ㅐ: "ㅏ",
  ㅒ: "ㅏ",
  ㅕ: "ㅓ",
  ㅔ: "ㅓ",
  ㅖ: "ㅓ",
  ㅛ: "ㅗ",
  ㅘ: "ㅗ",
  ㅙ: "ㅗ",
  ㅚ: "ㅗ",
  ㅠ: "ㅜ",
  ㅝ: "ㅜ",
  ㅞ: "ㅜ",
  ㅟ: "ㅜ",
  ㅢ: "ㅡ",
};

const INSTRUMENT_MAP = {
  ㅏ: "kick",
  ㅓ: "clap",
  ㅗ: "snare",
  ㅜ: "open_hihat",
  ㅡ: "clap",
  ㅣ: "hihat",
};

const SAMPLE_FILES = {
  kick: "../sounds/808_kick.wav",
  snare: "../sounds/snare.wav",
  hihat: "../sounds/hihat.wav",
  open_hihat: "../sounds/open_hihat.wav",
  clap: "../sounds/clap.wav",
};

const HANGUL_START = "가".codePointAt(0);
const HANGUL_END = "힣".codePointAt(0);
const SILENT_INITIAL = "ㅇ";
const PITCH_MIN_SEMITONES = -6;
const PITCH_MAX_SEMITONES = 6;
const PITCH_MAX_STEP = 17;

const playButton = document.querySelector("#playButton");
const stopButton = document.querySelector("#stopButton");
const statusElement = document.querySelector("#status");
const trackInputs = [...document.querySelectorAll(".track-input")];

let audioContext;
let sampleBuffers = {};
let activeSources = [];

playButton.addEventListener("click", playTracks);
stopButton.addEventListener("click", stopTracks);
trackInputs.forEach((input) => input.addEventListener("input", renderStatus));
renderStatus();

async function playTracks() {
  stopTracks();

  audioContext = audioContext || new AudioContext();
  await audioContext.resume();
  sampleBuffers = await loadSamples(audioContext);

  const parsedTracks = getParsedTracks();
  renderStatus(parsedTracks);

  const playableTracks = parsedTracks.filter((track) => track.ok);
  if (playableTracks.length === 0) {
    return;
  }

  const startAt = audioContext.currentTime + 0.08;
  for (const track of playableTracks) {
    scheduleTrack(track, startAt);
  }
}

function stopTracks() {
  for (const source of activeSources) {
    try {
      source.stop();
    } catch {
      // Already stopped.
    }
  }
  activeSources = [];
}

async function loadSamples(context) {
  const entries = await Promise.all(
    Object.entries(SAMPLE_FILES).map(async ([instrument, path]) => {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`${path} 샘플을 불러오지 못했습니다.`);
      }
      const data = await response.arrayBuffer();
      return [instrument, await context.decodeAudioData(data)];
    }),
  );

  return Object.fromEntries(entries);
}

function scheduleTrack(track, startAt) {
  const secondsPerBeat = 60 / track.settings.bpm;

  track.tokens.forEach((token, index) => {
    if (token.isRest || !token.instrument) {
      return;
    }

    const buffer = sampleBuffers[token.instrument];
    if (!buffer) {
      return;
    }

    const source = audioContext.createBufferSource();
    const gain = audioContext.createGain();
    source.buffer = buffer;
    source.playbackRate.value = 2 ** (token.semitones / 12);
    gain.gain.value = 1;

    source.connect(gain);
    gain.connect(audioContext.destination);
    source.start(startAt + index * secondsPerBeat);
    source.addEventListener("ended", () => {
      activeSources = activeSources.filter((item) => item !== source);
    });
    activeSources.push(source);
  });
}

function getParsedTracks() {
  return trackInputs.map((input, index) => {
    const parsed = parseInputLine(input.value);
    if (!parsed) {
      return {
        ok: false,
        label: `Track ${index + 1}`,
        message: "첫 음절 박자표, 두 번째 음절 BPM, 세 번째부터 비트가 필요합니다.",
      };
    }

    return {
      ok: true,
      label: `Track ${index + 1}`,
      ...parsed,
    };
  });
}

function renderStatus(tracks = getParsedTracks()) {
  statusElement.innerHTML = "";

  for (const track of tracks) {
    const line = document.createElement("div");
    line.className = "status-line";

    const label = document.createElement("strong");
    label.textContent = track.label;

    const body = document.createElement("div");
    if (!track.ok) {
      body.className = "error";
      body.textContent = track.message;
    } else {
      const events = track.tokens
        .map((token, index) => {
          const measure = Math.floor(index / track.settings.beatsPerMeasure) + 1;
          const beat = (index % track.settings.beatsPerMeasure) + 1;
          const instrument = token.isRest ? "쉼" : token.instrument;
          return `${token.raw}:${measure}마디 ${beat}박 ${instrument}`;
        })
        .join(" / ");

      body.textContent = `${track.settings.beatUnit}분의 ${track.settings.beatsPerMeasure}박자, ${track.settings.bpm} BPM - ${events}`;
      if (events.length === 0) {
        body.className = "muted";
        body.textContent = "재생 가능한 한글 비트가 없습니다.";
      }
    }

    line.append(label, body);
    statusElement.append(line);
  }
}

function parseInputLine(line) {
  const compact = [...line.replace(/\s/g, "")];
  if (compact.length < 3) {
    return null;
  }

  const meter = parseMeterSyllable(compact[0]);
  const bpm = parseBpmSyllable(compact[1]);
  if (!meter || !bpm) {
    return null;
  }

  return {
    settings: {
      beatsPerMeasure: meter.beatsPerMeasure,
      beatUnit: meter.beatUnit,
      bpm,
    },
    tokens: tokenizeText(compact.slice(2).join("")),
  };
}

function parseMeterSyllable(char) {
  const parts = splitSyllable(char);
  if (!parts) {
    return null;
  }

  const beatsPerMeasure = JAMO_NUMBER_MAP[parts.initial];
  const beatUnit = JAMO_NUMBER_MAP[parts.vowel];
  if (!beatsPerMeasure || !beatUnit) {
    return null;
  }

  return { beatsPerMeasure, beatUnit };
}

function parseBpmSyllable(char) {
  const parts = splitSyllable(char);
  if (!parts) {
    return null;
  }

  const initial = JAMO_NUMBER_MAP[parts.initial];
  const vowel = JAMO_NUMBER_MAP[parts.vowel];
  const final = JAMO_NUMBER_MAP[parts.final];
  if (initial === undefined || vowel === undefined || final === undefined) {
    return null;
  }

  const bpm = (initial + vowel + final) * 5;
  return bpm > 0 ? bpm : null;
}

function tokenizeText(text) {
  return [...text].map(tokenizeChar).filter(Boolean);
}

function tokenizeChar(char) {
  const parts = splitSyllable(char);
  if (!parts) {
    return null;
  }

  const normalizedVowel = VOWEL_NORMALIZE[parts.vowel] || parts.vowel;
  const instrument = INSTRUMENT_MAP[normalizedVowel];
  const isRest = parts.initial === SILENT_INITIAL || !instrument;
  const pitch = isRest ? null : PITCH_MAP[parts.initial];

  return {
    raw: parts.syllable,
    initial: parts.initial,
    vowel: parts.vowel,
    normalizedVowel,
    final: parts.final,
    instrument: isRest ? null : instrument,
    pitch,
    semitones: pitch === null ? 0 : pitchToSemitones(pitch),
    isRest,
  };
}

function splitSyllable(char) {
  const code = char.codePointAt(0);
  if (code < HANGUL_START || code > HANGUL_END) {
    return null;
  }

  const index = code - HANGUL_START;
  const initialIndex = Math.floor(index / 588);
  const vowelIndex = Math.floor((index % 588) / 28);
  const finalIndex = index % 28;

  return {
    syllable: char,
    initial: INITIALS[initialIndex],
    vowel: VOWELS[vowelIndex],
    final: FINALS[finalIndex],
  };
}

function pitchToSemitones(pitch) {
  const pitchRange = PITCH_MAX_SEMITONES - PITCH_MIN_SEMITONES;
  return PITCH_MIN_SEMITONES + (pitch / PITCH_MAX_STEP) * pitchRange;
}
