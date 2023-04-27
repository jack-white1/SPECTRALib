# Welcome to SPECTRALib!

SPECTRALib is a 100% python library with minimal dependencies (`numpy` and `matplotlib`) for handling filterbank files and generating synthetic transients such as pulsars and FRBs, mixed with RFI and other effects.

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
 - `python example_rfi.py` or `python3 example_rfi.py`
 - `python example_frb.py` or `python3 example_frb.py`
 - `python example_pulsar.py` or `python3 example_pulsar.py`

 # Documentation
 
 ## Filterbank Functions

 
 ## RFI Functions
 The RFI modelling in spectralib is designed to be as modular and parametric as possible.

 ## FRB Functions
To simulate the smearing seen at higher DMs and lower frequencies, there is an optional function to simulate FRBs at a higher resolution than the time and frequency quantization of the filterbank.

 ## Pulsar Functions
 Conceptually, spectralib models either solitary or binary pulsars (with `generate_solitary_pulsar()` and `generate_binary_pulsar()`) as a series of pulses, using the same function (`generate_pulse()`) as is used to generate FRBs. 
 

