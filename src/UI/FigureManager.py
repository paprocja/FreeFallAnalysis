import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np  # numpy needed to support the change from single ax to multiple

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons
        self.ax2 = None # A second axis that can be used if two plots need different y-axis

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

        if self.ax2 != None:
            self.ax2.clear()
            self.ax2 = None

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

            # if the display function is only expecting one axis we need to convert the array of axis into just the array
            if nrows * ncols == 1:
                self.ax = self.ax[0]
        else:
            self.clear()  # Clear existing content for reuse

        plot_function(self.ax, *args, **kwargs)

        self.fig.tight_layout()
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

