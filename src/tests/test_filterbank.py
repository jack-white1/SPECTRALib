import os
import numpy as np
import unittest
from spectralib.filterbank import create_filterbank, read_filterbank, show_filterbank
import matplotlib.pyplot as plt



class TestFilterbank(unittest.TestCase):
    
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_file = os.path.join(current_dir, "ASKAP.fil")
        self.output_file = os.path.join(current_dir, "test_filterbank.fil")
        self.data, self.metadata = read_filterbank(self.input_file)

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_read_filterbank_header(self):
        read_data, read_metadata = read_filterbank(self.input_file)
        self.assertDictEqual(self.metadata, read_metadata)

    def test_create_and_read_filterbank(self):
        create_filterbank(self.data, self.output_file,  self.metadata)
        self.assertTrue(os.path.exists(self.output_file))

        read_data, read_metadata = read_filterbank(self.output_file)
        self.assertDictEqual(self.metadata, read_metadata)

        np.testing.assert_array_equal(self.data, read_data, err_msg="Read data does not match expected data")

    def test_show_filterbank(self):
        # Read the filterbank data from a file
        data, metadata = read_filterbank(self.input_file)
        
        try:
            # Attempt to display the data as a 2D image without showing it
            with plt.ioff():  # Turn off interactive mode
                show_filterbank(data)
        except Exception as e:
            self.fail(f"show_filterbank() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
