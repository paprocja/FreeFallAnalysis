def display_peak(figure_manager, peak, g2g, drop_end, peak_center):
    """
    Displays the peak using the figure manager.
    """
    def plot(ax):
        ax.set_xlim(0, len(peak) + 10)
        ax.plot(peak, label='peak')
        ax.plot(g2g, label ='2g')
        ax.scatter(drop_end, peak[drop_end], marker='x', label='End of drop', color='black')
        ax.legend(loc='upper right')
        ax.set_title(f"Peak at {peak_center}")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
    
    figure_manager.display(plot)

    figure_manager.add_text_box("Enter Spike Selection: ", [0.15, 0.05, 0.1, 0.05], 'spike')
    figure_manager.add_button("Confirm", [0.26, 0.05, 0.1, 0.05])

    input_values = figure_manager.wait_for_valid_inputs()
    return int(input_values["Enter Spike Selection: "])

def display_decel_vel_dep(figure_manager, depth, decelleration, velocity):
    """
    Displays the deceleration, velocity, and depth data in one plot.
    """
    def plot(ax):
        ax.invert_yaxis()
        ax.set_ylim(max(depth), 0)
        ax.set_xlim(0, max(max(decelleration), max(velocity)))
        ax.plot(decelleration, depth, linestyle='-', label='Deceleration')
        ax.plot(velocity, depth, linestyle='--', label='Velocity')
        ax.set_ylabel('Depth [Meters]')
        ax.set_xlabel('Deceleration [g] // Velocity [m/s]')
        ax.legend(loc='upper right')

    figure_manager.display(plot)
    figure_manager.add_text_box("Enter Correction Type: ", [0.15, 0.01, 0.1, 0.05], 'correction')
    figure_manager.add_button("Confirm", [0.26, 0.01, 0.1, 0.05])
    figure_manager.add_info_text("1 for Log, 2 for Asinh, 3 for Beta", 0.02, 0.07, 0.34)
    figure_manager.add_radio([0.85, 0.02, 0.05, 0.08])
    figure_manager.add_info_text("In water?", 0.72, 0.03, 0.12)
    input_values = figure_manager.wait_for_valid_inputs()
    return int(input_values["Enter Correction Type: "]), figure_manager.radio_result

def display_QSBC_for_K(figure_manager, qsbc_for_k):
    """
    Displays the quasi static bearing capacity
    """
    def plot(ax):
        ax.set_xlim(0, len(qsbc_for_k) + 10)
        ax.plot(qsbc_for_k, label='QSBC')
        ax.set_xlabel('Bearing Capacity')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Bearing Capacity')
        ax.legend(loc='upper right')


    figure_manager.display(plot)

    # for input colection
    figure_manager.add_text_box("Enter Start Time: ", [0.15, 0.07, 0.1, 0.05], 'start', time_range=len(qsbc_for_k))
    figure_manager.add_text_box("Enter End Time: ", [0.15, 0.01, 0.1, 0.05], 'end', time_range=len(qsbc_for_k))
    figure_manager.add_button("Confirm", [0.26, 0.03, 0.1, 0.05])
    input_values = figure_manager.wait_for_valid_inputs()
    start = int(input_values["Enter Start Time: "])
    end = int(input_values["Enter End Time: "])
    return start, end


def display_corrected_QSBC(figure_manager, line1val1, line1val2, line1ave, line2val1, line2val2, line2ave,
                            depth, velocity, decelleration, qdyn, start, end, tilt_x, tilt_y, do_pore):
    """
    Displays the corrected quasi static bearing capacity
    """
    corrected_depth = depth[start:end+1]*100
    def plot(ax):
        #plot the decel and velocity to the left side of figure
        ax[0].invert_yaxis()
        ax[0].set_ylim(max(depth), 0)
        ax[0].set_xlim(0, max(max(decelleration), max(velocity)))
        ax[0].plot(decelleration, depth, linestyle='-', label='Deceleration')
        ax[0].plot(velocity, depth, linestyle='--', label='Velocity')
        ax[0].set_ylabel('Depth [Meters]')
        ax[0].set_xlabel('Deceleration [g] // Velocity [m/s]')
        ax[0].legend(loc='upper right')
        

        #Plot the Correction averages and the dynamic on the right side of figure
        ax[1].invert_yaxis()
        ax[1].set_ylim(max(corrected_depth), 0)
        ax[1].set_xlim(0, max(max(line1ave), max(line2ave), max(qdyn[start:end+1])/1000))
        
        #first correciton average line
        ax[1].plot(line1ave, corrected_depth, label='QSBC(av) k = 1.0 & 1.5')
        ax[1].fill_betweenx(corrected_depth, line1val1, line1val2, color='grey', alpha=0.3)

        #second correction average line
        ax[1].plot(line2ave, corrected_depth, label='QSBC(av) k = 0.2 & 0.4')
        ax[1].fill_betweenx(corrected_depth, line2val1, line2val2, color='grey', alpha=0.3)
        
        #plot the dynamic bearing capacity
        ax[1].plot(qdyn[start:end+1]/1000, corrected_depth, label='Qdyn')
        
        ax[1].set_xlabel('QSBC [kPa]')
        ax[1].set_ylabel('Depth [CM]')
        ax[1].set_title('QSBC corrections & Q_dynamic')
        ax[1].legend(loc='upper right')

    figure_manager.display(lambda axs :plot(axs), nrows=1, ncols = 2)
    figure_manager.add_info_text(f"Tilt x:  {tilt_x:.6f}, Tilt y: {tilt_y:.6f}", 0.25, 0.05, 0.50)

    figure_manager.add_button("Continue?", [0.76, 0.05, 0.1, 0.05])
    
    if not do_pore:
        figure_manager.add_radio([0.86, 0.02, 0.05, 0.08])
        figure_manager.wait_for_valid_inputs()
        return figure_manager.radio_result
    else:
        figure_manager.wait_for_valid_inputs()
        return None
    # figure_manager.add_info_text("Resart?", 0.76, 0.00, 0.1)
    

#Have each field represent a portion of display to allow this to be re-used for each graph
def display_selected_peak(figure_manager, val, peak):
    """
    Displays the peak using the figure manager.
    """
    def plot(ax):
        ax.set_xlim(0, len(peak.peak) + 10)
        ax.plot(peak.peak, label='peak')
        ax.plot(peak.g2g, label ='2g')
        ax.scatter(peak.end_of_drop, peak.peak[peak.end_of_drop], marker='x', label='End of drop', color='black')
        ax.legend(loc='upper right')
        ax.set_title(f"Peak at {peak.peak_center}")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
        ax.plot(val, peak.peak[val], 'rx')
    
    figure_manager.display(plot)

def display_selected_range(figure_manager, qsbc_for_k, valStart, valEnd):
    def plot(ax):
        ax.set_xlim(0, len(qsbc_for_k) + 10)
        ax.plot(qsbc_for_k, label='QSBC')
        ax.set_xlabel('Bearing Capacity')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Bearing Capacity')
        ax.legend(loc='upper right')
        ax.plot(valStart, qsbc_for_k[valStart], 'rx')
        ax.plot(valEnd, qsbc_for_k[valEnd], 'rx')
    figure_manager.display(plot)
