from data_reader_ours import *
from neural_net import *
from neural_net_impl import *
import sys
import random


def parseArgs(args):
    """Parses arguments vector, looking for switches of the form -key {optional value}.
    For example:
        parseArgs([ 'main.py', '-e', 20, '-r', 0.1, '-m', 'Simple' ]) = { '-e':20, '-r':5, '-t': 'simple' }"""
    args_map = {}
    curkey = None
    for i in xrange(1, len(args)):
        if args[i][0] == '-':
            args_map[args[i]] = True
            curkey = args[i]
        else:
            assert curkey
            args_map[curkey] = args[i]
            curkey = None
    return args_map

def validateInput(args):
    args_map = parseArgs(args)
    assert '-e' in args_map, "A number of epochs should be specified with the flag -e (ex: -e 10)"
    assert '-r' in args_map, "A learning rate should be specified with the flag -r (ex: -r 0.1)"
    assert '-t' in args_map, "A network type should be provided. Options are: simple | hidden | custom"
    return(args_map)

def main():

    # Parsing command line arguments
    args_map = validateInput(sys.argv)
    epochs = int(args_map['-e'])
    rate = float(args_map['-r'])
    networkType = args_map['-t']


    # Load in the training data.
    images1 = DataReader.GetImages('nutritious_test.txt', -1)
    print 'n', len(images1)
    images2 = DataReader.GetImages('poisnous_test.txt', -1)
    print 'p', len(images2)
    images = []
    for i in range(500):
        images.append(images1[i])
        images.append(images2[i])
        
    
    #images = images[:500]+images1[:500]
    print 'training', len(images)
    #print images

    # Load the validation set.
    validation1 = DataReader.GetImages('nutritious_valid.txt', -1)
    print 'n', len(validation1)
    validation2 = DataReader.GetImages('poisnous_valid.txt', -1) 
    print 'p', len(validation2)
    #validation = validation[:500]+validation2[:500]

    validation = []
    for i in range(500):
        validation.append(validation1[i])
        validation.append(validation2[i])
    print 'validation', len(validation)

    # Initializing network

    if networkType == 'simple':
        network = SimpleNetwork()
    if networkType == 'hidden':
        network = HiddenNetwork()
    if networkType == 'custom':
        network = CustomNetwork()

    # Hooks user-implemented functions to network
    network.FeedForwardFn = FeedForward
    network.TrainFn = Train

    # Initialize network weights
    network.InitializeWeights()

    # Displays information
    print '* * * * * * * * *'
    print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
    print 'Type of network used: %s' % network.__class__.__name__
    print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
                 (len(network.network.inputs), len(network.network.hidden_nodes),
                    len(network.network.outputs)))
    print '* * * * * * * * *'
    
    # Load the test data.
    test1= DataReader.GetImages('nutritious.txt', -1)
    print 'n', len(test1)
    test2 = DataReader.GetImages('poisnous.txt', -1)
    print 'p', len(test2)
    test_images = []
    for i in range(500):
        test_images.append(test1[i])
        test_images.append(test2[i])
    
    # Train the network.
    network.Train(images, validation, test_images, rate, epochs)
    
    perf_test = network.Performance(test_images)
    print 'Test Performance: %.8f ' % (perf_test)

weights = [-1.20427123442, -0.00424628826209, -0.964278197935, 0.244331250746, -0.288361816768, 2.10331453187, 1.54719783793, -0.658764513145, -0.279464443265, -0.239199110854, 0.626246546816, 0.440893228302, 0.473173577324, -1.05978067597, -0.262451719579, -2.21658810993, -2.15768401141, 0.145261082528, 0.991536326011, -0.0736698964158, 1.84804953828, 1.63938467372, -0.834576894308, 2.50325730411, 2.14284995071, 0.143765814209, 1.50359473634, 1.22069882314, 0.350053746782, 0.524158583252, 1.04273282167, -1.80564022242, -0.0725532272597, 0.771179844162, -0.550706391542, 0.363486090709, 1.69230357299, 1.20251076086, -0.00554224349246, 0.962074784256, -0.2409875051, 0.289124899972, -2.10232633516, -1.54669120246, 0.659005070648, 0.281563336586, 0.238999978889, -0.622895589472, -0.441386568922, -0.474736885751, 1.05943876453, 0.264183110881, 2.21908409518, 2.15827013768, -0.142943837766, -0.990326995619, 0.0753422975565, -1.84610648642, -1.64165804177, 0.834746087351, -2.50219968992, -2.1421926446, -0.142191932695, -1.50371336742, -1.21985971962, -0.350600031229, -0.523680717768, -1.04185239539, 1.80382544127, 0.0763526628852, -0.77636893571, 0.55016715994, -0.362973620148, -1.69245645096]    
    
def test():
    network = SimpleNetwork()
    for i in range(0, 36):
        network.AddNode(Node(), NeuralNetwork.INPUT)
        
    network.InitializeWeights()
        
# 2) Add an output node for each possible digit label.
    for i in range(0, 2):
        output = Node()
        count = 0
        print len(network.inputs)
        for input in network.inputs:
            output.AddInput(input, Weight(weights[count]), network)
            count+=1
            #output.AddInput(input, None, self.network)
        network.AddNode(output, NeuralNetwork.OUTPUT)
    print len(network.weights)
    #network.InitFromWeights(weights)
    
    
    
    
    
test()
    
#if __name__ == "__main__":
#    main()
