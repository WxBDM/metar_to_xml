import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.parser import Parser, ParsedObject

class TestAttributesOfParsedObject:

    def test_has_location_attr(self):
        """Tests to make sure parsed object has a location attribute and is set to None"""
        assert hasattr(ParsedObject(), 'location')
        assert ParsedObject().location is None

    def test_has_date_attr(self):
        """Tests to make sure parsed object has a date attribute and is set to None"""
        assert hasattr(ParsedObject(), 'date')
        assert ParsedObject().date is None

    def test_has_is_auto_attr(self):
        """Tests to make sure parsed object has an is_auto attribute and is set to None"""
        assert hasattr(ParsedObject(), 'is_auto')
        assert ParsedObject().is_auto is None

    def test_has_wind_attr(self):
        """Tests to make sure parsed object has a wind attribute and is set to None"""
        assert hasattr(ParsedObject(), 'wind')
        assert ParsedObject().wind is None

    def test_has_visibility_attr(self):
        """Tests to make sure parsed object has a visibility attribute and is set to None"""
        assert hasattr(ParsedObject(), 'visibility')
        assert ParsedObject().visibility is None

    def test_has_runway_visual_range_attr(self):
        """Tests to make sure parsed object has an rvr attribute and is set to None"""
        assert hasattr(ParsedObject(), 'runway_visual_range')
        assert ParsedObject().runway_visual_range is None

    def test_has_wxconditions_attr(self):
        """Tests to make sure parsed object has a wxconditions attribute and is set to None"""
        assert hasattr(ParsedObject(), 'wxconditions')
        assert ParsedObject().wxconditions is None

    def test_has_cloudcoverage_attr(self):
        """Tests to make sure parsed object has a cloudcoverage attribute and is set to None"""
        assert hasattr(ParsedObject(), 'cloudcoverage')
        assert ParsedObject().cloudcoverage is None

    def test_has_temperature_attr(self):
        """Tests to make sure parsed object has a temperature attribute and is set to None"""
        assert hasattr(ParsedObject(), 'temperature')
        assert ParsedObject().temperature is None

    def test_has_dewpoint_attr(self):
        """Tests to make sure parsed object has a dewpoint attribute and is set to None"""
        assert hasattr(ParsedObject(), 'dewpoint')
        assert ParsedObject().dewpoint is None

    def test_has_altimeter_attr(self):
        """Tests to make sure parsed object has an altimeter attribute and is set to None"""
        assert hasattr(ParsedObject(), 'altimeter')
        assert ParsedObject().altimeter is None

    def test_has_remarks_attr(self):
        """Tests to make sure parsed object has a remarks attribute and is set to None"""
        assert hasattr(ParsedObject(), 'remarks')
        assert ParsedObject().remarks is None


