import numpy as np
from scipy.signal import find_peaks
from binary_utils import stitch_files, load_penetrometer_data

class BD_Data:
    def __init__(self, file_paths, bdid=8):
        self.number_peaks = 0
        self.peaks = []
        self.heights = []
        self.set_data_from_file(file_paths)
        self.set_accelerometer_data_from_bdid(bdid)
        self.findpeaks()
        pass

    def set_data_from_file(self, file_paths):
        """
        Retrieves data from a raw binary 
        Parameters
        ---
        file_path: str
            Location of .csv or .bin file

        Assigns
        ---
        self.data: 32 bit integer data
        """
        # Checks file_paths tuple for multiple files and stitches to 1 accordingly
        num_files = len(file_paths)
        if num_files > 1:
            # if more than 1 file
            file_path = stitch_files(file_paths)
        elif num_files == 1:
            # if only 1 file, convert from single entry tuple to a string by extracting the first value
            file_path = file_paths[0]
        else:
            # Should be impossible due to the Windows file dialog requiring at least 1 file, but here for good measure
            raise Exception("Error: Please upload a file!")

        # read data from .bin
        self.data = load_penetrometer_data(file_path)

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

                # THE MATLAB SAID THIS WASN'T IMPORTANT. IT WAS.
                self.g2g = np.insert(self.g2g, 0, 1)
                self.g200g = np.insert(self.g200g, 0, 1)
                self.g18g = np.insert(self.g18g, 0, 1)

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
        """
        peaks, heights = find_peaks(self.g250g, height=5, distance=2000)
        if len(peaks) > 0:
            self.heights = heights['peak_heights']
            self.peaks = peaks
            self.number_peaks = len(peaks)
    
    def is_valid_peak(self, selected_peak):
        """
        Returns if a selected peak is within the range of peaks.

        Parameters
        ----------
        selected_peak: int
        The peak input by a user that needs to be validated
        """
        if selected_peak - 1 in range(0, self.number_peaks):
            return True
        else:
            return False


    def display_initial_data(self, fig_manager):
        """
        Displays initial data and peaks using the figure manager.
        """
        def plot(ax):
            ax.plot(self.g2g, linestyle='-', linewidth=.5, label="2g", color='green')
            ax.plot(self.g18g, linestyle='-', linewidth=.5, label="18g", color='red')
            ax.plot(self.g50g, linestyle='-', linewidth=.5, label="50g", color='blue')
            ax.plot(self.g200g, linestyle='-', linewidth=.5, label="200g", color='brown')
            ax.plot(self.g250g, linestyle='-', linewidth=.5, label="250g", color='purple')
            ax.scatter(self.peaks, self.heights, marker='*', label='peaks', color='black')
            for i, txt in enumerate(range(1, self.number_peaks + 1)):
                ax.annotate(txt, (self.peaks[i], self.heights[i]), xytext=(5, 5), textcoords='offset points',
                            ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
            ax.legend(loc='upper right')
            ax.set_xlabel('Steps')
            ax.set_ylabel('Deceleration (g)')
            ax.set_title('Initial Data Visualization')

        fig_manager.display(plot, display_type='peak_selection')


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
