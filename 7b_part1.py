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

# Task 1. (3 marks)
# Write the code for the init_guesses function 

# It should loop over q_list and
# enter a "?" into every "guess" in each 
# question dictionary it contains

# It should work even if q_list has more questions

def init_guesses(q_list):
    # add code here
    
    return
    

# do not edit below
if __name__ == "__main__":
    init_guesses(q_list)
    print(q_list)

# Expect output like:
# [{'text': 'Two plus two equals seven', 'answer': 'F', 'guess': '?'}, 
#  {'text': 'A carrot is the same colour as an orange', 'answer': 'T', 'guess': '?'}, 
# { 'text': 'Ten divided by two is five', 'answer': 'T', 'guess': '?'}]



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


def init_guesses(q_list):
    ## model answer
    for q in q_list:
        q_list['guess'] = '?'
    
    return
    

# do not edit below
if __name__ == "__main__":
    init_guesses(q_list)
    print(q_list)


# Markscheme /3
# part1 -- Loop over questions in q_list -- 1 mark
# part1 -- access guess key in dict -- 1 mark
# part1 -- sets guess key to '?' -- 1 mark

# model ans
'''
# place in init_guesses function
for q in q_list:
    q_list['guess'] = '?'
'''
