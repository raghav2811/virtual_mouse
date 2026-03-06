import math

def dist(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])


def fingers_state(lm):

    tips=[4,8,12,16,20]
    fingers=[]

    fingers.append(1 if lm[4].x > lm[3].x else 0)

    for i in range(1,5):
        fingers.append(1 if lm[tips[i]].y < lm[tips[i]-2].y else 0)

    return fingers