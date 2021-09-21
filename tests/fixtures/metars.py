import pytest

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
    return "KTPA 110353Z 15006KT 10SM VCTS FEW020 FEW038 SCT110 BKN160 27/23 A3007 RMK AO2 LTG DSNT W AND NW SLP182 OCNL LTGIC DSNT NW CB DSNT NW T02670233",

@pytest.fixture
def automated_metar():
    return "KP60 211356Z AUTO 00000KT M05/M06 A3057 RMK AO1 SLP375 T10501056"

@pytest.fixture
def all_metars():
    return [normal_metar, variable_wind_metar, visibility_metar,
        multiple_cloud_layer_metar, automated_metar]
