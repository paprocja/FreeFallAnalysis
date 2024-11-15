import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.buttons = []  # Store references to dynamically created buttons

    def clear(self):
        """
        Clears the current axes to prepare for new data.
        """
        self.ax.clear()
        for button in self.buttons:
            button.ax.remove()
        self.buttons.clear()

    def display(self, plot_function, *args, **kwargs):
        """
        Displays the plot by calling a provided plot function.

        Parameters
        ----------
        plot_function: callable
            A function that takes the axes object and any additional arguments.
        """
        self.clear()
        plot_function(self.ax, *args, **kwargs)
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def add_peak_buttons(self, peaks, callback):
        
        """
        Adds a button for each peak to the figure for interaction.

        Parameters
        ----------
        peaks: list
            List of peak numbers to create buttons for.
        callback: callable
            A function to call with the peak number when the button is pressed.
        """
        button_width = 0.1
        button_height = 0.05
        for i, peak in enumerate(peaks):
            position = [0.01 + i * (button_width + 0.01), 0.01, button_width, button_height]
            ax_button = self.fig.add_axes(position)
            button = Button(ax_button, f"Peak {peak}")
            button.on_clicked(lambda event, peak=peak: callback(peak))
            self.buttons.append(button)
