# clust.py
# -------
# Alisa Nguyen and Joy Ming

import sys
import random

DATAFILE = "adults.txt"

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
    printOutput(data,numExamples)

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
        r = [[0 for x in range(len(data))] for y in range(K)]
        #r = [[0 for x in range(K)] for x in range(len(data))]
        #Repeat until convergence:
        # TODO: Implement convergence param
        converging = True
        while (!converging):
            #For each n, r_nk =  1 for k = argmin_k'(||x_n - u_k'||^2), and r_nk = 0 otherwise
            for n in range(len(data)):
                for k in range(K):
                    b = argmin(u, lambda l: squareDistance(data[n], l))
                    r[k][n] = 1 if (k == b) else 0
            #For each k, u_k = check notes!
            for k in range(K):
                u[k] = sum([data[n]*r[k][n] for n in range(len(data))])/sum(r[k])

    def HAC(data, k):
        pass
      #E = set of subsets of each individual example
      #Repeat until |E| = K
        #Let A, B be the two closest clusters in E
        #Remove A and B from E
        #Insert A union B into E
    

        
    
if __name__ == "__main__":
    validateInput()
    main()
