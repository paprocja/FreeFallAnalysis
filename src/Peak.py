import math
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
        self.area = None

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
    
    def _get_mass_length(self, tip_type):
        """
        Gets the mass and length of a meter given a specific tip type.

        Parameters
        ----------
        tip_type: char
            the tip type to get the mass and length for 

        Return
        ------
        float:
            the mass of a meter
        float:
            the length of a meter
        """
        if tip_type == 'b':            
            return 10.30, 8.57
        elif tip_type ==  'e':
            return 9.15, 8.26
        else : 
            return 7.71, 7.87


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

    def _calculate_QSBC_for_K(self, correction_type, correction_factor, tip_type):
        """
        Corrects the quasi static bearing capacity to be standardized with other researchers.

        Parameters
        ----------
        correction_type: int
            the type of correction either Log, Asinh, Beta
        correction_factor: float
            either the k or beta value to be used in calculation
        tip_type: char
            the type of tip the penetrometer has

        Return
        ------
        numpy array
            the corrected qsbc for a given correction type, factor, and tip
        """
        mass, _ = self._get_mass_length(tip_type)

        # Take off the last value because it is 0 and we cannot take log of 0
        corrected_velocity = self.velocity[:-1] / 0.02

        # Calculate fsr
        if correction_type == 1:
            # Logarithmic
            fsr = np.array([1 + correction_factor * math.log10(v) for v in corrected_velocity])
        elif correction_factor == 2:
            # Asinh
            k_prime = correction_factor / math.log(10)
            fsr = np.array([1 + k_prime * math.asinh(v) for v in corrected_velocity])
        else:
            # Beta
            fsr = np.array([v ** correction_factor for v in corrected_velocity])

        force_bouyancy = self.decelleration * mass * 9.81

        # the first value in the area array is 0
        q_dynamic = force_bouyancy[1:] / self.area[1:]
        self.qdyn = q_dynamic
        # because we adjusted q_dynamic and velocity we need to correct here to allign the values
        corrected_QSBC =  q_dynamic[:-1] / fsr[1:]

        corrected_QSBC_kPa = corrected_QSBC / 1000

        return corrected_QSBC_kPa
    
    def _calculate_average_qsbc(self, correction_type, start_k, end_k, start_range, end_range, tip_type = 'c'):
        """
        Returns the average QSBC between two given strain-rate factors

        Parameters
        ----------
        correction_type: int
            the type of correction either Log, Asinh, Beta
        start_k: float
            the lower k value for the averaged range
        end_k: float
            the higher k value for the averaged range
        start_range: integer
            starting value of array to be used in calculation
        end_range: integer
            ending value of array to be used in calculation
        tip_type: char
            the type of tip the penetrometer has

        Return
        ------
        numpy array
            the average qsbc between the two given strain-rate factors
        """
        # Calculates lower bound array
        val1 = self._calculate_QSBC_for_K(correction_type, start_k, tip_type)
        # Calculates higher bound array
        val2 = self._calculate_QSBC_for_K(correction_type, end_k, tip_type)

        # Cuts off unneeded values
        val1r = val1[start_range - 2:end_range - 1]
        val2r = val2[start_range - 2:end_range - 1]

        #Finds average between arrays
        ave = (val1r + val2r) / 2
        
        return val1r, val2r, ave


        
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

    def display_decel_vel_dep(self, fig_manager, selected_spike=None):
        """
        Displays the deceleration, velocity, and depth data in one plot.

        Parameters
        ----------
        fig_manager: FigureManager
            The figure manager used to display the plot
        selected_spike: int
            The x value of the spike where we will start to calculate values from if not provided will use the already assigned velocity and depth

        """

        # TODO make sure if selected_spike is None velocity and depth exist
        if selected_spike is not None:
                self._integrate_acceleration(selected_spike)
                self._calculate_area_of_meter()
        
        def plot(ax):
            ax.invert_yaxis()
            ax.plot(self.decelleration, self.depth, label='decel')
            ax.plot(self.velocity, self.depth, label='vel')
            ax.legend(loc='upper right')

        fig_manager.display(plot)
        
    def _calculate_area_of_meter(self, tip_type='c', a_type='p'):
        """
        Calculates the array of a penetrometer at each step.

        Parameters
        ----------
        tip_type: str 
            Type of the tip ('c', 'b', or 'p')
        a_type: str 
            Area type ('m' or 'p')
        """

        _, length = self._get_mass_length(tip_type)
        
        depth_cm = np.array(self.depth) * 100  # Convert depth to cm
        A1 = np.zeros(len(depth_cm))
        r = np.zeros(len(depth_cm))
        
        for k in range(len(depth_cm)):
            if tip_type == 'c':
                if a_type == 'm':
                    if depth_cm[k] < length:
                        r[k] = depth_cm[k] * np.tan(np.radians(30))
                        A1[k] = np.pi * r[k] * (np.sqrt((r[k]**2) + (depth_cm[k]**2)))
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k] * (np.sqrt((r[k]**2) + (length**2)))
                elif a_type == 'p':
                    if depth_cm[k] < length:
                        r[k] = depth_cm[k] * np.tan(np.radians(30))
                        A1[k] = np.pi * r[k]**2
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k]**2
            
            elif tip_type == 'b':
                if a_type == 'm':
                    r[k] = 4.375
                    if depth_cm[k] < length:
                        A1[k] = np.pi * r[k]**2 + 2 * np.pi * r[k] * depth_cm[k]
                    else:
                        A1[k] = np.pi * r[k]**2 + 2 * np.pi * r[k] * length
                elif a_type == 'p':
                    A1[k] = np.pi * 4.375**2
            
            elif tip_type == 'p':
                if a_type == 'm':
                    if depth_cm[k] < length:
                        r[k] = np.sqrt(2.4184 * depth_cm[k])
                    else:
                        r[k] = 4.375
                    
                    polarfun = lambda theta, r: r * np.sqrt(0.745 * r**2 + 1)
                    A1[k], _ = integrate.dblquad(polarfun, 0, 2 * np.pi, lambda _: 0, lambda _: r[k])
                
                elif a_type == 'p':
                    if depth_cm[k] < length:
                        r[k] = np.sqrt(2.4184 * depth_cm[k])
                        A1[k] = np.pi * r[k]**2
                    else:
                        r[k] = 4.375
                        A1[k] = np.pi * r[k]**2
            
            A1[k] = A1[k] / 10000  # Convert area to square meters
        
        self.area = A1
    
    def display_QSBC_for_K(self, fig_manager, correction_type, correction_factor, tip_type = 'c'):
        """
        Calculates and displays the quasi static bearing capacity for a given type, factor, and tip.

        Parameters
        ----------
        correction_type: int
            the type of correction either Log, Asinh, Beta
        correction_factor: float
            either the k or beta value to be used in calculation
        tip_type: char
            the type of tip the penetrometer has
        """
        qsbc_for_k = self._calculate_QSBC_for_K(correction_type, correction_factor, tip_type)
        print("QSBC FOR K\n")
        print(qsbc_for_k)
        def plot(ax):
            ax.plot(qsbc_for_k)

        fig_manager.display(plot)


    def display_correction_QSBC(self, fig_manager, correction_type, start, end):

        line1val1, line1val2, line1ave = self._calculate_average_qsbc(correction_type, 1.0, 1.5, start, end)
        line2val1, line2val2, line2ave = self._calculate_average_qsbc(correction_type, 0.1, 0.2, start, end)
        depth = self.depth[start:end+1]*100
        def plot(ax):
            
            ax.plot(line1ave, depth, label='Line 1 Average')
            ax.invert_yaxis()
            ax.fill_betweenx(depth, line1val1, line1val2, color='grey', alpha=0.3, label='shaded correction 1')
            
            ax.plot(line2ave, depth, label='line 2 Average')
            ax.fill_betweenx(depth, line2val1, line2val2, color='grey', alpha=0.3, label='shaded correction 1')

            ax.plot(self.qdyn[start:end+1]/1000, depth, label='dynamic')


        fig_manager.display(plot)

        

    def is_valid_spike(self, spike):
        return True
