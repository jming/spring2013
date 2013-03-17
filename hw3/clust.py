# clust.py
# -------
# Alisa Nguyen and Joy Ming

import sys
import random
import copy
from utils import *
# from operator import itemgetter
import math
from scipy.misc import logsumexp
import time

DATAFILE = "adults.txt"
#DATAFILE = "adults-small.txt"
EPSILON = 1e-3

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
            # print round
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
        meansquarederror = sum(means)/len(means)
        #for each value of K, compute the mean
        return u
        #return sum(means)/len(means)
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
        
        #TODO: return means for each cluster:

    def autoclass(data, K):
        # Continuous attributes:
        cont = [0, 9, 10, 44, 45, 46]
        #Set theta_c, theta_n^(1), theta_n^(0) to initial values
        #TODO: what initial values?
        thetac = [1./K for x in range(K)]
        #Each element tuple of (mean, variance) of normal distribution
        theta = [[random.random() for x in range(len(data[0]))] for y in range(K)]
        #print theta
        loglikelihood = []
        for k in range(K):
            for i in cont:
                theta[k][i] = (.5 + random.uniform(-.1, .1), .25 + random.uniform(-.1, .1))

        #print theta
        #Keep track of iterations until convergence
        round = 0
        #TODO implement convergence parameter
        #Stop your algorithm if , where d is the Euclidean distance, for example. Make sure not to set epsilon too large or you won't actually be converging. Also, state your convergence criteria that you used. Anywhere from 1e-5 to 1e-10 should be a good value for epsilon.
        converging = [1 for x in range(K)]
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
        while sum(converging) > 0:
            # print theta
            # print E
            # print round, converging
            # print thetac
            # print round
            #For each instance x_n
            for x in range(len(data)):
                #probability of feature given class
                P = []
                tempproducts = [[] for x in range(K)]
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
                            if theta[k][d][1] == 0:
                                theta[k][d] = (theta[k][d][0], random.uniform(0, .1))
                            first = 1./math.sqrt(2 * math.pi * theta[k][d][1])
                            second = math.exp((-1) * (data[x][d] - theta[k][d][0]) / (2 * theta[k][d][1]))
                            # print "TWO", k, d, first,second, theta[k][d]
                            if second == 0:
                                # second = float("-inf")
                                second = random.uniform(0, .1)
                                # break
                            # print first*second, theta[k][d], (data[x][d] - theta[k][d][0])/(2*theta[k][d][1])
                            # print "theta"
                            # print theta[k]                        
                            # tempproducts[k] += math.log(first * second)
                            tempproducts[k].append(first*second)
                            # print 'd', tempproducts[k]
                        else:
                            tempproducts[k].append(pow(theta[k][d], data[x][d])*pow((1 - theta[k][d]), (1 - data[x][d])))
                            # print 'not d', tempproducts[k]
                    # print tempproducts[k]
                    # if tempproducts[k] > 500:
                    #     tempproducts[k] = float('inf')
                    # P.append(math.exp(tempproducts[k]))
                    P.append(thetac[k] * logsumexp(tempproducts[k]))
                #for each cluster update
                for k in range(len(P)):
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
                # converging[k] = math.fabs(EN[k]/len(data) - thetac[k])/EN[k]
                if not round == 0:
                    converging[k] = 0 if (math.fabs(EN[k]/len(data) - thetac[k])/EN[k] < EPSILON) else 1
                # converging[k] = math.fabs(EN[k]/len(data) - thetac[k])/EN[k]
                    # print 'converging', math.fabs(EN[k]/len(data) - thetac[k])/EN[k]
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
                            # print k, d, P[k], (topm, topv, bottom)
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
            probn = []
            probk = [0. for k in range(K)]
            probd = []

            for n in range(len(data)):
                for k in range(K):
                    probd = []
                    for d in range(len(data[n])):
                        if d in cont:
                            probk[k] += (theta[k][d][0] * thetac[k])
                        else:
                            probk[k] += (theta[k][d] * thetac[k])
                probn.append(logsumexp(probk[k]))
            loglikelihood.append(sum(probn))
            # print "probn", sum(probn)
            # print "probd", probd
            # print "probk", probk
            # break
            round += 1
            # print P
            #print 'P', P
            #print 'E', E
            #print 'EN', EN
            #print converging
            #print 'round', round
        # return round
        return loglikelihood

            #Theta_c = E[N1]/n
            #For each attribute d
                #Theta_d^1 =
                #Theta_d^0 =
    # t0 = time.time()
    # autoclass(data[:numExamples], numClusters)
    # kmeans(data[:numExamples], numClusters)
    # t1 = time.time()
    # print t1-t0
    print 'K-means means for each cluster of ', numClusters, 'clusters on ', numExamples, 'examples:', (kmeans(data[:numExamples], numClusters))
    # print 'HAC means for each cluster of ', numClusters, 'clusters on ', numExamples, 'examples:', HAC(data[:numExamples], numClusters, "max")
    #print 'Autoclass means for each cluster of ', numClusters, 'clusters on ', numExamples, 'examples:', (autoclass(data[:numExamples], numClusters))

if __name__ == "__main__":
    validateInput()
    main()
