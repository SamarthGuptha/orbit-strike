import math, config
from engine.trig_math import get_angle, lerp_angle
from engine.renderer import draw_neon_arc
class OrbitalShield:
    def __init__(self):
        self.radius=150
        self.angle=0.0
        self.target_angle=0.0
        self.arc_length = math.pi/2.5
        self.smoothness = 15.0
        self.pulse_timer = 0.0

    def pulse(self): self.pulse_timer = 0.15
    def is_blocking(self, incoming_angle):
        diff = (incoming_angle - self.angle+math.pi)%(2*math.pi)-math.pi
        return abs(diff)<=(self.arc_length/2)

    def update(self, mouse_x, mouse_y, dt):
        self.target_angle = get_angle(config.CX, config.CY, mouse_x, mouse_y)
        self.angle = lerp_angle(self.angle, self.target_angle, self.smoothness*dt)
        if self.pulse_timer>0:
            self.pulse_timer -= dt


    def draw(self, surface):
        start_a = self.angle - self.arc_length/2
        end_a = self.angle + self.arc_length/2
        width = 8 if self.pulse_timer>0 else 4

        draw_neon_arc(surface, config.SHIELD_COLOR, (config.CX, config.CY), self.radius, start_a, end_a, width)
