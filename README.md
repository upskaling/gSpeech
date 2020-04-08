# gSpeech

[![Build Status](https://travis-ci.org/mothsART/gSpeech.png?branch=master)](https://travis-ci.org/mothsART/gSpeech)

## Introduction

gSpeech: a simple GUI for SVox Pico TTS


## Installation instruction

Ubuntu:

Depends: python (>=2.7) python-gst1.0 (>=1.0) python-gtk2 (>=2.24) libttspico-utils (>= 1.0) python-notify (>=0.1) gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-pulseaudio

Suggests: sox


In any directory, where you want to install

1) Clone git repository

git clone https://github.com/lusum/gSpeech.git

2) Create .desktop launcher for gSpeech.sh

3) Use it


NB:
- sox is needed to speech text with more than 2^15 characters

## Tests

```
python3 -m unittest speech/tests/tests.py
```

```
./gSpeech-cli -i "mon chat s'appelle maurice" -o speech/tests/fr_FR/assets/chat_maurice.wav
```

