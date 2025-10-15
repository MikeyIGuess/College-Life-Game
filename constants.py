import pygame

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128) # Add this line for medium gray
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)

# --- Game Settings ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# --- Map Settings ---
# Adjust these dimensions based on your actual map size
MAP_WIDTH = 2000
MAP_HEIGHT = 1500
TILE_SIZE = 32 # Example tile size

# --- Player Settings ---
PLAYER_SPEED = 5
STARTING_ENERGY = 100
STARTING_MONEY = 50

# --- Add LOCATIONS_DATA Definition ---
LOCATIONS_DATA = {
    "Westgate Building": {
        "rect": pygame.Rect(100, 100, 200, 150), # x, y, width, height
        "color": (180, 180, 200),
        "is_enterable": True,
        "interior_color": (220, 220, 240)
        # Add interior setup details if needed, matching Location class
    },
    "HUB-Robeson Center": {
        "rect": pygame.Rect(400, 300, 300, 200),
        "color": (200, 180, 180),
        "is_enterable": True,
        "interior_color": (240, 230, 220)
    },
    "Computer Lab 1": {
        "rect": pygame.Rect(700, 100, 150, 100),
        "color": (180, 200, 180),
        "is_enterable": True,
        "interior_color": (180, 200, 220)
    },
    "Computer Lab 2": {
        "rect": pygame.Rect(700, 500, 150, 100),
        "color": (180, 200, 180),
        "is_enterable": True,
        "interior_color": (180, 200, 220)
    },
    "Dorm Building": {
        "rect": pygame.Rect(100, 600, 250, 180),
        "color": (200, 200, 160),
        "is_enterable": True,
        "interior_color": (220, 200, 180)
    },
    "IM Building": {
        "rect": pygame.Rect(500, 650, 200, 150),
        "color": (160, 200, 160),
        "is_enterable": True,
        "interior_color": (200, 240, 200)
    },
    # Add other locations as needed
}
# --- End LOCATIONS_DATA Definition ---

# You might have other constants defined here already...