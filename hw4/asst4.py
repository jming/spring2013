import random
import math

# code for problem 3
# d1 = {'prob':0.2, 'mu': 1, 'sigma': 25}
# d2 = {'prob':0.3, 'mu'}
# MOG = 


def normpdf(x, mu, sigmasq):
    return math.exp(pow((x-mu), 2)/(2*sigmasq))/math.sqrt(2*math.pi*sigmasq)


def p(x):
    return 0.2*normpdf(x, 1, 25)+0.3*normpdf(x, -2, 1)+0.5*normpdf(x, 3, 4)


def q(x):
    return normpdf(x, 0, 1)


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
def rejection(N, M):
    x = []
    i = 0
    while i != N:
        xi = random.gauss(0, 1)
        u = random.uniform(0, 1)
        if u < p(xi) / (M * q(xi)):
            x.append(xi)
            i += 1

# part d

def metrohast():
    pass

b = [direct() for x in range(500)]
print b
