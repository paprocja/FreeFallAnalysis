import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np  # numpy needed to support the change from single ax to multiple
import time

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons
        self.text_boxes = {}
        self.text_values = {} 
        self.validation_constraints = {} 
        self.valid_inputs = {}  
    
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

        for text_box in self.text_boxes.items():
            text_box.ax.remove()
        self.text_boxes.clear()
        self.text_values.clear()
        self.validation_rules.clear()
        self.valid_inputs.clear()

    def display(self, plot_function, nrows=1, ncols=1, *args, **kwargs):
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

        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def add_button(self, label, position, callback=None):
        """ Adds a button. """
        ax_button = self.fig.add_axes(position)
        button = Button(ax_button, label)
        button.on_clicked(callback if callback else lambda event: None)
        self.buttons.append(button)

    def add_text_box(self, label, position, validation_rule):
        """ Adds a text box and sets up validation. """
        ax_box = self.fig.add_axes(position)
        text_box = TextBox(ax_box, label)
        text_box.on_submit(lambda text: self.store_text(label, text))
        self.text_boxes[label] = text_box
        self.text_values[label] = ""
        self.validation_rules[label] = validation_rule  # Store validation function
        self.valid_inputs[label] = False  # Mark as not valid initially

    def store_text(self, label, text):
        """ Stores input, validates it, and updates status. """
        self.text_values[label] = text
        if self.validation_rules[label](text):  # Apply validation rule
            self.valid_inputs[label] = True
        else:
            self.valid_inputs[label] = False
            print(f"Invalid input for {label}, please try again.")

    def wait_for_valid_inputs(self):
        """ Waits until all text boxes contain valid values. """
        while not all(self.valid_inputs.values()):  # Check if all are valid
            plt.pause(0.1)  # Keep UI responsive
        return self.text_values  # Return valid inputs