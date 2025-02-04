import numpy as np
from scipy import integrate

def calculate_tilt(spike, drop_end, peak_x, peak_y):
    """
    Calculates the tilt in the x and y directions based off the 55g peak.

    Parameters
    ----------
    spike: int
        The x location of the spike

    drop_end: int
        The x location where the drop comes back to 0

    peak_x: numpy array
        The 55g peak array in the x direction

    peak_y: numpy array
        The 55g peak array in the x direction
    
    Assigns
    -------
    tilt_x: float
        The tilt in the x direction
    
    tilt_y: float
        The tilt in the y direction
    """
    spike_to_end_x = peak_x[spike:drop_end+1]
    spike_to_end_y = peak_y[spike:drop_end+1]

    spike_to_end_x = spike_to_end_x * 9.81
    spike_to_end_y = spike_to_end_y * 9.81

    STEP = 1/2000

    velocity_x = integrate.cumulative_trapezoid(spike_to_end_x, dx=STEP, initial=0)
    velocity_y = integrate.cumulative_trapezoid(spike_to_end_y, dx=STEP, initial=0)

    depth_x = integrate.cumulative_trapezoid(velocity_x, dx=STEP, initial=0)
    depth_y = integrate.cumulative_trapezoid(velocity_y, dx=STEP, initial=0)

    depth_x = [abs(x) * 100 for x in depth_x]
    depth_y = [abs(x) * 100 for x in depth_y]

    tilt_x = np.max(depth_x)
    tilt_y = np.max(depth_y)

    return tilt_x, tilt_y