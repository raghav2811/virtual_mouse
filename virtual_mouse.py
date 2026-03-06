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
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

frame_w = 640
frame_h = 480

# -------- Kalman Filter --------

kalman = cv2.KalmanFilter(4,2)

kalman.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]],np.float32)

kalman.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]],np.float32)

kalman.processNoiseCov = np.eye(4,dtype=np.float32)*0.03

# -------- Variables --------

dragging = False
scroll_prev_y = None

last_click = 0
click_delay = 0.35

prev_z = None


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

    success,frame=cap.read()
    if not success:
        break

    frame=cv2.flip(frame,1)
    frame=cv2.resize(frame,(frame_w,frame_h))

    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results=hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)

            lm=hand.landmark

            pts=[(int(l.x*frame_w),int(l.y*frame_h)) for l in lm]

            thumb=pts[4]
            index=pts[8]
            middle=pts[12]
            ring=pts[16]

            index_z = lm[8].z

            fingers=fingers_state(lm)

            # -------- CLOSED PALM --------

            if sum(fingers)==0:

                dragging=False
                pyautogui.mouseUp()

                cv2.putText(frame,"TRACKING OFF",(20,40),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                continue

            # -------- POINTER --------

            if fingers[1]==1 and fingers[2]==0:

                x=np.interp(index[0],(0,frame_w),(0,screen_w))
                y=np.interp(index[1],(0,frame_h),(0,screen_h))

                measurement=np.array([[np.float32(x)],
                                      [np.float32(y)]])

                kalman.correct(measurement)

                prediction=kalman.predict()

                smooth_x=int(prediction[0][0])
                smooth_y=int(prediction[1][0])

                pyautogui.moveTo(smooth_x,smooth_y)

                cv2.circle(frame,index,10,(255,0,255),-1)

            # -------- LEFT CLICK --------

            if dist(thumb,index)<30:

                if time.time()-last_click>click_delay:

                    pyautogui.click()
                    last_click=time.time()

                    cv2.putText(frame,"LEFT CLICK",(20,80),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # -------- RIGHT CLICK --------

            if dist(thumb,ring)<30:

                if time.time()-last_click>click_delay:

                    pyautogui.rightClick()
                    last_click=time.time()

                    cv2.putText(frame,"RIGHT CLICK",(20,120),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # -------- DOUBLE CLICK --------

            if dist(thumb,middle)<30:

                if time.time()-last_click>click_delay:

                    pyautogui.doubleClick()
                    last_click=time.time()

                    cv2.putText(frame,"DOUBLE CLICK",(20,160),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # -------- DRAG --------

            if dist(thumb,index)<25:

                if not dragging:

                    pyautogui.mouseDown()
                    dragging=True

            else:

                if dragging:

                    pyautogui.mouseUp()
                    dragging=False

            # -------- DEPTH CLICK --------

            if prev_z is not None:

                if prev_z - index_z > 0.05:

                    if time.time()-last_click>click_delay:

                        pyautogui.click()
                        last_click=time.time()

                        cv2.putText(frame,"DEPTH CLICK",(20,200),
                                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

            prev_z=index_z

           # -------- SCROLL --------

            if fingers[1]==1 and fingers[2]==1 and fingers[3]==0:

                if scroll_prev_y is None:
                    scroll_prev_y=index[1]

                delta = scroll_prev_y - index[1]

                # ignore small movements
                if abs(delta) > 25:

                    scroll_amount = int(delta * 0.5)

                    pyautogui.scroll(scroll_amount)

                    scroll_prev_y = index[1]

                    cv2.putText(frame,"SCROLL",(20,240),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

            else:
                scroll_prev_y=None


    cv2.imshow("Virtual Mouse",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()