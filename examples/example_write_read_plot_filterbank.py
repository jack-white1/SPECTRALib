import numpy as np
import matplotlib.pyplot as plt
import random

from spectralib import *


def main():
    tobs = 10 #observation time in seconds
    tsamp = 0.001 #sample time in seconds

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

    print("Observation time of " + str(nsamp*tsamp) + " seconds")

    # add random wandering baseline
    data = add_wandering_baseline(data, wanderingbaselineamplitude=30, wanderingbaselineperiod=1000)

    # add 50hz interference
    nsamp = data.shape[1]
    sampling_rate = 1/tsamp
    interferencefrequency = 50
    t = np.arange(nsamp) / sampling_rate
    sinusoidal_wave = np.sin(2 * np.pi * interferencefrequency * t)

    data = add_wandering_baseline(data, custom_baseline=sinusoidal_wave)
    
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

    DM = 1000  # Dispersion measure of the FRB

    # Binary pulsar parameters
    binary_params = {
        "inclination": np.radians(45),
        "orbital_period": 200,
        "start_phase": 0,
        "companion_mass": 1.4,
        "pulsar_mass": 1.4,
        "eccentricity": 0.1,
        "omega": np.radians(90),
    }

    # Rest pulse period of the pulsar
    p_rest = 1.0  # seconds

    frb_duration = 50  # Duration of the FRB
    frb_amplitude = 50  # Amplitude of the FRB

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

    # FRB parameters
    frb_params = {
        'frb_duration': frb_duration,
        'frb_amplitude': frb_amplitude,
        'time_profile': time_profile,
        'freq_profile': freq_profile,
    }

    # Inject the binary pulsar signature
    data = generate_binary_pulsar(data, DM, metadata['tsamp'], metadata['foff'], metadata['fch1'], p_rest, binary_params, **frb_params)

    filename = "RFIoutput.fil"
    create_filterbank(data, filename, metadata)
    show_filterbank(filename)




if __name__ == "__main__":
    main()
