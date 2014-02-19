#!/usr/bin/env python
  
import ctypes
import numpy as np
import scipy.optimize


def scalar_loglik(data, event_type, *args):
	"""Wrapper around the C function in scalar_log_likelihood.c
	We get data, a list of np.arrays of times of events (each element is an 
	array for a particular event). The event type is the index of
	the event we estimate the log likelihood for. 
	*args are parameter on which we optimize."""

	M = len(data)
	#print "Computing loglik of %d types of events" %M
	lambda_0 = args[0]
	alpha = args[1:M+1]
	#beta = args[M+1:]
	beta = [args[-1]]*len(alpha)

	print "Lambda_0 = %f, alpha = %s, beta = %s" %(lambda_0, alpha, beta)

	LIBRARY_PATH = './scalar_log_likelihood.so'
	scalar_log_likelihood = ctypes.CDLL(LIBRARY_PATH)

	# ctypes requires to declare the types of variable the function accepts
	scalar_log_likelihood._scalar_loglik.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),
	 ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

	# and return value
	scalar_log_likelihood._scalar_loglik.restype = ctypes.c_double

	# I need to convert all Python variables in C types
	event_type = ctypes.c_int(event_type)
	lambda_0 = ctypes.c_double(lambda_0)
	number_event_types = ctypes.c_int(len(data))

	# I just copy everything. These are C arrays
	length_time_series = (ctypes.c_int * len(data))()# don't forget the () at the end
	c_data = (ctypes.POINTER(ctypes.c_double) * len(data))()
	c_alpha = (ctypes.c_double * len(data))()
	c_beta = (ctypes.c_double * len(data))()

	for i in range(len(data)):
		length_time_series[i] = len(data[i])
		c_alpha[i] = alpha[i]
		c_beta[i] = beta[i]
		# neat feature of numpy: it can expose a pointer to the raw memory of the arrays (which are C arrays)  
		c_data[i] = data[i].ctypes.data_as(ctypes.POINTER(ctypes.c_double))

	print "Running C loglik"
	result =  scalar_log_likelihood._scalar_loglik(number_event_types, c_data, length_time_series, 
		event_type, lambda_0, c_alpha, c_beta)
	print "Obtained result %f" % result

	return result

def MLE_estimate(data, event_type, lambda_lasso):
	"""Optimization routine. I implement a lasso regularization
	and use the most advanced optimizer in scipy. It allows me to specify
	bounds."""
	optimizer_func = lambda x: -scalar_loglik(data, event_type, *x) + lambda_lasso * np.sum(np.abs(x[:-1]))#np.sum(np.abs(x[:(len(x)-1)/2 + 1])) #negative because we maximize
	#INITIAL_VALUES = [1] + [1] * len(data) * 2
#	INITIAL_VALUES = [1] * (len(data) + 2)
#	result = scipy.optimize.fmin_l_bfgs_b(optimizer_func, INITIAL_VALUES, bounds = [(0, None)]* (len(INITIAL_VALUES)-1) + [(1, None)], approx_grad = True, disp = True)
	INITIAL_VALUES = [1.03268077,   5.79553433,   0.        ,   0.97914971,
        23.84772554,  14.64064035,   1.19917264,   0.        ,
         6.68104094,   0.19220533,  40.06850691]
         
         
	optimizer = 'L-BFGS-B' # 'TNC' # 
	result = scipy.optimize.minimize(optimizer_func,  INITIAL_VALUES, method=optimizer, bounds = [(0, None)]* (len(INITIAL_VALUES)-1) + [(1, None)], \
	    options={'disp': True, 'approx_grad':True})
	return result

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
	result = MLE_estimate(data, 8, lambda_lasso = 1000)
	print "lambda_0 = %f, beta = %f" % (result[0][0], result[0][-1])
	print "%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t"%(result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9])
	print result


