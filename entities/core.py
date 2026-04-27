import math, config
from engine.renderer import draw_glow_circle
class AetherCore:
    def __init__(self):
        self.x = config.CX
        self.y = config.CY
        self.base_radius = 25
        self.time_passed = 0

    def update(self, dt):
        self.time_passed += dt

    def draw(self, surface):
        pulse = math.sin(self.time_passed * 4) * 4
        current_radius = self.base_radius + pulse
        glow_radius = current_radius * 3.5

        draw_glow_circle(surface, config.CORE_COLOR, (self.x, self.y), current_radius, glow_radius)