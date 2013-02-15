#from main import *

import matplotlib.pyplot as plt
from pylab import *
	
noiseless = [0.0, 0.8799999999999998, 0.8799999999999998, 0.8999999999999998, 0.9199999999999998, 0.8899999999999999, 0.8899999999999999, 0.8899999999999999, 0.8899999999999999, 0.8899999999999999, 0.8899999999999999, 0.8899999999999999, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998, 0.9099999999999998]

noisy = [0.0, 0.8199999999999997, 0.8199999999999997, 0.8099999999999997, 0.8299999999999997, 0.7999999999999997, 0.8199999999999997, 0.8199999999999997, 0.8199999999999997, 0.8299999999999997, 0.8199999999999997, 0.8299999999999997, 0.8499999999999998, 0.8299999999999997, 0.8499999999999998, 0.8499999999999998, 0.8499999999999998, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8199999999999997, 0.8399999999999997, 0.8499999999999998, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997, 0.8399999999999997]

def main():
	plt.clf()
	xs = range(1, len(noisy))
	boost_noisy = noisy[1:31]
	boost_nonnoisy = noiseless[1:31]
	p1, = plt.plot(xs, boost_noisy, color='r')
	p2, = plt.plot(xs, boost_nonnoisy, color='b')
	plt.title('Boosting Performance vs. Number of Rounds')
	plt.xlabel('Boosting Size')
	plt.ylabel('Accuracy')
	plt.axis([0, len(xs), .8, .94])
	plt.legend(((p1,),(p2,)), ('noisy', 'noiseless'), 'lower right')
	savefig('nguyen-ming-boosting.pdf') # save the figure to a file
	plt.show() # show the figure

#print len(noisy)
#print len(noiseless)	
main()