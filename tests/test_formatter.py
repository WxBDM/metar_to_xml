import pytest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.formatter import location, date, is_auto, wind, visibility, rvr, conditions, coverage, t_td, altimeter, remarks

## GENERAL FORM FOR FORMATTING:
# {'parsed' : VALUE,
# 'attribute1' : VALUE,
# ...
# 'attributeN' : VALUE,
# 'string' : 'string representing parsed values.'}

def get_all_methods():
    return [location('dummy'), date('dummy'), is_auto('dummy'), wind('dummy'),
        visibility('dummy'), rvr('dummy'), conditions('dummy'), coverage('dummy'),
        t_td('dummy'), altimeter('dummy'), remarks('dummy')]

def test_all_values_of_dictionaries_are_strings():
    """Tests to ensure all values of the dictionaries are strings."""

    for d in get_all_methods():
        values = d.values()
        for value in values:
            assert isinstance(value, str)

def test_contains_at_least_parsed_and_string_keys():
    """Tests to ensure that each dictionary has a parsed and string key at minimum."""

    for d in get_all_methods():
        keys = d.keys()
        # check to see if these values are in the keys.
        assert 'parsed' in keys
        assert 'string' in keys

def test_all_keys_in_dictionaries_are_strings():
    """Tests to make sure all keys are strings"""

    for d in get_all_methods():
        keys = d.keys()
        for key in keys:
            assert isinstance(key, str)

@pytest.mark.usefixtures("all_parsed")
def test_location_formatting(all_parsed):
    """Tests the location formatting.

    Expected Example: {'parsed' : 'KIAH', string : 'KIAH'}
    """

    expected = [{'parsed' : 'KIAH', 'string' : 'KIAH'},
                {'parsed' : 'KGNV', 'string' : 'KGNV'},
                {'parsed' : 'KNID', 'string' : 'KNID'},
                {'parsed' : 'KTPA', 'string' : 'KTPA'},
                {'parsed' : 'KP60', 'string' : 'KP60'},
                {'parsed' : 'KTDW', 'string' : 'KTDW'}]

    # TODO: add in the test case here. Guarenteed to fail unit done.
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_date_formatting(all_parsed):
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

    # TODO: add the test cases here. Guarenteed to fail until done.
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_is_auto_parsed(all_parsed):
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

    # TODO: add the test cases here. Guarenteed to fail until done.
    assert False is True

@pytest.mark.usefixtures("all_parsed", "runway_visual_range_parsed")
def test_wind_parsed(all_parsed, runway_visual_range_parsed):
    """Tests to ensure that wind is formatted properly.

    Expected Examples:
    No gust, normal: {'parsed' : '15007KT', 'string' : 'SSE winds at 7 knots.'}
    Gust: {'parsed' : '15007KT', 'string' : 'SSE winds at 7 knots.'}
    """

    # ======
    # Note: the rvr metar is appended to the end of the actual list.
    all_parsed.append(runway_visual_range_parsed)
    # Note: the conversions in the tests may need to be redone.
    # ======

    expected = [{'parsed' : '01015KT', 'direction' : 'N', 'speed' : '15',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'North at 15kts (5.75mph).'},
                {'parsed' : 'VRB03KT', 'direction' : 'Variable', 'speed' : '3',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'Variable at 3kts (3.45mph).'},
                {'parsed' : 'VRB03KT', 'direction' : 'Variable', 'speed' : '3',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'Variable at 3kts (3.45mph).'},
                {'parsed' : '15006KT', 'direction' : 'SSE', 'speed' : '6',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'SSE at 6kts (6.90mph).'},
                {'parsed' : '00000KT', 'direction' : 'Calm', 'speed' : '0',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'Calm.'},
                {'parsed' : '25010KT', 'direction' : 'WSW', 'speed' : '10',
                    'gust' : '0', 'unit' : 'kts', 'string' : 'West-South West at 10kts (11.50mph).'},
                # rvr metar
                {'parsed' : '33021G30KT', 'direction' : 'NNW', 'speed' : '21',
                    'gust' : '30', 'unit' : 'kts',
                    'string' : 'North-North West at 21kts (21.16mph), gusting at 30kts (34.52mph).'}]

    # TODO: add the test cases here. Guarenteed to fail until done.
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_visibility_parsed(all_parsed):
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
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_rvr_parsed(all_parsed):
    """Tests runway visual range to ensure it's formatted properly."""

    expected = [{'parsed' : 'None', 'value' : '10', 'unit' : 'SM',
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
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_wx_conditions_parsed(all_parsed):
    """Tests weather conditions to ensure it's formatted properly."""

    expected = [{'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                {'parsed' : 'HZ', 'value' : 'HZ', 'string' : 'Haze'},
                {'parsed' : 'VCTS', 'value' : 'VCTS',
                    'string' : 'Thunderstorm in the Vicitity'},
                {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
                {'parsed' : '-DZ BR', 'value' : '-DZ BR',
                    'string' : 'Light drizzle, mist'}]

    # TODO: add the test cases here. Guarenteed to fail until done.
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_wx_conditions_parsed(all_parsed):
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
                'string' : 'Few at 2000 feet, Few at 3800 feet, Scattered at \
                            11000 feet, Broken at 16000 feet.'},
                {'parsed' : 'None',
                'l1_cond' : 'None', 'l1_hgt' : 'None',
                'l2_cond' : 'None', 'l2_hgt' : 'None',
                'l3_cond' : 'None', 'l3_hgt' : 'None',
                'l4_cond' : 'None', 'l4_hgt' : 'None',
                'unit' : 'feet', 'string' : 'N/A'},
                {'parsed' : 'BKN005 OVC010',
                'l1_cond' : 'Broken', 'l1_hgt' : '500',
                'l2_cond' : 'Overcast', 'l2_hgt' : '1000',
                'l3_cond' : 'None', 'l3_hgt' : 'None',
                'l4_cond' : 'None', 'l4_hgt' : 'None',
                'unit' : 'feet', 'string' : 'Broken at 500 feet, Overcast at 1000 feet.'}
               ]

    # TODO: add the test cases here. Guarenteed to fail until done.
    assert False is True

@pytest.mark.usefixtures("all_parsed")
def test_location_formatting(all_parsed):
    """Tests the location formatting.

    Expected Example: {'parsed' : 'KIAH', string : 'KIAH'}
    """

    # TO DO: This. Lunch time.
    expected = [{'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"},
                {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"},
                {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"},
                {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"},
                {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"},
                {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
                    'string' : "11°C (51.8°F)"}]

    # TODO: add in the test case here. Guarenteed to fail unit done.
    assert False is True
