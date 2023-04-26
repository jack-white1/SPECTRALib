import sys
sys.path.append("..")

import unittest
import numpy as np
from spectralib.frb import generate_frb, calculate_dispersion_offsets

class TestFRB(unittest.TestCase):
    def test_calculate_dispersion_offsets(self):
        DM = 100
        tsamp = 0.001
        foff = -0.1
        fch1 = 1000
        nchans = 512

        offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)
        self.assertEqual(len(offsets), nchans)

    def test_generate_frb(self):
        nchans, nsamp = 100, 10000
        data = np.random.normal(0,18,size=(nchans, nsamp))+127
        DM = 100
        tsamp = 0.001
        foff = -0.5
        fch1 = 1500
        frb_params = {
            'frb_start_index': 1,
            'frb_duration': 10,
            'frb_amplitude': 50
        }
        datacopy = data.copy()
        data_with_frb = generate_frb(data, DM, tsamp, foff, fch1, **frb_params)

        self.assertIsNotNone(data_with_frb)
        self.assertEqual(data_with_frb.shape, data.shape)
        self.assertNotEqual(np.sum(datacopy), np.sum(data_with_frb))

if __name__ == '__main__':
    unittest.main()
