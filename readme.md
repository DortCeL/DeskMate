# DeskMate

A lightweight, always-on-top animated desktop companion for Windows.

## The famous **CHIKA FUJIWARA** lives on your very own desktop :)

> **Note:** The demonstration GIF below may take a moment to load.
> ![demo](demo.gif)

## Overview

DeskMate renders a borderless, transparent window pinned to the bottom-right corner of the screen (just above the taskbar) and plays an animated character `CHIKA FUJIWARA` on loop.

It's built as a native-feeling desktop widget rather than a browser or Electron app. no browser window, no border, no taskbar entry. It just makes the character floating on top of everything else. Can be exited from a proper system tray icon. It only takes up _33.8_ Megabytes of your memory!

## Features

- **Transparent window compositing** — no visible window frame or background, achieved via Windows color-keying and alpha-blended edge handling to avoid visual artifacts around the character
- **Animated rendering** — plays multi-frame GIF animation using each frame's native timing
- **System tray integration** — runs without a visible window, with a right-click tray menu for clean shutdown
- **Packaged as a standalone executable** — no Python installation required for end users

## Tech Stack

- **Python 3**
- **Tkinter** — window management and rendering
- **Pillow (PIL)** — image/GIF processing and frame compositing
- **pystray** — system tray icon and menu
- **PyInstaller** — packaging into a standalone `.exe`

## Installation

### Run from source

```bash
git clone https://github.com/DortCeL/deskmate.git
cd deskmate
pip install -r requirements.txt
python main.py
```

Place your own animated character file replacing `chika.gif` in the project root to have your very own companion cheering you up!

### Run the packaged executable

Download the `.exe` from [Releases](#) and run it directly. No installation required. Exit via the tray icon (bottom-right of your taskbar, near the clock).

## Building the executable yourself

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=chika_icon.ico --add-data "chika.gif;." main.py
```

The output executable will be in the generated `dist/` folder.

## How it works

A short technical breakdown of the interesting parts:

- **Transparency**: the window background is set to a solid color (black) and marked as transparent via `-transparentcolor`, which is done specifically for Windows, so any pixel of that exact color becomes a visual hole. Since Windows keys out _exact_ color matches only, anti-aliased/semi-transparent edges in the source image are pre-composited onto the same black color before being displayed, so they blend cleanly into the transparent background instead of leaving a visible fringe.
- **Threading model**: `pystray`'s tray icon runs its own blocking event loops on background threads, since it cannot share Tkinter's main thread. Callbacks from this thread only ever updates plain state or is routed back to the main thread via `root.after(...)`, since Tkinter itself is not thread-safe.
- **Animation**: GIF frames are decoded once at startup via `PIL.ImageSequence.Iterator`, each resized and pre-composited, then cycled using each frame's own duration metadata so playback speed matches the source file rather than a fixed frame rate.
