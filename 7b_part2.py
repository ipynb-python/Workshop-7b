# The code below sets up a Python list of question items for a quiz.

# Each item is a dictionary, with keys:
# "text"   - stores a statement
# "answer" - stores a character "T" or "F" depending if the statement is True or False
# "guess"  - placeholder for the player guess (either "T" or "F")

q_list = [
    {"text": "Two plus two equals seven",
     "answer": "F",
     "guess": None},
    {"text": "A carrot is the same colour as an orange",
     "answer": "T",
     "guess": None},
    {"text": "Ten divided by two is five",
     "answer": "T",
     "guess": None},
]

# Task 2. (4 marks)
# Look at the code provided to take_guess(q_list)
# Run the file and check how this function works.
#
# Make a modified version of this function called take_valid_guess 
# (a template for this has already been provided),
# 
# def take_valid_guess(q_list):
#
# This function should loop to take input until a VALID guess is entered
# Any input guess should be converted to UPPER CASE and checked it is valid i.e.
# - right length according to the length of the q_list provided
# - only stores T or F characters.
#
# To test your function edit the second-to-last line in the file
# to call take_valid_guess(q_list) not take_guess(q_list).

def take_guess(q_list):
    # initialise guest_list
    guess_list = []

    # take input
    guess_string = input("> ")
    # e.g. may store "TFT"

    # convert to list
    guess_list = list(guess_string)
    # e.g. may store [ "T", "F", "T" ]

    # store result.
    # do not change the code below
    print(f"Entering guess: {guess_list}")
    register_guesses(q_list, guess_list)
    return

def take_valid_guess(q_list):
    # initialise guest_list
    guess_list = []

    # add task 2 code here:
    
    
    # store result
    # do not change the code below
    print(f"Entering guess: {guess_list}")
    register_guesses(q_list, guess_list)
    return


# do not edit except to switch
#    take_guess(q_list) 
# to 
#    take_valid_guess(q_list)
# below for testing

def register_guesses(q_list, guess_list):
    n = len(q_list)
    for i in range(n):
        question = q_list[i]
        guess = guess_list[i]
        question["guess"] = guess


if __name__ == "__main__":
    take_guess(q_list)
    print(q_list)

# Expected behaviour. Only a valid string of 3 t/f or T/F characters will be accepted
# These will be written into the q_list guess entries as appropriate.