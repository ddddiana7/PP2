import random

def guess():
    print("Hello! What is your name?")

    name = input()

    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    number = random.randint(1, 20)

    guesses = 0

    while True:
        print("Take a guess")
        g=int(input())
        guesses +=1

        if g < number: print ("Your guess is too low.")
        elif g > number: print ("Your guess is too high.")
        else: 
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break
guess()