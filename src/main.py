#!/usr/bin/python3
import os
import UI.FileSelectUI as FileSelectUI
import Utils.io_utils as io
from UI.Figures.PeakDisplay import *
from UI.Figures.PenetrometerDataDisplay import display_initial_data
from Data.TiltCalculator import calculate_tilt
from UI.FigureManager import FigureManager
from Data.PenetrometerData import PenetrometerData
from Data.Peak import Peak

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
    Prompts user for yes/no response on restarting the program. 
    If yes, will create a new figure window and keep the old one in the background.
    """
    prompt_msg = "\nWould you like to analyze a peak from the same file? (Y/N)\n"
    happy_msg = "Valid response selected."
    response = io.prompt_user_for_val(prompt_msg, happy_msg, lambda res: res in ['n', 'N', 'y', 'Y'], data_type='s')
    if response in ['n', 'N']:
        print("Exiting program.")
        return False
    else:
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

def select_peak() -> Peak:
    """
    Prompts user to select a peak and returns peak object

    Returns
    -------
    selected_peak: Peak
        Peak object representing selected peak
    """
    options = [i+1 for i in range(penetrometer_data.number_peaks)]
    prompt_msg = f"Select a peak {options}:\n"
    happy_msg = "Valid peak selected.\n"
    peak_number = io.prompt_user_for_val(prompt_msg, happy_msg, penetrometer_data.is_valid_peak)
    selected_peak = Peak(peak_num=peak_number-1, penetrometer_data=penetrometer_data)
    return selected_peak

def select_spike(peak: Peak, fig_manager: FigureManager) -> int:
    prompt_msg = f"Select a spike within the peak:\n"
    happy = "Valid spike selected.\n"
    val = io.prompt_user_for_val(prompt_msg, happy, lambda _: True)

    user_happy = io.confirm_input_spike(fig_manager, peak, val)

    while (user_happy is False):
        display_peak(fig_manager, peak.peak, peak.g2g, peak.end_of_drop, peak.peak_center)
        val = io.prompt_user_for_val(prompt_msg, happy, lambda _: True)
        user_happy = io.confirm_input_spike(fig_manager, peak, val)

    return val

def get_correction_type() -> int:
    """
    Promps user to select a correction type

    Returns
    -------
    correction_type: int
        Int value of the strain rate correction type 
    """

    # determine if valid selection is entered
    def is_valid_correction_type(correction):
        return correction-1 in range(0,3)
    prompt_msg = "Select a correction type. Enter 1 for Logarithmic, 2 for Asinh, or 3 for Beta.\n"
    happy_msg = "Valid correction type entered.\n"
    # prompt the user for the correction type
    correction_type = io.prompt_user_for_val(prompt_msg, happy_msg, is_valid_correction_type)
    return correction_type

def get_correction_factor(correction_type: int) -> float:
    """
    Gets the correction factor for calculation from the user

    Parameters
    ----------
    correction_type: int
        Integer representation of correction type provided by user
    
    Returns
    -------
    correction_factor: float
        beta or k value for correction
    """
    def is_valid_k(k):
        return k >= 0 and k <= 1.5
        
    def is_valid_beta(k):
        return k >= 0.035 and k <= 0.085

    if correction_type == 3:
        prompt_msg = "Enter in a beta value between 0.035 and 0.085.\n"
        happy_msg = "Valid beta value.\n"
        # prompt user for beta value
        correction_factor = io.prompt_user_for_val(prompt_msg, happy_msg, is_valid_beta, 'f')
    else:
        # Start a UI thread to get k value
        prompt_msg = "Enter in a k value between 0 and 1.5.\n"
        happy_msg = "Valid k value.\n"
        correction_factor = io.prompt_user_for_val(prompt_msg, happy_msg, is_valid_k, 'f')

    return correction_factor


def get_range_vals(qsbc_for_K):
    def is_valid_start(start):
        if start >= 0 and start <= 86:
            return True
        else:
            return False
        
    start = io.prompt_user_for_val(f"Start time stamp?\n", "Valid starting point\n", is_valid_start)
        
    def is_valid_end(end, start=start):
        if end > start and end <= 86:
            return True
        else:
            return False

    end = io.prompt_user_for_val(f"End time stamp?\n", "Valid ending point\n", is_valid_end)

    user_happy = io.confirm_input_range(fig_manager, qsbc_for_K, start, end)

    while (user_happy is False):
        display_QSBC_for_K(fig_manager, qsbc_for_K)

        start = io.prompt_user_for_val(f"Start time stamp?\n", "Valid starting point\n", is_valid_start)
        end = io.prompt_user_for_val(f"End time stamp?\n", "Valid ending point\n", is_valid_end)
        user_happy = io.confirm_input_range(fig_manager, qsbc_for_K, start, end)

    return start, end


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
        peak_number = display_initial_data(fig_manager, penetrometer_data.g2g, penetrometer_data.g18g, penetrometer_data.g50g, penetrometer_data.g200g, penetrometer_data.g250g,
                              penetrometer_data.peaks, penetrometer_data.heights, penetrometer_data.number_peaks)

        # Prompt user to select a peak
        peak = Peak(peak_num=peak_number-1, penetrometer_data=penetrometer_data)

    
        # Once peak is selected, prompt user to select a spike within the peak
        spike = display_peak(fig_manager, peak.peak, peak.g2g, peak.end_of_drop, peak.peak_center) # select_spike(peak, fig_manager)
        peak.integrate_spike(spike)

        # Get input for type of correction log, asinh, or beta
        # Once spike is selected, prompt user to select a QSBC correction equation
        correction_type = display_decel_vel_dep(fig_manager, peak.depth, peak.decelleration, peak.velocity) #get_correction_type()

        # TODO prompt user for correction factor and tip_type
        correction_factor = 1.5
        tip_type = 'c'

        initial_qsbc = peak.calculate_QSBC_for_K(correction_type, correction_factor, tip_type)

        # Will also need to pass in the tip type when not using default to c
        
        # Tuple used to find start and end values. Could be changed so parameters are not needed for average calculation
        start, end = display_QSBC_for_K(fig_manager, initial_qsbc)  # get_range_vals(initial_qsbc)
        print(start, end)
        line1val1, line1val2, line1ave, line2val1, line2val2, line2ave = peak.calculate_corrected_qsbc(correction_type, start, end)

        # Currently hard coded to use values 1 and 1.5, but whatever values are needed for graph can be used
        display_corrected_QSBC(fig_manager, line1val1, line1val2, line1ave, line2val1, line2val2, line2ave,
                                peak.depth, peak.velocity, peak.decelleration, peak.qdyn, start, end)

        tilt_x, tilt_y = calculate_tilt(spike, peak.end_of_drop, peak.gX55g, peak.gY55g)

        print(f'Tilt x: {tilt_x}, Tilt y: {tilt_y}')

        # Prompt user to restart
        running = restart()

if __name__ == "__main__":
    main()