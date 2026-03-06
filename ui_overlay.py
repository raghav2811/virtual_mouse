import cv2

def draw_trackpad(frame, x1, y1, x2, y2):

    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)


def draw_hud(frame, gesture):

    cv2.rectangle(frame,(10,10),(300,60),(0,0,0),-1)

    cv2.putText(frame,
                "Gesture: "+gesture,
                (20,45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)