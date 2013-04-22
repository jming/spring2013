# Alisa and JOy

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
#REGIONS = [CENTER, INNER_RING, FIRST_PATCH, MIDDLE_RING, SECOND_PATCH, OUTER_RING, MISS]

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
    if points < 0:
        return 0
    #print points
    
    # Loop through to define transition function
    for i in range(-2,2):
        wedge_curr = (throw.wedges.index(a.wedge) + i)
        # Mod by number of wedges to wrap around if needed
        if wedge_curr >= throw.NUM_WEDGES:
            wedge_curr = wedge_curr%throw.NUM_WEDGES
        prob_wedge = 0.4/(pow(2, abs(i)))
        
        for j in range(-2,2):
            ring_curr = (a.ring + j)
            if ring_curr < 0:
                ring_curr = ring_curr % 7
            prob_ring = 0.4/(pow(2, abs(j)))
            
            '''if (a.ring == 0 and j < 0):
                ring_curr = 7 - ring_curr
            if (a.ring == 1 and j < -1):
                ring_curr = 7 - ring_curr'''
                
            if a.ring == 0:
                ring_curr = 7 - ring_curr
                if ring_curr == 0:
                    prob_ring = 0.4
                if ring_curr == 1:
                    prob_ring == 0.4
                if ring_curr == 2:
                    prob_ring = 0.2
            if a.ring == 1:
                ring_curr = 7 - ring_curr
                if ring_curr == 0:
                    prob_ring == 0.2
                if ring_curr == 1:
                    prob_ring = 0.5
                if ring_curr == 2:
                    prob_ring = 0.2
                if ring_curr == 3:
                    prob_ring == 0.1
            
            #print a.wedge, a.ring, j, i
            if(throw.location_to_score(throw.location(ring_curr, wedge_curr)) == points):
                prob += prob_wedge*prob_ring
                #print a.ring, j, i
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
            V[s] = Q[s][PI[s]]                                                        
            for a in actions:                                                         
                if V[s] <= Q[s][a]:                                                     
                    V[s] = Q[s][a]                                                        
                    PI[s] = a  

        notConverged = False
        for s in states:
            if abs(V[s] - V_prime[s]) > EPSILON:
                notConverged = True
