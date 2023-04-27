import unittest
import numpy as np
from spectralib.frb import generate_pulse, calculate_dispersion_offsets

class TestFRB(unittest.TestCase):
    def test_calculate_dispersion_offsets(self):
        DM = 100
        tsamp = 0.001
        foff = -0.1
        fch1 = 1000
        nchans = 512

        offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)
        self.assertEqual(len(offsets), nchans)

    def test_generate_pulse(self):
        nchans, nsamp = 100, 10000
        data = np.random.normal(0,18,size=(nchans, nsamp))+127
        DM = 100
        tsamp = 0.001
        foff = -0.5
        fch1 = 1500
        pulse_params = {
            'pulse_start_index': 1,
            'pulse_duration': 10,
            'pulse_amplitude': 50
        }
        datacopy = data.copy()
        data_with_frb = generate_pulse(data, DM, tsamp, foff, fch1, **pulse_params)

        self.assertIsNotNone(data_with_frb)
        self.assertEqual(data_with_frb.shape, data.shape)
        self.assertNotEqual(np.sum(datacopy), np.sum(data_with_frb))

if __name__ == '__main__':
    unittest.main()
