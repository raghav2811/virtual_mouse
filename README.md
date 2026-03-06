# Hand Mouse — AI Virtual Mouse via Hand Gestures

Control your system mouse using only your hand and a webcam. Powered by **MediaPipe**, **OpenCV**, and **PyAutoGUI**, the project detects hand landmarks in real time to move the cursor, click, scroll, and drag — no physical mouse required.

---

## Features

| Gesture | Action |
|---|---|
| Index finger up (only) | Move cursor |
| Index finger curled/bent down | Left click |
| Thumb pinches index finger | Drag (cursor moves while pinching) |
| Thumb pinches middle finger | Double click |
| Thumb pinches ring finger | Right click |
| Index + middle fingers up, move up | Scroll up |
| Index + middle fingers up, move down | Scroll down |
| Closed fist | Pause tracking |

- **Virtual trackpad zone** — green rectangle on screen bounds the active control area, mimicking a physical trackpad
- **Adaptive pinch threshold** — pinch distance scales with palm size for reliable detection at any distance from the camera
- **Kalman filter** smoothing for stable, jitter-free cursor movement
- **On-screen HUD** showing the currently detected gesture in real time
- **Always-on-top preview window** pinned to the top-left corner of the screen so it never gets buried under other windows
- Supports up to **2 hands** detected simultaneously
- Configurable click and scroll delays to prevent accidental inputs
- Mirrored webcam feed for intuitive control

---

## Requirements

- Python 3.8+
- Webcam

### Python dependencies

```
opencv-python
mediapipe
pyautogui
numpy
```

Install with:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## Usage

```bash
python main.py
```

- A window titled **"Vision Mouse"** opens showing the webcam feed with hand landmarks and the green trackpad zone drawn.
- Move your index finger inside the green zone to control the cursor.
- Use the gestures from the table above to click, scroll, and drag.
- Press **Esc** to quit.

---

## Project Structure

```
hand mouse/
├── main.py             # Entry point — main loop, orchestrates all modules
├── config.py           # Global constants (resolution, delays, thresholds)
├── hand_tracker.py     # MediaPipe hand detection and landmark drawing
├── gesture_engine.py   # Finger/gesture recognition logic
├── cursor_filter.py    # Kalman filter smoothing for cursor position
├── mouse_controller.py # PyAutoGUI mouse actions (move, click, drag)
├── ui_overlay.py       # Trackpad rectangle and HUD rendering
├── utils.py            # Shared helpers (dist, fingers_state)
└── README.md
```

---

## How It Works

1. **Hand detection** — `HandTracker` feeds each frame into MediaPipe Hands, which returns 21 3-D landmarks per hand.
2. **Gesture recognition** — `GestureEngine.analyze()` reads finger states and adaptive pinch distances (scaled to palm size) to classify gestures. Scroll direction (`scroll_up` / `scroll_down`) is determined by tracking index-finger vertical delta inside the engine.
3. **Virtual trackpad** — Only index-finger positions inside the green rectangle are mapped to screen coordinates, providing a stable bounded control area. The cursor continues to move while dragging (pinch).
4. **Left click via index bend** — Curling the index finger so its tip drops below its PIP joint triggers a left click, keeping pinch exclusively for drag.
5. **Cursor smoothing** — Raw mapped coordinates are fed into a Kalman filter (`CursorFilter`) to remove jitter before moving the cursor.
6. **Mouse actions** — `MouseController` translates gestures into PyAutoGUI calls (move, left-click, right-click, double-click, scroll, drag).
7. **HUD** — `draw_hud()` renders the active gesture name on the frame so you can verify detection at a glance.

---

## Configuration

All tuneable constants live in `config.py`:

| Constant | Default | Description |
|---|---|---|
| `FRAME_WIDTH` / `FRAME_HEIGHT` | `640` / `480` | Webcam capture resolution |
| `TRACKPAD_MARGIN` | `120` px | Inset of the virtual trackpad zone from frame edges |
| `CLICK_DELAY` | `0.35` s | Minimum time between consecutive clicks |
| `SCROLL_DELAY` | `0.08` s | Minimum time between scroll events |
| `SCROLL_THRESHOLD` | `20` px | Minimum hand movement to trigger a scroll |
| `SCROLL_MULTIPLIER` | `0.4` | Scroll speed multiplier |
