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

# Task 3. (2 marks)
# Once valid input has been provided and guesses have been entered into
# the question list entries we need to count the number of correct guesses.

# def check_results(q_list):
#
# should loop over the q_list and check
# whether each guess matches to the answer
# if so it should increment the n_correct by 1


def check_results(q_list):
    n_correct = 0
    
    # add task 3 code here:
    
    return n_correct

# >> MODEL ANS START

def check_results(q_list):
    n_correct = 0
    
    # add task 3 code here:
    for q in q_list:
        if q['answer'] == q['guess']:
            n_correct += 1

    return n_correct

# >> MODEL ANS END
        
# do not edit below

def register_guesses(q_list, guess_list):
    n = len(q_list)
    for i in range(n):
        question = q_list[i]
        guess = guess_list[i]
        question["guess"] = guess

if __name__ == "__main__":
    
    guess_list = ["F", "F", "F"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

    guess_list = ["F", "F", "T"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 
    
    guess_list = ["F", "T", "F"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

    guess_list = ["F", "T", "T"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

    guess_list = ["T", "F", "F"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

    guess_list = ["T", "F", "T"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 
    
    guess_list = ["T", "T", "F"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

    guess_list = ["T", "T", "T"]
    register_guesses(q_list, guess_list)
    count = check_results(q_list)
    print(f"Result for {guess_list}: {count}") 

# Markscheme /3
# part3 -- loop over questions  -- 1 mark
# part3 -- if statement to check if answer is correct -- 1 mark
# part3 -- increment n_correct -- 1 mark

# model ans
'''
# add task 3 code here:
for q in q_list:
    if q['answer'] == q['guess']:
        n_correct += 1
'''
