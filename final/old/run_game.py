import player1.player
import player2.player
import game_interface
import random
import signal
import sys
import time
import traceback
from optparse import OptionParser
from neural_net import *
from neural_net_impl import *
from data_reader_ours import *

class TimeoutException(Exception):
  def __init__(self):
    pass

def get_move(view, cmd, options, player_id, network):
  def timeout_handler(signum, frame):
    raise TimeoutException()
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1)
  try: 
    (mv, eat) = cmd(view, network)
    # Clear the alarm.
    signal.alarm(0)
  except TimeoutException:
    # Return a random value
    # Should probably log this to the interface
    (mv, eat) = (random.randint(0, 4), False)
    error_str = 'Error in move selection (%d).' % view.GetRound()
    if options.display:
      game_interface.curses_debug(player_id, error_str)
    else:
      print error_str
  return (mv, eat)

def run(options):
  game = game_interface.GameInterface(options.plant_bonus,
                                      options.plant_penalty,
                                      options.observation_cost,
                                      options.starting_life,
                                      options.life_per_turn)
  player1_view = game.GetPlayer1View()
  player2_view = game.GetPlayer2View()
  
  '''BEGIN NEURAL NETWORK ADDITIONS'''
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
    
  '''END OF NEURAL NETWORK ADDITIONS'''

  if options.display:
    if game_interface.curses_init() < 0:
      return
    game_interface.curses_draw_board(game)
  
  # Keep running until one player runs out of life.
  count = 0
  fp = open('poisnous_valid.txt', 'a')
  fn = open('nutritious_valid.txt', 'a')
  while count < 5000:
    (mv1, eat1) = get_move(player1_view, player1.player.get_move, options, 1, network)
    (mv2, eat2) = get_move(player2_view, player2.player.get_move, options, 2, network)

    o1 = player1_view.GetLife()
    o2 = player2_view.GetLife()
    game.ExecuteMoves(mv1, eat1, mv2, eat2)
    if options.display:
      game_interface.curses_draw_board(game)
      game_interface.curses_init_round(game)
    else:
      print mv1, eat1, mv2, eat2
      print player1_view.GetLife(), player2_view.GetLife()
    # Check whether someone's life is negative.
    l1 = player1_view.GetLife()
    l2 = player2_view.GetLife()

    image1 = player1.player.image1
    image2 = player2.player.image2

    # print image1
    # print image2

    if image1 != []:
      print image1
      if l1 == o1 + 19:
        for image in image1:
          fn.write(str(image) + '\n')
        fn.write('\n')
      else:
        for image in image1:
          fp.write(str(image) + '\n')
        fp.write('\n')
    if image2 != []:
      print image2
      if l2 == o2 + 19:
        for image in image2:
          fn.write(str(image) + '\n')
        fn.write('\n')
      else:
        for image in image2:
          fp.write(str(image) + '\n')
        fp.write('\n')


    # if l1 <= 0 or l2 <= 0:
    #   if options.display:
    #     winner = 0
    #     if l1 < l2:
    #       winner = 2
    #     else:
    #       winner = 1
    #     game_interface.curses_declare_winner(winner)
    #   else:
    #     if l1 == l2:
    #       print 'Tie, remaining life: %d v. %d' % (l1, l2)
    #     elif l1 < l2:
    #       print 'Player 2 wins: %d v. %d' % (l1, l2)
    #     else:
    #       print 'Player 1 wins: %d v. %d' % (l1, l2)
    #   # Wait for input
    #   sys.stdin.read(1)
    #   if options.display:
    #     game_interface.curses_close()
    #   break
    count += 1

def main(argv):
  parser = OptionParser()
  parser.add_option("-d", action="store", dest="display", default=1, type=int,
                    help="whether to display the GUI board")
  parser.add_option("--plant_bonus", dest="plant_bonus", default=20,
                    help="bonus for eating a nutritious plant",type=int)
  parser.add_option("--plant_penalty", dest="plant_penalty", default=10,
                    help="penalty for eating a poisonous plant",type=int)
  parser.add_option("--observation_cost", dest="observation_cost", default=1,
                    help="cost for getting an image for a plant",type=int)
  parser.add_option("--starting_life", dest="starting_life", default=100,
                    help="starting life",type=int)
  parser.add_option("--life_per_turn", dest="life_per_turn", default=1,
                    help="life spent per turn",type=int)
  (options, args) = parser.parse_args()

  try:
    run(options)
  except KeyboardInterrupt:
    if options.display:
      game_interface.curses_close()
  except:
    game_interface.curses_close()
    traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
  main(sys.argv)
