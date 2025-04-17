import pygame
from constants import *
from player import Player
from world import World
from ui import UI
from event_manager import EventManager
from time_manager import TimeManager
from start_screen import StartScreen
from camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Campus Connect")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False
        
        # Start screen
        self.start_screen = StartScreen(self.screen)
        
        # Create camera
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)
        
        # Game components will be initialized after major selection
        self.time_manager = None
        self.world = None
        self.player = None
        self.ui = None
        self.event_manager = None

    def initialize_game(self, selected_major):
        self.time_manager = TimeManager()
        self.world = World()
        self.player = Player(selected_major)  # Pass selected major to Player
        self.ui = UI(self.screen)
        self.event_manager = EventManager()
        self.game_started = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif not self.game_started:
                selected_major = self.start_screen.handle_input(event)
                if selected_major:
                    self.initialize_game(selected_major)
            else:
                self.event_manager.handle_event(event, self.player, self.world)

    def draw(self):
        if not self.game_started:
            self.start_screen.draw()
        else:
            self.screen.fill(WHITE)
            
            # Draw world with camera offset
            self.world.draw(self.screen, self.camera)
            
            # Draw player relative to camera
            player_rect = self.camera.apply(self.player)
            pygame.draw.circle(self.screen, BLUE, (player_rect.x + 16, player_rect.y + 16), 16)
            
            # Update UI
            self.ui.draw(self.player, self.time_manager)
            self.event_manager.draw(self.screen)
        pygame.display.flip()

    def update(self):
        if self.game_started:
            self.time_manager.update()
            self.world.update(self.time_manager)
            self.player.update(self.world, self.time_manager)
            self.camera.update(self.player)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)