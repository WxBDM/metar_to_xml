import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.parser import Parser, ParsedObject


# Individually testing each one, they're used as dependencies for other tests.
@pytest.mark.dependency(name="location_attr")
def test_has_location_attr():
    """Tests to make sure parsed object has a location attribute and is set to None"""
    assert hasattr(ParsedObject(), 'location')
    assert ParsedObject().location is None

@pytest.mark.dependency(name="date_attr")
def test_has_date_attr():
    """Tests to make sure parsed object has a date attribute and is set to None"""
    assert hasattr(ParsedObject(), 'date')
    assert ParsedObject().date is None

@pytest.mark.dependency(name="auto_attr")
def test_has_is_auto_attr():
    """Tests to make sure parsed object has an is_auto attribute and is set to None"""
    assert hasattr(ParsedObject(), 'is_auto')
    assert ParsedObject().is_auto is None

@pytest.mark.dependency(name="wind_attr")
def test_has_wind_attr():
    """Tests to make sure parsed object has a wind attribute and is set to None"""
    assert hasattr(ParsedObject(), 'wind')
    assert ParsedObject().wind is None

@pytest.mark.dependency(name="visibility_attr")
def test_has_visibility_attr():
    """Tests to make sure parsed object has a visibility attribute and is set to None"""
    assert hasattr(ParsedObject(), 'visibility')
    assert ParsedObject().visibility is None

@pytest.mark.dependency(name="rvr_attr")
def test_has_runway_visual_range_attr():
    """Tests to make sure parsed object has an rvr attribute and is set to None"""
    assert hasattr(ParsedObject(), 'runway_visual_range')
    assert ParsedObject().runway_visual_range is None

@pytest.mark.dependency(name="wxconditions_attr")
def test_has_wxconditions_attr():
    """Tests to make sure parsed object has a wxconditions attribute and is set to None"""
    assert hasattr(ParsedObject(), 'wxconditions')
    assert ParsedObject().wxconditions is None

@pytest.mark.dependency(name="cloud_attr")
def test_has_cloudcoverage_attr():
    """Tests to make sure parsed object has a cloudcoverage attribute and is set to None"""
    assert hasattr(ParsedObject(), 'cloudcoverage')
    assert ParsedObject().cloudcoverage is None

@pytest.mark.dependency(name="temp_attr")
def test_has_temperature_attr():
    """Tests to make sure parsed object has a temperature attribute and is set to None"""
    assert hasattr(ParsedObject(), 'temperature')
    assert ParsedObject().temperature is None

@pytest.mark.dependency(name="dewpoint_attr")
def test_has_dewpoint_attr():
    """Tests to make sure parsed object has a dewpoint attribute and is set to None"""
    assert hasattr(ParsedObject(), 'dewpoint')
    assert ParsedObject().dewpoint is None

@pytest.mark.dependency(name="altimeter_attr")
def test_has_altimeter_attr():
    """Tests to make sure parsed object has an altimeter attribute and is set to None"""
    assert hasattr(ParsedObject(), 'altimeter')
    assert ParsedObject().altimeter is None

@pytest.mark.dependency(name="remarks_attr")
def test_has_remarks_attr():
    """Tests to make sure parsed object has a remarks attribute and is set to None"""
    assert hasattr(ParsedObject(), 'remarks')
    assert ParsedObject().remarks is None


# @pytest.mark.usefixtures("normal_metar")
# def test_attribute_is_not_none_after_successful_parse(normal_metar):
#     """Tests to make sure attributes are set once the function runs. type/value doesn't matter."""
#
#     p = Parser(normal_metar)
#
#     attributes = [(p.get_parsedObject().location, p.location()),
#                   (p.get_parsedObject().date, p.date()),
#                   (p.get_parsedObject().is_auto, p.is_auto()),
#                   (p.get_parsedObject().wind, p.wind()),
#                   (p.get_parsedObject().visibility, p.wind()),
#                   (p.get_parsedObject().wxconditions, p.wxconditions()),
#                   (p.get_parsedObject().cloudcoverage, p.wxconditions()),
#                   (p.get_parsedObject().temperature, p.temperature()),
#                   (p.get_parsedObject().dewpoint, p.dewpoint()),
#                   (p.get_parsedObject().altimeter, p.altimeter()),
#                   (p.get_parsedObject().remarks, p.remarks()),
#                   (p.get_parsedObject().runway_visual_range, p.runway_visual_range())
#                  ]
#
#     for value, function in attributes:
#         function()
#         assert value is not None

