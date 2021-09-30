from xml.dom import minidom
import os
from parser import Parser
import sys

def make_xml(metar = None): # the function that the user will call when they click the button

    if metar is None:
        metar = sys.argv[0]

    save_loc_and_name = "../mtx/src/parsed_xml.xml"

    root = minidom.Document()
    root.appendChild(root.createComment("Sample XML Doc."))

    data = root.createElement('data')
    root.appendChild(data)

    locationChild = root.createElement('location')
    locationChild.setAttribute('value', 'KIAH')
    data.appendChild(locationChild)

    timeChild = root.createElement('time')
    timeChild.setAttribute('day', '14')
    timeChild.setAttribute('time', '1953')
    timeChild.setAttribute('unit', 'Z')
    data.appendChild(timeChild)

    windChild = root.createElement('wind')
    windDirectionChild = root.createElement("direction")
    windDirectionChild.setAttribute('value', 'N')
    windDirectionChild.setAttribute('angle', '10')
    windDirectionChild.setAttribute('unit', 'degrees')
    windChild.appendChild(windDirectionChild)

    windSpeedChild = root.createElement("speed")
    windSpeedChild.setAttribute("value", "15")
    windSpeedChild.setAttribute("unit", "KT")
    windChild.appendChild(windSpeedChild)

    windGustChild = root.createElement("gust")
    windGustChild.setAttribute('value', '0')
    windGustChild.setAttribute("unit", "KT")
    windChild.appendChild(windGustChild)

    data.appendChild(windChild)

    xml_str = root.toprettyxml(indent = "\t")

    with open("xml_test.xml", "w") as f:
        f.write(xml_str)


def parse_metar(metar):
    """Calls parser class to parse the metar"""

    parser = Parser(metar)
    parser.parse()
    parsed = parser.get_parsedObject()
    return parsed.d # return the dictionary associated with the parsed object.

if __name__ == "__main__":
    make_xml('KIAH 141953Z 01015KT 10SM OVC014 25/21 A2972 RMK AO2 SLP064 T02500206')
