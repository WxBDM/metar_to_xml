import re
from dataclasses import dataclass
try:
    from utils import get_wind_direction_from_degrees, NullReturn
except ModuleNotFoundError:
    from metar_to_xml.utils import get_wind_direction_from_degrees, NullReturn

class Parser:

    """Parser for a given METAR.

    NOTE: this does not handle XML construction. Output examples should be structured
    exaclty as such so that parsing for XML construction is made easier."""

    def __init__(self, metar = None):

        if metar is None:
            msg = "Be sure to put in either a testing value or a metar."
            raise ValueError(msg)

        self._metar = metar
        # dictionary to store information of the metar. Given to formatter.
        self._d = {'location' : 'None',
            'date' : 'None',
            'is_auto' : 'None',
            'wind' : 'None',
            'visibility' : 'None',
            'rvr' : 'None',
            'conditions' : 'None',
            'coverage' : 'None',
            'temperature' : 'None',
            'dewpoint' : 'None',
            'altimeter' : 'None',
            'remarks' : 'None',
            'metar' : self._metar
            }

    def location(self):
        """Sets the location of the METAR.

        Parsed Object Data Type: string"""

        regex = "^[A-Z0-9]{4}"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['location'] = match.group()


    def date(self):
        """Sets the date of the METAR.

        Parsed Object Data Type: List(string, string)"""
        # Input/output are same
        # 142059Z = [14, 2059, Z]
        regex = "[0-9]{6}[Z]"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['date']= match.group()

    def is_auto(self):
        """Returns a boolean if the station is AUTO"""
        regex = "AUTO"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['is_auto'] = 'True'
        else:
            self._d['is_auto'] = 'False'

    def wind(self):
        """Parses for wind."""
        # ULMM 121530Z 23001MPS 9999 -SHRA BKN015CB 04/04 Q0998 R13/290060 NOSIG RMK QFE742
        # international metars use MPS (meters per second).
        # Parser will pick it up.

        def as_str(data): # helper function to increase code reading.
            return str(int(data))

        # regex expression, get matches.
        regex = "([0-9]{5}(KT|MPS))|([0-9]{5}G[0-9]{2}(KT|MPS))|(VRB[0-9]{2}(KT|MPS))"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['wind'] = match.group()

    def visibility(self):
        # Input 10SM
        # Output 10 SM
        # regex: [0-9]{2}SM

        # 2 1/2SM
        # Output: 2 1/2 SM
        # regex: [0-9]\s[0-9]\/[0-9]SM
        # very niche case: <[0-9]\/[0-9]SM (i.e <1.4 mi)

        regex = '[0-9]{2}SM|[0-9]\s[0-9]\/[0-9]SM|<[0-9]\/[0-9]SM|VV[0-9]{3}'
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['visibility'] = match.group()

    def runway_visual_range(self):
        """If a RVR exists in a METAR, return values from it."""

        # ULMM 121530Z 23001MPS 9999 -SHRA BKN015CB 04/04 Q0998 R13/290060 NOSIG RMK QFE742
        # Had to add in (FT)? as optional for RVR.

        regex = "R[0-9LRC]{2,}\/[0-9MVP]{4,}(FT)?(\/[UDN])?"
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['rvr'] = match.group() # Gives a string (R23/5000VP6000FT)

    def wxconditions(self):
        regex = '\s([+-])?(VC)?(?:MI|PR|BC|DR|BL|SH|TS|FZ)?(?:DZ|RA|SN|SG|IC|PL|GR|GS|UP|RADZ)?(\s)?(BR|FG|FU|VA|DU|SA|HZ|PY)?(PO|SQ|FC|SS)?\s'

        # Found anomylous metar CYHU 121500Z AUTO 20007KT 9SM 20/15 A3009 RMK CLD MISG SLP191 DENSITY ALT 600FT (10/12/21)
        # conditions stated "Shallow Snow Grains", this was picked up in remarks (MISG)
        # this is supposed to be "missing cloud". Added in logic below to split along remark and look at not that.

        metar = self._metar.split('RMK')[0] # guarenteed to have RMK, so split it.
        match = re.search(fr"{regex}", metar)
        if match is not None:
            self._d['conditions'] = match.group().strip()

    def cloudcoverage(self):
        regex = 'CLR|FEW[0-9]{3}|SCT[0-9]{3}|BKN[0-9]{3}|OVC[0-9]{3}'
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['coverage'] = match.group()

    def t_td(self):
        regex = '\sM?[0-9]{2}\/M?[0-9]{2}\s'
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['t_td'] = match.group()

    def altimeter(self):
        regex = 'A[0-9]{4}'
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['altimeter'] = match.group()

    def remarks(self):
        regex = 'RMK(.*)'
        match = re.search(fr"{regex}", self._metar)
        if match is not None:
            self._d['remarks'] = match.group()

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
        return self._d
