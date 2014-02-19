from MLE_multidim_Hawkes_c import *

if __name__ == "__main__":
	event_type = 0
	data = []
	timestamps_and_labels = np.load('timestamps_and_labels.txt')
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 0, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 2, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 3, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 4, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 5, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 6, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 7, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 8, 0])
	data.append(timestamps_and_labels[timestamps_and_labels[:,1] == 9, 0])
	result = MLE_estimate(data, 3, lambda_lasso = 1000)
	print result
#	print "lambda_0 = %f, beta = %f" % (result[0][0], result[0][-1])
#	print "alpha = " + '\t'.join('%.4f' % k for k in result[0][1:-1]) 
