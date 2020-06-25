# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased : 1.0]

### Added
- GTK unit tests

## [0.10]

### Bugfix

- better sox integration : trigger when text to reach is too long.
- setup.py whith new dict tree
- edit speed on tray change speed on multimedia popup and vice versa
- edit lang on tray change lang on multimedia popup and vice versa

### Added

- speed management : voice speech integration on cli, tray and multimedia menu
- integrate sox into nix
- screenshots

## [0.9.2]

### Bugfix

- create all directories on a pid new path

## [0.9.1]

### Bugfix

- test permissions before write a conf file

## [0.9]

### Bugfix

- french text : 'fan'
- correction on about dialog
- give a parent on all dialogs (gtk warning)

### Added

- option dialog : can enable/disable notification popup
- create a changelog file
- create a Debian package
- create a ppa : https://launchpad.net/~jerem-ferry/+archive/ubuntu/tts
- create a nix build
- flake8 (and travisCI integration)
