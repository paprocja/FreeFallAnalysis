def display_Su_for_K(figure_manager, su):
    """
    Displays the undrained shear strength in units of Kpa
    """
    def plot(ax):
        ax.set_xlim(0, len(su) + 10)
        ax.plot(su, label='QSBC')
        ax.set_xlabel('Undrained Shear Strength')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Bearing Capacity')
        ax.legend(loc='upper right')


    figure_manager.display(plot)

    # for input colection
    figure_manager.add_text_box("Enter Start Time: ", [0.15, 0.07, 0.1, 0.05], 'start', time_range=len(su))
    figure_manager.add_text_box("Enter End Time: ", [0.15, 0.01, 0.1, 0.05], 'end', time_range=len(su))
    figure_manager.add_button("Confirm", [0.26, 0.03, 0.1, 0.05])
    input_values = figure_manager.wait_for_valid_inputs()
    start = int(input_values["Enter Start Time: "])
    end = int(input_values["Enter End Time: "])
    return start, end

