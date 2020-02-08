import random
import itertools

VIN_DIGIT_POSITION_MULTIPLIER = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
VIN_DIGIT_VALUES = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1,
                  'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5,
                  'W': 6, 'X': 7, 'Y': 8, 'Z': 9, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                  '7': 7, '8': 8, '9': 9, '0': 0}

VIN_YEAR = 'L'

class VinYear:
    def __init__(self, first8, year):
        self.First8 = first8
        self.Year = year

    def __repr__(self):
        return "First8: %s - Year: %s" % (self.First8, self.Year)


def get_next_vin(previous_vin):
    serial_number = int(previous_vin[11:]) + 1
    return get_next_vin_by_serial(serial_number)


def get_next_vin_by_serial(serial_number):
    results = []
    char = get_random_vin_char()
    vin_combos = get_possible_vins_starts()
    for combo in vin_combos:
        vin_year = VinYear(combo, VIN_YEAR)
        v = f'{vin_year.First8}{char}{vin_year.Year}G{serial_number:06}'
        check_char = get_check_sum_char(v)
        results.append("%s%s%s" % (v[0:8], check_char, v[9:]))
    return results


def get_check_sum_char(vin):
    # generate the check sum
    check_sum_total = 0

    if (len(vin) < 17):
        print("Invalid Length: %s" % len(vin))
        return -1

    for i in range(len(vin)):
        if (VIN_DIGIT_VALUES.get(vin[i], "-1") != "-1"):
            check_sum_total += int(VIN_DIGIT_VALUES[vin[i]]) * VIN_DIGIT_POSITION_MULTIPLIER[i];
        else:
            # Characters not in the VinDigitValues list are not valid VIN characters - return false (invalid)
            print("Illegal Character: %s" % vin[i])
            return -1;

    remain = check_sum_total % 11
    char = repr(remain)
    if remain == 10:
        char = 'X'

    return char


def get_random_vin_char():
    i = int(random.random() * len(VIN_DIGIT_VALUES))
    return list(VIN_DIGIT_VALUES.keys())[i]


def get_possible_vins_starts():
    models = [2,3,5,6]
    drives = ['D', '4']

    combos = [f'5XYP{model}{drive}HC' for (model,drive) in itertools.product(models, drives)]

    return combos


def is_valid_vin(vin):
    # print("Vin Lenth: %s" % len(vin))
    if (len(vin) != 17):
        return False

    c = get_check_sum_char(vin)
    # print("Expected Character %s - Actual: %s" % (c, vin[8]))

    # 9th character of the VIN is the Check Digit - if equal then valid
    return (c == vin[8]);
