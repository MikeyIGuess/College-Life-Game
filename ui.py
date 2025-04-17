import pygame
from constants import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, player, time_manager):
        # Time and date
        self.draw_text(f"Day {time_manager.day} - {time_manager.get_time_string()}", 10, 10)
        
        # Player stats
        self.draw_text(f"Energy: {int(player.energy)}", 10, 50)
        self.draw_text(f"Money: ${player.money}", 10, 90)
        self.draw_text(f"Social: {player.social_points}", 10, 130)
        self.draw_text(f"GPA: {self.calculate_gpa(player.grades):.2f}", 10, 170)
        
    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, BLACK)
        self.screen.blit(surface, (x, y))
        
    def calculate_gpa(self, grades):
        return sum(grades.values()) / len(grades)