from utils import dist, fingers_state


class GestureEngine:

    def __init__(self):

        self.scroll_prev_y = None

    def analyze(self, pts, lm):

        thumb = pts[4]
        index = pts[8]
        middle = pts[12]
        ring = pts[16]

        index_pip = pts[6]   # index middle joint

        fingers = fingers_state(lm)

        palm_size = dist(pts[0], pts[9])
        pinch_threshold = palm_size * 0.4

        # ---------- PAUSE ----------

        if sum(fingers) == 0:
            return "pause"

        # ---------- SCROLL ----------

        if fingers[1] and fingers[2] and not fingers[3]:

            if self.scroll_prev_y is None:
                self.scroll_prev_y = index[1]

            delta = self.scroll_prev_y - index[1]

            if abs(delta) > 25:  # larger threshold = less sensitive

                self.scroll_prev_y = index[1]

                if delta > 0:
                    return "scroll_up"
                else:
                    return "scroll_down"

        else:
            self.scroll_prev_y = None

        # ---------- RIGHT CLICK ----------

        if dist(thumb, ring) < pinch_threshold:
            return "right_click"

        # ---------- DOUBLE CLICK ----------

        if dist(thumb, middle) < pinch_threshold:
            return "double_click"

        # ---------- PINCH DRAG ----------

        if dist(thumb, index) < pinch_threshold:
            return "pinch"

        # ---------- INDEX BEND CLICK ----------

        # when fingertip goes below middle joint → finger bent
        if index[1] > index_pip[1] + 15:
            return "left_click"

        # ---------- POINTER ----------

        if fingers[1] and not fingers[2]:
            return "pointer"

        return "none"