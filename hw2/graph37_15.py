#from main import *

import matplotlib.pyplot as plt
from pylab import *

#data for 15 hidden units 33 epochs
#training error 15
training1 = [0.19644444, 0.11688889, 0.10122222, 0.09288889, 0.08744444, 0.08466667, 0.08188889, 0.07944444, 0.07644444, 0.07488889, 0.07411111, 0.07244444, 0.07055556, 0.06933333, 0.06711111, 0.06622222, 0.06455556, 0.06411111, 0.06333333, 0.063, 0.06333333, 0.06311111, 0.063, 0.06344444, 0.06333333, 0.06311111, 0.06311111, 0.06344444, 0.06333333, 0.06266667, 0.06211111, 0.06166667, 0.06122222]
#validation error 15
validation1 = [0.218, 0.13, 0.12, 0.114, 0.107, 0.1, 0.1, 0.096, 0.097, 0.094, 0.095, 0.095, 0.095, 0.095, 0.094, 0.094, 0.091, 0.091, 0.091, 0.092, 0.092, 0.091, 0.091, 0.091, 0.093, 0.093, 0.092, 0.091, 0.091, 0.092, 0.093, 0.096, 0.097]
#training error 30
training2 = [0.16, 0.10666667, 0.09288889, 0.08244444, 0.07566667, 0.069, 0.065, 0.061, 0.05833333, 0.05533333, 0.05433333, 0.05255556, 0.05077778, 0.049, 0.04833333, 0.04711111, 0.04611111, 0.04533333, 0.04411111, 0.043, 0.04255556, 0.04133333, 0.04, 0.03966667, 0.03877778, 0.03766667, 0.03677778, 0.03633333]
#validation error 30
validation2 = [0.175, 0.124, 0.108, 0.098, 0.095, 0.086, 0.083, 0.081, 0.078, 0.075, 0.076, 0.074, 0.072, 0.072, 0.072, 0.072, 0.071, 0.07, 0.071, 0.071, 0.072, 0.071, 0.069, 0.07, 0.07, 0.073, 0.073, 0.074]

def main():
	plt.clf()
	xs = range(1, 34)
  	ys = range(1, 29)
	p1, = plt.plot(xs, training1, color='r', ls ='dotted')
	p2, = plt.plot(xs, validation1, color='r')
	p3, = plt.plot(ys, training2, color ='b', ls = 'dotted')
	p4, = plt.plot(ys, validation2, color='b')
	plt.title('Training and Validation Error Vs. Number of Epochs')
	plt.xlabel('Number of Epochs')
	plt.ylabel('Error')
	plt.axis([1, 34, 0, 0.2])
	plt.legend(((p1,),(p2,),(p3,),(p4,)), ('training (15 units)', 'validation (15 units)', 'training (30 units)', 'validation (30 units)'), 'upper right')
	savefig('nguyen-ming-37c.pdf') # save the figure to a file
	plt.show() # show the figure

main()