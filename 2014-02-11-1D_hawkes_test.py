#1D Hawkes process estimation
from MLE_1D_Hawkes import *

if __name__ == "__main__":
	for PROVIDER in range(9,10):
		timestamps_and_labels = np.load('timestamps_and_labels.txt')
		data = timestamps_and_labels[timestamps_and_labels[:,1] == PROVIDER, 0]
		print "Provider number %d. There are %d quotes, i.e. an average of %.2f per minute." % (PROVIDER, len(data), 60*len(data)/(data[-1] - data[0]))  
		result = MLE_estimate(data)
		print "Optimal result is lambda_0 = %f, ampha = %f and beta = %f" %(result[0][0], result[0][1], result[0][2])