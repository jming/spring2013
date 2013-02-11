from dtree import *
# import sys

# Initialize with uniform weights (1/N)
# Run the algorithm
    # Check performance for each
        # (original)

# Compute weighted loss


def weight_loss():

    N = 10
    H[r] = DecisionTree(1)
    W = [[]]
    data = 0
    target = 9

    for n in range(1, N):
        classify_result = classify(H[r], data[n])
        weighted_loss[n] = W[r][n] * (classify_result != data[n].attrs[target])

    return weighted_loss


def hypothesis_weight(E, r):

    return 1 / 2 * log2((1 - E[r]) / E[r])


def set_weight(data):

    pass


def adaboost(dataset):

    N = len(dataset)
    R = 10

    # run series of r rounds
    for round in range(R):

        v = [0. for x in range(N)]

        # update
        for number in range(N):

            # if first round, all should be equal
            if round == 0:

                set_weight(number, 1 / N)

            # else, increase/decrease weight according to performance
            else:
                a = hypothesis_weight()
                v[number] = w[number - 1] * pow(e, a)
