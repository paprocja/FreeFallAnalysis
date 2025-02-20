import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#TODO: Include area
def display_peak(figure_manager, peak, g2g, drop_end, peak_center, save_data, filename="peak_data"):
    """
    Displays the peak using the figure manager.
    """
    def plot(ax):
        ax.plot(peak, label='peak')
        ax.plot(g2g, label ='2g')
        ax.scatter(drop_end, peak[drop_end], marker='x', label='End of drop', color='black')
        ax.legend(loc='upper right')
        ax.set_title(f"Peak at {peak_center}")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
    
    if save_data:
        df = pd.DataFrame({"Peak": peak, "G2G": g2g})
        filename1 = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        df.to_csv('saved_data/' + filename + '_' + filename1 + '.csv', index=False)
        

    figure_manager.display(plot)

def display_decel_vel_dep(figure_manager, depth, deceleration, velocity, save_data, filename="decel_vel_dep"):
    """
    Displays the deceleration, velocity, and depth data in one plot.
    """
    def plot(ax):
        ax.invert_yaxis()
        ax.set_ylim(max(depth), 0)
        ax.set_xlim(0, max(max(deceleration), max(velocity)))
        ax.plot(deceleration, depth, linestyle='-', label='Deceleration')
        ax.plot(velocity, depth, linestyle='--', label='Velocity')
        ax.set_ylabel('Depth [Meters]')
        ax.set_xlabel('Deceleration [g] // Velocity [m/s]')
        ax.legend(loc='upper right')

    if save_data:
        df = pd.DataFrame({"Deceleration": deceleration, "Velocity": velocity, "Depth (M)": depth})
        filename1 = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        df.to_csv('saved_data/' + filename + '_' + filename1 + '.csv', index=False)

    figure_manager.display(plot)

def display_QSBC_for_K(figure_manager, qsbc_for_k, save_data, filename="bearing_capacity"):
    """
    Displays the quasi static bearing capacity
    """
    def plot(ax):
        ax.plot(qsbc_for_k, label='QSBC')
        ax.set_xlabel('Bearing Capacity')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Bearing Capacity')
        ax.legend(loc='upper right')

    if save_data:
        df = pd.DataFrame({"QSBC": qsbc_for_k})
        filename1 = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        df.to_csv('saved_data/' + filename + '_' + filename1 + '.csv', index=False)

    figure_manager.display(plot)


def display_corrected_QSBC(fig_manager, line1val1, line1val2, line1ave, line2val1, line2val2, line2ave,
                            depth, velocity, deceleration, qdyn, start, end, save_data, filename="corrected_qsbc"):
    """
    Displays the corrected quasi static bearing capacity
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

    if save_data:
        #Save area and strain-rate correction factor
        df = pd.DataFrame({"Dynamic Bearing Capacity": qdyn[start:end+1] / 1000, "Depth(CM)": corrected_depth})
        filename1 = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        df.to_csv('saved_data/' + filename + '_' + filename1 + '.csv', index=False)

    fig_manager.display(lambda axs :plot(axs), nrows=1, ncols = 2)


#Have each field represent a portion of display to allow this to be re-used for each graph
def display_selected_peak(fig_manager, val, peak):
    """
    Displays the peak using the figure manager.
    """
    def plot(ax):
        ax.plot(peak.peak, label='peak')
        ax.plot(peak.g2g, label ='2g')
        ax.scatter(peak.end_of_drop, peak.peak[peak.end_of_drop], marker='x', label='End of drop', color='black')
        ax.legend(loc='upper right')
        ax.set_title(f"Peak at {peak.peak_center}")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
        plt.plot(val, peak.peak[val], 'rx')
    
    fig_manager.display(plot)

def display_selected_range(fig_manager, qsbc_for_k, valStart, valEnd):
    def plot(ax):
        ax.plot(qsbc_for_k, label='QSBC')
        ax.set_xlabel('Bearing Capacity')
        ax.set_ylabel('Depth')
        ax.set_title('Depth x Bearing Capacity')
        ax.legend(loc='upper right')
        plt.plot(valStart, qsbc_for_k[valStart], 'rx')
        plt.plot(valEnd, qsbc_for_k[valEnd], 'rx')
    fig_manager.display(plot)
