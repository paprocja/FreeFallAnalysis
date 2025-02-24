import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np  # numpy needed to support the change from single ax to multiple
import time
from .Validator import Validator  # Import the Validator class

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons
        self.text_boxes = {}
        self.text_values = {}
        self.validation_types = {}
        self.valid_inputs = {}
        self.validator = Validator()  # Only instantiate once, re-use it
        self.is_ready = False
        self.start = None
        self.end = None
        self.ax2 = None # A second axis that can be used if two plots need different y-axis

    def clear(self):
        """Clears the current axes and resets the figure."""
        if isinstance(self.ax, (list, np.ndarray)):  # Handle multiple axes
            for sub_ax in self.ax:
                sub_ax.clear()
        else:
            self.ax.clear()

        if self.ax2 != None:
            self.ax2.clear()
            self.ax2 = None

        for button in self.buttons:
            button.ax.remove()  # Remove buttons from the figure
        self.buttons.clear()

        for label, text_box in self.text_boxes.items():  # Iterate directly over the dictionary
            text_box.ax.remove()  # Correctly access text_box
        self.text_boxes.clear()
        self.text_values.clear()
        self.validation_types.clear()
        self.valid_inputs.clear()

    def display(self, plot_function, nrows=1, ncols=1, *args, **kwargs):
        """Displays the plot with subplots if specified."""
        if nrows * ncols != (len(self.ax) if isinstance(self.ax, np.ndarray) else 1):
            self.fig.clear()
            self.ax = self.fig.subplots(nrows=nrows, ncols=ncols, squeeze=False)
            self.ax = self.ax.flatten()  # Flatten for easy indexing

            # if the display function is only expecting one axis we need to convert the array of axis into just the array
            if nrows * ncols == 1:
                self.ax = self.ax[0]
        else:
            self.clear()  # Clear existing content for reuse

        plot_function(self.ax, *args, **kwargs)

        plt.subplots_adjust(bottom=0.1)

        self.fig.tight_layout(rect=[0, 0.1,1,1])
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def display_share_y(self, plot_function, nrows=1, ncols=1, *args, **kwargs):
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

            # if the display function is only expecting one axis we need to convert the array of axis into just the array
            if nrows * ncols == 1:
                self.ax = self.ax[0]
        else:
            self.clear()  # Clear existing content for reuse

        self.ax2 = plot_function(self.ax, *args, **kwargs)

        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def add_button(self, label, position, callback=None):
        """Adds a button."""
        ax_button = self.fig.add_axes(position)
        button = Button(ax_button, label)
        button.on_clicked(self.on_submit)
        self.buttons.append(button)

    def on_submit(self, event):
        if all(self.valid_inputs.values()):
            self.is_ready = True

    def add_text_box(self, label, position, validation_type):
        """ Adds a text box and sets up validation. """
        ax_box = self.fig.add_axes(position)
        text_box = TextBox(ax_box, label)
        
        # Explicitly use self.validator and bind the method is_valid_peak
        text_box.on_submit(lambda text: self.store_text(label, self.validator, text))
        
        self.text_boxes[label] = text_box
        self.text_values[label] = ""
        self.validation_types[label] = validation_type  # Store validation function
        self.valid_inputs[label] = False  # Mark as not valid initially

    def store_text(self, label, validator, text):
        """ Stores input, validates it, and updates status. """
        self.text_values[label] = text
        validator.set_type(self.validation_types[label])
        if validator.type == 'end':
            self.end = text
            if validator.validate(self.start, text):  # Apply the validation rule using the validator instance
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Start Time: "] = True
                self.end = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'start':
            self.start = text
            if validator.validate(text, self.end):  # Apply the validation rule using the validator instance
                self.valid_inputs[label] = True
                self.valid_inputs["Enter End Time: "] = True
                self.start = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        else:
            # Call the validation method (e.g., is_valid_peak) on the validator instance
            if validator.validate(text):  # Apply the validation rule using the validator instance
                self.valid_inputs[label] = True
                self.remove_invalid_text()
            
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()

  
    def wait_for_valid_inputs(self):
        """Waits until all text boxes contain valid values."""
        while not self.is_ready:
            plt.pause(0.1)
        self.is_ready = False
        self.remove_info_text()
        return self.text_values  # Return valid inputs
    
    def add_info_text(self):
        if hasattr(self, 'info_ax'):
            self.info_ax.remove()
        self.info_ax = self.fig.add_axes([0.02, 0.07, 0.34, 0.05], facecolor='lightgrey')
        self.info_ax.set_xticks([])
        self.info_ax.set_yticks([])
        self.info_text = self.info_ax.text(0.5, 0.5, "1 for Log, 2 for Asinh, 3 for Beta", 
                                           ha='center', va='center',
                                           color='black', fontsize=12, fontweight='bold')
        
    def remove_info_text(self):
        if hasattr(self, 'info_ax'):
            self.info_ax.remove()
            del self.info_ax

    def add_invalid_text(self):
        """ Adds text to the figure to indicate invalid input. """
        message_height = 0.05  # Height of the message area
        if hasattr(self, 'invalid_ax'):
            self.invalid_ax.remove()  # Clear previous messages
    
        # Create a new axes for the message at the bottom of the figure
        self.invalid_ax = self.fig.add_axes([0.38, 0.05, 0.5, message_height], facecolor='lightgrey')
        self.invalid_ax.set_xticks([])
        self.invalid_ax.set_yticks([])

        # Display the message in the newly created message area
        self.invalid_text = self.invalid_ax.text(0.5, 0.5, "Invalid input, please try again", 
                                                ha='center', va='center', 
                                                color='red', fontsize=12, fontweight='bold')
        # self.fig.canvas.draw_idle()
        
    def remove_invalid_text(self):
        """ Removes invalid input text from the figure. """
        if hasattr(self, 'invalid_ax'):
            self.invalid_ax.remove()
            del self.invalid_ax  # Clean up the reference
