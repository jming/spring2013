# main.py
# -------
# Alisa Nguyen and Joy Ming
# CS181 Assignment 1: Decision Trees
# Spring 2013

from dtree import *
import sys

class Globals:
    noisyFlag = True
    pruneFlag = False
    valSetSize = 0
    dataset = None

##Classify
#---------

def classify(decisionTree, example):
    return decisionTree.predict(example)

##Learn
#-------
def learn(dataset):
    learner = DecisionTreeLearner()
    learner.train( dataset)
    return learner.dt

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'main.py', '-n', '-p', 5 ]) = { '-n':True, '-p':5 }"""
  args_map = {}
  curkey = None
  for i in xrange(1, len(args)):
    if args[i][0] == '-':
      args_map[args[i]] = True
      curkey = args[i]
    else:
      assert curkey
      args_map[curkey] = args[i]
      curkey = None
  return args_map

def validateInput(args):
    args_map = parseArgs(args)
    valSetSize = 0
    noisyFlag = False
    pruneFlag = False
    boostRounds = -1
    maxDepth = -1
    if '-n' in args_map:
      noisyFlag = True
    if '-p' in args_map:
      pruneFlag = True
      valSetSize = int(args_map['-p'])
    if '-d' in args_map:
      maxDepth = int(args_map['-d'])
    if '-b' in args_map:
      boostRounds = int(args_map['-b'])
    return [noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds]

def prune(tree, treecopy, data_t, data_v):
    # traverse to the bottom of the tree
    for i in tree.branches:
        count = 0
        pos = 0
        #for k in tree.branches[i]:
        if tree.branches[i].nodetype == 1:
            count += 1
            if tree.branches[i].classification == 1:
                pos += 1
        else:
            prune(tree.branches[i], treecopy, data_t, data_v)
        if count == len(tree.branches):
            tree.nodetype = 1
            if pos/len(tree.branches) > 1/2:
                tree.classification = 1
            else:
                tree.classification = 0
            #classify(tree, DATASET) )
                
    # from the leaves upward
        # s = validation set performance of subtree rooted at that node
        # t = validation set performance of leaf that returns most common class
        # is s <= t prune the subtree    
    
def main():
    arguments = validateInput(sys.argv)
    noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds = arguments
    print noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds

    # Read in the data file
    
    if noisyFlag:
        f = open("noisy.csv")
    else:
        f = open("data.csv")

    data = parse_csv(f.read(), " ")
    dataset = DataSet(data)
    
    # Copy the dataset so we have two copies of it
    examples = dataset.examples[:]
 
    dataset.examples.extend(examples)
    dataset.max_depth = maxDepth
    if boostRounds != -1:
      dataset.use_boosting = True
      dataset.num_rounds = boostRounds

    # Ten-Fold Cross Validation
    # Sets k-fold cross validation and length of each partition of dataset
    k = 10
    dataset_length = len(examples)
    section_length = dataset_length / k
    # Array of arrays with classification results for test set for each classification for each experiment
    classify_result_test = [[0 for j in range(section_length)] for i in range(k)]
    # Array of classification results for test set for each experiment
    classify_score_test = [0. for l in range(k)]
    # Average accuracy
    total_score_test = 0.
    classify_result_training = [[0 for j in range(dataset_length - section_length)] for i in range(k)]
    classify_result_training_r = [[0 for j in range(dataset_length - section_length)] for i in range(k)]
    classify_score_training = [0. for l in range(k)]
    total_score_training = 0.
    counter = 0
    
    # PART A 

    # Run k experiments
    for i in range(k):

        # Sets bounds for k-1 partitions of data to train on
        low = i * section_length
        high = low + (dataset_length - section_length)

        learn_result = learn(DataSet(dataset.examples[low:high], values=dataset.values))

        # classify on test data
        for j in range(section_length):
            classify_result_test[i][j] = classify(learn_result, dataset.examples[high + j])
            if (classify_result_test[i][j] == dataset.examples[high + j].attrs[dataset.target]):
                classify_score_test[i] += 1. / section_length

        # TO DO CLEAN UP LATER        
        # classify on training data
        for l in range(dataset_length - section_length):
            classify_result_training[i][l] = classify(learn_result, dataset.examples[low + l])
            classify_result_training_r[i][l] = dataset.examples[low + l].attrs[dataset.target]
            if (classify_result_training[i][l] == dataset.examples[low + l].attrs[dataset.target]):
                classify_score_training[i] += 1. / (dataset_length - section_length)

        total_score_test += classify_score_test[i]
        total_score_training += classify_score_training[i]
        
    prune(learn_result, learn_result, dataset.examples[low:high], dataset.examples[high:high+section_length])

    # print classify_result_test
    # print classify_score_test
    # print classify_result_training
    # print classify_result_training_r
    # print classify_score_training
    # print total_score_test / k
    # print total_score_training / k

    # PART B

    # Use learn function to create a tree on data
    # Give pruning function a tree + data
    # Prune the tree

main()

# def prune(tree, data):
    # traverse to the bottom of the tree
    # from the leaves upward
        # s = validation set performance of subtree rooted at that node
        # t = validation set performance of leaf that returns most common class
        # is s <= t prune the subtree
