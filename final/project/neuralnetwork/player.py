# import common
import game_interface
import random
# import time
from neural_net_impl import *
from neural_net import *

network = SimpleNetwork()
'''def create_network(network):
    global network
    for i in range(0, 36):
        network.AddNode(Node(), NeuralNetwork.INPUT)

    for i in range(0, 2):
        output = Node()
        for input in network.inputs:
                output.AddInput(input, Weight(weights[network.inputs.index(input)]), network)
        network.AddNode(output, NeuralNetwork.OUTPUT)'''



#list of locations to not return to
blackloc = []

#FINITE STATE CONTROLLER
# List of states
states = [0, 1, 2, 3, 4]
# List of actions
actions = [0, 2, 2, 2, 1]

locs = []

#list of past 5 life scores
lifes = [0 for i in range(5)]

# Generate locations to visit in spiral shape
def generate_locations():
  global locs

  alldirs = [0,1]
  currindex = 0
  #[left+down, right+up]
  currx = 0
  curry = 0
  locs.append((currx,curry))
  for i in range (1,41):
    c = alldirs[currindex]
    if c == 0:
      for j in range(i):
        currx -= 1
        locs.append((currx,curry))
      for j in range(i):
        curry -= 1
        locs.append((currx,curry))
    else:
      for j in range(i):
        currx += 1
        locs.append((currx,curry))
      for j in range(i):
        curry += 1
        locs.append((currx,curry))
    currindex+=1
    currindex = currindex%2
  #print locs
  
def generate_spiral(loc,diameter):
    global locs
    locs = []
    alldirs = [0,1]
    currindex = 0
    #[left+down, right+up]
    currx = loc[0]
    curry = loc[1]
    locs.append((currx,curry))
    for i in range (1,diameter+1):
        c = alldirs[currindex]
        if c == 0:
            for j in range(i):
                currx -= 1
                locs.append((currx,curry))
            for j in range(i):
                curry -= 1
                locs.append((currx,curry))
        else:
            for j in range(i):
                currx += 1
                locs.append((currx,curry))
            for j in range(i):
                curry += 1
                locs.append((currx,curry))
        currindex+=1
        currindex = currindex%2
    #print locs
    


def move_toward(loc, view):
#loc is in form (x, y)

    dir = random.randint(0,4)

    if view.GetXPos() > loc[0]:
        dir = game_interface.LEFT
    elif view.GetXPos() < loc[0]:
        dir = game_interface.RIGHT
    elif view.GetYPos() > loc[1]:
        dir = game_interface.DOWN
    elif view.GetYPos() < loc[1]:
        dir = game_interface.UP

    return dir


def classify(image):
    '''global svc
    classified = int(svc.predict(image)[0])
    print classified
    return classified'''
    global network
    im = [[0 for x in range(6)] for y in range(6)]
    count = 0
    for i in range(6):
        for j in range(6):
            im[i][i] = image[count]
            count += 1
    i = Image(0)
    i.pixels = im
    print i
    return network.Classify(i)


def get_move(view):
    print "rounds", view.GetRound()
    # neural network for classifying
    global network
    network.FeedForwardFn = FeedForward
    network.TrainFn = Train
    # list of locations in the order that we wish to visit them
    global locs
    if len(locs)==0: 
        generate_spiral((0,0), 40)
        network.InitializeWeights()

    # list of locations do not want to return to
    global blackloc
    
    # current position
    currpos = (view.GetXPos(), view.GetYPos())
    # Remove current position from locations to visit
    if currpos in locs:
        locs.remove(currpos)

    # last 5 lifes
    # global lifes
    # lifes.insert(0, view.GetLife())
    # count_n = 0
    # for i in range(5):
    #     if lifes[i] > lifes[4]:
    #         count_n += 1
    # if count_n >= 3:
    #     generate_spiral(currpos, 10)

    eat = 0
    eatbool = False

    # 0. Land in square, check if there is a plant
    hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT


    #finite state controller current state starts at 2
    curr = 2
    # whether or not we have made decision to eat this plant (if exists) yet
    decision = 0

    #if already visited this location, don't eat
    if currpos in blackloc:
        eatbool = False
    # If there is a plant,
    elif hasPlant:

        # 1. Decide if observe/how many times
        # numobs = observe(view)
        life = view.GetLife()

        if life > 120:
            numobs = 0
        elif life >= 50:
            numobs = 5
        elif life >= 30:
            numobs = 4
        elif life >= 20:
            numobs = 3
        else:
            numobs = 0

        # 2. Classify plant that many number of times, keeping track of history of obs
        # Stop observing if finite state controller tells us to perform an action
        # ispoisonous = 0
        #build_svm()
        i = 0

        # for x in xrange(numobs):
        #     i += classify(view.GetImage())
        # # print i, i/numobs
        # eatbool = True if (i/float(numobs) > 0.5) else False

        while i < numobs and not decision:
            c = classify(view.GetImage())
            #ispoisonous += classify(view.GetImage())
            if c == 1:
                curr += 1
            else:
                curr -= 1
            if actions[curr] != 2:
                decision = 1
                eat = actions[curr]
                break
            i += 1

    eatbool = (eat != 0)

    # Add location to blackloc list, do not want to return
    blackloc.append((view.GetXPos(), view.GetYPos()))

    # 3. Decide where to go
    # Go towards the first location in the locs list
    move = move_toward(locs[0], view)
    #move = random.randint(0, 4)

    # 4. Execute move
    return (move, eatbool)


# def get_move(view):
#   return common.get_move(view)
