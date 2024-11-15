import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# Represents a peak where the penetrometer has hit the ground
class Peak:
    #peak_center is the x cordinate of the center of the peak
    #BD is a bd_data object that the peak is within
    def __init__(self, peak_num, BD):
        """
        Constructor for Peak object

        Parameters
        ----------
        peak_center: int
            x value of the highest point of the peak
        BD: BD_Data
            BD data object from which the peak comes from

        Assigns
        -------
        self.peak_center: int
            y-value or max height of peak
        self.start: int
            x-value for start of peak within BD_data object
        self.end: int
            x-value for end of peak within BD_data object

        self.data, self.g250g, self.g200g, self.g50g, self.g18g, self.g2g:
            Cut copies of accelerometer/raw data of peak from BD_Data
        """
        # grabs max height of peak
        self.peak_center = BD.peaks[peak_num]
        
        # determines bounds of peak to copy data from
        if self.peak_center <= 1500:
            # Peak is at the beginning of the file
            self.start = 0
            self.end = self.peak_center + 500
        elif self.peak_center > 119500:
            # Peak is in the middle of file
            self.start = self.peak_center - 1500
            self.end = BD.data.size
        else:
            # Peak is close to the end of file
            self.start = self.peak_center - 1500
            self.end = self.peak_center + 500

        # performs all calculations available at time of creation
        self._copy_from_BD_data(BD)    
        self._set_peak(BD)
        self._find_end_of_drop()

        # defines values to be used later for potential storage / saving objects
        self.decelleration = None
        self.velocity = None
        self.depth = None
        self.selected_spike = None

    def _copy_from_BD_data(self, BD):
        # copies data from the BD_data object
        self.data = BD.data[self.start:self.end].copy()
        self.g250g = BD.g250g[self.start:self.end].copy()
        self.g200g = BD.g200g[self.start:self.end].copy()
        self.g50g = BD.g50g[self.start:self.end].copy()
        self.g18g = BD.g18g[self.start:self.end].copy()
        self.g2g = BD.g2g[self.start:self.end].copy()
        # Grabs the x,y values of the peak. 
        # Offsets the x value to be in terms of the peak.
        self.peak_height = BD.g250g[self.peak_center].copy()
        self.peak_center = self.peak_center - self.start

    def _set_peak(self, BD):
        """
        Sets the peak that can be displayed and integrated.
        A column (meter) from the matrix based off the magnitude of the peak, centers the column around 0

        Parameters
        ----------
        BD: BD_Data
            The data the peak comes from
        
        Assigns
        -------
        self.peak: numpy array
            an array of offset data for a specific meter over an interval
        """

        # Returns the max value in the 250g array within the interval
        max_250 = np.max(self.g250g)

        # Returns the max value in the 250g array within the interval
        max_200 = np.max(self.g200g)

        # Based on the max value of the peak determine which accelerometer to use for the peak
        if (max_250 > 200):
            spliced_meter = self.g250g.copy()
            meter_to_analyze = BD.g250g.copy()
        elif (max_200 > 50):
            spliced_meter = self.g200g.copy()
            meter_to_analyze = BD.g200g.copy()
        elif (max_200 > 18):
            spliced_meter = self.g50g.copy()
            meter_to_analyze = BD.g50g.copy()
        elif (max_200 > 1.7):
            spliced_meter = self.g18g.copy()
            meter_to_analyze = BD.g18g.copy()
        else:
            spliced_meter = self.g2g.copy()
            meter_to_analyze = BD.g2g.copy()

        # Stores the peak as an array offset for integration
        offset = self._get_meter_offset(meter_to_analyze)        
        self.peak = spliced_meter - offset

    def _get_meter_offset(self, meter):
        """
        Gets the y-value offset for a particular meter.
        The values need to be offset so the peak starts to increase around 0 for integration

        Parameters
        ----------
        meter: numpy array
            the numpy array which the offset will be calculated off of

        Return
        ------
        float
            the y offset for a specific meter's data and interval
        """

        if self.end + 2000 > len(meter):
            # if at the end of the graph, return values before the interval
            return np.mean(meter[self.start - 2000:self.start - 1000])
        return np.mean(meter[self.end + 1000:self.end + 2000])

    def _find_end_of_drop(self):
        """
        TODO 
        Need see if this code can be cleaned up. Right now this is just the
        same functinoality that the matlab script had for `findent2`. 
        Not sure if its accounting for some edge case but seems extra, looks like
        we could just use num1? We're looping from peak to end of it, so its only 
        going down?
        """
        for i in range(self.peak_center, self.end):
            if self.peak[i] <= 0:
                num1 = i
                num2 = i-1
                break
        self.end_of_drop = num1 if abs(num1) < abs(num2) else num2

    def _integrate_acceleration(self, selected_spike):
        """
        Uses accelerometer data and selection of the spike to integrate for velocity and depth

        Parameters
        ----------
        selected_spike: int
            x value for start of peak from graph

        """
        # splices deceleration from peak_center to end_of_drop in peak
        decel = self.peak[selected_spike:self.end_of_drop]
        decel_ms2 = np.array([d*9.81 for d in decel])
        self.decelleration = decel_ms2
        # gets time incremenets for integration
        time = np.array([i * .005 for i in range(len(decel_ms2))])
        # integrates deceleration over time for velocity
        vel = integrate.cumulative_trapezoid(time, decel_ms2)

        # TODO from matlab script: "find a better way to do this, vel should be near 0" in reference to the next 2 lines
        max_vel = max(vel)
        vel_corrected = vel - max_vel
        self.velocity = vel_corrected

        # need to offset time by 1 because somehow velocity loses a value with integration?
        # integrates velocity over time for depth
        self.depth = integrate.cumulative_trapezoid(time[:len(time)-1], self.velocity)

    def display_peak(self, fig_manager):
        """
        Displays the peak using the figure manager.
        """
        def plot(ax):
            ax.plot(self.peak)
            ax.plot(self.g2g)
            ax.scatter(self.end_of_drop, self.peak[self.end_of_drop], marker='x', label='End of drop', color='black')
            ax.set_title(f"Peak at {self.peak_center}")
            ax.set_xlabel("Sample")
            ax.set_ylabel("Value")
        
        fig_manager.display(plot)


    def display_decel_vel_dep(self, fig_manager,  selected_spike=None):
        """
        Displays the deceleration, velocity, and depth data in one plot
        TODO incorporate this with QSBC QDYN stuff

        Parameters
        ----------
        selected_spike: int
            Optional x value for start of peak from graph. 
            If not provided, assumes integration has already occurred
        """
        if selected_spike is not None:
                self._integrate_acceleration(selected_spike)
        
        def plot(ax):
            end = self.depth[-1]
            ax.plot(self.decelleration, np.append(self.depth, [end, end]), label='decel')
            ax.plot(self.velocity, np.append(self.depth, [end]), label='vel')
            ax.legend(loc='upper right')

        fig_manager.display(plot)

    def is_valid_spike(self, spike):
        """
        TODO
        Currently everything is a valid spike. Ideas:
        - Check spike is not cut off by start/end of file
        - If not a good selection, provide suggestions
        """
        return True
    
    
