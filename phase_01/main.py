from fns import Functions

if __name__ == "__main__":
    # Create an instance of the Functions class
    fns = Functions()

    input_number = 8 # Example input number for testing

    random_number = fns.generate_random_number()
    guess_check = fns.match_values(input_number, random_number)

    print(f"Random Number: {random_number}")
    print(f"Input Number: {input_number}")
    print(f"Do the numbers match? {'Yes' if guess_check else 'No'}")

    