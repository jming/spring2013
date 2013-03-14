# clust.py
# -------
# Alisa Nguyen and Joy Ming

import sys
import random
import copy
from utils import *

#DATAFILE = "adults.txt"
DATAFILE = "adults-small.txt"

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
            #print 'round', round
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
        #return means
        return sum(means)/len(means)
        # return r
            
    metrics = ["min", "max", "mean", "cent"]
    def HAC(data, K):

        #E = set of subsets of each individual example
        E = []
        for n in data:
            E.append([n])
        print 'E', E
        #counter for printing
        counter = 0
        #Repeat until |E| = K
        while len(E) != K:
            dist = []
            for a in E:
                E.remove(a)
                print 'a', a
                for b in E:
                    xmin = cmin(a, b, squareDistance)
                    xmax = cmax(a, b, squareDistance)
                    xmean = cmean(a, b, squareDistance)
                    xcent = ccent(a, b, squareDistance)
                    dist.append({"a": a, "b": b, "min": xmin, "max": xmax, "mean": xmean, "cent": xcent})
                E.append(a)
            temp = []
            for c in range(len(dist)):
                temp.append(dist[c]["min"])
            mini = min(temp)
            index = temp.index(mini)
            a = dist[index]["a"]
            b = dist[index]["b"]
            newc = [a, b]
            E.remove(a)
            E.remove(b)
            E.append(newc)
            print 'E', E
            print 'counter', counter
            counter+=1
            
        return E
            #Let A, B be the two closest clusters in E
            #Remove A and B from E
            #Insert A union B into E

    
    print(kmeans(data[:numExamples], numClusters))
    print(HAC(data[:numExamples], numClusters))
    

        
    
if __name__ == "__main__":
    validateInput()
    main()
