import tkinter as tk
from tkinter import ttk
import pyperclip
from PIL import Image, ImageTk
from database import create_database, fetch_word_from_wordnet, store_words_in_database, get_word_count
from random_seed import generate_game_seed_from_database
import threading


class SeedGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Seed Generator")

        # Get window width
        self.update_idletasks()
        window_width = self.winfo_width()

        # Load and resize the banner image
        pil_image = Image.open('images/banner.png')
        aspect_ratio = pil_image.height / pil_image.width
        new_height = int(aspect_ratio * window_width)
        pil_image_resized = pil_image.resize((window_width, new_height))

        self.banner_image = ImageTk.PhotoImage(pil_image_resized)
        self.banner_label = tk.Label(self, image=self.banner_image)
        self.banner_label.pack(pady=10)

        # Create Database Button
        self.create_db_btn = tk.Button(self, text="Create/Recreate Database",
                                       command=self.create_database_with_progress)
        self.create_db_btn.pack(pady=20)

        # Generate Seed Button
        self.generate_seed_btn = tk.Button(self, text="Generate Seed", command=self.generate_seed)
        self.generate_seed_btn.pack(pady=20)

        # Seed Label
        self.seed_label = tk.Label(self, text="")
        self.seed_label.pack(pady=20)

        # Copy to Clipboard Button
        self.copy_btn = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_btn.pack(pady=20)

        # Progress bar frame
        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(pady=20)

        # Current word label
        self.current_word_label = tk.Label(self.progress_frame, text="")
        self.current_word_label.pack()

        # Progress Bar
        self.progress = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(fill=tk.X, expand=True)

        # Cancel button
        self.cancel_btn = tk.Button(self, text="Cancel", command=self.cancel_database_creation, state=tk.DISABLED)
        self.cancel_btn.pack(pady=20)

        # Word count label
        self.word_count_label = tk.Label(self, text="Words in database: 0")
        self.word_count_label.pack(pady=10)

        self.creating_database = False

    def create_database_with_progress(self):
        self.progress["maximum"] = 2000
        self.progress["value"] = 0
        self.create_db_btn["state"] = tk.DISABLED
        self.cancel_btn["state"] = tk.NORMAL
        self.creating_database = True

        # Separate thread for database creation
        thread = threading.Thread(target=self.threaded_db_creation)
        thread.start()

    def threaded_db_creation(self):
        create_database()
        for i in range(200):
            if not self.creating_database:
                break
            word = fetch_word_from_wordnet()
            self.current_word_label["text"] = f"Adding: {word}"
            store_words_in_database(num_words=1)
            self.progress["value"] = i + 1
            self.update_idletasks()

        if self.creating_database:
            self.current_word_label["text"] = "Database build completed."

        # Reset buttons
        self.create_db_btn["state"] = tk.NORMAL
        self.cancel_btn["state"] = tk.DISABLED

        # Update word count label
        word_count = get_word_count()
        self.word_count_label["text"] = f"Words in database: {word_count}"

    def generate_seed(self):
        seed = generate_game_seed_from_database()
        self.seed_label["text"] = seed
        self.copy_btn["state"] = tk.NORMAL

    def copy_to_clipboard(self):
        seed = self.seed_label["text"]
        pyperclip.copy(seed)

    def cancel_database_creation(self):
        self.creating_database = False


if __name__ == "__main__":

    app = SeedGeneratorApp()
    app.mainloop()
