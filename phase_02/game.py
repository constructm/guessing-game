import random

class Game:
    def __init__(self):
        self.number_to_guess = None
        self.continue_game: bool = False
        self.attempts = 0
        self.guesses = set()
        
    def generate_random_number(self, min: int = 0, max: int = 100) -> int: return random.randint(min, max)

    def match_values(self, value_a, value_b) -> bool: return value_a == value_b
    
    def start_game(self) -> None:
        self.number_to_guess = self.generate_random_number(1, 100)
        self.attempts = 0
        self.continue_game: bool = True

    def make_guess(self, guess):
        self.attempts += 1

        if guess in self.guesses: return (False, "You've already guessed that number. Try again.")
        
        self.guesses.add(guess)

        if guess < self.number_to_guess: return (False, "Higher!")
        elif guess > self.number_to_guess: return (False, "Lower!")
        else: return (True, "Correct! You've guessed the number in {} attempts.".format(self.attempts))
        