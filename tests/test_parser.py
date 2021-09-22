import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.parser import Parser, ParsedObject

class TestWithMetarValid:

    @pytest.mark.usefixtures("all_metars")
    def test_location(self, all_metars):
        """Tests valid locations found in metars."""
        expected = ["KIAH", 'KGNV', 'KNID', 'KTPA', 'KP60']
        for metar, expected_val in zip(all_metars, expected):
            actual = Parser(metar).location()
            assert expected_val == actual

    @pytest.mark.usefixtures("automated_metar", "normal_metar")
    def test_automated(self, automated_metar, normal_metar):
        """Tests if the metar is auto or not. Valid cases."""
        # Tests an actual metar to see if it's AUTO
        actual = Parser(automated_metar).is_auto()
        assert actual is True

        # not an AUTO metar.
        actual = parser.Parser(normal_metar).is_auto()
        assert actual is False

    @pytest.mark.usefixtures("variable_wind_metar", "normal_metar")
    def test_variable_wind(self, variable_wind_metar, normal_metar):
        """Tests a normal and variable wind metar for inclusion of variable wind."""

        actual = Parser(variable_wind_metar).wind()
        assert actual == ['VRB', 'VRB', 0, 0]

        actual = Parser(normal_metar).wind()
        assert actual == [N, 10, 15, 0]

    @pytest.mark.usefixtures("normal_metar")
    def test_date_format(self, normal_metar):
        """Tests to ensure time is formatted correctly"""

        actual = Parser(normal_metar).date()

        # test data structure regardless of what kind of metar is being tested
        assert isinstance(actual, list) # expected list
        assert len(actual) == 3 # number of items should be 3.

        # test the data types.
        # Date - dtype and length.
        assert isinstance(actual[0], str)
        assert len(actual[0]) == 2

        # Time - dtype and length
        assert isinstance(actual[1], str)
        assert len(actual[1]) == 4

        # Unit - dtype and length
        assert isinstance(actual[2], str)
        assert len(actual[2]) == 1

        # Now check to ensure that the normal metar is expected.
        assert actual == ['14', '1953', 'Z']

class TestParserObject:

    def test_has_attributes(self):
        """Determines if the Parser object has needed attributes. Don't care about values"""

        parsedObject = ParsedObject()

        assert hasattr(ParsedObject, location)
        assert hasattr(ParsedObject, date)
        assert hasattr(ParsedObject, is_auto)
        assert hasattr(ParsedObject, wind)
        assert hasattr(ParsedObject, visibility)
        assert hasattr(ParsedObject, wxconditions)
        assert hasattr(ParsedObject, cloudcoverage)
        assert hasattr(ParsedObject, temperature)
        assert hasattr(ParsedObject, dewpoint)
        assert hasattr(ParsedObject, altimeter)
        assert hasattr(ParsedObject, remarks)

    def test_attributes_set_to_none_to_start(self):

        parsedObject = ParsedObject()

        assert parsedObject.location is None
        assert parsedObject.date is None
        assert parsedObject.is_auto is None
        assert parsedObject.wind is None
        assert parsedObject.visibility is None
        assert parsedObject.wxconditions is None
        assert parsedObject.cloudcoverage is None
        assert parsedObject.temperature is None
        assert parsedObject.dewpoint is None
        assert parsedObject.altimeter is None
        assert parsedObject.remarks is None

class TestRegexLogic:

    def test_location_val_is_none(self):
        parser = Parser("AAAAAAA")
        parser.location()
        parsed_metar = parser.get_parsedObject()
        assert parsed_metar.location is None

    def test_location_val_is_valid(self):
        expected = "KHOU ABCD K543"
        parser = Parser(expected)
        parser.location()
        parsed_metar = parser.get_parsedObject()
        assert parsed_metar.location == 'KHOU'


