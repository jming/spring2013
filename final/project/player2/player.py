import time
import navigate
import eat
import pickle
import os
from history import History

history = None
prior = {}

def get_move(view):
  global history

  if history is None:
    history = History(view)
    load_prior()
  else:
    history.updateStatus(view)

  learn() # update the prior

  direction = navigate.goWhere(history, prior)
  shouldeat = eat.shouldEatOrNot(view, history, prior)

  time.sleep(0.1)
  return (direction, shouldeat)

def learn():
  positions = history.getPositions()
  if len(positions) < 2: return
  eat_results = history.getEatResults()
  (x, y) = positions[-2] 
  if not eat_results[-1]:
    for x_inc in [-1, 0, 1]:
      for y_inc in [-1, 0, 1]:
         prior[(x,y)] -= 0.01
  elif eat_results[-1]:
    for x_inc in [-1, 0, 1]:
      for y_inc in [-1, 0, 1]:
         prior[(x,y)] += 0.01


def load_prior():
   global prior
   filename = os.path.join(os.path.dirname(__file__), 'prior')
   pkl_file = open(filename, 'rb')
   compressed_prior = pickle.load(pkl_file)
   pkl_file.close()
   for (x, y) in compressed_prior:
     for x_inc in [-1,0,1]:
       for y_inc in [-1, 0, 1]:
         prior[(x+x_inc,y+y_inc)] = compressed_prior[(x,y)]
