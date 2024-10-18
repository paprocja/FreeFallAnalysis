import FileSelectUI
from BD_Data import BD_Data

# TODO look into making this not a global variable but it may be a necessity because IDK how the UI command can return
# a value
# BD_Data object with F array from mat lab script and g sensor values
bd_data = None

## UI COMMANDS

# This is a command that is passed into FileSelectUI to be executed on a button press
def on_select_file(file_path, bdid):
    global bd_data
    bd_data = BD_Data(file_path, bdid)
    
# saves a numpy array as a csv file
# may make more sense to go somewhere else at some point 
def save_to_csv():
    # Write output to csv file in output directory
    bd_data.save_data("../output/F_Matrix.csv")

def main():
    # create the file selection ui, passing in command to be executed when button is clicked
    file_select = FileSelectUI.FileSelectUI(on_select_file)
    
    # start the file selection ui loop
    file_select.create_ui()

    save_to_csv()

    bd_data.display_peak(24905)

    # print the numpy array to console
    bd_data.output()
    bd_data.plot_initial_data()

if __name__ == "__main__":
    main()