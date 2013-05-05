# import common
import game_interface
import random
# import time
from classify import *

#list of locations to not return to
blackloc = []

#FINITE STATE CONTROLLER
# List of states
states = [0, 1, 2, 3, 4]
# List of actions
actions = [0, 2, 2, 2, 1]

locs = []

'''
(0,0)
(-1,0)
(-1,-1)
(0,-1)
(1,-1)
(1,0)
(1,1)
(0,1)
(-1,1)
(-2,1)
'''

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

def move_toward(loc):
#loc is in form (x, y)
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
    global svc
    classified = int(svc.predict(image)[0])
    print classified
    return classified


def get_move(view):
    # list of locations in the order that we wish to visit them
    global locs
    if len(locs)==0: generate_locations()
    
    # list of locations do not want to return to
    global blackloc
    
    eat = 0
    eatbool = False

    # 0. Land in square, check if there is a plant
    hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
    # current position
    currpos = (view.GetPosX, view.GetPosY)
    # Remove current position from locations to visit
    if currpos in locs:
        locs.remove(currpos)
    
    #finite state controller current state starts at 2
    curr = 2
    # whether or not we have made decision to eat this plant (if exists) yet
    decision = 0

    #if already visited this location, don't eat
    if currpos in blackloc:
        eatbool = false
    # If there is a plant,
    elif hasPlant:

        # 1. Decide if observe/how many times
        # numobs = observe(view)
        numobs = 5

        # 2. Classify plant that many number of times, keeping track of history of obs
        # Stop observing if finite state controller tells us to perform an action
        # ispoisonous = 0
        build_svm()
        i = 0

        for x in xrange(numobs):
            i += classify(view.GetImage())
        # print i, i/numobs
        eatbool = True if (i/float(numobs) > 0.5) else False

    #     while i < numobs and not decision:
    #         c = classify(view.GetImage())
    #         #ispoisonous += classify(view.GetImage())
    #         if c == 0:
    #             curr += 1
    #         else:
    #             curr -= 1
    #         if actions[curr] != 2:
    #             decision = 1
    #             eat = actions[curr]
    #             break
    #         i += 1

    #     #eat = ispoisonous / numobs > 0.5

    # eatbool = (eat != 0)

    # Add location to blackloc list, do not want to return
    blackloc.append((view.GetPosX, view.GetPosY))
    
    # 3. Decide where to go
    # Go towards the first location in the locs list
    move = move_toward(locs[0])
    #move = random.randint(0, 4)

    # 4. Execute move
    return (move, eatbool)


# def get_move(view):
#   return common.get_move(view)