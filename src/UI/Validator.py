class Validator:
    def __init__(self):
        self.num_peaks = None  # Default value for num_peaks
        
    def set_num_peaks(self, num_peaks):
        """Set the number of peaks dynamically."""
        self.num_peaks = num_peaks

    def is_valid_peak(self, selected_peak):
        """Validates that the selected peak is within the valid range."""
        if self.num_peaks is None:
            raise ValueError("num_peaks must be set before validation.")
        
        if int(selected_peak) - 1 in range(0, self.num_peaks):
            return True
        else:
            return False