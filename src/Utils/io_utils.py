from Data.Peak import Peak
from UI.Figures.PeakDisplay import *
from UI.Figures.PorePressureDisplay import *

def prompt_user_for_val(input_msg, output_msg, is_valid, data_type='i'):
    """
    Prompts the user for an integer or float.
    Will continue to ask user for input until a valid input is provided.

    Parameters
    ----------
    input_msg: str
        The prompt displayed to the user asking for input
    output_msg: str
        The prompt displayed to the user after valid input is entered
    is_valid: Any -> Boolean
        A function of that validates the user input. Returns true or false.
    data_type: str
        The type of input expected from the user, defaults to 'i' for integer
    """
    invalid = True
    while invalid:
        # prompt user to select peaks
        selection = input(input_msg)
        try:
            # get the value the user entered for the specific data type
            if data_type == 'f':
                selection = float(selection)
            elif data_type == 's':
                selection = str(selection)
            else:
                selection = int(selection)

            # validate the users input
            if is_valid(selection):
                # if valid alert user and return value
                invalid = False
                print(output_msg)
                return selection
            else:
                print(f'{selection} is not a valid choice!')
        except Exception as _:
            match data_type:
                case 'f': type = 'float'
                case 's': type = 'string' 
                case _: type = 'integer'
            print(f'{selection} is not a valid {type}!')

def confirm_peak_range(fig_manager, qsbc_for_k, valStart, valEnd) -> bool:
    def is_valid_confirmation(val):
        if (val == 1 or val == 0):
            return True
        return False
    
    display_selected_range(fig_manager, qsbc_for_k, valStart, valEnd)

    prompt_msg = f"Would you like to confirm this range? (1 for yes, 0 for no)\n"
    happy = ""
    return_val = prompt_user_for_val(prompt_msg, happy, is_valid_confirmation)
    if (return_val == 0):
        return False
    return True

def confirm_pore_pressure_range(figure_manager, penetrometer_data, start, end) -> bool:
    def is_valid_confirmation(val):
        if (val == 1 or val == 0):
            return True
        return False
    
    display_peaks_and_ppm(figure_manager, penetrometer_data, start, end, True)

    prompt_msg = f"Would you like to confirm this range? (1 for yes, 0 for no)\n"
    happy = ""
    return_val = prompt_user_for_val(prompt_msg, happy, is_valid_confirmation)
    if (return_val == 0):
        return False
    return True

def confirm_deceleration_profile_range(figure_manager, pore_pressure, start, end) -> bool:
    def is_valid_confirmation(val):
        if (val == 1 or val == 0):
            return True
        return False
    
    display_deceleration_profile(figure_manager, pore_pressure, start, end, True)

    prompt_msg = f"Would you like to confirm this range? (1 for yes, 0 for no)\n"
    happy = ""
    return_val = prompt_user_for_val(prompt_msg, happy, is_valid_confirmation)
    if (return_val == 0):
        return False
    return True

def confirm_input_spike(fig_manager, peak, val) -> bool:
    def is_valid_confirmation(val):
        if (val == 1 or val == 0):
            return True
        return False
    display_selected_peak(fig_manager, val, peak)
    prompt_msg = f"Would you like to confirm this input? (1 for yes, 0 for no)\n"
    happy = ""
    return_val = prompt_user_for_val(prompt_msg, happy, is_valid_confirmation)
    if (return_val == 0):
        return False
    return True