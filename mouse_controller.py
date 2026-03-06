import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class MouseController:

    def __init__(self):

        self.dragging = False
        self.last_click = 0


    def move(self, x, y):

        pyautogui.moveTo(x, y)


    def left_click(self):

        pyautogui.click()


    def right_click(self):

        pyautogui.rightClick()


    def double_click(self):

        pyautogui.doubleClick()


    def scroll(self, amount):

        pyautogui.scroll(amount)


    def drag_start(self):

        if not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True


    def drag_stop(self):

        if self.dragging:
            pyautogui.mouseUp()
            self.dragging = False