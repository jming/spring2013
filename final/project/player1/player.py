import game_interface
import random
# from neural_net_impl import *
# from neural_net import *

##########################################################

import math

class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

class Weight:
  def __init__(self, value):
    self.value = value

class Node:
  """
  Attributes:
  ----------
  inputs            : a list of node who are inputs for this node
  weights           : a list of weight objects, for links with input nodes
  fixed_weight      : w0 in the lecture notes and slides
  forward_neighbors : a list of nodes who are output for this node
  raw_value         : the linear combination of weights and input signals, that is w'x
  transformed_value : the signal emitted by this node, that is g(w'x)

  Description:
  ------------
  The situation can be summarized as follow:


              weights[i]        forward_weights[i]
  inputs[i]   -----------> self ------------------> forward_neighbors[i]

  AND:

  inputs                 \
                           => raw_value => transformed value => 
  weights & fixed_weight /
  

  """
  def __init__(self):
    self.inputs = []
    self.weights = []
    self.fixed_weight = None
    self.forward_neighbors = []
    self.forward_weights = []
    self.raw_value = 0
    self.transformed_value = 0

  def AddInput(self, node, weight, network):
    self.inputs.append(node)
    if not weight:
      weight = network.GetNewWeight()
    self.weights.append(weight)
    node.forward_neighbors.append(self)
    node.forward_weights.append(weight)
    if not self.fixed_weight:
      self.fixed_weight = network.GetNewWeight()

class Input:
  def __init__(self):
    self.values = []

class Target:
  def __init__(self):
    self.values = []


class NeuralNetwork:
  INPUT = 1
  HIDDEN = 2
  OUTPUT = 3

  def __init__(self):
    self.complete = False
    self.inputs = []
    self.hidden_nodes = []
    self.outputs = []
    self.node_set = {}
    self.weights = []

  def GetNewWeight(self):
    weight = Weight(0.0)
    self.weights.append(weight)
    return weight

  def AddNode(self, node, node_type):
    self.CheckIncomplete()
    if node_type == self.INPUT:
      assert len(node.inputs) == 0, 'Input node cannot have inputs'
    # Check that we only reference inputs already in the network
    for input in node.inputs:
      assert input in self.node_set, 'Cannot reference input that is not already in the network'
    self.node_set[node] = True
    if node_type == self.INPUT:
      self.inputs.append(node)
    elif node_type == self.HIDDEN:
      self.hidden_nodes.append(node)
    else:
      assert node_type == self.OUTPUT, 'Unexpected node_type: ' % node_type
      self.outputs.append(node)
    
  def MarkAsComplete(self):
    seen_nodes = {}
    for input in self.inputs:
      seen_nodes[input] = True
      assert len(input.inputs) == 0, 'Inputs should not have inputs of their own.'
    for node in self.hidden_nodes:
      seen_nodes[node] = True
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    for node in self.outputs:
      assert len(node.forward_neighbors) == 0, 'Output node cannot have forward neighbors.'
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    self.complete = True

  def CheckComplete(self):
    if self.complete:
      return
    self.MarkAsComplete()

  def CheckIncomplete(self):
    assert not self.complete, ('Tried to modify the network when it has already been marked as'
      'complete')

  @staticmethod
  def ComputeRawValue(node):
    total_weight = 0

    for i in range(len(node.inputs)):
      total_weight += node.weights[i].value * node.inputs[i].transformed_value
    total_weight += node.fixed_weight.value
    return total_weight
  
  @staticmethod
  def Sigmoid(value):
    try:
      return 1.0 / (1 + math.exp(-value))
    except:
      if value < 0:
        return 0.0
      else:
        return 1.0

  @staticmethod
  def SigmoidPrime(value):
    try:
      return math.exp(-value) / math.pow(1 + math.exp(-value), 2)
    except:
      return 0

  def InitFromWeights(self, weights):
    assert len(self.weights) == len(weights), (
      'Trying to initialize from a different sized weight vector.')
    for i in range(len(weights)):
      self.weights[i].value = weights[i]


