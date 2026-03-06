from utils import dist, fingers_state
import time


class GestureEngine:

    def __init__(self):

        self.last_click = 0
        self.cooldown = 0.35

        self.scroll_mode = False
        self.scroll_anchor = None

    def analyze(self, pts, lm):

        thumb = pts[4]
        index = pts[8]
        middle = pts[12]
        ring = pts[16]
        pinky = pts[20]

        fingers = fingers_state(lm)

        palm_size = dist(pts[0], pts[9])
        pinch_threshold = palm_size * 0.32

        # ---------- PAUSE TRACKING ----------
        if sum(fingers) == 0:
            return "pause"

        # ---------- SCROLL MODE (FIST + THUMB UP) ----------
        if (fingers[0] == 1 and
            fingers[1] == 0 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0):

            if not self.scroll_mode:

                self.scroll_mode = True
                self.scroll_anchor = thumb[1]

            delta = self.scroll_anchor - thumb[1]

            if abs(delta) > 15:

                if delta > 0:
                    return "scroll_down"
                else:
                    return "scroll_up"

            return "scroll"

        else:

            self.scroll_mode = False
            self.scroll_anchor = None

        # ---------- POINTER MODE ----------
        if (fingers[0] == 1 and
            fingers[1] == 1 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0):

            return "pointer"

        # ---------- PINCH DRAG ----------
        if dist(thumb, index) < pinch_threshold:
            return "pinch"

        # ---------- LEFT CLICK ----------
        if dist(thumb, pinky) < pinch_threshold:

            if time.time() - self.last_click > self.cooldown:

                self.last_click = time.time()
                return "left_click"

        # ---------- RIGHT CLICK ----------
        if dist(thumb, ring) < pinch_threshold:
            return "right_click"

        # ---------- DOUBLE CLICK ----------
        if dist(thumb, middle) < pinch_threshold:
            return "double_click"

        return "none"