import sys
sys.path.append("../src/")

import numpy as np
import matplotlib.pyplot as plt
import random

from spectralib.rfi import generate_rfi, add_wandering_baseline, sampleloguniform
from spectralib.filterbank import create_filterbank
from spectralib.frb import generate_frb


def main():
    tobs = 10 # observation time in seconds
    tsamp = 0.001 # sample time in seconds

    metadata = {
    "source_name": "spectralib_FRB",
    "machine_id": 0,
    "telescope_id": 0,
    "data_type": 0,
    "fch1": 1500.0,
    "foff": -0.5,
    "nchans": 500,
    "nbits": 8,
    "tstart": 55555.0,
    "tsamp": tsamp,
    "nifs": 1,
    "nbeams": 1,
    "ibeam": 1,
    "nsamples": round(tobs/tsamp)
    }

    noisesigma = 18 #standard deviation of noise, value copied from some ASKAP data
    nchans = metadata["nchans"]
    nsamp = metadata["nsamples"]
    tsamp = metadata["tsamp"]
    fch1 = metadata["fch1"]
    foff = metadata["foff"]
    data = np.random.normal(0,noisesigma,size=(nchans, nsamp))+127
    data0 = data.copy()

    print("Observation time of " + str(nsamp*tsamp) + " seconds")

    # add random wandering baseline
    data = add_wandering_baseline(data, wanderingbaselineamplitude=30, wanderingbaselineperiod=1000)
    data1 = data.copy()

    # add 50hz interference
    nsamp = data.shape[1]
    sampling_rate = 1/tsamp
    interferencefrequency = 50
    t = np.arange(nsamp) / sampling_rate
    sinusoidal_wave = np.sin(2 * np.pi * interferencefrequency * t)

    data1a = add_wandering_baseline(data, custom_baseline=sinusoidal_wave)
    
    # add some narrowband RFI that is persistent
    persistent_narrowband_amount = 5
    for i in range(persistent_narrowband_amount):
        kwargs = {
            'freqchanswidth': round(sampleloguniform(1, 20)),
            'ispersistent': True,
            'doesrepeat': False,
            'RFIamplitude': random.uniform(20, 200)
        }
        data = generate_rfi(data, **kwargs)

    data2 = data.copy()

    # and some narrowband RFI that repeats
    repeating_narrowband_amount = 10
    for i in range(repeating_narrowband_amount):
        kwargs = {
            'freqchanswidth': round(sampleloguniform(1, 20)),
            'onlength': round(sampleloguniform(1, 1000)),
            'dutycycle': sampleloguniform(1, 100),
            'doesrepeat': True,
            'numrepeats': round(sampleloguniform(100, 10000)),
            'RFIamplitude': random.uniform(20, 200)
        }
        data = generate_rfi(data, **kwargs)

    data3 = data.copy()

    # and some narrowband RFI that is impulsive
    impulsive_narrowband_amount = 10
    for i in range(impulsive_narrowband_amount):
        kwargs = {
            'freqchanswidth': round(sampleloguniform(1, 20)),
            'onlength': round(sampleloguniform(1, 10000)),
            'ispersistent': False,
            'doesrepeat': False,
            'RFIamplitude': random.uniform(20, 200)
        }
        data = generate_rfi(data, **kwargs)

    data4 = data.copy()

    # and some broadband RFI that repeats
    broadband_repeating_amount = 3
    for i in range(broadband_repeating_amount):
        kwargs = {
            'freqchanswidth': nchans,
            'onlength': round(sampleloguniform(1, 1000)),
            'dutycycle': sampleloguniform(1, 10),
            'doesrepeat': True,
            'numrepeats': round(sampleloguniform(10, 10000)),
            'RFIamplitude': random.uniform(20, 200)
        }
        data = generate_rfi(data, **kwargs)

    data5 = data.copy()

    broadband_impulsive_amount = 10
    for i in range(broadband_impulsive_amount):
        kwargs = {
            'freqchanswidth': nchans,
            'onlength': round(sampleloguniform(1, 1000)),
            'ispersistent': False,
            'doesrepeat': False,
            'RFIamplitude': random.uniform(70, 200)
        }
        data = generate_rfi(data, **kwargs)


    # add an FRB

    data6 = data.copy()

    DM = 10000  # Dispersion measure of the FRB
    frb_start_index = 100  # Start index of the FRB
    frb_duration = 50  # Duration of the FRB
    frb_amplitude = 200  # Amplitude of the FRB

        # Create a realistic frequency profile (Gaussian profile)
    def gaussian(x, mu, sigma):
        return np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    freq_mu = nchans // 2
    freq_sigma = nchans // 8
    freq_profile = gaussian(np.arange(nchans), freq_mu, freq_sigma)

    # Create a realistic time profile (Gaussian profile)
    time_mu = frb_duration // 2
    time_sigma = frb_duration // 8
    time_profile = gaussian(np.arange(frb_duration), time_mu, time_sigma)

    frb_params = {
        'frb_start_index': frb_start_index,
        'frb_duration': frb_duration,
        'frb_amplitude': frb_amplitude,
        'time_profile': time_profile,  # Gaussian time profile
        'freq_profile': freq_profile  # Gaussian frequency profile
    }

    # Generate the FRB
    data = generate_frb(data, DM, metadata['tsamp'], metadata['foff'], metadata['fch1'], **frb_params)

    # Create the filterbank file
    output_filename = "RFIoutput_with_FRB.fil"
    create_filterbank(data, output_filename, metadata)

    # Plot the original data and the data with the injected FRB
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, sharey=True)

    im1 = ax1.imshow(data6, aspect="auto", cmap="plasma", origin="lower")
    ax1.set_title("Original Data")
    plt.colorbar(im1, ax=ax1)
    ax1.set_ylim(ax1.get_ylim()[::-1])  # Flip the y-axis

    im2 = ax2.imshow(data, aspect="auto", cmap="plasma", origin="lower")
    ax2.set_title("Data with Injected FRB")
    plt.colorbar(im2, ax=ax2)
    #ax2.set_ylim(ax2.get_ylim()[::-1])  # Flip the y-axis

    plt.xlabel("Time (bins)")
    plt.ylabel("Frequency Channel")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
