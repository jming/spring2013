import common

#list of locations to not return to
blackloc = []

#FINITE STATE CONTROLLER
# List of states
states = [0,1,2,3,4]
actions = [0,2,2,2,1]


def get_move(view):
  return common.get_move(view)

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
    # have not made a decision eat/not yet
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

'''BEGIN NEURAL NETWORK ADDITIONS
# Load in the training data.
images = DataReader.GetImages('nutritious_test.txt', -1)
#print images0
images1 = DataReader.GetImages('poisnous_test.txt', -1)
# images.extend(images1)
#print 'training', len(images)
images=images[:500]+images1[:500]

# Load the validation set.
validation = DataReader.GetImages('nutritious_valid.txt', -1)
validation2 = DataReader.GetImages('poisnous_valid.txt', -1) 
# validation.extend(validation2)
validation=validation[:500]+validation[:500]
#print 'validation', len(validation)

# Load the test data.
test = DataReader.GetImages('nutritious.txt', -1)
test2 = DataReader.GetImages('poisnous.txt', -1)
# test.extend(test2)
test=test[:500]+test2[:500]
#print 'test', len(test)

# Initializing network
rate = .1
epochs = 10
network = SimpleNetwork() 

# Hooks user-implemented functions to network
network.FeedForwardFn = FeedForward
network.TrainFn = Train

# Initialize network weights
network.InitializeWeights()


'''# Displays information
print '* * * * * * * * *'
print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
print 'Type of network used: %s' % network.__class__.__name__
print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
     (len(network.network.inputs), len(network.network.hidden_nodes),
      len(network.network.outputs)))
print '* * * * * * * * *'''

# Train the network.
network.Train(images, validation, test, rate, epochs)
print 'length', len(network.network.weights)
#for i in network.network.weights:
#  print i.value

END OF NEURAL NETWORK ADDITIONS'''