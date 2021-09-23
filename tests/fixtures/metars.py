import pytest

# ==== METARS to be used for validation. No niche cases. ===

@pytest.fixture
def normal_metar():
    return "KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206"

@pytest.fixture
def variable_wind_metar():
    return "KGNV 141953Z VRB03KT 10SM SCT040 32/24 A3001 RMK AO2 LTG DSNT NE-S SLPNO T03220239 $"

@pytest.fixture
def visibility_metar():
    return "KNID 141722Z VRB03KT 2 1/2SM HZ SCT000 27/M01 A2998 RMK AO2 SFC VIS 3 T02671011 $"

@pytest.fixture
def multiple_cloud_layer_metar():
    return "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233"

@pytest.fixture
def automated_metar():
    return "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056"

@pytest.fixture
def multiple_wx_conditions_metar():
    return 'KDTW 231453Z 25010KT 1 1/2SM -DZ BR BKN005 OVC010 11/09 A2967 RMK AO2 SFC VIS 2 1/2 DZE1356B32RAB1356E32 SLP046 P0000 60002 T01060094 51011'

@pytest.fixture
def all_metars(automated_metar, multiple_cloud_layer_metar, visibility_metar,
    variable_wind_metar, normal_metar, multiple_wx_conditions_metar):
    return [normal_metar, variable_wind_metar, visibility_metar,
        multiple_cloud_layer_metar, automated_metar, multiple_wx_conditions_metar]


# === Niche case metars - use under certain circumstances
@pytest.fixture
def runway_visual_range_metar():
    return "KMBS 231423Z 33021G30KT 1 1/4SM R23/5000VP6000FT -RA BR SCT006 OVC010 10/09 A2970 RMK AO2 PK WND 33030/1417 P0005 T01000089"

@pytest.fixture
def wx_conditions_vicinity(multiple_cloud_layer_metar):
    return multiple_cloud_layer_metar
