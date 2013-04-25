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


# Exploration/exploitation strategy two.
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
            
            #Choose exploration/exploitation strategy
            #epsilon greedy
            #to_explore = ex_strategy_one(s, num_iterations)
            #Boltzmann exploration
            to_explore = ex_strategy_one(s, num_iterations, Q, actions)
            
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
            # Get result of throw from dart thrower; update score if necessary
            loc = throw.throw(action)
            s_prime = s - throw.location_to_score(loc)
            if s_prime < 0:
                s_prime = s
                
            # Update experience:
            # increment number of times this action was taken in this state;
            # increment number of times we moved from this state to next state on this action.

            num_actions[s][a] += 1
            
            #alpha learning rate
            alpha = 0.3
            #gamma discount factor
            gamma = 0.5
            #find max action a_prime over Q[s_prime, a_prime]
            max_a = 0
            for a in range(len(actions)):
                if Q[s_prime][a_prime] > max_a:
                    max_a = Q[s_prime][a_prime]
            
            # update Q(s,a):= Q(s,a)+alpha(r+gamma max over a' Q(s',a') - Q(s,a))
            # s := s'
            Q[s][a] = Q[s][a] + alpha*(darts.R[s, actions[a]] + gamma*max_a - Q[s][a])
            
            s = s_prime
    return
