import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class MouseController:

    def __init__(self):

        self.dragging = False

        # click cooldowns
        self.left_last = 0
        self.right_last = 0
        self.double_last = 0

        self.cooldown = 0.35

        # drag delay
        self.pinch_start = None
        self.pinch_delay = 1.0

    def move(self, x, y):

        pyautogui.moveTo(x, y)

    def left_click(self):

        if time.time() - self.left_last > self.cooldown:

            pyautogui.click()
            self.left_last = time.time()

    def right_click(self):

        if time.time() - self.right_last > self.cooldown:

            pyautogui.rightClick()
            self.right_last = time.time()

    def double_click(self):

        if time.time() - self.double_last > self.cooldown:

            pyautogui.doubleClick()
            self.double_last = time.time()

    def scroll(self, amount):

        pyautogui.scroll(amount)

    def drag_start(self):

        if not self.dragging:

            self.dragging = True
            self.pinch_start = time.time()
            pyautogui.mouseDown()

    def drag_stop(self):

        if self.dragging:

            pyautogui.mouseUp()
            self.dragging = False
            self.pinch_start = None

    def drag_ready(self):

        if self.pinch_start is None:
            return False

        return time.time() - self.pinch_start > self.pinch_delay