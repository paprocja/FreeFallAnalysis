class Validator:
    def __init__(self):
        self.num_peaks = None  # Default value for num_peaks
        self.type = None
        
    def set_type(self, type):
        self.type = type

    def validate(self, data):
        if self.type == 'peak':
            return self.is_valid_peak(data)
        if self.type == 'spike':
            return self.is_valid_spike(data)
        else:
            return False

    def is_valid_spike(self, spike):
        if int(spike) > 0 and int(spike) < 2000:
            return True 
        else:
            return False

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