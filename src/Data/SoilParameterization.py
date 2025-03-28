import numpy as np
from scipy import integrate
from Data.Peak import Peak

class SoilParameterization:
    def __init__(self, peak: Peak):
        self.peak = peak
        self.framework = 'clay' if max(peak.depth) > 0.2 else 'sand'        
