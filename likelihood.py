import numpy as np
import time

timestamps_and_labels = np.load('timestamps_and_labels.txt')

def loglik(t,T,lam0,alpha,beta):
    K,M,N = alpha.shape
    R = np.zeros((K,M,N))
    Phi = np.ones((K,M,N))
    m = 0
    Phi[:,m,m] = 1
    prev_t = -np.ones(N)

    A = np.zeros((K,M,N))

    ell = T
    for row in t:
        tn = row[0]; n = row[1]
        # Computing R
        if prev_t[n] > 0:
            if m == n:
                Phi[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t))*Phi[:,m,:]
                R[:,m,:] = np.exp(-beta[:,m,:]*(tn-prev_t[m])) * R[:,m,:] + Phi[:,m,:]
                Phi[:,m,:] = 0; Phi[:,m,m] = 1
                
                # Computing ell
                ell += np.log(lam0 + np.sum(alpha*R,axis=(0,2)))
            elif prev_t[n] > prev_t[m]:
                Phi[:,m,n] = np.exp(-beta[:,m,n]*(tn-prev_t[n])) *(Phi[:,m,n] + 1)
        prev_t[n] = tn
        
        # Computing A
        A += np.exp(-beta*(T-tn))

    return R,alpha/beta*(1-A),ell-np.sum(alpha/beta*(1-A),axis=(0,2))
    
alpha = np.array(range(1,11),ndmin=3)
beta = np.array(range(1,11),ndmin=3)

T = 14*3600
start = time.time()
R,A,ell = loglik(timestamps_and_labels,T,.1,alpha,beta)
print "Elapsed time: " + str(time.time()-start)
print "R: ",R
print "A: ",A
print "loglik: ",ell
