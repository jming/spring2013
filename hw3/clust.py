# clust.py
# -------
# Alisa Nguyen and Joy Ming

import sys
import random
import copy
from utils import *
from operator import itemgetter
import math

# import numpy


DATAFILE = "adults.txt"
#DATAFILE = "adults-small.txt"

#validateInput()

def validateInput():
    if len(sys.argv) != 3:
        return False
    if sys.argv[1] <= 0:
        return False
    if sys.argv[2] <= 0:
        return False
    return True


#-----------


def parseInput(datafile):
    """
    params datafile: a file object, as obtained from function `open`
    returns: a list of lists

    example (typical use):
    fin = open('myfile.txt')
    data = parseInput(fin)
    fin.close()
    """
    data = []
    for line in datafile:
        instance = line.split(",")
        instance = instance[:-1]
        data.append(map(lambda x:float(x),instance))
    return data


def printOutput(data, numExamples):
    for instance in data[:numExamples]:
        print ','.join([str(x) for x in instance])

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def main():
    # Validate the inputs
    if(validateInput() == False):
        print "Usage: clust numClusters numExamples"
        sys.exit(1);

    numClusters = int(sys.argv[1])
    numExamples = int(sys.argv[2])

    #Initialize the random seed
    
    random.seed()

    #Initialize the data

    
    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"


    data = parseInput(dataset)
    
    dataset.close()
    #printOutput(data,numExamples)

    # ==================== #
    # WRITE YOUR CODE HERE #
    # ==================== #
    def kmeans(data, K):
        #For each k, set u_k to a random vector
        u = []
        k = 0
        while k < K:
            i = random.randint(0,len(data)-1)
            if data[i] not in u:
                u.append(data[i])
                k += 1
        #print 'u before', u
        r = [[0 for x in range(len(data))] for y in range(K)]
        #r = [[0 for x in range(K)] for x in range(len(data))]
        #Repeat until convergence:
        # TODO: Implement convergence param
        converging = False
        round = 0
        while not converging:
            prevr = copy.deepcopy(r)
            #For each n, r_nk =  1 for k = argmin_k'(||x_n - u_k'||^2), and r_nk = 0 otherwise
            for n in range(len(data)):
                for k in range(K):
                    b = argmin(u, lambda l: squareDistance(data[n], l))
                    index = u.index(b)
                    #print 'b', b
                    r[k][n] = 1 if (k == index) else 0
            #For each k, update u_k by taking the mean for each attribute of all examples in cluster k
            for k in range(K):
                for a in range(len(u[k])):
                    u[k][a] = sum([data[n][a]*r[k][n] for n in range(len(data))])/sum(r[k][n] for n in range (len(data)))
            #if none of the examples are assigned to different clusters, convergence!
            if r == prevr:
                converging = True
            # print 'round', round
            round += 1
        #for each value of K, compute the mean squared error (the mean squared distance of each point from its closest prototype vector)
        sum_errors = [0. for x in range(K)]
        means = []
        for k in range(K):
            counter = 0.;
            for n in range(len(data)):
                if r[k][n] == 1:
                    sum_errors[k] += squareDistance(data[n], u[k])
                    counter+=1.
            #print 'error', sum_errors[k]
            #print 'counter', counter
            means.append(sum_errors[k]/counter)
        #print 'r', r
        #print 'u after', u
        #print 'data', data
        #print 'means', means
        #return means
        return sum(means)/len(means)
        # return r

    def HAC(data, K, param):

        #E = set of subsets of each individual example
        E = []
        for n in data:
            E.append([n])

        #Repeat until |E| = K
        while len(E) != K:
            dist = []
            for a in range(len(E)):
                for b in range(a + 1, len(E)):
                    if param == "min":
                        res = cmin(E[a], E[b], squareDistance)
                    elif param == "max":
                        res = cmax(E[a], E[b], squareDistance)
                    elif param == "mean":
                        res = cmean(E[a], E[b], squareDistance)
                    elif param == "cent":
                        res = ccent(E[a], E[b], squareDistance)
                    dist.append({"a": E[a], "b": E[b], "d": res})
            # Find a, b with smallest distance
            temp = [dist[c]["d"] for c in range(len(dist))]
            mmin = min(temp)
            mini = temp.index(mmin)

            a = dist[mini]["a"]
            b = dist[mini]["b"]

            # Remove a, b and replace with union
            E.remove(a)
            E.remove(b)
            E.append(a+b)

        # find number of instances per cluster
        clusters = []
        for e in E:
            clusters.append(len(e))

        # return number of instances per cluster and instance vectors
        return clusters, E

    def autoclass(data, K):
        # Continuous attributes:
        cont = [0, 9, 10, 44, 45, 46]
        #Set theta_c, theta_n^(1), theta_n^(0) to initial values
        #TODO: what initial values?
        thetac = [1./K for x in range(K)]
        #theta1 = [random.random() for x in range(len(data))]
        #theta0 = [random.random() for x in range(len(data))]
        #Each element tuple of (mean, variance) of normal distribution
        theta = [[random.random() for x in range(len(data[0]))] for y in range(K)]
        #print theta
        for k in range(K):
            for i in cont:
                theta[k][i] = (.5 + random.uniform(-.1, .1), .25 + random.uniform(-.1, .1))

        #print theta
        #Keep track of iterations until convergence
        round = 0
        #TODO implement convergence parameter
        #Stop your algorithm if , where d is the Euclidean distance, for example. Make sure not to set epsilon too large or you won't actually be converging. Also, state your convergence criteria that you used. Anywhere from 1e-5 to 1e-10 should be a good value for epsilon.
        # converging = False
        #Repeat until convergence:
                    # Expectation Step
            #WAIT PSUEDOCODE ONLY FOR BINARY WHOOPS. Look here: https://piazza.com/class#spring2013/cs181/185
            #Expectation Step
            #E[N_1] = 0

            #for each d, E[N_d^(0)] = 0
            #for each d, E[E_d^(1)] = 0
        EN = [0. for x in range(K)]
        E = [[0. for x in range(len(data[0]))] for y in range(K)]
        # while not converging:
        while round < 10:
            print round
            #For each instance x_n
            for x in range(len(data)):
                #probability of feature given class
                P = []
                tempproducts = [1. for x in range(K)]
                #for each cluster
                for k in range(len(theta)):
                    #for each attribute
                    for d in range(len(theta[k])):
                        # print theta[k][d]
