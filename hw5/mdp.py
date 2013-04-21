

# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

# make pi global so computation need only occur once
PI = {}
EPSILON = .001
REGIONS = [CENTER, INNER_RING, FIRST_PATCH, MIDDLE_RING, SECOND_PATCH, OUTER_RING, MISS]

# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  #for ele in PI:
    #print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):

  return PI[score]

# define transition matrix/ function
def T(a, s, s_prime):
    # takes an action a, current state s, and next state s_prime
    # returns the probability of transitioning to s_prime when taking action a in state s
    # figure out where would give you that many points
    # figure out the probability of landing there
    prob = 0
    points = s - s_prime

    # if it hits the spot exactly
    if throw.location_to_score(throw.location(a.ring, a.wedge)) == points:
        prob += 0.4

    # if it hits a directly adjacent neighbor
    index = REGIONS.index(a.ring)
    neighbors = [REGIONS[index-1], REGIONS[index+1]]
    index_wedge = throw.wedges.index(a.wedge)
    if index_wedge == 0:
        neighbors_wedges = [throw.wedges[len(index_wedge)-1], throw.wedges[index_wedge+1]]
    elif index_wedge == len(index_wedge):
        neighbors_wedges = [throw.wedges[index_wedge - 1], throw.wedges[0]]
    else:
        neighbors_wedges = [throw.wedges[index_wedge-1], throw.wedges[index_wedge+1]]

    for neighbor in neighbors:
        if neighbor == CENTER or neighbor == INNER or neighbor == MISS:
            if throw.location_to_score(throw.location(neigbhor, a.wedge)) == points:
                prob += 0.2
        else:
            for n in neighbors_wedges:
                if throw.location_to_score(throw.location(neighbor, n)) == points:
                    prob += 0.2*0.2
    return prob


def infiniteValueIteration(gamma):
    # takes a discount factor gamma and convergence  cutoff epislon
    # returns

    V = {}
    Q = {}
    V_prime = {}

    states = darts.get_states()
    actions = darts.get_actions()

    notConverged = True

    # intialize value of each state to 0
    for s in states:
        V[s] = 0
        Q[s] = {}

    # until convergence is reached
    while notConverged:

        # store values from previous iteration
        for s in states:
            V_prime[s] = V[s]

        # update Q, pi, and V
        for s in states:
            for a in actions:

                # given current state and action, sum product of T and V over all states
                summand = 0
                for s_prime in states:
                    summand += T(a, s, s_prime)*V_prime[s_prime]

                # update Q
                Q[s][a] = darts.R(s, a) + gamma*summand

            # given current state, store the action that maximizes V in pi and the corresponding value in V
            PI[s] = actions[0]
            for a in actions:
                if V[s] <= Q[s][a]:
                    V[s] = Q[s][a]
                    PI[s] = a

        notConverged = False
        for s in states:
            if abs(V[s] - V_prime[s]) > EPSILON:
                notConverged = True
