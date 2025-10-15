import pygame
from constants import *

class JobMenu:
    def __init__(self, player):
        self.player = player
        self.visible = False
        self.jobs = [
            {"name": "Lifeguard", "energy": 20, "money": 30},
            {"name": "Trainer", "energy": 25, "money": 35},
            {"name": "Receptionist", "energy": 15, "money": 25},
            {"name": "Equipment Manager", "energy": 20, "money": 30},
            {"name": "Fitness Instructor", "energy": 30, "money": 40}
        ]
        
    def toggle_visibility(self):
        self.visible = not self.visible
        
    def handle_click(self, pos):
        if not self.visible:
            return False
            
        # Check if click is within job menu area
        menu_rect = pygame.Rect(50, 50, 400, 300)
        if not menu_rect.collidepoint(pos):
            return False
            
        # Calculate job button positions and check clicks
        for i, job in enumerate(self.jobs):
            job_rect = pygame.Rect(70, 80 + i * 50, 360, 40)
            if job_rect.collidepoint(pos):
                return self.take_job(i)
        return False
        
    def take_job(self, index):
        if index < 0 or index >= len(self.jobs):
            return False
            
        job = self.jobs[index]
        if self.player.energy < job["energy"]:
            return False
            
        # Apply job effects
        self.player.energy -= job["energy"]
        self.player.money += job["money"]
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
        title = font.render("Available Jobs", True, BLACK)
        screen.blit(title, (70, 60))
        
        # Draw jobs
        font = pygame.font.Font(None, 24)
        for i, job in enumerate(self.jobs):
            job_rect = pygame.Rect(70, 80 + i * 50, 360, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, job_rect)
            pygame.draw.rect(screen, BLACK, job_rect, 1)
            
            text = font.render(f"{job['name']} (-{job['energy']} energy, +${job['money']})", True, BLACK)
            screen.blit(text, (80, 90 + i * 50))