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
    {"text": "Viking bones were found at the South Pole",
     "answer": "F",
     "guess": None},
    {"text": "The oldest tortoises are over 100 years old",
     "answer": "T",
     "guess": None},
    {"text": "There are 29 letters in this sentence",
     "answer": "T",
     "guess": None},
    {"text": "Exeter used to be just called Eter. (Since then it has been known as Exeter)",
     "answer": "F",
     "guess": None}   
]

# Task 4a (3 marks)
# The code in this file includes the functions needed to run a complete game.
# It will function as written except correct guesses are not scored correctly
#
# Your task is to examine the play_game function and edit so that the game
# will end after the maximum allowed attempts are made, i.e. the game loop will
# exit setting finished = False, and success = False so the correct end message
# is shown.
#
# Task 4b (1 mark)
# Complete the code by copying in any working code from parts 1-3 over the template functions
# at the bottom of this file i.e.
#    init_guesses(q_list), 
#    take_valid_guess(q_list), 
#    check_results(q_list)
# Edit the code play_game() to make use of take_valid_guess function if you have it working.

def play_game(q_list):
    # initialise game variables
    n = len(q_list)
    n_attempt = 0
    max_attempts = 4

    # set up flags to store game state
    finished = False
    success = False

    # start game
    print("Welcome to the game. Let's play!")
    print(f"You have {max_attempts} attempts!")

    while not finished:
        n_attempt += 1
        
        # display game state to player
        print()
        print(f"=== Attempt {n_attempt} ===")
        print_questions(q_list)

        # take the users guess
        
        # change below to 
        #  take_valid_guess(q_list)  
        # when you have written it
        take_valid_guess(q_list) 

        # check if attempt is successful
        n_correct = check_results(q_list)
        print(f"{n_correct} are correct!")
        if n_correct == n:
            finished = True
            success = True

        # model ans (place at end of while loop)
        if n_attempt == max_attempts:
            success = False
            break

    # report result
    if success:  
        print(f"You did it in {n_attempt} attempts Well done!")
    else:
        print(f"You used all your attempts! Bad luck!")


def print_questions(q_list):
    
    n = len(q_list)
    n_correct = check_results(q_list)
    print(f"Look at the statements below. Which are true/false?")
    
    print("")
    print(f"Guess | Statement ({n_correct} are correct)")
    print("----- | ----------------------------------- ")
    
    for item in q_list:
        text = item['text']
        answer = item['answer']
        guess = item['guess']

        print(f"  {guess}   | {text}")

    print()
    print(f"Enter your next guess as a string of {n} T/F characters")


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


def register_guesses(q_list, guess_list):
    n = len(q_list)
    for i in range(n):
        question = q_list[i]
        guess = guess_list[i]
        question["guess"] = guess


#### Replace the functions below with working copies
#### from parts 1-3 to obtain fully working code
#### Change take_guess to take_valid_guess in play_game
#### to use your improved function.
    
def init_guesses(q_list):
    ## model answer
    for q in q_list:
        q_list['guess'] = '?'
    
    return

def take_valid_guess(q_list):
    # initialise guest_list
    guess_list = []

    # add task 2 code here:
    guess_string = None
    while len(guess_list) == 0:
        guess_string = input("> ").upper()

        if len(guess_string) != len(q_list):
            continue

        valid = True
        for letter in guess_string:
            if letter not in ("T","F"):
                valid = False

        if valid:
            guess_list = list(guess_string)
    
    # store result
    # do not change the code below
    print(f"Entering guess: {guess_list}")
    register_guesses(q_list, guess_list)
    return


def check_results(q_list):
    n_correct = 0
    
    # add task 3 code here:
    for q in q_list:
        if q['answer'] == q['guess']:
            n_correct += 1

    return n_correct


if __name__ == "__main__":
    play_game(q_list)


# Markscheme /2
# part4 -- while loop ends when attempts used up (allow break or set finished=True)  -- 1 mark
# part4 -- success set to False so correct message shown -- 1 mark

# model ans
'''
# model ans 
# place at end of while loop in play_game()
if n_attempt == max_attempts:
    success = False
    break
'''