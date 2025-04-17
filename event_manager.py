import pygame
from constants import *

class EventManager:
    def __init__(self):
        self.current_event = None
        self.message = ""
        self.message_timer = 0
        
    def handle_event(self, event, player, world):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.handle_interaction(player, world)
            elif event.key == pygame.K_e:
                self.handle_location_action(player, world)
                
    def handle_interaction(self, player, world):
        # Check for NPCs nearby
        for npc in world.npcs:
            if player.rect.colliderect(npc.rect):
                self.message = player.interact_with_npc(npc)
                self.message_timer = 180  # Show message for 3 seconds
                
    def handle_location_action(self, player, world):
        for location in world.locations.values():
            if player.rect.colliderect(location.rect):
                location.perform_action(player)
                
    def handle_events(self):
        # Handle academic events
        event_message = self.world.update(self.time_manager)
        if event_message:
            self.message = event_message
            self.message_timer = 180
            
        if self.world.current_academic_event:
            self.message = self.world.handle_academic_event(self.player)
            self.message_timer = 180
    def draw(self, screen):
        if self.message and self.message_timer > 0:
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 50))
            screen.blit(text, text_rect)
            self.message_timer -= 1