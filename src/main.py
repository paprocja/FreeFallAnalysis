#!/usr/bin/python3
import FileSelectUI
import os
from BD_Data import BD_Data
from Peak import Peak
from FigureManager import FigureManager


# BD_Data object with parsed data from binary file
bd_data = None
# FigureManager Object to handle all of our plot figures
fig_manager = FigureManager()

# Create a BD_Data object once a file has been selected by the UI component
def on_select_file(file_path, bdid):
    """
    Creates a BD_Data object from the selected file    
    """
    global bd_data
    bd_data = BD_Data(file_path, bdid)
    
def save_to_csv():
    """
    Writes output of binary data to CSV file
    """
    # Allows main to be executed from ui-ffp or ui-ffp/src folders
    # TODO make it so main can be executed anywhere on the system for packaging
    if os.path.exists("../output/F_Matrix.csv"):
        bd_data.save_data("../output/F_Matrix.csv")
    else:
        bd_data.save_data("output/F_Matrix.csv")

def prompt_user_for_num(input_msg, output_msg, is_valid, data_type='i'):
    """
    Prompts the user for an integer or float.
    Will continue to ask user for input until a valid input is provided.

    Parameters
    ----------
    input_msg: str
        The prompt displayed to the user asking for input
    output_msg: str
        The prompt displayed to the user after valid input is entered
    is_valid: Any -> Boolean
        A function of that validates the user input. Returns true or false.
    data_type: str
        The type of input expected from the user, defaults to 'i' for integer
    """
    invalid = True
    while invalid:
        # prompt user to select peaks
        selection = input(input_msg)
        try:
            # get the value the user entered for the specific data type
            if data_type != 'i':
                selection = float(selection)
            else:
                selection = int(selection)

            # validate the users input
            if is_valid(selection):
                # if valid alert user and return value
                invalid = False
                print(output_msg)
                return selection
            else:
                print(f'{selection} is not a valid choice!')
        except Exception as _:
            type = 'integer' if data_type == 'i' else 'float' 
            print(f'{selection} is not a valid {type}!')

def select_peak() -> Peak:
    """
    Prompts user to select a peak and returns peak object

    Returns
    -------
    selected_peak: Peak
        Peak object representing selected peak
    """
    options = [i+1 for i in range(bd_data.number_peaks)]
    prompt_msg = f"Select a peak {options}:\n"
    happy_msg = "Valid peak selected.\n"
    peak_number = prompt_user_for_num(prompt_msg, happy_msg, bd_data.is_valid_peak)
    selected_peak = Peak(peak_num=peak_number-1, BD=bd_data)
    return selected_peak

def select_spike(peak: Peak) -> int:
    prompt_msg = f"Select a spike within the peak:\n"
    happy = "Valid spike selected.\n"
    return prompt_user_for_num(prompt_msg, happy, peak.is_valid_spike)

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
    correction_type = prompt_user_for_num(prompt_msg, happy_msg, is_valid_correction_type)
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
        correction_factor = prompt_user_for_num(prompt_msg, happy_msg, is_valid_beta, 'f')
    else:
        # Start a UI thread to get k value
        prompt_msg = "Enter in a k value between 0 and 1.5.\n"
        happy_msg = "Valid k value.\n"
        correction_factor = prompt_user_for_num(prompt_msg, happy_msg, is_valid_k, 'f')

    return correction_factor


def get_range_vals():
    def is_valid_start(start):
        if start >= 0 and start <= 86:
            return True
        else:
            return False
        
    start = prompt_user_for_num(f"Start time stamp?\n", "Valid starting point\n", is_valid_start)
        
    def is_valid_end(end, start=start):
        if end > start and end <= 86:
            return True
        else:
            return False

    
    end = prompt_user_for_num(f"End time stamp?\n", "Valid ending point", is_valid_end)

    return start, end

def main():
    # Starts file selection UI
    file_select = FileSelectUI.FileSelectUI(on_select_file)
    file_select.create_ui()

    # ensures bd_data exists and has peaks
    if bd_data is None or bd_data.number_peaks == 0:
        print("No peaks found. Exiting Program.")
        return
    
    #display the initial plot through the figure manager
    bd_data.display_initial_data(fig_manager)

    # Prompt user to select a peak
    peak = select_peak()
    peak.display_peak(fig_manager)

    # Once peak is selected, prompt user to select a spike within the peak
    spike = select_spike(peak)
    peak.display_decel_vel_dep(fig_manager, spike)

    # Get input for type of correction log, asinh, or beta
    # Once spike is selected, prompt user to select a QSBC correction equation
    correction_type = get_correction_type()
    print(f'Correction type: {correction_type}')

    # Get correction value either k or beta value
    # correction_factor = get_correction_factor(correction_type)
    # print(f'Correction factor: {correction_factor}')

    # Will also need to pass in the tip type when not using default to c
    peak.display_QSBC_for_K(fig_manager, correction_type, 1.5)
    input("Press enter to continue.")  
    
    # Tuple used to find start and end values. Could be changed so parameters are not needed for average calculation
    start, end = get_range_vals()

    # Currently hard coded to use values 1 and 1.5, but whatever values are needed for graph can be used
    peak.display_correction_QSBC(fig_manager, correction_type, start, end)
    # peak._calculate_average_qsbc(correction_type, 1, 1.5, start, end)

    input("Press enter to end the program.")  


if __name__ == "__main__":
    main()