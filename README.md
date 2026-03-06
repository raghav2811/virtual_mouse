import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

frame_w = 640
frame_h = 480

# ---------- TRACKPAD ----------

trackpad_margin = 120
trackpad_x1 = trackpad_margin
trackpad_y1 = trackpad_margin
trackpad_x2 = frame_w - trackpad_margin
trackpad_y2 = frame_h - trackpad_margin

# ---------- KALMAN FILTER ----------

kalman = cv2.KalmanFilter(4,2)

kalman.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]],np.float32)

kalman.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]],np.float32)

kalman.processNoiseCov = np.eye(4,dtype=np.float32)*0.03

# ---------- STATE VARIABLES ----------

dragging = False
scroll_prev_y = None
last_click = 0
click_delay = 0.35
last_scroll = 0
scroll_delay = 0.08
prev_z = None

gesture_name = "None"


def dist(p1,p2):
    return math.hypot(p2[0]-p1[0],p2[1]-p1[1])


def fingers_state(lm):

    tips=[4,8,12,16,20]
    fingers=[]

    fingers.append(1 if lm[4].x > lm[3].x else 0)

    for i in range(1,5):
        fingers.append(1 if lm[tips[i]].y < lm[tips[i]-2].y else 0)

    return fingers


while True:

    success,frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame,(frame_w,frame_h))

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # draw trackpad
    cv2.rectangle(frame,(trackpad_x1,trackpad_y1),
                  (trackpad_x2,trackpad_y2),(0,255,0),2)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark

            pts=[(int(l.x*frame_w),int(l.y*frame_h)) for l in lm]

            thumb=pts[4]
            index=pts[8]
            middle=pts[12]
            ring=pts[16]

            index_z = lm[8].z

            fingers=fingers_state(lm)

            # adaptive pinch
            palm_size = dist(pts[0], pts[9])
            pinch_threshold = palm_size * 0.4

            # ---------- CLOSED FIST ----------

            if sum(fingers)==0:

                gesture_name="Paused"

                dragging=False
                pyautogui.mouseUp()
                continue

            # ---------- SCROLL ----------

            if fingers[1]==1 and fingers[2]==1 and fingers[3]==0:

                gesture_name="Scroll"

                if scroll_prev_y is None:
                    scroll_prev_y=index[1]

                delta=scroll_prev_y-index[1]

                if abs(delta)>20:

                    if time.time()-last_scroll > scroll_delay:

                        pyautogui.scroll(int(delta*0.4))

                        scroll_prev_y=index[1]
                        last_scroll=time.time()

                continue

            else:
                scroll_prev_y=None

            # ---------- TRACKPAD LIMIT ----------

            if not (trackpad_x1 < index[0] < trackpad_x2 and
                    trackpad_y1 < index[1] < trackpad_y2):
                continue

            # ---------- POINTER ----------

            if fingers[1]==1 and fingers[2]==0:

                x=np.interp(index[0],
                            (trackpad_x1,trackpad_x2),
                            (0,screen_w))

                y=np.interp(index[1],
                            (trackpad_y1,trackpad_y2),
                            (0,screen_h))

                measurement=np.array([[np.float32(x)],
                                      [np.float32(y)]])

                kalman.correct(measurement)
                prediction=kalman.predict()

                smooth_x=int(prediction[0][0])
                smooth_y=int(prediction[1][0])

                pyautogui.moveTo(smooth_x,smooth_y)

                gesture_name="Pointer"

            # ---------- DRAG ----------

            if dist(thumb,index) < pinch_threshold:

                if not dragging:

                    pyautogui.mouseDown()
                    dragging=True
                    gesture_name="Dragging"

            else:

                if dragging:

                    pyautogui.mouseUp()
                    dragging=False

            # ---------- LEFT CLICK ----------

            if dist(thumb,index) < pinch_threshold and fingers[2]==0:

                if time.time()-last_click > click_delay:

                    pyautogui.click()
                    last_click=time.time()
                    gesture_name="Left Click"

            # ---------- RIGHT CLICK ----------

            if dist(thumb,ring) < pinch_threshold:

                if time.time()-last_click > click_delay:

                    pyautogui.rightClick()
                    last_click=time.time()
                    gesture_name="Right Click"

            # ---------- DOUBLE CLICK ----------

            if dist(thumb,middle) < pinch_threshold and fingers[1]==0:

                if time.time()-last_click > click_delay:

                    pyautogui.doubleClick()
                    last_click=time.time()
                    gesture_name="Double Click"

            # ---------- DEPTH CLICK ----------

            if prev_z is not None:

                if prev_z - index_z > 0.05:

                    if time.time()-last_click > click_delay:

                        pyautogui.click()
                        last_click=time.time()
                        gesture_name="Depth Click"

            prev_z=index_z

    # ---------- HUD ----------

    cv2.rectangle(frame,(10,10),(300,60),(0,0,0),-1)

    cv2.putText(frame,
                "Gesture: "+gesture_name,
                (20,45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.imshow("AI Virtual Mouse",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()