import math
import game_interface
from history import History
from collections import defaultdict

UNDEFINED = -1000
goal = (UNDEFINED,UNDEFINED)

INTERVAL = 5 # Predetermined in the clustering process

explore = True
steps = [game_interface.LEFT]

def goWhere(history, prior):
  global goal
  global explore

  positions = history.getPositions()
  bonus = history.getBonus()
  life_per_turn = history.getLifePerTurn()

  if explore: switchMode(history)

  if len(positions) <= 1 or positions[-1] == goal:
    goal = next_goal(positions)
    while goal in positions:
         positions.append(goal)
         goal = next_goal(positions)    
  direction = to_goal(goal, positions)
  return direction


def switchMode(history):
   global explore
   global INTERVAL
   global steps

   eat_results = history.getEatResults()
   count = 0

   if len(eat_results) > 3:
       for e in eat_results[-3:]: count += e
   if count >= 2:
       #print 'SWITCH...............'
       explore = False
       INTERVAL = 1
       steps = [game_interface.UP]



def next_goal(positions):
  (x,y) = positions[-1]
   
  (c1, c2, c3) = get_step_counts(steps)
  # figure out what step is
  step = steps[-1]
  if c1==c2:
     if c3==c2+INTERVAL: step = next_step(steps[-1])
  elif c1 < c2:
     if c3==c2: step = next_step(steps[-1])     

  goal = next_cell(positions[-1], step)

  steps.append(step)
  return goal      
  
def get_step_counts(steps):
  if len(steps) <= INTERVAL:
     return (0,0,len(steps))
  elif len(steps) <= INTERVAL*2:
     return (0,9,len(steps)-9)
  elif len(steps) <= INTERVAL*4:
     return (INTERVAL,INTERVAL,len(steps)-INTERVAL*2)
  step_dict = defaultdict(int)
  step_array = []

  for s in reversed(steps):
     if s not in step_dict and len(step_dict) == 3: break
     if s not in step_dict: step_array.insert(0, s)
     step_dict[s] += 1
  
  counts = [step_dict[s] for s in step_array]
  return (counts[0], counts[1], counts[2])














def to_goal(goal, positions):
  # it doesn't go to previously visited cell
  current_position = positions[-1]
  (x1, y1) = current_position
  (x2, y2) = goal
  possible_directions = []
  if x2 > x1: possible_directions.append(game_interface.RIGHT)
  if x2 < x1: possible_directions.append(game_interface.LEFT)
  if y2 > y1: possible_directions.append(game_interface.UP)
  if y2 < y1: possible_directions.append(game_interface.DOWN)

  if len(possible_directions) == 1:
      return possible_directions[0]
  else: 
      for d in possible_directions:
          next_pos = next_cell(current_position, d)
          if next_pos not in positions: return d
  return possible_directions[0]

def distance(a, b):
  x1, y1 = a
  x2, y2 = b
  return math.fabs(x1-x2)+math.fabs(y1-y2)

def next_step(step):
  if step == game_interface.UP:
     return  game_interface.RIGHT
  elif step == game_interface.DOWN:
     return  game_interface.LEFT
  elif step == game_interface.LEFT:
     return  game_interface.UP
  elif step == game_interface.RIGHT:
     return  game_interface.DOWN
  else: print 'Next Step Error!!'

           
def next_cell(current_cell, direction):
  (x, y) = current_cell
  if direction == game_interface.RIGHT: return (x+1, y)
  elif direction == game_interface.LEFT: return (x-1, y)
  elif direction == game_interface.UP: return (x, y+1)
  else: return (x, y-1)
  

"""
def next_goal(positions, bonus, life_per_turn, prior):
  # Find a goal that
  # A. we've never visited
  # B. Maximizes bonus*p(nutritious)-life_per_turn*distance

  (x,y) = positions[-1]
  max_dest = (UNDEFINED, UNDEFINED) 
  max_reward = UNDEFINED

  for x_inc in range(-5, 5):
    for y_inc in range(-5, 5):
       xx = x+x_inc
       yy = y+y_inc
       if (xx,yy) not in positions:
          p = prior[(xx, yy)]
          d = distance((xx,yy),(x,y))
          reward = bonus * p - float(life_per_turn)*d
          if reward > max_reward:
             max_reward = reward
             max_dest = (xx, yy)
  #print 'Destination, reward =', positions[-1], max_dest, max_reward
  return max_dest    
"""
