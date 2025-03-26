#!/usr/bin/python3
import os
from Data.SoilParameterization import SoilParameterization
import UI.FileSelectUI as FileSelectUI
import Utils.io_utils as io
from UI.Figures.PeakDisplay import *
from UI.Figures.PorePressureDisplay import *
from UI.Figures.PenetrometerDataDisplay import display_initial_data
from UI.Figures.ClayFrameworkDisplay import display_Su_for_K
from Data.TiltCalculator import calculate_tilt
from UI.FigureManager import FigureManager
from Data.PenetrometerData import PenetrometerData
from Data.Peak import Peak
from Data.PorePressure import PorePressure
from Data.ClayFramework import ClayFramework


#from Utils.io_utils import prompt_user_for_val, confirm_input_range, confirm_input_spike

# penetrometer_data object with parsed data from binary file
penetrometer_data = None

# flag to mark the first run with a set of files
original_run = None

# FigureManager Object to handle all of our plot figures
fig_manager = FigureManager()

# Create a penetrometer_data object once a file has been selected by the UI component 
def on_select_file(file_paths, penetrometer_id):
    """
    Creates a penetrometer_data object from the selected file    
    """
    global penetrometer_data
    global original_run
    if original_run is None:
        penetrometer_data = PenetrometerData(file_paths, penetrometer_id)
        original_run = [file_paths, penetrometer_id]
    

def save_to_csv():
    """
    Writes output of binary data to CSV file
    """
    # Allows main to be executed from ui-ffp or ui-ffp/src folders
    # TODO make it so main can be executed anywhere on the system for packaging
    if os.path.exists("../output/F_Matrix.csv"):
        penetrometer_data.save_data("../output/F_Matrix.csv")
    else:
        penetrometer_data.save_data("output/F_Matrix.csv")

def restart() -> bool:
    """
    if the user selected it will restart the program. 
    If yes, will create a new figure window and keep the old one in the background.
    """
    print("Loading original data...")
    global original_run
    if not original_run is None:
        global penetrometer_data
        penetrometer_data = PenetrometerData(original_run[0], original_run[1])
        print("Loaded original data successfully!")
        print("Creating figure manager for new window...")
        global fig_manager
        fig_manager = FigureManager()
        print("Created new figure manager successfully!\n")
        return True
    else:
        print("Failed to load original data! Please restart the program and reselect the file.\n")
        return False
    


def main():
    # Starts file selection UI
    file_select = FileSelectUI.FileSelectUI(on_select_file)
    file_select.create_ui()

    # ensures penetrometer_data exists and has peaks
    if penetrometer_data is None or penetrometer_data.number_peaks == 0:
        print("No peaks found. Exiting Program.")
        return
    
    running = True
    while running:
        #display the initial plot through the figure manager
        peak_number, do_calculate_pore_pressure = display_initial_data(fig_manager, penetrometer_data.g2g, penetrometer_data.g18g, penetrometer_data.g50g, penetrometer_data.g200g, penetrometer_data.g250g,
                              penetrometer_data.peaks, penetrometer_data.heights, penetrometer_data.number_peaks)

        # Prompt user to select a peak
        peak = Peak(peak_num=peak_number-1, penetrometer_data=penetrometer_data)

        # Determine if this peak will be used to calculate pore pressure
        # Once peak is selected, prompt user to select a spike within the peak
        spike = display_peak(fig_manager, peak.peak, peak.g2g, peak.end_of_drop, peak.peak_center) 
        peak.integrate_spike(spike)

        soil_parameterization = SoilParameterization(peak)

        # Get input for type of correction log, asinh, or beta
        # Once spike is selected, prompt user to select a QSBC correction equation
        correction_type, in_water = display_decel_vel_dep(fig_manager, peak.depth, peak.decelleration, peak.velocity)

        # TODO prompt user for correction factor and tip_type
        correction_factor = 1.5
        tip_type = 'c'

        initial_qsbc = peak.calculate_QSBC_for_K(correction_type, correction_factor, tip_type, in_water)

        # Will also need to pass in the tip type when not using default to c
        
        # Tuple used to find start and end values. Could be changed so parameters are not needed for average calculation
        start, end = display_QSBC_for_K(fig_manager, initial_qsbc)
        
        line1val1, line1val2, line1ave, line2val1, line2val2, line2ave = peak.calculate_corrected_qsbc(correction_type, start, end, in_water)

         # Get the tilt in the x and y directions
        tilt_x, tilt_y = calculate_tilt(spike, peak.end_of_drop, peak.gX55g, peak.gY55g)

        # Currently hard coded to use values 1 and 1.5, but whatever values are needed for graph can be used
        running = display_corrected_QSBC(fig_manager, line1val1, line1val2, line1ave, line2val1, line2val2, line2ave,
                                peak.depth, peak.velocity, peak.decelleration, peak.qdyn, start, end, tilt_x, tilt_y, do_calculate_pore_pressure)

        if soil_parameterization.framework == 'clay':
            framework = ClayFramework(peak, line1ave)
            # currently "hard coded"
            #framework.select_other_correction('Logarithmic')
            #framework.select_min_max_constants(0, max(su)) # will select entire range
            framework.select_ntk(1) # will output same as QSBC
            su = framework.proceed()
            display_Su_for_K(fig_manager, su)

        # Determine if this is the first peak and if the user would like to calculate pore pressure for that peak
        if do_calculate_pore_pressure:
            
            # Get the bounds of the pore pressure for the first peak
            pore_pressure_start, pore_pressure_end = display_peaks_and_ppm(fig_manager, penetrometer_data)

            # Create PorePressure object calculate deceleration profile based on bounds
            pore_pressure = PorePressure(peak, penetrometer_data, pore_pressure_start, pore_pressure_end)

            pore_pressure.calculate_deceleration_profile()

            # Get the bounds of the deceleration profile
            profile_increase, profile_decrease = display_deceleration_profile(fig_manager, pore_pressure)

            # Calculate and display pore pressure based on profile bounds
            pore_pressure.calculate_pore_pressure(profile_increase, profile_decrease)

            running = display_pore_pressure(fig_manager, pore_pressure)
    

        # Prompt user to restart
        # running = restart(running)


        if running:
            restart()
            
    print("Exiting program.")


if __name__ == "__main__":
    main()