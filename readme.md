# Aquahack

## How to run

### 1. Clone the repository

### 2. Install dependencies
  - Python 3.8
  - Pipenv (used for dependency management, optional if you know what you're doing)
  - MPV (optional, for audio/music support)
  - Libraries used:
    - rich
    - python-mpv (optional, for audio/music support)

### 3. Run
If you're using Pipenv (recommended)
```sh
pipenv run main.py
```
Otherwise, if you've installed the libraries manually,
just run the `main.py` file from the command line; i.e.
```sh
python main.py
```

## Notes

### Terminal
This game is best enjoyed from a terminal with colour support.
If you are using Windows, the Windows Terminal app works well and has
a "retro" mode for more immersion.

### MPV
On Windows, you may need to obtain and place `mpv-1.dll` in the path
or in a folder `mpv` next to `main.py`.

### Music
Audio/music files are not included in this repository.
You can choose whatever music you would like and adjust timings accordingly.
For personal use, the songs Revolve (r mix) and Roller Mobster from the
Hacknet Soundtrack could be used for the main and tense music respectively.
However, the game should still work without MPV or audio files present.
