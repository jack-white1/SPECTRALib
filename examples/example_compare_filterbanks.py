from spectralib.filterbank import *

filename1 = "RFIoutput_with_binary_pulsar.fil"
filename2 = "sigproc_binary.fil"

data1, header1 = read_filterbank(filename1)
data2,header2 = read_filterbank(filename2)


#plot data, dataafter in same window in adjacent subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.imshow(data1,aspect='auto')
ax1.set_title('spectralib')
ax2.imshow(data2[:,1:10000],aspect='auto')
ax2.set_title('sigproc')
plt.show()