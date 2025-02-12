import numpy as np
import os

def stitch_files(file_paths):
    """
    Accepts a list of binary file paths representing 10x120,000 matrices.
    Returns the file path to a new file concatenating the previous in order of file names.
    Only called with > 1 entry in file_paths.
    """
    file_paths = sort_by_hex(file_paths)
    matrices = []
    for file in file_paths:
        matrices.append(np.fromfile(file, dtype=np.uint8))
    
    # Creates a temporary directory if it doesn't already exist
    try:
        os.mkdir('./temp')
    except OSError as e:
        print(f'./temp/ diectory already exists.')

    # Grab the file names without their parent directories
    file_names = [path.split('/')[-1] for path in file_paths]

    # Combine file names to create a new file name.
    new_file_name = '-'.join([name[:-4] for name in file_names])
    
    # If the file name is too long, shorten it to "first-to-last.bin"
    MAX_PATH = 260 # On windows systems, there is a hard limit to the number of characters that can go in a file name.
    if len(new_file_name) + len(os.getcwd()) > MAX_PATH - 4: # -4 for .bin suffix
        new_file_name = f'{file_names[0][:-4]}-to-{file_names[-1][:-4]}'
    file_path = f'./temp/{new_file_name}.bin'

    # concatenate the matrices to extend the columns to one another
    final_matrix = np.concatenate(matrices, axis=0)
    
    # Write to file in the ./temp/ directory
    final_matrix.tofile(file_path, sep="")
    print(f"binary_utils.py: Combined file created at {file_path}.")
    print('WARNING: If you have uploaded multiple files that are not chronologically associated, '
        'then this analysis will have undefined behavior. Please only upload files that were recorded together. '
        'The program will automatically sort these files into the correct order (ascending based on the hexidecimal tag in the file name).')
    return file_path

PREFIX = 'bLog' # Represents the file prefix before the hexidecimal number. Is likely 'bLog' for everything, but can be changed just in case.
def validate_penetrometer_file(file_path):
    """
    Validates a penetrometer file by checking for PREFIX and '.bin'.
    Also checks against .csv.
    Raises an Exception on error.
    """
    if '.csv' in file_path:
        raise Exception(f'Error: Support for csv is not yet implemented.\nFile: {file_path} will not work.\nPlease select .bin files.')
    if not '.bin' in file_path:
        raise Exception(f"Error: {file_path} is not a .csv or .bin file. Please try again!")
    if not PREFIX in file_path:
        raise Exception(f"{file_path} doesn't contain {PREFIX}. Are you sure this is binary penetrometer data?")

def sort_by_hex(file_paths):
    """
    Takes an iterator of file paths, presumably all with .bin in the file name. 
    Returns a list of the file paths sorted by their hexidecimal number following PREFIX
    Prone to errors if an invalid file passes the validate_penetrometer_file() check.
    """
    num_path = [] # list to map hexidecimal integer -> file path
    for file_path in file_paths:
        validate_penetrometer_file(file_path)
        file = file_path.split("/")[-1] # parse out absolute path to only have the file name
        num = int(file.split('.')[0][len(PREFIX):], 16) # remove .bin extension, then grab characters after PREFIX, then convert from hex string to integer 
        num_path.append((num, file_path)) # add (num, file_path) to list
    num_path.sort(key=lambda kv: kv[0]) # sort list based on the first value in the pair (the number)
    sorted_file_paths = [kv[1] for kv in num_path]
    return sorted_file_paths

def load_penetrometer_data(file_path):
    """
    Loads 10 columns of data from a raw binary penetrometer data file.
    Returns an np.int32 array representing the data.
    """
    validate_penetrometer_file(file_path)

    # converts tuple of files to single file, if only one file is selected
    data = np.fromfile(file_path, dtype=np.uint8)  # Read data as unsigned 8-bit integers (bytes)

    # Reshape the data to handle 3 bytes per sample
    data = data.reshape(-1, 3)

    # Convert the 24-bit chunks to signed 32-bit integers
    # By shifting and combining the 3 bytes to create a 32-bit signed integer
    int32_data = (data[:, 0].astype(np.int32) << 16) | (data[:, 1].astype(np.int32) << 8) | data[:, 2].astype(np.int32)

    # Handle sign extension for negative values (if the 24-bit number is negative)
    int32_data[int32_data >= 2**23] -= 2**24

    # Reshape the data into the desired matrix
    array_size = (int)(int32_data.size / 10)
    raw_data = int32_data.reshape(array_size, 10)
    return raw_data