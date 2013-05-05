import game_interface
import random
import time
from classify import *


def get_move(view):
    global svc

    eat = False

    # 0. Land in square, check if there is a plant
    hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

    # If there is a plant,
    if hasPlant:

        # 1. Decide if observe/how many times
        numobs = 5

        # 2. Classify plant that many number of times
        ispoisonous = 0
        build_svm()
        for i in xrange(numobs):
            ispoisonous += classify(view.GetImage())
            # ispoisonous = svc.predict(view.GetImage)[0]

        # print "ISPOI", ispoisonous
        eat = True if (ispoisonous / numobs > 0.5) else False
        # print "EAT", eat

    # 3. Decide where to go
    move = random.randint(0, 4)

    # 4. Execute move
    # time.sleep(0.1)
    return (move, eat)


def classify(image):
    global svc
    classified = svc.predict(image)[0]
    print classified
    return classified

# def classify(image):
#     # print "CLASSIFYING"
#     # print image
#     global svc
#     build_svm()
#     classified = int(svc.predict(image)[0])
#     print classified
#     return classified
#     # return run_classify(image)
