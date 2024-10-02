import tkinter as tk
from tkinter import filedialog

class FileSelectUI:

    def __init__(self, command):
        self.command = command
        self.root = tk.Tk()

    def dispose(self):
        self.root.destroy()

    def on_button_click(self):
        # get the file path from the users selection
        file_path = filedialog.askopenfilename(title="Select a file")

        try:
            # run the command to get the data from the file
            self.command(file_path)
        finally:
            self.dispose()

    #makes the ui
    def create_ui(self):
        # add a title to the UI
        self.root.title("File Reader")
        
        # add a label to the UI
        label = tk.Label(self.root, text="Click to select file to read")

        # UI padding
        label.pack(pady=10)
        label.pack(padx=50)
        

        # configure the button to execute on_button_click on click
        raw_file_button = tk.Button(self.root, text="Select Data File", command=self.on_button_click)

        # UI padding
        raw_file_button.pack(pady=10)
        raw_file_button.pack(padx=25)
        raw_file_button.pack(side="left")

        # button to slelect existing data file
        existing_file_button = tk.Button(self.root, text="Select Existing File", command=self.on_button_click)

        # UI padding
        existing_file_button.pack(pady=10)
        existing_file_button.pack(padx=25)
        existing_file_button.pack(side="right")


        # execute the main UI loop
        self.root.mainloop()
