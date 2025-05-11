# Flip-a-Pair

A fast-paced, offline memory-matching game written in **Python 3** using **Tkinter** and **Pillow**.  
Flip two cards at a time, match pairs, and beat the clock — all in a single 60-second run.

## Gameplay

- Match 2 identical cards to score **+10 points**
- Game starts with 4 cards and adds +2 each level (max: 20 cards)
- Timer counts down from 60 seconds
- Local leaderboard saves the **top 3 scores** in `high_scores.json`
- Fully mouse-driven and fullscreen by default

## Download Standalone Installer for Windows

If you don’t want to install Python, just download and run:

[Flip a Pair Standalone Installer.exe](https://github.com/nshengelaia/flip-a-pair/raw/main/releases/Flip-a-Pair-Standalone-Installer.exe)

No setup required. Works on Windows 10/11.

## Requirements to run the code yourself

- Python 3.10 or later  
- [Pillow](https://pypi.org/project/Pillow/) — automatically installed below

## Assets

All graphics (card faces, card back, background, play button, title) are included in the `assets/` folder.

## Running the Game

1. Clone the repo or download the ZIP  
2. In your terminal:

```bash
cd flip-a-pair
python -m venv .venv
.venv\Scripts\activate    
python -m pip install "Pillow==11.2.1"
python main.py
```




