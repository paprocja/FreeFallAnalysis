#!/usr/bin/python3
def verify_deceleration(deceleration):
    valid = is_same(deceleration[0],  0.273029271) \
            and is_same(deceleration[1], 0.344186163) \
            and is_same(deceleration[2], 0.478478511) \
            and is_same(deceleration[len(deceleration) -1], -0.0134663027) \
            and is_same(deceleration[len(deceleration) - 2], 0.116289459) \
            and is_same(deceleration[len(deceleration) - 3],  0.218982684)
     
    if not valid:
        print('Incorrect deceleration')
    

def verify_velocity(velocity):
    valid = is_same(velocity[0],  5.34641748) \
            and is_same(velocity[1], 5.34490376) \
            and is_same(velocity[2], 5.34288618) \
            and is_same(velocity[len(velocity) -1], 0.00000000) \
            and is_same(velocity[len(velocity) - 2], 0.000252173792) \
            and is_same(velocity[len(velocity) - 3],  0.00107442872)
     
    if not valid:
        print('Incorrect velocity')

def verify_depth(depth):
    valid = is_same(depth[0],  0) \
            and is_same(depth[1], 0.00267283) \
            and is_same(depth[2], 0.00534478) \
            and is_same(depth[len(depth) -1], 0.11289662) \
            and is_same(depth[len(depth) - 2], 0.11289656) \
            and is_same(depth[len(depth) - 3], 0.11289622)
     
    if not valid:
        print('Incorrect depth')

def verify_area(area):
    valid = is_same(area[0],  0) \
            and is_same(area[1],  0.00000748120221) \
            and is_same(area[2], 0.0000299149256) \
            and is_same(area[len(area) -1], 0.00601320469) \
            and is_same(area[len(area) - 2], 0.00601320469) \
            and is_same(area[len(area) - 3], 0.00601320469)
     
    if not valid:
        print('Incorrect area')

def verify_qsbc_in_air(qsbc):
    valid = is_same(qsbc[0],  749.88259127) \
            and is_same(qsbc[1],  260.71666243) \
            and is_same(qsbc[2], 150.26916241) \
            and is_same(qsbc[len(qsbc) -1], -0.7910829) \
            and is_same(qsbc[len(qsbc) - 2], -3.04428189) \
            and is_same(qsbc[len(qsbc) - 3], -12.52020871)
     
    if not valid:
        print('Incorrect qsbc air')

def verify_qsbc_in_water(qsbc):
    valid = is_same(qsbc[0],  504.54551719) \
            and is_same(qsbc[1],  175.41869196) \
            and is_same(qsbc[2], 101.10600399) \
            and is_same(qsbc[len(qsbc) -1], -0.53226643) \
            and is_same(qsbc[len(qsbc) - 2], -2.04829236) \
            and is_same(qsbc[len(qsbc) - 3], -8.42400564)
     
    if not valid:
        print('Incorrect qsbc water')

def verify_tilt(tilt_x, tilt_y):
    valid = is_same(tilt_x, 118.09521795311922) and is_same(tilt_y, 38.23828843890631)

    if not valid:
        print('Incorrect tilt')

def verify_deceleration_profile(deceleration_profile):
    valid = is_same(deceleration_profile[0],  -4.65240745) \
            and is_same(deceleration_profile[1],  -4.52336153) \
            and is_same(deceleration_profile[2], -4.44451725) \
            and is_same(deceleration_profile[len(deceleration_profile) -1], 0.46939123) \
            and is_same(deceleration_profile[len(deceleration_profile) - 2], 0.93444932) \
            and is_same(deceleration_profile[len(deceleration_profile) - 3], 0.75212191)
     
    if not valid:
        print('Incorrect deceleration profile')

def verify_pore_pressure(bernoulli_pressure):
    valid = is_same(bernoulli_pressure[0],  9.78795155) \
            and is_same(bernoulli_pressure[1],  9.79107515) \
            and is_same(bernoulli_pressure[2], 9.78559273) \
            and is_same(bernoulli_pressure[len(bernoulli_pressure) -1], 124.34832006) \
            and is_same(bernoulli_pressure[len(bernoulli_pressure) - 2], 124.40439272) \
            and is_same(bernoulli_pressure[len(bernoulli_pressure) - 3], 124.3842021)
     
    if not valid:
        print('Incorrect deceleration profile')

def is_same(x, y):
    return abs(x - y) < 0.00001