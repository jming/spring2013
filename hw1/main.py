# main.py
# -------
# Alisa Nguyen and Joy Ming
# CS181 Assignment 1: Decision Trees
# Spring 2013

from dtree import *
import sys
from math import *


# makes graphs
#import matplotlib.pyplot as plt
#from pylab import *


class Globals:
    noisyFlag = False
    pruneFlag = False
    valSetSize = 0
    dataset = None

##Classify
#---------


def classify(decisionTree, example):
    return decisionTree.predict(example)

##Classify Multi Tree
#---------


# Takes in a weighted list of trees and returns majority classification
def classify_multi(decisionTrees, example):

    # tracks how many positive classifications
    pos = 0.

    # loop through and check hypotheses and classifications
    for d in decisionTrees:
        pos += classify(d['hypothesis'], example) * d['weight']

    # return majority classification based on weighing
    if(pos / sum([d['weight'] for d in decisionTrees]) < 1. / 2):
        return 0
    else:
        return 1


##Learn
#-------


def learn(dataset):
    learner = DecisionTreeLearner()
    learner.train(dataset)
    return learner.dt


# Given a tree, make into node with majority label
def majority_chop(tree):
    # print tree

    pos, count = 0., 0

    # Loop through tree branches
    if tree.nodetype == 0:
        for i in tree.branches:
            # Keep track of number of leaves
            if(tree.branches[i].nodetype == 1):
                count += 1
                # Keep track of number of positives
                if(tree.branches[i].nodetype == 1):
                    pos += 1
            else:
                # print "before"
                # print tree.branches[i]
                # Chop the subtrees of the tree
                tree.branches[i] = majority_chop(tree.branches[i])
                # print "after"
                # print tree.branches[i]
            # Condense leaves into majority classification
            if count == len(tree.branches):
                tree.nodetype = 1
                if pos / count < 1. / 2:
                    tree.classification = 0
                else:
                    tree.classification = 1
                count = 0
                pos = 0.

    return tree

    # return chopped tree
    # TODO: Will this properly reduce ALL branches into ONE SINGLE leaf??
    # print "majchop"
    # print tree
    # return tree


# Takes in a tree and chops it to established maximum depth
def chop(tree, k):

    # initialize queue to include root node
    queue = []
    queue.append({'node': tree, 'dist': 0})

    # keep popping things off the queue if it is not empty
    while (len(queue) > 0):
        # print queue
        v = queue.pop(0)
        # look through branches of popped off subtree
        for i in v['node'].branches:
            # If the distance is not k, keep popping children onto queue
            if v['dist'] < k:
                # Pop only subtrees, ignore leaves
                if v['node'].branches[i].nodetype == 0:
                    queue.append({'node': v['node'].branches[i], 'dist': v['dist'] + 1})
            # If the distance is k, reduce this subtree into leaf with majority classification
            elif v['dist'] == k:
                # print "here"
                tree = majority_chop(v['node'])
                # print tree
                # TODO: Where does this go in the tree?!?

    # return chopped tree
    # print "learndepth"
    # print tree
    # print tree
    return tree


# New definition of learn that takes in max depth for tree
def learn_depth(dataset, k_depth):
    # Set max_depth
    # TODO: Is this necessary?
    dataset.max_depth = k_depth
    # Initialize learner
    learner = DecisionTreeLearner()
    # Create learner based on dataset
    learner.train(dataset)
    # Return learner chopped to max depth
    chopped = chop(learner.dt, k_depth)
    # print "chopped"
    # print chopped
    return chopped

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
    noisyFlag = True
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


# Parses data to include only relevant attributes
def parse(data, attr, val):

    result = []

    # Loop through each example and check for corresponding attributes
    for example in data:
        if example.attrs[attr] == val:
            result.append(example)

    return result


def prune(tree, validation):

    # Initialize variables
    count = 0
    pos = 0

    # Traverse each child
    for i in tree.branches:

        # If the child is a leaf
        if (tree.branches[i].nodetype == 1):
            # Track how many leafs each branch has
            count += 1
            # Track if target is positive
            if (tree.branches[i].classification == 1):
                pos += 1
        # If the child is a subtree
        else:
            tree.branches[i] = prune(tree.branches[i], parse(validation, tree.attr, i))

        # If all nodes in this branch are leaves
        if count == len(tree.branches):
            # Classify original tree
            prior = classify_on(tree, validation, 9)
            # Create copy of tree with to subtree collapsed into leaf with majority label
            new_tree = DecisionTree(1)
            if pos / float(len(tree.branches)) > 1. / 2:
                new_tree.classification = 1
            else:
                new_tree.classification = 0

            # Classify modified tree
            post = classify_on(new_tree, validation, 9)

            count = 0
            pos = 0

            # Collapse subtree in original tree if modification was more efficient
            if (post >= prior):
                tree.nodetype = 1
                tree.classification = new_tree.classification

    return tree


# Return classification accuracy for given tree on target in examples
def classify_on(tree, data, target):

    # initialize score
    classify_score = 0.

    # loop through each datapoint to check against tree classification
    for point in range(len(data)):
        classify_result = classify(tree, data[point])
        # increase score by fraction if correct
        if (classify_result == data[point].attrs[target]):
            classify_score += 1. / len(data)

    return classify_score


