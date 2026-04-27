import pygame, config
from engine.trig_math import polar_to_cartesian

class Asteroid:
    def __init__(self, note_data):
        self.hit_time = note_data['hit_time'] + config.TRAVEL_TIME
        self.spawn_time = self.hit_time - config.TRAVEL_TIME
        self.angle = note_data['angle']
        self.base_radius = note_data['radius']

        self.active = False
        self.state = "incoming"
        self.counted = False

        self.x, self.y = 0, 0
        self.trail = []

    def update(self, current_time):
        if current_time >= self.spawn_time and self.state == "incoming": self.active= True
        if not self.active or self.state != "incoming": return

        progress = (current_time - self.spawn_time) / config.TRAVEL_TIME
        if progress >= 1.0:
            self.state = "missed"
            self.active = False
            return

        current_distance = config.SPAWN_RADIUS - (config.SPAWN_RADIUS-150)*progress
        self.x, self.y = polar_to_cartesian(config.CX, config.CY, current_distance, self.angle)
        self.trail.append((self.x, self.y))
        if len(self.trail)>12: self.trail.pop(0)

    def draw(self, surface):
        if not self.active or self.state != "incoming": return

        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255*(i/len(self.trail)))
            size = self.base_radius*(i/len(self.trail))

            if size>1:
                trail_surf = pygame.Surface((int(size*2), int(size*2)), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (*config.ASTEROID_COLOR[:3], alpha), (int(size), int(size)), size)
                surface.blit(trail_surf, (tx-size, ty-size), special_flags = pygame.BLEND_RGBA_ADD)\

        head_surf = pygame.Surface((int(self.base_radius*4), int(self.base_radius*4)), pygame.SRCALPHA)
        cx, cy = int(self.base_radius*2), int(self.base_radius*2)

        pygame.draw.circle(head_surf, (255, 255, 255, 255), (cx, cy), self.base_radius*0.5)
        pygame.draw.circle(head_surf, (*config.ASTEROID_COLOR[:3], 150), (cx, cy), self.base_radius)

        surface.blit(head_surf, (self.x-cx, self.y-cy), special_flags=pygame.BLEND_RGB_ADD)