class TestParsingLogic:

    @pytest.mark.usefixtures("all_metars")
    def test_location(self, all_metars):
        """Tests valid locations found in metars."""
        expected = ["KIAH", 'KGNV', 'KNID', 'KTPA', 'KP60']
        for metar, expected_val in zip(all_metars, expected):
            parser = Parser(metar)
            parser.location()
            actual = parser.get_parsedObject()
            assert expected_val == actual.location

    @pytest.mark.usefixtures("automated_metar", "normal_metar")
    def test_automated(self, automated_metar, normal_metar):
        """Tests if the metar is auto or not. Valid cases."""
        # Tests an actual metar to see if it's AUTO
        parser = Parser(automated_metar)
        parser.is_auto()
        actual = parser.get_parsedObject()
        assert actual.is_auto is True

        # not an AUTO metar.
        parser = Parser(normal_metar)
        parser.is_auto()
        actual = parser.get_parsedObject()
        assert actual.is_auto is False

    @pytest.mark.usefixtures("variable_wind_metar", "normal_metar")
    def test_variable_wind(self, variable_wind_metar, normal_metar):
        """Tests a normal and variable wind metar for inclusion of variable wind."""

        parser = Parser(variable_wind_metar)
        parser.wind()
        actual = parser.get_parsedObject()
        assert actual.wind == ['VRB', 'VRB', '3', '0']

        parser = Parser(normal_metar)
        parser.wind()
        actual = parser.get_parsedObject()
        assert actual.wind == ['N', '10', '15', '0']

    @pytest.mark.usefixtures("normal_metar")
    def test_date_format_dstructure_is_expected_len(self, normal_metar):
        """Tests to ensure time is formatted correctly"""

        parser = Parser(normal_metar)
        parser.date()
        actual = parser.get_parsedObject()
        actual = actual.date

        # test data structure regardless of what kind of metar is being tested
        assert isinstance(actual, list) # expected list
        assert len(actual) == 3 # number of items should be 3.

    @pytest.mark.usefixtures("normal_metar")
    def test_date_format_dstructure_is_expected_len(self, normal_metar):

        parser = Parser(normal_metar)
        parser.date()
        actual = parser.get_parsedObject()
        actual = actual.date

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

    @pytest.mark.usefixtures("normal_metar")
    def test_wind_format_is_expected_length(self, normal_metar):

            parser = Parser(normal_metar)
            parser.wind()
            actual = parser.get_parsedObject()
            actual = actual.wind

            # test data structure
            assert isinstance(actual, list) # expected list
            assert len(actual) == 4 # number of items should be 4.

    @pytest.mark.usefixtures("normal_metar")
    def test_wind_format_is_expected_dtypes(self, normal_metar):

            parser = Parser(normal_metar)
            parser.wind()
            actual = parser.get_parsedObject()
            actual = actual.wind

            # test the data types.
            # Direction - dtype and length.
            assert isinstance(actual[0], str)
            assert len(actual[0]) <= 3

            # Direction Degrees - dtype and length
            assert isinstance(actual[1], str)
            assert 2 <= len(actual[1]) <= 4

            # Windspeed - dtype and length
            assert isinstance(actual[2], str)
            assert 1 <= len(actual[2]) <= 2

            # Now check to ensure that the normal metar is expected.
            assert actual == ['N', '10', '15', '0']

    # Need tests for visibility, wxconditions, cloudcoverage, temperature, dewpoint, altimeter, remarks
    @pytest.mark.usefixtures("normal_metar")
    def test_visibility_normal_10sm_normal(self, normal_metar):

        parser = Parser(normal_metar)
        parser.visibility()
        actual = parser.get_parsedObject()
        actual = actual.visibility

        assert actual == '10'

    @pytest.mark.usefixtures("visibility_metar")
    def test_visibility_fractional_metar(self, visibility_metar):

        parser = Parser(visibility_metar)
        parser.visibility()
        actual = parser.get_parsedObject()
        actual = actual.visibility

        assert actual == "2 1/2"

    @pytest.mark.usefixtures('normal_metar')
    def test_wx_conditions_none(self, normal_metar):

        parser = Parser(normal_metar)
        parser.wxconditions()
        actual = parser.get_parsedObject()
        actual = actual.wxconditions

        assert actual is None

    @pytest.mark.usefixtures('visibility_metar')
    def test_wx_conditions_haze(self, visibility_metar):

        parser = Parser(visibility_metar)
        parser.wxconditions()
        actual = parser.get_parsedObject()
        actual = actual.wxconditions

        assert isinstance(actual[0], str)
        assert actual == ['HZ']

    @pytest.mark.usefixtures('multiple_wx_conditions_metar')
    def test_wx_conditions_multiple(self, multiple_wx_conditions_metar):

        parser = Parser(multiple_wx_conditions_metar)
        parser.wxconditions()
        actual = parser.get_parsedObject()
        actual = actual.wxconditions

        for val in actual:
            assert isinstance(val, str)

        assert actual == ['-RA', 'BR']

    @pytest.mark.usefixtures('wx_conditions_vicinity')
    def test_wxconditions_vicinity(self, wx_conditions_vicinity):

        parser = Parser(wx_conditions_vicinity)
        parser.wxconditions()
        actual = parser.get_parsedObject()
        actual = actual.wxconditions

        assert isinstance(actual[0], str)
        assert actual == ['VCTS']

class TestNicheParsingCases:

    @pytest.mark.usefixtures("runway_visual_range_metar")
    def test_valid_rvr_metar(self, runway_visual_range_metar):

        parser = Parser(runway_visual_range_metar)
        parser.runway_visual_range()
        actual = parser.get_parsedObject()
        actual = actual.runway_visual_range

        # ['Runway #', 'distance 1', 'distance 2']

        # test dstructure and length
        assert isinstance(actual, list)
        assert len(actual) == 3

        # test data types
        for val in actual:
            assert isinstance(val, (type(None), str))

    @pytest.mark.usefixtures("normal_metar")
    def test_invalid_rvr_metar(self, normal_metar):

        parser = Parser(normal_metar)
        parser.runway_visual_range()
        actual = parser.get_parsedObject()
        actual = actual.runway_visual_range

        assert actual == [None, None, None]
