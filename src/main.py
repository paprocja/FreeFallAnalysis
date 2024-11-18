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

def prompt_user_for_int(input_msg, output_msg, is_valid):
    """
    Prompts the user for an interger. Designed to be run as a thread.
    Will continue to ask user for input until a valid integer is input.

    Parameters
    ----------
    selection_resuls: Queue
        Thread-safe data structure to return selected peak to main thread
    input_msg: f string
        The prompt displayed to the user asking for input
    output_msg: f string
        The prompt displayed to the user after valid input is entered
    is_valid: function
        A function that returns true if the input is valid for the context
    """
    invalid = True
    while invalid:
        # prompt user to select peaks
        selection = input(input_msg)
        # attempt to convert input to an integer
        try:
            # get the value the user entered
            selection = int(selection)

            # validate the users input
            if is_valid(selection):
                # if valid queue the selection and output that the value is okay
                invalid = False
                return selection
            else:
                print(f'{selection} is not a valid choice!')
        except Exception as _:
            print(f'{selection} is not a valid integer!')


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
    peak_number = prompt_user_for_int(f"Select a peak {options}:\n", f"Please close the figure to see the selected plot.\n", bd_data.is_valid_peak)
    selected_peak_index = peak_number - 1
    if bd_data.is_valid_peak(selected_peak_index + 1):  # Check if the peak is valid
        selected_peak = Peak(selected_peak_index, bd_data)
        selected_peak.display_peak(fig_manager)
    else:
        print(f"Peak {peak_number} is not valid!")

    # Have the user select the spike
    spike_number = prompt_user_for_int( f"Select a spike within the peak:\n", "Please close the figure to see the integration graphs.\n", selected_peak.is_valid_spike)
    
    selected_peak.display_decel_vel_dep(fig_manager, spike_number)
    input("Press enter to continue.")   

    selected_peak.find_area()

if __name__ == "__main__":
    main()