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
        self.decelleation_ms2 = None
        self.velocity = None
        self.depth = None
        self.selected_spike = None

    def _copy_from_BD_data(self, BD):
        # copies data from the BD_data object
        self.data = BD.data[self.start:self.end+1].copy()
        self.g250g = BD.g250g[self.start:self.end+1].copy()
        self.g200g = BD.g200g[self.start:self.end+1].copy()
        self.g50g = BD.g50g[self.start:self.end+1].copy()
        self.g18g = BD.g18g[self.start:self.end+1].copy()
        self.g2g = BD.g2g[self.start:self.end+1].copy()
        # Grabs the x,y values of the peak. 
        # Offsets the x value to be in terms of the peak.
        self.peak_height = BD.g250g[self.peak_center]
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
        offset = None
        if (max_250 > 200):
            spliced_meter = self.g250g.copy()
            meter_to_analyze = BD.g250g.copy()
        elif (max_200 > 50):
            spliced_meter = self.g200g.copy()
            meter_to_analyze = BD.g200g.copy()
        elif (max_200 > 18):
            spliced_meter = self.g50g.copy()
            meter_to_analyze = BD.g50g.copy()
            offset = np.mean(meter_to_analyze[self.end + 100:self.end + 201])
        elif (max_200 > 1.7):
            spliced_meter = self.g18g.copy()
            meter_to_analyze = BD.g18g.copy()
        else:
            spliced_meter = self.g2g.copy()
            meter_to_analyze = BD.g2g.copy()

        # Stores the peak as an array offset for integration
        if offset is None:
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

        if self.end + 2001 > len(meter):
            # if at the end of the graph, return values before the interval
            return np.mean(meter[self.start - 2000:self.start - 999])
        return np.mean(meter[self.end + 1000:self.end + 2001])

    def _find_end_of_drop(self):
        """
        TODO 
        Need see if this code can be cleaned up. Right now this is just the
        same functinoality that the matlab script had for `findent2`. 
        Not sure if its accounting for some edge case but seems extra, looks like
        we could just use num1? We're looping from peak to end of it, so its only 
        going down?
        """
        for i in range(self.peak_center, len(self.peak)):
            if self.peak[i] <= 0:
                num1 = i
                num2 = i-1
                break
        self.end_of_drop = num1 if abs(self.peak[num1]) < abs(self.peak[num2]) else num2

    def _integrate_acceleration(self, selected_spike):
        """
        Uses accelerometer data and selection of the spike to integrate for velocity and depth

        Parameters
        ----------
        selected_spike: int
            x value for start of peak from graph

        """
        # splices deceleration from peak_center to end_of_drop in peak
        decel = np.array(self.peak[selected_spike:self.end_of_drop + 1]) # +1 for inclusion (difference in MATLAB)
        self.decelleration = decel
        self.decelleation_ms2 = decel * 9.81
        
        # integrates deceleration over time (.0005 seconds per record) for velocity
        vel = integrate.cumulative_trapezoid(self.decelleation_ms2, dx=.0005, initial=0)

        # TODO from matlab script: "find a better way to do this, vel should be near 0" in reference to the next 2 lines
        max_vel = np.max(vel)
        vel_corrected = max_vel - vel
        self.velocity = vel_corrected

        # integrates velocity over time for depth
        self.depth = integrate.cumulative_trapezoid(self.velocity, dx=.0005, initial=0)
        
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
            ax.invert_yaxis()
            ax.plot(self.decelleration, self.depth, label='decel')
            ax.plot(self.velocity, self.depth, label='vel')
            ax.legend(loc='upper right')

        fig_manager.display(plot)

    def is_valid_spike(self, spike):
        return True

    def find_area(self, depth, tip_type='c', a_type='p', tip_length=7.87):
        """
        Parameters
        ----------
        depth: numpy array
            Array of depth values
        tip_type: str 
            Type of the tip ('c', 'b', or 'p')
        a_type: str 
            Area type ('m' or 'p')
        tip_length: float
            Length of the tip
        
        Return
        ------
        numpy array 
            Area values for each depth
        """
        
        depth_cm = np.array(depth) * 100  # Convert depth to cm
        A1 = np.zeros(len(depth_cm))
        r = np.zeros(len(depth_cm))
        
        for k in range(len(depth_cm)):
            if tip_type == 'c':
                if a_type == 'm':
                    if depth_cm[k] < tip_length:
                        r[k] = depth_cm[k] * np.tan(np.radians(30))
                        A1[k] = np.pi * r[k] * (np.sqrt((r[k]**2) + (depth_cm[k]**2)))
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k] * (np.sqrt((r[k]**2) + (tip_length**2)))
                elif a_type == 'p':
                    if depth_cm[k] < tip_length:
                        r[k] = depth_cm[k] * np.tan(np.radians(30))
                        A1[k] = np.pi * r[k]**2
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k]**2
            
            elif tip_type == 'b':
                if a_type == 'm':
                    r[k] = 4.375
                    if depth_cm[k] < tip_length:
                        A1[k] = np.pi * r[k]**2 + 2 * np.pi * r[k] * depth_cm[k]
                    else:
                        A1[k] = np.pi * r[k]**2 + 2 * np.pi * r[k] * tip_length
                elif a_type == 'p':
                    A1[k] = np.pi * 4.375**2
            
            elif tip_type == 'p':
                if a_type == 'm':
                    if depth_cm[k] < tip_length:
                        r[k] = np.sqrt(2.4184 * depth_cm[k])
                    else:
                        r[k] = 4.375
                    
                    polarfun = lambda theta, r: r * np.sqrt(0.745 * r**2 + 1)
                    A1[k], _ = dblquad(polarfun, 0, 2 * np.pi, lambda _: 0, lambda _: r[k])
                
                elif a_type == 'p':
                    if depth_cm[k] < tip_length:
                        r[k] = np.sqrt(2.4184 * depth_cm[k])
                        A1[k] = np.pi * r[k]**2
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k]**2
            
            A1[k] = A1[k] / 10000  # Convert area to square meters
        
        self.area = A1
        return A1
