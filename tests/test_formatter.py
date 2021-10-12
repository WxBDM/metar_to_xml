import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.formatter import location, date, is_auto, wind, visibility, rvr, \
        conditions, coverage, temperature, dewpoint, altimeter, remarks, \
        format_parsed_information

## GENERAL FORM FOR FORMATTING:
# {'parsed' : VALUE,
# 'attribute1' : VALUE,
# ...
# 'attributeN' : VALUE,
# 'string' : 'string representing parsed values.'}

def get_all_methods():
    return [location('KMBS'), date('231423Z'), is_auto('False'), wind('33021G30KT'),
        visibility('1 1/4S'), rvr('R23/5000VP6000FT'), conditions('-RA BR'),
        coverage('SCT006 OVC010'), temperature('10/09'), dewpoint('10/09'),
        altimeter('A2970'), remarks('RMK AO2 PK WND 33030/1417 P0005 T01000089')]

@pytest.mark.usefixtures("all_parsed")
class TestFormatterDataStructureAndTypes:
    """Class to do unittest-like testing on the formatting functions.

    Tests the data structure (expected: dictionary) and all of the key/value
        pairs (expected: string).

    This class does NOT test the actual values, nor does it test if the keys are
        set properly.
    """

    def test_all_return_vals_are_dicts(self):
        """Tests to make sure that the return data structure is a dictionary."""

        for d in get_all_methods():
            assert isinstance(d, dict)

    def test_all_values_of_dictionaries_are_strings(self):
        """Tests to ensure all values of the dictionaries are strings."""

        for d in get_all_methods():
            for value in d.values():
                assert isinstance(value, str)

    def test_all_keys_in_dictionaries_are_strings(self):
        """Tests to make sure all keys are strings"""

        for d in get_all_methods():
            for key in d.keys():
                assert isinstance(key, str)

@pytest.mark.usefixtures("all_parsed")
class TestFormatterFunctionDictionaryKeys:
    """Class used to test if the proper keys exist in the return dictionary.

    Note: this is slightly redundant to the TestDictionaryExactly class.
        It's primarily as a precursor test to determine a "baseline" for each
        dictionary.

    Any dictionaries that only contain 'parsed' and 'string' as keys are not
        tested individually, as they're tested with `test_contains_at_least_parsed_and_string_keys`.
    """

    def test_date(self, all_parsed):
        """Tests proper keys of the date dict exist"""

        for d in all_parsed:
            formatted = date(d['date'])
            assert 'day' in formatted
            assert 'time' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_wind(self, all_parsed):
        """Tests proper keys of the wind dict exist"""

        for d in all_parsed:
            formatted = wind(d['wind'])
            assert 'direction' in formatted
            assert 'speed' in formatted
            assert 'gust' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_visibility(self, all_parsed):
        """Tests proper keys of the visibility dict exist"""

        for d in all_parsed:
            formatted = visibility(d['visibility'])
            assert 'value' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_rvr(self, all_parsed):
        """Tests proper values of the rvr dict exist"""

        for d in all_parsed:
            formatted = rvr(d['rvr'])
            assert 'runway' in formatted
            assert 'value' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_wx_conditions(self, all_parsed):
        """Tests keys of the wxconditions dict exist"""

        for d in all_parsed:
            formatted = conditions(d['conditions'])
            assert 'value' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_cloud_coverage(self, all_parsed):
        """Tests keys of the cloud coverage dict exist"""

        for d in all_parsed:
            formatted = coverage(d['coverage'])
            assert 'l1_cond' in formatted
            assert 'l1_hgt' in formatted
            assert 'l2_cond' in formatted
            assert 'l2_hgt' in formatted
            assert 'l3_cond' in formatted
            assert 'l3_hgt' in formatted
            assert 'l4_cond' in formatted
            assert 'l4_hgt' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_temperature(self, all_parsed):
        """Tests keys of the temperature dict exist """

        for d in all_parsed:
            formatted = temperature(d['t_td'])
            assert 'value' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_dewpoint(self, all_parsed):
        """Tests keys of the dewpoint dict exist"""

        for d in all_parsed:
            formatted = dewpoint(d['t_td'])
            assert 'value' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

    def test_altimeter(self, all_parsed):
        """Tests keys of the altimeter dict exist"""

        for d in all_parsed:
            formatted = altimeter(d['altimeter'])
            assert 'value' in formatted
            assert 'unit' in formatted
            assert 'parsed' in formatted
            assert 'string' in formatted

