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
        menu_rect = pygame.Rect(WINDOW_WIDTH - 420, 20, 400, 300)
        if not menu_rect.collidepoint(pos):
            return False
            
        # Calculate job button positions and check clicks
        for i, job in enumerate(self.jobs):
            job_rect = pygame.Rect(WINDOW_WIDTH - 400, 50 + i * 50, 360, 40)
            if job_rect.collidepoint(pos):
                self.take_job(i)
                return True
        return False
        
    def take_job(self, index):
        if index < 0 or index >= len(self.jobs):
            return False, "Invalid job selection"
            
        job = self.jobs[index]
        if self.player.energy < job["energy"]:
            return False, "Not enough energy for this job"
            
        # Apply job effects
        self.player.energy -= job["energy"]
        self.player.money += job["money"]
        return True, f"Worked as {job['name']} and earned ${job['money']}"
        
    def draw(self, screen, x, y, width, height):
        if not self.visible:
            # Draw just the button
            button_rect = pygame.Rect(x, y, width, 40)
            pygame.draw.rect(screen, GREEN, button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Jobs", True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            return
            
        # Draw menu background
        menu_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 2)
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title = font.render("Available Jobs", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        # Draw jobs
        for i, job in enumerate(self.jobs):
            job_rect = pygame.Rect(x + 20, y + 50 + i * 50, width - 40, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, job_rect)
            pygame.draw.rect(screen, BLACK, job_rect, 1)
            
            text = font.render(f"{job['name']} (-{job['energy']} energy, +${job['money']})", True, BLACK)
            screen.blit(text, (x + 30, y + 60 + i * 50))

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
        menu_rect = pygame.Rect(WINDOW_WIDTH - 420, 20, 400, 300)
        if not menu_rect.collidepoint(pos):
            return False
            
        # Calculate club button positions and check clicks
        for i, club in enumerate(self.clubs):
            club_rect = pygame.Rect(WINDOW_WIDTH - 400, 50 + i * 50, 360, 40)
            if club_rect.collidepoint(pos):
                self.join_club(i)
                return True
        return False
        
    def join_club(self, index):
        if index < 0 or index >= len(self.clubs):
            return False, "Invalid club selection"
            
        club = self.clubs[index]
        if self.player.energy < club["energy"]:
            return False, "Not enough energy to participate"
            
        # Apply club effects
        self.player.energy -= club["energy"]
        self.player.social += club["social"]
        return True, f"Participated in {club['name']} and gained {club['social']} social points"
        
    def draw(self, screen, x, y, width, height):
        if not self.visible:
            # Draw just the button
            button_rect = pygame.Rect(x, y, width, 40)
            pygame.draw.rect(screen, PURPLE, button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Clubs", True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            return
            
        # Draw menu background
        menu_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 2)
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title = font.render("Available Clubs", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        # Draw clubs
        for i, club in enumerate(self.clubs):
            club_rect = pygame.Rect(x + 20, y + 50 + i * 50, width - 40, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, club_rect)
            pygame.draw.rect(screen, BLACK, club_rect, 1)
            
            text = font.render(f"{club['name']} (-{club['energy']} energy, +{club['social']} social)", True, BLACK)
            screen.blit(text, (x + 30, y + 60 + i * 50))