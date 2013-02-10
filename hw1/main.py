# main.py
# -------
# Alisa Nguyen and Joy Ming
# CS181 Assignment 1: Decision Trees
# Spring 2013

from dtree import *
import sys


class Globals:
    noisyFlag = False
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
    learner.train(dataset)
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
    count = 0
    pos = 0

    for i in tree.branches:
        if (tree.branches[i].nodetype == 1):
            count += 1
            # print 'count', count
            # print 'c', tree.branches[i].classification
            if (tree.branches[i].classification == 1):
                pos += 1
                # print 'pos', pos
        else:
            # print 'i', i, 'recursive prune'
            prune(tree.branches[i], treecopy, data_t, data_v)
        # print len(tree.branches), count
        if count == len(tree.branches):
            print classify_on(tree, data_t, 9)
            # count = setproblem(data_t, i)
            # tree.nodetype = 1
            # if pos / len(tree.branches) > 1 / 2:
            #     tree.classification = 1
            # else:
            #     tree.classification = 0
            # print classify(tree, data_t)

    # from the leaves upward
        # s = validation set performance of subtree rooted at that node
        # t = validation set performance of leaf that returns most common class
        # is s <= t prune the subtree


def classify_on(tree, data, target):

    classify_score = 0.
    for i in range(len(data)):
        classify_result = classify(tree, data[i])
        if (classify_result == data[i].attrs[target]):
            classify_score += 1. / len(data)

    return classify_score


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

    # PART A

    # Run k experiments
    for i in range(k):

        # Sets bounds for k-1 partitions of data to train on
        low = i * section_length
        high = low + (dataset_length - section_length)

        learn_result = learn(DataSet(dataset.examples[low:high], values=dataset.values))

        # classify on test data
        score_test = classify_on(learn_result, dataset.examples[high:high + section_length], dataset.target)

        # classify on training data
        score_training = classify_on(learn_result, dataset.examples[low:high], dataset.target)

    prune(learn_result, learn_result, dataset.examples[low:high], dataset.examples[high:high+section_length])

    # print score_test * 100.
    # print score_training * 100.
    # print total_score_test / k
    # print total_score_training / k

    # PART B

    # Use learn function to create a tree on data
    # Give pruning function a tree + data
    # Prune the tree

main()
