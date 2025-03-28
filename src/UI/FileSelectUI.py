import tkinter as tk
from tkinter import filedialog

class FileSelectUI:

    def __init__(self, command):
        self.command = command
        self.root = tk.Tk()

    def dispose(self):
        self.root.destroy()
        self.root.quit()

    def on_button_click(self):
        # get a tuple of file paths from the user selection
        file_paths = filedialog.askopenfilenames(title="Select .bin file(s)")
        try:
            # run the command to get the data from the file
            self.command(file_paths, self.selected_option.get())
        finally:
            self.dispose()

    #makes the ui
    def create_ui(self):
        # add a title to the UI window
        self.root.title("File Reader")
        
        # add a label to the UI
        label = tk.Label(self.root, text="Click to select file to read")
        label.pack(pady=10, padx=50)

        # button to open select a file dialog and load data
        raw_file_button = tk.Button(self.root, text="Select Data File", command=self.on_button_click)
        raw_file_button.pack(pady=10, padx=25, side='left')

        # variable to store blueDrop id number (default 8)
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set('8')
        # options
        options = ['1', '2', '3', '8', 'json']
        # dropdown to select blueDrop id number
        bD_dropdown = tk.OptionMenu(self.root, self.selected_option, *options)
        bD_dropdown.pack(pady=10, padx=25, side="right")

        # execute the main UI loop
        self.root.mainloop()
