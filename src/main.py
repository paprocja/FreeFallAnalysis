#!/usr/bin/python3
import FileSelectUI
import os
from queue import Queue
from BD_Data import BD_Data
from Peak import Peak
from FigureManager import FigureManager


# BD_Data object with parsed data from binary file
bd_data = None
# FigureManager Object to handle all of our plot figures
fig_manager = FigureManager()
# thread-safe data structure for return value
selection_results = Queue()

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

def prompt_user_for_num(input_msg, output_msg, is_valid, data_type="i"):
    """
    Prompts the user for an integer or float.
    Will continue to ask user for input until a valid input is provided.

    Parameters
    ----------
    input_msg: f string
        The prompt displayed to the user asking for input
    output_msg: f string
        The prompt displayed to the user after valid input is entered
    is_valid: function
        A function that returns true if the input is valid for the context
    data_type: char
        The type of input expected from the user, defaults to integer
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


def get_correction_type():
    """
    Gets a correction type from the user.

    Parameters
    ----------

    Return
    ----------
    int: Int value of the strain rate correction type 
    """

    # determine if valid selection is entered
    def is_valid_correction_type(correction):
        if correction - 1 in range(0, 3):
            return True
        else:
            return False

    # Start a UI thread to get correction type
    correction_type = prompt_user_for_num(f"Select a correction type. Enter 1 for Logarithmic, 2 for Asinh, or 3 for Beta.\n",
                                                                            "Valid correction type entered.\n", is_valid_correction_type)
    return correction_type

def get_correction_factor(correction_type):
    def is_valid_k(k):
        if k >= 0 and k <= 1.5:
            return True
        else:
            return False
        
    def is_valid_beta(k):
        if k >= 0.035 and k <= 0.085:
            return True
        else:
            return False


    if correction_type == 3:
        # Start a UI thread to get beta value
        correction_factor = prompt_user_for_num(f"Enter in a beta value between 0.035 and 0.085.\n",
                                                                                "Valid beta value.\n", is_valid_beta, 'f')
    else:
        # Start a UI thread to get k value
        correction_factor = prompt_user_for_num(f"Enter in a k value between 0 and 1.5.\n",
                                                                                "Valid k value.\n", is_valid_k, 'f')

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
    # File selection UI
    file_select = FileSelectUI.FileSelectUI(on_select_file)
    file_select.create_ui()

    # make sure that bd_data is created
    if bd_data is None or bd_data.number_peaks == 0:
        print("No peaks found. Exiting Program.")
        return
    
    #display the initial plot through the figure manager
    bd_data.display_initial_data(fig_manager)

    # Get the peaks set up and allow for user to input a peak to move to the spike figure
    options = [i+1 for i in range(bd_data.number_peaks)]
    peak_number = prompt_user_for_num(f"Select a peak {options}:\n", f"Please close the figure to see the selected plot.\n", bd_data.is_valid_peak)
    selected_peak_index = peak_number - 1
    if bd_data.is_valid_peak(selected_peak_index + 1):  # Check if the peak is valid
        selected_peak = Peak(selected_peak_index, bd_data)
        selected_peak.display_peak(fig_manager)
    else:
        print(f"Peak {peak_number} is not valid!")

    # Have the user select the spike
    spike_number = prompt_user_for_num( f"Select a spike within the peak:\n", "Please close the figure to see the integration graphs.\n", selected_peak.is_valid_spike)
    
    selected_peak.display_decel_vel_dep(fig_manager, spike_number)
    input("Press enter to continue.")   

    selected_peak.calculate_area_of_meter()
    
    # Get input for type of correction log, asinh, or beta
    correction_type = get_correction_type()

    print(f'Correction type: {correction_type}')

    # Get correction value either k or beta value
    correction_factor = get_correction_factor(correction_type)

    print(f'Correction factor: {correction_factor}')

    # Will also need to pass in the tip type when not using default to c
    selected_peak.display_QSBC_for_K(fig_manager, correction_type, correction_factor)
    input("Press enter to continue.")  
    
    # Tuple used to find start and end values. Could be changed so parameters are not needed for average calculation
    start, end = get_range_vals()

    # Currently hard coded to use values 1 and 1.5, but whatever values are needed for graph can be used
    selected_peak._calculate_average_qsbc(correction_type, 1, 1.5, start, end)

    input("Press enter to end the program.")  




if __name__ == "__main__":
    main()