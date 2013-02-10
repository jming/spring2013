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
            new_tree = tree
            new_tree.nodetype = 1
            if pos / len(tree.branches) > 1 / 2:
                new_tree.classification = 1
            else:
                new_tree.classification = 0

            # Classify Modified tree
            post = classify_on(new_tree, validation, 9)

            # Collapse subtree in original tree if modification was more efficient
            if (post > prior):
                #print "post > prior"
                tree.branches[i] = new_tree

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

# PART A: Cross validation

    # Sets k-fold cross validation and length of each partition of dataset
    k = 10

    # Measures dataset_length and section_length based on data
    dataset_length = len(examples)
    section_length = dataset_length / k

    # Initialize scores
    score_test = 0
    score_train = 0
    score_validation = [[0 for x in range(1, 80)] for y in range(k)]
    # TEST
    score_validation2 = [0 for x in range(k)]
    
    # Run k experiments
    for i in range(k):

        # Sets bounds for k-1 partitions of data to train on
        low = i * section_length
        high = low + (dataset_length - section_length)

        learn_data = DataSet(dataset.examples[low:high], values=dataset.values)
        learn_result = learn(learn_data)

        # classify on test data
        test_exs = dataset.examples[high:high + section_length]
        score_test += classify_on(learn_result, test_exs, dataset.target) / section_length

        # classify on training data
        training_exs = dataset.examples[low:high]
        score_train += classify_on(learn_result, training_exs, dataset.target) / section_length

# PART B: Post pruning

        # # Loop through possible validation sizes [1, 80]
        for validation_size in range(1, 80):

        #     # Sectioining data into training + validation + test
            mid = high - validation_size

        #     # Build tree on training data
            learn_data_p = DataSet(dataset.examples[low:mid], values=dataset.values)
            learn_result_p = learn(learn_data_p)

        #     # Prune tree on validation data
            pruned_tree = prune(learn_result_p, dataset.examples[mid:high])

        #     # Test tree on test data
            test_data_p = dataset.examples[high:high + section_length]
            score_validation[i][validation_size - 1] = classify_on(pruned_tree, test_data_p, dataset.target)
            
            #TODO why are pruned scores worse than the other ones T.T
            score_validation2[i] += score_validation[i][validation_size - 1]
            
            
        #     # It's getting stuck at i = 0, validation_size = 49
            # Fixed by adding values = dataset.values to line 217 and subtracting 1 from validation_size on line 225
            #print i, validation_size
            
    
    # 2D array with all vlidation scores
    print score_test
    print score_train
    print score_validation2
    

main()
