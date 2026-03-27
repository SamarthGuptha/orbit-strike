import math
def get_angle(x1, y1, x2, y2): return math.atan2(y2-y1, x2-x1)
def polar_to_cartesian(cx, cy, radius, angle):
    x = cx+radius*math.cos(angle)
    y = cy+radius*math.sin(angle)
    return x, y

def lerp_angle(current, target, factor):
    diff = (target - current+math.pi)%(2*math.pi)-math.pi
    return current + diff*factor
