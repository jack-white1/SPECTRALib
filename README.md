# Welcome to SPECTRALib!

SPECTRALib is a 100% python library with minimal dependencies (`numpy` and `matplotlib`) for handling filterbank files and generating synthetic transients such as pulsars and FRBs, mixed with RFI and other effects. These functions are designed to be fully parametric, so you can generate a wide range of synthetic data, e.g. arbitrary pulse time and frequency profiles, arbitrary RFI time and frequency profiles.

It can also simulate intra-channel smearing of pulses with an arbitrary time profile. This is useful for simulating FRBs at high DMs and low frequencies, where the smearing is significant.

SPECTRALib stands for Synthetic Pulsar Emission, Contamination and Transients Radio Astronomy Library.

### Feel free to use the code however you wish:
 - You can `import spectralib` and use the functions in your code
 - You can modify the [**example scripts**](https://github.com/jack-white1/SPECTRALib/examples) to generate files that fit your requirement
 - The functions should be modular enough to **copy and paste** into your own code

### Citation
If you use SPECTRALib to contribute to a publication, please cite:
___Paper that you can cite___

# Installation

`pip install spectralib`

# RFI Example
![Animation showing RFI creation process](/images/rfi.gif)

# FRB Example
![Example of FRB created with spectralib](/images/frb.png)

# Pulsar Example
![Example of pulsar created with spectralib](/images/pulsar.png)

# Usage
Once you have installed SPECTRALib with `pip install spectralib`, you can import the library into your python code with `import spectralib`.

To test the library, download and run the examples by cloning this git repo.

 - `git clone https://github.com/jack-white1/SPECTRALib`
 - `cd SPECTRALib/examples`
 - `python example_rfi_generator.py` or `python3 example_rfi_generator.py`
 - `python example_frb_generator.py` or `python3 example_frb_generator.py`
 - `python example_pulsar_generator.py` or `python3 example_pulsar_generator.py`

 # Documentation
 
 ## Filterbank Functions
Check `/examples/example_write_read_plot_filterbank.py` for a full example of how to use the filterbank functions.
 
 ## RFI Functions
 The RFI modelling in spectralib is designed to be as modular and parametric as possible.

 Check `/examples/example_rfi_generator.py` for a full example of how to use the RFI functions.

 ## FRB Functions
To simulate the smearing seen at higher DMs and lower frequencies, there is an optional function to simulate FRBs at a higher resolution than the time and frequency quantization of the filterbank.

Check `/examples/example_frb_generator.py` for a full example of how to use the FRB functions.

 ## Pulsar Functions
 Conceptually, spectralib models either solitary or binary pulsars (with `generate_solitary_pulsar()` and `generate_binary_pulsar()`) as a series of pulses, using the same function (`generate_pulse()`) as is used to generate FRBs.

Check `/examples/example_pulsar_generator.py` for a full example of how to use `generate_binary_pulsar()` to generate a semi-realistic filterbank.

#### `generate_binary_pulsar(data, DM, tsamp, foff, fch1, binary_params, **pulse_params)`

Check `/examples/example_simple_binary_pulsar_generator.py` for a full example of how to use `generate_binary_pulsar()`.

This function aspires to be a python version of the `fake` function in SIGPROC (Lorimer).
 - data (2D numpy array): Input data array of shape (nchans, nsamp) where nchans is the number of frequency channels and nsamp is the number of time samples.
 - DM (float): Dispersion measure of the pulsar signal.
 - tsamp (float): Sampling time in seconds.
 - foff (float): Frequency offset between two adjacent channels.
 - fch1 (float): Frequency of the first channel in MHz.
 - binary_params (dictionary): A dictionary containing the binary pulsar parameters with the following keys:
     - rest_period (float): Rest period of the pulsar in seconds, e.g. 0.005 for a 200 Hz pulsar.
     - inclination (float): Inclination angle of the binary system in radians, e.g. 0.5 for ~28.59 degrees.
     - orbital_period (float): Orbital period of the binary system in seconds, e.g. 7200 for a 2 hr orbit binary system.
     - start_phase (float): Starting phase of the pulsar in radians, e.g. 0.
     - companion_mass (float): Mass of the companion in solar masses, e.g. 5.
     - pulsar_mass (float): Mass of the pulsar in solar masses, e.g. 1.4.
     - eccentricity (float): Eccentricity of the binary system, e.g. 0 for a circular orbit.
     - omega (float): Longitude of periastron in radians, e.g. 0.
 - **pulse_params: Additional pulse parameters to pass to the generate_pulse function. These include:
     - pulse_start_index (int): The start offset time sample index for the pulse. Delays pulse by number of bins provided. Default is 0.
     - pulse_duration (int): The duration of the pulse in time samples. Default is 100.
     - pulse_amplitude (int): The amplitude of the pulse. Default is 200.
     - time_profile (1D numpy array with length = pulse_duration): The time profile of the pulse. Default is None which will produce a top-hat pulse.
     - freq_profile (1D numpy array with length = nchans): The frequency profile of the pulse. Default is None which will produce a uniform frequency profile.

 

