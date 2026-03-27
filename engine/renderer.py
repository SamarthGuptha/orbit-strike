import pygame, math
from engine.trig_math import polar_to_cartesian
_glow_surf = None
def get_glow_surface(size):
    global _glow_surf
    if _glow_surf is None or _glow_surf.get_size() != size:
        _glow_surf = pygame.Surface(size, pygame.SRCALPHA)
    _glow_surf.fill((0, 0, 0, 0))
    return _glow_surf

def draw_glow_circle(surface, color, center, radius, glow_radius):
    surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
    cx, cy = glow_radius, glow_radius

    layers = 6
    for i in range(layers, 0, -1):
        r = radius + (glow_radius - radius)*(i/layers)
        alpha = int(255*(0.15*(1-i/layers)))
        pygame.draw.circle(surf, (*color[:3], alpha), (cx, cy), r)

    pygame.draw.circle(surf, (255, 255, 255, 255), (cx, cy), radius*0.8)
    pygame.draw.circle(surf, (*color[:3], 200), (cx, cy), radius)
    surface.blit(surf, (center[0]-cx, center[1]-cy), special_flags=pygame.BLEND_RGBA_ADD)

def draw_neon_arc(surface, color, center, radius, start_angle, end_angle, width=4):
    glow_surf = get_glow_surface(surface.get_size())

    points = []
    steps=30
    for i in range(steps+1):
        theta = start_angle+(end_angle-start_angle)*(i/steps)
        points.append(polar_to_cartesian(center[0], center[1], radius, theta))
    pygame.draw.lines(glow_surf, (*color[:3], 80), False, points, width*4)
    pygame.draw.lines(glow_surf, (255, 255, 255, 255), False, points)
    surface.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def draw_void_grid(surface, center):
    for r in [150, 300, 450, 600]:
        pygame.draw.circle(surface, (25, 20, 40), center, r, 1)





