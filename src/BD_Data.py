import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class BD_Data:
    def __init__(self, file_path, bdid=8):
        self.set_data_from_file(file_path)
        self.set_accelerometer_data_from_bdid(bdid)
        pass

    def set_data_from_file(self, file_path):
        """
        Retrieves data from a raw binary, errors on other file types        
        Parameters
        ---
        file_path: str
            Location of .csv or .bin file

        Assigns
        ---
        self.data: 32 bit integer data
        """
        if file_path:
            if '.csv' in file_path:
                raise Exception('Not yet implemented')
            elif '.bin' in file_path:
            # read data from .bin
                with open(file_path, 'rb') as f:
                    data = np.fromfile(f, dtype=np.uint8)  # Read data as unsigned 8-bit integers (bytes)
                
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

                    self.data = raw_data
            else:
                raise Exception(f"Error: {file_path} is not a .csv or .bin file. Please try again!")
        else:
            raise Exception(f'Error: please select a file!')

    def set_accelerometer_data_from_bdid(self, bdid):
        """
        Equivalent to gdata from BD_Inwater.m, converts data into SI units based on
        the blueDrop number and its associated calibration constants as well as the 
        raw data

        Parameters
        ---
        bdid: int
            blueDrop ID number
        
        Assisgns
        ---
        self.g2g
        self.g18g 
        self.g50g 
        self.g200g 
        self.gX55g
        self.gY55g
        self.g250g
        self.ppm 
        """
        match bdid:
            case 1:
                # calibration factors from July 2020
                self.g2g = ((self.data[:, 2] - 42590.9) / 1626361.1)
                self.g18g = ((self.data[:, 3] - 44492.9) / 161125.5)
                self.g50g = ((self.data[:, 4] - 171656.1) / 64020.3)
                self.ppm = ((self.data[:, 5] + 31776.1) / 20679.7)
                self.g200g = (((self.data[:, 6] - 723404.8) / 32209.7))
                self.gX55g = ((self.data[:, 7] - 54881.1) / 64858.6)
                self.gY55g = ((self.data[:, 8] - 28735.5) / 63839.9)
                self.g250g = ((self.data[:, 9] + 13299.7) / 13697.1)
                self.g2g = np.delete(self.g2g, -1)
                self.g2g = np.insert(self.g2g, 0, 1)
                self.g200g = np.delete(self.g200g, -1)
                self.g200g = np.insert(self.g200g, 0, 1)
                self.g18g = np.delete(self.g18g, -1)
                self.g200g = np.delete(self.g200g, -1)
                self.g200g = np.insert(self.g200g, 0, 1)
                self.ppm *= 6.89475729  # Convert to kPa
            case 2:
                # calibration factors from Aug 26, 2021
                self.g2g = ((self.data[:, 2] + 37242.2) / 1639250.2)
                self.g18g = ((self.data[:, 3] - 26867.0) / 160460.5)
                self.g50g = ((self.data[:, 4] - 213923.3) / 64080.7)
                self.ppm = ((self.data[:, 5] + 55518.9) / 18981.7)
                self.g200g = ((self.data[:, 6] - 171448.6) / 30334.2)
                self.gX55g = ((self.data[:, 7] - 54242.6) / 64767.7)
                self.gY55g = ((self.data[:, 8] - 40574.2) / 66343.1)
                self.g250g = ((self.data[:, 9] - 40614.9) / 13654.6)
                self.ppm *= 6.89475729  # Convert to kPa
                
            case 3:
                # calibration factors from July 2019
                self.g2g = ((self.data[:, 2] - 38285.6) / 1615800.9)
                self.g18g = ((self.data[:, 3] + 13738) / 163516.8)
                self.g50g = ((self.data[:, 4] - 238520.6) / 63666)
                self.ppm = ((self.data[:, 5] - 139040.1) / 20705)
                self.g200g = (((self.data[:, 6] + 12142.6) / 27751.9))
                self.gX55g = ((self.data[:, 7] - 90237) / 65351.5)
                self.gY55g = ((self.data[:, 8] - 57464.2) / 65545.5)
                self.g250g = ((self.data[:, 9] - 40420.3) / 13636.9)
                self.g2g = np.delete(self.g2g, -1)
                self.g2g = np.insert(self.g2g, 0, 1)
                self.g200g = np.delete(self.g200g, -1)
                self.g200g = np.insert(self.g200g, 0, 1)
                self.g18g = np.delete(self.g18g, -1)
                self.g200g = np.delete(self.g200g, -1)
                self.g200g = np.insert(self.g200g, 0, 1)
                self.ppm *= 6.89475729  # Convert to kPa
            case 8:
                # calibration factors from Feb 2023
                self.g2g = ((self.data[:, 2]) + 48961.0) / 1629804.6
                self.g18g = ((self.data[:, 3] - 45301.2) / 160611.4)
                self.g50g = ((self.data[:, 4] - 208714.3) / 63704.3)
                self.ppm = ((self.data[:, 5] - 96576.0) / 19436.3)
                self.g200g = (((self.data[:, 6] - 49688.7) / 32695.6))
                self.gX55g = ((self.data[:, 7] - 52767.2) / 64099.0)
                self.gY55g = ((self.data[:, 8] - 28735.5) / 63839.9)
                self.g250g = ((self.data[:, 9] - 46439.9) / 13677.9)
                self.ppm *= 6.89475729  # Convert to kPa

            case _:
                raise Exception(f'Unknown Blue Drop #{bdid}')


    def findpeaks(self):
        """
        Finds peaks within g250g! Similar to matlab function
        Peaks increase by a height of 5 and are at least 
        "1 second" away from another (2000 distance)

        Parameters
        ----------
        None

        Returns
        -------
        peaks: List[int]
            X values of each peak
        heights: List[int]
            Y values of each peak
        """
        peaks, heights = find_peaks(self.g250g, height=5, distance=2000)
        if len(peaks) > 0:
            heights = heights['peak_heights']
        else:
            heights = []
        return peaks, heights
    
    def display_initial_data(self, peaks, heights, num_peaks):
        """
        Displays initial data and peaks

        Parameters
        ----------
        peaks: List[int]
            x values of peaks
        heights: List[int]
            y values of peaks
        num_peaks: int
            len(peaks) as it is called elsewhere        
        """
        # establish plot and axis
        fig, ax = plt.subplots(figsize=(12, 6))

        # plot vertical accelerometer data
        ax.plot(self.g2g, linestyle='-', linewidth=.5, label="g2g", color='green')
        ax.plot(self.g18g, linestyle='-', linewidth=.5, label="g18g", color='red')
        ax.plot(self.g50g, linestyle='-', linewidth=.5, label="g50g", color='blue')
        ax.plot(self.g250g, linestyle='-', linewidth=.5, label="g250g", color='purple')
        # plot peaks as stars
        ax.scatter(peaks, heights, marker='*', label='peaks', color='black')

        # label peaks with selection numbers
        for i, txt in enumerate(range(1, num_peaks+1)):
            plt.annotate(txt, (peaks[i], heights[i]), xytext=(5,5), textcoords='offset points',
                            ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
                        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

        # label legend, axis, title
        ax.legend(loc='upper right')
        ax.set_xlabel('Steps', fontsize=15)
        ax.set_ylabel('Deceleration (g)', fontsize=15)
        ax.set_title('Initial Data Visualization', fontsize=15)
        plt.tight_layout()
        plt.show()
    

    def save_data(self, file_path):
        """
        Exports the raw data as a .csv
        """
        np.savetxt(file_path, self.data, delimiter=",")

    def output(self):
        print(f"{self.data = }")
        print(f'{self.g2g = }')
        print(f'{self.g18g = }')
        print(f'{self.g50g = }') 
        print(f'{self.g200g = }') 
        print(f'{self.gX55g = }')
        print(f'{self.gY55g = }')
        print(f'{self.g250g = }')
        print(f'{self.ppm = }')
