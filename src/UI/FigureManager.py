import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
# from BD_Data import is_valid_peak
import numpy as np  # numpy needed to support the change from single ax to multiple

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons
        self.textboxes = []
        self.selected_peak_number = None #used for returning the value from the button
        self.is_ready = False # flag for if ready to go to next display (has input value)
    


    def clear(self):
        """
        Clears the current axes and resets the figure. 

        Clears the ax if it has multiple axes or just one
        """
        if isinstance(self.ax, (list, np.ndarray)):  # Handle multiple axes
            for sub_ax in self.ax:
                sub_ax.clear()
        else:
            self.ax.clear()

        for button in self.buttons:
            button.ax.remove()  # Remove buttons from the figure
        self.buttons.clear()

        for textbox in self.textboxes:
            textbox.ax.remove()
        self.textboxes.clear()

    def display(self, plot_function, nrows=1, ncols=1, display_type=None, *args, **kwargs):
        """
        Displays the plot with subplots if specified.

        Parameters
        ----------
        plot_function: callable
            A function that takes axes and any additional arguments.
        nrows: int
            Number of rows of subplots.
        ncols: int
            Number of columns of subplots.
        """
        # Update layout only if it changes
        if nrows * ncols != (len(self.ax) if isinstance(self.ax, np.ndarray) else 1):
            # Clear existing figure content
            self.fig.clear()

            # Create new subplots with the specified layout
            self.ax = self.fig.subplots(nrows=nrows, ncols=ncols, squeeze=False)
            self.ax = self.ax.flatten()  # Flatten for easy indexing
        else:
            self.clear()  # Clear existing content for reuse

        plot_function(self.ax, *args, **kwargs)

        plt.subplots_adjust(bottom=0.1)

        if display_type:
            self.setup_widgets(display_type)

        self.fig.tight_layout(rect=[0, 0.1,1,1])
        self.fig.canvas.draw_idle()
        plt.show(block=False)


    def setup_widgets(self, display_type):
        # Define widget setups based on display type
        if display_type == 'peak_selection':
            self.add_peak_selection_widgets()
        elif display_type == 'spike_selection': #todo implement this
            self.add_spike_selection_widgets()
        elif display_type == 'correction_type': # todo implement this
            self.add_correction_type_widgets()

    def add_peak_selection_widgets(self):
        # Setup widgets specific for peak selection
        axbox = plt.axes([0.1, 0.05, 0.1, 0.05])
        textbox = TextBox(axbox, 'Enter Peak #')
        self.textboxes.append(textbox)
        axbutton = plt.axes([0.21, 0.05, 0.1, 0.05])
        button = Button(axbutton, 'Submit')
        self.buttons.append(button)
        button.on_clicked(self.on_peak_submit)

    def on_peak_submit(self, event):
        # Handler for peak selection submit button
        print(f"Peak number {self.textboxes[0].text} submitted")
        try:
            peak_number = int(self.textboxes[0].text)
            self.selected_peak_number = peak_number  # Store the peak number
            self.is_ready = True #set flag that input is gathered
            print(f"Peak number {peak_number} selected and stored.")
        except ValueError:
            print("Please enter a valid integer for the peak number.")


    def wait_for_input(self): # temp method to wait for button press
        while not self.is_ready:
            plt.waitforbuttonpress(timeout=0.1)