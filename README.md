# Hand Mouse — AI Virtual Mouse via Hand Gestures

Control your system mouse using only your hand and a webcam. Powered by **MediaPipe**, **OpenCV**, and **PyAutoGUI**, the project detects hand landmarks in real time to move the cursor, click, scroll, and drag — no physical mouse required.

---

## Features

| Gesture | Hand Shape | Action |
|---|---|---|
| Pointer | Thumb + index finger extended, all others curled | Move cursor |
| Pinch drag | Thumb tip touches index fingertip | Drag — holds for 1 s then locks mouse button down |
| Thumb → pinky | Thumb tip touches pinky fingertip | Left click |
| Thumb → middle | Thumb tip touches middle fingertip | Double click |
| Thumb → ring | Thumb tip touches ring fingertip | Right click |
| Thumb scroll ↑ | Only thumb extended, move thumb upward | Scroll up |
| Thumb scroll ↓ | Only thumb extended, move thumb downward | Scroll down |
| Closed fist | All fingers curled | Pause / resume tracking |

- **Virtual trackpad zone** — green rectangle on screen bounds the active control area, mimicking a physical trackpad
- **Adaptive pinch threshold** — pinch distance scales with palm size for reliable detection at any distance from the camera
- **Drag intent delay** — pinch must be held for **1 second** before drag activates, preventing accidental drags
- **Thumb-based scroll mode** — raise only the thumb and move it up or down to scroll; a 15 px delta threshold filters noise
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
2. **Gesture recognition** — `GestureEngine.analyze()` reads finger states (extended vs. curled) and adaptive pinch distances (scaled to palm size) to classify gestures. Each click type uses a distinct pinch pair: index for drag, middle for double-click, ring for right-click, pinky for left-click.
3. **Scroll mode** — When only the thumb is extended, the engine enters scroll mode and anchors the thumb's Y position. Moving the thumb more than 15 px from that anchor fires `scroll_up` or `scroll_down`.
4. **Virtual trackpad** — Only index-fingertip positions inside the green rectangle are mapped to screen coordinates, providing a stable bounded control area. The cursor continues to move while dragging (pinch).
5. **Drag intent delay** — When a pinch is detected, `MouseController` starts a 1-second timer. The mouse button is only held down after that delay elapses, making drag intentional rather than accidental.
6. **Cursor smoothing** — Raw mapped coordinates are fed into a Kalman filter (`CursorFilter`) to remove jitter before moving the cursor.
7. **Mouse actions** — `MouseController` translates gestures into PyAutoGUI calls (move, left-click, right-click, double-click, scroll, drag).
8. **HUD** — `draw_hud()` renders the active gesture name on the frame so you can verify detection at a glance.

---

## Configuration

All tuneable constants live in `config.py`:

| Constant | Default | Description |
|---|---|---|
| `FRAME_WIDTH` / `FRAME_HEIGHT` | `640` / `480` | Webcam capture resolution |
| `TRACKPAD_MARGIN` | `120` px | Inset of the virtual trackpad zone from frame edges |
| `CLICK_DELAY` | `0.35` s | Minimum time between consecutive clicks |
| `SCROLL_DELAY` | `0.08` s | Minimum time between scroll events |
| `SCROLL_THRESHOLD` | `20` px | Reserved scroll delta threshold constant |
| `SCROLL_MULTIPLIER` | `0.4` | Reserved scroll speed multiplier constant |
