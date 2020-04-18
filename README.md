# gSpeech

[![Build Status](https://travis-ci.org/mothsART/gSpeech.png?branch=master)](https://travis-ci.org/mothsART/gSpeech)

## Introduction

gSpeech: a simple GUI for SVox Pico TTS


## Installation instruction

Ubuntu:

Depends: python (>=3.5) python-gst1.0 (>=1.0) python3-gi (>=2.24) libttspico-utils (>= 1.0) python-notify (>=0.1) gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-pulseaudio

Suggests: sox (is needed to speech text with more than 2^15 characters)

## CLI usage

```sh
./gspeech-cli -i "mon chat s'appelle maurice" -o speech/tests/fr_FR/assets/chat_maurice.wav
```

## Docker

```sh
git clone https://github.com/mothsART/gspeech.git
cd gspeech/docker
docker build .
docker run -i -t gspeech /bin/bash
```

## Tests

```sh
python3 -m unittest speech/tests/tests.py
```

## Create a Debian package

```sh
git clone https://github.com/mothsART/gspeech.git
cd gspeech
debuild -S // alias of dpkg-buildpackage -rfakeroot -d -us -uc -S
```

and launch with :

```sh
sudo dpkg -i ../gspeech*_all.deb
```
