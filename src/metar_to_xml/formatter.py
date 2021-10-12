"""File to format the data coming in from the Parser to the XML maker."""
try:
    from utils import get_wind_direction_from_degrees, NullReturn
except ModuleNotFoundError:
    from metar_to_xml.utils import get_wind_direction_from_degrees, NullReturn

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
#                     'string' : 'AO2 SLP064 T02500206'},
#     'metar' : 'KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206'
# }

def format_parsed_information(parsed):

    print(parsed)
    print(parsed['metar'])

    d = {'location' : location(parsed['location']),
        'date' : date(parsed['date']),
        'is_auto' : is_auto(parsed['is_auto']),
        'wind' : wind(parsed['wind']),
        'visibility' : visibility(parsed['visibility']),
        'rvr' : rvr(parsed['rvr']),
        'wxconditions' : conditions(parsed['conditions']),
        'cloud_coverage' : coverage(parsed['coverage']),
        'temperature' : temperature(parsed['t_td']),
        'dewpoint' : dewpoint(parsed['t_td']),
        'altimeter' : altimeter(parsed['altimeter']),
        'remarks' : remarks(parsed['remarks']),
        'metar' : parsed['metar']
        }

    return d

def location(loc):
    """Function to format location"""

    if loc == 'None':
        return {'parsed' : 'None', 'string' : 'N/A'}

    return {'parsed' : loc, 'string' : loc}


def date(date):
    """Function to format date"""

    if date == 'None':
        return {'parsed' : 'None', 'day' : 'None', 'time' : 'None',
            'unit' : 'None', 'string' : 'None'}

    # {'parsed' : '141953Z', 'day' : '14', 'time': '1953', 'unit' : 'Z',
    #                 'string' : '14th at 19:53z'},
    day = date[:2]
    time = date[2:-1]

    #1st 2nd 3rd, ..., 20th, etc
    if int(day) in [11, 12, 13]:
        postfix = 'th'
    elif int(day[-1]) == 1:
        postfix = 'st'
    elif int(day[-1]) == 2:
        postfix = 'nd'
    elif int(day[-1]) == 3:
        postfix = 'rd'
    else:
        postfix = 'th'

    # construct the string
    string_repr = f"{int(day)}{postfix} at {time[:2]}:{time[2:]}z"

    return {'parsed' : date, 'day' : day, 'time' : time, 'unit' : 'Z',
        'string' : string_repr}

def is_auto(auto):
    """Function to format auto"""

    if auto == 'None':
        return {'parsed' : 'None', 'string': 'N/A'}

    if auto == "True":
        formatted = "Yes"
    else:
        formatted = "No"

    return {'parsed' : auto, 'string': formatted}

def wind(wind):
    """Function to format wind"""

    wind_dir_str = {'N' : 'North', 'NNE' : "North-North East", 'NE' : 'Northeast',
        'ENE' : 'East-Northeast', 'E' : 'East', 'ESE' : 'East-Southeast',
        'SE' : 'Southeast', 'SSE' : 'South-Southeast', 'S' : 'South',
        'SSW' : 'South-Southwest', 'SW' : 'Southwest', 'WSW': 'West-Southwest',
        'W' : 'West', 'WNW' : 'West-Northwest', 'NW' : 'Northwest',
        'NNW' : 'North-Northwest'}

    if wind == 'None': # some stations don't report wind (???)
        return {'parsed' : 'None', 'direction' : 'None', 'speed' : 'None',
                'gust' : 'None', 'unit' : 'kts', 'string' : 'N/A'}

    if wind[0:3] == 'VRB':
        dir = 'VRB'
        dir_english = 'Variable'
    elif wind[0:-2] == '00000':
        dir = 'Calm'
        dir_english = 'Calm'
    else:
        dir = get_wind_direction_from_degrees(int(wind[0:3]))
        dir_english = wind_dir_str[dir]

    speed = int(wind[3:5])
    mph = '{:.2f}'.format(round(speed * 1.150779, 2))
    gust = 0 # assume it's 0, checking happens below.
    if dir != 'Calm':
        string_repr = f'{dir_english} at {speed}kts ({mph}mph)'
    else:
        string_repr = f'{dir_english} ({mph}mph)'

    cache_wind = wind.split("G")
    if len(cache_wind) == 2: # gust exists
        gust = cache_wind[1][:2]
        mph_gust = '{:.2f}'.format(round(int(gust) * 1.150779, 2))
        string_repr += f', gusting at {gust}kts ({mph_gust}mph)'

    return {'parsed' : wind, 'direction' : dir, 'speed' : str(speed),
    'gust' : str(gust), 'unit' : 'kts', 'string' : string_repr + '.'}

