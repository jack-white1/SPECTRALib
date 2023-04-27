import unittest
import numpy as np
from spectralib.frb import generate_pulse, calculate_dispersion_offsets
from spectralib.pulsar import generate_binary_pulsar, generate_solitary_pulsar, apparent_pulse_period

class TestPulsar(unittest.TestCase):

    def test_apparent_pulse_period(self):
        binary_params = {
            'rest_period': 1,
            'inclination': 0.5,
            'orbital_period': 3600,
            'start_phase': 0,
            'companion_mass': 1.0,
            'pulsar_mass': 1.4,
            'eccentricity': 0.1,
            'omega': 0.3
        }
        time = 1000
        p_apparent = apparent_pulse_period(binary_params, time)
        self.assertIsNotNone(p_apparent)

    def test_generate_binary_pulsar(self):
        data = np.zeros((64, 1024), dtype=np.uint8)
        DM = 100
        tsamp = 0.000064
        foff = -0.09765625
        fch1 = 1500
        binary_params = {
            'rest_period': 100,
            'inclination': 0.5,
            'orbital_period': 3600,
            'start_phase': 0,
            'companion_mass': 1.0,
            'pulsar_mass': 1.4,
            'eccentricity': 0.1,
            'omega': 0.3
        }
        pulse_params = {
            'pulse_duration': 10,
            'pulse_amplitude': 50
        }

        data_with_pulsar = generate_binary_pulsar(data, DM, tsamp, foff, fch1, binary_params, **pulse_params)

        self.assertIsNotNone(data_with_pulsar)
        self.assertEqual(data_with_pulsar.shape, data.shape)

    def test_generate_solitary_pulsar(self):
        data = np.zeros((64, 1024), dtype=np.uint8)
        DM = 100
        tsamp = 0.000064
        foff = -0.09765625
        fch1 = 1500
        rest_period = 100
        pulse_params = {
            'pulse_amplitude': 50
        }

        data_with_pulsar = generate_solitary_pulsar(data, DM, tsamp, foff, fch1, rest_period, **pulse_params)

        self.assertIsNotNone(data_with_pulsar)
        self.assertEqual(data_with_pulsar.shape, data.shape)

if __name__ == '__main__':
    unittest.main()
