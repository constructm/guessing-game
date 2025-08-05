from game import Game

def set_level(game: Game):
    level_set = False

    while not level_set:
        selected_level = input(f"Select difficulty level {list(game.levels.keys())}: ").strip().lower()

        if selected_level in game.levels:
            game.set_level(selected_level)
            level_set = True
            return True
        elif selected_level in ('q', 'exit'):
            print("Exiting the game.")
            return False
        else:
            print("Invalid level selected.")


if __name__ == "__main__":
   
    game = Game(set_default_level=False)
    confirm = set_level(game)

    if not confirm: exit() # if no level is set, exit the game

    game.start_game()
    print(f"Starting game with level: {game.level['min']} to {game.level['max']}")
    print("Type 'q' or 'exit' to quit the game at any time.")

    while game.continue_game:
        user_input = input(f"Guess a number between {game.level['min']} and {game.level['max']}: ").strip().lower()
        if user_input.isdigit():
            input_number = int(user_input)
            win, message = game.make_guess(input_number)
            print(message)

            if win: game.continue_game = False
        else:
            if user_input in ('q','exit'):
                game.continue_game = False
                print("Exiting the game. Thank you for playing!")
                break
