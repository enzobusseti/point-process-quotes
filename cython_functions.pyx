#import numpy as np
import math

def R_i_1D_internal(diff_time, beta):
	#result = np.zeros(len(diff_time) + 1)
	result = [0.] * (len(diff_time) + 1)
	for i in range(1, len(result)):
		result[i] = math.exp(-beta * diff_time[i-1])*(1 + result[i-1]) 
	return result