def visibility(vis):
    """Function to format visibility"""

    if vis == 'None':
        return {'parsed' : 'None', 'value' : 'None', 'unit' : 'None',
                'string': 'N/A'}

    if 'VV' not in vis:
        value = vis[:-2]
        unit = 'SM'
        unit_english = 'Statute Miles'
    else:
        value = f'Vertical Visibility: {int(vis[2:]) * 100}'
        unit = 'ft'
        unit_english = 'Feet'

    return {'parsed' : vis, 'value' : value, 'unit' : unit,
    'string' : f'{value} {unit_english}'}

def rvr(rvr):
    """Function to format runway visual range"""

    d = {'parsed' : 'None', 'runway' : 'None', 'value' : 'None',
            'unit' : 'None', 'string' : 'N/A'}

    if rvr == "None":
        return d

    d['parsed'] = rvr
    cache_split = rvr.split("/")
    d['unit'] = 'feet'
    d['runway'] = f'{cache_split[0][1:]}'

    # Need to check for "V" in the visual. This is "x to y".
    cache_split = cache_split[1].split("V")
    for index, element in enumerate(cache_split):
        cache_split[index] = element.replace("M", "<")
        cache_split[index] = element.replace("P", ">")
        cache_split[index] = cache_split[index].replace("FT", "")

    value_str = cache_split[0]
    if len(cache_split) == 2:
        value_str += " to " + cache_split[1]
    d['value'] = value_str
    string_repr = f'Runway {d["runway"]} at {value_str} feet.'
    d['string'] = string_repr

    return d

def conditions(cond):
    """Function to format weather conditions"""

    d = {'parsed' : 'None', 'value' : 'None', 'string' : 'N/A'}

    if cond == "None":
        return d

    # this absolutely needs to get cleaned up, but it works for now.
    cond = cond.strip()

    str_repr = ''
    str_repr_append = '' #string to append at the end.

    # Intensity. Note that +FC depicts tornado or waterspout
    if '-' in cond:
        str_repr += 'Light '
    if '+' in cond:
        if '+FC' not in cond:
            str_repr_append += 'Tornado/Waterspout'
        else:
            str_repr += 'Heavy '

    # Descriptors
    if 'MI' in cond:
        str_repr += 'Shallow '
    if 'PR' in cond:
        str_repr += 'Partial '
    if 'BC' in cond:
        str_repr += 'Patches '
    if 'DR' in cond:
        str_repr += 'Low drifting '
    if 'BL' in cond:
        str_repr += 'Blowing '
    if 'SH' in cond:
        str_repr += 'Shower(s) '
    if 'TS' in cond:
        str_repr += 'Thunderstorm '
    if 'FZ' in cond:
        str_repr += 'Freezing '

    if 'VC' in cond: # this can't be part of intensity or proximity, order matters.
        str_repr_append += "in the vicinity"

    # Conditions
    if 'DZ' in cond:
        str_repr += 'Drizzle '
    if 'RA' in cond:
        str_repr += 'Rain '
    if 'SN' in cond:
        str_repr += 'Snow '
    if 'SG' in cond:
        str_repr += 'Snow Grains '
    if 'IC' in cond:
        str_repr += 'Ice Crystals '
    if 'PL' in cond:
        str_repr += 'Ice Pellents '
    if 'GR' in cond:
        str_repr += 'Hail '
    if 'GS' in cond:
        str_repr += 'Small Hail/Snow Pellets '
    if 'UP' in cond:
        str_repr += 'Unknown Precip '

    # Obscurations
    if 'BR' in cond:
        str_repr += 'Mist '
    if 'FG' in cond:
        str_repr += 'Fog '
    if 'FU' in cond:
        str_repr += 'Smoke '
    if 'VA' in cond:
        str_repr += 'Volcanic Ash '
    if 'DU' in cond:
        str_repr += 'Widespread Dust '
    if 'SA' in cond:
        str_repr += 'Sand '
    if 'HZ' in cond:
        str_repr += 'Haze '
    if 'PY' in cond:
        str_repr += 'Spray '

    # Other
    if 'PO' in cond:
        str_repr += "Well developed dust/sand whirls "
    if 'SQ' in cond:
        str_repr += 'Squalls '
    if 'FC' in cond:
        if '+FC' not in cond:
            str_repr += 'Funnel Cloud '
    if 'SS' in cond:
        str_repr += 'Sandstorm/Duststorm '

    if str_repr_append != '':
        str_repr += str_repr_append
    else:
        str_repr = str_repr.strip()

    return  {'parsed' : cond, 'value' : cond, 'string' : str_repr}

