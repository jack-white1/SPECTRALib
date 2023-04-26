import sys
sys.path.append("..")

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
        self.metadata = {'source_name': 'G348-50', 'data_type': 1, 'nchans': 336, 'barycentric': 0, 'pulsarcentric': 0, 'tsamp': 0.00126646875, 'rawdatafile': '2017-04-16-22:16:47_0000000000000000.000000.00.fil', 'src_raj': 215057.8011944, 'az_start': 0.0, 'za_start': 0.0, 'nifs': 1, 'telescope_id': 7, 'nbits': 8, 'fch1': 1488.0, 'foff': -1.0, 'src_dej': -33242.295403568, 'tstart': 57859.96643286721, 'machine_id': 0}

        # Update the shape of the data array to match the metadata
        num_samples = 10
        self.data = np.random.randint(0, 256, size=(num_samples, self.metadata['nchans']), dtype=np.uint8)

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

        # Reshape the read_data before comparison
        num_samples = self.data.shape[0]
        read_data_reshaped = read_data.reshape((num_samples, self.metadata['nchans']))
        np.testing.assert_array_equal(self.data, read_data_reshaped, err_msg="Read data does not match expected data")

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
