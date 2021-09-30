from xml.dom import minidom
import os
from parser import Parser
import sys

def make_xml(): # the function that the user will call when they click the button
    root = minidom.Document()

    xml = root.createElement('root')
    root.appendChild(xml)

    productChild = root.createElement('product')
    productChild.setAttribute('name', 'Brandon Molyneaux')

    xml.appendChild(productChild)

    xml_str = root.toprettyxml(indent = "\t")

    with open("xml_test.xml", "w") as f:
        f.write(xml_str)


def parse_metar(metar):
    """Calls parser class to parse the metar"""

    parser = Parser(metar)
    parser.parse()
    parsed = parser.get_parsedObject()
    return parsed.d # return the dictionary associated with the parsed object.
