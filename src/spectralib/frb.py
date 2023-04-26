import numpy as np

def generate_frb(data, DM, tsamp, foff, fch1, **frb_params):
    frb_start_index = frb_params.get('frb_start_index', 0)
    frb_duration = frb_params.get('frb_duration', 100)
    frb_amplitude = frb_params.get('frb_amplitude', 200)
    time_profile = frb_params.get('time_profile', None)
    freq_profile = frb_params.get('freq_profile', None)

    nchans, nsamp = data.shape

    if time_profile is None:
        time_profile = np.ones(frb_duration)
    if freq_profile is None:
        freq_profile = np.ones(nchans)

    offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)

    for i in range(nchans):
        for j in range(frb_duration):
            time_index = round(frb_start_index + j + offsets[i])
            if 0 <= time_index < nsamp:
                data[i, time_index] += frb_amplitude * time_profile[j] * freq_profile[i]

    data = np.clip(data, 0, 255)
    return data

def calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp):
    freqs = np.zeros(nchans)
    for i in range(nchans):
        freqs[i] = fch1 + i * foff

    delays = np.zeros(nchans)
    for i in range(nchans):
        delays[i] = 4148.741601 * DM * ((1 / (freqs[i] ** 2)) - (1 / (freqs[0] ** 2)))

    offsets = np.zeros(nchans)
    for i in range(nchans):
        offsets[i] = round(delays[i] / tsamp)
    
    return offsets