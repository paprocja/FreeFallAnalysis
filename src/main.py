#!/usr/bin/python3
import FileSelectUI
import os
import threading
from queue import Queue
from BD_Data import BD_Data
from Peak import Peak

# TODO look into making this not a global variable
# may be a necessity because UI might be able to return a value
# BD_Data object with parsed data from binary file
bd_data = None

# thread-safe data structure for return value
selection_results = Queue()

def on_select_file(file_path, bdid):
    """
    Creates a BD_Data object from the selected file    
    """
    global bd_data
    bd_data = BD_Data(file_path, bdid)
    
def save_to_csv():
    """
    Writes output of binary data to CSV file
    TODO Should probably be placed within BD_Data so we can save that instead, CSV isn't the best here 
    """
    # Allows main to be executed from ui-ffp or ui-ffp/src folders
    # TODO make it so main can be executed anywhere on the system for packaging
    if os.path.exists("../output/F_Matrix.csv"):
        bd_data.save_data("../output/F_Matrix.csv")
    else:
        bd_data.save_data("output/F_Matrix.csv")

def prompt_user_for_int(selection_results, input_msg, output_msg, is_valid):
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
        A function that returns true if the input is valid
    """
    invalid = True
    while invalid:
        # prompt user to select peaks
        selection = input(input_msg)
        # attempt to convert input to an integer
        try:
            selection = int(selection)
            if is_valid(selection):
                invalid = False
                selection_results.put(selection)
                print(output_msg)
            else:
                print(f'{selection} is not a valid choice!')
        except Exception as _:
            print(f'{selection} is not a valid integer!')

def get_peak_number(peaks, heights, num_peaks):
    """
    Gets a number of a peak that will be analyzed.

    Parameters
    ----------
    peaks : List[int]
    x values of peaks

    heights : List[int]
    y values of peaks

    num_peaks : int
    len(peaks) as it is called elsewhere
    """
    # Prompts user to select a peak
    selection_thread = threading.Thread(target=lambda: prompt_user_for_int(selection_results, f"Select a peak (1, ..., {num_peaks}):\n", f"Please close the figure to see the selected plot.\n", bd_data.is_valid_peak))
    selection_thread.start()

    # Displays initial data and peaks
    bd_data.display_initial_data(peaks, heights, num_peaks)

    # Return the selected peak and adjust for 0 index
    return selection_results.get() - 1

def get_spike(selected_peak):
    """
    Gets a spike from a user based off the graph of the peak.

    Parameters
    ----------
    selected_peak: Peak
    The peak to be graphed
    """
    # Start a UI thread to get spike number from user
    selection_thread = threading.Thread(target=lambda: prompt_user_for_int(selection_results, f"Select a spike within the peak:\n", "Please close the figure to see the integration graphs.\n", selected_peak.is_valid_spike))
    selection_thread.start()

    # Displays the peak
    selected_peak.display_peak()

    # Return the selected spike
    return selection_results.get()

def main():
    # Creates the file selection ui, passing in command to be executed when button is clicked
    file_select = FileSelectUI.FileSelectUI(on_select_file)
    
    # Starts the file selection ui loop
    file_select.create_ui()

    ## save_to_csv()

    # Finds peaks within data
    peaks, heights = bd_data.findpeaks()
    num_peaks = len(peaks)
    if num_peaks == 0:
        exit("No peaks found. Exiting Program.")
    
    # print out peak x and y values
    print(f'x values: {peaks}')
    print(f'y values: {heights}')

    selected_peak_number = get_peak_number(peaks, heights, num_peaks)

    # Create a peak based off the x value of the peak
    selected_peak = Peak(peaks[selected_peak_number], bd_data)
    
    selected_spike = get_spike(selected_peak)

    print(f'Selected spike: {selected_spike}')


if __name__ == "__main__":
    main()