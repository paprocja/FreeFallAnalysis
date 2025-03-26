from Data.PorePressure import PorePressure

def display_peaks_and_ppm(figure_manager, penetrometer_data, pressure_start=0, pressure_end=0, display_range=False):
    """
    Displays initial data and peaks using the figure manager.
    """
    def plot(ax):
        ax.plot(penetrometer_data.g2g, linestyle='-', linewidth=.5, label="2g", color='green')
        ax.plot(penetrometer_data.g18g, linestyle='-', linewidth=.5, label="18g", color='red')
        ax.plot(penetrometer_data.g50g, linestyle='-', linewidth=.5, label="50g", color='blue')
        ax.plot(penetrometer_data.g200g, linestyle='-', linewidth=.5, label="200g", color='brown')
        ax.plot(penetrometer_data.g250g, linestyle='-', linewidth=.5, label="250g", color='purple')
        ax.scatter(penetrometer_data.peaks, penetrometer_data.heights, marker='*', label='peaks', color='black')

        ax2 = ax.twinx()
        ax2.plot(penetrometer_data.ppm, linestyle='-', linewidth=.5, label="ppm", color='orange')

        if display_range:
            ax2.plot(pressure_start, penetrometer_data.ppm[pressure_start], 'rx')
            ax2.plot(pressure_end, penetrometer_data.ppm[pressure_end], 'rx')

        # add an invisible line to the plot so we can add ppm to the legend
        ax.plot([], [], label = 'ppm', color='orange')

        for i, txt in enumerate(range(1, penetrometer_data.number_peaks + 1)):
            ax.annotate(txt, (penetrometer_data.peaks[i], penetrometer_data.heights[i]), xytext=(5, 5), textcoords='offset points',
                        ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
                        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        
        ax.legend(loc='upper right')
        ax.set_xlabel('Steps')
        ax.set_ylabel('Deceleration (g)')
        ax.set_title('Pore Pressure')

        return ax2

    figure_manager.display_share_y(plot)
    figure_manager.add_text_box("Enter Pressure Start: ", [0.15, 0.07, 0.1, 0.05], 'p_start', pen_data=penetrometer_data)
    figure_manager.add_text_box("Enter Pressure End: ", [0.15, 0.01, 0.1, 0.05], 'p_end', pen_data=penetrometer_data)
    figure_manager.add_button("Confirm", [0.26, 0.03, 0.1, 0.05])
    input_values = figure_manager.wait_for_valid_inputs()
    p_start = int(input_values["Enter Pressure Start: "])
    p_end = int(input_values["Enter Pressure End: "])
    return p_start, p_end

def display_deceleration_profile(figure_manager, pore_pressure: PorePressure, start=0, end=0, display_range=False):
    def plot(ax):
        ax.set_xlim(0, len(pore_pressure.deceleration_profile) + 10)
        ax.plot(pore_pressure.deceleration_profile, linestyle='-', linewidth=.5, label="2g", color='blue')
        ax.set_title('Deceleration Profile')

        if display_range:
            ax.plot(start, pore_pressure.deceleration_profile[start], 'rx')
            ax.plot(end, pore_pressure.deceleration_profile[end], 'rx')

    figure_manager.display(plot)
    figure_manager.display_share_y(plot)
    figure_manager.add_text_box("Enter Profile Increase: ", [0.15, 0.07, 0.1, 0.05], 'p_inc', pressure=pore_pressure)
    figure_manager.add_text_box("Enter Profile Decrease: ", [0.15, 0.01, 0.1, 0.05], 'p_dec', pressure=pore_pressure)
    figure_manager.add_button("Confirm", [0.26, 0.03, 0.1, 0.05])
    input_values = figure_manager.wait_for_valid_inputs()
    p_inc = int(input_values["Enter Profile Increase: "])
    p_dec = int(input_values["Enter Profile Decrease: "])
    return p_inc, p_dec

def display_pore_pressure(figure_manager, pore_pressure: PorePressure):
    def plot(ax):
        ax.set_xlim(-25, max(pore_pressure.hydrostatic_pressure) + 25)

        # Deceleration
        ax.plot(pore_pressure.raw_deceleration, pore_pressure.depth, linestyle='-', linewidth='0.5', label='Dec (g)', color='blue')

        # Velocity
        ax.plot(pore_pressure.velocity, pore_pressure.depth, linestyle='-', linewidth='0.5', label='Velocity (m/s)', color='red')

        # Hydrostatic pressure
        ax.plot(pore_pressure.hydrostatic_pressure, pore_pressure.depth, linestyle='-', linewidth='0.5', label='Hydrostatic Pressure', color='black')

        # Point of impact
        ax.plot([pore_pressure.min_deceleration, pore_pressure.max_measured_pressure], [pore_pressure.point_of_impact, pore_pressure.point_of_impact],
                linestyle='--', linewidth = 1, label='Point of impact', color='purple')

        # Point of impact plus
        ax.plot([pore_pressure.min_deceleration, pore_pressure.max_measured_pressure], [pore_pressure.point_of_impact_plus, pore_pressure.point_of_impact_plus],
                linestyle='--', linewidth = 1, label='Point of impact + 8.833cm', color='black')
        
        # Measured pressure
        ax.plot(pore_pressure.measured_pressure, pore_pressure.depth, linestyle='-', linewidth='1', label='Measured Pressure', color='green')

        # Bernouli pressure
        ax.plot(pore_pressure.bernoulli_pressure, pore_pressure.depth, linestyle='-', linewidth='1', label='Bernouli Pressure', color='pink')

        ax.legend(loc='upper right')
        ax.set_xlabel('dec(g), v(m/s), and Pressure (kPa)')
        ax.set_ylabel('Vertical Distance (m)')
        ax.set_title('Pressures')


    figure_manager.display(plot)
    figure_manager.add_button("Continue?", [0.76, 0.05, 0.1, 0.05])
    figure_manager.add_radio([0.86, 0.02, 0.05, 0.08])
    figure_manager.wait_for_valid_inputs()
    return figure_manager.radio_result

