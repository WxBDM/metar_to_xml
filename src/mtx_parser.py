# parser for the metar.

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

    def __init__(self, metar):
        self._metar = metar


    def location(self):
        # examples:
        #   input: KHOU
        #   Output: KHOU
        pass

    def date(self):
        # examples
        #   input: 141953Z
        #   output: 14th, 19:53 UTC
        # Should be string.

        pass

    def wind(self):
        # input: 01015KT
        # output: North 10 15 Knots 0 Gust

        # input: VRB03KT
        # output: Variable Variable 3 Knots 0 Gust

        # input: 08023G33KT
        # output: East 80 23 Knots 33 Gust
        pass

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
