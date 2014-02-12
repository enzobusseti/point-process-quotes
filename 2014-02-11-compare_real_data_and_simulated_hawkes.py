import matplotlib.pyplot as plt
import numpy as np
from generate_1D_Hawkes import *

PROVIDER = 6

horizon = 150

lambda_0 = 0.167242
alpha = 1.189406
beta = 1.909375

data = generate_1D_Hawkes(horizon, lambda_0, alpha, beta)
plt.plot(data, '.')
plt.title("Generated, %d seconds" %horizon)
	

timestamps_and_labels = np.load('timestamps_and_labels.txt')
real_data = timestamps_and_labels[timestamps_and_labels[:,1] == PROVIDER, 0]

plt.figure()
plt.plot(real_data, '.')
plt.title("Real data, complete")


real_data = real_data[real_data< horizon]
plt.figure()
plt.plot(real_data, '.')
plt.title("Real data, first %d seconds" % horizon)

plt.show()