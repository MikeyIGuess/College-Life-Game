import pygame
from constants import *

class Player:
    def __init__(self, x, y, major): # Add 'major' parameter
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = RED
        self.speed = PLAYER_SPEED
        self.energy = STARTING_ENERGY
        self.money = STARTING_MONEY
        # --- Change starting GPA to 2.0 ---
        self.gpa = 2.0
        # --- End Change ---
        # --- Change starting social to 0 ---
        self.social = 0 # Starting social points
        # --- End Change ---
        self.major = major
        self.grades = {} # Initialize grades as an empty dictionary
        self.schedule = {} # Player's class/activity schedule
        self.current_job = None # Track current job
        self.job_performance = 0 # Track job performance
        self.clubs = [] # List of clubs joined
        self.friends_count = 0 # Initialize friend count

    def update(self, world, time_manager): # Added world and time_manager args
        # Store previous position
        prev_x, prev_y = self.x, self.y
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move player based on key presses
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # Keep player within map bounds
        self.x = max(0, min(self.x, MAP_WIDTH - 32))
        self.y = max(0, min(self.y, MAP_HEIGHT - 32))
        
        # Update player rectangle
        self.rect.topleft = (self.x, self.y)
        
        # Check for collisions with buildings
        collision_detected = False
        for location in world.locations.values():
            if self.rect.colliderect(location.rect):
                # Check if player is trying to enter through the entrance
                is_at_entrance = (location.is_enterable and 
                                 self.x + 16 > location.x + location.width//2 - 15 and
                                 self.x + 16 < location.x + location.width//2 + 15 and
                                 self.y + 16 > location.y + location.height - 20)
                
                # If not at entrance, mark collision
                if not is_at_entrance:
                    collision_detected = True
        
        # If collision detected and not at entrance, revert position
        if collision_detected:
            self.x, self.y = prev_x, prev_y
            self.rect.topleft = (self.x, self.y)
    
    def update_interior(self, current_building):
        # Store previous position
        prev_x, prev_y = self.x, self.y
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move player based on key presses
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # Keep player within building bounds
        self.x = max(50, min(self.x, WINDOW_WIDTH - 50))
        self.y = max(100, min(self.y, WINDOW_HEIGHT - 50))
        
        # Update player rectangle
        self.rect.topleft = (self.x, self.y)
        
        # Check for collisions with interior walls if they exist
        if hasattr(current_building, 'interior_walls'):
            # Store previous position in case of collision
            prev_x, prev_y = self.x, self.y
            
            # Check collision with each wall
            for wall in current_building.interior_walls:
                if self.rect.colliderect(wall):
                    # Collision detected, revert position
                    self.x, self.y = prev_x, prev_y
                    self.rect.topleft = (self.x, self.y)
                    break
    
    def draw(self, screen, camera):
        # Apply camera offset to get the player's drawing rectangle on the screen
        player_rect_on_screen = camera.apply_rect(self.rect)

        # Draw the player (e.g., as a circle) using the center of the *new* rectangle
        # Ensure the center coordinates are integers for drawing
        center_pos = (int(player_rect_on_screen.centerx), int(player_rect_on_screen.centery))
        pygame.draw.circle(screen, BLUE, center_pos, 16) # Use the calculated rect's center

    def draw_interior(self, screen):
        # Draw player inside buildings (no camera offset)
        # Ensure the coordinates are integers for drawing
        # Assuming self.x/self.y represent the top-left, calculate center
        # If self.x/self.y are already center, just use them. Adjust as needed.
        center_x = int(self.rect.centerx)
        center_y = int(self.rect.centery)
        pygame.draw.circle(screen, BLUE, (center_x, center_y), 16)

    def add_friend(self):
        # Placeholder: Add friend to self.friends_list
        self.friends_count += 1

    def apply_job_effects(self, hours):
        # Placeholder: Apply job effects
        self.energy -= hours * self.speed

    def join_club(self, club_name):
        # Placeholder: Join club to self.clubs_list
        self.clubs.append(club_name)

    def calculate_gpa(self):
        # Calculate overall GPA from self.grades
        if self.grades:
            # Calculate the average of all grades in the dictionary
            self.gpa = sum(self.grades.values()) / len(self.grades)
            # Clamp overall GPA just in case
            self.gpa = max(0.0, min(4.0, self.gpa))
        else:
            # If no grades yet, keep the initial GPA or set a default
            # self.gpa = 2.0 # Or keep the value set in __init__
            pass # Keep initial GPA if no grades exist
        return self.gpa # Return the calculated GPA

    def update_grade(self, subject, change):
        # Update a specific grade and recalculate GPA
        if subject not in self.grades:
            self.grades[subject] = 0.0 # Initialize if not present
        self.grades[subject] += change
        # Clamp grade between 0.0 and 4.0 (or your desired range)
        self.grades[subject] = max(0.0, min(4.0, self.grades[subject]))
        # Recalculate overall GPA
        self.calculate_gpa() # Call the updated method