# N 348.75 - 11.25
# NNE 11.25 - 33.75
# NE 33.75 - 56.25
# ENE 56.25 - 78.75
# E 78.75 - 101.25
# ESE 101.25 - 123.75
# SE 123.75 - 146.25
# SSE 146.25 - 168.75
# S 168.75 - 191.25
# SSW 191.25 - 213.75
# SW 213.75 - 236.25
# WSW 236.25 - 258.75
# W 258.75 - 281.25
# WNW 281.25 - 303.75
# NW 303.75 - 326.25
# NNW 326.25 - 348.75

def get_wind_direction_from_degrees(degrees):

    if not isinstance(degrees, int) and not isinstance(degrees, float):
        raise ValueError("Parameter must be integer or float.")
    if isinstance(degrees, float):
        degrees = int(degrees)

    if degrees <= 11 or degrees > 348:
        return "N"

    if 11 < degrees <= 33:
        return "NNE"

    if 33 < degrees <= 56:
        return "NE"

    if 56 < degrees <= 78:
        return "ENE"

    if 78 < degrees <= 101:
        return "E"

    if 101 < degrees <= 123:
        return "ESE"

    if 123 < degrees <= 146:
        return "SE"

    if 146 < degrees <= 168:
        return "SSE"

    if 168 < degrees <= 191:
        return "S"

    if 191 < degrees <= 213:
        return "SSW"

    if 213 < degrees <= 236:
        return "SW"

    if 236 < degrees <= 258:
        return "WSW"

    if 258 < degrees <= 281:
        return "W"

    if 281 < degrees <= 303:
        return "WNW"

    if 303 < degrees <= 326:
        return "NW"

    if 326 < degrees <= 348:
        return "NNW"
