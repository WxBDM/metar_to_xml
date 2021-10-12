import pytest

# ==== METARS that are already parsed. No niche cases. ===

# Copy and paste the below template if adding new metars.
# d = {'location' : '', 'date' : '', 'is_auto' : '',
#     'wind' : '', 'visibility' : '',
#     'runway_visual_range' : '', 'wxconditions' : '',
#     'cloudcoverage' : '', 'temperature' : '',
#     'dewpoint' : '', 'altimeter' : '', 'remarks' : '',
#     'metar' : ''}

# ======================================
# coming FROM the parser TO the formatter. Formatter takes THESE and creates NEW stuff.
# ======================================

@pytest.fixture
def normal_parsed():
    return {'location' : 'KIAH', 'date' : '141953Z', 'is_auto' : 'False',
        'wind' : '01015KT', 'visibility' : '10SM',
        'rvr' : 'None', 'conditions' : 'None',
        'coverage' : 'OVC014', 't_td' : '25/21',
        'altimeter' : 'A2972', 'remarks' : 'AO2 SLP064 T02500206',
        'metar' : 'KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206'}

@pytest.fixture
def variable_wind_parsed():
    return {'location' : 'KGNV', 'date' : '141953Z', 'is_auto' : 'False',
        'wind' : 'VRB03KT', 'visibility' : '10SM',
        'rvr' : 'None', 'conditions' : 'None',
        'coverage' : 'SCT040', 't_td' : '32/24',
        'altimeter' : 'A3001', 'remarks' : 'LTG DSNT NE-S SLPNO T03220239 $',
        'metar' : 'KGNV 141953Z VRB03KT 10SM SCT040 32/24 A3001 RMK AO2 LTG DSNT NE-S SLPNO T03220239 $'}

@pytest.fixture
def visibility_parsed():
    return {'location' : 'KNID', 'date' : '141722Z', 'is_auto' : 'False',
        'wind' : 'VRB03KT', 'visibility' : '2 1/2SM',
        'rvr' : 'None', 'conditions' : 'HZ',
        'coverage' : 'SCT000', 't_td' : '27/M01',
        'altimeter' : 'A2998', 'remarks' : 'AO2 SFC VIS 3 T02671011 $',
        'metar' : 'KNID 141722Z VRB03KT 2 1/2SM HZ SCT000 27/M01 A2998 RMK AO2 SFC VIS 3 T02671011 $'}

@pytest.fixture
def multiple_cloud_layer_parsed():
    return {'location' : 'KTPA', 'date' : '110353Z', 'is_auto' : 'False',
        'wind' : '15006KT', 'visibility' : '10SM',
        'rvr' : 'None', 'conditions' : 'VCTS',
        'coverage' : 'FEW020 FEW038 SCT110 BKN160', 't_td' : '27/23',
        'altimeter' : 'A3007', 'remarks' : 'AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233',
        'metar' : 'KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233'}

@pytest.fixture
def automated_parsed():
    return {'location' : 'KP60', 'date' : '211356Z', 'is_auto' : 'True',
        'wind' : '00000KT', 'visibility' : 'None',
        'rvr' : 'None', 'conditions' : 'None',
        'coverage' : 'None', 't_td' : 'M05/M06',
        'altimeter' : 'A3057', 'remarks' : 'AO1 SLP375 T10501056',
        'metar' : '"KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056'}

@pytest.fixture
def multiple_wx_conditions_parsed():
     return {'location' : 'KDTW', 'date' : '231453Z', 'is_auto' : 'False',
        'wind' : '25010KT', 'visibility' : '1 1/2SM',
        'rvr' : 'None', 'conditions' : '-DZ BR',
        'coverage' : 'BKN005 OVC010', 't_td' : '11/09',
        'altimeter' : 'A2967', 'remarks' : 'AO2 SFC VIS 2 1/2 DZE1356B32RAB1356E32 SLP046 P0000 60002 T01060094 51011',
        'metar' : 'KDTW 231453Z 25010KT 1 1/2SM -DZ BR BKN005 OVC010 11/09 A2967 RMK AO2 SFC VIS 2 1/2 DZE1356B32RAB1356E32 SLP046 P0000 60002 T01060094 51011'}

@pytest.fixture
def all_parsed(normal_parsed, variable_wind_parsed, visibility_parsed,
    multiple_cloud_layer_parsed, automated_parsed, multiple_wx_conditions_parsed):
    return [normal_parsed, variable_wind_parsed, visibility_parsed,
        multiple_cloud_layer_parsed, automated_parsed, multiple_wx_conditions_parsed]


# === Niche case metars - use under certain circumstances
@pytest.fixture
def runway_visual_range_parsed():
    return {'location' : 'KMBS', 'date' : '231423Z', 'is_auto' : 'False',
        'wind' : '33021G30KT', 'visibility' : '1 1/4SM',
        'rvr' : 'R23/5000VP6000FT', 'conditions' : '-RA BR',
        'coverage' : 'SCT006 OVC010', 't_td' : '10/09',
        'altimeter' : 'A2970', 'remarks' : 'AO2 PK WND 33030/1417 P0005 T0100008',
        'metar' : 'KMBS 231423Z 33021G30KT 1 1/4SM R23/5000VP6000FT -RA BR SCT006 OVC010 10/09 A2970 RMK AO2 PK WND 33030/1417 P0005 T01000089'}

@pytest.fixture
def wx_conditions_vicinity_parsed(multiple_cloud_layer_parsed):
    return multiple_cloud_layer_parsed
