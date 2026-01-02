import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk


# ============================================================================
# DATA MANAGER - Handles all data persistence and monster data structure
# ============================================================================
class DataManager:
    """Manages monster data, saving, and loading operations."""
    
    def __init__(self):
        self.monster_data = self._create_empty_monster()
    
    def _create_empty_monster(self):
        """Create an empty monster data structure."""
        return {
            'name': '',
            'max_health': 0,
            'current_health': 0,
            'abilities': {},  # {name: [max_uses, current_uses]}
            'background_image': None
        }
    
    def get_monster_name(self):
        """Get the monster's name."""
        return self.monster_data['name']
    
    def set_monster_name(self, name):
        """Set the monster's name."""
        self.monster_data['name'] = name
    
    def get_max_health(self):
        """Get the monster's maximum health."""
        return self.monster_data['max_health']
    
    def set_max_health(self, health):
        """Set the monster's maximum health."""
        self.monster_data['max_health'] = health
    
    def get_current_health(self):
        """Get the monster's current health."""
        return self.monster_data['current_health']
    
    def set_current_health(self, health):
        """Set the monster's current health."""
        self.monster_data['current_health'] = max(0, min(health, self.monster_data['max_health']))
    
    def get_abilities(self):
        """Get all abilities."""
        return self.monster_data['abilities']
    
    def add_ability(self, name, max_uses=0):
        """Add a new ability."""
        self.monster_data['abilities'][name] = [max_uses, max_uses]
    
    def remove_ability(self, name):
        """Remove an ability."""
        if name in self.monster_data['abilities']:
            del self.monster_data['abilities'][name]
    
    def use_ability(self, name):
        """Use an ability (decrement its counter). Returns True if successful."""
        if name in self.monster_data['abilities']:
            max_uses, current_uses = self.monster_data['abilities'][name]
            if max_uses > 0 and current_uses > 0:
                self.monster_data['abilities'][name][1] -= 1
                return True
            elif max_uses == 0:
                return True  # Unlimited use ability
        return False
    
    def reset_abilities(self):
        """Reset all ability uses to their maximum."""
        for ability in self.monster_data['abilities']:
            max_uses = self.monster_data['abilities'][ability][0]
            self.monster_data['abilities'][ability][1] = max_uses
    
    def get_background_image(self):
        """Get the background image path."""
        return self.monster_data['background_image']
    
    def set_background_image(self, path):
        """Set the background image path."""
        self.monster_data['background_image'] = path
    
    def save_to_file(self, filename):
        """Save monster data to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.monster_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def load_from_file(self, filename):
        """Load monster data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                self.monster_data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False