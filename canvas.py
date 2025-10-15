import pygame
from constants import *
import random

class Assignment:
    def __init__(self, name, due_day, difficulty):
        self.name = name
        self.due_day = due_day  # Day number when it's due
        self.difficulty = difficulty  # 0.1 to 0.5
        self.completed = False
        
class Lecture:
    def __init__(self, name, day):
        self.name = name
        self.day = day  # Day when it should be watched
        self.watched = False

class Canvas:
    def __init__(self, player, game):
        self.player = player
        self.game = game # Store the game reference
        self.assignments = []
        self.lectures = []
        self.current_day = 1
        self.visible = False  # Canvas starts hidden
        self.button_rect = pygame.Rect(WINDOW_WIDTH - 50, 20, 40, 40)  # Small icon in corner
        self.buttons = []  # Track clickable buttons
        self.last_checked_day = 0  # Track the last day we checked for new content
        
        # CS-specific assignment names
        self.assignment_names = [
            "Data Structures Project", "Algorithm Analysis", "Database Design", 
            "Web Development Task", "Machine Learning Lab", "Network Programming",
            "Software Engineering Milestone", "Operating Systems Lab", "Computer Graphics Project",
            "AI Implementation", "Cybersecurity Analysis", "Mobile App Development"
        ]
        
        # CS-specific lecture names
        self.lecture_names = [
            "Introduction to Python", "Advanced Data Structures", "Database Management Systems",
            "Web Technologies", "Machine Learning Fundamentals", "Computer Networks",
            "Software Design Patterns", "Operating System Concepts", "Computer Graphics Algorithms",
            "Artificial Intelligence", "Cybersecurity Principles", "Mobile Development Frameworks"
        ]
        
        # Generate initial assignments and lectures
        self.generate_initial_content()
        
    def generate_initial_content(self):
        # Generate 3-5 initial assignments
        num_assignments = random.randint(3, 5)
        for _ in range(num_assignments):
            due_day = self.current_day + random.randint(2, 5)
            name = f"{random.choice(self.assignment_names)} #{random.randint(1, 100)}"
            difficulty = round(random.uniform(0.1, 0.5), 1)
            self.assignments.append(Assignment(name, due_day, difficulty))
            
        # Generate 2-4 initial lectures
        num_lectures = random.randint(2, 4)
        for _ in range(num_lectures):
            name = f"{random.choice(self.lecture_names)} #{random.randint(1, 100)}"
            self.lectures.append(Lecture(name, self.current_day))
        
    def new_day(self, day_number):
        # Only update if it's actually a new day
        if day_number > self.last_checked_day:
            self.current_day = day_number
            self.last_checked_day = day_number
            
            # Check for incomplete assignments and lectures from previous day
            self.check_incomplete_work()
            
            # Generate new assignments (1-3 per day)
            num_assignments = random.randint(1, 2)
            for _ in range(num_assignments):
                # Due in 2-5 days
                due_day = self.current_day + random.randint(2, 5)
                name = f"{random.choice(self.assignment_names)} #{random.randint(1, 100)}"
                difficulty = round(random.uniform(0.1, 0.5), 1)
                self.assignments.append(Assignment(name, due_day, difficulty))
                
            # Generate new lectures (1-2 per day)
            num_lectures = random.randint(1, 2)
            for _ in range(num_lectures):
                name = f"{random.choice(self.lecture_names)} #{random.randint(1, 100)}"
                self.lectures.append(Lecture(name, self.current_day))
                
            # Show notification for new content
            if hasattr(self.player, 'game') and hasattr(self.player.game, 'event_manager'):
                self.player.game.event_manager.message = f"New assignments and lectures posted on Canvas!"
                self.player.game.event_manager.message_timer = 180
    
    def check_incomplete_work(self):
        # Check for overdue assignments
        for assignment in self.assignments[:]:
            if assignment.due_day < self.current_day and not assignment.completed:
                # --- Check if major exists before penalizing ---
                if self.player.major in self.player.grades:
                    self.player.grades[self.player.major] -= assignment.difficulty
                    # Clamp grade
                    self.player.grades[self.player.major] = max(0.0, self.player.grades[self.player.major])
                # --- End check ---
                
                # Show notification for missed assignment
                if hasattr(self.player, 'game') and hasattr(self.player.game, 'event_manager'):
                    self.player.game.event_manager.message = f"You missed {assignment.name}! GPA -{assignment.difficulty}"
                    self.player.game.event_manager.message_timer = 180
                
                self.assignments.remove(assignment)
                
        # Check for unwatched lectures from previous day
        for lecture in self.lectures[:]:
            if lecture.day < self.current_day and not lecture.watched:
                # --- Check if major exists before penalizing ---
                if self.player.major in self.player.grades:
                    # Smaller penalty for missing lectures
                    self.player.grades[self.player.major] -= 0.1
                    # Clamp grade
                    self.player.grades[self.player.major] = max(0.0, self.player.grades[self.player.major])
                # --- End check ---
                
                # Show notification for missed lecture
                if hasattr(self.player, 'game') and hasattr(self.player.game, 'event_manager'):
                    self.player.game.event_manager.message = f"You missed {lecture.name}! GPA -0.1"
                    self.player.game.event_manager.message_timer = 180
                
                self.lectures.remove(lecture)
                
        # --- Recalculate overall GPA after potential changes ---
        self.player.calculate_gpa()
        # --- End change ---

    def complete_assignment(self, index, assignments_due_today):
        if 0 <= index < len(assignments_due_today):
            assignment = assignments_due_today[index]

            # Check if player is in a valid location (Computer Lab or Dorm)
            if not self._is_in_valid_location(): # Use the helper method
                return False, "You must be in a Computer Lab or your Dorm to complete assignments!"

            if not assignment.completed:
                if self.player.energy >= 20:
                    self.player.energy -= 20
                    assignment.completed = True
                    # --- Check if major exists before boosting ---
                    if self.player.major in self.player.grades:
                        # Small GPA boost for completing assignments
                        self.player.grades[self.player.major] += 0.05
                        # Clamp grade
                        self.player.grades[self.player.major] = min(4.0, self.player.grades[self.player.major])
                        self.player.calculate_gpa() # Recalculate overall GPA
                    # --- End check ---
                    return True, f"{assignment.name} completed! +0.05 GPA"
                else:
                    return False, "Not enough energy to complete assignment"
            else:
                return False, "Assignment already completed"
        return False, "Invalid assignment index"

    def watch_lecture(self, index, lectures_due_today):
        if 0 <= index < len(lectures_due_today):
            lecture = lectures_due_today[index]

            # Check if player is in a valid location (Computer Lab or Dorm)
            if not self._is_in_valid_location(): # Use the helper method
                return False, "You must be in a Computer Lab or your Dorm to watch lectures!"

            if not lecture.watched:
                if self.player.energy >= 10:
                    self.player.energy -= 10
                    lecture.watched = True
                    # --- Check if major exists and fix GPA update ---
                    if self.player.major in self.player.grades:
                        # Small GPA boost for watching lectures
                        self.player.grades[self.player.major] += 0.02
                        # Clamp grade
                        self.player.grades[self.player.major] = min(4.0, self.player.grades[self.player.major])
                        self.player.calculate_gpa() # Recalculate overall GPA
                    # --- End check and fix ---
                    return True, f"{lecture.name} watched! +0.02 GPA"
                else:
                    return False, "Not enough energy to watch lecture"
            else:
                return False, "Lecture already watched"
        return False, "Invalid lecture index"

    def get_due_today(self):
        """Return assignments and lectures due today"""
        today_assignments = [a for a in self.assignments if a.due_day == self.current_day and not a.completed]
        today_lectures = [l for l in self.lectures if l.day == self.current_day and not l.watched]
        return today_assignments, today_lectures

    def get_all_due_items(self):
        """Return all assignments and lectures that are due and not completed/watched"""
        due_assignments = [a for a in self.assignments if not a.completed]
        due_lectures = [l for l in self.lectures if not l.watched]
        return due_assignments, due_lectures

    def get_notification_count(self):
        """Return the count of items due today"""
        today_assignments, today_lectures = self.get_due_today()
        return len(today_assignments) + len(today_lectures)

    def toggle_visibility(self):
        """Toggle the visibility of the Canvas panel"""
        self.visible = not self.visible

    def handle_click(self, mouse_pos):
        """Handle mouse clicks on the Canvas button or panel"""
        if self.button_rect.collidepoint(mouse_pos):
            self.toggle_visibility()
            return True
            
        if self.visible:
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "assignment":
                        assignments_due_today, _ = self.get_due_today()
                        success, message = self.complete_assignment(button["index"], assignments_due_today)
                        if hasattr(self.player, 'game') and hasattr(self.player.game, 'event_manager'):
                            self.player.game.event_manager.message = message
                            self.player.game.event_manager.message_timer = 180
                        return True
                    elif button["action"] == "lecture":
                        _, lectures_due_today = self.get_due_today()
                        success, message = self.watch_lecture(button["index"], lectures_due_today)
                        if hasattr(self.player, 'game') and hasattr(self.player.game, 'event_manager'):
                            self.player.game.event_manager.message = message
                            self.player.game.event_manager.message_timer = 180
                        return True
            return True
        return False
    
    # --- Add helper method to check location ---
    def _is_in_valid_location(self):
        """Checks if the player is in a Computer Lab or Dorm."""
        if self.game and self.game.current_building:
            return self.game.current_building.name in ["Computer Lab 1", "Computer Lab 2", "Dorm Building"]
        return False
    # --- End helper method ---

    def draw(self, screen, x, y, width, height):
        # Always draw the Canvas button
        pygame.draw.rect(screen, (100, 100, 200), self.button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("LMS", True, BLACK)
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)
        
        # Reset buttons list
        self.buttons = []
        
        # Get assignments and lectures due today
        assignments_due_today, lectures_due_today = self.get_due_today()
        
        # Draw notification indicator if there are due items
        notification_count = self.get_notification_count()
        if notification_count > 0:
            pygame.draw.circle(screen, RED, (self.button_rect.right - 5, self.button_rect.top + 5), 10)
            small_font = pygame.font.Font(None, 20)
            count_text = small_font.render(str(notification_count), True, WHITE)
            count_rect = count_text.get_rect(center=(self.button_rect.right - 5, self.button_rect.top + 5))
            screen.blit(count_text, count_rect)
        
        # Only draw the Canvas panel if visible
        if self.visible:
            # Draw Canvas panel
            pygame.draw.rect(screen, (220, 220, 220), (x, y, width, height))
            pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
            
            # Title
            font_title = pygame.font.Font(None, 36)
            title = font_title.render("CANVAS LMS - DUE TODAY", True, BLACK)
            title_rect = title.get_rect(center=(x + width//2, y + 30))
            screen.blit(title, title_rect)
            
            # Draw day indicator
            day_text = font_title.render(f"Day {self.current_day}", True, BLACK)
            day_rect = day_text.get_rect(topright=(x + width - 20, y + 20))
            screen.blit(day_text, day_rect)
            
            # Assignments section
            font = pygame.font.Font(None, 28)
            assignments_title = font.render("Assignments Due Today:", True, BLACK)
            screen.blit(assignments_title, (x + 20, y + 70))
            
            if not assignments_due_today:
                no_assignments = font.render("No assignments due today!", True, (100, 100, 100))
                screen.blit(no_assignments, (x + 40, y + 100))
                y_offset = y + 130
            else:
                y_offset = y + 100
                for i, assignment in enumerate(assignments_due_today):
                    # Create clickable button for assignment
                    button_rect = pygame.Rect(x + 20, y_offset, width - 40, 40)
                    color = (200, 230, 200) if assignment.completed else (230, 200, 200)
                    pygame.draw.rect(screen, color, button_rect)
                    pygame.draw.rect(screen, BLACK, button_rect, 1)
                    
                    # Add button to clickable elements
                    self.buttons.append({
                        "rect": button_rect,
                        "action": "assignment",
                        "index": i
                    })
                    
                    # Draw assignment text
                    status = "✓" if assignment.completed else ""
                    text = font.render(f"{assignment.name} {status}", True, BLACK)
                    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
                    
                    y_offset += 50
            
            # Lectures section
            lectures_title = font.render("Lectures Due Today:", True, BLACK)
            screen.blit(lectures_title, (x + 20, y_offset))
            
            if not lectures_due_today:
                no_lectures = font.render("No lectures due today!", True, (100, 100, 100))
                screen.blit(no_lectures, (x + 40, y_offset + 30))
            else:
                y_offset += 30
                for i, lecture in enumerate(lectures_due_today):
                    # Create clickable button for lecture
                    button_rect = pygame.Rect(x + 20, y_offset, width - 40, 40)
                    color = (200, 230, 200) if lecture.watched else (230, 200, 200)
                    pygame.draw.rect(screen, color, button_rect)
                    pygame.draw.rect(screen, BLACK, button_rect, 1)
                    
                    # Add button to clickable elements
                    self.buttons.append({
                        "rect": button_rect,
                        "action": "lecture",
                        "index": i
                    })
                    
                    # Draw lecture text
                    status = "✓" if lecture.watched else ""
                    text = font.render(f"{lecture.name} {status}", True, BLACK)
                    screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
                    
                    y_offset += 50
            
            # Draw location requirement notice
            notice_font = pygame.font.Font(None, 20)
            notice_text = notice_font.render("* Must be in Computer Lab or Dorm to complete tasks", True, (100, 100, 100))
            screen.blit(notice_text, (x + 20, y + height - 30))