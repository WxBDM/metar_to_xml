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
    metar = None

    def pack(self):
        d = {'location' : self.location, 'date' : self.date, 'is_auto' : self.is_auto,
            'wind' : self.wind, 'visibility' : self.visibility,
            'runway_visual_range' : self.runway_visual_range, 'wxconditions' : self.wxconditions,
            'cloudcoverage' : self.cloudcoverage, 'temperature' : self.temperature,
            'dewpoint' : self.dewpoint, 'altimeter' : self.altimeter, 'remarks' : self.remarks,
            'metar' : self.metar}
        return d

class Parser:

    """Parser for a given METAR.

    NOTE: this does not handle XML construction. Output examples should be structured
    exaclty as such so that parsing for XML construction is made easier."""

    def __init__(self, metar = None):

        if metar is None:
            msg = "Be sure to put in either a testing value or a metar."
            raise ValueError(msg)

        self._metar = metar

        # This is how we're going to get the values.
        self._parsedObject = ParsedObject()
        self._parsedObject.metar = metar

    def _compile_and_find(self, regex, other = None):

        pattern = re.compile(regex)
        if other is None:
            return pattern.findall(self._metar)
        else:
            # dtype checking
            if not isinstance(other, str):
                raise ValueError(f"`other` must be string. Found: {type(other)}")

            return pattern.findall(other)

    def get_parsedObject(self):
        return self._parsedObject

    def location(self):
        """Sets the location of the METAR.

        Parsed Object Data Type: string"""

        match = self._compile_and_find("^[KA-Z0-9]{4}")

        # Store in parsed object.
        self._parsedObject.location = match[0]

    def date(self):
        """Sets the date of the METAR.

        Parsed Object Data Type: List(string, string)"""
        # Input/output are same
        # 142059Z = [14, 2059, Z]
        match = self._compile_and_find("([0-9]{6}[Z])")[0]
        data = [match[:2], match[2:-1]]
        self._parsedObject.date = data

    def is_auto(self):
        """Returns a boolean if the station is AUTO"""
        match = self._compile_and_find("AUTO")

        if len(match) != 0: #e.g. ['AUTO']
            self._parsedObject.is_auto = "True"
        else:
            self._parsedObject.is_auto = "False"

    def wind(self):
        """Parses for wind."""
        # 01015KT -> ['010', '15', '0']
        # 01015G21KT -> ['010', '15', '21']
        # VRB02KT -> ['VRB', '02', '0']

        def as_str(data): # helper function to increase code reading.
            return str(int(data))

        regex = "([0-9]{5}KT)|([0-9]{5}G[0-9]{2}KT)|(VRB[0-9]{2}KT)"
        match = self._compile_and_find(regex)

        data = None
        for val in match[0]: # match is in [('15007KT', '', '')]
            if val != '':
                data = val # match exists
                break

        # if for some reason there isn't a wind value, return a dummy variable.
        if data is None:
            return 0

        if 'VRB' in data:
            self._parsedObject.wind = ['VRB', 'VRB', as_str(data[3:5]), "0"]

        else:
            wind_dir = get_wind_direction_from_degrees(int(data[:3]))
            data = data.split("G") # without gust: [abc], with gust: [abc, def]

            if len(data) == 1: # there is not a gust
                self._parsedObject.wind = [wind_dir, as_str(data[0][:3]), as_str(data[0][3:5]), '0']
            else: # there is a gust
                self._parsedObject.wind = [wind_dir, as_str(data[0][:3]), as_str(data[0][3:5]), data[1]]

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

        # Examples:
        #   R01L/0800FT => Runway 01L, 800 FT
        #   R01L/0600V1000FT => Runway 01L, 600 - 1000 FT
        #   R01L/M0600FT => Runway 01L, < 600 FT
        #   R27/P6000FT => Runway 01L, > 6000 FT
        # rvr = [runway #, Visual (str), I/D/N/None]
        #   Note: last element will likely be None.

        self._parsedObject.runway_visual_range = ["None", "None", "None"]
        regex = "R[0-9LRC]{2,}\/[0-9MVP]{4,}FT(\/[UDN])?"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            match = match.group() # Gives a string (R23/5000VP6000FT)

            match = match.split("/")
            # runway value
            self._parsedObject.runway_visual_range[0] = match[0][1:]

            # Parsing visual value(s)
            regex = "[MP]?[0-9]{4}"
            pattern = re.compile(regex)
            matches = pattern.findall(match[1])
            print(matches)

            # Something like 0800FT, M0600FT, or P6000FT
            if len(matches) == 1:
                match_temp = matches[0] # extract it, parse appropriately.
                if "M" in match_temp:
                    string_val = f"< {match_temp[1:-2]}"
                    self._parsedObject.runway_visual_range[1] = string_val
                elif "P" in match_temp:
                    string_val = f"> {match_temp[1:-2]}"
                    self._parsedObject.runway_visual_range[1] = string_val
                else:
                    self._parsedObject.runway_visual_range[1] = match_temp[1:-2]

            # Something like 5000VP6000FT
            if len(matches) == 2:
                string_val = f"{matches[0]} - {matches[1]}"
                self._parsedObject.runway_visual_range[1] = string_val

    def wxconditions(self):
        pass

    def cloudcoverage(self):
        self._parsedObject.cloudcoverage = [("None", "None"), ("None", "None"),
                                            ("None", "None"), ("None", "None")]
        regex = 'CLR|FEW[0-9]{3}|SCT[0-9]{3}|BKN[0-9]{3}|OVC[0-9]{3}'
        match = self._compile_and_find(regex)

        if len(match) == 0: # it is possible to have no obs
            return 0 # dummy return, don't do anything with it.

        cloud_d = {'CLR' : 'Clear', 'FEW' : 'Few', 'SCT' : 'Scattered',
                    'BKN' : 'Broken', 'OVC' : 'Overcast'}

        for index, element in enumerate(match):
            if 'CLR' in element:
                self._parsedObject.wxconditions[index] = 'Clear'
            else:
                height = str(int(element[3:]) * 100)
                clouds = cloud_d[element[:3]]

                self._parsedObject.cloudcoverage[index] = (clouds, height)

    def t_td(self):
        pattern = '\sM?[0-9]{2}\/M?[0-9]{2}\s'
        match = re.search(fr"{pattern}", self._metar).group()
        split = match.split("/")

        for index, val in enumerate(split):
            if 'M' in val:
                val = "-" + str(int(val[1:]))
            if index == 0:
                self._parsedObject.temperature = str(int(val))
            else:
                self._parsedObject.dewpoint = str(int(val))

    def altimeter(self):
        pattern = 'A[0-9]{4}'
        match = re.search(fr'{pattern}', self._metar).group()
        altimeter = match[1:3] + '.' + match[3:]
        self._parsedObject.altimeter = altimeter

    def remarks(self):
        pattern = 'RMK(.*)'
        match = re.search(fr'{pattern}', self._metar).group()
        self._parsedObject.remarks = match

    def parse(self):
        self.location()
        self.date()
        self.is_auto()
        self.wind()
        self.visibility()
        self.runway_visual_range()
        self.wxconditions()
        self.cloudcoverage()
        self.t_td()
        self.altimeter()
        self.remarks()


if __name__ == "__main__":
    # metars = ["KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206",
    # "KGNV 141953Z VRB03KT 10SM SCT040 32/24 A3001 RMK AO2 LTG DSNT NE-S SLPNO T03220239 $",
    # "KNID 141722Z VRB03KT 2 1/2SM HZ SCT000 27/M01 A2998 RMK AO2 SFC VIS 3 T02671011 $",
    # "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233",
    # "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056",
    # "KMBS 231423Z 33021G30KT 1 1/4SM R23/5000VP6000FT -RA BR SCT006 OVC010 10/09 A2970 RMK AO2 PK WND 33030/1417 P0005 T01000089"]

    metar = 'KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206'
    parser = Parser(metar)
    parser.parse()
    a = parser.get_parsedObject()
    print(a.location)
    print(a.date)
    print(a.is_auto)
    print(a.wind)
    print(a.visibility)
    print(a.runway_visual_range)
    print(a.wxconditions)
    print(a.cloudcoverage)
    print(a.temperature)
    print(a.dewpoint)
    print(a.altimeter)
    print(a.remarks)
