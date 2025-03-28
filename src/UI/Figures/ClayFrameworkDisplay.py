def display_Su_for_K(figure_manager, su, do_pore):
    """
    Displays the undrained shear strength in units of Kpa
    """
    def plot(ax):
        ax.set_xlim(0, len(su) + 10)
        ax.plot(su, label='QSBC')
        ax.set_xlabel('Undrained Shear Strength')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Undrained Shear Strength (Kpa)')
        ax.legend(loc='upper right')

    figure_manager.display(plot)
    figure_manager.add_button("Continue?", [0.76, 0.05, 0.1, 0.05])
    if not do_pore:
        figure_manager.add_radio([0.86, 0.02, 0.05, 0.08])
        figure_manager.wait_for_valid_inputs()
        return figure_manager.radio_result
    else:
        figure_manager.wait_for_valid_inputs()
        return None


def redisplay_corrected_qsbc(figure_manager, line1val1, line1val2, line1ave, line2val1, line2val2, line2ave,
                            depth, velocity, deceleration, qdyn, start, end, tilt_x, tilt_y):
    """
    Re-displays the corrected quasi static bearing capacity
    """
    corrected_depth = depth[start:end+1]*100
    def plot(ax):
        #plot the decel and velocity to the left side of figure
        ax[0].invert_yaxis()
        ax[0].set_ylim(max(depth), 0)
        ax[0].set_xlim(0, max(max(deceleration), max(velocity)))
        ax[0].plot(deceleration, depth, linestyle='-', label='Deceleration')
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
    
    # NTK input box
    ntk_label = "Enter NTK: "

    # for input colection
    figure_manager.add_text_box(ntk_label, [0.1, 0.05, 0.1, 0.05], 'ntk')
    input_values = figure_manager.wait_for_valid_inputs()
    return input_values[ntk_label]


  