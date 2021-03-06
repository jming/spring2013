import common

#list of locations to not return to
blackloc = []

#FINITE STATE CONTROLLER
# List of states
states = [0,1,2,3,4]
# List of actions
actions = [0,2,2,2,1]

locs = []

def generate_locations():
  global locs
  '''for i in range(-20,20):
    for j in range(-20,20):
      locs.append((i,j))'''
  
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
  print locs
  
generate_locations()

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

def get_move(view):
  global locs
  if len(locs)==0: generate_locations()
  # If there is a plant in this location, then try and eat it.
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  # Choose a random direction
  if hasPlant:
    for i in xrange(5):
      #print view.GetImage()
  time.sleep(0.1)
  dir = random.randint(0,4)

  return (dir, hasPlant)

def observe(view):
  return 5
  
def clssify(image):
  return 1
  
'''
def get_move(view):

    eat = 0

    # 0. Land in square, check if there is a plant
    hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
    # If no plant, add location to blackloc list
    #blackloc.append((view.GetPosX, view.GetPosY))
    #finite state controller current state starts at 2
    curr = 2
    # whether or not we have made decision to eat this plant (if exists) yet
    decision = 0

    # If there is a plant,
    if hasPlant:

        # 1. Decide if observe/how many times
        numobs = observe(view)

        # 2. Classify plant that many number of times, keeping track of history of obs
        # Stop observing if finite state controller tells us to perform an action
        ispoisonous = 0
        i = 0
        while i < numobs and !decision:
            c = classify(view.GetImage())
            #ispoisonous += classify(view.GetImage())
            if c = 0:
                curr += 1
            else:
                curr -= 1
            if actions[curr] != 2:
                decision = 1
                eat = actions[curr]
                break
            i+=1

        #eat = ispoisonous / numobs > 0.5
    
    eatbool = (eat != 0)
    
    # 3. Decide where to go
    move = random.randint(0, 4)

    # 4. Execute move
    return (move, eatbool)
'''

# ORIGINAL GET_MOVE FROM COMMON.PY
# def get_move(view):
#   # Check if there is a plant in this location
#   hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
#   # if there is a plant,
#   if hasPlant:
#       # take five observations
#     for i in xrange(5):
#       # print these observations
#       print view.GetImage()
#   # wait a few seconds
#   time.sleep(0.1)
#   # return a random direction and whether to eat it
#   return (random.randint(0, 4), hasPlant)