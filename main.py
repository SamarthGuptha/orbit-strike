import pygame, random, config
from entities.core import AetherCore
from entities.shield import OrbitalShield
from engine.renderer import draw_void_grid
from systems.midi_parser import LevelLoader
from entities.asteroid import Asteroid
from systems.particle_system import ParticleSystem
from ui.menu import MainMenu

def draw_hud(surface, health, combo):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    # Integrity (Health) Bar
    bar_width = 300
    bar_height = 10
    x, y = 20, 20
    pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_width, bar_height))
    health_ratio = max(0, health / config.MAX_INTEGRITY)
    color = (0, 255, 100) if health_ratio > 0.3 else (255, 50, 50)
    pygame.draw.rect(surface, color, (x, y, bar_width * health_ratio, bar_height))
    health_text = font.render(f"INTEGRITY: {int(health)}%", True, (255, 255, 255))
    surface.blit(health_text, (x, y + 15))
    combo_text = font.render(f"SYNCHRO: x{combo}", True, config.CORE_COLOR)
    surface.blit(combo_text, (config.WIDTH - 150, 20))


def main():
    pygame.init()
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), flags)
    pygame.display.set_caption("Orbit Strike!")
    clock = pygame.time.Clock()
    core = AetherCore()
    shield = OrbitalShield()
    particles = ParticleSystem()
    menu = MainMenu()

    # Game State Machine variables
    game_state = "MENU"
    asteroids = []
    audio_time = 0.0
    shake_time = 0.0
    shake_intensity = 0.0
    time_passed = 0.0
    health = config.MAX_INTEGRITY
    combo = 0
    main_surface = pygame.Surface((config.WIDTH, config.HEIGHT), flags)
    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        time_passed += dt
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    filepath = menu.get_midi_file()
                    if filepath:
                        loader = LevelLoader(filepath)
                        note_data = loader.parse()
                        asteroids = [Asteroid(data) for data in note_data]
                        audio_time = 0.0
                        health = config.MAX_INTEGRITY
                        combo = 0
                        game_state = "PLAYING"

            elif game_state in ["PLAYING", "GAMEOVER"]:
                if event.type == pygame.MOUSEBUTTONDOWN or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    if game_state == "GAMEOVER":
                        game_state = "MENU"
                        continue

                    shield.pulse()
                    for ast in asteroids:
                        if ast.state == "incoming" and ast.active:
                            time_diff = abs(audio_time - ast.hit_time)

                            if time_diff <= config.HIT_WINDOW_GOOD and shield.is_blocking(ast.angle):
                                ast.state = "destroyed"
                                combo += 1
                                if time_diff <= config.HIT_WINDOW_PERFECT:
                                    shake_time = 0.15
                                    shake_intensity = 8.0
                                    particles.emit(ast.x, ast.y, config.PARTICLE_COLOR, count=35)
                                else:
                                    particles.emit(ast.x, ast.y, config.PARTICLE_COLOR, count=15)

        core.update(dt)
        shield.update(mouse_x, mouse_y, dt)
        particles.update(dt)

        if game_state == "PLAYING":
            audio_time += dt
            for ast in asteroids:
                ast.update(audio_time)
                if ast.state == "missed" and not ast.counted:
                    ast.counted = True
                    health -= config.DAMAGE_PER_MISS
                    combo = 0

                    shake_time = 0.2
                    shake_intensity = 10.0
                    particles.emit(config.CX, config.CY, (255, 50, 50), count=40)

                    if health <= 0:
                        health = 0
                        game_state = "GAMEOVER"
        offset_x, offset_y = 0, 0
        if shake_time > 0:
            shake_time -= dt
            offset_x = random.uniform(-shake_intensity, shake_intensity)
            offset_y = random.uniform(-shake_intensity, shake_intensity)
        main_surface.fill(config.BG_COLOR)
        draw_void_grid(main_surface, (config.CX, config.CY))

        if game_state == "MENU":
            core.draw(main_surface)
            menu.draw(main_surface, time_passed)

        elif game_state in ["PLAYING", "GAMEOVER"]:
            for ast in asteroids:
                ast.draw(main_surface)
            particles.draw(main_surface)
            core.draw(main_surface)
            shield.draw(main_surface)
            draw_hud(main_surface, health, combo)

            if game_state == "GAMEOVER":
                font = pygame.font.SysFont('Arial', 64, bold=True)
                text = font.render("CORE BREACHED", True, (255, 50, 50))
                main_surface.blit(text, text.get_rect(center=(config.CX, config.CY - 50)))

                sub_font = pygame.font.SysFont('Arial', 24)
                sub_text = sub_font.render("[ CLICK TO RETURN TO MENU ]", True, (255, 255, 255))
                main_surface.blit(sub_text, sub_text.get_rect(center=(config.CX, config.CY + 20)))

        screen.blit(main_surface, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()