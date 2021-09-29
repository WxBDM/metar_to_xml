import re
from dataclasses import dataclass
try:
    from utils import get_wind_direction_from_degrees
except ModuleNotFoundError:
    from metar_to_xml.utils import get_wind_direction_from_degrees

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
    runway_visual_range = None

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

    def _compile_and_find(self, regex):
        pattern = re.compile(regex)
        return pattern.findall(self._metar)

    def get_parsedObject(self):
        return self._parsedObject

    def location(self):
        """Returns the location of the METAR"""

        match = self._compile_and_find("^[KA-Z0-9]{4}")

        # Store in parsed object.
        self._parsedObject.location = match[0]

    def date(self):
        """Returns a string representation of the date"""
        # Input/output are same
        # 142059Z = [14, 2059, Z]
        match = self._compile_and_find("([0-9]{6}[Z])")[0]
        data = [match[:2], match[2:-1], 'Z']
        self._parsedObject.date = data

    def is_auto(self):
        """Returns a boolean if the station is AUTO"""
        match = self._compile_and_find("AUTO")
        print(match)

        if len(match) != 0: #e.g. ['AUTO']
            self._parsedObject.is_auto = True
        else:
            self._parsedObject.is_auto = False

    def wind(self):

        def as_str(data): # helper function to increase code reading.
            return str(int(data))

        regex_vals = ["([0-9]{5}KT)", "([0-9]{5}G[0-9]{2}KT)", "(VRB[0-9]{2}KT)"]
        for n, regex in enumerate(regex_vals):
            match = self._compile_and_find(regex)
            if len(match) == 0: # if it's not a sucessful match, go to the next regex.
                continue

            if n == 0: # normal metar (01015KT => [N, 10, 15, 0] )
                data = match[0]
                wind_dir = get_wind_direction_from_degrees(int(data[:3]))
                self._parsedObject.wind = [wind_dir, as_str(data[:3]), as_str(data[3:5]), '0']
                break

            if n == 1: # metar with gust (08023G33KT => [E, 80, 23, 33] )
                data = match[0]
                wind_dir = get_wind_direction_from_degrees(int(data[:3]))
                gust = data.split("G")[1] # splits along the gust variable.
                # spaghetti, but changing data type and slicing a string.
                self._parsedObject.wind = [wind_dir, as_str(data[:3]), as_str(data[3:5]), gust[:2]]
                break

            if n == 2: # VRB metar (VRB03KT => [VRB, VRB, 3, 0] )
                self._parsedObject.wind = ['VRB', 'VRB', as_str(match[0][3:5]), "0"]
                break

    def visibility(self):
        # Input 10SM
        # Output 10 SM
        # regex: [0-9]{2}SM

        # 2 1/2SM
        # Output: 2 1/2 SM
        # regex: [0-9]\s[0-9]\/[0-9]SM
        # very niche case: <[0-9]\/[0-9]SM (i.e <1.4 mi)

        regex_vals = ['[0-9]{2}SM', '[0-9]\s[0-9]\/[0-9]SM', '<[0-9]\/[0-9]SM']
        self._parsedObject.visibility = None # assume that there isn't a visibility

        # iterate through regex, if a value is found, set it. If not, set to None.
        for n, regex in enumerate(regex_vals):
            match = self._compile_and_find(regex)

            if len(match) != 0: # a successful match has been found, so set and break.
                self._parsedObject.visibility = match[0][:-2]
                break

    def runway_visual_range(self):
        """If a RVR exists in a METAR, return values from it."""

        regex = "R[0-9LRC]{2,}\/[0-9MVP]{4,}FT(\/[UDN])?"
        match = self._compile_and_find(value)

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
    "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056",
    "KMBS 231423Z 33021G30KT 1 1/4SM R23/5000VP6000FT -RA BR SCT006 OVC010 10/09 A2970 RMK AO2 PK WND 33030/1417 P0005 T01000089"]

    for metar in metars:
        parser = Parser(metar)
        parser.wind()
        a = parser.get_parsedObject()
        print(a.wind)
