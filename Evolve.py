import turtle
import math
from random import randint


def move_prey(prey, i):
    """i can be between 0 and 7, each value of i corresponds to a direction to move in """
    x = prey.xcor()
    y = prey.ycor()
    if i == 0:
        y += 10
    elif i == 1:
        y += 5
        x += 5
    elif i == 2:
        x += 10
    elif i == 3:
        x += 5
        y -= 5
    elif i == 4:
        y -= 10
    elif i == 5:
        y -= 5
        x -= 5
    elif i == 6:
        x -= 10
    elif i == 7:
        y += 5
        x -= 5
    prey.setpos(x, y)


def handle_prey_movement(prey, pred, move_list):
    """Takes an array of numbers and picks one based on the position of the predator
    turtle in relation to the prey turtle"""
    predx = pred.xcor()
    predy = pred.ycor()
    preyx = prey.xcor()
    preyy = prey.ycor()
    if preyx > predx and preyy > predy:
        move_prey(prey, move_list[7])
    elif preyx > predx and preyy < predy:
        move_prey(prey, move_list[5])
    elif preyx > predx and preyy == predy:
        move_prey(prey, move_list[6])
    elif preyx < predx and preyy > predy:
        move_prey(prey, move_list[3])
    elif preyx < predx and preyy < predy:
        move_prey(prey, move_list[1])
    elif preyx < predx and preyy == predy:
        move_prey(prey, move_list[2])
    elif preyx == predx and preyy > predy:
        move_prey(prey, move_list[4])
    elif preyx == predx and preyy < predy:
        move_prey(prey, move_list[0])


def handle_pred_movement(pred, prey):
    """Moves the predator turtle towards the prey turtle"""
    speed = 8
    predx = pred.xcor()
    predy = pred.ycor()
    preyx = prey.xcor()
    preyy = prey.ycor()

    if preyy > predy:
        predy += speed
    else:
        predy -= speed

    if preyx > predx:
        predx += speed
    else:
        predx -= speed

    pred.setpos(predx,predy)


def initialise(pred, prey):
    """Sets up the turtles for a test by giving them random coordinates"""
    pred.penup()
    prey.penup()
    pred_start_x = randint(-500, 500)
    pred_start_y = randint(-500, 500)
    prey_start_x = randint(-500, 500)
    prey_start_y = randint(-500, 500)
    pred.setpos(pred_start_x, pred_start_y)
    prey.setpos(prey_start_x, prey_start_y)


def get_score(pred, prey, move_list):
    """Runs random tests a set number of times then works out an average,
    caps the score at 100 to prevent it running forever"""
    NUM_TESTS = 75
    score = []

    for test in range(1, NUM_TESTS):
        current_score = 0
        while (abs(pred.ycor() - prey.ycor()) > 10 or abs(pred.xcor() - prey.xcor()) > 10) and current_score < 100:
            handle_pred_movement(pred, prey)
            handle_prey_movement(prey, pred, move_list)
            current_score += 1
        initialise(pred,prey)
        score.append(current_score)
    return sum(score) / NUM_TESTS


def generate_list():
    """Generate an array of 7 random numbers between 0 and 7"""
    return [randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7)]


def combine_lists(parent1, parent2):
    """Generates a new array from two parent arrays"""
    child = [0,0,0,0,0,0,0,0]
    for num in range(0,8):
        flip = randint(0, 1)
        if (flip == 0):
            child[num] = parent1[num]
        else:
            child[num] = parent2[num]
    return child


def run(data):
    data = sorted(data, key=lambda k: k['score'], reverse=True)
    halfLen = math.ceil(len(data) / 2)
    data = data[0:halfLen]

    for i in range(0, halfLen):
        parent1 = randint(0, 4)
        parent2 = randint(0, 4)
        move_list = combine_lists(data[parent1]["moves"], data[parent2]["moves"])
        tmp = {
            "score": get_score(pred, prey, move_list),
            "moves": move_list
        }
        data.append(tmp)
    mutate(data)
    for d in data:
        print(str(d["moves"]) + " --- " + str(d["score"]))
    print("*************************************")

def mutate(data):
    """Adds in the chance for random mutation to avoid the pool of arrays becoming
    stagnant and recombining into the same thing"""
    for d in data:
        MutationChance = randint(0,4)
        if(MutationChance == 2):
            MutatedNum = randint(0,7)
            d["moves"][MutatedNum] = randint(0, 7)
            d["score"] = get_score(pred, prey, move_list)

wn = turtle.Screen()
pred = turtle.Turtle()
prey = turtle.Turtle()
pred.color("red")
pred.shape("turtle")
prey.shape("turtle")
pred.speed(0)
prey.speed(0)
#Comment out the below line if you want to see the turtles move
#This will increase the time it takes by quite alot
turtle.tracer(0, 0)
initialise(pred, prey)

data = []
for i in range(0, 15):
    move_list = generate_list()
    tmp = {
        "score": get_score(pred, prey, move_list),
        "moves": move_list
    }
    data.append(tmp)

for d in data:
    print(str(d["moves"]) + " --- " + str(d["score"]))
print("*************************************")

for i in range(1, 5):
    run(data)
data = sorted(data, key=lambda k: k['score'], reverse=True)
max = data[0]
print("*************************************")
print(str(max["moves"]) + " --- " + str(max["score"]))
wn.mainloop()

