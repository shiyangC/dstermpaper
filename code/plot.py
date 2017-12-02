import matplotlib.pyplot as plt
import numpy as np

d = np.array([i for i in range(50)])
print(d)
maximum = 10 
epsilon = 0.5

R = np.ceil(np.log2(np.sqrt(d) / epsilon * maximum))
print(R)
line1, = plt.plot(d, R, label = 'MH')

U_v = 2
gamma = 0.0001
R8 = 1 + np.ceil(np.log(np.sqrt(d) * U_v / epsilon) / np.log(1 / (1 - gamma)))
line2, = plt.plot(d, R8, label = "VG")
plt.legend(handles=[line1, line2])

from matplotlib2tikz import save as tikz_save
tikz_save('plot_5.tikz')
plt.show()
