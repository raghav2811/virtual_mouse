import cv2
import pyautogui

from config import *
from hand_tracker import HandTracker
from cursor_filter import CursorFilter
from mouse_controller import MouseController
from gesture_engine import GestureEngine
from ui_overlay import draw_trackpad, draw_hud


# ---------- INITIALIZE SYSTEM ----------

tracker = HandTracker()
cursor = CursorFilter()
mouse = MouseController()
engine = GestureEngine()

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

gesture = "none"


# ---------- TRACKPAD REGION ----------

trackpad_x1 = TRACKPAD_MARGIN
trackpad_y1 = TRACKPAD_MARGIN
trackpad_x2 = FRAME_WIDTH - TRACKPAD_MARGIN
trackpad_y2 = FRAME_HEIGHT - TRACKPAD_MARGIN


# ---------- PREVIEW WINDOW (ALWAYS ON TOP) ----------

cv2.namedWindow("Vision Mouse", cv2.WINDOW_AUTOSIZE)

cv2.setWindowProperty(
    "Vision Mouse",
    cv2.WND_PROP_TOPMOST,
    1
)

cv2.moveWindow("Vision Mouse", 20, 20)


# ---------- MAIN LOOP ----------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame = cv2.resize(
        frame,
        (FRAME_WIDTH, FRAME_HEIGHT)
    )

    results = tracker.detect(frame)

    draw_trackpad(
        frame,
        trackpad_x1,
        trackpad_y1,
        trackpad_x2,
        trackpad_y2
    )

    gesture = "none"

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            tracker.draw(frame, hand)

            lm = hand.landmark

            pts = [
                (int(l.x * FRAME_WIDTH), int(l.y * FRAME_HEIGHT))
                for l in lm
            ]

            gesture = engine.analyze(pts, lm)

            index = pts[8]

            # ---------- POINTER ----------

            if gesture == "pointer":

                if (trackpad_x1 < index[0] < trackpad_x2 and
                    trackpad_y1 < index[1] < trackpad_y2):

                    x = (index[0] - trackpad_x1) / (trackpad_x2 - trackpad_x1) * screen_w
                    y = (index[1] - trackpad_y1) / (trackpad_y2 - trackpad_y1) * screen_h

                    x, y = cursor.smooth(x, y)

                    mouse.move(x, y)

            # ---------- PINCH DRAG ----------

            elif gesture == "pinch":

                mouse.drag_start()

            else:

                mouse.drag_stop()

            # ---------- LEFT CLICK (INDEX BEND) ----------

            if gesture == "left_click":

                mouse.left_click()

            # ---------- RIGHT CLICK ----------

            if gesture == "right_click":

                mouse.right_click()

            # ---------- DOUBLE CLICK ----------

            if gesture == "double_click":

                mouse.double_click()

            # ---------- SCROLL ----------

            if gesture == "scroll_up":

                mouse.scroll(40)

            if gesture == "scroll_down":

                mouse.scroll(-40)

    # ---------- HUD ----------

    draw_hud(frame, gesture)

    cv2.imshow(
        "Vision Mouse",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break


# ---------- CLEANUP ----------

cap.release()
cv2.destroyAllWindows()