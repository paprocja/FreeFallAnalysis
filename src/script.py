import numpy as np

# Function to open the file dialog and read the selected file
def select_and_read_file(file_path):

    # Check if the user selected a file
    if file_path:
        try:
            # Open and read the file
            with open(file_path, 'rb') as file:
                data = np.fromfile(file, dtype=np.uint8)  # Read data as unsigned 8-bit integers (bytes)
                
                # Reshape the data to handle 3 bytes per sample
                data = data.reshape(-1, 3)
            
                # Convert the 24-bit chunks to signed 32-bit integers
                # By shifting and combining the 3 bytes to create a 32-bit signed integer
                int32_data = (data[:, 0].astype(np.int32) << 16) | (data[:, 1].astype(np.int32) << 8) | data[:, 2].astype(np.int32)

                # Handle sign extension for negative values (if the 24-bit number is negative)
                int32_data[int32_data >= 2**23] -= 2**24

                # Reshape the data into the desired matrix
                F = int32_data.reshape(120000, 10)

                # Write output to csv file in output directory
                np.savetxt("../output/F_Matrix.csv", F, delimiter=",")

                print(F)
                
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        print("No file selected")



if __name__ == "__main__":
    select_and_read_file()
