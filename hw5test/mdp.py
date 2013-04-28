

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
    probabilities = [0 for i in range(throw.START_SCORE + 1)]

    for i in range(-2,2):
        index = throw.wedges.index(a.wedge)+i
        if index >= throw.NUM_WEDGES:
            index = index % throw.NUM_WEDGES
        new_wedge = throw.wedges[index]

        prob_wedge = .4 / (pow(2,abs(i)))

        for j in range(-2,2):
            prob_ring = .4 / (pow(2,abs(j)))
            if a.ring == 0:
                if j == 0:
                    prob_ring = .4
                if j == 1 or j == -1:
                    prob_ring = .4
                if j == 2 or j == -2:
                    prob_ring = .2
            elif a.ring == 1:
                if j == 0 or j == -2: 
                    prob_ring = .5
                if j == -1: 
                    prob_ring = .2
                if j == 1:
                    prob_ring = .2
                if j == 2:
                    prob_ring = .1

            new_ring = a.ring + i
            if new_ring < 0:
                new_ring = new_ring % 7

            loc = throw.location(new_ring, new_wedge)
            score = int(throw.location_to_score(loc))

            new_score = s - score
            if new_score < 0:
                return 0

            prob = prob_wedge * prob_ring
            probabilities[new_score] = probabilities[new_score] + prob

    return probabilities[s_prime]



def infiniteValueIteration(gamma):
    # takes a discount factor gamma and convergence cutoff epislon
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
                
    
