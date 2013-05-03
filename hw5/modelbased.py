import random
import throw
import darts
import math

EPSILON_VI = .001

# NOTE: We did not implement the interface methods start_game and get_target.
# Functions below are simply the default darts player discussed in modelfree.py.
# Instead, we defined the function modelbased, which uses the helper methods
# ex_strategy_one and ex_strategy_two.

def start_game():

  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))

def get_target(score):

  if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
  
  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))

# Define your first exploration/exploitation strategy here. Return 0 to exploit and 1 to explore.
# You may want to pass arguments from the modelbased function.
def ex_strategy_one(s, num_iterations):
  # implement epsilon greedy algorithm
  
  #epsilon is equal to an exponentially decaying function
  e = 500*math.exp(-0.0675*num_iterations)
  x = random.random()
  # given current state, pick best with prob e
  if x < e:
    # with probability epsilon, explore by returning 1
    #return pi_star[s]
    return 1
  # With prob 1-e, exploit by returning 0
  else:
    y = random.choice([i for i in range(throw.NUM_WEDGES*6)])
    #return darts.get_actions()[y]
    return 0
    
# Define your second exploration/exploitation strategy here. Return action
# You may want to pass arguments from the modelbased function.
# Boltzmann Exploration
def ex_strategy_two(s, num_iterations, Q, actions):
    
    probs = [0.0 for x in range(len(actions))]
    #Exponentially decaying function
    T = 500*math.exp(-0.0675*num_iterations)+100
    #T = 1./num_iterations
    for a in range(len(actions)):
        #print Q[s][a], T
        probs[a] = math.exp(Q[s][a]/T)
    total = sum(probs)
    
    for a in range(len(probs)):
        probs[a] = probs[a]/total
    
    r = random.random()
    cumulative = 0
    for a in range(len(probs)):
        cumulative += probs[a]
        if r < cumulative:
            return a, actions[a]
    
    return a, actions[a]
    

# Implement a model-based reinforcement learning algorithm.
# Given num_games (the number of games to play), store the
# learned transition probabilities in T.
def modelbased(gamma, epoch_size, num_games):

    # store all actions (targets on dartboard) in actions array
    actions = darts.get_actions()
    states = darts.get_states()
    
    pi_star = {}
    g = 0
    num_actions = {}
    num_transitions = {}
    T_matrix = {}
    num_iterations = 0
    Q = {}
    
    
    # Initialize all arrays to 0 except the policy, which should be assigned a random action for each state.
    for s in states:
        pi_star[s] = random.randint(0, len(actions)-1)
        num_actions[s] = {}
        num_transitions[s] = {}
        T_matrix[s] = {}
        Q[s] = {}
        
        for a in range(len(actions)):
            num_actions[s][a] = 0
            Q[s][a] = 0
            
        for s_prime in states:
            num_transitions[s][s_prime] = {}
            T_matrix[s][s_prime] = {}
            for a in range(len(actions)):
                num_transitions[s][s_prime][a] = 0
                T_matrix[s][s_prime][a] = 0


    # play num_games games, updating policy after every EPOCH_SIZE number of throws
    for g in range(1, num_games + 1):
    
     # run a single game
        s = throw.START_SCORE
        while s > 0:

            num_iterations += 1
    
            # The following two statements implement two exploration-exploitation
            # strategies. Comment out the strategy that you wish not to use.

            #to_explore = ex_strategy_one(s, num_iterations)
            # Second strategy
            to_explore = 2
            newindex, newaction = ex_strategy_two(s, num_iterations, Q, actions)
    
            if to_explore == 2:
                a = newindex
                action = newaction
            elif to_explore:
             # explore
                a = random.randint(0, len(actions)-1)
                action = actions[a]
            else:
             # exploit
                a = pi_star[s]
                action = actions[a]
            
            # Get result of throw from dart thrower; update score if necessary
            loc = throw.throw(action)
            s_prime = s - throw.location_to_score(loc)
            if s_prime < 0:
                s_prime = s
                
            # Update experience:
            # increment number of times this action was taken in this state;
            # increment number of times we moved from this state to next state on this action.

            num_actions[s][a] += 1
            num_transitions[s][s_prime][a] += 1

# Next state becomes current state
            s = s_prime

            # Update our learned MDP and optimal policy after every EPOCH_SIZE throws,
            # using infinite-horizon value iteration.

            if num_iterations % epoch_size == 0:

                # Update transition probabilities
                for i in states:
                    for j in states:
                        for k in range(len(actions)):
                            if num_actions[i][k] != 0:
                                T_matrix[i][j][k] = float(num_transitions[i][j][k]) / float(num_actions[i][k])

                # Update strategy (stored in pi) based on newly updated reward function and transition
                # probabilities
                T_matrix, pi_star, Q = modelbased_value_iteration(gamma, T_matrix, pi_star)
    
    print "Average turns = ", float(num_iterations)/float(num_games)


# A modified version of infinite horizon value iteration from part 2 */
def modelbased_value_iteration(gamma, T_matrix, pi_star):
  V = {}
  V[0] = {}
  V[1] = {}
  converging = 0
  num_iterations = 0
  Q = {}

  # Get all possible actions
  actions = darts.get_actions()

  states = darts.get_states()

  # initialize v
  for s in states:
    V[0][s] = 0
    V[1][s] = 0

  # iterate until all state values (v[s]) converge
  while not(converging):
    num_iterations += 1
    for s in states:
      Q[s] = {}
      for a in range(len(actions)):

        # find the value of each action, given state s
        Q[s][a] = darts.R(s, actions[a])
        for s_prime in states:

          Q[s][a] += gamma * T_matrix[s][s_prime][a] * V[0][s_prime]

          # find the action that maximizes Q and the maximum value of Q
          if a == 0 or (Q[s][a] >= V[1][s]):
            pi_star[s] = a
            V[1][s] = Q[s][a]

                  
    # values of v for iteration k become the values of v for iteration k-1
    converging = True
    for s in states:
      # check for one component that does not converge
      if EPSILON_VI < abs(V[0][s] - V[1][s]):
        converging = False

      V[0][s] = V[1][s]

  return T_matrix, pi_star, Q
