<p align="center">
  <img src="assets/icon.png" width="112" alt="Mental Math Trainer abacus mark">
</p>

<h1 align="center">Mental Math Trainer</h1>

<p align="center">A thoughtful, lightweight desktop trainer for mental arithmetic.</p>

<p align="center">
  <a href="https://github.com/psyhocow/mental-math-trainer/releases/latest">Download the latest release</a>
  &nbsp;·&nbsp; English, Russian, and Kazakh
  &nbsp;·&nbsp; Windows, macOS, and Linux
</p>

## About

This project remasters a mental arithmetic trainer created for my IT Step Academy graduate work. It keeps the original practice idea and adds a more complete learning flow, persistent settings, and desktop builds for the major operating systems.

## Features

- **Three practice levels:** Easy and Normal have a visible countdown; Hard gives you untimed focus with larger calculations.
- **A guided beginner lesson:** six simple questions introduce counting on, making ten, subtraction through ten, multiplication, and division.
- **FSU formula practice:** quick rounds on the square of a sum, square of a difference, and difference of squares.
- **Two helpful guides:** an FSU walkthrough and practical mental arithmetic strategies for all four operations.
- **Personal settings:** choose English, Russian, or Kazakh, enable desktop mistake feedback, toggle FSU hints, and switch the original background music on or off.
- **Private local records:** scores and preferences stay in your operating system's user data folder.
- **Cross-platform desktop builds:** release archives are built for Windows x86_64, macOS Intel, macOS Apple Silicon, and Linux x86_64.

## Get the app

Download the archive for your system from [Releases](https://github.com/psyhocow/mental-math-trainer/releases/latest).

| Platform | Archive | Start the app |
| --- | --- | --- |
| Windows x86_64 | `MentalMathTrainer-windows-x86_64.zip` | Extract and open `MentalMathTrainer.exe` |
| macOS Apple Silicon | `MentalMathTrainer-macos-apple-silicon.zip` | Extract, then open `MentalMathTrainer.app` |
| macOS Intel | `MentalMathTrainer-macos-intel.zip` | Extract, then open `MentalMathTrainer.app` |
| Linux x86_64 / Kali | `MentalMathTrainer-linux-x86_64.zip` | Extract and run `./MentalMathTrainer/MentalMathTrainer` |

The macOS builds are unsigned. On first launch, choose **Open** from the app's Finder context menu if macOS asks for confirmation.

## Run from source

Python 3.11 and Tkinter are required. Background music uses pygame; the trainer still starts if audio is unavailable.

```bash
python -m pip install -r requirements.txt
python run.py
```

On Debian-based Linux systems, install the Tkinter package for your Python version if it is not already present (usually `python3-tk`).

## Build locally

```bash
python -m pip install -r requirements-build.txt
python scripts/make_assets.py
python -m PyInstaller --clean --noconfirm app.spec
```

PyInstaller builds need to run on the same operating system and CPU architecture as the intended download. The GitHub Actions release workflow builds each target on a matching runner and attaches the archives when a `v*` tag is pushed.

## Data and privacy

The app does not connect to a service. Settings and records are stored in the standard per-user application data directory:

- Windows: `%APPDATA%/MentalMathTrainer`
- macOS: `~/Library/Application Support/MentalMathTrainer`
- Linux: `$XDG_DATA_HOME/MentalMathTrainer`, or `~/.local/share/MentalMathTrainer`

## Project status

The desktop trainer is maintained as a personal project. No third-party fonts, images, or music are bundled. The ambient loop and app icon are generated from the included project script.
