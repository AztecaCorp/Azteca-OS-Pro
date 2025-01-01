import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os
import shutil

class FileSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File System App")

        # Get the directory where the script is located
        self.app_directory = os.path.dirname(os.path.abspath(__file__))

        # Set the starting root directory to the "root" folder located in the same directory as the script
        self.root_directory = os.path.join(self.app_directory, "root")

        # Check if the root directory exists, if not, create it
        if not os.path.exists(self.root_directory):
            os.makedirs(self.root_directory)

        self.current_directory = self.root_directory  # Set the current directory to root

        # Set up the directory display
        self.directory_label = tk.Label(self.root, text="Current Directory: " + self.current_directory, font=("Arial", 12))
        self.directory_label.pack(pady=10)

        # Create the listbox to display files and directories
        self.file_listbox = tk.Listbox(self.root, width=60, height=15)
        self.file_listbox.pack(pady=10)

        # Buttons for file operations
        self.open_button = tk.Button(self.root, text="Open", width=20, command=self.open_item)
        self.open_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete", width=20, command=self.delete_item)
        self.delete_button.pack(pady=5)

        self.create_folder_button = tk.Button(self.root, text="Create Folder", width=20, command=self.create_folder)
        self.create_folder_button.pack(pady=5)

        self.create_file_button = tk.Button(self.root, text="Create File", width=20, command=self.create_file)
        self.create_file_button.pack(pady=5)

        self.leave_folder_button = tk.Button(self.root, text="Leave Folder", width=20, command=self.leave_folder)
        self.leave_folder_button.pack(pady=5)

        # Refresh the file list on start
        self.refresh_file_list()

    def refresh_file_list(self):
        """Refresh the list of files and directories in the current directory."""
        self.file_listbox.delete(0, tk.END)
        try:
            for item in os.listdir(self.current_directory):
                self.file_listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Permission Error", "You do not have permission to view this directory.")

    def open_item(self):
        """Open the selected file or folder."""
        try:
            selected_item = self.file_listbox.get(tk.ACTIVE)
            selected_path = os.path.join(self.current_directory, selected_item)
            if os.path.isfile(selected_path):
                os.startfile(selected_path)
            elif os.path.isdir(selected_path):
                self.current_directory = selected_path
                self.directory_label.config(text="Current Directory: " + self.current_directory)
                self.refresh_file_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_item(self):
        """Delete the selected file or directory."""
        try:
            selected_item = self.file_listbox.get(tk.ACTIVE)
            selected_path = os.path.join(self.current_directory, selected_item)
            if os.path.isfile(selected_path):
                os.remove(selected_path)
            elif os.path.isdir(selected_path):
                shutil.rmtree(selected_path)
            self.refresh_file_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_folder(self):
        """Create a new folder."""
        folder_name = simpledialog.askstring("Create Folder", "Enter the folder name:")
        if folder_name:
            new_folder_path = os.path.join(self.current_directory, folder_name)
            try:
                os.makedirs(new_folder_path)
                self.refresh_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_file(self):
        """Create a new file."""
        file_name = simpledialog.askstring("Create File", "Enter the file name:")
        if file_name:
            new_file_path = os.path.join(self.current_directory, file_name)
            try:
                with open(new_file_path, 'w') as file:
                    pass  # Create an empty file
                self.refresh_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def leave_folder(self):
        """Navigate to the parent folder."""
        parent_folder = os.path.dirname(self.current_directory)
        if parent_folder != self.root_directory:  # Don't go above the root folder
            self.current_directory = parent_folder
            self.directory_label.config(text="Current Directory: " + self.current_directory)
            self.refresh_file_list()
        else:
            messagebox.showinfo("Info", "You are already in the root folder.")

# Create the main window
root = tk.Tk()
app = FileSystemApp(root)

# Run the Tkinter event loop
root.mainloop()
