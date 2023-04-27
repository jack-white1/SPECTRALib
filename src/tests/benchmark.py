import sys
sys.path.append("../spectralib/")
import numpy as np
import timeit
import os
from spectralib.filterbank import create_filterbank
from spectralib.pulsar import generate_binary_pulsar
from spectralib.frb import generate_pulse
from spectralib.rfi import generate_rfi

def benchmark_filterbank():
    def run_create_filterbank():
        tobs = 600 # observation time in seconds
        tsamp = 0.000128 # sample time in seconds
        metadata = {
        "source_name": "SPECTRAL_FRB",
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
        data = np.random.normal(0,noisesigma,size=(nchans, nsamp))+127
        output_file = "benchmark_filterbank.fil"
        create_filterbank(data,output_file, metadata)
        if os.path.exists(output_file):
            os.remove(output_file)

    return timeit.timeit(run_create_filterbank, number=10)

def benchmark_pulsar():
    def run_generate_pulsar():
        tobs = 600 # observation time in seconds
        tsamp = 0.000128 # sample time in seconds
        metadata = {
        "source_name": "SPECTRAL_FRB",
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
        data = np.random.normal(0,noisesigma,size=(nchans, nsamp))+127
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
        pulse_params = {
            'pulse_duration': 100,
            'pulse_amplitude': 200,
            'time_profile': np.random.normal(1, 0.1, 100),
            'freq_profile': np.random.normal(1, 0.1, metadata['nchans']),
        }

        # Inject the binary pulsar signature
        data = generate_binary_pulsar(data, DM, metadata['tsamp'], metadata['foff'], metadata['fch1'], p_rest, binary_params, **pulse_params)

        # Create the filterbank file
        output_filename = "RFIoutput_with_binary_pulsar.fil"
        create_filterbank(data,output_filename, metadata)

    return timeit.timeit(run_generate_pulsar, number=10)

def benchmark_frb():
    def run_generate_pulse():
        generate_pulse()

    return timeit.timeit(run_generate_pulse, number=10)

def benchmark_rfi():
    def run_generate_rfi():
        generate_rfi()

    return timeit.timeit(run_generate_rfi, number=10)

if __name__ == "__main__":
    filterbank_time = benchmark_filterbank()
    pulsar_time = benchmark_pulsar()
    #frb_time = benchmark_frb()
    #rfi_time = benchmark_rfi()

    print(f"Create Filterbank: {filterbank_time:.4f} seconds")
    print(f"Generate Pulsar: {pulsar_time:.4f} seconds")
    #print(f"Generate FRB: {frb_time:.4f} seconds")
    #print(f"Generate RFI: {rfi_time:.4f} seconds")
