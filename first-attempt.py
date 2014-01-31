import os
import numpy as np


datestr2num = lambda date: float(date[17:]) + int(date[14:16]) * 60 + int(date[11:13]) * 3600

## load all providers
filenames = ["../data/"+i for i in  os.listdir("../data/")]
filenames = [filename for filename in filenames if filename[-3:] == 'csv']
print filenames
providers = [filename.split('-')[-2] for filename in filenames]

vectors_of_timestamps = {}
timestamps_and_labels = np.array([[],[]])
timestamps_and_labels.shape = (0,2)

for index in range(10): ##change to len(filenames)
    print "Loading file: " + filenames[index]
    print "for provider: " + providers[index]
    vectors_of_timestamps[index] = np.loadtxt(filenames[index],delimiter="','",usecols=(2,),skiprows=2, converters={2:datestr2num})
    print "This vector of data occupies %.2f Mb" % (vectors_of_timestamps[index].nbytes/1000000.)
    timestamps_and_labels = np.concatenate((timestamps_and_labels, np.column_stack((vectors_of_timestamps[index],
     index*np.ones(len(vectors_of_timestamps[index]))))),0)
    print "This complete vector of data occupies %.2f Mb" % (timestamps_and_labels.nbytes/1000000.)