#                        print 'k', k, 'd', d
#                        print theta[k][d]
                        if d in cont:
                            # print "isneg?", theta[k][d][1]
                            # print theta[k][d]
                            tempproducts[k] *= (1./(math.sqrt(2 * math.pi * theta[k][d][1])))*math.exp(-1 * math.pow(data[x][d] - theta[k][d][0], 2)/(2*theta[k][d][1]))
                            # print 'd', tempproducts[k]
                        else:
                            tempproducts[k] *= pow(theta[k][d], data[x][d])*pow((1 - theta[k][d]), (1 - data[x][d]))
                            # print 'not d', tempproducts[k]
                    P.append(thetac[k] * tempproducts[k])
                #for each cluster update
                for k in range(len(EN)):
                    EN[k] += P[k]/sum(P)
                #for each attribute
                for d in range(len(theta[k])):
                    #for each cluster
                    for k in range(len(E)):
                        E[k][d] += data[x][d]*P[k]/sum(P)
            # print 'sum E', sum(EN)
            # print 'P', P
            # print 'EN', EN
            # print 'E', E
            # print 'theta before', theta
            #Maximization step
            for k in range(len(thetac)):
                thetac[k] = EN[k]/len(data)
            for k in range(len(theta)):
                for d in range(len(theta[k])):
                    # m1 = E[k][d]/EN[k]
                    if d in cont:
                        if d == 45:
                            theta[k][d] = (.5 + random.uniform(-.1, .1), .25 + random.uniform(-.1, .1))
                        else:
                            bottom = sum(P)
                            topm = P[k] * sum([data[x][d] for x in range(len(data))])
                            m = topm/bottom
                            topv = P[k] * sum([pow((data[x][d] - m), 2) for x in range(len(data))])
                            v = topv/bottom
                            theta[k][d] = (m, v)
                            print k, d, P[k], (topm, topv, bottom)
                    else:
                        theta[k][d] = E[k][d]/EN[k]
                    # v = sum([P[k]*pow(data[x][d]-m,2) for x in range(len(data))])/sum([P[k] for k in range(len(P))])
                    # if d in cont:
                    #     for x in range(len(data)):
                    #         # if P[k]*pow(data[x][d] - m, 2) == 0:
                    #         print data[x][d]
                    #             # print "oops"
                    #     top = sum([P[k]*pow(data[x][d]-m, 2) for x in range(len(data))])
                    #     bottom = sum([P[x] for x in range(len(P))])
                    #     v = top/bottom
                    #     # print top, bottom
                    #     theta[k][d] = (m, v)
                    # else:
                    #     # print "discrete"
                    #     theta[k][d] = m
            # print 'theta after', theta
            round += 1
            # print 'round', round

        return 0

            #Theta_c = E[N1]/n
            #For each attribute d
                #Theta_d^1 =
                #Theta_d^0 =
    # print(kmeans(data[:numExamples], numClusters))
    # print(HAC(data[:numExamples], numClusters, "max"))
    print(autoclass(data[:numExamples], numClusters))

if __name__ == "__main__":
    validateInput()
    main()
