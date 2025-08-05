import random

class Functions:
    def __init__(self):
        pass
    
    def generate_random_number(self, min: int = 0, max: int = 100) -> int: 
        """        
        Generate a random integer between min and max (inclusive).
        """
        return random.randint(min, max)

    def match_values(self, value_a, value_b) -> bool:
        """
        Check if two values are equal.
        """
        return value_a == value_b
    
