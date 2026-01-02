import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class HealthBarWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Boss Health Bar")
        self.window.geometry("800x600")
        self.window.configure(bg='black')
        
        # Boss name label
        self.name_label = tk.Label(
            self.window,
            text="",
            font=("Georgia", 28, "bold"),
            fg='#FFD700',
            bg='black'
        )
        self.name_label.pack(pady=(150, 20))
        
        # Health bar container
        self.health_frame = tk.Frame(self.window, bg='black')
        self.health_frame.pack(pady=20)
        
        # Health bar background
        self.health_bg = tk.Canvas(
            self.health_frame,
            width=600,
            height=40,
            bg='black',
            highlightthickness=0
        )
        self.health_bg.pack()
        
        # Draw health bar border
        self.health_bg.create_rectangle(
            2, 2, 598, 38,
            outline='#8B4513',
            width=3
        )
        
        # Health bar fill
        self.health_bar = self.health_bg.create_rectangle(
            5, 5, 595, 35,
            fill='#DC143C',
            outline=''
        )
        
        # Health text
        self.health_text = tk.Label(
            self.window,
            text="",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='black'
        )
        self.health_text.pack(pady=10)
        
        self.max_health = 100
        self.current_health = 100
        
    def update_health(self, current, maximum, name):
        self.current_health = current
        self.max_health = maximum
        self.name_label.config(text=name)
        
        if current <= 0:
            # Death animation
            self.window.configure(bg='black')
            for widget in self.window.winfo_children():
                widget.pack_forget()
            self.window.update()
        else:
            # Update health bar
            percentage = max(0, current / maximum)
            bar_width = 590 * percentage
            
            self.health_bg.coords(self.health_bar, 5, 5, 5 + bar_width, 35)
            
            # Change color based on health percentage
            if percentage > 0.6:
                color = '#DC143C'  # Red
            elif percentage > 0.3:
                color = '#FF8C00'  # Orange
            else:
                color = '#8B0000'  # Dark red
            
            self.health_bg.itemconfig(self.health_bar, fill=color)
            
            self.health_text.config(text=f"{int(current)} / {int(maximum)}")

class StatsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Master - Monster Stats")
        self.root.geometry("500x700")
        
        # Create health bar window
        self.health_window = HealthBarWindow()
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Monster name
        ttk.Label(main_frame, text="Monster Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Health
        ttk.Label(main_frame, text="Max Health:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_health_entry = ttk.Entry(main_frame, width=30, font=("Arial", 11))
        self.max_health_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(main_frame, text="Current Health:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.current_health_label = ttk.Label(main_frame, text="0", font=("Arial", 11))
        self.current_health_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Abilities section
        ttk.Label(main_frame, text="Abilities:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky=tk.W, pady=(15, 5))
        
        # Abilities list frame
        abilities_frame = ttk.Frame(main_frame)
        abilities_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.abilities_listbox = tk.Listbox(abilities_frame, height=6, font=("Arial", 10))
        self.abilities_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(abilities_frame, orient=tk.VERTICAL, command=self.abilities_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.abilities_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add ability
        ability_input_frame = ttk.Frame(main_frame)
        ability_input_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.ability_name_entry = ttk.Entry(ability_input_frame, width=20)
        self.ability_name_entry.grid(row=0, column=0, padx=2)
        ttk.Label(ability_input_frame, text="Uses:").grid(row=0, column=1, padx=2)
        self.ability_uses_entry = ttk.Entry(ability_input_frame, width=5)
        self.ability_uses_entry.grid(row=0, column=2, padx=2)
        
        ttk.Button(ability_input_frame, text="Add Ability", command=self.add_ability).grid(row=0, column=3, padx=5)
        ttk.Button(ability_input_frame, text="Use Ability", command=self.use_ability).grid(row=0, column=4, padx=2)
        ttk.Button(ability_input_frame, text="Remove", command=self.remove_ability).grid(row=0, column=5, padx=2)
        
        # Damage/Healing section
        ttk.Label(main_frame, text="Damage/Healing:", font=("Arial", 12, "bold")).grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        
        damage_frame = ttk.Frame(main_frame)
        damage_frame.grid(row=7, column=0, columnspan=2, pady=5)
        
        self.damage_entry = ttk.Entry(damage_frame, width=10)
        self.damage_entry.grid(row=0, column=0, padx=5)
        
        ttk.Button(damage_frame, text="Apply Damage", command=self.apply_damage).grid(row=0, column=1, padx=5)
        ttk.Button(damage_frame, text="Apply Healing", command=self.apply_healing).grid(row=0, column=2, padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(control_frame, text="Initialize Monster", command=self.initialize_monster).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Save Monster", command=self.save_monster).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Load Monster", command=self.load_monster).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset_monster).grid(row=0, column=3, padx=5)
        
        # Data storage
        self.abilities = {}  # {name: [max_uses, current_uses]}
        self.current_health = 0
        self.max_health = 0
        
    def add_ability(self):
        name = self.ability_name_entry.get().strip()
        uses = self.ability_uses_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter an ability name")
            return
        
        try:
            uses_count = int(uses) if uses else 0
        except ValueError:
            messagebox.showwarning("Warning", "Uses must be a number")
            return
        
        self.abilities[name] = [uses_count, uses_count]
        self.update_abilities_list()
        
        self.ability_name_entry.delete(0, tk.END)
        self.ability_uses_entry.delete(0, tk.END)
    
    def update_abilities_list(self):
        self.abilities_listbox.delete(0, tk.END)
        for name, (max_uses, current_uses) in self.abilities.items():
            if max_uses > 0:
                display = f"{name} ({current_uses}/{max_uses})"
            else:
                display = name
            self.abilities_listbox.insert(tk.END, display)
    
    def use_ability(self):
        selection = self.abilities_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ability")
            return
        
        idx = selection[0]
        ability_name = list(self.abilities.keys())[idx]
        max_uses, current_uses = self.abilities[ability_name]
        
        if max_uses > 0:
            if current_uses > 0:
                self.abilities[ability_name][1] -= 1
                self.update_abilities_list()
            else:
                messagebox.showinfo("Info", "No uses remaining for this ability")
    
    def remove_ability(self):
        selection = self.abilities_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ability to remove")
            return
        
        idx = selection[0]
        ability_name = list(self.abilities.keys())[idx]
        del self.abilities[ability_name]
        self.update_abilities_list()
    
    def initialize_monster(self):
        try:
            self.max_health = int(self.max_health_entry.get())
            self.current_health = self.max_health
            self.current_health_label.config(text=str(self.current_health))
            
            name = self.name_entry.get() or "Unknown Monster"
            self.health_window.update_health(self.current_health, self.max_health, name)
            
            messagebox.showinfo("Success", "Monster initialized!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid health values")
    
    def apply_damage(self):
        try:
            damage = int(self.damage_entry.get())
            self.current_health = max(0, self.current_health - damage)
            self.current_health_label.config(text=str(self.current_health))
            
            name = self.name_entry.get() or "Unknown Monster"
            self.health_window.update_health(self.current_health, self.max_health, name)
            
            self.damage_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid damage amount")
    
    def apply_healing(self):
        try:
            healing = int(self.damage_entry.get())
            self.current_health = min(self.max_health, self.current_health + healing)
            self.current_health_label.config(text=str(self.current_health))
            
            name = self.name_entry.get() or "Unknown Monster"
            self.health_window.update_health(self.current_health, self.max_health, name)
            
            self.damage_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid healing amount")
    
    def save_monster(self):
        data = {
            'name': self.name_entry.get(),
            'max_health': self.max_health,
            'current_health': self.current_health,
            'abilities': self.abilities
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", "Monster saved!")
    
    def load_monster(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, data['name'])
            
            self.max_health_entry.delete(0, tk.END)
            self.max_health_entry.insert(0, str(data['max_health']))
            
            self.max_health = data['max_health']
            self.current_health = data['current_health']
            self.current_health_label.config(text=str(self.current_health))
            
            self.abilities = data['abilities']
            self.update_abilities_list()
            
            name = data['name']
            self.health_window.update_health(self.current_health, self.max_health, name)
            
            messagebox.showinfo("Success", "Monster loaded!")
    
    def reset_monster(self):
        self.current_health = self.max_health
        self.current_health_label.config(text=str(self.current_health))
        
        # Reset ability uses
        for ability in self.abilities:
            self.abilities[ability][1] = self.abilities[ability][0]
        self.update_abilities_list()
        
        name = self.name_entry.get() or "Unknown Monster"
        self.health_window.update_health(self.current_health, self.max_health, name)

if __name__ == "__main__":
    root = tk.Tk()
    app = StatsWindow(root)
    root.mainloop()