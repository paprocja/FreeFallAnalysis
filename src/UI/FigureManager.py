import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np  # numpy needed to support the change from single ax to multiple
from datetime import datetime

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons

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

        plt.subplots_adjust(bottom=0.1)

        axbutton = plt.axes([0.4, 0.005, 0.1, 0.05])
        png_button = Button(axbutton, 'Save as PNG')
        self.buttons.append(png_button)
        png_button.on_clicked(self.save_to_png)

        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def save_to_png(self, event):
        filename = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        plt.savefig('saved_data/' + 'figure_' + filename + '.png')