def coverage(cov):
    """Function to format coverage"""

    d = {'parsed' : 'None', 'l1_cond' : 'None', 'l1_hgt' : 'None',
        'l2_cond' : 'None', 'l2_hgt' : 'None', 'l3_cond' : 'None', 'l3_hgt' : 'None',
        'l4_cond' : 'None', 'l4_hgt' : 'None', 'unit' : 'None', 'string' : 'N/A'}

    if cov == "None":
        return d

    d['parsed'] = cov # add in the parsed string
    d['unit'] = 'feet' # set the unit.
    coverage_split = cov.split(" ")

    # enumerate it: see default dictionary cond and hgt vars.
    cloud_d = {'CLR' : 'Clear', 'FEW' : 'Few', 'SCT' : 'Scattered',
                'BKN' : 'Broken', 'OVC' : 'Overcast'}
    string = ''
    for index, element in enumerate(coverage_split):
        if 'CLR' in element:
            d[f'l{index}_cond'] = 'Clear'
            d[f'l{index}_hgt'] = '0000'
            string = 'Clear'
        else:

            if index > 0: # adds in the comma appropriately.
                string += ", "

            # extract the conditions, make english-like, same with height.
            conditions = cloud_d[element[:3]]
            height =  str(int(element[3:]) * 100)
            # add into dictionary at appropriate height level.
            # syntax a bit tricky, but iterating through l1_hgt, l2_hgt, etc
            d[f'l{str(index + 1)}_cond'] = conditions

            if height != '0':
                d[f'l{str(index + 1)}_hgt'] = height
                # form the string and append.
                string += conditions + " at " + height + " feet"
            else:
                d[f'l{str(index + 1)}_hgt'] = "0000"
                # form the string and append.
                string += conditions + " at surface"

    string += '.' # append a period to the string.
    d['string'] = string # add in the string.
    return d

def temperature(t):
    """Function to format temperature"""

    d = {'parsed' : 'None', 'value' : 'None', 'unit' : 'None',
        'string' : "None"}

    if t == 'None':
        return d

    d['parsed'] = t
    d['unit'] = 'C'

    temp_c = int(t.split('/')[0].replace("M", '-'))
    temp_f = round((9/5) * int(temp_c) + 32, 1)
    str_repr = f'{temp_c}°C ({temp_f}°F)'
    d['value'] = str(temp_c)
    d['string'] = str_repr

    return d

def dewpoint(td):
    """Function to format dewpoint"""

    d = {'parsed' : 'None', 'value' : 'None', 'unit' : 'None',
        'string' : "None"}

    d = {'parsed' : 'None', 'value' : 'None', 'unit' : 'None',
        'string' : "None"}

    if td == 'None':
        return d

    d['parsed'] = td
    d['unit'] = 'C'

    temp_c = int(td.split('/')[1].replace("M", '-'))
    temp_f = round((9/5) * int(temp_c) + 32, 1)
    str_repr = f'{temp_c}°C ({temp_f}°F)'
    d['value'] = str(temp_c)
    d['string'] = str_repr

    return d

def altimeter(alt):
    """Function to format altimeter"""

    d = {'parsed' : 'None', 'value' : 'None', 'unit' : 'None', 'string' : 'N/A'}

    if alt == 'None':
        return d

    d['parsed'] = alt
    d['value'] = alt[1:3] + "." + alt[3:]
    d['unit'] = 'inHg'
    d['string'] = f'{d["value"]} {d["unit"]}'
    return d

def remarks(rmk):
    """Function to format remarks."""

    d = {'parsed' : 'None', 'string' : 'N/A'}

    if rmk == 'None':
        return d

    return {'parsed' : f'RMK {rmk}', 'string' : rmk}
