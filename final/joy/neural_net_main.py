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
  images1 = DataReader.GetImages('nutritious.txt', -1)
  print 'n', len(images1)
  images2 = DataReader.GetImages('poisnous.txt', -1)
  print 'p', len(images2)
  images = []
  for i in range(300):
      images.append(images1[i])
      images.append(images2[i])
      
  
  #images = images[:500]+images1[:500]
  print 'training', len(images)
  #print images

  # # Load the validation set.
  # validation1 = DataReader.GetImages('nutritious_valid.txt', -1)
  # print 'n', len(validation1)
  # validation2 = DataReader.GetImages('poisnous_valid.txt', -1) 
  # print 'p', len(validation2)
  # #validation = validation[:500]+validation2[:500]

  # validation = []
  # for i in range(100):
  #     validation.append(validation1[i])
  #     validation.append(validation2[i])
  # print 'validation', len(validation)

  # # Load the test data.
  # test1= DataReader.GetImages('nutritious_test.txt', -1)
  # print 'n', len(test1)
  # test2 = DataReader.GetImages('poisnous_test.txt', -1)
  # print 'p', len(test2)
  # test = []
  # for i in range(100):
  #     test.append(test1[i])
  #     test.append(test2[i])


  # Load in the training data.
  images = DataReader.GetImages('nutritious.txt', 1000) + DataReader.GetImages('poisnous.txt', 1000)
  random.shuffle(images)
  # print images
  for image in images:
    # print image.pixels
    assert len(image.pixels) == 6
    assert len(image.pixels[0]) == 6

  # Load the validation set.
  validation = DataReader.GetImages('nutritious_valid.txt', 100) + DataReader.GetImages('poisnous_valid.txt', 100)
  random.shuffle(validation)
  for image in validation:
    assert len(image.pixels) == 6
    assert len(image.pixels[0]) == 6

  # Load the test data.
  test = DataReader.GetImages('nutritious_test.txt', 100) + DataReader.GetImages('poisnous_test.txt', 100)
  random.shuffle(test)
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
  weightf = open('weights.txt', 'a')
  for i in range(len(network.network.weights)):
    print network.network.weights[i].value
    weightf.write(str(network.network.weights[i].value) + '\n')

if __name__ == "__main__":
  main()
