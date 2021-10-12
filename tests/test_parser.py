import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.parser import Parser

class TestParsingLogic:

    @pytest.mark.usefixtures("all_metars")
    def test_location(self, all_metars):
        """Tests valid locations found in metars."""
        expected = ["KIAH", 'KGNV', 'KNID', 'KTPA', 'KP60']
        for metar, expected_val in zip(all_metars, expected):
            parser = Parser(metar)
            actual = parser.parse()
            assert expected_val == actual['location']

    @pytest.mark.usefixtures("automated_metar", "normal_metar")
    def test_automated(self, automated_metar, normal_metar):
        """Tests if the metar is auto or not. Valid cases."""
        # Tests an actual metar to see if it's AUTO
        parser = Parser(automated_metar)
        actual = parser.parse()
        assert actual['is_auto'] is 'True'

        # not an AUTO metar.
        parser = Parser(normal_metar)
        actual = parser.parse()
        assert actual['is_auto'] is 'False'

    @pytest.mark.usefixtures("variable_wind_metar", "normal_metar")
    def test_variable_wind(self, variable_wind_metar, normal_metar):
        """Tests a normal and variable wind metar for inclusion of variable wind."""

        parser = Parser(variable_wind_metar)
        actual = parser.parse()
        assert actual['wind'] == 'VRB03KT'

        parser = Parser(normal_metar)
        actual = parser.parse()
        assert actual['wind'] == '01015KT'

    # Need tests for visibility, wxconditions, cloudcoverage, temperature, dewpoint, altimeter, remarks
    @pytest.mark.usefixtures("normal_metar")
    def test_visibility_normal_10sm_normal(self, normal_metar):

        parser = Parser(normal_metar)
        actual = parser.parse()
        assert actual['visibility'] == '10SM'

    @pytest.mark.usefixtures("visibility_metar")
    def test_visibility_fractional_metar(self, visibility_metar):

        parser = Parser(visibility_metar)
        actual = parser.parse()
        assert actual['visibility'] == "2 1/2SM"

    @pytest.mark.usefixtures('normal_metar')
    def test_wx_conditions_none(self, normal_metar):

        parser = Parser(normal_metar)
        actual = parser.parse()
        assert actual['conditions'] is 'None'

    @pytest.mark.usefixtures('visibility_metar')
    def test_wx_conditions_haze(self, visibility_metar):

        parser = Parser(visibility_metar)
        parser.wxconditions()
        actual = parser.parse()
        assert actual['conditions'] == 'HZ'

    @pytest.mark.usefixtures('multiple_wx_conditions_metar')
    def test_wx_conditions_multiple(self, multiple_wx_conditions_metar):

        parser = Parser(multiple_wx_conditions_metar)
        actual = parser.parse()
        assert actual['conditions'] == '-RA BR'

    @pytest.mark.usefixtures('wx_conditions_vicinity')
    def test_wxconditions_vicinity(self, wx_conditions_vicinity):

        parser = Parser(wx_conditions_vicinity)
        actual = parser.parse()
        assert actual['conditions'] == 'VCTS'

class TestNicheParsingCases:

    @pytest.mark.usefixtures("normal_metar")
    def test_invalid_rvr_metar(self, normal_metar):

        parser = Parser(normal_metar)
        actual = parser.parse()
        assert actual['rvr'] == "None"
