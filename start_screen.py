import pygame
from constants import *

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.selected_major = 0
        self.majors = [
            "Computer Science",
            "Software Engineering",
            "Computer Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Data Science",
            "Information Technology",
            "Cybersecurity",
            "Game Development",
            "Robotics Engineering"
        ]
        self.controls_text = [
            "Contact the PSU Office of the Dean for Undergraduate",
            "Education to ask for more in-person options.",
            "Speak Up. Get involved. Make campus feel like campus again.",
            "Arrow Keys - Move",
            "G - Interact",
            "F - Enter Locations",
            "",
            "Goal:",
            "Find 5 friends in your major!",
            "Keep your GPA High",
            "",
            "Press ENTER to start"
        ]
        
    def draw(self):
        self.screen.fill(WHITE)
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)
        
        # Title
        title = font.render("Campus Connect", True, BLUE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)

        
        # Display current major
        current = small_font.render(f"> {self.majors[self.selected_major]} <", True, BLUE)
        current_rect = current.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(current, current_rect)
        
        # Controls and instructions
        for i, text in enumerate(self.controls_text):
            line = small_font.render(text, True, BLACK)
            rect = line.get_rect(center=(WINDOW_WIDTH//2, 300 + i*30))
            self.screen.blit(line, rect)
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Add F key handling
                if self.selected_major:  # Only proceed if a major is selected
                    return self.selected_major
            if event.key == pygame.K_LEFT:
                self.selected_major = (self.selected_major - 1) % len(self.majors)
            elif event.key == pygame.K_RIGHT:
                self.selected_major = (self.selected_major + 1) % len(self.majors)
            elif event.key == pygame.K_RETURN:
                return self.majors[self.selected_major]
        return None