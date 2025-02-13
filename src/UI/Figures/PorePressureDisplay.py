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
