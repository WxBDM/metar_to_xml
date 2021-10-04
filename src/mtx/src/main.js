'use strict';

// Click the button, get a new message.
var metarParsed = document.getElementById("SubmitButton");
metarParsed.onclick = function() {

  // Get the value from the text box (in this case, the metar)
  var textFromTextBox = document.getElementById("TextBox").value

  // Checking to ensure that there isn't anything there.
  if (!textFromTextBox) {
    string_to_show = "No METAR inputted."
  }
  else { // There is a valid metar that shows.

    exec(`python3 ../../metar_to_xml/xml_maker.py ${textFromTextBox}`, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });

    const { exec } = require("child_process");

    // construct the string.
    var string_to_show = `<p>METAR: ${textFromTextBox}<br>`

    // Call the constructTable function to create the table.
    // Append it to the string to show on the web page.
    var table = constructTable()
    string_to_show += table
  }

  document.getElementById('display_metar').innerHTML = string_to_show;
}

class TableConstructor {
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
    return this.element_cache;
  }

  getAttr(attr) {
    // gets an attribute from a given tag.
    this.attribute_tag_cache = this.element_cache[0].getAttribute(attr);
    return this.attribute_tag_cache;
  }

  getFullTableString() {
    // returns the entire table string.
    this.table += "</table>"
    return this.table
  }
}

function tagName(tag) {
  // To clean up the code a bit.
  return xmlDoc.getElementsByTagName(tag);
}

function constructTable() {

  var file = new XMLHttpRequest();
  file.open("GET", "./uploads/parsed_metar.xml", false);
  file.send(null);

  // Create a new parser object to get xmlDoc text.
  var parser = new DOMParser();
  var xmlDoc = parser.parseFromString(file.responseText,"text/xml");

  // Create a new table object. Cleans code up considerably, makes it easier to read.
  let table = new TableConstructor(xmlDoc);

  table.setTag("location");
  table.addRow("Location", table.getAttr("value"));

  table.setTag("time");
  table.addRow("Day", table.getAttr("day"));
  table.addRow("Time", table.getAttr("time") + " " + table.getAttr("unit"));

  table.setTag("automated")
  table.addRow("Automated", table.getAttr("value"));

  // TODO: wind
  // TODO: visibility

  //always None until parser gets updated.
  table.setTag("wxconditions")
  table.addRow("Conditions", table.getAttr("values"));

  // TODO: cloud coverage.

  table.setTag("temperature")
  table.addRow("Temperature", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("dewpoint")
  table.addRow("Dewpoint", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("altimeter")
  table.addRow("Altimeter", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("remarks")
  table.addRow("Remarks", table.getAttr("value"));

  return table.getFullTableString();
}
