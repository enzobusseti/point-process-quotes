def build_R_vector(data, beta, event_type):
    diff_times = np.diff(data[event_type])
    result = np.zeros((len(diff_times), len(data)))
    for i in range(1, len(result)):
        for n in range(len(data)):
            if n == event_type:
                result[i,n] = np.exp(-beta[n] * diff_time[i-1])*(1 + result[i-1,n])
            else:
                result[i,n] = np.exp(-beta[n] * diff_time[i-1])*(1 + result[i-1,n])
    return result



def scalar_loglik(data, event_type, lambda_0, alpha, beta):
    """Data is a list of M np.arrays. Each one of these arrays
    is the time series of events of a particular type. 
    Lambda_0 is a scalar. Alpha and beta
    are M vectors. """

    T = np.max([events[-1] for events in data])
    t_0 = np.min([events[0] for events in data])

    M = len(data)

    assert np.isscalar(lambda_0)
    assert len(beta) = M
    assert len(alpha) = M

    result = T
    result -= lambda_0 * (T - t_0)

    for n in len(data): # iterate over event type
        diff_from_endtime = T - data[n]
        result -= np.sum((1 - np.exp(-beta[n] * diff_from_endtime)) * alpha[n] / beta[n])

    # now we need R


    for row in t:
        tn = row[0]; n = row[1]
        # Computing R
        if prev_t[n] > 0:
            if m == n:
                Phi[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t))*Phi[:,m,:]
                R[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t[m])) * R[:,m,:] + Phi[:,m,:]
                Phi[:,m,:] = 0; Phi[:,m,m] = 1
                
                # Computing ell
                ell += np.log(lambda_0 + np.sum(alpha*R,axis=(0,2)))
            elif prev_t[n] > prev_t[m]:
                Phi[:,m,n] = np.exp(-beta[:,m,n]*(tn-prev_t[n])) *(Phi[:,m,n] + 1)
        prev_t[n] = tn
        
        # Computing A
        A += np.exp(-beta*(T-tn))

    return R,alpha/beta*(1-A),ell-np.sum(alpha/beta*(1-A),axis=(0,2))
