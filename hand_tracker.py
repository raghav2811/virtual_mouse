import mediapipe as mp

class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils


    def detect(self, frame):

        rgb = frame[:, :, ::-1]

        results = self.hands.process(rgb)

        return results


    def draw(self, frame, hand):

        self.drawer.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )