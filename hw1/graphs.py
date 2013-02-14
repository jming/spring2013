from main import *

import matplotlib.pyplot as plt
from pylab import *
	
	plt.clf()
    xs = range(1, len(score_boost))
    boost = score_boost[1:31]
    p1, = plt.plot(xs, boost, color='r')
    plt.title('Boosting Performance vs. Number of Rounds (Non-Noisy)')
    plt.xlabel('Boosting Size')
    plt.ylabel('Accuracy')
    plt.axis([0, len(xs), .8, .94])
#     plt.legend((p1,), ('boosting accuracy'), 'lower center')
    savefig('nguyen-ming-boosting-non-noisy.pdf') # save the figure to a file
    plt.show() # show the figure