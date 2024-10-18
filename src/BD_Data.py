import numpy as np
import matplotlib.pyplot as plt

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
                    raw_data = int32_data.reshape(120000, 10)

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

    def display_peak(self, peak_center):
        """
        Displays a plot of a peak so that a user can determine which spike they want within the pea
        The return will be integrated over the interval spike selection to y = 1

        Parameters
            peak_center: int
                the location of the center of the peak
        
        Returns
            numpy array that contains the peak offset around 1 for the relevant meter

        """
        ## Get an interval around the center of the peak
        interval_start, interval_end = self.get_peak_bounds(peak_center)

        ## Get an array that represents the data in the peak for the relevant meter
        peak = self.get_peak_for_meter(interval_start, interval_end)

        ## Plot peak so that user can select an x 
        _, ax = plt.subplots()

        ax.plot(peak[interval_start:interval_end])

        #plt.xlim(interv0al_start, interval_end)
        
        plt.show()
        return peak
    
    ## Returns the start and end of the interval that the peak is 
    def get_peak_bounds(self, peak_center):
        """
        Gets the bounds for a peak.

        Parameters
            peak_center: int
                the location of the center of the peak
        
        Return
            int:
                the start of the interval
            int:
                the end of the interval

        """
                
        if peak_center <= 1500:
            return 1, peak_center + 500
        elif peak_center > 119500:
            return peak_center - 1500, 120000
        else:
            return peak_center - 1500, peak_center + 500

    ## Gets offset for a meter based on the meter and end value
    def get_meter_offset(self, meter, start, end):
        """
        Gets the meter offset for a specific meter

        Parameters
            meter: numpy array
                the numpy array which the offset will be calculated off of
            end: int
                the end value of the interval
        
        Return
            float:
                the offset for a specific meter's data and interval

        """
        # if at the end of the graph return values before the interval
        if end + 2000 > len(meter):
            return np.mean(meter[start - 2000:start - 1000])

        return np.mean(meter[end + 1000:end + 2000])
        
    ## Gets a column (meter) from the matrix based off the magnitude of the peak, centers the column around 0
    def get_peak_for_meter(self, start, end):
        """
        Gets the peak that can be displayed and integrated.

        Parameters
            start: int
                the start of the interval to display
            end: int
                the end of the interval to display
        
        Return
            numpy array:
                an array of offset data for a specific meter over an interval

        """

        ## Returns the max value in the 250g array within the interval
        max_250 = np.max(self.g250g[start:end])

        ## Returns the max value in the 250g array within the interval
        max_200 = np.max(self.g200g[start:end])

        ## Based on the max value of the peak determine which column to use and how to offset the column
        if (max_250 > 200):
            meter_to_analyze = self.g250g.copy()
        elif (max_200 > 50):
            meter_to_analyze = self.g200g.copy()
        elif (max_200 > 18):
            meter_to_analyze = self.g50g.copy()
        elif (max_200 > 1.7):
            meter_to_analyze = self.g18g.copy()
        else:
            meter_to_analyze = self.g2g.copy()

        ## Get the offset for the specific meter
        offset = self.get_meter_offset(meter_to_analyze, start, end)

        ## Apply the offset to the data and return
        return meter_to_analyze - offset

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

    def plot_initial_data(self):
        plt.figure(figsize=(15,15))
        
        plt.plot(self.g2g, linestyle='-', label="g2g")
        plt.plot(self.g18g, linestyle='-', label="g18g")
        plt.plot(self.g50g, linestyle='-', label="g50g")
        plt.plot(self.gX55g, linestyle='-', label="gx55g")
        plt.plot(self.gY55g, linestyle='-', label="gy55g")
        plt.plot(self.g250g, linestyle='-', label="g250g")
        plt.legend(loc='upper right')

        plt.xlabel('Steps', fontsize=15)
        plt.ylabel('Deceleration (g)', fontsize=15)
        plt.title('Initial Data Visualization', fontsize=15)
        plt.show()