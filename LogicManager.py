import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

class LogicManager:
    """Manages the application logic and coordinates between UI and data."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.ui_manager = None  # Will be set after UI initialization
    
    def set_ui_manager(self, ui_manager):
        """Set the UI manager reference."""
        self.ui_manager = ui_manager
    
    def initialize_monster(self, name, max_health):
        """Initialize a new monster with the given stats."""
        try:
            max_health = int(max_health)
            self.data_manager.set_monster_name(name)
            self.data_manager.set_max_health(max_health)
            self.data_manager.set_current_health(max_health)
            self.update_ui()
            return True
        except ValueError:
            return False
    
    def apply_damage(self, amount):
        """Apply damage to the monster."""
        try:
            amount = int(amount)
            current = self.data_manager.get_current_health()
            self.data_manager.set_current_health(current - amount)
            self.update_ui()
            return True
        except ValueError:
            return False
    
    def apply_healing(self, amount):
        """Apply healing to the monster."""
        try:
            amount = int(amount)
            current = self.data_manager.get_current_health()
            self.data_manager.set_current_health(current + amount)
            self.update_ui()
            return True
        except ValueError:
            return False
    
    def add_ability(self, name, uses):
        """Add a new ability."""
        if not name.strip():
            return False
        try:
            uses_count = int(uses) if uses else 0
            self.data_manager.add_ability(name, uses_count)
            self.ui_manager.update_abilities_display()
            return True
        except ValueError:
            return False
    
    def use_ability(self, ability_name):
        """Use an ability."""
        success = self.data_manager.use_ability(ability_name)
        if success:
            self.ui_manager.update_abilities_display()
        return success
    
    def remove_ability(self, ability_name):
        """Remove an ability."""
        self.data_manager.remove_ability(ability_name)
        self.ui_manager.update_abilities_display()
    
    def reset_monster(self):
        """Reset the monster to full health and restore abilities."""
        max_health = self.data_manager.get_max_health()
        self.data_manager.set_current_health(max_health)
        self.data_manager.reset_abilities()
        self.update_ui()
    
    def set_background_image(self, path):
        """Set the background image."""
        self.data_manager.set_background_image(path)
        self.ui_manager.update_background_image(path)
    
    def clear_background_image(self):
        """Clear the background image."""
        self.data_manager.set_background_image(None)
        self.ui_manager.update_background_image(None)
    
    def save_monster(self, filename):
        """Save the monster to a file."""
        return self.data_manager.save_to_file(filename)
    
    def load_monster(self, filename):
        """Load a monster from a file."""
        success = self.data_manager.load_from_file(filename)
        if success:
            self.update_ui()
            self.ui_manager.update_abilities_display()
            bg_image = self.data_manager.get_background_image()
            self.ui_manager.update_background_image(bg_image)
        return success
    
    def update_ui(self):
        """Update all UI elements with current data."""
        if self.ui_manager:
            name = self.data_manager.get_monster_name()
            current = self.data_manager.get_current_health()
            maximum = self.data_manager.get_max_health()
            self.ui_manager.update_health_display(current, maximum, name)
    
    def get_abilities_list(self):
        """Get formatted abilities list for display."""
        abilities = self.data_manager.get_abilities()
        result = []
        for name, (max_uses, current_uses) in abilities.items():
            if max_uses > 0:
                result.append(f"{name} ({current_uses}/{max_uses})")
            else:
                result.append(name)
        return result
    
    def get_ability_names(self):
        """Get list of ability names."""
        return list(self.data_manager.get_abilities().keys())