@pytest.mark.usefixtures("all_metars")
@pytest.mark.dependency(depends=["location_attr"])
def test_location(all_metars):
    """Tests valid locations found in metars."""
    expected = ["KIAH", 'KGNV', 'KNID', 'KTPA', 'KP60']
    for metar, expected_val in zip(all_metars, expected):
        parser = Parser(metar)
        parser.location()
        actual = parser.get_parsedObject()
        assert expected_val == actual.location

@pytest.mark.usefixtures("automated_metar", "normal_metar")
@pytest.mark.dependency(depends=["auto_attr"])
def test_automated(automated_metar, normal_metar):
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

@pytest.mark.usefixtures("variable_wind_metar")
@pytest.mark.dependency(depends=["wind_attr"])
def test_variable_wind(variable_wind_metar):
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
@pytest.mark.dependency(depends=["date_attr"])
def test_date_format_dstructure_is_expected_len(normal_metar):
    """Tests to ensure time is formatted correctly"""

    parser = Parser(normal_metar)
    parser.date()
    actual = parser.get_parsedObject()
    actual = actual.date

    # test data structure regardless of what kind of metar is being tested
    assert isinstance(actual, list) # expected list
    assert len(actual) == 3 # number of items should be 3.

@pytest.mark.usefixtures("normal_metar")
@pytest.mark.dependency(depends=["date_attr"])
def test_date_format_dstructure_is_expected_len(normal_metar):

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
@pytest.mark.dependency(depends=["wind_attr"])
def test_wind_format_is_expected_length(normal_metar):

        parser = Parser(normal_metar)
        parser.wind()
        actual = parser.get_parsedObject()
        actual = actual.wind

        # test data structure
        assert isinstance(actual, list) # expected list
        assert len(actual) == 4 # number of items should be 3.

@pytest.mark.usefixtures("normal_metar")
@pytest.mark.dependency(depends=["wind_attr"])
def test_wind_format_is_expected_dtypes(normal_metar):

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
@pytest.mark.dependency(depends=["visibility_attr"])
def test_visibility_normal_10sm_normal(normal_metar):

    parser = Parser(normal_metar)
    parser.visibility()
    actual = parser.get_parsedObject()
    actual = actual.visibility

    assert actual == '10'

@pytest.mark.usefixtures("visibility_metar")
@pytest.mark.dependency(depends=["visibility_attr"])
def test_visibility_fractional_metar(visibility_metar):

    parser = Parser(visibility_metar)
    parser.visibility()
    actual = parser.get_parsedObject()
    actual = actual.visibility

    assert actual == "2.5"

@pytest.mark.usefixtures('normal_metar')
@pytest.mark.dependency(depends=["wxconditions_attr"])
def test_wx_conditions_none(normal_metar):

    parser = Parser(normal_metar)
    parser.wxconditions()
    actual = parser.get_parsedObject()
    actual = actual.wxconditions

    assert actual is None

@pytest.mark.usefixtures('visibility_metar')
@pytest.mark.dependency(depends=["wxconditions_attr"])
def test_wx_conditions_haze(visibility_metar):

    parser = Parser(visibility_metar)
    parser.wxconditions()
    actual = parser.get_parsedObject()
    actual = actual.wxconditions

    assert isinstance(actual[0], str)
    assert actual == ['HZ']

@pytest.mark.usefixtures('multiple_wx_conditions_metar')
@pytest.mark.dependency(depends=["wxconditions_attr"])
def test_wx_conditions_multiple(multiple_wx_conditions_metar):

    parser = Parser(multiple_wx_conditions_metar)
    parser.wxconditions()
    actual = parser.get_parsedObject()
    actual = actual.wxconditions

    for val in actual:
        assert isinstance(val, str)

    assert actual == ['-RA', 'BR']

@pytest.mark.usefixtures('wx_conditions_vicinity')
@pytest.mark.dependency(depends=["wxconditions_attr"])
def test_wxconditions_vicinity(wx_conditions_vicinity):

    parser = Parser(wx_conditions_vicinity)
    parser.wxconditions()
    actual = parser.get_parsedObject()
    actual = actual.wxconditions

    assert isinstance(actual[0], str)
    assert actual == ['VCTS']


# ==== TESTS FOR NICHE CASES ====

@pytest.mark.usefixtures("runway_visual_range_metar")
@pytest.mark.dependency(depends=["rvr_attr"])
def test_valid_rvr_metar(runway_visual_range_metar):

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

@pytest.mark.usefixtures("normal_metar")
@pytest.mark.dependency(depends=["rvr_attr"])
def test_invalid_rvr_metar(normal_metar):

    parser = Parser(normal_metar)
    parser.runway_visual_range()
    actual = parser.get_parsedObject()
    actual = actual.runway_visual_range

    assert actual is None
