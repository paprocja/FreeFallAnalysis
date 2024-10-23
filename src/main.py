#!/usr/bin/python3
import FileSelectUI
import os
import threading
from queue import Queue
from BD_Data import BD_Data

# TODO look into making this not a global variable
# may be a necessity because UI might be able to return a value
# BD_Data object with parsed data from binary file
bd_data = None

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

def prompt_user_for_peak(num_peaks, selection_results):
    """
    Prompts the user to select a peak. Designed to be run as a thread.
    Will continue to ask user for input until a valid peak is selected.

    Parameters
    ----------
    num_peaks: int
        Number of peaks to select from
    selection_resuls: Queue
        Thread-safe data structure to return selected peak to main thread
    """
    invalid = True
    while invalid:
        # prompt user to select peaks
        selection = input(f"Select a peak (1, ..., {num_peaks}):\n")
        # attempt to convert input to an integer
        try:
            selected_peak = int(selection) - 1
            if selected_peak in range(0, num_peaks):
                invalid = False
                selection_results.put(selected_peak)
                print("Please close the figure to see the selected plot.")
            else:
                print(f'{selection} is not a valid choice!')
        except Exception as _:
            print(f'{selection} is not a valid integer!')

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
    
    # Prompts user to select a peak
    selection_results = Queue() # thread-safe data structure for return value
    selection_thread = threading.Thread(target=lambda: prompt_user_for_peak(num_peaks, selection_results))
    selection_thread.start()

    # Displays initial data and peaks
    bd_data.display_initial_data(peaks, heights, num_peaks)
    
    # Retrieves the selected peak and displays it
    selected_peak = selection_results.get()
    bd_data.display_peak(peaks[selected_peak])

if __name__ == "__main__":
    main()