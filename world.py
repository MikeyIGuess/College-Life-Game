import pygame
import random
from constants import *
from npc import NPC
from location import Location

class World:
    def __init__(self):
        self.npcs = []
        self.locations = {}
        self.initialize_world()
        self.academic_event_timer = 0
        self.current_academic_event = None
        
    def initialize_world(self):
        # Spread locations across the smaller map
        locations_pos = {
            "dorm": {"x": 100, "y": 100},
            "classroom": {"x": 400, "y": 150},
            "library": {"x": 700, "y": 200},
            "cafeteria": {"x": 250, "y": 400},
            "gym": {"x": 500, "y": 600},
            "club_room": {"x": 900, "y": 500}
        }
        
        # Create locations with proper sprites
        for name, pos in locations_pos.items():
            self.locations[name] = Location(name, pos["x"], pos["y"])
            
        # Create NPCs within smaller bounds
        for _ in range(5):
            x = random.randint(50, MAP_WIDTH - 82)
            y = random.randint(50, MAP_HEIGHT - 82)
            major = random.choice(MAJORS)
            self.npcs.append(NPC(x, y, major))
            
    def generate_academic_event(self):
        event_types = [
            {"type": "Pop Quiz", "difficulty": 0.3},
            {"type": "Midterm", "difficulty": 0.5},
            {"type": "Project Due", "difficulty": 0.4},
            {"type": "Final Exam", "difficulty": 0.7}
        ]
        return random.choice(event_types)
        
    def update(self, time_manager):
        for npc in self.npcs:
            npc.update(time_manager)
            
        # Handle academic events
        if time_manager.hour >= 8 and time_manager.hour <= 16:  # School hours
            if random.random() < 0.001 and not self.current_academic_event:  # Small chance each update
                self.current_academic_event = self.generate_academic_event()
                return f"Surprise! {self.current_academic_event['type']}!"
                
    def handle_academic_event(self, player):
        if self.current_academic_event:
            difficulty = self.current_academic_event['difficulty']
            success_chance = (player.grades[player.major] / 4.0) - difficulty
            
            if random.random() < success_chance:
                player.grades[player.major] += 0.1
                self.current_academic_event = None
                return f"You passed the {self.current_academic_event['type']}! GPA increased!"
            else:
                player.grades[player.major] -= 0.2
                self.current_academic_event = None
                return f"You struggled with the {self.current_academic_event['type']}. GPA decreased..."
            
    def draw(self, screen, camera):
        # Draw locations with camera offset
        for location in self.locations.values():
            location_rect = camera.apply(location)
            pygame.draw.rect(screen, location.color, location_rect)
            
            # Only draw text if location is on screen
            if screen.get_rect().colliderect(location_rect):
                font = pygame.font.Font(None, 20)
                text = font.render(location.name, True, BLACK)
                text_rect = text.get_rect(center=(location_rect.x + 32, location_rect.y + 32))
                screen.blit(text, text_rect)
        
        # Draw NPCs with camera offset
        for npc in self.npcs:
            npc_rect = camera.apply(npc)
            if screen.get_rect().colliderect(npc_rect):
                pygame.draw.circle(screen, npc.color, (npc_rect.x + 16, npc_rect.y + 16), 16)