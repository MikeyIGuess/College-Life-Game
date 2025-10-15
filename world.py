import pygame
# --- Import MAP_WIDTH and MAP_HEIGHT ---
from constants import * # Keep existing imports
from constants import MAP_WIDTH, MAP_HEIGHT # Add this line
# --- End Import ---
from location import Location
from npc import NPC # Make sure NPC is imported
import random

# --- Add a list of possible majors ---
# --- Add POSSIBLE_MAJORS if not already defined or imported ---
# Example:
POSSIBLE_MAJORS = ["Computer Science", "Engineering", "Arts", "Business", "Science"]
# --- End Add ---

class World:
    # Modify the __init__ signature to accept time_manager
    def __init__(self, locations_data, time_manager):
        self.locations = {}
        for name, data in locations_data.items():
            rect_obj = data['rect'] # Get the Rect object
            self.locations[name] = Location(
                name,
                rect_obj.x, # Pass x
                rect_obj.y, # Pass y
                rect_obj.width, # Pass width
                rect_obj.height, # Pass height
                color=data.get('color', BLUE), # Pass color keyword argument
                is_enterable=data.get('is_enterable', True), # Pass is_enterable keyword argument
                interior_color=data.get('interior_color', (240, 240, 240)) # Pass interior_color keyword argument
            )
        # Store the time_manager reference
        self.time_manager = time_manager
        # --- Keep using a single list for all NPCs ---
        self.all_npcs = []
        self.spawn_npcs(5) # Initial spawn of 5 NPCs
        # --- End change ---

    def spawn_npcs(self, count):
        """Spawns a specific number of NPCs, potentially inside or near buildings."""
        self.all_npcs.clear() # Clear existing NPCs before spawning new ones
        spawned_count = 0
        max_attempts = count * 20 # Increased attempts slightly

        spawnable_buildings = [loc for name, loc in self.locations.items() if name in ["HUB-Robeson Center", "Dorm Building", "IM Building", "Westgate Building", "Computer Lab 1", "Computer Lab 2"]] # Include more buildings if desired
        all_buildings = list(self.locations.values()) # Get all building locations

        attempts = 0
        while spawned_count < count and attempts < max_attempts:
            attempts += 1
            npc_name = f"Person {spawned_count + 1}" # Simple naming
            npc_major = random.choice(POSSIBLE_MAJORS) # Assign a random major
            dialogue = [f"Hi, I'm {npc_name}.", "Just wandering around."]

            # --- Decide spawn location: 60% chance outside (near building), 40% inside ---
            if random.random() < 0.6 or not spawnable_buildings: # Spawn outside near a building
                # --- Spawn Outside (Near a Building) ---
                if not all_buildings: continue # Skip if no buildings exist

                valid_spawn = False
                for _ in range(10): # Try 10 times to find a spot near a building
                    target_building = random.choice(all_buildings)
                    # Spawn within a radius around the building's center
                    spawn_radius = max(target_building.width, target_building.height) * 1.5 # Adjust radius as needed
                    offset_x = random.uniform(-spawn_radius, spawn_radius)
                    offset_y = random.uniform(-spawn_radius, spawn_radius)
                    x = target_building.rect.centerx + offset_x
                    y = target_building.rect.centery + offset_y

                    # Clamp coordinates to map bounds
                    x = max(0, min(x, MAP_WIDTH - TILE_SIZE))
                    y = max(0, min(y, MAP_HEIGHT - TILE_SIZE))

                    temp_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                    # Check collision with ALL buildings
                    collides_with_building = any(temp_rect.colliderect(loc.rect) for loc in all_buildings)

                    if not collides_with_building:
                        # Pass the assigned major to the NPC constructor
                        npc = NPC(x, y, name=npc_name, dialogue=dialogue, major=npc_major)
                        npc.current_location_name = None # Explicitly set as outside
                        self.all_npcs.append(npc)
                        spawned_count += 1
                        valid_spawn = True
                        break # Found a valid spot

                if not valid_spawn:
                    print(f"Warning: Could not find valid outdoor spawn point near a building for NPC {spawned_count + 1}")
                # --- End Spawn Outside ---
            else:
                # --- Spawn Inside (Existing Logic - Minor Refinements) ---
                building = random.choice(spawnable_buildings)
                # Ensure interior setup exists (using rect as a proxy for now)
                if hasattr(building, 'rect'): # Basic check if building has dimensions
                     valid_spawn = False
                     for _ in range(10): # Try 10 times
                         # Spawn within the building's main rectangle, slightly inset
                         inset = TILE_SIZE // 2 # Small inset from edges
                         min_x = building.rect.left + inset
                         max_x = building.rect.right - TILE_SIZE - inset
                         min_y = building.rect.top + inset
                         max_y = building.rect.bottom - TILE_SIZE - inset

                         if max_x > min_x and max_y > min_y: # Ensure valid range
                             x = random.randint(min_x, max_x)
                             y = random.randint(min_y, max_y)

                             # TODO: Add collision check with interior walls/objects if necessary
                             # For now, just spawn within the bounds

                             # Pass the assigned major to the NPC constructor
                             npc = NPC(x, y, name=npc_name, dialogue=dialogue, major=npc_major)
                             npc.current_location_name = building.name # Assign building name
                             self.all_npcs.append(npc)
                             spawned_count += 1
                             valid_spawn = True
                             break # Found a spot
                         else: # Fallback if building rect is too small
                             print(f"Warning: Building {building.name} rect too small for indoor spawn.")
                             break # Stop trying for this building

                     if not valid_spawn:
                         print(f"Warning: Could not find valid indoor spawn point in {building.name} for NPC {spawned_count + 1}")
                else:
                     print(f"Warning: Building {building.name} selected for indoor spawn, but has no defined rect.")
                # --- End Spawn Inside ---

        if spawned_count < count:
            print(f"Warning: Only managed to spawn {spawned_count}/{count} NPCs after {max_attempts} attempts.")

    # --- Add method to get NPCs in a specific building ---
    def get_npcs_in_building(self, building_name):
        """Returns a list of NPCs currently inside the specified building."""
        return [npc for npc in self.all_npcs if npc.current_location_name == building_name]
    # --- End Add ---

    def respawn_npcs(self):
        """Clears existing NPCs and spawns 5 new ones."""
        print("Respawning NPCs for the new day...")
        # --- Clear the single list ---
        self.all_npcs.clear()
        # --- End Change ---
        self.spawn_npcs(5)

    def update(self):
        # Update NPCs that are outside
        for npc in self.all_npcs:
            if npc.current_location_name is None: # Only update world NPCs here
                # Pass the stored time_manager to npc.update
                npc.update(self.time_manager)
        # Interior NPC updates will be handled by the Game class

    def draw(self, screen, camera):
        # Draw locations
        for location in self.locations.values():
            location.draw(screen, camera)

        # Draw NPCs that are outside
        for npc in self.all_npcs:
             if npc.current_location_name is None: # Only draw world NPCs
                npc.draw(screen, camera)
        # Interior NPC drawing will be handled by the Game class