class NetworkFramework(object):
  def __init__(self):
    self.network = NeuralNetwork()

    # Don't worry about these functions, you 
    # will be asked to implement them in another
    # file. You should not modify them here
    self.FeedForwardFn = None
    self.TrainFn = None


  def EncodeLabel(self, label):
    raise NotImplementedError("This function has not been implemented")

  def GetNetworkLabel(self, label):
    raise NotImplementedError("This function has not been implemented")

  def Convert(self, image):
    raise NotImplementedError("This function has not been implemented")

  def InitializeWeights(self):
    for weight in self.network.weights:
      weight.value = 0

  def Classify(self, image):
    input = self.Convert(image)
    self.FeedForwardFn(self.network, input)
    return self.GetNetworkLabel()

  def Performance(self, images):

    # Loop over the set of images and count the number correct.
    correct = 0
    for image in images:
      if self.Classify(image) == image.label:
        correct += 1
    return correct * 1.0 / len(images)

  def Train(self, images, validation_images, test, learning_rate, epochs):

    # Convert the images and labels into a format the network can understand.
    inputs = []
    targets = []
    for image in images:
      inputs.append(self.Convert(image))
      targets.append(self.EncodeLabel(image.label))

    # Initializes performance log
    performance_log = []
    performance_log.append((self.Performance(images), self.Performance(validation_images), self.Performance(test)))
    
    # pre-defined tolerance for performance convergence
    e = 0.0001
    prev = 0.
    perf_validate = 1.
    diff = 1.
    i = 0
    no_improv = 0

    # Loop through the specified number of training epochs while maximum epochs not reached
    # And convergence tolerance threshold has not been reached yet
    while i < epochs and no_improv < 5:
      self.TrainFn(self.network, inputs, targets, learning_rate, 1)

      # Print out the current training and validation performance.
      perf_train = self.Performance(images)
      perf_validate = self.Performance(validation_images)
      perf_test = self.Performance(test)
      diff = perf_validate - prev
      prev = perf_validate
      epochs -= 1
      i += 1
      
      if diff < e:
        no_improv+=1
      else:
        no_improv = 0
      
      print '%d Performance: %.8f %.3f %.3f' % (
        i, perf_train, perf_validate, perf_test)
        
      # updates log
      performance_log.append((perf_train, perf_validate, perf_test))

    return(performance_log)

  def RegisterFeedForwardFunction(self, fn):
    self.FeedForwardFn = fn

  def RegisterTrainFunction(self, fn):
    self.TrainFn = fn

##########################################################
# from neural_net import NeuralNetwork, NetworkFramework
# from neural_net import Node, Target, Input
# import random

num_input_nodes = 36
num_output_nodes = 2


# <--- Problem 3, Question 1 --->

def FeedForward(network, input):
  """
  Arguments:
  ---------
  network : a NeuralNetwork instance
  input   : an Input instance

  Returns:
  --------
  Nothing

  Description:
  -----------
  This function propagates the inputs through the network. That is,
  it modifies the *raw_value* and *transformed_value* attributes of the
  nodes in the network, starting from the input nodes.

  Notes:
  -----
  The *input* arguments is an instance of Input, and contains just one
  attribute, *values*, which is a list of pixel values. The list is the
  same length as the number of input nodes in the network.

  i.e: len(input.values) == len(network.inputs)

  This is a distributed input encoding (see lecture notes 7 for more
  informations on encoding)

  In particular, you should initialize the input nodes using these input
  values:

  network.inputs[i].raw_value = input.values[i]
  """
  network.CheckComplete()

  # (1) Assign input values to input nodes
  for i in range(len(input.values)):
    network.inputs[i].raw_value = input.values[i]
    network.inputs[i].transformed_value = input.values[i]

  # (2) Propogate from one layer to the next
  for node in (network.hidden_nodes + network.outputs):
    node.raw_value = network.ComputeRawValue(node)
    node.transformed_value = network.Sigmoid(node.raw_value)

