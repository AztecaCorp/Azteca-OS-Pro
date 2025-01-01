import tkinter as tk
from tkinter import filedialog
import pygame
import os

# Initialize pygame mixer for audio
pygame.mixer.init()

# Create a simple music player class
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        self.root.geometry("400x250")
        
        # Initialize variables
        self.current_song = None
        self.is_paused = False
        self.paused_position = 0
        
        # Create buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)
        
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)
        
        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_music, state=tk.DISABLED)
        self.resume_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)
        
        self.load_button = tk.Button(self.root, text="Load Music", command=self.load_music)
        self.load_button.pack(pady=10)
        
        # Label for showing the current song
        self.song_label = tk.Label(self.root, text="No song loaded")
        self.song_label.pack(pady=5)
        
    def load_music(self):
        # Open file dialog to select a music file
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
        
        if file_path:
            self.current_song = file_path
            self.song_label.config(text=f"Playing: {os.path.basename(file_path)}")
            pygame.mixer.music.load(self.current_song)
        
    def play_music(self):
        if self.current_song:
            pygame.mixer.music.play(loops=0, start=0.0)
            self.is_paused = False
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
        else:
            self.song_label.config(text="No song selected!")
        
    def pause_music(self):
        if self.current_song:
            self.paused_position = pygame.mixer.music.get_pos() / 1000.0  # Get current position in seconds
            pygame.mixer.music.pause()
            self.is_paused = True
            self.resume_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
        
    def resume_music(self):
        if self.current_song and self.is_paused:
            pygame.mixer.music.play(loops=0, start=self.paused_position)
            self.is_paused = False
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
        
    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.paused_position = 0
        self.song_label.config(text="No song loaded")
        self.resume_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

# Set up the main Tkinter window
root = tk.Tk()
player = MusicPlayer(root)

# Run the Tkinter event loop
root.mainloop()
