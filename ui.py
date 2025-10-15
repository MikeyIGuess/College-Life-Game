import pygame
from constants import *

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 30) # Default font

    def draw_player_stats(self, screen, player, time_manager):
        # Display Time and Day
        day_str = time_manager.get_day_of_week()
        time_str = time_manager.get_formatted_time()
        time_text = self.font.render(f"Day {time_manager.day} ({day_str}) {time_str}", True, BLACK)
        screen.blit(time_text, (10, 10))

        # Display Player Stats
        energy_text = self.font.render(f"Energy: {player.energy}", True, BLACK)
        money_text = self.font.render(f"Money: ${player.money}", True, BLACK)
        gpa_text = self.font.render(f"GPA: {player.gpa:.2f}", True, BLACK)
        social_text = self.font.render(f"Social: {player.social}", True, BLACK)
        # --- Modify Friend Counter Display ---
        friends_text = self.font.render(f"Friends: {player.friends_count} / 5", True, BLACK)
        # --- End Modify ---

        screen.blit(energy_text, (10, 40))
        screen.blit(money_text, (10, 70))
        screen.blit(gpa_text, (10, 100))
        screen.blit(social_text, (10, 130))
        screen.blit(friends_text, (10, 160)) # Adjust Y position if needed

    def draw_message(self, screen, message):
        # Render the string message into a text surface
        if message and isinstance(message, str): # Check if message is a non-empty string
            text_surface = self.font.render(message, True, BLACK) # Render the text
            screen.blit(text_surface, (10, WINDOW_HEIGHT - 40)) # Blit the surface (Adjust Y position if needed)
        # If message is not a string or is empty, do nothing or handle differently