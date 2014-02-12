from MLE_multidim_Hawkes_c.py import *

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
	print "lambda_0 = %f, beta = %f" % (result[0][0], result[0][-1])
	print "%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t"%(result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9])
	print result