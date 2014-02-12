#1D Hawkes process estimation
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import cython_functions

DEBUG = True
INITIAL_VALUES = [1,1,1]

# Recursive definition of R
def R_i(data,beta):
	diff_time = np.diff(data)
	return np.array(cython_functions.R_i_1D_internal(diff_time, beta))

# this is the non-cython version
#def R_i_1D_internal(diff_time, beta):
#	result = np.zeros(len(diff_time)) + 1
#	for i in range(1, len(result)):
#		result[i] = np.exp(-beta * diff_time[i-1])*(1 + result[i-1]) 
#	return result
	
# this is faster (not faster than the Cython version) but has numerical stability problems
R = lambda data, beta: np.concatenate(([0], np.exp(-beta * data)[1:] * np.cumsum(np.exp(beta * data))[:-1]))

def loglik(data, lambda_0, alpha, beta):
	if DEBUG: print "Computing loglik with lambda_0 = %f, ampha = %f and beta = %f" %(lambda_0, alpha, beta)
	result = data[-1]
	result -= lambda_0 * (data[-1] - data[0])
	diff_from_endtime = data[-1] - data
	result -= np.sum((1 - np.exp(-beta * diff_from_endtime)) * alpha/beta)
	R_i_vec = np.array(R_i(data, beta))
	result += np.sum(np.log(lambda_0 + alpha * R_i_vec ))
	if DEBUG: print "Loglik = %f" % result
	return result

def MLE_estimate(data):
	optimizer_func = lambda x: -loglik(data, *x) #negative because we maximize
	result = scipy.optimize.fmin(optimizer_func, INITIAL_VALUES, full_output=True, disp = True)
	return result

# plot intensity
#lambda_0, alpha, beta = np.array([ 0.25973032,  1.78225494,  2.67907145])
#intensity = np.zeros(len(data))
#intensity += lambda_0
#for i in range(len(intensity)):
#	intensity[i] += alpha * np.sum(np.exp(-beta * (data[i] - data[0:i])))
#
#plt.plot(data, intensity)
#plt.plot(data, [0] * len(data), '*')
#plt.show()

if __name__ == "__main__":
	timestamps_and_labels = np.load('timestamps_and_labels.txt')
	PROVIDER = 5
	data = timestamps_and_labels[timestamps_and_labels[:,1] == PROVIDER, 0]
	print "Provider number %d. There are %d quotes, i.e. an average of %.2f per minute." % (PROVIDER, len(data), 60*len(data)/(data[-1] - data[0]))  
	result = MLE_estimate(data)
	print "Optimal result is lambda_0 = %f, ampha = %f and beta = %f" %(result[0][0], result[0][1], result[0][2])