#< --- Problem 3, Question 2

def Backprop(network, input, target, learning_rate):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  input         : an Input instance
  target        : a target instance
  learning_rate : the learning rate (a float)

  Returns:
  -------
  Nothing

  Description:
  -----------
  The function first propagates the inputs through the network
  using the Feedforward function, then backtracks and update the
  weights.

  Notes:
  ------
  The remarks made for *FeedForward* hold here too.

  The *target* argument is an instance of the class *Target* and
  has one attribute, *values*, which has the same length as the
  number of output nodes in the network.

  i.e: len(target.values) == len(network.outputs)

  In the distributed output encoding scenario, the target.values
  list has 10 elements.

  When computing the error of the output node, you should consider
  that for each output node, the target (that is, the true output)
  is target[i], and the predicted output is network.outputs[i].transformed_value.
  In particular, the error should be a function of:

  target[i] - network.outputs[i].transformed_value
  
  """
  network.CheckComplete()

  # 1) We first propagate the input through the network
  FeedForward(network, input)

  # 2) Then we compute the errors and update the weigths starting with the last layer
  nodes = network.outputs[::-1] + network.hidden_nodes[::-1] + network.inputs[::-1]
  
  for node in nodes:
    if node in network.outputs:
      node.e = target.values[network.outputs.index(node)] - node.transformed_value
    else:
      node.e = 0.
      for i in range(len(node.forward_neighbors)):
        node.e += node.forward_weights[i].value * node.forward_neighbors[i].delta
    node.delta = network.SigmoidPrime(node.raw_value) * node.e

  for node in nodes:
    for m in range(len(node.inputs)):
      node.weights[m].value += learning_rate * node.inputs[m].transformed_value * node.delta


# <--- Problem 3, Question 3 --->

def Train(network, inputs, targets, learning_rate, epochs):

  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  inputs        : a list of Input instances
  targets       : a list of Target instances
  learning_rate : a learning_rate (a float)
  epochs        : a number of epochs (an integer)

  Returns:
  -------
  Nothing

  Description:
  -----------
  This function should train the network for a given number of epochs. That is,
  run the *Backprop* over the training set *epochs*-times
  """
  network.CheckComplete()
  
  for epoch in range(epochs):
    for i in range(len(inputs)):
      Backprop(network, inputs[i], targets[i], learning_rate)


