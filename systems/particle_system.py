import pygame, math, random

class Particle:
    def __init__(self, x, y, color):
        self.x=x
        self.y=y
        self.color = color

        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(100, 400)
        self.vx = math.cos(angle)*speed
        self.vy = math.sin(angle)*speed

        self.max_life = random.uniform(0.3, 0.7)
        self.lifetime = self.max_life

    def update(self, dt):
        self.x +=self.vx*dt
        self.y = self.vy*dt
        self.vx *= 0.95
        self.vy *= 0.95

        self.lifetime -=dt


    def draw(self, surface):
        if self.lifetime <= 0: return

        life_ratio = max(0, self.lifetime/self.max_life)
        alpha = int(255*life_ratio)
        size = max(1, int(4*life_ratio))

        surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color[:3], alpha), (size, size), size)
        surface.blit(surf, (self.x-size, self.y-size), special_flags=pygame.BLEND_RGBA_ADD)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime>0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)