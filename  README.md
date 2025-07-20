# 🎮 Vertical Pong

**Vertical Pong** is a dynamic arcade game written in Python using the `pygame` library.

## 🕹️ Game Modes

- **2 Players** (local multiplayer)
- **Play vs Bot** (AI uses superpowers too)

## ⚡ Superpowers

| Player   | Key     | Ability                                 |
|----------|---------|------------------------------------------|
| Left     | `F`     | Boost ball speed (3 uses)               |
|          | `E`     | Freeze ball (3 uses)                    |
|          | `R`     | Unfreeze the ball                       |
|          | `D`     | Trigger sinusoidal ball motion (3 uses) |
| Right    | `I`     | Boost ball speed (3 uses)               |
|          | `L`     | Freeze ball (3 uses)                    |
|          | `K`     | Unfreeze the ball                       |
|          | `O`     | Trigger sinusoidal ball motion (3 uses) |

## 🧱 Features

- 🎵 Background music (`background_music.mp3`)
- 🖼️ Menu background image (`menu_background.jpg`)
- 🧊 Freeze mechanic and unfreeze recovery
- 🌀 Sinusoidal motion with increased speed
- ⚡ Speed boost for the ball
- 🧱 Central barrier appears every **35 seconds** for **15 seconds**
- ⏩ After 2 minutes, ball speed increases every **10 seconds by 10%**

## 💻 How to Run

1. Install dependencies:
pip install pygame

2. Place all required files in the same directory:

main.py
background_music.mp3
menu_background.jpg

3. Run the game:
4. 
python main.py