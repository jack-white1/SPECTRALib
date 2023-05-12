import struct
import numpy as np
import matplotlib.pyplot as plt
import os
from spectralib.frb import calculate_dispersion_offsets

def plot_and_save(data, title, file_name):
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, aspect="auto", cmap="plasma", origin="lower")
    ax.set_title(title)
    plt.colorbar(im, ax=ax)
    ax.set_ylim(ax.get_ylim()[::-1])  # Flip the y-axis
    plt.xlabel("Time (bins)")
    plt.ylabel("Frequency (bins)")
    plt.tight_layout()
    plt.savefig(file_name, dpi=300)  # Save as a high-quality PNG image
    plt.close(fig)  # Close the figure to free up memory

def dedisperse_filterbank_data_to_timeseries(data, DM, tsamp, foff, fch1):
    dedispersed_data = dedisperse_filterbank_data(data, DM, tsamp, foff, fch1)
    timeseries = np.sum(dedispersed_data, axis=0)
    return timeseries

def dedisperse_filterbank_data(data, DM, tsamp, foff, fch1):
    nchans, nsamp = data.shape
    dedispersed_data = np.zeros_like(data)
    offsets = calculate_dispersion_offsets(DM, fch1, foff, nchans, tsamp)

    for i in range(nchans):
        offset = int(offsets[i])
        dedispersed_data[i] = np.roll(data[i], -offset)

    return dedispersed_data


def create_filterbank(data,output_filename, metadata):
    """
    Create a filterbank file with the given data and metadata.

    :param output_filename: The output filterbank file path.
    :param data: The data to be included in the filterbank file.
    :param metadata: The metadata to be included in the filterbank file.
    """
    print(output_filename)
    with open(output_filename, 'wb') as f:
        # Write the header start marker
        # Use '<I' for little-endian unsigned int encoding
        f.write(struct.pack('<I', len('HEADER_START')))
        f.write(b'HEADER_START')
        
        # Write metadata key-value pairs
        for key, value in metadata.items():
            #print("Writing key: '", key, "' value: '", value, "' to file.")
            # Encode and write the length of the metadata key
            f.write(struct.pack('<I', len(key)))
            # Encode and write the metadata key as bytes
            f.write(key.encode())
            
            # Check the type of the metadata value and encode it accordingly
            if isinstance(value, str):
                # Encode and write the length of the string value
                f.write(struct.pack('<I', len(value)))
                # Encode and write the string value as bytes
                f.write(value.encode())
            elif isinstance(value, int):
                # Encode and write the integer value as little-endian signed int
                f.write(struct.pack('<i', value))
            elif isinstance(value, float):
                # Encode and write the float value as little-endian double precision float
                f.write(struct.pack('<d', value))
            else:
                raise ValueError(f"Unsupported data type for key '{key}': {type(value)}")
                
        # Write the header end marker
        f.write(struct.pack('<I', len('HEADER_END')))
        f.write(b'HEADER_END')
        
        # Write the signal data
        # tofile() writes the array to a binary file in a machine-specific format
        data = data.astype(np.uint8)
        data = data.transpose()
        #data = np.fliplr(data)
        #data = np.flipud(data)
        data.tofile(f)

def read_filterbank_data(file_path, header_params, header_len):
    nchans = header_params["nchans"]
    nbits = header_params["nbits"]

    # Validate that the data format is supported
    if nbits not in [8, 16, 32]:
        raise ValueError(f"Unsupported data format: {nbits}-bit")

    # Calculate the size of one sample in bytes
    sample_size = nbits // 8

    # Open the file and seek to the end of the header
    with open(file_path, "rb") as file:
        file.seek(header_len)

        # Read the entire file into a 1D NumPy array
        data = np.fromfile(file, dtype=np.uint8 if nbits == 8 else (np.uint16 if nbits == 16 else np.uint32))

    # Calculate the number of time samples
    nsamples = len(data) // (nchans * sample_size)

    # Reshape the data into a 2D NumPy array
    data_2d = data.reshape((nsamples, nchans))
    data_2d = data_2d.transpose()
    #data_2d = np.flipud(data_2d)

    return data_2d

def read_filterbank_header(file_path):
    def get_string(file):
        nchar = struct.unpack("<i", file.read(4))[0]

        if nchar > 80 or nchar < 1:
            file.seek(-3, os.SEEK_CUR)
            string_data = file.read(4)
            print(f"Error occurred. Raw bytes: {string_data}")
            return "ERROR", 1

        string_data = file.read(nchar)
        string = string_data.decode("utf-8", "ignore")
        return string, nchar + 4

    def read_int(file):
        return struct.unpack("<i", file.read(4))[0], 4

    def read_double(file):
        return struct.unpack("<d", file.read(8))[0], 8

    header_params = {}

    with open(file_path, "rb") as file:
        param_name, nbytes = get_string(file)

        if param_name != "HEADER_START":
            file.seek(0)
            return header_params, 0
        totalbytes = nbytes

        while True:
            param_name, nbytes = get_string(file)
            #print("param_name: ", param_name, " nbytes: ", nbytes)
            totalbytes += nbytes

            if param_name == "HEADER_END":
                break

            if param_name in ["rawdatafile", "source_name"]:
                string_value, nbytes_read = get_string(file)
                header_params[param_name] = string_value
                totalbytes += nbytes_read

            elif param_name in ["az_start", "za_start", "src_raj", "src_dej", "tstart", "tsamp", "period", "fch1", "foff", "nchans", "telescope_id", "machine_id", "data_type", "ibeam", "nbeams", "nbits", "barycentric", "pulsarcentric", "nbins", "nifs", "npuls", "refdm"]:
                value, nbytes_read = read_double(file) if param_name in ["az_start", "za_start", "src_raj", "src_dej", "tstart", "tsamp", "period", "fch1", "foff"] else read_int(file)
                header_params[param_name] = value
                totalbytes += nbytes_read

            else:
                print(f"Unknown parameter: {param_name}")
                return header_params, totalbytes

    return header_params, totalbytes

def read_filterbank(file_path):
    header_params, header_len = read_filterbank_header(file_path)
    data = read_filterbank_data(file_path, header_params, header_len)
    return data, dict(header_params)


def show_filterbank(data, title='Filterbank'):
    """
    Display the filterbank data as a 2D image.

    :param data: The 2D array containing filterbank data.
    :param title: Optional title for the plot.
    """
    plt.figure()
    plt.imshow(data, aspect='auto', cmap='viridis')
    plt.colorbar()
    plt.title(title)
    plt.xlabel('Time Samples')
    plt.ylabel('Frequency Channels')
    plt.show()

