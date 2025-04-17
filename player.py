import pygame
from constants import *

class Player:
    def __init__(self, selected_major):  # Add selected_major parameter
        self.energy = STARTING_ENERGY
        self.money = STARTING_MONEY
        self.grades = {major: 3.0 for major in MAJORS}
        self.friends = []
        self.social_points = 0
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.major = selected_major  # Use the selected major
        self.facing = 'down'
        self.moving = False
        self.major_friends_goal = 0  # Track progress towards 5 friends
        self.major_friends_needed = 5  # Goal to reach

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Keep player within strict map bounds
        if 0 <= new_x <= MAP_WIDTH - self.rect.width:
            self.x = new_x
        if 0 <= new_y <= MAP_HEIGHT - self.rect.height:
            self.y = new_y
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self, world, time_manager):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        
        if dx != 0 or dy != 0:
            self.move(dx, dy)
            self.moving = True
            if dx > 0: self.facing = 'right'
            elif dx < 0: self.facing = 'left'
            elif dy > 0: self.facing = 'down'
            elif dy < 0: self.facing = 'up'
        else:
            self.moving = False

    def draw(self, screen):
        # Draw player as a colored circle with a direction indicator
        pygame.draw.circle(screen, BLUE, (self.x + 16, self.y + 16), 16)
        
        # Draw direction indicator
        indicator_pos = {
            'right': (self.x + 24, self.y + 16),
            'left': (self.x + 8, self.y + 16),
            'down': (self.x + 16, self.y + 24),
            'up': (self.x + 16, self.y + 8)
        }
        pygame.draw.circle(screen, RED, indicator_pos[self.facing], 4)

    def study(self, subject):
        if self.energy >= 30:  # Check if player has enough energy
            self.energy -= 30
            self.grades[subject] += 0.2  # Improve grades in the subject
            self.social_points -= 5  # Studying reduces social points
            
    def work_part_time(self):
        if self.energy >= 40:
            self.energy -= 40
            self.money += 30
            self.social_points -= 3
            
    def tutor_students(self):
        if self.energy >= 25 and any(grade >= 3.5 for grade in self.grades.values()):
            self.energy -= 25
            self.money += 40
            self.social_points += 2

    def interact_with_npc(self, npc):
        if not npc.talked_today:
            message = npc.interact(self)
            if npc.major == self.major:
                self.social_points += 10
                self.major_friends_goal += 1
                if self.major_friends_goal >= self.major_friends_needed:
                    return f"Found a {npc.major} major! You've reached your goal of {self.major_friends_needed} friends!"
                return f"Found a {npc.major} major! ({self.major_friends_goal}/{self.major_friends_needed} friends)"
            else:
                self.social_points -= 5
                return f"They're a {npc.major} major. -5 points"
        return "Already talked to this person today."