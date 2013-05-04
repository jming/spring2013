import game_interface
import random
import time
from classify import *


def get_move(view):

    eat = 0

    # 0. Land in square, check if there is a plant
    hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

    # If there is a plant,
    if hasPlant:

        # 1. Decide if observe/how many times
        numobs = 5

        # 2. Classify plant that many number of times
        ispoisonous = 0
        for i in xrange(numobs):
            ispoisonous += classify(view.GetImage())

        eat = ispoisonous / numobs > 0.5

    # 3. Decide where to go
    move = random.randint(0, 4)

    # 4. Execute move
    time.sleep(0.1)
    return (move, eat)


def classify(image):
    return run_classify(image)
