timestamps_and_labels = np.load('timestamps_and_labels.txt')

def loglik(t,alpha,beta):
    K,M,N = alpha.shape
    R = np.zeros((K,M,N))
    Phi = np.ones((K,M,N))
    m = 0
    Phi[:,m,m] = 1
    prev_t = -np.ones(N)

    for row in t:
        tn = row[0]; n = row[1]
        if prev_t[n] > 0:
            if m == n:
                Phi[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t))*Phi[:,m,:]
                R[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t[m])) * R[:,m,:] + Phi[:,m,:]
                Phi[:,m,:] = 0
                Phi[:,m,m] = 1
            elif prev_t[n] > prev_t[m]:
                Phi[:,m,n] = np.exp(-beta[:,m,n]*(tn-prev_t[n])) *(Phi[:,m,n] + 1)
            
        prev_t[n] = tn

    return R
    
alpha = np.array(range(10),ndmin=3)
beta = np.array(range(10),ndmin=3)

# R = loglik(timestamps_and_labels,alpha,beta)

# print R

