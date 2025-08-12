import random
from models import GameLevel

class Game:
    def __init__(self, level: str = 'easy', set_default_level: bool = True):
        self.number_to_guess = None
        self.continue_game: bool = False
        self.attempts = 0
        self.guesses = set()
        self.level: dict = {}
        self.levels: dict = {
            'easy': {'min': 1, 'max': 10},
            'medium': {'min': 1, 'max': 50},
            'hard': {'min': 1, 'max': 100},
            'hard-2': {'min': 1, 'max': 10000},
            'hard-3': {'min': 1, 'max': 100000},
            'extreme': {'min': 1, 'max': 1000000}
        }

        if set_default_level: self.set_level(level, set_default=set_default_level)

    
    def set_levels(self, levels: dict) -> None:
        self.levels = GameLevel


    def set_level(self, level: str = None, set_default: bool = False) -> bool:

        if set_default: 
            self.level: dict = self.levels['easy']
            return True

        if level in self.levels:
            self.level = self.levels[level]
            print(f"Level set to {level}. Range is {self.level['min']} to {self.level['max']}.")
            return True
        else:
            print("Invalid level selected.")
            return False

    def generate_random_number(self, min: int = 0, max: int = 100) -> int: return random.randint(min, max)

    def match_values(self, value_a, value_b) -> bool: return value_a == value_b
    
    def start_game(self, number:int = None) -> None:
        self.number_to_guess = number if number is not None else self.generate_random_number(self.level['min'], self.level['max'])
        self.attempts = 0
        self.continue_game: bool = True
        self.guesses.clear()

    def make_guess(self, guess):
        self.attempts += 1

        if guess in self.guesses: return (False, "You've already guessed that number. Try again.")
        
        self.guesses.add(guess)

        if guess < self.number_to_guess: return (False, "Higher!")
        elif guess > self.number_to_guess: return (False, "Lower!")
        else: return (True, "Correct! You've guessed the number in {} attempts.".format(self.attempts))
        