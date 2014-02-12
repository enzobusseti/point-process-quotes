import numpy as np
import random

"""I follow the algo described in the HawkesCourseSlides.pdf
It generates a 1D hawkes process with the specified parameters."""

def lambda_t(t, lambda_0, alpha, beta, points):
	"""Generic function (could be used outside, for e.g. plotting)
	that generates the value of Hawkes' lambda given the parameters
	and the past values of times of events. """

	points = np.array(points)
	points = points[points < t]
	return lambda_0 + alpha * np.sum(np.exp(-beta * (t - points)))

def generate_1D_Hawkes(time_horizon, lambda_0, alpha, beta):
	"""Actual algo for generating a Hawkes Process.
	It uses the "thinning procedure" by Lewis & Shedler.
	I follows the slides."""

	result = []
	lambda_star = lambda_0

	# initialization
	u = random.uniform(0,1)
	s = -np.log(u)/lambda_star
	if s > time_horizon: return result
	else: result.append(s)

	# general loop
	while True:
		lambda_star = lambda_t(result[-1], lambda_0, alpha, beta, result) + alpha
		while True: #steps 2 and 3 
			u = random.uniform(0,1)
			s = s - np.log(u)/lambda_star
			if s > time_horizon: return result
			# point 3
			d = random.uniform(0,1)
			lambda_s = lambda_t(s, lambda_0, alpha, beta, result)
			if d <= (lambda_s / lambda_star):
				result.append(s)
				break
			else:
				lambda_star = lambda_s

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	horizon = 150
	lambda_0 = .4
	alpha = 400
	beta = 600
	data = generate_1D_Hawkes(horizon, lambda_0, alpha, beta)
	#xdata = np.arange(0,horizon,.01)
	plt.plot(data, '.')
	plt.show()