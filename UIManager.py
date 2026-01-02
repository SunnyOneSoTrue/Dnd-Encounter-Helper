import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

# ============================================================================
# UI MANAGER - Handles all UI components and user interactions
# ============================================================================
class UIManager:
    """Manages all UI components including stats and health bar windows."""
    
    def __init__(self, root, logic_manager):
        self.root = root
        self.logic_manager = logic_manager
        
        # Initialize windows
        self.stats_window = StatsWindow(root, self)
        self.health_bar_window = HealthBarWindow()
        
    def update_health_display(self, current, maximum, name):
        """Update health displays in both windows."""
        self.stats_window.update_current_health(current)
        self.health_bar_window.update_health(current, maximum, name)
    
    def update_abilities_display(self):
        """Update the abilities list display."""
        self.stats_window.update_abilities_list()
    
    def update_background_image(self, path):
        """Update the background image in the health bar window."""
        self.health_bar_window.set_background_image(path)
        self.stats_window.update_image_label(path)


class HealthBarWindow:
    """Manages the Dark Souls-style health bar display window."""
    
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Boss Health Bar")
        self.window.geometry("800x600")
        self.window.configure(bg='black')
        
        self._setup_ui()
        
        self.bg_image_path = None
        self.bg_photo = None
    
    def _setup_ui(self):
        """Set up the UI components."""
        # Background canvas
        self.bg_canvas = tk.Canvas(
            self.window,
            width=800,
            height=600,
            bg='black',
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)
        
        # Boss name label (bottom of screen)
        self.name_label = tk.Label(
            self.window,
            text="",
            font=("Georgia", 20, "bold"),
            fg='#E8E8E8',
            bg='black'
        )
        self.name_label.place(x=400, y=510, anchor='center')
        
        # Health bar container
        self.health_frame = tk.Frame(self.window, bg='black')
        self.health_frame.place(x=400, y=545, anchor='center')
        
        # Health bar canvas
        self.health_bg = tk.Canvas(
            self.health_frame,
            width=700,
            height=20,
            bg='black',
            highlightthickness=0
        )
        self.health_bg.pack()
        
        # Draw health bar background
        self.health_bg.create_rectangle(
            0, 0, 700, 20,
            fill='#1a1a1a',
            outline=''
        )
        
        # Health bar fill
        self.health_bar = self.health_bg.create_rectangle(
            0, 0, 700, 20,
            fill='#8B0000',
            outline=''
        )
    
    def set_background_image(self, image_path):
        """Set the background image."""
        if image_path and os.path.exists(image_path):
            try:
                self.bg_image_path = image_path
                img = Image.open(image_path)
                img = img.resize((800, 600), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(img)
                
                self.bg_canvas.delete("all")
                self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')
                
                self.name_label.config(bg='')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        else:
            self.bg_image_path = None
            self.bg_photo = None
            self.bg_canvas.delete("all")
            self.name_label.config(bg='black')
    
    def update_health(self, current, maximum, name):
        """Update the health bar display."""
        self.name_label.config(text=name)
        
        if current <= 0:
            # Death animation - fade to black
            self.bg_canvas.delete("all")
            self.bg_canvas.config(bg='black')
            self.name_label.place_forget()
            self.health_frame.place_forget()
            self.window.update()
        else:
            # Show widgets
            self.name_label.place(x=400, y=510, anchor='center')
            self.health_frame.place(x=400, y=545, anchor='center')
            
            # Calculate health bar width
            percentage = max(0, current / maximum) if maximum > 0 else 0
            bar_width = 700 * percentage
            
            # Update health bar
            self.health_bg.coords(self.health_bar, 0, 0, bar_width, 20)
            
            # Color based on health percentage (Dark Souls style)
            if percentage > 0.6:
                color = '#8B0000'
            elif percentage > 0.3:
                color = '#A52A2A'
            else:
                color = '#5C0000'
            
            self.health_bg.itemconfig(self.health_bar, fill=color)


class StatsWindow:
    """Manages the stats control window."""
    
    def __init__(self, root, ui_manager):
        self.root = root
        self.ui_manager = ui_manager
        self.logic_manager = ui_manager.logic_manager
        
        self.root.title("Dungeon Master - Monster Stats")
        self.root.geometry("500x700")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._create_monster_info_section(main_frame)
        self._create_abilities_section(main_frame)
        self._create_damage_section(main_frame)
        self._create_control_buttons(main_frame)
        self._create_background_section(main_frame)
    
    def _create_monster_info_section(self, parent):
        """Create the monster information section."""
        # Monster name
        ttk.Label(parent, text="Monster Name:", font=("Arial", 12, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.name_entry = ttk.Entry(parent, width=30, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Max health
        ttk.Label(parent, text="Max Health:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.max_health_entry = ttk.Entry(parent, width=30, font=("Arial", 11))
        self.max_health_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Current health
        ttk.Label(parent, text="Current Health:", font=("Arial", 12, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.current_health_label = ttk.Label(parent, text="0", font=("Arial", 11))
        self.current_health_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
    
    def _create_abilities_section(self, parent):
        """Create the abilities section."""
        ttk.Label(parent, text="Abilities:", font=("Arial", 12, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        # Abilities list
        abilities_frame = ttk.Frame(parent)
        abilities_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.abilities_listbox = tk.Listbox(abilities_frame, height=6, font=("Arial", 10))
        self.abilities_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(abilities_frame, orient=tk.VERTICAL, command=self.abilities_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.abilities_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add ability controls
        ability_input_frame = ttk.Frame(parent)
        ability_input_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.ability_name_entry = ttk.Entry(ability_input_frame, width=20)
        self.ability_name_entry.grid(row=0, column=0, padx=2)
        
        ttk.Label(ability_input_frame, text="Uses:").grid(row=0, column=1, padx=2)
        
        self.ability_uses_entry = ttk.Entry(ability_input_frame, width=5)
        self.ability_uses_entry.grid(row=0, column=2, padx=2)
        
        ttk.Button(ability_input_frame, text="Add Ability", command=self._on_add_ability).grid(
            row=0, column=3, padx=5
        )
        ttk.Button(ability_input_frame, text="Use Ability", command=self._on_use_ability).grid(
            row=0, column=4, padx=2
        )
        ttk.Button(ability_input_frame, text="Remove", command=self._on_remove_ability).grid(
            row=0, column=5, padx=2
        )
    
    def _create_damage_section(self, parent):
        """Create the damage/healing section."""
        ttk.Label(parent, text="Damage/Healing:", font=("Arial", 12, "bold")).grid(
            row=6, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        damage_frame = ttk.Frame(parent)
        damage_frame.grid(row=7, column=0, columnspan=2, pady=5)
        
        self.damage_entry = ttk.Entry(damage_frame, width=10)
        self.damage_entry.grid(row=0, column=0, padx=5)
        
        ttk.Button(damage_frame, text="Apply Damage", command=self._on_apply_damage).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(damage_frame, text="Apply Healing", command=self._on_apply_healing).grid(
            row=0, column=2, padx=5
        )
    
    def _create_control_buttons(self, parent):
        """Create the control buttons section."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(control_frame, text="Initialize Monster", command=self._on_initialize).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(control_frame, text="Save Monster", command=self._on_save).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(control_frame, text="Load Monster", command=self._on_load).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(control_frame, text="Reset", command=self._on_reset).grid(
            row=0, column=3, padx=5
        )
    
    def _create_background_section(self, parent):
        """Create the background image section."""
        ttk.Label(parent, text="Background Image:", font=("Arial", 12, "bold")).grid(
            row=9, column=0, sticky=tk.W, pady=(10, 5)
        )
        
        image_button_frame = ttk.Frame(parent)
        image_button_frame.grid(row=10, column=0, columnspan=2, pady=5)
        
        ttk.Button(image_button_frame, text="Set Background Image", command=self._on_set_background).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(image_button_frame, text="Clear Background", command=self._on_clear_background).grid(
            row=0, column=1, padx=5
        )
        
        self.image_path_label = ttk.Label(parent, text="No image set", font=("Arial", 9), foreground="gray")
        self.image_path_label.grid(row=11, column=0, columnspan=2, pady=5)
    
    # Event handlers
    def _on_initialize(self):
        """Handle initialize monster button."""
        name = self.name_entry.get() or "Unknown Monster"
        max_health = self.max_health_entry.get()
        
        if self.logic_manager.initialize_monster(name, max_health):
            messagebox.showinfo("Success", "Monster initialized!")
        else:
            messagebox.showerror("Error", "Please enter valid health values")
    
    def _on_add_ability(self):
        """Handle add ability button."""
        name = self.ability_name_entry.get()
        uses = self.ability_uses_entry.get()
        
        if not name.strip():
            messagebox.showwarning("Warning", "Please enter an ability name")
            return
        
        if self.logic_manager.add_ability(name, uses):
            self.ability_name_entry.delete(0, tk.END)
            self.ability_uses_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Uses must be a number")
    
    def _on_use_ability(self):
        """Handle use ability button."""
        selection = self.abilities_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ability")
            return
        
        idx = selection[0]
        ability_names = self.logic_manager.get_ability_names()
        if idx < len(ability_names):
            ability_name = ability_names[idx]
            if not self.logic_manager.use_ability(ability_name):
                messagebox.showinfo("Info", "No uses remaining for this ability")
    
    def _on_remove_ability(self):
        """Handle remove ability button."""
        selection = self.abilities_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ability to remove")
            return
        
        idx = selection[0]
        ability_names = self.logic_manager.get_ability_names()
        if idx < len(ability_names):
            ability_name = ability_names[idx]
            self.logic_manager.remove_ability(ability_name)
    
    def _on_apply_damage(self):
        """Handle apply damage button."""
        amount = self.damage_entry.get()
        if self.logic_manager.apply_damage(amount):
            self.damage_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a valid damage amount")
    
    def _on_apply_healing(self):
        """Handle apply healing button."""
        amount = self.damage_entry.get()
        if self.logic_manager.apply_healing(amount):
            self.damage_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a valid healing amount")
    
    def _on_save(self):
        """Handle save monster button."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.logic_manager.save_monster(filename):
                messagebox.showinfo("Success", "Monster saved!")
            else:
                messagebox.showerror("Error", "Failed to save monster")
    
    def _on_load(self):
        """Handle load monster button."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.logic_manager.load_monster(filename):
                # Update input fields
                data_manager = self.logic_manager.data_manager
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, data_manager.get_monster_name())
                
                self.max_health_entry.delete(0, tk.END)
                self.max_health_entry.insert(0, str(data_manager.get_max_health()))
                
                messagebox.showinfo("Success", "Monster loaded!")
            else:
                messagebox.showerror("Error", "Failed to load monster")
    
    def _on_reset(self):
        """Handle reset button."""
        self.logic_manager.reset_monster()
    
    def _on_set_background(self):
        """Handle set background image button."""
        filename = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.logic_manager.set_background_image(filename)
    
    def _on_clear_background(self):
        """Handle clear background button."""
        self.logic_manager.clear_background_image()
    
    # Display update methods
    def update_current_health(self, health):
        """Update the current health display."""
        self.current_health_label.config(text=str(health))
    
    def update_abilities_list(self):
        """Update the abilities listbox."""
        self.abilities_listbox.delete(0, tk.END)
        abilities = self.logic_manager.get_abilities_list()
        for ability in abilities:
            self.abilities_listbox.insert(tk.END, ability)
    
    def update_image_label(self, path):
        """Update the background image label."""
        if path:
            filename = os.path.basename(path)
            self.image_path_label.config(text=f"Image: {filename}", foreground="green")
        else:
            self.image_path_label.config(text="No image set", foreground="gray")
