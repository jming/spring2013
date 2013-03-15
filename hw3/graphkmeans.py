# import matplotlib.pyplot as plt
# from pylab import *

msqe = [1.655322531, 1.40723349954, 1.35330392268, 1.25885399889, 1.1515697001, 1.08294591318, 1.05032445647, 1.04234005957, 1.02474669853]
y = [range(2,10)]
# plt.clf()
# xs = range(2,11)

# p1, = plt.plot(xs, msqe, color='b')
# # plt.title('Mean squared error vs. number of clusters')
# # plt.xlabel('Number of Clusters')
# # plt.ylabel('Mean Squared Error')
# plt.axis([2,11,0,1])
# # savefig('graph.pdf')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
xs = range(2,11)
p1, = plt.plot(xs, msqe)
# plt.plot(msqe)
plt.title('Mean squared error vs. number of clusters')
plt.xlabel('Number of clusters')
plt.ylabel('Mean squared error')
plt.show()