#from main import *

import matplotlib.pyplot as plt
from pylab import *

#data for 30 hidden units 28 epochs
#training error
training = [0.16, 0.10666667, 0.09288889, 0.08244444, 0.07566667, 0.069, 0.065, 0.061, 0.05833333, 0.05533333, 0.05433333, 0.05255556, 0.05077778, 0.049, 0.04833333, 0.04711111, 0.04611111, 0.04533333, 0.04411111, 0.043, 0.04255556, 0.04133333, 0.04, 0.03966667, 0.03877778, 0.03766667, 0.03677778, 0.03633333]
#validation error
validation = [0.175, 0.124, 0.108, 0.098, 0.095, 0.086, 0.083, 0.081, 0.078, 0.075, 0.076, 0.074, 0.072, 0.072, 0.072, 0.072, 0.071, 0.07, 0.071, 0.071, 0.072, 0.071, 0.069, 0.07, 0.07, 0.073, 0.073, 0.074]

def main():
	plt.clf()
	xs = range(1, 29)
	p1, = plt.plot(xs, training, color='r')
	p2, = plt.plot(xs, validation, color='b')
	plt.title('Training and Validation Error Vs. Number of Epochs (30 Hidden Units)')
	plt.xlabel('Number of Epochs')
	plt.ylabel('Error')
	plt.axis([1, 29, 0, 0.2])
	plt.legend(((p1,),(p2,)), ('training', 'validation'), 'lower right')
	savefig('nguyen-ming-37c_30.pdf') # save the figure to a file
	plt.show() # show the figure

main()