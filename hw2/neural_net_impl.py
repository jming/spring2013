from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input
import random


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

  # Pick a unit j all of whose parents have been processed
  for node in (network.hidden_nodes + network.outputs):
    # z = 0.
    # for i in range(len(node.inputs)):
    #   z += node.inputs[i].transformed_value * node.weights[i].value
    # node.raw_value = z
    node.raw_value = network.ComputeRawValue(node)
    node.transformed_value = network.Sigmoid(node.raw_value)

  '''
  # 2) Propagates to hidden layer
  #activations_hidden = []
  # go through all the nodes in the hidden nodes
  for node in network.hidden_nodes:
    z = 0.
    # sum the product of the input and weight
    for i in range(len(node.inputs)):
      z += node.inputs[i].raw_value * node.weights[i].value
    # append to array of all activations of hidden nodes
    node.raw_value = z
    node.transformed_value = network.Sigmoid(z)

  # 3) Propagates to the output layer
  #activations_output = []
  # go through all nodes in output nodes
  for node in network.outputs:
    z = 0.
    # sum the product of the input and weight
    for i in range(len(node.inputs)):
      z += node.inputs[i].transformed_value * node.weights[i].value
    # append to array of all activations of output nodes
    node.raw_value = z
    node.transformed_value = network.Sigmoid(z)
  '''

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
  #BEGIN COMMENT
  '''errors_outputs = []
  for k in range(len(network.outputs)):
    network.outputs[k].delta = network.SigmoidPrime(network.outputs[k].raw_value) * target[k] - network.outputs[k].transformed_value
    for i in range(len(network.hidden_nodes)):
    # TODO: add alpha in later
      network.outputs[k].weights[i] += network.outputs[k].transformed_value * network.outputs[k].delta
  # 3) We now propagate the errors to the hidden layer, and update the weights there too. Iterates through hidden nodes in reverse order
  for node in range(len(network.hidden_nodes), 0):
    e = 0.
    for i in range(len(network.outputs)):
      e += network.hidden_nodes[node].forward_weights[i] * network.outputs[i].delta
    network.hidden_nodes[node].delta = network.SigmoidPrime(network.hidden_nodes[node].raw_value) * e
    #update weights
    network.inputs[k].weights[node] += network.inputs[k].transformed_value * network.hidden_nodes[i].delta
  #END COMMENT'''

  '''
  #DOOVER
  for k in range(len(network.outputs)):
    network.outputs[k].delta = network.SigmoidPrime(network.outputs[k].raw_value) * (target[k] - network.outputs[k].transformed_value)
  for k in range(len(network.hidden_nodes)):
    network.hidden_nodes[k].e = 0
    for j in range(len(network.outputs)):
      network.hidden_nodes[k].e += network.hidden_nodes[k].weights[j].value * network.outputs[j].delta
    network.hidden_nodes[k].delta = network.SigmoidPrime(network.hidden_nodes[k].raw_value) * (network.hidden_nodes[k].e)
  for k in range(len(network.inputs)):
    network.inputs[k].e = 0
    for j in range(len(network.hidden_nodes)):
      network.inputs[k].e += network.inputs[k].weights[j].value * network.hidden_nodes[j].delta
    network.inputs[k].delta = network.SigmoidPrime(network.inputs[k].raw_value) * (network.inputs[k].e)
  
  #UPDATES WEIGHTS, TO DO INCLUDE ALPHA
  # for j in range(len(network.outputs)):
  #   for m in range(len(network.hidden_nodes)):
  #     network.outputs[j].weights[m].value += network.hidden_nodes[m].transformed_value*network.outputs[j].delta*learning_rate
  # for j in range(len(network.hidden_nodes)):
  #   for m in range(len(network.inputs)):
  #     network.hidden_nodes[j].weights[m].value += network.inputs[m].transformed_value*network.hidden_nodes[j].delta*learning_rate
  
  # update weights
  # for simplenetwork only
  for j in range(len(network.outputs)):
    for m in range(len(network.inputs)):
      #print network.outputs[j].weights[m].value, network.inputs[j].transformed_value, network.outputs[j].delta, learning_rate
      network.outputs[j].weights[m].value += network.inputs[j].transformed_value*network.outputs[j].delta*learning_rate
      #print network.outputs[j].weights[m].value
  print "output weights"
  for n in network.outputs:
    for i in range(len(n.weights)):
      print n.weights[i].value
  
  #TODO: for inputs BETTER: generalize for multilayer hidden networks
  #TODO: ? Move all update weights outside and do it together?
  '''

  # DOOVER 2??

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
      # print network.weights[12].value


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
    t.values = [0. for i in range(10)]
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
    #print a, a.index(max(a))
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

    for i in range(14):
      for j in range(14):
        inp.values.append(image.pixels[i][j] / 256.)

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
    # print "insideweights", self.network.weights
    random.seed()
    for i in range(len(self.network.weights)):
      self.network.weights[i].value = random.uniform(-.01, .01)
      # print self.network.weights[i].value
    # print "outsideweights", self.network.weights


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
    for i in range(196):
      n = Node()
      # n.weights.append(weight)
      # n.forward_weights.append(weight)
      #n.AddInput(n, false, self.INPUT)
      self.network.AddNode(n, self.network.INPUT)
    # 2) Add an output node for each possible digit label.
    for i in range(10):
      n = Node()
      for j in range(196):
        n.AddInput(self.network.inputs[j], None, self.network)
      self.network.AddNode(n, self.network.OUTPUT)
    
    # for i in self.network.inputs:
    #   for j in self.network.outputs:
    #     i.forward_neighbors.append(j)
    #     j.inputs.append(i)
    
    #self.InitializeWeights()
    #magnitudes = [1.0, 0.1, 0.01, 0.001]
    #performance = [0.0 for i in range(len(magnitudes))]
    #for i in range(len(magnitudes)):
      #Train(self.inputs, self.targets, magnitudes[i], 100)
      #performance[i] = self.Performance()

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

    number_of_hidden_nodes = 15

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

    # 3) Adds an output node for each possible digit label.
    for i in range(10):
      n = Node()
      for j in range(number_of_hidden_nodes):
        n.AddInput(self.network.hidden_nodes[number_of_hidden_nodes + j], None, self.network)
      self.network.AddNode(n, self.network.OUTPUT)
