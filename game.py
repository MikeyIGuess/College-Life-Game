import pygame
# --- Add GRAY to this import ---
from constants import *
from constants import LOCATIONS_DATA, GRAY # Add GRAY here
# --- End Add ---
from camera import Camera
from player import Player
from world import World # Ensure it imports from world.py
from ui import UI
from time_manager import TimeManager
from event_manager import EventManager
from start_screen import StartScreen
from canvas import Canvas
from job_menu import JobMenu
from club_menu import ClubMenu
import textwrap # Import textwrap for multi-line text

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Campus Connect")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'main_menu'  # Start at main menu
        self.game_started = False
        self.job_menu = None
        self.club_menu = None
        # --- Add initialization for end screen flag ---
        self.show_end_screen = False # Initialize the flag here
        # --- End Add ---

        # Initialize start screen
        self.start_screen = StartScreen(self.screen)

        # Initialize camera with map size
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)
        
        # Set all game components to None initially
        self.time_manager = None
        self.world = None
        self.player = None
        self.ui = None
        self.event_manager = None
        self.canvas = None
        self.current_building = None

    def initialize_game(self, selected_major):
        # Initialize game components here
        # --- First, initialize time_manager ---
        self.time_manager = TimeManager()
        # --- Then, pass it to World ---
        self.world = World(LOCATIONS_DATA, self.time_manager) # Pass the time_manager
        # --- End Modify ---

        # --- Set Player Start Position near Dorm ---
        # Find Dorm Building coordinates (adjust if necessary based on constants.py)
        dorm_rect = LOCATIONS_DATA.get("Dorm Building", {}).get("rect")
        if dorm_rect:
            # Start near the bottom-center entrance of the dorm
            start_x = dorm_rect.centerx
            start_y = dorm_rect.bottom - 40 # Slightly above the bottom edge
        else:
            # Fallback if Dorm Building data isn't found
            start_x = MAP_WIDTH // 2
            start_y = MAP_HEIGHT // 2

        self.player = Player(start_x, start_y, selected_major)
        # --- End change ---

        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT) # Use MAP dimensions for camera bounds
        # self.time_manager = TimeManager() # Moved up
        self.event_manager = EventManager()
        self.ui = UI()
        self.canvas = Canvas(self.player, self) # Pass 'self' (the game instance)
        self.job_menu = JobMenu(self.player) # Pass player reference
        self.club_menu = ClubMenu(self.player) # Pass player reference

        # Pass references to event manager
        self.event_manager.set_references(self.world, self.player, self.time_manager) # Pass references
        # --- Also pass world reference to time_manager if needed ---
        self.time_manager.set_references(self.world)

        # Set game as started and change state to world
        self.game_started = True
        self.game_state = 'world'

    def enter_building(self, building):
        if building.is_enterable:
            self.game_state = 'inside_building'
            self.current_building = building
            # Save player's outside position
            self.player.outside_pos = (self.player.x, self.player.y)
            # Place player at building entrance
            self.player.x = WINDOW_WIDTH // 2
            self.player.y = WINDOW_HEIGHT - 100
            self.player.rect.topleft = (self.player.x, self.player.y)

    def exit_building(self):
        if self.game_state == 'inside_building':
            self.game_state = 'world'
            # Restore player's position outside
            if hasattr(self.player, 'outside_pos'):
                self.player.x, self.player.y = self.player.outside_pos
            self.player.rect.topleft = (self.player.x, self.player.y)
            self.current_building = None

    def update(self, dt): # Add dt parameter here
        if not self.game_started:
            return # Don't update game logic if on start screen

        if self.game_state == 'world':
            # Pass the world and time_manager objects to player update
            self.player.update(self.world, self.time_manager) # Ensure this line exists and passes args
            # --- Fix: Remove the time_manager argument ---
            self.world.update()
            # --- End Fix ---
            self.time_manager.update(dt) # Pass dt here
            self.camera.update(self.player)

        elif self.game_state == 'inside_building' and self.current_building is not None:
            # Pass current_building to interior update
            self.player.update_interior(self.current_building) # Ensure this line exists
            self.time_manager.update(dt) # Pass dt here
            # --- Add: Update NPCs inside the current building ---
            npcs_inside = self.world.get_npcs_in_building(self.current_building.name)
            for npc in npcs_inside:
                npc.update_interior(self.time_manager) # Call the new interior update method
            # --- End Add ---

        # Update Canvas if it exists and is visible
        # if self.canvas and self.canvas.visible: # Remove this block
        #     self.canvas.update()               # Remove this block

        # Update UI elements if they exist
        # if self.ui:
        #     self.ui.update() # Remove this line if UI class has no update method

        # Update Canvas if it exists
        # Note: Canvas updates related to new_day should be triggered differently,
        # perhaps via a scheduled event in TimeManager or a direct call when day changes.
        if self.canvas: # Check if canvas exists
             # If canvas needs per-frame updates, add:
             # self.canvas.update()
             # Check for new day and update canvas (consider moving this logic)
             if self.time_manager.day > self.canvas.last_checked_day:
                 self.canvas.new_day(self.time_manager.day)


        # Remove the redundant update block below
        # # Update game components based on game state - This block seems redundant
        # # as player and world updates are already handled above based on game_state.
        # # Consider removing this redundant block.
        # if self.game_state == 'world':  # Changed from 'playing' to 'world'
        #     # self.world.update(self.time_manager) # Redundant world update?
        #     # self.player.update(self.world, self.time_manager) # Redundant player update?
        #     # self.camera.update(self.player) # Moved up
        #     # self.event_manager.handle_events() # handle_events is called in run loop, not here
        # elif self.game_state == 'inside_building':
        #     # Update player movement inside building
        #     # self.player.update_interior(self.current_building) # Redundant interior update?

    def draw_interior(self):
        self.screen.fill(self.current_building.interior_color)

        # Draw interior features (walls, objects)
        self.current_building.draw_interior(self.screen)

        # Draw building name
        font = pygame.font.Font(None, 48)
        text = font.render(f"{self.current_building.name}", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(text, text_rect)

        # Draw exit prompt
        small_font = pygame.font.Font(None, 36)
        exit_text = small_font.render("Press 'F' to Exit", True, BLACK)
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(exit_text, exit_rect)

        # Draw player (no camera offset needed inside)
        self.player.draw_interior(self.screen) # Use the interior draw method

        # --- Add: Draw NPCs inside the current building ---
        npcs_inside = self.world.get_npcs_in_building(self.current_building.name)
        for npc in npcs_inside:
            npc.draw_interior(self.screen) # Call the new interior draw method
        # --- End Add ---

        # Draw UI (Stats, Time) - Pass self.screen
        if self.ui:
            self.ui.draw_player_stats(self.screen, self.player, self.time_manager) # Pass self.screen

        # Draw Event Manager UI (Messages and Menus)
        if self.event_manager:
            self.event_manager.draw(self.screen)

        # Draw Job Menu if visible
        if self.job_menu and self.job_menu.visible:
            self.job_menu.draw(self.screen)

        # Draw Club Menu if visible
        if self.club_menu and self.club_menu.visible:
            self.club_menu.draw(self.screen)

        # Draw Canvas if visible and in a valid building
        # Check visibility *before* calling draw_panel
        if self.canvas and self.canvas.visible and self.current_building.name in ["Computer Lab 1", "Computer Lab 2", "Dorm Building"]:
             # Define position/size for the panel
             canvas_width = 400 # Or get from constants/canvas object
             canvas_height = 300 # Or get from constants/canvas object
             canvas_x = WINDOW_WIDTH - canvas_width - 20
             canvas_y = 20
             # Call draw with position and size arguments
             self.canvas.draw(self.screen, canvas_x, canvas_y, canvas_width, canvas_height)
        elif self.canvas and self.current_building.name in ["Computer Lab 1", "Computer Lab 2", "Dorm Building"]:
             # If canvas exists for this building but isn't visible, draw just the button
             # Provide dummy args as the method handles drawing only the button
             self.canvas.draw(self.screen, 0, 0, 0, 0)


    # --- Add method to trigger the end screen ---
    # --- Ensure trigger_end_screen method exists ---
    def trigger_end_screen(self):
        """Sets the flag and state to show the end screen."""
        self.show_end_screen = True
        self.game_state = 'end' # Change game state to 'end'
    # --- End ensure ---

    def run(self):
        while self.running:
            # --- Check for end screen state FIRST ---
            if self.show_end_screen:
                # Handle minimal events (just quit) in the end screen state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    # Optional: Allow closing with ESC key
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False

                # Draw the end screen and update display
                self.draw_end_screen()
                pygame.display.flip()
                continue # IMPORTANT: Skip the rest of the normal game loop
            # --- End check ---

            # --- Normal game loop logic ---
            dt = self.clock.tick(FPS) / 1000.0

            if not self.game_started: # Main Menu state
                self.handle_events()
                self.draw()
            else: # Game is running (world, inside, etc.)
                self.handle_events()
                # Update only if not ending (redundant due to check above, but safe)
                if not self.show_end_screen:
                    self.update(dt)
                self.draw()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle start screen input first if not started
            # --- Change: Check game_state instead of game_started ---
            elif self.game_state == 'main_menu':
            # --- End Change ---
                selected_major = self.start_screen.handle_input(event)
                if selected_major:
                    self.initialize_game(selected_major)
                continue # Don't process other events if on start screen

            # Handle events based on game state (pass event to event_manager)
            elif self.game_state == 'world':
                 if self.event_manager:
                    self.event_manager.handle_world_event(event, self.player, self.world, self)
            elif self.game_state == 'inside_building' and self.current_building is not None:
                 if self.event_manager:
                    self.event_manager.handle_interior_event(event, self)

    def draw_world(self):
        # Fill background
        self.screen.fill(WHITE)

        # Draw locations (buildings) relative to camera
        for location in self.world.locations.values():
            location.draw(self.screen, self.camera)

        # Draw NPCs relative to camera
        for npc in self.world.all_npcs:
            if npc.current_location_name is None: # Only draw NPCs in the world
                npc.draw(self.screen, self.camera)

        # Draw player relative to camera
        self.player.draw(self.screen, self.camera)

        # Draw UI elements (stats, messages) - Fixed Method Call
        # --- Fix: Call draw_player_stats instead of draw ---
        self.ui.draw_player_stats(self.screen, self.player, self.time_manager)
        # --- End Fix ---
        if self.event_manager.message_timer > 0:
            self.ui.draw_message(self.screen, self.event_manager.message)

        # Draw Event Manager UI (Messages)
        if self.event_manager:
            self.event_manager.draw(self.screen)

        # Draw Canvas button (panel only drawn if visible, which shouldn't happen in world view)
        if self.canvas:
            # Provide dummy args; draw method handles visibility check internally
            self.canvas.draw(self.screen, 0, 0, 0, 0)
    # --- End of added method ---
    def draw(self):
        # --- Check for end screen state (again, redundant but safe) ---
        if self.show_end_screen:
            self.draw_end_screen()
            return
        # --- End check ---

        # --- Normal drawing logic based on game_state ---
        if self.game_state == 'main_menu':
            self.start_screen.draw()
        # --- End Add ---
        elif self.game_state == 'start': # Keep this if 'start' is used elsewhere, otherwise review
            self.draw_world()
        elif self.game_state == 'world':
            self.draw_world()
        elif self.game_state == 'inside_building':
            self.draw_interior()
        elif self.game_state == 'canvas':
             self.draw_canvas() # Assuming you have this method

        # Draw Event Manager UI (Messages, Menus) on top if game started
        if self.event_manager and self.game_started:
             self.event_manager.draw(self.screen)

        # Draw other UI elements like Job Menu, Club Menu if visible and game started
        if self.job_menu and self.job_menu.visible and self.game_started:
            self.job_menu.draw(self.screen)
        if self.club_menu and self.club_menu.visible and self.game_started:
            self.club_menu.draw(self.screen)

    # --- Add method to draw the end screen ---
    def draw_end_screen(self):
        """Draws the final advocacy message screen."""
        self.screen.fill(WHITE) # White background

        # Define fonts
        font_title = pygame.font.Font(None, 48)
        font_body = pygame.font.Font(None, 28)
        font_link = pygame.font.Font(None, 26) # Slightly smaller for link
        font_small = pygame.font.Font(None, 22) # For exit instruction

        # Title
        title_text = "Thank You for Playing Campus Connect"
        title_surface = font_title.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title_surface, title_rect)

        # Main message body - Use textwrap for formatting
        body_lines_raw = [
            "If you felt disconnected, overwhelmed, or frustrated during this game, you’re not alone.",
            "Many students at Penn State are experiencing",
            "the same struggles due to the overuse of online classes.",
            " ", # Blank line for spacing
            "You can help advocate for change. Contact the Office of the",
            "Vice President and Dean for Undergraduate Education and let them know how online",
            "classes have impacted your college experience.",
            "Share your story, ask for more in-person options, and be part of the solution.",
            " ", # Blank line
            "Learn more and take action:"
        ]
        link_text = "https://undergrad.psu.edu/contact-us.html"
        final_line = "Your voice matters."

        # Wrap and draw body text
        max_width_pixels = WINDOW_WIDTH - 100 # Max width for text wrapping in pixels
        # Estimate characters per line (adjust based on font/size)
        chars_per_line_est = 85
        current_y = title_rect.bottom + 40

        for line_raw in body_lines_raw:
            if line_raw == " ": # Handle blank lines
                current_y += 15 # Add smaller space for blank lines
                continue

            # Wrap the raw line based on estimated character width
            wrapped_lines = textwrap.wrap(line_raw, width=chars_per_line_est)
            for line in wrapped_lines:
                body_surface = font_body.render(line, True, BLACK)
                # Center each wrapped line
                body_rect = body_surface.get_rect(center=(WINDOW_WIDTH // 2, current_y))
                self.screen.blit(body_surface, body_rect)
                current_y += 30 # Line spacing

        # Draw the link (make it look clickable)
        link_surface = font_link.render(link_text, True, BLUE) # Blue color for link
        link_rect = link_surface.get_rect(center=(WINDOW_WIDTH // 2, current_y + 10))
        self.screen.blit(link_surface, link_rect)
        # Optional: Underline the link
        # pygame.draw.line(self.screen, BLUE, link_rect.bottomleft, link_rect.bottomright, 1)

        # Draw the final line
        final_surface = font_body.render(final_line, True, BLACK)
        final_rect = final_surface.get_rect(center=(WINDOW_WIDTH // 2, link_rect.bottom + 40))
        self.screen.blit(final_surface, final_rect)

        # Instruction to close
        close_text = "Press ESC or close the window to exit."
        close_surface = font_small.render(close_text, True, GRAY) # Use the imported GRAY
        close_rect = close_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(close_surface, close_rect)
    # --- End add method ---