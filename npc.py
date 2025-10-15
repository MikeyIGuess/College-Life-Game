import pygame
from constants import *
import random

class NPC:
    def __init__(self, x, y, name="NPC", color=BLUE, dialogue=None, schedule=None, major="Undecided"): # Add major parameter with default
        self.name = name
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.dialogue = dialogue if dialogue else [f"Hello, I'm {self.name}.", "Nice weather today."]
        self.dialogue_index = 0
        self.schedule = schedule # Optional: Define movement patterns
        self.target_pos = None # For movement
        self.move_timer = 0
        self.friendship = 0 # Track player friendship
        self.major = major # Assign the major
        # --- Add location tracking ---
        self.current_location_name = None # None means outside in the world, otherwise stores building name
        # --- End add ---

    def update(self, time_manager):
        # Placeholder for NPC movement or other updates
        # If NPCs move, update self.rect here:
        # self.rect.center = (self.x, self.y)
        # Reset talked status at the start of a new day
        # This might need adjustment based on how TimeManager signals a new day
        pass # Currently handled by World calling reset_daily

    # --- Add Interior Update Method ---
    def update_interior(self, time_manager):
        # Placeholder for any updates needed while inside a building
        # e.g., pathfinding within the interior, specific interactions
        pass
    # --- End Add ---

    def draw(self, screen, camera):
        # Apply camera offset to the NPC's rect
        npc_rect_on_screen = camera.apply_rect(self.rect)

        # Draw the NPC using the offset rect
        pygame.draw.rect(screen, self.color, npc_rect_on_screen) # Example drawing

        # Optionally draw name/major near the offset rect
        font = pygame.font.Font(None, 18)
        name_text = font.render(self.name, True, BLACK)
        name_rect = name_text.get_rect(centerx=npc_rect_on_screen.centerx, bottom=npc_rect_on_screen.top - 2)
        screen.blit(name_text, name_rect)

    # --- Add Interior Draw Method ---
    def draw_interior(self, screen):
        # Draw the NPC directly using its rect (no camera offset)
        pygame.draw.rect(screen, self.color, self.rect) # Example drawing

        # Optionally draw name/major near the rect (no offset)
        font = pygame.font.Font(None, 18)
        name_text = font.render(self.name, True, BLACK)
        name_rect = name_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 2)
        screen.blit(name_text, name_rect)
    # --- End Add ---

    def interact(self, player):
        # Interaction logic - Now self.major exists
        return f"Hello, I'm {self.name}, studying {self.major}."

    def reset_daily(self):
        # Reset daily interaction flags if any
        pass

# Make sure npc.py exists and is imported correctly in world.py