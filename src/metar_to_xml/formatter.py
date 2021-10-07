"""File to format the data coming in from the Parser to the XML maker."""

# This is what is coming FROM the parser.
# {'location' : 'KIAH', 'date' : '141953Z', 'is_auto' : 'False',
#     'wind' : '01015KT', 'visibility' : '10SM',
#     'runway_visual_range' : 'None', 'wxconditions' : 'None',
#     'cloudcoverage' : 'OVC014', 'temperature' : '25',
#     'dewpoint' : '21', 'altimeter' : 'A2972', 'remarks' : 'AO2 SLP064 T02500206',
#     'metar' : 'KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206'}
#
# Expected output from above metar (calling format()) going to xml maker.
#  {'location' : {'parsed' : 'KIAH', 'string' : 'KIAH'},
#   'date' : {'parsed' : '141953Z', 'day' : '14', 'time': '1953', 'unit' : 'Z',
#                 'string' : '14th at 19:53z'},
#     'is_auto' : {'parsed' : 'False', 'string' : 'No'},
#     'wind' : {'parsed' : '01015KT', 'direction' : 'N', 'speed' : '15',
#             'gust' : '0', 'unit' : 'kts', 'string' : 'North at 15kts (5.75mph).'},
#     'visibility' : {'parsed' : '10SM', 'value' : '10', 'unit' : 'SM',
#                     'string' : '10 Statute Miles'},
#     'rvr' : {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
#                     'unit' : 'None', 'string' : 'N/A'},
#     'wxconditions' : {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'},
#     'cloud_coverage' : {'parsed' : 'OVC014',
#                 'l1_cond' : 'Overcast', 'l1_hgt' : '1400',
#                 'l2_cond' : 'None', 'l2_hgt' : 'None',
#                 'l3_cond' : 'None', 'l3_hgt' : 'None',
#                 'l4_cond' : 'None', 'l4_hgt' : 'None',
#                 'unit' : 'feet', 'string' : 'Overcast at 1400 feet.'},
#                 {'parsed' : 'SCT040',
#                 'l1_cond' : 'Scattered', 'l1_hgt' : '4000',
#                 'l2_cond' : 'None', 'l2_hgt' : 'None',
#                 'l3_cond' : 'None', 'l3_hgt' : 'None',
#                 'l4_cond' : 'None', 'l4_hgt' : 'None',
#                 'unit' : 'feet', 'string' : 'Scattered at 4000 feet.'},
#     'temperature' : {'parsed' : '11/09', 'value' : '11', 'unit' : 'C',
#                     'string' : "11°C (51.8°F)"},
#     'dewpoint' : {'parsed' : '11/09', 'value' : '9', 'unit' : 'C',
#                     'string' : "9°C (48.2°F)"},
#     'altimeter' : {'parsed' : 'A2972', 'value' : '29.72', 'unit' : 'inHg',
#                     'string' : '29.72 inHg'},
#     'remarks' : {'parsed' : 'RMK AO2 SLP064 T02500206',
#                     'string' : 'AO2 SLP064 T02500206'}
# }

def format_parsed_information(parsed):
    pass

def location(loc):
    """Function to format location"""

    return 0

def date(date):
    """Function to format date"""

    return 0

def is_auto(auto):
    """Function to format auto"""

    return 0

def wind(wind):
    """Function to format wind"""

    return 0

def visibility(vis):
    """Function to format visibility"""
    return 0

def rvr(rvr):
    """Function to format runway visual range"""

    return 0

def conditions(cond):
    """Function to format weather conditions"""

    return 0

def coverage(cov):
    """Function to format coverage"""

    return 0

def temperature(t):
    """Function to format temperature"""

    return 0

def dewpoint(td):
    """Function to format dewpoint"""

    return 0

def altimeter(alt):
    """Function to format altimeter"""

    return 0

def remarks(rmk):
    """Function to format remarks"""

    return 0
