import pygame
from constants import *

class ClubMenu:
    def __init__(self, player):
        self.player = player
        self.visible = False
        self.clubs = [
            {"name": "Chess Club", "energy": 15, "social": 20},
            {"name": "Debate Team", "energy": 20, "social": 25},
            {"name": "Gaming Club", "energy": 10, "social": 15},
            {"name": "Drama Club", "energy": 25, "social": 30},
            {"name": "Music Society", "energy": 15, "social": 20}
        ]
        
    def toggle_visibility(self):
        self.visible = not self.visible
        
    def handle_click(self, pos):
        if not self.visible:
            return False
            
        # Check if click is within club menu area
        menu_rect = pygame.Rect(50, 50, 400, 300)
        if not menu_rect.collidepoint(pos):
            return False
            
        # Calculate club button positions and check clicks
        for i, club in enumerate(self.clubs):
            club_rect = pygame.Rect(70, 80 + i * 50, 360, 40)
            if club_rect.collidepoint(pos):
                return self.join_club(i)
        return False
        
    def join_club(self, index):
        if index < 0 or index >= len(self.clubs):
            return False
            
        club = self.clubs[index]
        if self.player.energy < club["energy"]:
            return False
            
        # Apply club effects
        self.player.energy -= club["energy"]
        self.player.social += club["social"]
        return True
        
    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw menu background
        menu_rect = pygame.Rect(50, 50, 400, 300)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 2)
        
        # Draw title
        font = pygame.font.Font(None, 32)
        title = font.render("Available Clubs", True, BLACK)
        screen.blit(title, (70, 60))
        
        # Draw clubs
        font = pygame.font.Font(None, 24)
        for i, club in enumerate(self.clubs):
            club_rect = pygame.Rect(70, 80 + i * 50, 360, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, club_rect)
            pygame.draw.rect(screen, BLACK, club_rect, 1)
            
            text = font.render(f"{club['name']} (-{club['energy']} energy, +{club['social']} social)", True, BLACK)
            screen.blit(text, (80, 90 + i * 50))