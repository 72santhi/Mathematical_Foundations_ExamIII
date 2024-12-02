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




import math
from random import sample

class BullsAndCowsGame:
    def __init__(self):
        self.secret = sample(range(10), 4)  # Secret number (4 unique digits)
        self.attempts = 0
        self.previous_guesses = []  # Track guesses
        self.all_possible_guesses = self.generate_possible_guesses()  # List of all possible guesses at start
        self.valid_guesses = self.all_possible_guesses  # Initially, all possible guesses are valid

    def calculate_bulls_and_cows(self, guess):
        # Calculate number of bulls and cows for a given guess
        bulls = sum(s == g for s, g in zip(self.secret, guess))
        cows = len(set(self.secret) & set(guess)) - bulls
        return bulls, cows

    def generate_possible_guesses(self):
        # Generate all possible valid 4-digit guesses (no repeated digits)
        return [list(map(int, str(i).zfill(4))) for i in range(10000) if len(set(str(i))) == 4]

    def update_valid_guesses(self, guess, bulls, cows):
        # Filter the valid guesses based on bulls and cows feedback
        self.valid_guesses = [
            valid_guess for valid_guess in self.all_possible_guesses
            if self.calculate_bulls_and_cows(valid_guess) == (bulls, cows)
        ]
        print(f"Remaining valid guesses: {len(self.valid_guesses)}")  # Debugging output

    def calculate_entropy(self):
        # Entropy calculation based on the remaining valid guesses
        remaining_possibilities = len(self.valid_guesses)
        if remaining_possibilities > 0:
            entropy = math.log2(remaining_possibilities)  # Log2 of remaining possibilities
        else:
            entropy = 0  # Prevent zero division or negative entropy
        print(f"Entropy: {entropy}")  # Debugging output
        return round(entropy, 2)

    def calculate_mutual_information(self, previous_entropy):
        # Mutual Information is the difference in entropy before and after the guess
        current_entropy = self.calculate_entropy()
        mutual_info = previous_entropy - current_entropy
        print(f"Mutual Information: {mutual_info}")  # Debugging output
        return round(mutual_info, 2)

    def process_guess(self, guess):
        # Validate input (guess should be 4 unique digits)
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            return "Invalid Input: Enter 4 unique digits!"

        guess = list(map(int, guess))
        self.attempts += 1

        # Calculate bulls and cows
        bulls, cows = self.calculate_bulls_and_cows(guess)

        # Calculate entropy before the guess
        previous_entropy = self.calculate_entropy()

        # Update valid guesses based on the feedback (bulls, cows)
        self.update_valid_guesses(guess, bulls, cows)

        # Calculate mutual information after the guess
        mutual_information = self.calculate_mutual_information(previous_entropy)

        # Calculate entropy after the guess
        entropy = self.calculate_entropy()

        # Check if the guess is correct (4 bulls)
        if bulls == 4:
            return f"Congratulations! You guessed the number in {self.attempts} attempts!"

        return bulls, cows, mutual_information, entropy

    def reset_game(self):
        # Reset the game to initial conditions
        self.secret = sample(range(10), 4)
        self.attempts = 0
        self.previous_guesses = []
        self.valid_guesses = self.all_possible_guesses  # Reset valid guesses
