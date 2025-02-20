import numpy as np
from scipy import integrate
from Data.Peak import Peak
from Data.PenetrometerData import PenetrometerData

class PorePressure:
    def __init__(self, peak: Peak, penetrometer_data: PenetrometerData, start, end):
        self.peak = peak
        self.penetrometer_data = penetrometer_data
        self.pressure_start = start
        self.pressure_end = end
        self.deceleration_start = 0
        self.deceleration_end = 0
        self.point_of_impact = 0
        self.point_of_impact_plus = 0
        self.min_deceleration = 0
        self.max_measured_pressure = 0
        self.measured_pressure = None
        self.raw_deceleration = None
        self.deceleration_profile = None
        self.specific_deceleration = None
        self.velocity = None
        self.depth = None
        self.hydrostatic_pressure = None
        self.bernoulli_pressure = None

    def calculate_deceleration_profile(self):
        # The integration delta
        STEP = 1/2000

        # Get pressure from the penetrometer and truncate by start and end
        ppm = self.penetrometer_data.ppm
        self.measured_pressure = ppm[self.pressure_start:self.pressure_end + 1]
        
        # Get the offset deceleration
        deceleration = (self.peak.g50g_whole[self.pressure_start:self.pressure_end + 1] - self.peak.offset)
        self.raw_deceleration = deceleration
        deceleration = deceleration * 9.81

        velocity = integrate.cumulative_trapezoid(deceleration, dx=STEP, initial=0)

        max_velocity = np.max(velocity)

        # Correc the velocity based on the max
        corrected_velocity = max_velocity - velocity

        # Get the depth and correct based on average
        depth = (integrate.cumulative_trapezoid(corrected_velocity, dx=STEP, initial=0)) * -1
        correction_factor = np.mean(ppm[self.pressure_start - 200 :self.pressure_start + 1]) / 9.807
        depth = depth - correction_factor

        # Assign members for plotting
        self.deceleration_profile = deceleration
        self.velocity = corrected_velocity
        self.depth = depth

    def calculate_pore_pressure(self, start, end):
        TIP_PRESSURE_DISTANCE = 0.08833 # Hard coded now but varies with the tip
        PRESSURE_COEFFICIENT = 0.5 # From a paper can vary

        # Assign member variables
        self.deceleration_start = start
        self.deceleration_end = end

        # Get and correct the raw deceleration from g50g meter
        deceleration = self.raw_deceleration[self.deceleration_start:self.deceleration_end+1] - self.raw_deceleration[self.deceleration_start]
        deceleration = deceleration * 9.81
        self.min_deceleration = min(deceleration) - 20

        # Get the point of impact and impact with depth constant
        self.point_of_impact = self.depth[self.deceleration_start]
        self.point_of_impact_plus = self.point_of_impact + TIP_PRESSURE_DISTANCE

        # Assign variables for plotting
        self.hydrostatic_pressure = self.depth * -9.807
        self.max_measured_pressure = max(self.hydrostatic_pressure) + 50

        self.bernoulli_pressure = self.measured_pressure + PRESSURE_COEFFICIENT * (np.square(self.velocity) / 2)

        '''
        print(f'bernoulli: {self.bernoulli_pressure}')
        print(f'min decel: {self.min_deceleration}')
        print(f'point of impact: {self.point_of_impact}')
        print(f'point of impact plus: {self.point_of_impact_plus}')
        print(f'hydrostatic pressure: {self.hydrostatic_pressure}')
        print(f'max pressure: {self.max_measured_pressure}')
        '''

