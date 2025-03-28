class Validator:
    def __init__(self):
        self.num_peaks = None  # Default value for num_peaks
        self.type = None
        self.penetrometer_data = None
        self.pore_pressure = None
        self.time_range = None
        
    def set_type(self, type):
        self.type = type

    def set_penetrometer_data(self, data):
        self.penetrometer_data = data

    def set_pore_pressure(self, data):
        self.pore_pressure = data

    def set_time_range(self, data):
        self.time_range = data

    def validate(self, data, data2=None):
        if self.type == 'peak':
            return self.is_valid_peak(data)
        elif self.type == 'spike':
            return self.is_valid_spike(data)
        elif self.type == 'correction':
            return self.is_valid_correction_type(data)
        elif self.type == 'ntk':
            return self.is_valid_ntk(data)
        elif self.type == 't_start' or self.type == 't_end':
            return self.is_valid_start_and_end(data, data2)
        elif self.type == 'p_start' or self.type == 'p_end':
            return self.is_valid_p_start_and_end(data, data2)
        elif self.type == 'p_inc' or self.type == 'p_dec':
            return self.is_valid_p_inc_and_dec(data, data2)
        else:
            return False
    
    def is_valid_ntk(self, ntk):
        try:
            ntk = float(ntk)
            return ntk > 0
        except:
            return False
    
    def is_valid_p_inc_and_dec(self, inc, dec):
        if inc == "" or inc is None:
            return False
        if dec == "" or dec is None:
            return False
        if int(inc) >= 0 and int(inc) < int(dec) and int(dec) <= self.pore_pressure.pressure_end:
            return True
        else:
            return False
        
    def is_valid_p_start_and_end(self, start, end):
        if start == "" or start is None:
            return False
        if end == "" or end is None:
            return False
        if int(start) >= 0 and int(start) < int(end) and int(end) <= len(self.penetrometer_data.g50g):
            return True
        else:
            return False

    def is_valid_start_and_end(self, start, end):
        if start == "" or start is None:
            return False
        if end == "" or end is None:
            return False
        if int(start) >= 0 and int(start) < int(end) and int(end) <= len(self.time_range):
            return True
        else:
            return False
    
    def is_valid_correction_type(self, correction_val):
        if int(correction_val) in range(1,4):
            return True
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