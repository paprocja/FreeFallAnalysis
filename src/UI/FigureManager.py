import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons
import numpy as np  # numpy needed to support the change from single ax to multiple
from datetime import datetime
from .Validator import Validator  # Import the Validator class

class FigureManager:
    def __init__(self, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create the figure and axes once
        self.buttons = []  # Store references to dynamically created buttons
        self.radio_buttons = []
        self.radio_result = False
        self.text_boxes = {}
        self.text_values = {}
        self.validation_types = {}
        self.valid_inputs = {}
        self.validator = Validator()  # Only instantiate once, re-use it
        self.is_ready = False
        self.start = None
        self.end = None
        self.p_start = None
        self.p_end = None
        self.p_inc = None
        self.p_dec = None
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
        self.buttons = []

        for radio in self.radio_buttons:
            radio.ax.remove()
        self.radio_buttons = []

        for label, text_box in self.text_boxes.items():  # Iterate directly over the dictionary
            text_box.ax.remove()  # Correctly access text_box
        self.text_boxes.clear()
        self.text_values.clear()
        self.validation_types.clear()
        self.valid_inputs.clear()
        self.radio_result = False
        self.remove_info_text()

    def display(self, plot_function, nrows=1, ncols=1, *args, **kwargs):
        """Displays the plot with subplots if specified."""
        if nrows * ncols != (len(self.ax) if isinstance(self.ax, np.ndarray) else 1):
            self.clear()
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
            self.clear()
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

        plt.subplots_adjust(bottom=0.1)

        axbutton = plt.axes([0.4, 0.005, 0.1, 0.05])
        png_button = Button(axbutton, 'Save as PNG')
        self.buttons.append(png_button)
        png_button.on_clicked(self.save_to_png)

        self.fig.tight_layout()
        self.ax2 = plot_function(self.ax, *args, **kwargs)
        
        plt.subplots_adjust(bottom=0.1)
    
        self.fig.tight_layout(rect=[0, 0.1,1,1])
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def save_to_png(self, event):
        #Save to fig file format
        filename = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        plt.savefig('saved_data/' + 'figure_' + filename + '.png')

        self.ax2 = plot_function(self.ax, *args, **kwargs)
        
        plt.subplots_adjust(bottom=0.1)
    
        self.fig.tight_layout(rect=[0, 0.1,1,1])
        self.fig.canvas.draw_idle()
        plt.show(block=False)

    def add_button(self, label, position, callback=None):
        """Adds a button."""
        ax_button = self.fig.add_axes(position)
        button = Button(ax_button, label)
        button.on_clicked(self.on_submit)
        self.buttons.append(button)


    def on_submit(self, event):
        """
        When on click is called from a button check if all input options are validated,
          and then set the figure to be ready to move on.

        Parameters
        ----------
        event: lambda
            Nothing is set here for this program.
              it is simple needed to be compiled for a on_clicked parameter
        """
        if all(self.valid_inputs.values()):
            self.is_ready = True

    def add_text_box(self, label, position, validation_type, time_range=None, pen_data=None, pressure=None):
        """ 
        Adds a text box and sets up validation. 
        Parameters
        ----------
        label: string
            The name string fo the textbox being created
        position: float[]
            The [x_offset, y_offset, width, height] used for the widet
        validation_type: string
            Used to assign a validation type for the input value to be run against
        time_range: int
            Max range possible for the value. Used for validation later
        pen_data: Obj (penetrometer_data)
            Used later for validation range check
        pressure: Obj (pore_pressure)
            Used later for validation range check
        """
        ax_box = self.fig.add_axes(position)
        text_box = TextBox(ax_box, label)
        

        if time_range is not None:
            self.validator.set_time_range(time_range)
        if pen_data is not None:
            self.validator.set_penetrometer_data(pen_data)
        if pressure is not None:
            self.validator.set_pore_pressure(pressure)

        # Explicitly use self.validator and bind the method is_valid_peak
        text_box.on_submit(lambda text: self.store_text(label, self.validator, text))
        
        self.text_boxes[label] = text_box
        self.text_values[label] = ""
        self.validation_types[label] = validation_type  # Store validation function
        self.valid_inputs[label] = False  # Mark as not valid initially

    def store_text(self, label, validator, text):
        """ 
        Stores input, validates it, and updates status. 
        
        Parameters
        ----------
        label: string
            The name of the textbox being run
        validator: validator
            The instance of the validator being run for the program
        text: string
            The info currently stored in the textbox widget
        
        """
        self.text_values[label] = text
        validator.set_type(self.validation_types[label])
        # Apply the validation rule using the validator instance. 
        #   Special cases for anything with multiple inputs.
        if validator.type == 'end':
            self.end = text
            if validator.validate(self.start, text):  
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Start Time: "] = True
                self.end = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'start':
            self.start = text
            if validator.validate(text, self.end):
                self.valid_inputs[label] = True
                self.valid_inputs["Enter End Time: "] = True
                self.start = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'p_end':
            self.p_end = text
            if validator.validate(self.p_start, text):
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Pressure Start: "] = True
                self.p_end = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'p_start':
            self.p_start = text
            if validator.validate(text, self.p_end):
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Pressure End: "] = True
                self.p_start = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'p_dec':
            self.p_dec = text
            if validator.validate(self.p_inc, text):
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Profile Increase: "] = True
                self.p_dec = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        elif validator.type == 'p_inc':
            self.p_inc = text
            if validator.validate(text, self.p_dec): 
                self.valid_inputs[label] = True
                self.valid_inputs["Enter Profile Decrease: "] = True
                self.p_inc = text
                self.remove_invalid_text()
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()
        else:
            if validator.validate(text):  
                self.valid_inputs[label] = True
                self.remove_invalid_text()
            
            else:
                self.valid_inputs[label] = False
                self.add_invalid_text()

    def add_radio(self, position):
        """
        Creates a yes/no radio button widget on the screen

        Parameters
        ----------
        position: float[]
            The location of where the widget goes [x_offset, y_offset, width, height]

        """

        rax = self.fig.add_axes(position, facecolor='lightgrey')

        radio = RadioButtons(rax, ('Yes', 'No'))

        #set the active at the start be 'No'
        radio.set_active(1)

        radio.on_clicked(self.yes_no_from_radio)
        self.radio_buttons.append(radio)



    def yes_no_from_radio(self, label):
        """
        sets the result of the radio button based on what value is clicked.

        Parameters
        ----------
        label: string
            The name of the clicked radio button
        """
        if label == 'Yes':
            self.radio_result = True
        else:
            self.radio_result = False
            

  
    def wait_for_valid_inputs(self):
        """
        Waits until all text boxes contain valid values.
        
        Return:
            A map of all the text_values that are valid.  ---> ex: ('label', value)
        """
        while not self.is_ready:
            plt.pause(0.1)
        self.is_ready = False
        
        return self.text_values  # Return valid inputs
    
    def add_info_text(self, text, x_off, y_off, width):
        """
        Adds a default axes to be used to but text into

        Parameters
        ----------
        text: string
            What you want the info to be displayed in the box
        x_off: float
            The x_offset to be used for the possition of the widget
        y_off: float
            The y_offset to be used for the possition of the widget
        width: float
            The width of the widget for the information to be but into
        """

        if hasattr(self, 'info_ax'):
            self.info_ax.remove()
        self.info_ax = self.fig.add_axes([x_off, y_off, width, 0.05], facecolor='lightgrey')
        self.info_ax.set_xticks([])
        self.info_ax.set_yticks([])
        self.info_text = self.info_ax.text(0.5, 0.5, text, 
                                           ha='center', va='center',
                                           color='black', fontsize=12)
        
    def remove_info_text(self):
        """
        Removes any instances of info_text widgets currently in the figure
        """

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


    # def plot_point(self, x_val, y_val):
    #     x_val = int(x_val)
    #     y_val = int(y_val)
    #     self.ax.scatter([x_val], [y_val], color='red', s=100, marker='x')  # Mark with red cross
    #     self.ax.annotate(f'Marked at ({x_val}, {y_val})', (x_val, y_val),
    #                       textcoords="offset points", xytext=(0,10), ha='center')

