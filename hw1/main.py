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


def parse(data, attr, val):
    result = []
    for example in data:
        if example.attrs[attr] == val:
            result.append(example)
        # if example.attrs[attr] == 1:
            # result.append(example)
    return result


def prune(tree, training, test):
    # traverse to the bottom of the tree
    count = 0
    pos = 0

    for i in tree.branches:

        if (tree.branches[i].nodetype == 1):

            count += 1

            if (tree.branches[i].classification == 1):
                pos += 1

            if count == len(tree.branches):
                prior = classify_on(tree, training, 9)
                new_tree = tree
                new_tree.nodetype = 1
                if pos / len(tree.branches) > 1 / 2:
                    new_tree.classification = 1
                else:
                    new_tree.classification = 0
                post = classify_on(new_tree, training, 9)
                # if (post  prior):
                print "prior = " + str(prior) + " post = " + str(post) + " i =" + str(i)
                    # FUCK WHY IS THERE A ZERO?
        else:
            prune(tree.branches[i], parse(training, i, tree.branches[i].attr), parse(test, i, tree.branches[i].attr))
            # print prior
            # print post

            # count = setproblem(data_t, i)
            # tree.nodetype = 1
            # if pos / len(tree.branches) > 1 / 2:
            #     tree.classification = 1
            # else:
            #     tree.classification = 0
            # print classify(tree, data_t)


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
    # print noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds

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
    score_test = 0
    score_training = 0
    
    # PART A

    # Run k experiments
    for i in range(k):

        # Sets bounds for k-1 partitions of data to train on
        low = i * section_length
        high = low + (dataset_length - section_length)

        learn_result = learn(DataSet(dataset.examples[low:high], values=dataset.values))
        print learn_result
        # break

        # classify on test data
        score_test += classify_on(learn_result, dataset.examples[high:high + section_length], dataset.target)

        # classify on training data
        score_training += classify_on(learn_result, dataset.examples[low:high], dataset.target)

    prune(learn_result, dataset.examples[low:high], dataset.examples[high:high+section_length])

    # print score_test
    # print score_training
    # print score_test/k
    # print score_training/k

    # PART B

    # Use learn function to create a tree on data
    # Give pruning function a tree + data
    # Prune the tree

main()
