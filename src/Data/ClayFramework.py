from Data.Peak import Peak
import numpy as np

class ClayFramework:

    def __init__(self, peak: Peak, qsbc):
        self.peak = peak
        self.correction_method = None
        self.min = None
        self.max = None
        self.ntk_min = None
        self.ntk_max = None
        self.su = None
        self.qsbc = qsbc

    def select_other_correction(self, method):
        self.correction_method = method

    def select_min_max_constants(self, min, max):
        self.min = min
        self.max = max

    def select_ntk(self, ntk):
        self.ntk = ntk

    def proceed(self):
        su = self.qsbc / self.ntk
        return su