@pytest.mark.usefixtures("all_parsed", "runway_visual_range_parsed")
class TestFormatterFunctionDictionaryExactly:
    """Class to test to ensure the dictionary keys and values are properly
        set using metar fixtures.
    """

    def run_and_assert(self, expected, test_function, all_parsed, key, append_d = None):
        """Refactored code to run and assert"""

        if append_d is not None:
            all_parsed.append(append_d)

        for parsed, expected_d in zip(all_parsed, expected):
            actual = test_function(parsed[key])
            assert actual == expected_d

    def test_location(self, all_parsed):
        """Tests the location formatting.

        Expected Example: {'parsed' : 'KIAH', string : 'KIAH'}
        """

        expected = [{'parsed' : 'KIAH', 'string' : 'KIAH'},
                    {'parsed' : 'KGNV', 'string' : 'KGNV'},
                    {'parsed' : 'KNID', 'string' : 'KNID'},
                    {'parsed' : 'KTPA', 'string' : 'KTPA'},
                    {'parsed' : 'KP60', 'string' : 'KP60'},
                    {'parsed' : 'KDTW', 'string' : 'KDTW'}]

        self.run_and_assert(expected, location, all_parsed, 'location')

    def test_date(self, all_parsed):
        """Tests the date formatting.

        Expected Example: {'parsed' : '14953Z', 'day' : '14', 'string' : '14'}
        """

        expected = [{'parsed' : '141953Z', 'day' : '14', 'time': '1953', 'unit' : 'Z',
                        'string' : '14th at 19:53z'},
                    {'parsed' : '141953Z', 'day' : '14', 'time': '1953', 'unit' : 'Z',
                        'string' : '14th at 19:53z'},
                    {'parsed' : '141722Z', 'day' : '14', 'time': '1722', 'unit' : 'Z',
                        'string' : '14th at 17:22z'},
                    {'parsed' : '110353Z', 'day' : '11', 'time': '0353', 'unit' : 'Z',
                        'string' : '11th at 03:53z'},
                    {'parsed' : '211356Z', 'day' : '21', 'time': '1356', 'unit' : 'Z',
                        'string' : '21st at 13:56z'},
                    {'parsed' : '231453Z', 'day' : '23', 'time': '1453', 'unit' : 'Z',
                        'string' : '23rd at 14:53z'}]

        self.run_and_assert(expected, date, all_parsed, 'date')


    def test_is_auto_parsed(self, all_parsed):
        """Tests to ensure that is_auto is formatted properly.

        Expected Examples:
        AUTO doesn't exist:  {'parsed' : 'False', 'string' : 'No'}
        AUTO exists:         {'parsed' : 'True', 'string' : 'Yes'}
        """

        expected = [{'parsed' : 'False', 'string' : 'No'},
                    {'parsed' : 'False', 'string' : 'No'},
                    {'parsed' : 'False', 'string' : 'No'},
                    {'parsed' : 'False', 'string' : 'No'},
                    {'parsed' : 'True', 'string' : 'Yes'},
                    {'parsed' : 'False', 'string' : 'No'}]

        self.run_and_assert(expected, is_auto, all_parsed, 'is_auto')

    def test_wind_parsed(self, all_parsed, runway_visual_range_parsed):
        """Tests to ensure that wind is formatted properly.

        Expected Examples:
        No gust, normal: {'parsed' : '15007KT', 'string' : 'SSE winds at 7 knots.'}
        Gust: {'parsed' : '15007KT', 'string' : 'SSE winds at 7 knots.'}
        """

        # ======
        # Note: the rvr metar is appended to the end of the actual list.
        # Note: the conversions in the tests may need to be redone.
        # ======

        expected = [{'parsed' : '01015KT', 'direction' : 'N', 'speed' : '15',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'North at 15kts (17.26mph).'},
                    {'parsed' : 'VRB03KT', 'direction' : 'VRB', 'speed' : '3',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'Variable at 3kts (3.45mph).'},
                    {'parsed' : 'VRB03KT', 'direction' : 'VRB', 'speed' : '3',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'Variable at 3kts (3.45mph).'},
                    {'parsed' : '15006KT', 'direction' : 'SSE', 'speed' : '6',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'South-Southeast at 6kts (6.90mph).'},
                    {'parsed' : '00000KT', 'direction' : 'Calm', 'speed' : '0',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'Calm (0.00mph).'},
                    {'parsed' : '25010KT', 'direction' : 'WSW', 'speed' : '10',
                        'gust' : '0', 'unit' : 'kts', 'string' : 'West-Southwest at 10kts (11.51mph).'},
                    # rvr metar
                    {'parsed' : '33021G30KT', 'direction' : 'NNW', 'speed' : '21',
                        'gust' : '30', 'unit' : 'kts',
                        'string' : 'North-Northwest at 21kts (24.17mph), gusting at 30kts (34.52mph).'}]

        # TODO: add the test cases here. Guarenteed to fail until done.
        self.run_and_assert(expected, wind, all_parsed, 'wind',
                append_d = runway_visual_range_parsed)

    def test_visibility_parsed(self, all_parsed):
        """Tests visibility to ensure it's formatted properly."""

        expected = [{'parsed' : '10SM', 'value' : '10', 'unit' : 'SM',
                        'string' : '10 Statute Miles'},
                    {'parsed' : '10SM', 'value' : '10', 'unit' : 'SM',
                        'string' : '10 Statute Miles'},
                    {'parsed' : '2 1/2SM', 'value' : '2 1/2', 'unit' : 'SM',
                        'string' : '2 1/2 Statute Miles'},
                    {'parsed' : '10SM', 'value' : '10', 'unit' : 'SM',
                        'string' : '10 Statute Miles'},
                    {'parsed' : 'None', 'value' : 'None', 'unit' : 'None',
                        'string' : 'N/A'},
                    {'parsed' : '1 1/2SM', 'value' : '1 1/2', 'unit' : 'SM',
                        'string' : '1 1/2 Statute Miles'}]

        # TODO: add the test cases here. Guarenteed to fail until done.
        self.run_and_assert(expected, visibility, all_parsed, 'visibility')

    def test_rvr_parsed(self, all_parsed, runway_visual_range_parsed):
        """Tests runway visual range to ensure it's formatted properly."""

        expected = [{'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
                        'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'R23/5000VP6000FT', 'runway' : '23',
                        'value' : '5000 to >6000', 'unit' : 'feet',
                        'string' : 'Runway 23 at 5000 to >6000 feet.'}]

        self.run_and_assert(expected, rvr, all_parsed, 'rvr',
                append_d = runway_visual_range_parsed)

    def test_wx_conditions_parsed(self, all_parsed):
        """Tests weather conditions to ensure it's formatted properly."""

        expected = [{'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'HZ', 'value' : 'HZ', 'string' : 'Haze'},
                    {'parsed' : 'VCTS', 'value' : 'VCTS',
                        'string' : 'Thunderstorm in the vicinity'},
                    {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                    {'parsed' : '-DZ BR', 'value' : '-DZ BR',
                        'string' : 'Light Drizzle Mist'}]

        self.run_and_assert(expected, conditions, all_parsed, 'conditions')

    def test_cloud_coverage_parsed(self, all_parsed):
        """Tests cloud coverage to ensure it's formatted properly."""

        # Future note: Could reformat as such (but will break an above test):
        # {'parsed' : 'text',
        #   'layers' : {'l1_cond' : 'text', 'l1_hgt' : 'text', ...},
        #   'units' : 'feet', 'string' : 'The associated string'
        #  }

        expected = [{'parsed' : 'OVC014',
                    'l1_cond' : 'Overcast', 'l1_hgt' : '1400',
                    'l2_cond' : 'None', 'l2_hgt' : 'None',
                    'l3_cond' : 'None', 'l3_hgt' : 'None',
                    'l4_cond' : 'None', 'l4_hgt' : 'None',
                    'unit' : 'feet', 'string' : 'Overcast at 1400 feet.'},
                    {'parsed' : 'SCT040',
                    'l1_cond' : 'Scattered', 'l1_hgt' : '4000',
                    'l2_cond' : 'None', 'l2_hgt' : 'None',
                    'l3_cond' : 'None', 'l3_hgt' : 'None',
                    'l4_cond' : 'None', 'l4_hgt' : 'None',
                    'unit' : 'feet', 'string' : 'Scattered at 4000 feet.'},
                    {'parsed' : 'SCT000',
                    'l1_cond' : 'Scattered', 'l1_hgt' : '0000',
                    'l2_cond' : 'None', 'l2_hgt' : 'None',
                    'l3_cond' : 'None', 'l3_hgt' : 'None',
                    'l4_cond' : 'None', 'l4_hgt' : 'None',
                    'unit' : 'feet', 'string' : 'Scattered at surface.'},
                    {'parsed' : 'FEW020 FEW038 SCT110 BKN160',
                    'l1_cond' : 'Few', 'l1_hgt' : '2000',
                    'l2_cond' : 'Few', 'l2_hgt' : '3800',
                    'l3_cond' : 'Scattered', 'l3_hgt' : '11000',
                    'l4_cond' : 'Broken', 'l4_hgt' : '16000',
                    'unit' : 'feet',
                    'string' : 'Few at 2000 feet, Few at 3800 feet, Scattered at ' +
                                '11000 feet, Broken at 16000 feet.'},
                    {'parsed' : 'None',
                    'l1_cond' : 'None', 'l1_hgt' : 'None',
                    'l2_cond' : 'None', 'l2_hgt' : 'None',
                    'l3_cond' : 'None', 'l3_hgt' : 'None',
                    'l4_cond' : 'None', 'l4_hgt' : 'None',
                    'unit' : 'None', 'string' : 'N/A'},
                    {'parsed' : 'BKN005 OVC010',
                    'l1_cond' : 'Broken', 'l1_hgt' : '500',
                    'l2_cond' : 'Overcast', 'l2_hgt' : '1000',
                    'l3_cond' : 'None', 'l3_hgt' : 'None',
                    'l4_cond' : 'None', 'l4_hgt' : 'None',
                    'unit' : 'feet', 'string' : 'Broken at 500 feet, Overcast at 1000 feet.'}
                   ]

        self.run_and_assert(expected, coverage, all_parsed, 'coverage')

    def test_temperature_formatting(self, all_parsed):
        """Tests the temperature formatting."""

        expected = [{'parsed' : '25/21', 'value' : '25', 'unit' : 'C',
                        'string' : "25°C (77.0°F)"},
                    {'parsed' : '32/24', 'value' : '32', 'unit' : 'C',
                        'string' : "32°C (89.6°F)"},
                    {'parsed' : '27/M01', 'value' : '27', 'unit' : 'C',
                        'string' : "27°C (80.6°F)"},
                    {'parsed' : '27/23', 'value' : '27', 'unit' : 'C',
                        'string' : "27°C (80.6°F)"},
                    {'parsed' : 'M05/M06', 'value' : '-5', 'unit' : 'C',
                        'string' : "-5°C (23.0°F)"},
                    {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                        'string' : "11°C (51.8°F)"}]

        self.run_and_assert(expected, temperature, all_parsed, 't_td')

    def test_dewpoint_formatting(self, all_parsed):
        """Tests the dewpoint formatting."""

        expected = [{'parsed' : '25/21', 'value' : '21', 'unit' : 'C',
                        'string' : "21°C (69.8°F)"},
                    {'parsed' : '32/24', 'value' : '24', 'unit' : 'C',
                        'string' : "24°C (75.2°F)"},
                    {'parsed' : '27/M01', 'value' : '-1', 'unit' : 'C',
                        'string' : "-1°C (30.2°F)"},
                    {'parsed' : '27/23', 'value' : '23', 'unit' : 'C',
                        'string' : "23°C (73.4°F)"},
                    {'parsed' : 'M05/M06', 'value' : '-6', 'unit' : 'C',
                        'string' : "-6°C (21.2°F)"},
                    {'parsed' : '11/09', 'value' : '9', 'unit' : 'C',
                        'string' : "9°C (48.2°F)"}]

        self.run_and_assert(expected, dewpoint, all_parsed, 't_td')

    def test_altimeter_parsed(self, all_parsed):
        """Tests to ensure that altimeter is formatted properly."""

        expected = [{'parsed' : 'A2972', 'value' : '29.72', 'unit' : 'inHg',
                        'string' : '29.72 inHg'},
                    {'parsed' : 'A3001', 'value' : '30.01', 'unit' : 'inHg',
                        'string' : '30.01 inHg'},
                    {'parsed' : 'A2998', 'value' : '29.98', 'unit' : 'inHg',
                        'string' : '29.98 inHg'},
                    {'parsed' : 'A3007', 'value' : '30.07', 'unit' : 'inHg',
                        'string' : '30.07 inHg'},
                    {'parsed' : 'A3057', 'value' : '30.57', 'unit' : 'inHg',
                        'string' : '30.57 inHg'},
                    {'parsed' : 'A2967', 'value' : '29.67', 'unit' : 'inHg',
                        'string' : '29.67 inHg'},]

        self.run_and_assert(expected, altimeter, all_parsed, 'altimeter')

    def test_remarks_formatting(self, all_parsed):
        """Tests the formatting of the remarks"""

        expected = [{'parsed' : 'RMK AO2 SLP064 T02500206',
                        'string' : 'AO2 SLP064 T02500206'},
                    {'parsed' : 'RMK LTG DSNT NE-S SLPNO T03220239 $',
                        'string' : 'LTG DSNT NE-S SLPNO T03220239 $'},
                    {'parsed' : 'RMK AO2 SFC VIS 3 T02671011 $',
                        'string' : 'AO2 SFC VIS 3 T02671011 $'},
                    {'parsed' : 'RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233',
                        'string' : 'AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233'},
                    {'parsed' : 'RMK AO1 SLP375 T10501056',
                        'string' : 'AO1 SLP375 T10501056'},
                    {'parsed' : 'RMK AO2 SFC VIS 2 1/2 DZE1356B32RAB1356E32 SLP046 P0000 60002 T01060094 51011',
                        'string' : 'AO2 SFC VIS 2 1/2 DZE1356B32RAB1356E32 SLP046 P0000 60002 T01060094 51011'},
                   ]

        self.run_and_assert(expected, remarks, all_parsed, 'remarks')

    def test_formatted_all_has_correct_keys(self, all_parsed):
        """Tests formatted dictionary to have all appropriate keys"""

        for element in all_parsed:
            d = format_parsed_information(element)
            assert 'location' in d
            assert 'date' in d
            assert 'is_auto' in d
            assert 'wind' in d
            assert 'visibility' in d
            assert 'rvr' in d
            assert 'wxconditions' in d
            assert 'cloud_coverage' in d
            assert 'temperature' in d
            assert 'dewpoint' in d
            assert 'altimeter' in d
            assert 'remarks' in d

    def test_formatted_dtype_is_correct(self, all_parsed):
        """Tests formatted dictionary data type"""

        for expected_d in all_parsed:
            actual_d = format_parsed_information(expected_d)
            for element in actual_d:
                if element == 'metar':
                    assert isinstance(actual_d[element], str)
                else:
                    assert isinstance(actual_d[element], dict)
