import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageOps
import subprocess


def setup_environment():
    if not os.path.exists('system'):
        os.makedirs('system')
    if not os.path.exists('apps'):
        os.makedirs('apps')

    username = simpledialog.askstring("Setup", "Create your username:")
    password = simpledialog.askstring("Setup", "Create your password:")

    if username and password:
        config = {
            "os_name": "Azteca OS Pro",
            "version": "1.0.0",
            "user": username,
            "password": password,
            "wallpaper": None
        }
        with open('system/config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        messagebox.showinfo("Setup", "Setup complete!")
    else:
        messagebox.showerror("Setup", "Setup was not completed. Please try again.")
        exit()


def load_config():
    with open('system/config.json', 'r') as config_file:
        return json.load(config_file)


def save_config(config):
    with open('system/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


def login_screen(root):
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        config = load_config()
        if username == config['user'] and password == config['password']:
            messagebox.showinfo("Login", "Login successful!")
            root.destroy()
            main_menu()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Login", command=attempt_login).pack(pady=10)


def main_menu():
    menu = tk.Tk()
    menu.title("Azteca OS Pro - Main Menu")
    menu.geometry("800x600")

    config = load_config()
    wallpaper_path = config.get("wallpaper")

    if wallpaper_path and os.path.exists(wallpaper_path):
        bg_image = Image.open(wallpaper_path)
        bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(menu, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)

    def view_system_info():
        messagebox.showinfo(
            "System Info",
            f"OS: {config['os_name']} Version: {config['version']}\nUser: {config['user']}"
        )

    def list_apps():
        apps_dir = 'apps'
        if not os.path.exists(apps_dir):
            os.makedirs(apps_dir)

        apps = [f for f in os.listdir(apps_dir) if f.endswith('.py')]
        if apps:
            apps_list = "\n".join(apps)
            selected_app = simpledialog.askstring(
                "Run App", f"Available Apps:\n{apps_list}\n\nEnter app name to run:")
            if selected_app and selected_app in apps:
                run_app(selected_app)
            else:
                messagebox.showerror(
                    "Run App", "Invalid app name or no app selected.")
        else:
            messagebox.showinfo("Run App", "No apps available.")

    def run_app(app_name):
        app_path = os.path.join('apps', app_name)
        if not os.path.exists(app_path):
            messagebox.showerror("Run App", f"App {app_name} not found.")
            return

        try:
            subprocess.Popen(['python', app_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("Run App", f"Failed to run {app_name}: {e}")

    def change_wallpaper():
        new_wallpaper = filedialog.askopenfilename(
            title="Select Wallpaper",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if new_wallpaper:
            config['wallpaper'] = new_wallpaper
            save_config(config)
            messagebox.showinfo("Wallpaper", "Wallpaper updated! Restart to see changes.")

    tk.Button(menu, text="View System Info", command=view_system_info).pack(pady=10)
    tk.Button(menu, text="Run an App", command=list_apps).pack(pady=10)
    tk.Button(menu, text="Change Wallpaper", command=change_wallpaper).pack(pady=10)
    tk.Button(menu, text="Exit", command=menu.destroy).pack(pady=10)

    menu.mainloop()


if __name__ == "__main__":
    if not os.path.exists('system/config.json'):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        setup_environment()
        root.destroy()

    root = tk.Tk()
    root.title("Azteca OS Pro - Login")
    root.geometry("300x200")
    login_screen(root)
    root.mainloop()
