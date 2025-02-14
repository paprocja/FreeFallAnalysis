from Validator import Validator

def display_initial_data(figure_manager, g2g, g18g, g50g, g200g, g250g, peaks, heights, number_peaks):
    """
    Displays initial data and peaks using the figure manager.
    """
    def plot(ax):
        ax.plot(g2g, linestyle='-', linewidth=.5, label="2g", color='green')
        ax.plot(g18g, linestyle='-', linewidth=.5, label="18g", color='red')
        ax.plot(g50g, linestyle='-', linewidth=.5, label="50g", color='blue')
        ax.plot(g200g, linestyle='-', linewidth=.5, label="200g", color='brown')
        ax.plot(g250g, linestyle='-', linewidth=.5, label="250g", color='purple')
        ax.scatter(peaks, heights, marker='*', label='peaks', color='black')
        for i, txt in enumerate(range(1, number_peaks + 1)):
            ax.annotate(txt, (peaks[i], heights[i]), xytext=(5, 5), textcoords='offset points',
                        ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
                        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        ax.legend(loc='upper right')
        ax.set_xlabel('Steps')
        ax.set_ylabel('Deceleration (g)')
        ax.set_title('Initial Data Visualization')

    figure_manager.display(plot)

    figure_manager.add_text_box("Start Index", [0.4, 0.02, 0.15, 0.05], Validator.is_valid_peak)
    figure_manager.add_button("Submit", [0.8, 0.02, 0.1, 0.05])
    peak_number = fig_manager.wait_for_valid_inputs()
    return peak_number