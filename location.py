import pygame
from constants import *

class Location:
    def __init__(self, name, x, y, width, height, color=(200, 200, 200), is_enterable=True, interior_color=(240, 240, 240)):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_enterable = is_enterable
        self.interior_color = interior_color
        self.rect = pygame.Rect(x, y, width, height)
        self.interior_walls = []
        self.interior_objects = []
        self.job_button = None
        self.club_button = None
        self.setup_interior()

    def setup_interior(self):
        # Westgate Building
        if self.name == "Westgate Building":
            self.interior_walls = [
                pygame.Rect(100, 100, 200, 20),
                pygame.Rect(100, 100, 20, 200),
                pygame.Rect(400, 200, 200, 20),
                pygame.Rect(400, 200, 20, 200),
            ]
            self.interior_objects = [
                {"name": "Classroom", "rect": pygame.Rect(150, 150, 100, 100), "action": "study"},
                {"name": "Lecture Hall", "rect": pygame.Rect(450, 250, 120, 80), "action": "attend_class"},
                # --- Add Professor's Office Object ---
                {
                    "name": "Professor's Office",
                    "rect": pygame.Rect(500, 400, 100, 80), # Adjust position (x, y) and size (width, height) as needed
                    "color": (200, 180, 220), # Light purple color
                    "action": "professor_office" # Action identifier for event_manager
                }
                # --- End Add ---
            ]
            self.interior_color = (220, 220, 240)
        # HUB-Robeson Center
        elif self.name == "HUB-Robeson Center":
            self.interior_walls = [
                pygame.Rect(100, 100, 600, 20),
                pygame.Rect(100, 100, 20, 400),
                pygame.Rect(700, 100, 20, 400),
                pygame.Rect(100, 500, 620, 20),
            ]
            # Define the club button rect coordinates here for consistency
            club_button_rect_coords = (400, 150, 200, 100)
            self.interior_objects = [
                {"name": "Food Court", "rect": pygame.Rect(150, 150, 200, 150), "action": "eat"},
                {"name": "Bookstore", "rect": pygame.Rect(450, 150, 200, 150), "action": "shop"}, # Adjusted Bookstore rect slightly if needed
                {"name": "Study Area", "rect": pygame.Rect(300, 350, 200, 100), "action": "study"},
                # Add the Club Area object for interaction
                {"name": "Club Area", "rect": pygame.Rect(*club_button_rect_coords), "action": "socialize", "color": PURPLE, "text": "Socialize (Press G)"}
            ]
            self.interior_color = (240, 230, 220)
            # Keep the club_button for drawing the visual element
            self.club_button = pygame.Rect(*club_button_rect_coords)
        # Computer Labs
        elif self.name in ["Computer Lab 1", "Computer Lab 2"]:
            self.interior_walls = [
                pygame.Rect(100, 100, 600, 20),
                pygame.Rect(100, 100, 20, 400),
                pygame.Rect(700, 100, 20, 400),
                pygame.Rect(100, 500, 620, 20),
            ]
            self.interior_objects = [
                {"name": "Computer Station 1", "rect": pygame.Rect(150, 150, 100, 80), "action": "study"},
                {"name": "Computer Station 2", "rect": pygame.Rect(350, 150, 100, 80), "action": "study"},
                {"name": "Computer Station 3", "rect": pygame.Rect(550, 150, 100, 80), "action": "study"},
                {"name": "Study Area", "rect": pygame.Rect(250, 300, 300, 150), "action": "study"}
            ]
            self.interior_color = (180, 200, 220)
        # Dorm Building
        elif self.name == "Dorm Building":
            self.interior_walls = [
                pygame.Rect(100, 100, 600, 20),
                pygame.Rect(100, 100, 20, 400),
                pygame.Rect(700, 100, 20, 400),
                pygame.Rect(100, 500, 620, 20),
                pygame.Rect(350, 100, 20, 150),
                pygame.Rect(450, 250, 20, 250),
            ]
            self.interior_objects = [
                {"name": "Bed", "rect": pygame.Rect(150, 150, 150, 80), "action": "rest"},
                {"name": "Desk", "rect": pygame.Rect(550, 150, 100, 80), "action": "study"},
                {"name": "Couch", "rect": pygame.Rect(200, 350, 200, 100), "action": "rest"},
                {"name": "TV", "rect": pygame.Rect(550, 350, 100, 80), "action": "relax"}
            ]
            self.interior_color = (220, 200, 180)
        # IM Building
        elif self.name == "IM Building":
            self.interior_walls = [
                pygame.Rect(100, 100, 600, 20),
                pygame.Rect(100, 100, 20, 400),
                pygame.Rect(700, 100, 20, 400),
                pygame.Rect(100, 500, 620, 20),
            ]
            self.interior_objects = [
                {
                    "name": "Information Desk",
                    "rect": pygame.Rect(100, 150, 200, 100),
                    "action": "info",
                    "color": (173, 216, 230),
                    "text": "Information Desk (Press Space)"
                },
                {
                    "name": "Job Area",
                    "rect": pygame.Rect(400, 150, 200, 100),
                    "action": "work",
                    "color": (0, 255, 0),
                    "text": "Job"
                }
            ]
            self.interior_color = (200, 240, 200)
            self.job_button = pygame.Rect(400, 150, 200, 100)

    def draw(self, screen, camera):
        # Apply camera offset to the building's rect
        building_rect_on_screen = camera.apply_rect(self.rect)

        # Draw the building rectangle
        pygame.draw.rect(screen, self.color, building_rect_on_screen)
        pygame.draw.rect(screen, BLACK, building_rect_on_screen, 2) # Outline

        # Draw the building name
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=building_rect_on_screen.center)
        screen.blit(text, text_rect)

    def draw_interior(self, screen):
        # Draw walls or basic layout
        wall_thickness = 10
        interior_rect = pygame.Rect(wall_thickness, wall_thickness,
                                    WINDOW_WIDTH - 2 * wall_thickness,
                                    WINDOW_HEIGHT - 2 * wall_thickness - 50) # Adjust for bottom exit prompt
        pygame.draw.rect(screen, self.interior_color, interior_rect) # Fill interior space
        pygame.draw.rect(screen, DARK_GRAY, interior_rect, wall_thickness) # Draw walls

        # Draw interior objects if they exist
        if hasattr(self, 'interior_objects') and self.interior_objects:
            font = pygame.font.Font(None, 24) # Smaller font for object names
            for obj in self.interior_objects:
                obj_rect = pygame.Rect(obj["rect"])
                obj_color = obj.get("color", LIGHT_BLUE) # Default color if not specified
                pygame.draw.rect(screen, obj_color, obj_rect)
                pygame.draw.rect(screen, BLACK, obj_rect, 1) # Outline

                # --- Updated Text Drawing ---
                # Use specific text if provided, otherwise use name
                display_text = obj.get("text", obj["name"])
                text_surface = font.render(display_text, True, BLACK if obj_color != PURPLE else WHITE) # Use white text on purple
                text_rect = text_surface.get_rect(center=obj_rect.center)
                screen.blit(text_surface, text_rect)

        # --- This block is now redundant for drawing the button as it's handled above ---
        # # Draw specific buttons/areas for certain locations
        # if self.name == "HUB-Robeson Center" and self.club_button:
        #     pygame.draw.rect(screen, PURPLE, self.club_button)
        #     font = pygame.font.Font(None, 24)
        #     text = font.render("Clubs", True, WHITE) # Changed text for clarity
        #     text_rect = text.get_rect(center=self.club_button.center)
        #     screen.blit(text, text_rect)
        # elif self.name == "IM Building" and self.job_button:
        #     pygame.draw.rect(screen, GREEN, self.job_button)
        #     font = pygame.font.Font(None, 24)
        #     text = font.render("Jobs", True, BLACK)
        #     text_rect = text.get_rect(center=self.job_button.center)
        #     screen.blit(text, text_rect)