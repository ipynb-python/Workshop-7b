import random

def roll_dice(n_dice):
    n_sides = 6
    # you do not need to change the code below
    rolls = []
    for i in range(n_dice):
        rolls.append(random.randint(1,n_sides))
    return rolls

demo1 = roll_dice(2)
print(demo1)