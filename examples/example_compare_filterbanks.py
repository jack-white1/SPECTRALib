from spectralib.filterbank import *
from spectralib.frb import *

tobs = 10
tsamp = 0.001
nchans = 500
noisesigma = 18
nsamp = round(tobs/tsamp)
metadata = {
    "source_name": "spectralib_FRB",
    "machine_id": 0,
    "telescope_id": 0,
    "data_type": 0,
    "fch1": 1500.0,
    "foff": -1.0,   # must be a float
    "nchans": 500,
    "nbits": 8,
    "tstart": 55555.0,
    "tsamp": tsamp,
}

data = np.random.normal(0,noisesigma,size=(nchans, nsamp))+127
filename1 = "RFIoutput_test.fil"
create_filterbank(data, filename1, metadata)

filename2 = "sigproc_binary.fil"

data1, header1 = read_filterbank(filename1)
data2,header2 = read_filterbank(filename2)


#plot data, dataafter in same window in adjacent subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
ax1.imshow(data,aspect='auto')
ax1.set_title('spectralib')
ax2.imshow(data1,aspect='auto')
ax2.set_title('sigproc')
plt.show()