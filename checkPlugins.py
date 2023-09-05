#!/usr/bin/env python3

"""
Unreal Plugin Manager

This script provides a GUI tool to manage plugins in an Unreal project.
The user can:
- Browse to an Unreal project folder.
- View a list of plugins in the project.
- Enable or disable plugins using checkboxes.
- Save changes to the project file.

Usage:
Run the script, and the GUI will appear. From there, you can browse to your Unreal project folder,
select or deselect plugins, and save your changes.

Requirements:
- tkinter
"""
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class UnrealPluginManager:
    """
    A class to represent the Unreal Plugin Manager GUI.
    
    Attributes:
    - root: The main tkinter window.
    - plugins_frame: Frame to hold the plugins list.
    - project_path: Path to the selected Unreal project.
    - plugins: List of plugins in the project.
    """
    def __init__(self, root):
        """Initialize the GUI components."""
        self.root = root
        self.root.title("Unreal Plugin Manager")

        self.plugins_frame = ttk.Frame(root)
        self.plugins_frame.pack(pady=10)

        self.project_path = ""
        self.plugins = []

        # Add Select All and Deselect All buttons
        self.button_frame = ttk.Frame(self.plugins_frame)
        self.button_frame.pack(pady=10)

        self.select_all_button = ttk.Button(self.button_frame, text="Select All", command=self.select_all_plugins)
        self.select_all_button.pack(side=tk.LEFT, padx=5)

        self.deselect_all_button = ttk.Button(self.button_frame, text="Deselect All", command=self.deselect_all_plugins)
        self.deselect_all_button.pack(side=tk.LEFT, padx=5)

        self.load_default_project()

    def load_default_project(self):
         # Add a button to select the Unreal project folder
        self.browse_button = ttk.Button(self.root, text="Browse Unreal Project Folder", command=self.browse_folder)
        self.browse_button.pack(pady=10)
    def browse_folder(self):
        """
        Open a directory browser and let the user select an Unreal project folder.
        If a valid project is found, load the plugins from it.
        """
    # Ask the user to select a directory
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            uproject_files = [f for f in os.listdir(selected_directory) if f.endswith('.uproject')]
            if uproject_files:
                self.project_path = os.path.join(selected_directory, uproject_files[0])
                self.load_plugins()
            else:
                tk.messagebox.showwarning("Warning", "No .uproject files found in the selected directory!")

    def select_all_plugins(self):
    
        """Select all plugins."""
        for var in self.checkbox_vars.values():
            var.set(True)

    def deselect_all_plugins(self):
        """Deselect all plugins."""
        for var in self.checkbox_vars.values():
            var.set(False)

    def load_default_project(self):
        """Load the plugins from the default(Current directory) Unreal project."""
        script_directory = os.path.dirname(os.path.abspath(__file__))
        uproject_files = [f for f in os.listdir(script_directory) if f.endswith('.uproject')]

        if uproject_files:
            self.project_path = os.path.join(script_directory, uproject_files[0])
            self.load_plugins()
        else:
            self.load_button = ttk.Button(self.root, text="Load .uproject", command=self.load_project)
            self.load_button.pack()

    def load_project(self):
        """Load the plugins from the selected Unreal project."""
        self.project_path = filedialog.askopenfilename(filetypes=[("Unreal Project Files", "*.uproject")])
        if self.project_path:
            self.load_plugins()

    def load_plugins(self):
        # Read and parse .uproject file
        with open(self.project_path, "r") as f:
            uproject_data = json.load(f)

        # Extract enabled plugins
        self.plugins = uproject_data.get("Plugins", [])

        # Create plugin checkboxes
        self.checkbox_vars = {}
        for plugin_data in self.plugins:
            plugin_name = plugin_data.get("Name", "")
            enabled = plugin_data.get("Enabled", False)
            checkbox_var = tk.BooleanVar(value=enabled)
            self.checkbox_vars[plugin_name] = checkbox_var
            checkbox = ttk.Checkbutton(self.plugins_frame, text=plugin_name, variable=checkbox_var)
            checkbox.pack()

        save_button = ttk.Button(self.root, text="Save", command=self.save_plugins)
        save_button.pack()

    def save_plugins(self):
        # Define the provided content
        header_data = {
            "FileVersion": 3,
            "EngineAssociation": "5.2",
            "Category": "",
            "Description": ""
        }
        # Update plugin enabled status based on checkboxes
        for plugin_data in self.plugins:
            plugin_name = plugin_data.get("Name", "")
            checkbox_var = self.checkbox_vars.get(plugin_name)
            if checkbox_var is not None:
                plugin_data["Enabled"] = checkbox_var.get()
        # Merge the header data with the modified plugins data
        save_data = {**header_data, "Plugins": self.plugins}
    
        # Write back to .uproject file
        with open(self.project_path, "w") as f:
            json.dump(save_data, f, indent=4)
        tk.messagebox.showinfo("Information", "File Saved Successfully!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UnrealPluginManager(root)
    root.mainloop()
