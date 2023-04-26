from spectralib.frb import generate_frb, calculate_dispersion_offsets
import numpy as np

def apparent_pulse_period(binary_params, p_rest, time):
    # heavily influenced by sigproc's fake, Duncan Lorimer, and Mike Keith's implementation in C
    G = 6.67430e-11
    M_SUN = 1.9885e30
    SPEED_OF_LIGHT = 299792458

    inclination = binary_params["inclination"]
    orbital_period = binary_params["orbital_period"]
    start_phase = binary_params["start_phase"]
    mass_companion = binary_params["companion_mass"]
    mass_pulsar = binary_params["pulsar_mass"]
    eccentricity = binary_params["eccentricity"]
    omega = binary_params["omega"]

    omega_b = 2 * np.pi / orbital_period
    t0 = start_phase * orbital_period
    mass_function = (mass_companion * np.sin(inclination))**3 / (mass_companion + mass_pulsar)**2
    asini = (G * M_SUN * mass_function * orbital_period**2 / (4 * np.pi**2))**(1/3)

    mean_anomaly = omega_b * (time - t0)
    eccentric_anomaly = mean_anomaly

    for _ in range(10):
        e_next = eccentric_anomaly - (eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly) - mean_anomaly) / (1 - eccentricity * np.cos(eccentric_anomaly))
        if abs(e_next - eccentric_anomaly) < 1e-10:
            break
        eccentric_anomaly = e_next

    true_anomaly = 2 * np.arctan(np.sqrt((1 + eccentricity) / (1 - eccentricity)) * np.tan(eccentric_anomaly / 2))
    velocity = omega_b * asini / np.sqrt(1 - eccentricity**2) * (np.cos(omega + true_anomaly) + eccentricity * np.cos(omega))
    p_apparent = p_rest * (1 + velocity / SPEED_OF_LIGHT)

    return p_apparent

def generate_binary_pulsar(data, DM, tsamp, foff, fch1, p_rest, binary_params, **frb_params):
    nchans, nsamp = data.shape
    pulse_duration = frb_params.get("frb_duration", 100)

    # Use calculate_dispersion_offsets from frb.py to calculate the maximum offset, and subtract it from 0 to get the start index
    # this ensures the pulsar signal is present in the entire data array
    offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)
    start_index = -max(offsets)

    pulse = 0
    pulse_start_time = start_index*tsamp
    while pulse_start_time < nsamp*tsamp:
        pulse_start_time = start_index*tsamp + pulse * p_rest
        app_pulse_period = apparent_pulse_period(binary_params, p_rest, pulse_start_time)
        print("At time : ",pulse_start_time," apparent pulse period: ", app_pulse_period)
        frb_start_time = pulse_start_time + app_pulse_period
        frb_start_index = int(frb_start_time / tsamp)

        data = generate_frb(data, DM, tsamp, foff, fch1, frb_start_index=frb_start_index, **frb_params)
        pulse+=1

    return data

def generate_solitary_pulsar(data, DM, tsamp, foff, fch1, p_rest, **frb_params):
    nchans, nsamp = data.shape
    pulse_duration = frb_params.get("frb_duration", 100)


    # Use calculate_dispersion_offsets from frb.py to calculate the maximum offset, and subtract it from 0 to get the start index
    # this ensures the pulsar signal is present in the entire data array, rather than missing from the bottom left corner
    offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)
    start_index = -max(offsets)
    pulse = 0
    pulse_start_time = start_index*tsamp
    while pulse_start_time < nsamp*tsamp:
        pulse_start_time = start_index*tsamp + pulse * p_rest
        frb_start_index = int(pulse_start_time / tsamp)

        data = generate_frb(data, DM, tsamp, foff, fch1, frb_start_index=frb_start_index, frb_duration=pulse_duration, **frb_params)
        pulse+=1

    return data