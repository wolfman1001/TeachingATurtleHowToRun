import turtle
from random import randint


def move_prey(prey, i):
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
    pred.penup()
    prey.penup()
    pred_start_x = randint(-500, 500)
    pred_start_y = randint(-500, 500)
    prey_start_x = randint(-500, 500)
    prey_start_y = randint(-500, 500)
    pred.setpos(pred_start_x, pred_start_y)
    prey.setpos(prey_start_x, prey_start_y)


def get_score(pred, prey, move_list):
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
    return [randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7),
            randint(0, 7)]


def combine_lists(parent1, parent2):
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
    data = data[0:5]

    for i in range(0, 5):
        parent1 = randint(0, 4)
        parent2 = randint(0, 4)
        move_list = combine_lists(data[parent1]["moves"], data[parent2]["moves"])
        tmp = {
            "score": get_score(pred, prey, move_list),
            "moves": move_list
        }
        data.append(tmp)
    for d in data:
        print(str(d["moves"]) + " --- " + str(d["score"]))
    print("*************************************")


wn = turtle.Screen()
pred = turtle.Turtle()
prey = turtle.Turtle()
pred.color("red")
pred.shape("turtle")
prey.shape("turtle")
pred.speed(0)
prey.speed(0)
turtle.tracer(0, 0)
initialise(pred, prey)

data = []
for i in range(0, 10):
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

