import numpy as np
import math
cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t

# This version is waaay slower than the plain one I use below
# it must use the python for loop...
def R_i_1D_internal_numpy(np.ndarray[DTYPE_t, ndim=1] diff_time, double beta):
	assert diff_time.dtype == DTYPE
	cdef np.ndarray[DTYPE_t, ndim=1] result = np.zeros(len(diff_time) + 1)
	assert result.dtype == DTYPE
	#result = [0.] * (len(diff_time) + 1)
	for i in range(1, len(result)):
		result[i] = math.exp(-beta * diff_time[i-1])*(1 + result[i-1]) 
	return result

def R_i_1D_internal(np.ndarray[DTYPE_t, ndim=1] diff_time, double beta):
	result = [0.] * (len(diff_time) + 1)
	for i in range(1, len(result)):
		result[i] = math.exp(-beta * diff_time[i-1])*(1 + result[i-1]) 
	return result

#from libcpp.vector cimport vector
#def R_i_1D_internal(diff_time, double beta):
#	cdef vector[double] result
#	result.push_back(0.)
#	#result = np.zeros(len(diff_time) + 1)
#	#result = [0.] * (len(diff_time) + 1)
#	for i in range(0, len(diff_time)):
#		result.push_back(math.exp(-beta * diff_time[i])*(1 + result[i]))
#	return list(result)