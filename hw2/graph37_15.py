#from main import *

import matplotlib.pyplot as plt
from pylab import *

#data for 15 hidden units 33 epochs
#training error
training = [0.19644444, 0.11688889, 0.10122222, 0.09288889, 0.08744444, 0.08466667, 0.08188889, 0.07944444, 0.07644444, 0.07488889, 0.07411111, 0.07244444, 0.07055556, 0.06933333, 0.06711111, 0.06622222, 0.06455556, 0.06411111, 0.06333333, 0.063, 0.06333333, 0.06311111, 0.063, 0.06344444, 0.06333333, 0.06311111, 0.06311111, 0.06344444, 0.06333333, 0.06266667, 0.06211111, 0.06166667, 0.06122222]
#validation error
validation = [0.218, 0.13, 0.12, 0.114, 0.107, 0.1, 0.1, 0.096, 0.097, 0.094, 0.095, 0.095, 0.095, 0.095, 0.094, 0.094, 0.091, 0.091, 0.091, 0.092, 0.092, 0.091, 0.091, 0.091, 0.093, 0.093, 0.092, 0.091, 0.091, 0.092, 0.093, 0.096, 0.097]

def main():
	plt.clf()
	xs = range(1, 34)
	p1, = plt.plot(xs, training, color='r')
	p2, = plt.plot(xs, validation, color='b')
	plt.title('Training and Validation Error Vs. Number of Epochs (15 Hidden Units)')
	plt.xlabel('Number of Epochs')
	plt.ylabel('Error')
	plt.axis([1, 34, 0, 0.2])
	plt.legend(((p1,),(p2,)), ('training', 'validation'), 'lower right')
	savefig('nguyen-ming-37c_15.pdf') # save the figure to a file
	plt.show() # show the figure

main()