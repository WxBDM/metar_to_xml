from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
import os
from parser import Parser
from formatter import *
import sys

class XMLMaker:
    """Class to construct the XML file.

    Note: this class makes it much easier to debug/test compared to one
        function to create the xml file."""

    def __init__(self):

        self.root = Element('data')

        # Create document and create outer-most tag.
        # self.root = minidom.Document()
        # self.data = self.root.createElement('data')
        # self.root.appendChild(self.data)

    def save(self, verbose = False):
        """Writes and saves the XML file"""

        save_file = "../mtx/src/uploads/parsed_metar.xml"

        rough_string = tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        xml_str = reparsed.toprettyxml(indent="  ")

        if os.path.exists(save_file):
            os.remove(save_file)

        with open(save_file, "w") as f:
            f.write(xml_str)

    def add_comment(self, comment, append_node = None):
        # dev integreity check. English hard, spelling off.
        if not isinstance(comment, str):
            raise ValueError(f"Comment param must be a string. Found: {type(comment)}, val: {comment}")

        if append_node is None:
            self.root.appendChild(self.root.createComment(comment))
        else:
            node.appendChild(self.root.createComment(comment))

    def add_location(self, info):
        """Adds location information to the XML file"""

        # create new dictionary in-place to be used as elements.
        node = SubElement(self.root, 'location',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_date(self, info):
        """Adds time information to the XML file"""

        node = SubElement(self.root, 'date',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_auto(self, info):

        node = SubElement(self.root, 'auto',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_wind(self, info):
        """Adds wind information to the XML file."""

        node = SubElement(self.root, "wind",
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_visibility_and_rvr(self, info, rvr_info):
        """Adds visibilty and rvr information to the XML file.

        Grouped together because rvr is nested in visibility info"""

        node = SubElement(self.root, "visibility",
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

        rvr_node = SubElement(self.root, "rvr",
            {key:val for key, val in rvr_info.items() if key not in ['parsed', 'string']})
        rvr_node.text = rvr_info['string']

    def add_wx_conditions(self, info):
        """Adds wx conditions string to the XML file.

        Note that parser does not currently support detailed parsing. It only
        has a direct string from the metar"""

        node = SubElement(self.root, 'conditions',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_clouds(self, info):
        """Adds cloud cover info to the XML file."""

        node = SubElement(self.root, "cloudcoverage")
        node.text = info['string']

        for layer_n in range(1, 5):
            layer_d = {'coverage' : info[f'l{layer_n}_cond'],
                        'height' : info[f'l{layer_n}_hgt'], 'unit' : 'feet'}
            layer_node = SubElement(node, "layer", layer_d)

    def add_temperature(self, info):
        """Adds temperature value to the XML file."""

        node = SubElement(self.root, 'temperature',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_dewpoint(self, info):
        """Adds temperature value to the XML file."""

        node = SubElement(self.root, 'dewpoint',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_altimeter(self, info):
        """Adds altimiter value to xml file"""

        node = SubElement(self.root, 'altimeter',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_remarks(self, info):
        """Adds remarks value to xml file"""

        node = SubElement(self.root, 'remarks',
            {key:val for key, val in info.items() if key not in ['parsed', 'string']})
        node.text = info['string']

    def add_metar(self, info):
        """Adds the original metar to the file"""

        node = SubElement(self.root, 'metar')
        node.text = info

def make_xml(metar): # the function that the user will call when they click the button

    print(metar)
    parser = Parser(metar)
    parsed = parser.parse()

    print(parsed)
    formatted = format_parsed_information(parsed)

    xml = XMLMaker()
    # xml.add_comment("XML file created by METAR parser.")
    xml.add_metar(formatted['metar'])
    xml.add_location(formatted['location'])
    xml.add_date(formatted['date'])
    xml.add_auto(formatted['is_auto'])
    xml.add_wind(formatted['wind'])
    xml.add_visibility_and_rvr(formatted['visibility'], formatted['rvr'])
    xml.add_wx_conditions(formatted['wxconditions'])
    xml.add_clouds(formatted['cloud_coverage'])
    xml.add_temperature(formatted['temperature'])
    xml.add_dewpoint(formatted['dewpoint'])
    xml.add_altimeter(formatted['altimeter'])
    xml.add_remarks(formatted['remarks'])

    xml.save()

if __name__ == "__main__":
    metar = sys.argv[1:]
    metar = " ".join(metar)
    make_xml(metar)
