import pygame
from constants import *

class Location:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 64, 64)
        # Add color mapping for locations
        self.color = {
            "dorm": (200, 200, 200),
            "classroom": (150, 150, 150),
            "library": (170, 140, 100),
            "cafeteria": (200, 150, 150),
            "gym": (150, 200, 150),
            "club_room": (150, 150, 200)
        }.get(self.name, WHITE)

    def draw(self, screen):
        # Draw locations as colored rectangles with labels
        color = {
            "dorm": (200, 200, 200),
            "classroom": (150, 150, 150),
            "library": (170, 140, 100),
            "cafeteria": (200, 150, 150),
            "gym": (150, 200, 150),
            "club_room": (150, 150, 200)
        }.get(self.name, WHITE)
        
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw location name
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + 32, self.y + 32))
        screen.blit(text, text_rect)

    def perform_action(self, player):
        # Actions for each location
        if self.name == "library":
            player.study(player.major)
        elif self.name == "dorm":
            player.energy = min(player.energy + 50, 100)
        elif self.name == "cafeteria":
            if player.money >= 10:
                player.money -= 10
                player.energy = min(player.energy + 30, 100)
        elif self.name == "gym":
            if player.energy >= 20:
                player.energy -= 20
                player.social_points += 5
        elif self.name == "classroom":
            if player.energy >= 30:
                player.energy -= 30
                player.grades[player.major] += 0.1
        elif self.name == "club_room":
            if player.energy >= 15:
                player.energy -= 15
                player.social_points += 10
        elif self.name == "student_center":  # New location
            player.work_part_time()
        elif self.name == "study_hall":      # New location
            player.tutor_students()