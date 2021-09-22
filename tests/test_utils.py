import unittest
import sys
sys.path.insert(0, '/Users/bdmolyne/Documents/metar_to_xml/src')
from metar_to_xml.utils import get_wind_direction_from_degrees

def test_correct_wind_dir_not_bounds():

    """Tests a random direction to ensure it kicks back the right direction"""

    test_info = [(0, 'N'), (20, 'NNE'), (40, 'NE'), (60, 'ENE'), (80, 'E'),
    (115, 'ESE'), (130, 'SE'), (150, 'SSE'), (170, 'S'), (192, 'SSW'),
    (215, 'SW'), (240, 'WSW'), (270, 'W'), (290, 'WNW'), (310, 'NW'),
    (330, 'NNW')]

    for direction, expected in test_info:
        actual = get_wind_direction_from_degrees(direction)
        assert actual == expected

def test_correct_wind_dir_bounds():

    """Tests the whole value bounds to ensure it kicks back the right direction"""

    bounds = [('N', 349, 11), ('NNE', 12, 33), ('NE', 34, 56),
    ('ENE', 57, 78), ('E', 79, 101), ('ESE', 102, 123), ('SE', 124, 146),
    ('SSE', 147, 168), ('S', 169, 191), ('SSW', 192, 213), ('SW', 214, 236),
    ('WSW', 237, 258), ('W', 259, 281), ('WNW', 282, 303), ('NW', 304, 326),
    ('NNW', 327, 348)]


    for direction, lower, upper in bounds:
        actual = get_wind_direction_from_degrees(lower)
        assert actual == direction

        actual = get_wind_direction_from_degrees(upper)
        assert actual == direction