# Update weights for given examples based on correctness of hypothesis
# TODO: should we be modifying original data or making a copy??
def example_weights(hypothesis, dataset, hyp_weight):
    # Array of non-normalised weights
    v_array = []
    # Loop through and update weights based on correctness and hypthesis weight
    for e in dataset.examples:
        # print "classify"
        # print classify(hypothesis, e)
        # print "attrs"
        # print e.attrs[dataset.target]
        if classify(hypothesis, e) == e.attrs[dataset.target]:
            v_array.append(e.weight * exp(-hyp_weight))
        else:
            v_array.append(e.weight * exp(hyp_weight))
    # Sum all values of non-normalised weights
    v_sum = sum(v_array)
    # Loop through and update weights to be normalised values
    for v in range(len(v_array)):
        dataset.examples[v].weight = v_array[v] / v_sum


# Weigh hypothesis based on error
def hypothesis_weight(hypothesis, dataset):
    # Create an array of error values for each dataset example
    e_array = []
    for e in dataset.examples:
        if classify(hypothesis, e) != e.attrs[dataset.target]:
            e_array.append(e.weight)
    # Sum over all error values
    # print e_array
    error = sum(e_array)
    # print error
    # Return hypothesis weighing
    return (1. / 2) * log((1 - error) / error)


# Wrapper function for adaBoost
def adaBoost(R, dataset):

    # Array of hypotheses
    hypotheses = []
    # initialize example weights to 1
    for d in dataset.examples:
        d.weight = 1. / len(dataset.examples)

    for r in range(R):
        # create a hypothesis
        # hypothesis = learn(dataset)
        hypothesis = learn_depth(dataset, 2)
        # print "hypothesis"
        # print hypothesis
        # create a weight
        weight = hypothesis_weight(hypothesis, dataset)
        # put it in the list
        hypotheses.append({'hypothesis': hypothesis, 'weight': weight})
        # update weights based on correctness
        example_weights(hypothesis, dataset, weight)

    # return list of hypotheses and their weights
    return hypotheses


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

    print adaBoost(5, dataset)

# # PART A: Cross validation

#     # Sets k-fold cross validation and length of each partition of dataset
#     k = 10

#     # Measures dataset_length and section_length based on data
#     dataset_length = len(examples)
#     section_length = dataset_length / k

#     # Initialize scores
#     score_test = 0
#     score_train = 0
#     score_pruned_test = [0 for x in range(81)]
#     score_original_test = [0 for x in range(81)]
#     score_pruned_training = [0 for x in range(81)]
#     score_original_training = [0 for x in range(81)]

#     # Run k experiments
#     for i in range(k):

#         # Sets bounds for k-1 partitions of data to train on
#         low = i * section_length
#         high = low + (dataset_length - section_length)

#         learn_data = DataSet(dataset.examples[low:high], values=dataset.values)
#         learn_result = learn(learn_data)

#         # classify on test data
#         test_exs = dataset.examples[high:high + section_length]
#         score_test += classify_on(learn_result, test_exs, dataset.target) / section_length

#         # classify on training data
#         training_exs = dataset.examples[low:high]
#         score_train += classify_on(learn_result, training_exs, dataset.target) / section_length

# # PART B: Post pruning

#         # Loop through possible validation sizes [1, 80]
#         for validation_size in range(1, 81):

#             # Sectioning data into training + validation + test
#             mid = high - validation_size

#             # Build tree on training data
#             learn_data_p = DataSet(dataset.examples[low:mid], values=dataset.values)
#             learn_result_p = learn(learn_data_p)
#             learn_result_p2 = learn(learn_data_p)

#             # Prune tree on validation data
#             pruned_tree = prune(learn_result_p, dataset.examples[mid:high])

#             # Test tree on test data
#             test_data_p = dataset.examples[high:high + section_length]
#             pruned_accuracy_test = classify_on(pruned_tree, test_data_p, dataset.target)
#             original_accuracy_test = classify_on(learn_result_p2, test_data_p, dataset.target)
#             score_pruned_test[validation_size] += pruned_accuracy_test / k
#             score_original_test[validation_size] += original_accuracy_test / k

#             # Test tree on training data
#             pruned_accuracy_training = classify_on(pruned_tree, learn_data_p.examples, dataset.target)
#             original_accuracy_trainig = classify_on(learn_result_p2, learn_data_p.examples, dataset.target)
#             score_pruned_training[validation_size] += pruned_accuracy_training / k
#             score_original_training[validation_size] += original_accuracy_trainig / k


#     #print 'pruned', mean(score_pruned_test)
#     #print 'original', mean(score_original_test)
#     #print mean(score_pruned_training)

#     '''CODE FOR PLOTTING REMOVE LATER
#     plt.clf()
#     xs = range(1, len(score_pruned_training))
#     training1 = score_pruned_training[1:81]
#     #training2 = score_original_training[1:81]
#     test1 = score_pruned_test[1:81]
#     #test2 = score_original_test[1:81]
#     p1, = plt.plot(xs, training1, color='b')
#     #p2, = plt.plot(xs, training2, color='r')
#     p3, = plt.plot(xs, test1, color='r')
#     #p4, = plt.plot(xs, test2, color='r', ls = 'dotted')
#     plt.title('Cross-Validated Performance vs. Validation Size (Noisy)')
#     plt.xlabel('Validation Set Size')
#     plt.ylabel('Accuracy')
#     plt.axis([0, len(xs), .7, 1])
#     plt.legend(((p1,), (p3,)), ('pruned training','pruned test'), 'lower center')
#     savefig('nguyen-ming-noisy.pdf') # save the figure to a file
#     plt.show() # show the figure'''

#     # print score_validation
#     # print score_original
#     #print score_pruned_test
#     #print score_original_test
#     #print score_pruned_training
#     #print score_original_training

# # PART C adaBoost


main()
