# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
STARTING_ENERGY = 100
STARTING_MONEY = 100
ENERGY_DECAY_RATE = 0.1
STUDY_ENERGY_COST = 20
SOCIAL_ENERGY_COST = 10

# Locations
LOCATIONS = {
    "dorm": {"x": 100, "y": 100},
    "classroom": {"x": 300, "y": 100},
    "library": {"x": 500, "y": 100},
    "cafeteria": {"x": 300, "y": 300},
    "gym": {"x": 100, "y": 500},
    "club_room": {"x": 500, "y": 500}
}

# Majors
MAJORS = [
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

# Add these new constants
# Update map dimensions to be smaller
MAP_WIDTH = 1200   # Reduced from 2000
MAP_HEIGHT = 900   # Reduced from 1500