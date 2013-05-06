from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input
import random

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
