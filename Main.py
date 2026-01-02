import DataManager
import LogicManager
import UIManager
import tkinter as tk
# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Initialize and
    run the application."""
    root = tk.Tk()
    
    # Create managers
    data_manager = DataManager.DataManager()
    logic_manager = LogicManager.LogicManager(data_manager)
    ui_manager = UIManager.UIManager(root, logic_manager)
    
    # Connect logic manager to UI
    logic_manager.set_ui_manager(ui_manager)
    
    root.mainloop()


if __name__ == "__main__":
    main()