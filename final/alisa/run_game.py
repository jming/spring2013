import player1.player
import player2.player
import game_interface
import random
import signal
import sys
import time
import traceback
from optparse import OptionParser

class TimeoutException(Exception):
  def __init__(self):
    pass

def get_move(view, cmd, options, player_id):
  def timeout_handler(signum, frame):
    raise TimeoutException()
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1)
  try: 
    (mv, eat) = cmd(view)
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

  if options.display:
    if game_interface.curses_init() < 0:
      return
    game_interface.curses_draw_board(game)
  

  nlocs1 = [[0 for x in range(100)] for x in range(100)]
  #plocs1 = [[0 for x in range(50)] for x in range(50)]
  plocs2 = [[0 for x in range(100)] for x in range(100)]
  #plocs2 = [[0 for x in range(50)] for x in range(50)]
  # Keep running until one player runs out of life.
  fp = open('locs1.txt', 'a')
  fn = open('locs2.txt', 'a')
  f0 = open('locationsvisited.txt', 'a')
  count = 0
  while count < 5000:
    (mv1, eat1) = get_move(player1_view, player1.player.get_move, options, 1)
    (mv2, eat2) = get_move(player2_view, player2.player.get_move, options, 2)

    loc1x = player1_view.GetXPos()
    loc1y = player1_view.GetYPos()
    loc2x = player2_view.GetXPos()
    loc2y = player2_view.GetYPos()
    
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

    #image1 = player1.player.image1
    #image2 = player2.player.image2

    # print image1
    # print image2

    if eat1:
      if l1 == o1 + 19:
        locs1[loc1x+50][loc1y+50] += 1
        #f0.write('n')
        #f0.write(str(loc1x)+str(loc1y))  
      else:
        locs1[loc1x+50][loc1y+50] -= 1
        #f0.write('p')
        #f0.write(str(loc1x) + str(loc1y)) 
    if eat2:
      if l2 == o2 + 19:
        locs2[loc2x+50][loc2y+50] += 1
        #f0.write('n')
        #f0.write(str(loc2x) + str(loc2y)) 
      else:
        locs2[loc2x+50][loc2y+50] -= 1
        #f0.write('p')
        #f0.write(str(loc2x) + str(loc2y)) 
    
    count += 1
    
  fn.write(str(locs1))
  fp.write(str(locs2))

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
