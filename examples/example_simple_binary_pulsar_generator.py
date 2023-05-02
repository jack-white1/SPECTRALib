import numpy as np
import matplotlib.pyplot as plt

from spectralib.filterbank import create_filterbank, dedisperse_filterbank_data, dedisperse_filterbank_data_to_timeseries, read_filterbank
from spectralib.pulsar import generate_binary_pulsar


def main():

    # Initialise telescope metadata
    tobs = 10 # observation time in seconds
    tsamp = 0.001 # sample time in seconds

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
    "nifs": 1,
    "nbeams": 1,
    "ibeam": 1
    }

    noisesigma = 18 #standard deviation of noise, value copied from some ASKAP data
    nchans = metadata["nchans"]
    nsamp = round(tobs/tsamp)
    tsamp = metadata["tsamp"]
    fch1 = metadata["fch1"]
    foff = metadata["foff"]
    data = np.random.normal(0,noisesigma,size=(nchans, nsamp))+127
    data0 = data.copy()

    print("Observation time of " + str(nsamp*tsamp) + " seconds")

    DM = 2000  # Dispersion measure of the FRB

    # Binary pulsar parameters
    binary_params = {
        "rest_period":  1.0,                 # Rest period of the pulsar (seconds)
        "inclination": np.radians(45),  # Inclination angle of the binary system (radians)
        "orbital_period": 7200,          # Orbital period of the binary system (seconds)
        "start_phase": 0,               # Starting phase of the pulsar (radians)
        "companion_mass": 5,          # Mass of the companion (solar masses)
        "pulsar_mass": 1.4,             # Mass of the pulsar (solar masses)
        "eccentricity": 0.0,            # Eccentricity of the binary system
        "omega": np.radians(0),        # Longitude of periastron (radians)
    }

    
      # seconds

    pulse_duration = 100  # Duration of the FRB
    pulse_amplitude = 100  # Amplitude of the FRB

    freq_profile = np.ones(nchans)
    time_profile = np.ones(pulse_duration)

    # Pulse parameters
    pulse_params = {
        'pulse_duration': pulse_duration,
        'pulse_amplitude': pulse_amplitude,
        'time_profile': time_profile,
        'freq_profile': freq_profile,
    }

    # Inject the binary pulsar signature
    data = generate_binary_pulsar(data, DM, metadata['tsamp'], metadata['foff'], metadata['fch1'], binary_params, **pulse_params)

    # Create the filterbank file
    output_filename = "output_with_binary_pulsar.fil"
    create_filterbank(data,output_filename, metadata)

    # Dedisperse the data
    dedispersed_data = dedisperse_filterbank_data(data, DM, tsamp, foff, fch1)
    dedispersed_timeseries = dedisperse_filterbank_data_to_timeseries(data, DM, tsamp, foff, fch1)

    # Create the figure and axes
    fig, axes = plt.subplots(4, 1, figsize=(10, 14), sharex=True)

    ax1, ax2, ax3, ax4 = axes

    # Plot the data
    im1 = ax1.imshow(data0, aspect="auto", cmap="plasma")
    ax1.set_title("Original Data")
    #ax1.set_ylim(ax1.get_ylim()[::-1])  # Flip the y-axis

    im2 = ax2.imshow(data, aspect="auto", cmap="plasma")
    ax2.set_title("Data with Injected Binary Pulsar")
    #ax2.set_ylim(ax2.get_ylim()[::-1])  # Flip the y-axis

    im3 = ax3.imshow(dedispersed_data, aspect="auto", cmap="plasma")
    ax3.set_title("Dedispersed Data")
    #ax3.set_ylim(ax3.get_ylim()[::-1])  # Flip the y-axis

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

