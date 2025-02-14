class Validator:

    def is_valid_peak(self, selected_peak):
        """
        Returns if a selected peak is within the range of peaks.

        Parameters
        ----------
        selected_peak: int
        The peak input by a user that needs to be validated
        """
        if selected_peak - 1 in range(0, self.number_peaks):
            return True
        else:
            return False