# <--- Problem 3, Question 4 --->

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    """
    Initialization.
    YOU DO NOT NEED TO MODIFY THIS __init__ method
    """
    super(EncodedNetworkFramework, self).__init__() # < Don't remove this line >

  # <--- Fill in the methods below --->

  def EncodeLabel(self, label):
    """
    Arguments:
    ---------
    label: a number between 0 and 9

    Returns:
    ---------
    a list of length 10 representing the distributed
    encoding of the output.

    Description:
    -----------
    Computes the distributed encoding of a given label.

    Example:
    -------
    0 => [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    3 => [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    Notes:
    ----
    Make sure that the elements of the encoding are floats.
    
    """
    t = Target()
    t.values = [0. for i in range(2)]
    t.values[label] = 1.
    return t

  def GetNetworkLabel(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    the 'best matching' label corresponding to the current output encoding

    Description:
    -----------
    The function looks for the transformed_value of each output, then decides 
    which label to attribute to this list of outputs. The idea is to 'line up'
    the outputs, and consider that the label is the index of the output with the
    highest *transformed_value* attribute

    Example:
    -------

    # Imagine that we have:
    map(lambda node: node.transformed_value, self.network.outputs) => [0.2, 0.1, 0.01, 0.7, 0.23, 0.31, 0, 0, 0, 0.1, 0]

    # Then the returned value (i.e, the label) should be the index of the item 0.7,
    # which is 3
    
    """
    a = map(lambda node: node.transformed_value, self.network.outputs)
    return a.index(max(a))

  def Convert(self, image):
    """
    Arguments:
    ---------
    image: an Image instance

    Returns:
    -------
    an instance of Input

    Description:
    -----------
    The *image* arguments has 2 attributes: *label* which indicates
    the digit represented by the image, and *pixels* a matrix 14 x 14
    represented by a list (first list is the first row, second list the
    second row, ... ), containing numbers whose values are comprised
    between 0 and 256.0. The function transforms this into a unique list
    of 14 x 14 items, with normalized values (that is, the maximum possible
    value should be 1).
    
    """

    inp = Input()

    for i in range(6):
      for j in range(6):
        inp.values.append(image.pixels[i][j])

    return inp

  def InitializeWeights(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes the weights with random values between [-0.01, 0.01].

    Hint:
    -----
    Consider the *random* module. You may use the the *weights* attribute
    of self.network.
    
    """

    # random.seed()
    # for i in range(len(self.network.weights)):
    #   self.network.weights[i].value = random.uniform(-.01, .01)
    weights = [-1.20427123442, -0.00424628826209, -0.964278197935, 0.244331250746, -0.288361816768, 2.10331453187, 1.54719783793, -0.658764513145, -0.279464443265, -0.239199110854, 0.626246546816, 0.440893228302, 0.473173577324, -1.05978067597, -0.262451719579, -2.21658810993, -2.15768401141, 0.145261082528, 0.991536326011, -0.0736698964158, 1.84804953828, 1.63938467372, -0.834576894308, 2.50325730411, 2.14284995071, 0.143765814209, 1.50359473634, 1.22069882314, 0.350053746782, 0.524158583252, 1.04273282167, -1.80564022242, -0.0725532272597, 0.771179844162, -0.550706391542, 0.363486090709, 1.69230357299, 1.20251076086, -0.00554224349246, 0.962074784256, -0.2409875051, 0.289124899972, -2.10232633516, -1.54669120246, 0.659005070648, 0.281563336586, 0.238999978889, -0.622895589472, -0.441386568922, -0.474736885751, 1.05943876453, 0.264183110881, 2.21908409518, 2.15827013768, -0.142943837766, -0.990326995619, 0.0753422975565, -1.84610648642, -1.64165804177, 0.834746087351, -2.50219968992, -2.1421926446, -0.142191932695, -1.50371336742, -1.21985971962, -0.350600031229, -0.523680717768, -1.04185239539, 1.80382544127, 0.0763526628852, -0.77636893571, 0.55016715994, -0.362973620148, -1.69245645096] 
    for i in range(len(self.network.weights)):
      print i
      self.network.weights[i].value = weights[i]

#<--- Problem 3, Question 6 --->

class SimpleNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a simple network, with 196 input nodes,
    10 output nodes, and NO hidden nodes. Each input node
    should be connected to every output node.
    """
    super(SimpleNetwork, self).__init__() # < Don't remove this line >

    # 1) Adds an input node for each pixel.
    for i in range(36):
      n = Node()
      self.network.AddNode(n, self.network.INPUT)
    # 2) Add an output node for each possible digit label.
    for i in range(2):
      n = Node()
      for j in range(36):
        n.AddInput(self.network.inputs[j], None, self.network)
      self.network.AddNode(n, self.network.OUTPUT)

#<---- Problem 3, Question 7 --->

class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=30):
    """
    Arguments:
    ---------
    number_of_hidden_nodes : the number of hidden nodes to create (an integer)

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a network with a hidden layer. The network
    should have 196 input nodes, the specified number of
    hidden nodes, and 10 output nodes. The network should be,
    again, fully connected. That is, each input node is connected
    to every hidden node, and each hidden_node is connected to
    every output node.
    """
    super(HiddenNetwork, self).__init__() # < Don't remove this line >

    # 1) Adds an input node for each pixel
    for i in range(196):
      n = Node()
      self.network.AddNode(n, self.network.INPUT)
    # 2) Adds the hidden layer
    for i in range(number_of_hidden_nodes):
      n = Node()
      for j in range(len(self.network.inputs)):
        n.AddInput(self.network.inputs[j], None, self.network)
      self.network.AddNode(n, self.network.HIDDEN)
    # 3) Adds an output node for each possible digit label.
    for i in range(10):
      n = Node()
      for j in range(len(self.network.hidden_nodes)):
        n.AddInput(self.network.hidden_nodes[j], None, self.network)
      self.network.AddNode(n, self.network.OUTPUT)
    

#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Your pick.

    Returns:
    --------
    Your pick

    Description:
    -----------
    Surprise me!
    """
    super(CustomNetwork, self).__init__() # <Don't remove this line>

    number_of_hidden_nodes = 10

    # 1) Adds an input node for each pixel
    for i in range(196):
      n = Node()
      self.network.AddNode(n, self.network.INPUT)

    # 2) Adds the first hidden layer
    for i in range(number_of_hidden_nodes):
      n = Node()
      for j in range(len(self.network.inputs)):
        n.AddInput(self.network.inputs[j], None, self.network)
      self.network.AddNode(n, self.network.HIDDEN)

    # 3) Adds the second hidden layer
    for i in range(number_of_hidden_nodes):
      n = Node()
      for j in range(number_of_hidden_nodes):
        n.AddInput(self.network.hidden_nodes[j], None, self.network)
      self.network.AddNode(n, self.network.HIDDEN)

    # 3) Adds the third hidden layer
    for i in range(number_of_hidden_nodes):
      n = Node()
      for j in range(number_of_hidden_nodes):
        n.AddInput(self.network.hidden_nodes[number_of_hidden_nodes+j], None, self.network)
      self.network.AddNode(n, self.network.HIDDEN)

    # 3) Adds an output node for each possible digit label.
    for i in range(10):
      n = Node()
      for j in range(number_of_hidden_nodes):
        n.AddInput(self.network.hidden_nodes[2*number_of_hidden_nodes + j], None, self.network)
      self.network.AddNode(n, self.network.OUTPUT)

##########################################################

network = SimpleNetwork()

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

    dir = random.randint(0, 4)

    if view.GetXPos() > loc[0]:
        dir = game_interface.LEFT
    elif view.GetXPos() < loc[0]:
        dir = game_interface.RIGHT
    elif view.GetYPos() > loc[1]:
        dir = game_interface.DOWN
    elif view.GetYPos() < loc[1]:
        dir = game_interface.UP

    return dir


def classify_svm(image):
    global svc
    classified = int(svc.predict(image)[0])
    print classified
    return classified


def classify(image):
    global network
    count = 0
    im = Image(0)
    im.pixels = [[0 for x in range(6)] for y in range(6)]
    for i in range(6):
        for j in range(6):
            im.pixels[i][j] = image[count]
            count += 1
    return network.Classify(im)


def get_move(view):
    print "rounds", view.GetRound()
    # neural network for classifying
    global network
    network.FeedForwardFn = FeedForward
    network.TrainFn = Train
    # list of locations in the order that we wish to visit them
    global locs
    if len(locs) == 0:
        generate_spiral((0, 0), 80)
        network.InitializeWeights()

    # list of locations do not want to return to
    global blackloc

    # current position
    currpos = (view.GetXPos(), view.GetYPos())
    # Remove current position from locations to visit
    if currpos in locs:
        locs.remove(currpos)

    # last 5 lifes
    global lifes
    lifes.insert(0, view.GetLife())
    count_n = 0
    for i in range(5):
        if lifes[i] > lifes[4]:
            count_n += 1
    if count_n >= 3:
        generate_spiral(currpos, 40)

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
        # build_svm()
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
