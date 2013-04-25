from random import *
import throw
import darts
 
# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.

def start_game():

  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES)) 

def get_target(score):

  if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
  
  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))


# Exploration/exploitation strategy one.
def ex_strategy_one():
  return 0


# Exploration/exploitation strategy two.
def ex_strategy_two():
  return 1


# The Q-learning algorithm:
def Q_learning():

    # Set things up like in modelbased
    actions = darts.get_actions()
    states = darts.get_states()

    pi_star = {}
    g = 0
    num_actions = {}
    num_iterations = 0
    Q = {}

    # Initialize Q(s,a) arbitrarily -> all to 0
    for s in states:
        pi_star[s] = random.randint(0, len(actions)-1)
        num_actions[s] = {}
        Q[s] = {}
        
        for a in range(len(actions)):
            num_actions[s][a] = 0
            Q[s][a] = 0

    # Repeat (for each episode)
    for g in range(1, num_games + 1):
        
        # run a single game
        s = throw.START_SCORE
        
        # repeat (for each step of episode) until s is terminal (????)
        while s > 0: #??? IS THIS RIGHT ???#
            # choose a from s using policy derived from Q
            num_iterations += 1
            to_explore = ex_strategy_one(s, num_iterations)
            if to_explore == 2:
                a = newindex
                action = newaction
            elif to_explore:
                a = random.randint(0, len(actions)-1)
                action = actions[a]
            else:
                a = pi_star[s]
                action = actions[a]
            # take action a, observe r, s'
            # update Q(s,a):= Q(s,a)+alpha(r+gamma max over a' Q(s',a') - Q(s,a))
            # s := s'

    # Choose actions
    # update Q-fuctions
    # Update rule: Q(s,a) <- Q(s, a) + alpha (r + \gamma max_a' \in A Q(s', a')) - Q(s, a))
    return
