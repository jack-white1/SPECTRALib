import unittest
import numpy as np
from spectralib.frb import generate_frb, calculate_dispersion_offsets
from spectralib.pulsar import generate_binary_pulsar, generate_solitary_pulsar, apparent_pulse_period

class TestPulsar(unittest.TestCase):

    def test_apparent_pulse_period(self):
        binary_params = {
            'inclination': 0.5,
            'orbital_period': 3600,
            'start_phase': 0,
            'companion_mass': 1.0,
            'pulsar_mass': 1.4,
            'eccentricity': 0.1,
            'omega': 0.3
        }
        p_rest = 1
        time = 1000
        p_apparent = apparent_pulse_period(binary_params, p_rest, time)
        self.assertIsNotNone(p_apparent)

    def test_generate_binary_pulsar(self):
        data = np.zeros((64, 1024), dtype=np.uint8)
        DM = 100
        tsamp = 0.000064
        foff = -0.09765625
        fch1 = 1500
        p_rest = 100
        binary_params = {
            'inclination': 0.5,
            'orbital_period': 3600,
            'start_phase': 0,
            'companion_mass': 1.0,
            'pulsar_mass': 1.4,
            'eccentricity': 0.1,
            'omega': 0.3
        }
        frb_params = {
            'frb_duration': 10,
            'frb_amplitude': 50
        }

        data_with_pulsar = generate_binary_pulsar(data, DM, tsamp, foff, fch1, p_rest, binary_params, **frb_params)

        self.assertIsNotNone(data_with_pulsar)
        self.assertEqual(data_with_pulsar.shape, data.shape)

    def test_generate_solitary_pulsar(self):
        data = np.zeros((64, 1024), dtype=np.uint8)
        DM = 100
        tsamp = 0.000064
        foff = -0.09765625
        fch1 = 1500
        p_rest = 100
        frb_params = {
            'frb_amplitude': 50
        }

        data_with_pulsar = generate_solitary_pulsar(data, DM, tsamp, foff, fch1, p_rest, **frb_params)

        self.assertIsNotNone(data_with_pulsar)
        self.assertEqual(data_with_pulsar.shape, data.shape)

if __name__ == '__main__':
    unittest.main()
