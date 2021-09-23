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
        parser = parser.Parser(normal_metar)
        parser.is_auto()
        actual = parser.get_parsedObject()
        assert actual.is_auto is False

    @pytest.mark.usefixtures("variable_wind_metar")
    def test_variable_wind(self, variable_wind_metar):
        """Tests a normal and variable wind metar for inclusion of variable wind."""

        parser = Parser(variable_wind_metar)
        parser.wind()
        actual = parser.get_parsedObject()
        assert actual.wind == ['VRB', 'VRB', 0, 0]

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
            assert len(actual) == 4 # number of items should be 3.

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

        assert actual == "2.5"

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


# ==== TESTS FOR NICHE CASES ====

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
            assert isinstance(val, str)

    @pyteest.mark.usefixtures("normal_metar")
    def test_invalid_rvr_metar(self, normal_metar):

        parser = Parser(normal_metar)
        parser.runway_visual_range()
        actual = parser.get_parsedObject()
        actual = actual.runway_visual_range

        assert actual is None


class TestParserObject:

    def test_has_attributes(self):
        """Determines if the Parser object has needed attributes. Don't care about values"""

        p = ParsedObject()

        attributes = ['location', 'date', 'is_auto', 'wind', 'visibility',
            'wxconditions', 'cloudcoverage', 'temperature', 'dewpoint',
            'altimeter', 'remarks', 'runway_visual_range']

        for attribute in attributes:
            assert hasattr(p, attribute)

    def test_attributes_set_to_none_to_start(self):

        p = ParsedObject()

        attributes = [p.location, p.date, p.is_auto, p.wind, p.visibility,
            p.wxconditions, p.cloudcoverage, p.temperature, p.dewpoint,
            p.altimeter, p.remarks, p.runway_visual_range]

        for attribute in attributes:
            assert attribute is None

    @pytest.mark.usefixtures("normal_metar")
    def test_attribute_is_not_none_after_successful_parse(self, normal_metar):
        """Tests to make sure attributes are set once the function runs. type/value doesn't matter."""

        p = Parser(normal_metar)

        attributes = [(p.get_parsedObject().location, p.location()),
                      (p.get_parsedObject().date, p.date()),
                      (p.get_parsedObject().is_auto, p.is_auto()),
                      (p.get_parsedObject().wind, p.wind()),
                      (p.get_parsedObject().visibility, p.wind()),
                      (p.get_parsedObject().wxconditions, p.wxconditions()),
                      (p.get_parsedObject().cloudcoverage, p.wxconditions()),
                      (p.get_parsedObject().temperature, p.temperature()),
                      (p.get_parsedObject().dewpoint, p.dewpoint()),
                      (p.get_parsedObject().altimeter, p.altimeter()),
                      (p.get_parsedObject().remarks, p.remarks()),
                      (p.get_parsedObject().runway_visual_range, p.runway_visual_range())
                     ]

        for value, function in attributes:
            function()
            assert value is not None

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
