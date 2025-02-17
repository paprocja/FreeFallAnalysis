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
        self.validation_rules = {}
        self.valid_inputs = {}
        self.validator = Validator()  # Only instantiate once, re-use it

    def clear(self):
        """Clears the current axes and resets the figure."""
        if isinstance(self.ax, (list, np.ndarray)):  # Handle multiple axes
            for sub_ax in self.ax:
                sub_ax.clear()
        else:
            self.ax.clear()

        for button in self.buttons:
            button.ax.remove()  # Remove buttons from the figure
        self.buttons.clear()

        for label, text_box in self.text_boxes.items():  # Iterate directly over the dictionary
            text_box.ax.remove()  # Correctly access text_box
        self.text_boxes.clear()
        self.text_values.clear()
        self.validation_rules.clear()
        self.valid_inputs.clear()

    def display(self, plot_function, nrows=1, ncols=1, *args, **kwargs):
        """Displays the plot with subplots if specified."""
        if nrows * ncols != (len(self.ax) if isinstance(self.ax, np.ndarray) else 1):
            self.fig.clear()
            self.ax = self.fig.subplots(nrows=nrows, ncols=ncols, squeeze=False)
            self.ax = self.ax.flatten()  # Flatten for easy indexing
        else:
            self.clear()  # Clear existing content for reuse

        plot_function(self.ax, *args, **kwargs)

        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def add_button(self, label, position, callback=None):
        """Adds a button."""
        ax_button = self.fig.add_axes(position)
        button = Button(ax_button, label)
        button.on_clicked(callback if callback else lambda event: None)
        self.buttons.append(button)

    def add_text_box(self, label, position, validation_rule):
        """ Adds a text box and sets up validation. """
        ax_box = self.fig.add_axes(position)
        text_box = TextBox(ax_box, label)
        
        # Explicitly use self.validator and bind the method is_valid_peak
        text_box.on_submit(lambda text: self.store_text(label, self.validator, text))
        
        self.text_boxes[label] = text_box
        self.text_values[label] = ""
        self.validation_rules[label] = validation_rule  # Store validation function
        self.valid_inputs[label] = False  # Mark as not valid initially

    def store_text(self, label, validator, text):
        """ Stores input, validates it, and updates status. """
        self.text_values[label] = text
        # Call the validation method (e.g., is_valid_peak) on the validator instance
        if validator.is_valid_peak(text):  # Apply the validation rule using the validator instance
            self.valid_inputs[label] = True
            self.remove_invalid_text()
        else:
            self.valid_inputs[label] = False
            print(f"Invalid input for {label}, please try again.")
            self.add_invalid_text()

  
    def wait_for_valid_inputs(self):
        """Waits until all text boxes contain valid values."""
        while not all(self.valid_inputs.values()):  # Check if all are valid
            plt.pause(0.1)  # Keep UI responsive
        return self.text_values  # Return valid inputs

    def add_invalid_text(self):
        """ Adds text to the figure to indicate invalid input. """
        if hasattr(self, 'invalid_text'):  # If invalid text exists, remove it first
            self.invalid_text.remove()

         # If there is only one Axes object, use it directly
        if isinstance(self.ax, plt.Axes):  # Single Axes
            self.invalid_text = self.ax.text(0.5, 0.01, "Invalid input, please try again", 
                                            transform=self.ax.transAxes, 
                                            ha='center', va='center', 
                                            color='red', fontsize=12, fontweight='bold')
        else:  # Multiple Axes (array)
            self.invalid_text = self.ax[0].text(0.5, 0.01, "Invalid input, please try again", 
                                                transform=self.ax[0].transAxes, 
                                                ha='center', va='center', 
                                                color='red', fontsize=12, fontweight='bold')
        
    def remove_invalid_text(self):
        """ Removes invalid input text from the figure. """
        if hasattr(self, 'invalid_text'):
            self.invalid_text.remove()
            del self.invalid_text  # Clean up the reference
