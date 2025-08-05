# guessing-game
A game where users guess the number that the system generated


## Project Build Phases

### Phase 1 (Basic functions)
Derive and test basic game functionalities:
* Generating a random number
* Testing if a given number matches the randomly generated number

### Phase 2 (Game class)
Create class of all the relevant functionality and add more functions
* Set relevant game class properties
    * number_to_guess
    * continue_game
    * attempts
    * guesses
    * levels
    * level
* set_level()
* generate_random_number()
* make_guess()
* start_game()

### Phase 3 (Command-line game)
Use game functions to create a game that can be played on the terminal
* Import and initialise the game class in a separate file/script
* Create a function that prompt user to set level based of predefined levels
* Once a level has been set, start the game and prompt the user for a number within the range based on the selected level
* Check if the guess is correct
    * If the guess is incorrect, ask the user to try again
    * If the guess is correct, congratulate the user and tell them how many attempts it took to guess the correct number
* At all times, the user should have the option to exit the game by either using the word “exit” or the letter “q”

### Phase 4 (FastAPI and SQLite)
Design a database table to store player information and player sessions.
* Design models using FastAPI connected to SQLite database
* Create CRUD API endpoints for database tables

### Phase 5 (Login and session management)
Create functionality to login in order to use the API

### Phase 6 (Game code redesign)
Re-design game code to make functionality accessible from/through the API

### Phase 7 (Frontend part 1)
Create a web page using ReactJS
* Login page
    * Username and passwords fields
    * Validate user login against API
    * Store session key upon valid login

### Phase 8 (Frontend part 2)
* Main game page
    * Accessible only after login
    * Prompts user to enter a number in a field (guess)
    * Checks if guess is correct against the API
    * Shows response message from the API 