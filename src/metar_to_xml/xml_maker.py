from xml.dom import minidom
import os
from parser import Parser
import sys

class XMLMaker:
    """Class to construct the XML file.

    Note: this class makes it much easier to debug/test compared to one
        function to create the xml file."""

    def __init__(self):

        # Create document and create outer-most tag.
        self.root = minidom.Document()
        self.data = self.root.createElement('data')
        self.root.appendChild(self.data)

    def save(self, verbose = False):
        """Writes and saves the XML file"""

        save_file = "../mtx/src/uploads/parsed_metar.xml"

        xml_str = self.root.toprettyxml(indent = "\t")
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

    def add_location(self, value):
        """Adds location information to the XML file"""

        locationChild = self.root.createElement('location')
        locationChild.setAttribute('value', value)
        self.data.appendChild(locationChild)

    def add_date(self, date):
        """Adds time information to the XML file"""

        timeChild = self.root.createElement('time')
        timeChild.setAttribute('day', date[0])
        timeChild.setAttribute('time', date[1])
        timeChild.setAttribute('unit', 'Z')
        self.data.appendChild(timeChild)

    def add_auto(self, auto):
        autoChild = self.root.createElement('automated')
        autoChild.setAttribute('value', auto)
        self.data.appendChild(autoChild)

    def add_wind(self, wind):
        """Adds wind information to the XML file."""

        windChild = self.root.createElement('wind')

        windDirectionChild = self.root.createElement("direction")
        windDirectionChild.setAttribute('value', wind[0])
        windDirectionChild.setAttribute('angle', wind[1])
        windDirectionChild.setAttribute('unit', 'degrees')

        windSpeedChild = self.root.createElement("speed")
        windSpeedChild.setAttribute("value", wind[2])
        windSpeedChild.setAttribute("unit", "KT")

        windGustChild = self.root.createElement("gust")
        windGustChild.setAttribute('value', wind[3])
        windGustChild.setAttribute("unit", "KT")
        windChild.appendChild(windGustChild)

        windChild.appendChild(windDirectionChild)
        windChild.appendChild(windSpeedChild)
        windChild.appendChild(windGustChild)
        self.data.appendChild(windChild)

    def add_visibility_and_rvr(self, vis, rvr):
        """Adds visibilty and rvr information to the XML file.

        Grouped together because rvr is nested in visibility info"""

        visChild = self.root.createElement("visibility")

        visChild.setAttribute('value', vis)
        visChild.setAttribute('unit', 'SM')

        rvrChild = self.root.createElement("rvr")
        rvrChild.setAttribute("runway", rvr[0])
        rvrChild.setAttribute("distance", rvr[1])
        rvrChild.setAttribute("trend", rvr[2])

        visChild.appendChild(rvrChild)
        self.data.appendChild(visChild)

    def add_wx_conditions(self, wxcond):
        """Adds wx conditions string to the XML file.

        Note that parser does not currently support detailed parsing. It only
        has a direct string from the metar"""

        wxcondChild = self.root.createElement('wxconditions')

        # CHANGE AT A LATER TIME
        wxcondChild.setAttribute('values', "None")

        self.data.appendChild(wxcondChild)

    def add_clouds(self, clouds):
        """Adds cloud cover info to the XML file."""

        cloudChild = self.root.createElement('cloudcoverage')

        # itearte through all of the info found in clodus.
        for cloud_type, height in clouds:
            # create, add attributes, append
            layer = self.root.createElement('layer')
            layer.setAttribute('coverage', cloud_type)
            layer.setAttribute('height', height)
            layer.setAttribute('unit', 'Feet')
            cloudChild.appendChild(layer)

        self.data.appendChild(cloudChild)

    def add_temperature(self, temp):
        """Adds temperature value to the XML file."""

        tempChild = self.root.createElement('temperature')
        tempChild.setAttribute('value', temp)
        tempChild.setAttribute('unit', 'C')
        self.data.appendChild(tempChild)

    def add_dewpoint(self, td):
        """Adds temperature value to the XML file."""

        tempChild = self.root.createElement('dewpoint')
        tempChild.setAttribute('value', td)
        tempChild.setAttribute('unit', 'C')
        self.data.appendChild(tempChild)

    def add_altimeter(self, alt):
        """Adds altimiter value to xml file"""

        altChild = self.root.createElement("altimeter")
        altChild.setAttribute('value', alt)
        altChild.setAttribute('unit', 'In. Hg')
        self.data.appendChild(altChild)

    def add_remarks(self, remarks):
        """Adds remarks value to xml file"""

        remarkChild = self.root.createElement("remarks")
        remarkChild.setAttribute('value', remarks)
        self.data.appendChild(remarkChild)

    def add_metar(self, metar):
        """Adds the original metar to the file"""

        metarChild = self.root.createElement("metar")
        metarChild.setAttribute('value', metar)
        self.data.appendChild(metarChild)

def make_xml(metar): # the function that the user will call when they click the button

    parsed = parse_metar(metar)
    xml = XMLMaker()

    xml.add_comment("XML file created by METAR parser.")
    xml.add_metar(parsed['metar'])
    xml.add_location(parsed['location'])
    xml.add_date(parsed['date'])
    xml.add_auto(parsed['is_auto'])
    xml.add_wind(parsed['wind'])
    xml.add_visibility_and_rvr(parsed['visibility'], parsed['runway_visual_range'])
    xml.add_wx_conditions(parsed['wxconditions'])
    xml.add_clouds(parsed['cloudcoverage'])
    xml.add_temperature(parsed['temperature'])
    xml.add_dewpoint(parsed['dewpoint'])
    xml.add_altimeter(parsed['altimeter'])
    xml.add_remarks(parsed['remarks'])

    xml.save()


def parse_metar(metar):
    """Calls parser class to parse the metar"""

    parser = Parser(metar)
    parser.parse()
    parsed = parser.get_parsedObject()
    return parsed.pack()

if __name__ == "__main__":
    metar = sys.argv[1:]
    metar = " ".join(metar)
    make_xml(metar)
