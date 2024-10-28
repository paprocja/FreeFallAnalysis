import numpy as np
import matplotlib.pyplot as plt

# Represents a peak where the penetrometer has hit the ground
class Peak:
    #peak_center is the x cordinate of the center of the peak
    #BD is a bd_data object that the peak is within
    def __init__(self, peak_center, BD):
        self.peak_center = peak_center
        self.BD = BD
        self.start = 0
        self.end = 0
        pass

    def display_peak(self):
        """
        Displays a plot of a peak so that a user can determine which spike they want within the pea
        The return will be integrated over the interval spike selection to y = 1
        
        Returns
        -------
            numpy array that contains the peak offset around 1 for the relevant meter

        """
        ## Get an interval around the center of the peak
        self.get_peak_bounds()

        ## Get an array that represents the data in the peak for the relevant meter
        peak = self.get_peak_for_meter()

        ## Plot peak so that user can select an x 
        _, ax = plt.subplots()

        ax.plot(peak[self.start:self.end])

        #plt.xlim(interv0al_start, interval_end)
        
        plt.show()
        return peak
    
    ## Returns the start and end of the interval that the peak is 
    def get_peak_bounds(self):
        """
        Gets the bounds for a peak.

        Parameters
        ----------
        peak_center: int
            the location of the center of the peak
        
        Returns
        -------
        int:
            the start of the interval
        int:
            the end of the interval

        """
        if self.peak_center <= 1500:
            self.start = 1
            self.end = self.peak_center + 500
        elif self.peak_center > 119500:
            self.start = self.peak_center - 1500
            self.end = self.BD.data.size
        else:
            self.start = self.peak_center - 1500
            self.end = self.peak_center + 500

    ## Gets offset for a meter based on the meter and end value
    def get_meter_offset(self, meter):
        """
        Gets the meter offset for a specific meter

        Parameters
        ----------
        meter: numpy array
            the numpy array which the offset will be calculated off of
        end: int
            the end value of the interval
        
        Return
        ------
        float:
            the offset for a specific meter's data and interval

        """
        # if at the end of the graph return values before the interval
        if self.end + 2000 > len(meter):
            return np.mean(meter[self.start - 2000:self.start - 1000])

        return np.mean(meter[self.end + 1000:self.end + 2000])
        
    ## Gets a column (meter) from the matrix based off the magnitude of the peak, centers the column around 0
    def get_peak_for_meter(self):
        """
        Gets the peak that can be displayed and integrated.

        Parameters
        ----------
        start: int
            the start of the interval to display
        end: int
            the end of the interval to display
        
        Returns
        -------
        numpy array:
            an array of offset data for a specific meter over an interval

        """

        ## Returns the max value in the 250g array within the interval
        max_250 = np.max(self.BD.g250g[self.start:self.end])

        ## Returns the max value in the 250g array within the interval
        max_200 = np.max(self.BD.g200g[self.start:self.end])

        ## Based on the max value of the peak determine which column to use and how to offset the column
        if (max_250 > 200):
            meter_to_analyze = self.BD.g250g.copy()
        elif (max_200 > 50):
            meter_to_analyze = self.BD.g200g.copy()
        elif (max_200 > 18):
            meter_to_analyze = self.BD.g50g.copy()
        elif (max_200 > 1.7):
            meter_to_analyze = self.BD.g18g.copy()
        else:
            meter_to_analyze = self.BD.g2g.copy()

        ## Get the offset for the specific meter
        offset = self.get_meter_offset(meter_to_analyze)

        ## Apply the offset to the data and return
        return meter_to_analyze - offset

    def is_valid_spike(self, spike):
        return True