# class Parser:
#
#     def test_valid_identifier(self):
#         """Tests the 4 letter identifier at the beginning of the METAR. Note that this
#         will only test for KXXX (USA)"""
#         expected = ["KIAH", "KGNV", "KNID", "KTPA", "KP60"]
#         for metar, expected in zip(self.metars, expected):
#             parser = Parser(metar)
#             actual = parser.location()
#             self.assertEqual(expected, actual)
#
#     def test_valid_time(self):
#         """Tests to make sure the time was properly identified"""
#         expected = [[14, 2059, "Z"], [14, 1953, "Z"], [14, 1722, "Z"],
#                 [11, 0353, "Z"], [21, 1356, "Z"]]
#
#         for metar, expected in zip(self.metars, expected):
#             parser = Parser(metar)
#             actual = parser.date()
#
#             self.assertTrue(isinstance(actual, list)) # check to make sure it's a list
#
#             for actual_val, expected_val in zip(actual, expected): # iterate through values
#
#                 # Check the data type and compare with expected.
#                 dtype_expected = type(expected_val)
#                 dtype_actual = type(actual_val)
#                 fail_msg = f"Data type of {actual_val} not {dtype_expected}." +
#                     "Found: {dtype_actual}. Expected: {dtype_expected}"
#                 self.assertEqual(dtype_expected, dtype_actual, fail_msg)
#
#                 self.assertTrue()
#                 self.assertEqual(actual_val, expected_val)
#
#     def test_valid_wind(self):
#         """Tests the wind information and puts it into the appropriate datastructure"""
#
#         # Structure: [Direction, Numerical Direction, Speed, Gust]
#         expected = [['N', 10, 15, 0], ['VAR', 0, 3, 0], [VAR, VAR, 3, 0],
#                     ['SSE', 3, 6, 0], ['CALM', 0, 0, 0]]
#
#         for metar, expected in zip(self.metars, expected):
#             parser = Parser(metar)
#             actual = parser.wind()
#             self.assertTrue(isinstance(actual, list)) # check to make sure it's a list
#             for actual_val, expected_val in zip(actual, expected): # iterate through values
#                 self.assertEqual(actual_val, expected_val)
#
#     def test_valid_visibility(self):
#         """Tests visibility to ensure its formatted properly"""
#
#         expected = [[10, 'SM'], [10, 'SM'], [2.5, 'SM'], [10, 'SM'], [None, None]]
#         for metar, expected in zip(self.metars, expected):
#             parser = Parser(metar)
#             actual = parser.visibility()
#             self.assertEqual(actual, expected)
#
#     def test_valid_wxconditions(self):
#
#         "KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206",
#         "KGNV 141953Z VRB03KT 10SM SCT040 32/24 A3001 RMK AO2 LTG DSNT NE-S SLPNO T03220239 $",
#         "KNID 141722Z VRB03KT 2 1/2SM HZ SCT000 27/M01 A2998 RMK AO2 SFC VIS 3 T02671011 $",
#         "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233",
#         "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056"
#
#         # Dictionary: {level : [observation, cloud cover string, height, TCU/CB/ACC]}
#         expected = [ {'l1' : ['OVC014', 'Overcast', 1400, None]},
#                     {'l1' : ['SCT040', 'Scattered', 4000, None]},
#                     {'l1' : ['SCT000', 'Scattered', 0, None]},
#                     {'l1' : ['FEW020', 'Few', 2000, None],
#                      'l2' : ['FEW038', 'Few', 3800, None],
#                      'l3' : ['SCT110', 'Scattered', 11000],
#                      'l4' : ['BKN160', 'Broken', 16000]},
#                     {'l1' : None}
#                    ]
#
#
#
#         ['Scattered', '014'], ['Scattered', '040'], ['Scattered', '000'],
#                     ['Few', '020', 'Few', '038', 'SCT', '110', 'BKN', '160']
#                    ]
#
#         parser = Parser(metar)
#         actual = parser.wxconditions()
#         self.assertTrue(isinstance(actual, list)) # check to make sure it's a list
#         for actual_val, expected_val in zip(actual, expected): # iterate through values
#             self.assertEqual(actual_val, expected_val)
#
#     def test_valid_cloudcoverage(self):
#         pass
#
#     def test_valid_temperature(self):
#         pass
#
#     def test_valid_dewpoint(self):
#         pass
#
#     def test_valid_altimeter(self):
#         pass
#
#     def test_valid_remarks(self):
#         pass

# if __name__ == "__main__":
#     import xmlrunner
#     unittest.main(testRunner=xmlrunner.XMLTestRunner(output='tests/test-reports'))
