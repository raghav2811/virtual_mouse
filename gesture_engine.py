import time
from utils import dist, fingers_state

class GestureEngine:

    def __init__(self):

        self.scroll_prev_y = None
        self.prev_z = None


    def analyze(self, pts, lm):

        thumb = pts[4]
        index = pts[8]
        middle = pts[12]
        ring = pts[16]

        fingers = fingers_state(lm)

        palm_size = dist(pts[0], pts[9])
        pinch_threshold = palm_size * 0.4

        gesture = "none"

        if sum(fingers) == 0:
            return "pause"

        if fingers[1] and fingers[2] and not fingers[3]:
            return "scroll"

        if dist(thumb,index) < pinch_threshold:
            return "pinch"

        if dist(thumb,ring) < pinch_threshold:
            return "right_click"

        if dist(thumb,middle) < pinch_threshold:
            return "double_click"

        if fingers[1] and not fingers[2]:
            return "pointer"

        return gesture