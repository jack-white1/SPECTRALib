import numpy as np
import unittest
from spectralib.rfi import generate_rfi, add_wandering_baseline

class TestRFI(unittest.TestCase):
    
    def setUp(self):
        nchans, nsamp = 10, 10
        self.data = np.random.normal(0,18,size=(nchans, nsamp))+127
    
    def test_generate_rfi(self):
        rfi_data = generate_rfi(self.data)
        self.assertEqual(self.data.shape, rfi_data.shape, "Data shapes don't match after RFI generation")
        self.assertNotEqual(np.sum(self.data), np.sum(rfi_data), "Data is not changed after RFI generation")

    def test_add_wandering_baseline(self):
        wanderingbaselineamplitude = 30
        wanderingbaselineperiod = 1000
        datacopy = self.data.copy()
        wb_data = add_wandering_baseline(self.data, wanderingbaselineamplitude=wanderingbaselineamplitude, wanderingbaselineperiod=wanderingbaselineperiod)
        self.assertEqual(self.data.shape, wb_data.shape, "Data shapes don't match after wandering baseline addition")
        self.assertNotEqual(np.sum(datacopy), np.sum(wb_data), "Data is not changed after wandering baseline addition")

if __name__ == '__main__':
    unittest.main()
