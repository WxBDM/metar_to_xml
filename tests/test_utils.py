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

    bounds = [('N', 348, 11), ('NNE', 11, 33), ('NE', 33, 56),
    ('ENE', 56, 78), ('E', 78, 101), ('ESE', 101, 123), ('SE', 123, 146),
    ('SSE', 146, 168), ('S', 168, 191), ('SSW', 191, 213), ('SW', 213, 236),
    ('WSW', 236, 258), ('W', 258, 281), ('WNW', 281, 303), ('NW', 303, 326),
    ('NNW', 326, 348)]


    for direction, lower, upper in bounds:
        actual = get_wind_direction_from_degrees(lower)
        assert actual == direction

        actual = get_wind_direction_from_degrees(upper)
        assert actual == direction
