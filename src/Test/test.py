#!/usr/bin/python3
import sys
import os
import pickle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from verify import *
from Data.SoilParameterization import SoilParameterization
from Data.PenetrometerData import PenetrometerData
from Data.TiltCalculator import calculate_tilt
from Data.Peak import Peak
from Data.PorePressure import PorePressure

penetrometer_data = PenetrometerData(['TestData/bLogtest.bin'], 8)

peak = Peak(peak_num=0, penetrometer_data=penetrometer_data)

peak.integrate_spike(1463)

verify_decelleration(peak.decelleration)
verify_velocity(peak.velocity)
verify_depth(peak.depth)
verify_area(peak.area)

soil_parameterization = SoilParameterization(peak)

correction_type = 1
correction_factor = 1.5
tip_type = 'c'

qsbc = peak.calculate_QSBC_for_K(correction_type, correction_factor, tip_type, False)
verify_qsbc_in_air(qsbc)

initial_qsbc = peak.calculate_QSBC_for_K(correction_type, correction_factor, tip_type, True)
verify_qsbc_in_water(qsbc)

line1val1, line1val2, line1ave, line2val1, line2val2, line2ave = peak.calculate_corrected_qsbc(correction_type, 10, 80, False)
# Verify


tilt_x, tilt_y = calculate_tilt(1, peak.end_of_drop, peak.gX55g, peak.gY55g)
# Verify

pore_pressure = PorePressure(peak, penetrometer_data, 20486, 25077)
# Verify

pore_pressure.calculate_deceleration_profile()
# Verify

pore_pressure.calculate_pore_pressure(4381, 4468)
# Verify

print("Exiting program.")
