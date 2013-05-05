from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input
import random
import math

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
    
    network.inputs[i].raw_value = input[i]
    """
    network.CheckComplete()
    # 1) Assign input values to input nodes
    for i in range(len(input.values)):
        network.inputs[i].raw_value = input.values[i]
        network.inputs[i].transformed_value = input.values[i]
        
    # 2) Propagates to hidden layer
    
    def FeedLayer(layer):
        for node in layer:
            node.raw_value = NeuralNetwork.ComputeRawValue(node)
            node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value)

    FeedLayer(network.hidden_nodes)
            
    # 3) Propagates to the output layer
    FeedLayer(network.outputs)

    pass

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

    deltas = {}
    # 2) Then we compute the errors and update the weights starting with the last layer   
    
    def update_deltas(layer):
        for i, node in reversed(list(enumerate(layer))):
            error = 0.0
            if layer == network.outputs:
                error = target[i] - node.transformed_value
            else:
                for weight, child in zip(node.forward_weights, node.forward_neighbors):
                    error += weight.value * deltas[child]
            delta = error * node.transformed_value * (1 - node.transformed_value)
            deltas[node] = delta
            
    update_deltas(network.outputs)
    update_deltas(network.hidden_nodes)
         
    
    def update_weights(layer):            
        for node in reversed(layer):
            for weight, parent in zip(node.weights, node.inputs):
                weight.value += learning_rate * parent.transformed_value * deltas[node]
    
    update_weights(network.outputs)
    update_weights(network.hidden_nodes)

    pass

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
    for i in range(epochs):
        for j, input in enumerate(inputs):
            Backprop(network, input, targets[j], learning_rate)
    
    pass
    


# <--- Problem 3, Question 4 --->

class EncodedNetworkFramework(NetworkFramework):
    def __init__(self):
        """
        Initializatio.
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
        # Replace line below by content of function
        return [1.0 if i == label else 0.0 for i in range(2)]
        

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
        # Replace line below by content of function
        
        values = map(lambda node: node.transformed_value, self.network.outputs)
        return values.index(max(values))


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
        # Replace line below by content of function
        
        input = Input()
        for row in image.pixels:
            for pixel in row:
                input.values.append(pixel/256.0)
                
        return input
        
        

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
        # replace line below by content of function

        weights = [random.uniform(-0.01,0.01) for i in range(len(self.network.weights))]
        self.network.InitFromWeights(weights)
        pass



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
        self.network = NeuralNetwork()
        
        for i in range(0, 36):
            self.network.AddNode(Node(), NeuralNetwork.INPUT)
                
        # 2) Add an output node for each possible digit label.
        for i in range(0, 2):
            output = Node()
            for input in self.network.inputs:
#                output.AddInput(input, Weight(random.uniform(-0.01, 0.01)), self.network)
                output.AddInput(input, None, self.network)
            self.network.AddNode(output, NeuralNetwork.OUTPUT)
        pass


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
        self.network = NeuralNetwork()
        
        for i in range(36):
            self.network.AddNode(Node(), NeuralNetwork.INPUT)
        
        # 2) Adds the hidden layer
        for i in range(number_of_hidden_nodes):
            hidden_node = Node()
            for input in self.network.inputs:
                hidden_node.AddInput(input, None, self.network)
            self.network.AddNode(hidden_node, NeuralNetwork.HIDDEN)        
        
        # 3) Adds an output node for each possible digit label.
        for i in range(0, 2):
            output = Node()
            for hidden_node in self.network.hidden_nodes:
                output.AddInput(hidden_node, None, self.network)
            self.network.AddNode(output, NeuralNetwork.OUTPUT)
        
        pass
        

#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
    def __init__(self, number_of_hidden_nodes=30):
        """
        Arguments:
        ---------
        number_of_hidden_nodes: the number of hidden nodes

        Returns:
        --------
        None

        Description:
        -----------
        Initializes a network with two hidden layers. The network
        should have 196 input nodes, the specified number of
        hidden nodes, and 10 output nodes. The network should be,
        again, fully connected. That is, each input node is connected
        to every hidden node, each hidden_node is connected to every other
        hidden_node and each hidden_node is connected to every output node.

        """
        super(CustomNetwork, self).__init__() # <Don't remove this line>

        # 1) Adds an input node for each pixel
        self.network = NeuralNetwork()
        
        for i in range(49):
            self.network.AddNode(Node(), NeuralNetwork.INPUT)
        
#        # 2) Adds the first hidden layer
#        for i in range(number_of_hidden_nodes/2):
#            hidden_node = Node()
#            for input in self.network.inputs:
#                hidden_node.AddInput(input, None, self.network)
#            self.network.AddNode(hidden_node, NeuralNetwork.HIDDEN)        
#
#        for i in range(int(math.ceil(number_of_hidden_nodes/2.))):
#            hidden_node = Node()
#            for node in self.network.hidden_nodes[:(number_of_hidden_nodes/2)]:
#                hidden_node.AddInput(node, None, self.network)
#            self.network.AddNode(hidden_node, NeuralNetwork.HIDDEN)
#            
#        # 3) Adds an output node for each possible digit label.
#        for i in range(0, 10):
#            output = Node()
#            for hidden_node in self.network.hidden_nodes[(number_of_hidden_nodes/2):]:
#                output.AddInput(hidden_node, None, self.network)
#            self.network.AddNode(output, NeuralNetwork.OUTPUT)

        # 2) Adds the hidden layer
        for i in range(number_of_hidden_nodes):
            hidden_node = Node()
            for input in self.network.inputs:
                hidden_node.AddInput(input, None, self.network)
            self.network.AddNode(hidden_node, NeuralNetwork.HIDDEN)        
        
        # 3) Adds an output node for each possible digit label.
        for i in range(0, 2):
            output = Node()
            for hidden_node in self.network.hidden_nodes:
                output.AddInput(hidden_node, None, self.network)
            self.network.AddNode(output, NeuralNetwork.OUTPUT)

        pass

    
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
        of 7 x 7 items, with normalized values (that is, the maximum possible
        value should be 1).
        
        """
        input = Input()
        
        def compressPixels(pixels, row, col):
            total = 0
            for i in range(2):
                for j in range(2):
                    total += pixels[row+i][col+j]
            return (total/4.0)
        
        for i in xrange(0,len(image.pixels),2):
            for j in xrange(0, len(image.pixels[0]),2):
                input.values.append(compressPixels(image.pixels, i, j))
        print input        
        return input
