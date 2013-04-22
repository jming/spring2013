# Joy Ming and Alisa Nguyen
# April 12, 2013
# CS 181: HW4

import random
import math
import matplotlib.pyplot as plt

# HELPER FUNCTIONS


# returns normal pdf based on given mean and variance
# def normpdf(x, mu, sigmasq):
#     numerator = math.exp(pow((x-mu), 2)/(2*sigmasq))
#     denominator = math.sqrt(2*math.pi*sigmasq)
#     return numerator/denominator

def normpdf(x, mu, sigma):
    u = (x-mu)/abs(sigma)
    y = (1/(math.sqrt(2*math.pi)*abs(sigma)))*math.exp(-u*u/2)
    return y


# returns application of given mixture of gaussians
def p(x):
    # d1 = 0.2*normpdf(x, 1, 25)
    # d2 = 0.3*normpdf(x, -2, 1)
    # d3 = 0.5*normpdf(x, 3, 4)
    d1 = 0.2*normpdf(x, 1, 5)
    d2 = 0.3*normpdf(x, -2, 1)
    d3 = 0.5*normpdf(x, 3, 4)
    return d1 + d2 + d3


# returns application of guessed bound
def q(x):
    return normpdf(x, 0, 5)

# CODE FOR PROBLEM 3

#  part b
def direct():
    u = random.uniform(0, 1)
    if u < 0.2:
        return random.gauss(1, 5)
    elif u >= 0.2 and u < 0.5:
        return random.gauss(-2, 1)
    else:
        return random.gauss(3, 2)


# part c
def rejection(N):
    x = []
    i = 0
    reject = 0
    while i != N:
        # xi = random.gauss(0, 5)
        # u = random.uniform(0, 1)
        # if u < p(xi) / (2 * q(xi)):
        #     x.append(xi)
        #     i += 1
        # else:
        #     reject += 1
        xi = random.gauss(0, 5)
        u = random.uniform(0, 2 * q(xi))
        if u < p(xi):
            x.append(xi)
            i += 1
        else:
            reject += 1
    return reject

# part d
def metrohast(N):
    reject = 0
    var = 6
    x = [0]
    for i in range(N):
        u = random.uniform(0, 1)
        xi = random.gauss(x[i], var)
        # print xi, x[i]
        acceptp = p(xi)/p(x[i])
        acceptq = normpdf(x[i], xi, var)/normpdf(xi, x[i], var)
        if u < min(1, acceptp*acceptq):
            x.append(xi)
        else:
            x.append(x[i])
            reject += 1
    return reject, x

# MAIN

b = [direct() for x in range(500)]
#print b

c = rejection(500)
#print c

d = metrohast(500)
print d

# PLOTTING DATA

def plot(data):
    count, bins, ignored = plt.hist(data, 60, normed=True)
    plt.show()


plot(d[1])
