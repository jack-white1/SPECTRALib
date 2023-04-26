import numpy as np
import math
import random

def generate_rfi(data, **kwargs):
    """
    Generate synthetic RFI data and save it as a filterbank file.

    :param data: The input data to add RFI to.
    :param kwargs: Additional keyword arguments.
    """
    nchans, nsamp = data.shape

    # Set default values for the keyword arguments
    default_kwargs = {
        'freqchanswidth': nchans,
        'onlength': 10,
        'ispersistent': False,
        'doesrepeat': False,
        'numrepeats': 0,
        'dutycycle': 50,  # Added default value for duty cycle
        'RFIamplitude': 200
    }

    # Update default values with provided keyword arguments
    default_kwargs.update(kwargs)

    # Unpack the updated keyword arguments
    freqchanswidth = default_kwargs['freqchanswidth']
    onlength = default_kwargs['onlength']
    ispersistent = default_kwargs['ispersistent']
    doesrepeat = default_kwargs['doesrepeat']
    numrepeats = default_kwargs['numrepeats']
    dutycycle = default_kwargs['dutycycle']  # Unpacked duty cycle
    RFIamplitude = default_kwargs['RFIamplitude']

    # Compute offlength based on the provided onlength and dutycycle
    offlength = round(onlength * (100 - dutycycle) / dutycycle)

    startfreqindex = 0
    if nchans == freqchanswidth:
        print("Adding broadband ", end="")
    else:
        print("Adding narrowband ", end="")
        startfreqindex = np.random.randint(0, nchans)

    if ispersistent and not doesrepeat:
        print("persistent RFI")
    elif not ispersistent and doesrepeat:
        print("repeating RFI, nrepeat = " + str(numrepeats))
    elif not ispersistent and not doesrepeat:
        print("impulse RFI")
    elif ispersistent and doesrepeat:
        print("persistent periodic RFI")

    endfreqindex = startfreqindex + freqchanswidth

    if ispersistent == False:
        starttimeindex = np.random.randint(0, nsamp)
        starttimeindex = starttimeindex - round(onlength/2)
        endtimeindex = starttimeindex + onlength
        if starttimeindex < 0:
            starttimeindex = 0
        if endtimeindex > nsamp:
            endtimeindex = nsamp
    else:
        starttimeindex = 0
        if doesrepeat:
            endtimeindex = starttimeindex + onlength
        else:
            endtimeindex = nsamp

    if doesrepeat:
        if ispersistent:
            while endtimeindex < nsamp:
                data[startfreqindex:endfreqindex, starttimeindex:endtimeindex] += RFIamplitude
                starttimeindex += onlength + offlength
                endtimeindex += onlength + offlength
        else:
            for i in range(-round(numrepeats/2),round(numrepeats/2),1):
                offset = i * (onlength + offlength)
                if starttimeindex + offset < 0:
                    continue
                if endtimeindex + offset > nsamp:
                    continue
                data[startfreqindex:endfreqindex, starttimeindex+offset:endtimeindex+offset] += RFIamplitude
    else:
        data[startfreqindex:endfreqindex, starttimeindex:endtimeindex] += RFIamplitude

    data = np.clip(data, 0, 255)
    return data

def add_wandering_baseline(data, **kwargs):
    # A function to add a slowly varying random signal to all channels

    default_kwargs = {
        'wanderingbaselineamplitude': 1,
        'wanderingbaselineperiod': 100,
        'custom_baseline': None
    }
    default_kwargs.update(kwargs)

    wanderingbaselineamplitude = default_kwargs['wanderingbaselineamplitude']
    wanderingbaselineperiod = default_kwargs['wanderingbaselineperiod']
    custom_baseline = default_kwargs['custom_baseline']

    nchans, nsamp = data.shape

    if custom_baseline is None:
        # Generate a random signal that is the length of the data
        wanderingbaseline = np.random.normal(0, wanderingbaselineamplitude, nsamp + wanderingbaselineperiod)

        # Lowpass filter the signal
        # This is to simulate the effect of a slowly varying baseline
        # The filter is a simple moving average
        filteredwanderingbaseline = np.zeros(nsamp)
        for i in range(nsamp):
            filteredwanderingbaseline[i] = np.mean(wanderingbaseline[i:i + wanderingbaselineperiod])
    else:
        # Use the custom provided baseline
        assert len(custom_baseline) == nsamp, "Custom baseline must have the same length as the data"
        filteredwanderingbaseline = custom_baseline


    # Add the filtered signal to each channel
    for i in range(nchans):
        data[i, :] += filteredwanderingbaseline

    data = np.clip(data, 0, 255)

    return data


def sampleloguniform(lower,upper):
    lowerlog = math.log(lower)
    upperlog = math.log(upper)
    return math.exp(random.uniform(lowerlog,upperlog))