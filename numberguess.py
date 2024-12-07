import random
def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I have chosen a number between 1 and 100. Can you guess what it is?")
    target_number = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            if guess < target_number:
                print("Too low! Try again.")
            elif guess > target_number:
                print("Too high! Try again.")
            elif guess == target_number:
                print(f"Congratulations! You guessed the number {target_number} correctly in {attempts} attempts!")
                break
        except ValueError:
            print("Please enter a valid number.")
    print("Thanks for playing!")
if __name__ == "__main__":
    number_guessing_game()