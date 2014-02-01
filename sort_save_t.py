from operator import itemgetter

execfile("first-attempt.py")


print '\n\n\n'
print timestamps_and_labels.shape[0]
n = timestamps_and_labels.shape[0]
ep = 1e-5
timestamps_and_labels[:,0] += np.random.uniform( low=-ep, high=ep, size=n) - 8*3600

timestamps_and_labels = np.array(sorted(timestamps_and_labels, key=itemgetter(0), reverse=False))

print type(timestamps_and_labels)
print timestamps_and_labels[:10,]

with open('timestamps_and_labels.txt','w') as f:
    np.save(f,timestamps_and_labels)

