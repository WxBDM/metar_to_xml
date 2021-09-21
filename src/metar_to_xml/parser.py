# parser for the metar.

import re

# N 348.75 - 11.25
# NNE 11.25 - 33.75
# NE 33.75 - 56.25
# ENE 56.25 - 78.75
# E 78.75 - 101.25
# ESE 101.25 - 123.75
# SE 123.75 - 146.25
# SSE 146.25 - 168.75
# S 168.75 - 191.25
# SSW 191.25 - 213.75
# SW 213.75 - 236.25
# WSW 236.25 - 258.75
# W 258.75 - 281.25
# WNW 281.25 - 303.75
# NW 303.75 - 326.25
# NNW 326.25 - 348.75

class Parser:

    """Parser for a given METAR.

    NOTE: this does not handle XML construction. Output examples should be structured
    exaclty as such so that parsing for XML construction is made easier."""

    def __init__(self, metar, is_testing = False, testing_value = None):
        if not is_testing:
            self._metar = metar
        else:
            if testing_value is None:
                msg = "testing_value cannot be None. Initialize the class with" \
                    " is_testing = True, testing_value to be a value to test."
                raise ValueError(msg)

            self._metar = testing_value

    def location(self):
        """Returns the location of the METAR"""
        pattern = re.compile("^[KA-Z]{4}")
        match = pattern.match(self._metar)
        return match[0]

    def date(self):
        """Returns a string representation of the date"""
        # Input/output are same
        # 142059Z = [14, 2059, Z]
        pattern = re.compile("(\d{6}[Z])")
        match = pattern.findall(self._metar)[0]




    def wind(self):
        # input: 01015KT
        # output: [N, 10, 15, 0]

        # input: VRB03KT
        # output: [VRB, VRB, 3, 0]

        # input: 08023G33KT
        # output: [E, 80, 23, 33]

        patterns = ["(\d{5}KT)", "(\d{5}G\d{2}KT)", "(VRB\d{2}KT)"]
        time = None
        for pattern in patterns:
            pattern = re.compile(pattern)
            match = pattern.findall(self._metar)
            if match is not None:
                time = match[0]
                break

        # format the time


    def visibility(self):
        # Input 10SM
        # Output 10 SM

        # 2 1/2SM
        # Output: 2.5 SM
        pass

    def wxconditions(self):
        pass

    def cloudcoverage(self):
        pass

    def temperature(self):
        pass

    def dewpoint(self):
        pass

    def altimeter(self):
        pass

    def remarks(self):
        pass



if __name__ == "__main__":
    metars = ["KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206",
    "KGNV 141953Z VRB03KT 10SM SCT040 32/24 A3001 RMK AO2 LTG DSNT NE-S SLPNO T03220239 $",
    "KNID 141722Z VRB03KT 2 1/2SM HZ SCT000 27/M01 A2998 RMK AO2 SFC VIS 3 T02671011 $",
    "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233"
    ]

    for metar in metars:
        parser = Parser(metar)
        parser.wind()
