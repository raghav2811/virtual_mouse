import cv2
import pyautogui
from config import *
from hand_tracker import HandTracker
from cursor_filter import CursorFilter
from mouse_controller import MouseController
from gesture_engine import GestureEngine
from ui_overlay import draw_trackpad, draw_hud

tracker = HandTracker()
cursor = CursorFilter()
mouse = MouseController()
engine = GestureEngine()

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

trackpad_x1 = TRACKPAD_MARGIN
trackpad_y1 = TRACKPAD_MARGIN
trackpad_x2 = FRAME_WIDTH - TRACKPAD_MARGIN
trackpad_y2 = FRAME_HEIGHT - TRACKPAD_MARGIN

gesture = "none"

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame,(FRAME_WIDTH,FRAME_HEIGHT))

    results = tracker.detect(frame)

    draw_trackpad(frame,trackpad_x1,trackpad_y1,trackpad_x2,trackpad_y2)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            tracker.draw(frame,hand)

            lm = hand.landmark

            pts = [(int(l.x*FRAME_WIDTH),int(l.y*FRAME_HEIGHT)) for l in lm]

            gesture = engine.analyze(pts,lm)

            index = pts[8]

            if gesture == "pointer":

                x = (index[0]-trackpad_x1)/(trackpad_x2-trackpad_x1)*screen_w
                y = (index[1]-trackpad_y1)/(trackpad_y2-trackpad_y1)*screen_h

                x,y = cursor.smooth(x,y)

                mouse.move(x,y)

            elif gesture == "pinch":

                mouse.drag_start()

            else:

                mouse.drag_stop()

            if gesture == "right_click":
                mouse.right_click()

            if gesture == "double_click":
                mouse.double_click()

    draw_hud(frame,gesture)

    cv2.imshow("Vision Mouse",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()