from data_reader import *
from neural_net import *
from neural_net_impl import *
import sys
import random


def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'main.py', '-e', 20, '-r', 0.1, '-t', 'Simple' ]) = { '-e':20, '-r':5, '-t': 'simple' }"""
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
  images = DataReader.GetImages('nutritious.txt', 1000) + DataReader.GetImages('poisnous.txt', 1000)
  # print images
  for image in images:
    # print image.pixels
    assert len(image.pixels) == 6
    assert len(image.pixels[0]) == 6

  # Load the validation set.
  validation = DataReader.GetImages('nutritious_valid.txt', 100) + DataReader.GetImages('poisnous_valid.txt', 100)
  for image in validation:
    assert len(image.pixels) == 6
    assert len(image.pixels[0]) == 6

  # Load the test data.
  test = DataReader.GetImages('nutritious_test.txt', 100) + DataReader.GetImages('poisnous_test.txt', 100)
  for image in test:
    assert len(image.pixels) == 6
    assert len(image.pixels[0]) == 6

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
  # print "weights"
  # for i in range(len(network.network.weights)):
  #   print network.network.weights[i].value
  

  # Displays information
  print '* * * * * * * * *'
  print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
  print 'Type of network used: %s' % network.__class__.__name__
  print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
         (len(network.network.inputs), len(network.network.hidden_nodes),
          len(network.network.outputs)))
  print '* * * * * * * * *'
 
  # Train the network.
  network.Train(images, validation, test, rate, epochs)

  # print "weights"
  # for i in range(len(network.network.weights)):
  #   print network.network.weights[i].value

if __name__ == "__main__":
  main()
