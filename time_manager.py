import pygame
from constants import *

class TimeManager:
    def __init__(self, world=None): # Add world reference
        self.day = 1
        self.hour = 7 # Start at 7 AM
        self.minute = 0
        # --- Remove time_speed, add frame counter ---
        # self.time_speed = 60 # No longer needed for interval-based update
        self.frame_counter = 0
        self.scheduled_events = [] # List to hold scheduled events
        # --- End change ---
        self.world = world # Store world reference

    def set_references(self, world): # Method to set reference if not done in init
        self.world = world

    def update(self, dt):
        # --- Interval-based time update ---
        self.frame_counter += 1

        # Check if one second (FPS frames) has passed
        if self.frame_counter >= FPS:
            self.frame_counter = 0 # Reset counter

            # Advance time by 30 minutes
            self.minute += 30

            if self.minute >= 60:
                hours_passed = self.minute // 60
                self.minute %= 60
                self.hour += hours_passed

                # --- Check for day rollover (Corrected Attributes) ---
                # This logic might be redundant if the interval update handles it,
                # but ensure the attribute names are correct if it's kept.
                # A potential issue: This check might run *before* the interval update
                # increments the hour past 23 in the same frame, causing the day
                # to increment prematurely or twice. Consider integrating this
                # check *within* the interval update block.

                # Let's assume the interval update handles the hour increment correctly first.
                # The check for >= 24 should happen *after* the hour could have been incremented.

                # --- Revised logic integrated into interval update ---
                self.frame_counter += 1

                # Check if one second (FPS frames) has passed
                if self.frame_counter >= FPS:
                    self.frame_counter = 0 # Reset counter

                    # Advance time by 30 minutes
                    self.minute += 30

                    if self.minute >= 60:
                        hours_passed = self.minute // 60
                        self.minute %= 60
                        self.hour += hours_passed

                        # --- Day Rollover Check (Moved Here) ---
                        if self.hour >= 24:
                            days_passed = self.hour // 24 # Usually 1
                            self.hour %= 24
                            self.day += days_passed
                            # --- Call NPC respawn on new day ---
                            if self.world:
                                self.world.respawn_npcs()
                            # --- End call ---
                            print(f"A new day has begun! Day {self.day}") # Use self.day
                            # --- Daily Stat Decay ---
                            # Example: player loses some energy/social overnight
                            # self.player.energy = max(0, self.player.energy - 10)
                            # self.player.social = max(0, self.player.social - 5)
                            # --- End Daily Stat Decay ---
                        # --- End Day Rollover Check ---

                # --- Check scheduled events (basic placeholder) ---
                # current_time_tuple = (self.day, self.hour, self.minute)
                # for event in self.scheduled_events[:]:
                #     target_day, target_hour, target_minute, callback, args = event
                #     if self.day > target_day or \
                #        (self.day == target_day and self.hour > target_hour) or \
                #        (self.day == target_day and self.hour == target_hour and self.minute >= target_minute):
                #         callback(*args)
                #         self.scheduled_events.remove(event)
                # --- End placeholder check ---

        # --- Original continuous update (commented out) ---
        # minutes_passed = self.time_speed / FPS # Correct calculation
        # self.minute += minutes_passed
        # if self.minute >= 60:
        #     hours_passed = int(self.minute // 60)
        #     self.minute %= 60
        #     self.hour += hours_passed
        #     if self.hour >= 24:
        #         days_passed = int(self.hour // 24)
        #         self.hour %= 24
        #         self.day += days_passed
        # --- End original update ---

        # --- Fix: Use self.hour and self.day instead of self.current_hour and self.current_day ---
        if self.hour >= 24: # Check self.hour
            # This block seems redundant now with the interval-based update above,
            # but let's fix the attribute names anyway in case it's intended.
            # Consider reviewing if this logic is still needed.
            self.hour = 0 # Reset self.hour
            self.day += 1 # Increment self.day
            # --- Call NPC respawn on new day ---
            if self.world:
                self.world.respawn_npcs()
            # --- End call ---
            # Trigger other daily events here if needed
            print(f"A new day has begun! Day {self.day}") # Use self.day
            # --- Daily Stat Decay ---
            # Example: player loses some energy/social overnight
            # This should ideally be passed the player object
            # self.player.energy = max(0, self.player.energy - 10)
            # self.player.social = max(0, self.player.social - 5)
            # --- End Daily Stat Decay ---
        # --- End Fix ---


    def get_day_of_week(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[(self.day - 1) % 7]

    # --- Add this method ---
    def get_formatted_time(self):
        hour_12 = self.hour % 12
        if hour_12 == 0:
            hour_12 = 12 # Midnight or Noon is 12
        am_pm = "AM" if self.hour < 12 else "PM"
        return f"{hour_12:02}:{int(self.minute):02} {am_pm}"
    # --- End of added method ---

    # --- Add the missing method ---
    def add_scheduled_event(self, target_day, target_hour, target_minute, callback, *args):
        """Schedules a function to be called at a specific game time."""
        # Basic implementation: Store event details
        # More robust implementation might handle recurring events, etc.
        event_details = (target_day, target_hour, target_minute, callback, args)
        self.scheduled_events.append(event_details)
        print(f"Scheduled event for Day {target_day}, {target_hour:02}:{target_minute:02}") # Debug print
    # --- End of added method ---

    # --- Optional: Placeholder for new day logic ---
    # def trigger_new_day_events(self):
    #     print(f"Starting Day {self.day}")
    #     # Example: Reset NPC interactions, generate new assignments, etc.
    #     # if hasattr(self, 'world'): # Check if world reference exists
    #     #     self.world.reset_npcs_daily()
    #     # if hasattr(self, 'canvas'): # Check if canvas reference exists
    #     #     self.canvas.generate_daily_tasks()
    # --- End placeholder ---