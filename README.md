# Hand Mouse — Virtual Mouse via Hand Gestures

Control your mouse cursor using only your hand and a webcam. Powered by **MediaPipe**, **OpenCV**, and **PyAutoGUI**, this project tracks real-time hand landmarks to move the cursor, click, scroll, and drag — no physical mouse required.

---

## Features

| Gesture | Action |
|---|---|
| Index finger up (only) | Move cursor |
| Thumb touches index finger | Left click / Drag |
| Thumb touches middle finger | Double click |
| Thumb touches ring finger | Right click |
| Index + middle fingers up | Scroll (move hand up/down) |
| Index finger pushed forward (z-axis) | Depth click |
| Closed fist | Pause tracking |

- **Kalman filter** smoothing for stable, jitter-free cursor movement
- Configurable click delay to prevent accidental rapid clicks
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
python virtual_mouse.py
```

- A window titled **"Virtual Mouse"** will open showing the webcam feed with hand landmarks drawn.
- Use the gestures from the table above to control your system mouse.
- Press **Esc** to quit.

---

## How It Works

1. **Hand detection** — MediaPipe Hands detects 21 hand landmarks in each webcam frame.
2. **Finger state** — Fingertip positions relative to their knuckles determine which fingers are raised.
3. **Cursor movement** — The index fingertip coordinates are mapped from the camera frame resolution to screen resolution and smoothed with a Kalman filter before moving the cursor.
4. **Gesture recognition** — Distances between the thumb tip and other fingertips trigger click/drag actions. Two-finger detection triggers scrolling.
5. **Depth click** — A sudden forward movement of the index finger (decrease in z-depth) triggers a click without a pinch gesture.

---

## Configuration

These variables near the top of `virtual_mouse.py` can be tuned:

| Variable | Default | Description |
|---|---|---|
| `frame_w` / `frame_h` | `640` / `480` | Webcam capture resolution |
| `click_delay` | `0.35` s | Minimum time between consecutive clicks |
| `min_detection_confidence` | `0.7` | MediaPipe detection threshold |
| `min_tracking_confidence` | `0.7` | MediaPipe tracking threshold |
| `processNoiseCov` scale | `0.03` | Kalman filter smoothness (lower = smoother) |

---

## Project Structure

```
hand mouse/
├── virtual_mouse.py   # Main application
└── README.md
```
