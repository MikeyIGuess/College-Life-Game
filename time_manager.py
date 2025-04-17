import time
from constants import *

class TimeManager:
    def __init__(self):
        self.day = 1
        self.hour = 8
        self.minute = 0
        self.last_update = time.time()
        self.time_scale = 0.5  # Much slower: 1 real second = 15 game minutes
        
    def update(self):
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        if elapsed >= 1/self.time_scale:
            self.minute += 30  # Increment by 30 minutes instead of 1
            if self.minute >= 60:
                self.minute = 0
                self.hour += 1
                
            if self.hour >= 24:
                self.hour = 8
                self.day += 1
                
            self.last_update = current_time
            
    def get_time_string(self):
        return f"{self.hour:02d}:{self.minute:02d}"
        
    def is_new_day(self):
        return self.hour == 8 and self.minute == 0