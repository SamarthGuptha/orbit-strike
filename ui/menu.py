import pygame, math, config
import tkinter as tk
from tkinter import filedialog

class MainMenu:
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 72, bold=True)
        self.sub_font = pygame.font.SysFont('Arial', 24, bold=True)

    def draw(self, surface, time_passed):
        alpha = int(128+127*math.sin(time_passed*4))
        title_surf = self.title_font.render("ORBIT STRIKE", True, config.CORE_COLOR)
        title_rect = title_surf.get_rect(center=(config.CX, config.CY - 50))
        prompt_surf = self.sub_font.render("[CLICK TO SELECT MIDI TRACK]", True, config.SHIELD_COLOR)
        prompt_surf.set_alpha(alpha)
        prompt_rect = prompt_surf.get_rect(center=(config.CX, config.CY + 50))

        surface.blit(title_surf, title_rect)
        surface.blit(prompt_surf, prompt_rect)

    def get_midi_file(self):
        root = tk.Tk()
        root.withdraw()

        try:
            root.attributes('-topmost', True)
        except tk.TclError: pass

        filepath = filedialog.askopenfilename(
            title="Select MIDI Track",
            filetypes=[("MIDI Files", "*.mid *.midi"), ("All Files", "*.*")]
        )
        root.destroy()
        return filepath

