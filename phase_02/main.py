from game import Game




if __name__ == "__main__":
   
    game = Game()
    game.start_game()  # Start the game with a random number

    input_number = 8 # Example input number for testing

    win, msg = game.make_guess(input_number)  # Make a guess with the input number

    

    print(f"Random Number: {game.number_to_guess}")
    print(f"Input Number: {input_number}")
    print(f"Do the numbers match? {'Yes' if win else 'No'}")
    print(msg)  # Print the message returned from make_guess


    
    
