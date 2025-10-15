import pygame
from constants import *
import random # Import random for application result

class EventManager:
    def __init__(self):
        self.message = ""
        self.message_timer = 0
        self.world = None
        self.player = None
        self.time_manager = None
        # State for the simple receptionist application menu
        self.show_receptionist_menu = False
        self.receptionist_apply_button_rect = None
        self.receptionist_menu_rect = None # To handle clicks outside the button
        # --- Add state for work shift menu ---
        self.show_work_shift_menu = False
        self.work_shift_button_rect = None
        self.work_shift_menu_rect = None
        # --- Add state for Professor's Office menu ---
        self.show_professor_menu = False
        self.professor_menu_rect = None
        self.professor_button_rect = None
        # --- End add ---

    def set_references(self, world, player, time_manager):
        self.world = world
        self.player = player
        self.time_manager = time_manager

    def handle_events(self):
        # This method is called with no arguments
        # It should handle general game events that happen every frame
        pass

    def handle_world_event(self, event, player, world, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Use F to enter buildings
                # Check if player is near any building entrance
                for location in world.locations.values():
                    # Check collision with the building rectangle first for efficiency
                    if player.rect.colliderect(location.rect):
                         # Now check if the player is near the conceptual entrance area
                         is_at_entrance = (location.is_enterable and
                                           player.rect.centerx > location.rect.left and # Player center X > building left
                                           player.rect.centerx < location.rect.right and # Player center X < building right
                                           player.rect.bottom > location.rect.bottom - 30 and # Player bottom edge near building bottom
                                           player.rect.bottom < location.rect.bottom + 10) # Player bottom edge slightly below building bottom allowed

                         if is_at_entrance:
                            game.enter_building(location)
                            return # Stop checking other locations once entered

            elif event.key == pygame.K_c:  # Use C to toggle Canvas visibility (World View)
                if game.canvas:
                    game.canvas.toggle_visibility()
            # --- Change G to SPACE for NPC interaction ---
            elif event.key == pygame.K_SPACE:  # Use SPACE to talk to NPCs
                is_on_building = False
                for location in world.locations.values():
                    if player.rect.colliderect(location.rect):
                        is_on_building = True
                        break

                if not is_on_building:
                    # Check proximity to NPCs
                    npc_interacted_or_checked = False
                    for npc in world.all_npcs:
                        # Use a slightly larger rect for interaction range
                        interaction_rect = player.rect.inflate(20, 20)
                        if interaction_rect.colliderect(npc.rect):
                            # First, check if player is close enough
                            # THEN, check if they have enough social points
                            if player.social >= 25:
                                interaction_result = npc.interact(player) # Pass player to track friendship
                                self.message = interaction_result
                                self.message_timer = 180
                                # --- Add Friend Counter/Social Adjustment ---
                                # (Keep the existing logic for friend count/social adjustment here)
                                if npc.major == "Computer Science":
                                    player.friends_count += 1
                                    # Optional: Add message about making a friend
                                    # self.message += " You made a friend!"
                                else:
                                    player.social = max(0, player.social - 10) # Decrease social, min 0
                                    # Optional: Add message about social decrease
                                    # self.message += " Awkward..."
                                # --- End Add ---
                            else:
                                # Player is close, but doesn't have enough social points
                                self.message = "You need at least 25 social points to talk to NPCs!"
                                self.message_timer = 180
                            # --- End Social Points Check ---
                            npc_interacted_or_checked = True
                            break # Interact/check with only one NPC at a time
                        # Removed the incorrect 'else' block that was here

                    # Optional message if SPACE pressed but no NPC is near
                    # if not npc_interacted_or_checked:
                    #     self.message = "No one close enough to interact with."
                    #     self.message_timer = 120


    def handle_receptionist_application(self, game):
        """Handles the logic when the player clicks 'Apply' for the receptionist job."""
        player = game.player
        # --- Define Requirements ---
        required_gpa = 3.0
        cost_energy = 20
        # --- Remove Money Cost ---
        # cost_money = 50
        # --- End Remove ---
        # --- End Requirements ---

        # --- Check Requirements ---
        # --- Fix: Check player.current_job ---
        if player.current_job is not None:
        # --- End Fix ---
            self.message = "You already have a job."
            self.message_timer = 120
        elif player.gpa < required_gpa:
            self.message = f"Requires {required_gpa:.1f} GPA. Your GPA is {player.gpa:.2f}."
            self.message_timer = 180
        elif player.energy < cost_energy:
            self.message = f"Not enough energy ({cost_energy} required)."
            self.message_timer = 120
        # --- Remove Money Check ---
        # elif player.money < cost_money:
        #     self.message = f"Not enough money (${cost_money} required)."
        #     self.message_timer = 120
        # --- End Remove ---
        else:
            # --- Requirements Met - Apply Costs & Grant Job ---
            player.energy -= cost_energy
            # --- Remove Money Deduction ---
            # player.money -= cost_money
            # --- End Remove ---

            job_name = "Receptionist"
            job_pay = 50 # Example pay per shift/day (adjust as needed)
            job_energy_cost = 20 # Add energy cost for the job itself

            # Assign the job (store details if needed)
            # --- Fix: Assign to player.current_job ---
            player.current_job = {"name": job_name, "pay": job_pay, "energy_cost": job_energy_cost} # Store job info
            # --- End Fix ---
            # Note: Payment might happen later via scheduled events or shifts
            # --- Update Message ---
            self.message = f"Applied! (-{cost_energy} Energy). You got the {job_name} job!"
            # --- End Update ---
            self.message_timer = 180
            # --- End Apply Costs & Grant Job ---

        # Close the menu regardless of outcome
        self.show_receptionist_menu = False

    def handle_interior_event(self, event, game):
        player = game.player
        building = game.current_building

        if not building: # Simplified check
             return

        # --- Handle Professor Menu Click FIRST ---
        if self.show_professor_menu and event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is on the button
            if self.professor_button_rect and self.professor_button_rect.collidepoint(event.pos):
                self.handle_in_person_request(game) # Call the requirement check logic
                # Menu closing is handled within handle_in_person_request
                return # Click handled

            # Check if click is outside the menu area to close it
            elif self.professor_menu_rect and not self.professor_menu_rect.collidepoint(event.pos):
                 self.show_professor_menu = False # Close menu if clicked outside
                 return # Click handled

            # If click is inside menu but not on button, do nothing (consume event)
            elif self.professor_menu_rect and self.professor_menu_rect.collidepoint(event.pos):
                 return # Click handled (inside menu)

        # --- Handle Work Shift Menu Click ---
        if self.show_work_shift_menu and event.type == pygame.MOUSEBUTTONDOWN:
            # Check work button click
            if self.work_shift_button_rect and self.work_shift_button_rect.collidepoint(event.pos):
                # --- Add Work Shift Logic ---
                # --- Fix: Check player.current_job ---
                if player.current_job: # Check if the player actually has a job
                    job_details = player.current_job # Use current_job
                    shift_energy_cost = job_details.get("energy_cost", 20) # Default if not found
                    shift_pay = job_details.get("pay", 50) # Default if not found

                    if player.energy >= shift_energy_cost:
                        player.energy -= shift_energy_cost
                        player.money += shift_pay
                        self.message = f"Worked a shift. (+${shift_pay}, -{shift_energy_cost} Energy)"
                        self.message_timer = 180
                    else:
                        self.message = f"Not enough energy to work ({shift_energy_cost} required)."
                        self.message_timer = 120
                else:
                    self.message = "You don't have a job to work at!"
                    self.message_timer = 120
                # --- End Fix ---

                self.show_work_shift_menu = False # Close menu after action
                # --- End Work Shift Logic ---
                return # Click handled
            # Check if click is outside the menu area
            elif self.work_shift_menu_rect and not self.work_shift_menu_rect.collidepoint(event.pos):
                 self.show_work_shift_menu = False # Close menu
                 return # Click handled
            # Click was inside the menu but not on the button
            elif self.work_shift_menu_rect and self.work_shift_menu_rect.collidepoint(event.pos):
                 return # Click handled (by doing nothing)
        # --- End Work Shift Menu Click ---

        # Handle menu clicks first if the receptionist menu is visible
        elif self.show_receptionist_menu and event.type == pygame.MOUSEBUTTONDOWN:
            # Check apply button click
            if self.receptionist_apply_button_rect and self.receptionist_apply_button_rect.collidepoint(event.pos):
                self.handle_receptionist_application(game)
                # Close menu handled within handle_receptionist_application
                return # Click handled
            # Check if click is outside the menu area
            elif self.receptionist_menu_rect and not self.receptionist_menu_rect.collidepoint(event.pos):
                 self.show_receptionist_menu = False # Close menu
                 return # Click handled
            # Click was inside the menu but not on the button
            elif self.receptionist_menu_rect and self.receptionist_menu_rect.collidepoint(event.pos):
                 return # Click handled (by doing nothing)

        # Handle other clicks if no menu handled it
        elif event.type == pygame.MOUSEBUTTONDOWN:
             # Handle Canvas clicks first if visible
            if game.canvas and game.canvas.visible:
                 if game.canvas.handle_click(event.pos):
                     return # Stop further processing if canvas handled click

            # Handle building-specific button clicks (Job Menu / Club Menu toggles)
            if building.name == "IM Building":
                # Check if clicking the green "Job" box (Job Area object)
                job_area_obj = next((obj for obj in building.interior_objects if obj["name"] == "Job Area"), None)
                if job_area_obj and pygame.Rect(job_area_obj["rect"]).collidepoint(event.pos):
                    # --- Check if player already has a job BEFORE showing menu ---
                    # --- Fix: Check player.current_job ---
                    if not player.current_job: # Only allow applying if no job
                    # --- End Fix ---
                        if game.job_menu:
                            game.job_menu.toggle_visibility() # Toggle full menu on box click
                            self.show_receptionist_menu = False # Ensure simple menu is closed
                            return
                    else:
                        # --- If player has a job, show work shift menu instead ---
                        self.show_work_shift_menu = True
                        # Define menu and button rects for the work shift menu
                        menu_width, menu_height = 300, 150
                        menu_x = (WINDOW_WIDTH - menu_width) // 2
                        menu_y = (WINDOW_HEIGHT - menu_height) // 2
                        self.work_shift_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
                        button_width, button_height = 150, 50
                        button_x = menu_x + (menu_width - button_width) // 2
                        button_y = menu_y + 50 # Position button inside menu
                        self.work_shift_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        return # Stop further processing
                        # --- End Work Shift Menu Logic ---

                # Handle clicks within the full JobMenu if it's visible
                elif game.job_menu and game.job_menu.visible:
                    # --- Fix: Pass game instance to handle_click ---
                    success, message = game.job_menu.handle_click(event.pos, game) # Pass game
                    # --- End Fix ---
                    if success is not None: # Check if handle_click returned something
                        if success: # If a job was successfully taken
                            self.message = message
                            self.message_timer = 180
                            game.job_menu.toggle_visibility() # Close menu on success
                        else: # If taking job failed (e.g., not enough energy)
                            self.message = message
                            self.message_timer = 120
                        return # Click handled by job menu


        # --- KEYDOWN Event Handling (Corrected) ---
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Exit building with F key
                game.exit_building()
                self.show_receptionist_menu = False # Close menu on exit
                self.show_work_shift_menu = False # Close work menu on exit
                if game.job_menu: game.job_menu.visible = False # Close job menu on exit
                if game.club_menu: game.club_menu.visible = False # Close club menu on exit
                return

            # --- C Key: ONLY for Canvas Toggle ---
            elif event.key == pygame.K_c:
                # Check if in a building where Canvas is allowed
                if game.canvas and building.name in ["Computer Lab 1", "Computer Lab 2", "Dorm Building"]:
                     game.canvas.toggle_visibility()
                # If C is pressed elsewhere inside, do nothing specific for interaction
                return # C key event processed

            # --- G Key: For ALL Interior Interactions ---
            elif event.key == pygame.K_g:
                # Remove or comment out the print statement below
                # print("G key pressed inside building:", building.name) # DEBUG
                interaction_handled = False
                # Priority 1: Westgate Building - Professor's Office
                if building.name == "Westgate Building":
                    # Remove or comment out the print statement below
                    # print("  In Westgate Building check") # DEBUG
                    if hasattr(building, 'interior_objects'):
                        prof_office_obj = next((obj for obj in building.interior_objects if obj.get("action") == "professor_office"), None)
                        if prof_office_obj:
                            # Remove or comment out the print statements below
                            # print(f"  Found Professor's Office object: {prof_office_obj['rect']}") # DEBUG
                            office_interaction_rect = pygame.Rect(prof_office_obj["rect"]).inflate(10, 10)
                            # print(f"  Player rect: {player.rect}") # DEBUG
                            # print(f"  Office interaction rect (inflated): {office_interaction_rect}") # DEBUG

                            if player.rect.colliderect(office_interaction_rect):
                                # Remove or comment out the print statements below
                                # print("  Collision DETECTED with Professor's Office!") # DEBUG
                                self.show_professor_menu = not self.show_professor_menu
                                # print(f"  Toggled show_professor_menu to: {self.show_professor_menu}") # DEBUG
                                # Ensure other potentially open menus are closed
                                self.show_receptionist_menu = False
                                self.show_work_shift_menu = False
                                if game.job_menu: game.job_menu.visible = False
                                if game.club_menu: game.club_menu.visible = False
                                self.message = "" # Clear any previous message
                                self.message_timer = 0
                                interaction_handled = True
                            else:
                                # Remove or comment out the print statement below
                                # print("  Collision NOT detected with Professor's Office.") # DEBUG
                                pass # Add this pass statement
                        # else:
                             # Remove or comment out the print statement below
                             # print("  Professor's Office object not found in interior_objects.") # DEBUG

                # Priority 2: IM Building - Specific Interactions
                elif building.name == "IM Building":
                    if hasattr(building, 'interior_objects'):
                        info_desk_obj = next((obj for obj in building.interior_objects if obj["name"] == "Information Desk"), None)
                        job_area_obj = next((obj for obj in building.interior_objects if obj["name"] == "Job Area"), None)

                        # --- Check Information Desk Collision ---
                        if info_desk_obj and player.rect.colliderect(info_desk_obj["rect"]):
                            if not player.current_job: # Use current_job instead of job
                                self.show_receptionist_menu = not self.show_receptionist_menu
                                self.show_work_shift_menu = False # Close work menu if open
                                self.message = "" # Clear message
                                self.message_timer = 0
                            else:
                                # Optionally show a message if they already have a job
                                self.message = "You already have a job. Go to the Job Area to work."
                                self.message_timer = 120
                                self.show_receptionist_menu = False # Ensure menus are closed
                                self.show_work_shift_menu = False
                            interaction_handled = True

                        # --- Check Job Area Collision ---
                        elif job_area_obj and player.rect.colliderect(job_area_obj["rect"]):
                            # --- Modify: Directly handle work action instead of menu ---
                            if player.current_job and player.current_job.get("name") == "Receptionist":
                                # Directly attempt to work
                                job_details = player.current_job
                                shift_energy_cost = job_details.get("energy_cost", 20)
                                shift_pay = job_details.get("pay", 50)

                                if player.energy >= shift_energy_cost:
                                    player.energy -= shift_energy_cost
                                    player.money += shift_pay
                                    self.message = f"Worked a shift. (+${shift_pay}, -{shift_energy_cost} Energy)"
                                    self.message_timer = 180
                                else:
                                    self.message = f"Not enough energy to work ({shift_energy_cost} required)."
                                    self.message_timer = 120
                                # Ensure other menus are closed
                                self.show_receptionist_menu = False
                                self.show_work_shift_menu = False
                            # --- End Modify ---
                            else:
                                # Message if they don't have the job
                                self.message = "You need the Receptionist job to work here. Apply at the desk."
                                self.message_timer = 120
                                self.show_receptionist_menu = False # Ensure menus are closed
                                self.show_work_shift_menu = False
                            interaction_handled = True

                        # Close menus if G pressed near one interaction point while the other's menu was open
                        if interaction_handled:
                             if game.job_menu: game.job_menu.visible = False # Close full job menu too

                # Priority 2: General Interior Object Interaction (if not handled above)
                if not interaction_handled and hasattr(building, 'interior_objects'):
                     interaction_result = self.handle_interior_interaction(player, building, game) # Pass game object
                     if interaction_result: # Check if interaction occurred
                         interaction_handled = True

                # If G was pressed but nothing happened (e.g., not near desk or object)
                if not interaction_handled:
                     # Close menus if player moved away from interaction points and pressed G
                     self.show_receptionist_menu = False
                     self.show_work_shift_menu = False # Close work menu too
                     self.show_professor_menu = False # Close professor menu too
                     if game.job_menu: game.job_menu.visible = False
                     if game.club_menu: game.club_menu.visible = False
                return # G key event processed

    # --- Add method to handle the in-person class request ---
    def handle_in_person_request(self, game):
        """Checks requirements and triggers game end if met."""
        player = game.player
        required_friends = 5
        required_money = 100
        required_gpa = 3.5
        required_energy = 50

        if player.friends_count < required_friends:
            self.message = f"You need {required_friends} friends first."
            self.message_timer = 180
        elif player.money < required_money:
            self.message = f"You need ${required_money}."
            self.message_timer = 180
        elif player.gpa < required_gpa:
            self.message = f"Your GPA needs to be at least {required_gpa:.1f}."
            self.message_timer = 180
        elif player.energy < required_energy:
            self.message = f"You need {required_energy} energy."
            self.message_timer = 180
        else:
            # Requirements met!
            player.energy -= required_energy
            player.money -= required_money # Deduct costs
            # Set flag in game object to trigger end screen
            game.trigger_end_screen()
            self.message = "You advocate for change..." # Optional brief message
            self.message_timer = 60 # Show briefly before end screen

        # Close the menu only if requirements are NOT met (otherwise game ends)
        if not game.show_end_screen:
             self.show_professor_menu = False
    # --- End add method ---

    def draw(self, screen):
        # Draw message if timer is active
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message:
                font = pygame.font.Font(None, 30)
                text_surface = font.render(self.message, True, BLACK)
                # Position message at the bottom center
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
                # Optional: Add a semi-transparent background for readability
                bg_rect = text_rect.inflate(10, 5)
                bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                bg_surface.fill((200, 200, 200, 180)) # Light gray, semi-transparent
                screen.blit(bg_surface, bg_rect)
                screen.blit(text_surface, text_rect)
        else:
            self.message = "" # Clear message when timer runs out

        # --- Draw Simple Receptionist Application Menu ---
        if self.show_receptionist_menu:
            self.draw_receptionist_menu(screen)
        # --- End Draw ---

        # --- Draw Work Shift Menu ---
        if self.show_work_shift_menu:
            self.draw_work_shift_menu(screen)
        # --- End Draw ---

        # --- Draw Professor's Office Menu ---
        if self.show_professor_menu:
            self.draw_professor_menu(screen)
        # --- End Draw ---

        # --- Add: Draw Player Job Status ---
        if self.player: # Ensure player object exists
            font = pygame.font.Font(None, 24)
            # --- Fix: Access player.current_job ---
            job_details = self.player.current_job if self.player else {} # Get player job details safely
            # --- End Fix ---
            job_name = job_details.get("name", "Unemployed") if job_details else "Unemployed"
            job_text = f"Job: {job_name}"
            text_surface = font.render(job_text, True, BLACK)
            # Position near other stats (adjust as needed)
            screen.blit(text_surface, (10, 190)) # Below Friends count
        # --- End Add ---


    def draw_receptionist_menu(self, screen):
        # Define menu dimensions and position
        menu_width, menu_height = 300, 150
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        self.receptionist_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        # Draw menu background
        pygame.draw.rect(screen, WHITE, self.receptionist_menu_rect)
        pygame.draw.rect(screen, BLACK, self.receptionist_menu_rect, 2)

        # Draw title and info
        font = pygame.font.Font(None, 30)
        title = font.render("Apply for Receptionist?", True, BLACK)
        screen.blit(title, (menu_x + 10, menu_y + 10))

        info_font = pygame.font.Font(None, 24)
        req_gpa = 3.0
        req_energy = 20
        # req_money = 50 # Removed
        info1 = info_font.render(f"Requires: {req_gpa:.1f} GPA, {req_energy} Energy", True, DARK_GRAY)
        # info2 = info_font.render(f"Cost: ${req_money}", True, DARK_GRAY) # Removed
        screen.blit(info1, (menu_x + 10, menu_y + 50))
        # screen.blit(info2, (menu_x + 10, menu_y + 75)) # Removed

        # Draw Apply button
        button_width, button_height = 100, 40
        button_x = menu_x + (menu_width - button_width) // 2
        # button_y = menu_y + menu_height - button_height - 10 # Original position
        button_y = menu_y + 100 # Adjusted position after removing cost line
        self.receptionist_apply_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, self.receptionist_apply_button_rect)
        pygame.draw.rect(screen, BLACK, self.receptionist_apply_button_rect, 1)
        apply_text = font.render("Apply", True, BLACK)
        apply_rect = apply_text.get_rect(center=self.receptionist_apply_button_rect.center)
        screen.blit(apply_text, apply_rect)

    # --- Add Draw Work Shift Menu ---
    def draw_work_shift_menu(self, screen):
        # Use the rects defined when the menu was shown
        if not self.work_shift_menu_rect or not self.work_shift_button_rect:
            return # Don't draw if rects aren't set

        # Draw menu background
        pygame.draw.rect(screen, WHITE, self.work_shift_menu_rect)
        pygame.draw.rect(screen, BLACK, self.work_shift_menu_rect, 2)

        # Draw title
        font = pygame.font.Font(None, 30)
        title = font.render("Work Shift?", True, BLACK)
        screen.blit(title, (self.work_shift_menu_rect.x + 10, self.work_shift_menu_rect.y + 10))

        # Draw Work button
        pygame.draw.rect(screen, LIGHT_BLUE, self.work_shift_button_rect)
        pygame.draw.rect(screen, BLACK, self.work_shift_button_rect, 1)
        work_text = font.render("Work", True, BLACK)
        work_rect = work_text.get_rect(center=self.work_shift_button_rect.center)
        screen.blit(work_text, work_rect)
    # --- End Draw Work Shift Menu ---

    # --- Add Draw Professor Menu ---
    def draw_professor_menu(self, screen):
        # Define menu dimensions and position dynamically
        menu_width, menu_height = 400, 200 # Adjusted size for new line
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        self.professor_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        # Draw menu background
        pygame.draw.rect(screen, (230, 230, 250), self.professor_menu_rect) # Light lavender background
        pygame.draw.rect(screen, BLACK, self.professor_menu_rect, 2)

        # Draw title and info
        font_title = pygame.font.Font(None, 32)
        font_info = pygame.font.Font(None, 24)
        title = font_title.render("Professor's Office", True, BLACK)
        screen.blit(title, (menu_x + 10, menu_y + 10))

        info1 = font_info.render("Request In-Person Classes?", True, DARK_GRAY)
        info2 = font_info.render("Requires: 5 Friends, 3.5 GPA, 50 Social", True, DARK_GRAY) # Updated text
        info3 = font_info.render("Cost: 30 Energy", True, DARK_GRAY)
        screen.blit(info1, (menu_x + 10, menu_y + 50))
        screen.blit(info2, (menu_x + 10, menu_y + 75))
        screen.blit(info3, (menu_x + 10, menu_y + 100))

        # Draw Request button
        button_width, button_height = 120, 40
        button_x = menu_x + (menu_width - button_width) // 2
        button_y = menu_y + menu_height - button_height - 20 # Adjusted position
        self.professor_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (100, 150, 255), self.professor_button_rect) # Nice blue button
        pygame.draw.rect(screen, BLACK, self.professor_button_rect, 1)
        request_text = font_title.render("Request", True, WHITE) # White text on blue
        request_rect = request_text.get_rect(center=self.professor_button_rect.center)
        screen.blit(request_text, request_rect)
    # --- End Draw Professor Menu ---

    # --- Add Handle In-Person Request Logic ---
    def handle_in_person_request(self, game):
        player = game.player
        required_gpa = 3.5
        required_social = 50
        required_friends = 5 # New requirement
        cost_energy = 30

        # Check requirements
        if player.friends_count < required_friends: # Check friends first
            self.message = f"Professor: You need more allies ({required_friends} Friends needed)."
            self.message_timer = 180
        elif player.gpa < required_gpa:
            self.message = f"Professor: Your GPA ({player.gpa:.2f}) isn't quite high enough ({required_gpa:.1f} needed)."
            self.message_timer = 180
        elif player.social < required_social:
            self.message = f"Professor: You need more social influence ({required_social} needed)."
            self.message_timer = 180
        elif player.energy < cost_energy:
            self.message = f"Too tired to make your case ({cost_energy} Energy needed)."
            self.message_timer = 120
        else:
            # Requirements met - Apply costs and determine outcome
            player.energy -= cost_energy

            # Random chance of success (e.g., 50%)
            if random.random() < 0.5: # 50% chance
                # Success! Trigger the end screen
                self.message = "Professor: Impressive! I'll advocate for more in-person options."
                self.message_timer = 240 # Longer message display
                # --- Trigger the end game sequence ---
                game.trigger_end_screen() # Call the method in Game class
                # --- End Trigger ---
            else:
                # Failure
                self.message = "Professor: I understand, but it's complex. Maybe try again later."
                self.message_timer = 180
                # Optional: Small penalty or cooldown?

        # Close the menu regardless of outcome
        self.show_professor_menu = False
    # --- End Handle In-Person Request Logic ---

    def handle_interior_interaction(self, player, building, game):
        """Handles interaction with objects inside a building when G is pressed."""
        interaction_occurred = False
        if not hasattr(building, 'interior_objects'):
            # This shouldn't happen if building setup is correct, but good failsafe
            print(f"Warning: Building '{building.name}' missing 'interior_objects' for interaction.")
            return False # Indicate no interaction occurred

        for obj in building.interior_objects:
            obj_rect = pygame.Rect(obj["rect"])
            # Check collision between player and the object
            if player.rect.colliderect(obj_rect):
                action = obj.get("action")
                # Handle interaction based on object action type
                if action == "study":
                    cost_energy = 15
                    gain_gpa = 0.1 # Example GPA gain
                    if player.energy >= cost_energy:
                        player.energy -= cost_energy
                        player.gpa = min(4.0, player.gpa + gain_gpa) # Cap GPA at 4.0
                        self.message = f"You studied. (-{cost_energy} Energy, +{gain_gpa:.1f} GPA)"
                        interaction_occurred = True
                    else:
                        self.message = "You're too tired to study."
                    self.message_timer = 120
                    break # Interact with only one object at a time

                elif action == "rest":
                    gain_energy = 20
                    max_energy = 100 # Assuming max energy is 100
                    energy_recovered = min(gain_energy, max_energy - player.energy) # Don't exceed max
                    if energy_recovered > 0:
                        player.energy += energy_recovered
                        self.message = f"You rested for a bit. (+{energy_recovered} Energy)"
                    else:
                        self.message = "You are already fully rested."
                    self.message_timer = 120
                    interaction_occurred = True
                    break

                elif action == "eat":
                    cost_money = 10
                    gain_energy = 15
                    if player.money >= cost_money:
                         if player.energy < 100:
                             player.money -= cost_money
                             player.energy = min(100, player.energy + gain_energy)
                             self.message = f"Grabbed a bite to eat. (-${cost_money}, +{gain_energy} Energy)"
                         else:
                             self.message = "You're not hungry right now."
                    else:
                         self.message = "Not enough money to buy food."
                    self.message_timer = 120
                    interaction_occurred = True
                    break

                elif action == "attend_class":
                    cost_energy = 25
                    gain_gpa = 0.2
                    if player.energy >= cost_energy:
                        player.energy -= cost_energy
                        player.gpa = min(4.0, player.gpa + gain_gpa)
                        self.message = f"Attended class. (-{cost_energy} Energy, +{gain_gpa:.1f} GPA)"
                        interaction_occurred = True
                    else:
                        self.message = "Too tired to focus in class."
                    self.message_timer = 120
                    break

                # --- Add Socialize Action ---
                elif action == "socialize":
                    cost_energy = 10
                    cost_money = 5
                    gain_social = 15
                    max_social = 100 # Assuming a max social limit

                    if player.energy < cost_energy:
                        self.message = f"Too tired to socialize. (-{cost_energy} Energy required)"
                        self.message_timer = 120
                    elif player.money < cost_money:
                        self.message = f"Need ${cost_money} to join the fun."
                        self.message_timer = 120
                    else:
                        player.energy -= cost_energy
                        player.money -= cost_money
                        social_gained = min(gain_social, max_social - player.social) # Don't exceed max
                        player.social += social_gained
                        self.message = f"Socialized! (-{cost_energy} Energy, -${cost_money}, +{social_gained} Social)"
                        self.message_timer = 180
                    interaction_occurred = True
                    break
                # --- End Socialize Action ---

                # Add more object interactions here based on "action" key...
                # Example for Club Area (though click might be preferred)
                # elif action == "club_info": # If object represents club info area
                #      if game.club_menu:
                #          game.club_menu.toggle_visibility()
                #          self.message = "Opened Club Menu."
                #          interaction_occurred = True
                #      else:
                #          self.message = "Club menu not available."
                #      self.message_timer = 120
                #      break


        # Return True if an interaction happened, False otherwise
        return interaction_occurred