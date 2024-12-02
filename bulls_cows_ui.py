"""
Bulls and Cows Game UI

This program provides a graphical user interface for the classic "Bulls and Cows" game using the tkinter library.
Players guess a 4-digit number with unique digits, and the game provides feedback in the form of:
- Bulls: Correct digits in the correct position.
- Cows: Correct digits in the wrong position.

Features:
- Multi-page UI (Intro, Rules, and Game pages).
- Interactive input with feedback.
- Display of guesses with advanced metrics (Mutual Information and Entropy).
- Reset functionality to restart the game.

Dependencies:
- tkinter (for UI elements)
- game_logic (custom module handling game logic, including mutual information and entropy calculations)

Author: Santhi Daggubati
Date: 12/01/2024

Instructions:
- Ensure `bull_cows_ui.py` and image files (bg1.gif, bg2.gif) are in the same directory.
- Run the script to launch the game.
"""


import tkinter as tk
from tkinter import messagebox
from game_logic import BullsAndCowsGame

class BullsAndCowsGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulls and Cows Game")
        self.root.geometry("700x500")

        # Initialize the game logic
        self.game = BullsAndCowsGame()

        # Load image paths
        self.intro_image_path = "bg1.gif"  # Replace with your intro image path
        self.game_bg_image_path = "bg2.gif"  # Replace with your game background path

        # Load images
        self.intro_image = tk.PhotoImage(file=self.intro_image_path)
        self.game_bg_image = tk.PhotoImage(file=self.game_bg_image_path)

        # Frames for different pages
        self.intro_frame = tk.Frame(self.root)
        self.rules_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)

        # Initialize pages
        self.create_intro_page()
        self.create_rules_page()
        self.create_game_page()

        # Show intro page
        self.show_intro_page()

        # Resize event
        self.root.bind("<Configure>", self.resize_background)

    def create_intro_page(self):
        self.intro_frame.place(relwidth=1, relheight=1)
        self.intro_canvas = tk.Canvas(self.intro_frame)
        self.intro_canvas.pack(fill="both", expand=True)

    def create_rules_page(self):
        self.rules_frame.place(relwidth=1, relheight=1)
        self.rules_canvas = tk.Canvas(self.rules_frame)
        self.rules_canvas.pack(fill="both", expand=True)
        self.rules_label = tk.Label(
            self.rules_frame,
            text=( 
                "Rules of Bulls and Cows:\n\n"
                "1. Guess the 4-digit number.\n"
                "2. Each digit must be unique.\n"
                "3. 'Bull' means a correct digit in the correct position.\n"
                "4. 'Cow' means a correct digit in the wrong position.\n"
                "5. Continue guessing until you find the secret number!"
            ),
            font=("Arial", 16),
            bg="#FFD700",
            wraplength=700,
        )
        self.rules_label.place(relx=0.5, rely=0.4, anchor="center")
        self.rules_start_button = tk.Button(
            self.rules_frame, text="Proceed to Game", font=("Arial", 16), bg="#00FF7F",
            relief="raised", bd=4, command=self.start_game
        )
        self.rules_start_button.place(relx=0.5, rely=0.8, anchor="center")

    def create_game_page(self):
        self.game_frame.place(relwidth=1, relheight=1)
        self.game_canvas = tk.Canvas(self.game_frame)
        self.game_canvas.pack(fill="both", expand=True)

        # Game widgets
        self.title_label = tk.Label(
            self.game_frame, text="Bulls and Cows Game", font=("Arial", 24, "bold"),
            bg="#FFD700", fg="black"
        )
        self.input_label = tk.Label(
            self.game_frame, text="Enter your guess (4 unique digits):", font=("Arial", 14), bg="#F0F8FF"
        )
        self.input_entry = tk.Entry(self.game_frame, font=("Arial", 14))
        self.submit_button = tk.Button(
            self.game_frame, text="Submit Guess", command=self.process_guess,
            font=("Arial", 14), bg="#7CFC00", relief="raised", bd=4
        )
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 14), bg="#87CEEB")
        self.guesses_list = tk.Listbox(self.game_frame, width=50, height=10, font=("Arial", 12))
        self.reset_button = tk.Button(
            self.game_frame, text="Reset Game", command=self.reset_game,
            font=("Arial", 14), bg="#FF4500", relief="raised", bd=4
        )

        # Place widgets
        self.title_label.place(relx=0.5, y=20, anchor="n")
        self.input_label.place(relx=0.5, y=80, anchor="n")
        self.input_entry.place(relx=0.5, y=120, anchor="n")
        self.submit_button.place(relx=0.5, y=160, anchor="n")
        self.guesses_list.place(relx=0.5, y=240, anchor="n", width=600, height=200)
        self.reset_button.place(relx=0.5, y=450, anchor="n")
        self.feedback_label.place(relx=0.5, y=210, anchor="n")

    def show_intro_page(self):
        self.intro_frame.tkraise()
        self.resize_background()
        self.root.after(3500, self.show_rules_page)

    def show_rules_page(self):
        self.rules_frame.tkraise()
        self.resize_background()

    def start_game(self):
        self.game_frame.tkraise()

    def resize_background(self, event=None):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        self.intro_canvas.delete("all")
        self.rules_canvas.delete("all")
        self.game_canvas.delete("all")

        # Rescale intro background
        self.intro_canvas.create_image(width // 2, height // 2, anchor="center", image=self.intro_image)
        self.rules_canvas.create_image(width // 2, height // 2, anchor="center", image=self.game_bg_image)
        self.game_canvas.create_image(width // 2, height // 2, anchor="center", image=self.game_bg_image)

    def process_guess(self):
        guess = self.input_entry.get()

        result = self.game.process_guess(guess)

        if isinstance(result, str):  # If it's an error message
            messagebox.showerror("Invalid Input", result)
        else:
            bulls, cows, mutual_information, entropy = result
            # Update feedback
            self.feedback_label.config(text=f"Bulls: {bulls}, Cows: {cows}, Mutual Information: {mutual_information} | Entropy: {entropy}")

            # Log the guess in the history list
            self.guesses_list.insert(tk.END, f"Guess: {guess} | Bulls: {bulls} | Cows: {cows} | Mutual Information: {mutual_information} | Entropy: {entropy}")

            # Check for win condition
            if bulls == 4:
                messagebox.showinfo("Congratulations!", f"You guessed the number in {self.game.attempts} attempts!")

    def reset_game(self):
        self.game.reset_game()
        self.guesses_list.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.input_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    game_ui = BullsAndCowsGameUI(root)
    root.mainloop()
