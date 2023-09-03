import os
import json
import tkinter as tk
from tkinter import ttk, filedialog

class UnrealPluginManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Unreal Plugin Manager")

        self.plugins_frame = ttk.Frame(root)
        self.plugins_frame.pack()

        self.project_path = ""
        self.plugins = []

        self.load_default_project()

    def load_default_project(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        uproject_files = [f for f in os.listdir(script_directory) if f.endswith('.uproject')]

        if uproject_files:
            self.project_path = os.path.join(script_directory, uproject_files[0])
            self.load_plugins()
        else:
            self.load_button = ttk.Button(self.root, text="Load .uproject", command=self.load_project)
            self.load_button.pack()

    def load_project(self):
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
        # Update plugin enabled status based on checkboxes
        for plugin_data in self.plugins:
            plugin_name = plugin_data.get("Name", "")
            checkbox_var = self.checkbox_vars.get(plugin_name)
            if checkbox_var is not None:
                plugin_data["Enabled"] = checkbox_var.get()

        # Write back to .uproject file
        with open(self.project_path, "w") as f:
            json.dump({"Plugins": self.plugins}, f, indent=4)

        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UnrealPluginManager(root)
    root.mainloop()
