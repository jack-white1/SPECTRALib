import numpy as np
import matplotlib.pyplot as plt
import random

from spectralib.rfi import generate_rfi, add_wandering_baseline, sampleloguniform
from spectralib.filterbank import create_filterbank, plot_and_save


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
    sinusoidal_wave = np.sin(2 * np.pi * interferencefrequency * t) * 10

    data = add_wandering_baseline(data, custom_baseline=sinusoidal_wave)
    data1a = data.copy()
    
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

    filename = "RFIoutput.fil"
    create_filterbank(data, filename, metadata)


    # Plot data0, data1, data1a, data2, data3, data4, data5, data6 in the same window so you can see the progression of adding RFI
    # and give each subplot a title saying what type of noise has been added
    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, figsize=(16, 6), sharex=True, sharey=True)

    im0 = ax1.imshow(data0, aspect="auto", cmap="plasma", origin="lower")
    ax1.set_title("0. Original Data")
    plt.colorbar(im0, ax=ax1)
    ax1.set_ylim(ax1.get_ylim()[::-1])  # Flip the y-axis

    im1 = ax2.imshow(data1, aspect="auto", cmap="plasma", origin="lower")
    ax2.set_title("1. Wandering Baseband")
    plt.colorbar(im1, ax=ax2)
    #ax2.set_ylim(ax2.get_ylim()[::-1])  # Flip the y-axis

    im1a = ax3.imshow(data1a, aspect="auto", cmap="plasma", origin="lower")
    ax3.set_title("1a. 50Hz Mains Interference")
    plt.colorbar(im1a, ax=ax3)
    #ax3.set_ylim(ax3.get_ylim()[::-1])  # Flip the y-axis

    im2 = ax4.imshow(data2, aspect="auto", cmap="plasma", origin="lower")
    ax4.set_title("2. Add Persistent Narrowband RFI")
    plt.colorbar(im2, ax=ax4)
    #ax4.set_ylim(ax4.get_ylim()[::-1])  # Flip the y-axis

    im3 = ax5.imshow(data3, aspect="auto", cmap="plasma", origin="lower")
    ax5.set_title("3. Add Repeating Narrowband RFI")
    plt.colorbar(im3, ax=ax5)
    #ax5.set_ylim(ax5.get_ylim()[::-1])  # Flip the y-axis

    im4 = ax6.imshow(data4, aspect="auto", cmap="plasma", origin="lower")
    ax6.set_title("4. Add Impulsive Narrowband RFI")
    plt.colorbar(im4, ax=ax6)
    #ax6.set_ylim(ax6.get_ylim()[::-1])  # Flip the y-axis

    im5 = ax7.imshow(data5, aspect="auto", cmap="plasma", origin="lower")
    ax7.set_title("5. Add Repeating Broadband RFI")
    plt.colorbar(im5, ax=ax7)
    #ax7.set_ylim(ax7.get_ylim()[::-1])  # Flip the y-axis

    im6 = ax8.imshow(data6, aspect="auto", cmap="plasma", origin="lower")
    ax8.set_title("6. Add Impulsive Broadband RFI")
    plt.colorbar(im6, ax=ax8)
    #ax8.set_ylim(ax8.get_ylim()[[::-1]])  # Flip the y-axis

    plt.xlabel("Time (bins)")
    plt.ylabel("Frequency (bins)")
    plt.tight_layout()
    plt.show()

    # Call the function for each dataset
    #plot_and_save(data0, "0. Original Data", "../images/original_data.png")
    #plot_and_save(data1, "1. Wandering Baseband", "../images/wandering_baseband.png")
    #plot_and_save(data1a, "1a. 50Hz Mains Interference", "../images/mains_interference.png")
    #plot_and_save(data2, "2. Add Persistent Narrowband RFI", "../images/persistent_narrowband_RFI.png")
    #plot_and_save(data3, "3. Add Repeating Narrowband RFI", "../images/repeating_narrowband_RFI.png")
    #plot_and_save(data4, "4. Add Impulsive Narrowband RFI", "../images/impulsive_narrowband_RFI.png")
    #plot_and_save(data5, "5. Add Repeating Broadband RFI", "../images/repeating_broadband_RFI.png")
    #plot_and_save(data6, "6. Add Impulsive Broadband RFI", "../images/impulsive_broadband_RFI.png")



if __name__ == "__main__":
    main()

