import re
from dataclasses import dataclass

@dataclass
class ParsedObject:
    """An object that the XML constructor is going to pull information from"""

    location = None
    date = None
    is_auto = None
    wind = None
    visibility = None
    wxconditions = None
    cloudcoverage = None
    temperature = None
    dewpoint = None
    altimeter = None
    remarks = None

class Parser:

    """Parser for a given METAR.

    NOTE: this does not handle XML construction. Output examples should be structured
    exaclty as such so that parsing for XML construction is made easier."""

    def __init__(self, metar = None, test_val = None):

        if all([metar is None, test_val is None]):
            msg = "Be sure to put in either a testing value or a metar."
            raise ValueError(msg)

        if test_val is None:
            self._metar = metar
        else:
            self._metar = testing_value

        # This is how we're going to get the values.
        self._parsedObject = ParsedObject()

    def get_parsedObject(self):
        return self._parsedObject

    def location(self):
        """Returns the location of the METAR"""

        pattern = re.compile("^[KA-Z0-9]{4}")
        match = pattern.findall(self._metar)

        # Store in parsed object.
        self._parsedObject.location = match[0]

    def date(self):
        """Returns a string representation of the date"""
        # Input/output are same
        # 142059Z = [14, 2059, Z]
        pattern = re.compile("(\d{6}[Z])")
        match = pattern.findall(self._metar)[0]
        return match

    def is_auto(self):
        """Returns a boolean if the station is AUTO"""
        pattern = re.compile("AUTO")
        match = pattern.findall(self._metar)[0]
        print(match)
        return match

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
    "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233",
    "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056"]

    for metar in metars:
        parser = Parser(metar)
        parser.location()
        print(parser.parsedObject.location)
