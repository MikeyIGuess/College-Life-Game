import pygame
import random
from constants import *

class NPC:
    def __init__(self, x, y, major):
        self.x = x
        self.y = y
        self.major = major
        self.friendship_level = 0
        self.rect = pygame.Rect(x, y, 32, 32)
        self.talked_today = False
        self.personality = random.choice(["shy", "outgoing", "studious"])
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
    def update(self, time_manager):
        if time_manager.is_new_day():
            self.talked_today = False
            # Random movement
            self.x += random.randint(-50, 50)
            self.y += random.randint(-50, 50)
            # Keep within bounds
            self.x = max(0, min(self.x, WINDOW_WIDTH - 32))
            self.y = max(0, min(self.y, WINDOW_HEIGHT - 32))
            self.rect.x = self.x
            self.rect.y = self.y
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x + 16, self.y + 16), 16)
        if self.talked_today:
            # Show if we've talked to them
            pygame.draw.circle(screen, BLACK, (self.x + 16, self.y + 16), 18, 2)

    def interact(self, player):
        if not self.talked_today:
            self.talked_today = True
            if self.major == player.major:
                player.social_points += 10
                self.friendship_level += 1
                return f"Found a {self.major} major! +10 social points!"
            else:
                player.social_points += 2
                return f"They're a {self.major} major. +2 social points"
        return "Already talked today."