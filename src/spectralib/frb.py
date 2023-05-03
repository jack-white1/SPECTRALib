import numpy as np

def generate_high_resolution_pulse(data, DM, tsamp, foff, fch1, freq_upsample_factor, **pulse_params):
    pulse_start_index = pulse_params.get('pulse_start_index', 0)
    pulse_duration = pulse_params.get('pulse_duration', 100)
    pulse_amplitude = pulse_params.get('pulse_amplitude', 200)
    time_profile = pulse_params.get('time_profile', None)
    freq_profile = pulse_params.get('freq_profile', None)

    nchans, nsamp = data.shape

    if time_profile is None:
        time_profile = np.ones(pulse_duration)
    if freq_profile is None:
        freq_profile = np.ones(nchans)

    # Interpolate time and frequency profiles
    time_profile_hr = np.interp(np.linspace(0, pulse_duration - 1, pulse_duration * freq_upsample_factor),
                                np.arange(pulse_duration), time_profile)
    freq_profile_hr = np.interp(np.linspace(0, nchans - 1, nchans * freq_upsample_factor),
                                np.arange(nchans), freq_profile)

    # Calculate high-resolution dispersion offsets
    foff_hr = foff / freq_upsample_factor
    fch1_hr = np.array([fch1 + i * foff for i in range(nchans * freq_upsample_factor)])
    sub_band_offsets = calculate_dispersion_offsets(DM, fch1_hr, foff_hr, nchans * freq_upsample_factor, tsamp)

    for i in range(nchans * freq_upsample_factor):
        for j in range(pulse_duration * freq_upsample_factor):
            time_index = round((pulse_start_index * freq_upsample_factor) + j + sub_band_offsets[i])
            if 0 <= time_index < nsamp * freq_upsample_factor:
                data[i // freq_upsample_factor, time_index] += pulse_amplitude * time_profile_hr[j] * freq_profile_hr[i]

    data = np.clip(data, 0, 255)
    return data

def generate_pulse(data, DM, tsamp, foff, fch1, **pulse_params):
    pulse_start_index = pulse_params.get('pulse_start_index', 0)
    pulse_duration = pulse_params.get('pulse_duration', 100)
    pulse_amplitude = pulse_params.get('pulse_amplitude', 200)
    time_profile = pulse_params.get('time_profile', None)
    freq_profile = pulse_params.get('freq_profile', None)

    nchans, nsamp = data.shape

    if time_profile is None:
        time_profile = np.ones(pulse_duration)
    if freq_profile is None:
        freq_profile = np.ones(nchans)

    offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)

    for i in range(nchans):
        for j in range(pulse_duration):
            time_index = round(pulse_start_index + j + offsets[i])
            if 0 <= time_index < nsamp:
                data[i, time_index] += pulse_amplitude * time_profile[j] * freq_profile[i]

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