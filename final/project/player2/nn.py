import os

weights = None
network = None

### NODE
class Weight:
  def __init__(self, value):
    self.value = value

class Node:
  """
  Attributes:
    inputs            : a list of node who are inputs for this node
    weights           : a list of weight objects, for links with input nodes
    fixed_weight      : w0 in the lecture notes and slides
    raw_value         : the linear combination of weights and input signals, that is w'x
    transformed_value : the signal emitted by this node, that is g(w'x)
  """
  def __init__(self):
    self.inputs = []
    self.weights = []
    self.fixed_weight = None
    self.raw_value = 0
    self.transformed_value = 0

  def AddInput(self, node, weight, network):
    self.inputs.append(node)
    if not weight:
      weight = network.GetNewWeight()
    self.weights.append(weight)
    if not self.fixed_weight:
      self.fixed_weight = network.GetNewWeight()

### NETWORK
class NeuralNetwork:
  INPUT = 1
  HIDDEN = 2
  OUTPUT = 3

  def __init__(self, number_of_hidden_nodes = 5, number_of_layers = 2):
    self.inputs = []
    self.hidden_nodes = []
    self.outputs = []
    self.weights = []
    
    # 1) Adds an input node for each pixel
    for i in range(36):
      self.AddNode(Node(), 1) 
    # 2)(a) Adds the first hidden layer

    for i in range(number_of_hidden_nodes):
    	node = Node()
    	self.AddNode(node, 2)
    	for j in range(36):
          node.AddInput(self.inputs[j], None, self)    
    # 2)(b) Adds the next hidden layer(s)

    for k in range(number_of_layers - 1):
    	for i in range(number_of_hidden_nodes):
    		node = Node()
    		self.AddNode(node, 2)
    		for j in range(number_of_hidden_nodes):
    			node.AddInput(self.hidden_nodes[number_of_hidden_nodes*k + j], None, self)		
    # 3) Adds an output node for each possible digit label.

    for i in range(2):
    	node = Node()
    	self.AddNode(node, 3)
    	for j in range(number_of_hidden_nodes):
    		node.AddInput(self.hidden_nodes[number_of_hidden_nodes*(number_of_layers-1) + j], None, self)
    # 4) Initialize weights

    for i in range(len(weights)):
      self.weights[i].value = weights[i].value


      
  def GetNewWeight(self):
    weight = Weight(0.0)
    self.weights.append(weight)
    return weight

  def AddNode(self, node, node_type):
    if node_type == self.INPUT:
      self.inputs.append(node)
    elif node_type == self.HIDDEN:
      self.hidden_nodes.append(node)
    else:
      self.outputs.append(node)
     
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

      
### FRAMEWORK
def FeedForward(input):
  """
  Arguments:
    input: an Input instance
  Description:
    This function propagates the inputs through the network.
    Note: network.inputs[i].raw_value = input[i]
  """
  # 1) Assign input values to input nodes
  for i in range(len(network.inputs)):
    network.inputs[i].raw_value = input[i]
    network.inputs[i].transformed_value = network.inputs[i].raw_value
  # 2) Propagates to hidden layer
  for i in range(len(network.hidden_nodes)):
    network.hidden_nodes[i].raw_value = network.ComputeRawValue(network.hidden_nodes[i])
    network.hidden_nodes[i].transformed_value = network.Sigmoid(network.hidden_nodes[i].raw_value)
  # 3) Propagates to the output layer
  for i in range(len(network.outputs)):
    network.outputs[i].raw_value = network.ComputeRawValue(network.outputs[i])
    network.outputs[i].transformed_value = network.Sigmoid(network.outputs[i].raw_value)
    
def GetNetworkLabel():
  """
  Returns:
    the 'best matching' label corresponding to the current output encoding
  """  
  List = map(lambda node: node.transformed_value, network.outputs)
  return List.index(max(List))
  
def ReadWeights(filename):
  filename = os.path.join(os.path.dirname(__file__), filename)
  infile = open(filename, 'r')
  global weights 
  weights = []
  for line in infile:
    value = float(line.strip())
    w = Weight(value)
    weights.append(w)  

    
def is_nutritious(image):
  """
  Image is a TUPLE of 36 binary digits.
  Returns a boolean indicating whether the image is nutritious. 
  Returns True if it is nutritious. Returns False if it is poisonous.
  """
  global weights

  if weights == None:
    ReadWeights('weights-356')

  global network
  if network == None:
    network = NeuralNetwork()
  
  input = list(image)
  FeedForward(input)
  output = GetNetworkLabel()
  
  return GetNetworkLabel()



def main():
  nutritious_file = open('nutritious.txt')

  nutritious_images = []

  for line in nutritious_file:
    image = line[1:-2].split(',')
    image = [float(i) for i in image]    
    nutritious_images.append(image)

  y = 0
  for i,image in enumerate(nutritious_images):
    if i == len(nutritious_images)-2: break
    image2 = nutritious_images[i+1]
    image3 = nutritious_images[i+2]

    image_average = []
    for i in range(len(image)):
      image_average.append((image[i]+image2[i]+image3[i])/3.0)

    if is_nutritious(image_average): y+=1
  print 'Nutritious accuracy:', y/float(len(nutritious_images)-2)
  print len(nutritious_images)

  poisonous_file = open('poisonous.txt')

  poisonous_images = []

  for line in poisonous_file:
    image = line[1:-2].split(',')
    image = [float(i) for i in image]    
    poisonous_images.append(image)

  y = 0
  for i,image in enumerate(poisonous_images):
    if i == len(poisonous_images)-2: break
    image2 = poisonous_images[i+1]
    image3 = poisonous_images[i+2]

    image_average = []
    for i in range(len(image)):
      image_average.append((image[i]+image2[i]+image3[i])/3.0)

    if not is_nutritious(image_average):  y+=1
  print 'Poisonous accuracy:', y/float(len(poisonous_images)-2)
  print len(poisonous_images)
