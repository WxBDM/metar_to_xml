'use strict';

// Click the button, opens text file where the XML file is.
// Displays the METAR from the XML file.
var metarParsed = document.getElementById("SubmitButton");
metarParsed.onclick = function() {

    document.getElementById("metar_display").innerHTML = 'Loading...'

    // Put the entire table and METAR on the screen.
    document.getElementById('metar_display').innerHTML = constructTable();
}

class TableCreator {
  // A constructor for the table.
  constructor(xmlDoc) {
    this.doc = xmlDoc;
    this.table = "<table><tr><th>Item</th><th>Value</th><tr>";

    this.element_cache;
    this.attribute_tag_cache;
  }

  addRow(column1, column2) {
    // Adds a new row to the table.
    this.table += `<tr id="parsedMetarRow">
      <td id="itemName">${column1}</td>
      <td id="itemValue">${column2}</td>
    </tr>`
  }

  setTag(tag) {
    // gets a tag from the doc.
    this.element_cache = this.doc.getElementsByTagName(tag);
    this.tag = tag
    return this.element_cache;
  }

  getAttr(attr) {
    // gets an attribute from a given tag.
    this.attribute_tag_cache = this.element_cache[0].getAttribute(attr);
    return this.attribute_tag_cache;
  }

  getTextContent() {
    try {
      return this.element_cache[0].textContent
    }
    catch (err) {
      let e_str = `Providing string: not in XML file. Tag: ${this.tag}. Error:`
      console.log(e_str)
      console.log(err)
      return "Element not found in XML file."
    }
  }

  getFullTableString() {
    // returns the entire table string.
    this.table += "</table>"
    return this.table
  }
}

function constructTable() {

  var file = new XMLHttpRequest();
  file.open("GET", "./uploads/parsed_metar.xml", false);
  file.send(null);

  // Create a new parser object to get xmlDoc text.
  var parser = new DOMParser();
  var xmlDoc = parser.parseFromString(file.responseText,"text/xml");

  // Create a new table object. Cleans code up considerably, makes it easier to read.
  let table = new TableCreator(xmlDoc);

  table.setTag("metar");
  table.addRow("Original Metar", table.getTextContent());

  table.setTag("location");
  table.addRow("Location", table.getTextContent());

  table.setTag("date");
  table.addRow("Date/Time", table.getTextContent());

  table.setTag("auto");
  table.addRow("Automated", table.getTextContent());

  table.setTag("wind");
  table.addRow("Wind", table.getTextContent());

  table.setTag("visibility");
  table.addRow("Visibility", table.getTextContent());

  table.setTag("rvr");
  if (table.getTextContent() !== 'N/A') {
    table.addRow("Runway Visual Range", table.getTextContent());
  }

  table.setTag("conditions");
  table.addRow("Conditions", table.getTextContent());

  table.setTag("cloudcoverage");
  table.addRow("Cloud Coverage", table.getTextContent());

  table.setTag("temperature");
  table.addRow("Temperature", table.getTextContent());

  table.setTag("dewpoint");
  table.addRow("Dewpoint", table.getTextContent());

  table.setTag("altimeter");
  table.addRow("Altimeter", table.getTextContent());

  table.setTag("remarks");
  table.addRow("Remarks", table.getTextContent());

  return table.getFullTableString();
}
