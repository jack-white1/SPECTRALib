import numpy as np
import matplotlib.pyplot as plt
import random

from spectralib.rfi import generate_rfi, add_wandering_baseline, sampleloguniform
from spectralib.filterbank import create_filterbank, dedisperse_filterbank, dedisperse_filterbank_to_timeseries
from spectralib.pulsar import generate_binary_pulsar


def main():
    tobs = 600 # observation time in seconds
    tsamp = 0.000128 # sample time in seconds

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

    # FRB parameters
    frb_params = {
        'frb_duration': 100,
        'frb_amplitude': 200,
        'time_profile': np.random.normal(1, 0.1, 100),
        'freq_profile': np.random.normal(1, 0.1, metadata['nchans']),
    }

    # Inject the binary pulsar signature
    data = generate_binary_pulsar(data, DM, metadata['tsamp'], metadata['foff'], metadata['fch1'], p_rest, binary_params, **frb_params)

    # Create the filterbank file
    output_filename = "RFIoutput_with_binary_pulsar.fil"
    create_filterbank(data,output_filename, metadata)

    # Dedisperse the data
    dedispersed_data = dedisperse_filterbank(data, DM, tsamp, foff, fch1)
    dedispersed_timeseries = dedisperse_filterbank_to_timeseries(data, DM, tsamp, foff, fch1)

    # Create the figure and axes
    fig, axes = plt.subplots(4, 1, figsize=(10, 14), sharex=True)

    ax1, ax2, ax3, ax4 = axes

    # Plot the data
    im1 = ax1.imshow(data6, aspect="auto", cmap="plasma", origin="lower")
    ax1.set_title("Original Data")
    ax1.set_ylim(ax1.get_ylim()[::-1])  # Flip the y-axis

    im2 = ax2.imshow(data, aspect="auto", cmap="plasma", origin="lower")
    ax2.set_title("Data with Injected Binary Pulsar")
    ax2.set_ylim(ax2.get_ylim()[::-1])  # Flip the y-axis

    im3 = ax3.imshow(dedispersed_data, aspect="auto", cmap="plasma", origin="lower")
    ax3.set_title("Dedispersed Data")
    ax3.set_ylim(ax3.get_ylim()[::-1])  # Flip the y-axis

    im4 = ax4.plot(dedispersed_timeseries)
    ax4.set_title("Dedispersed Time Series")

    # Set the xlabel only for the bottom plot
    ax4.set_xlabel("Time (bins)")

    # Set the ylabel for all plots
    ax1.set_ylabel("Frequency Channel")
    ax2.set_ylabel("Frequency Channel")
    ax3.set_ylabel("Frequency Channel")

    plt.tight_layout()
    plt.show()








if __name__ == "__main__":
    main()

