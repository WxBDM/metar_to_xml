'use strict';

// Click the button, opens text file where the XML file is.
// Displays the METAR from the XML file.
var metarParsed = document.getElementById("SubmitButton");
metarParsed.onclick = function() {

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
  table.addRow("Original Metar", table.getAttr('value'));

  table.setTag("location");
  table.addRow("Location", table.getAttr("value"));

  table.setTag("time");
  table.addRow("Day", table.getAttr("day"));
  table.addRow("Time", table.getAttr("time") + table.getAttr("unit"));

  table.setTag("automated");
  table.addRow("Automated", table.getAttr("value"));

  let wind_str = ""
  table.setTag("direction");
  if (table.getAttr('value') === 'VRB') {
    wind_str += "Variable winds at "
  }
  else {
    wind_str += `${table.getAttr('value')} winds at `
  }
  table.setTag("speed");
  wind_str += `${table.getAttr('value')} knots`

  table.setTag("gust");
  if (table.getAttr("value") != 0) {
    wind_str += `, Gusting at ${table.getAttr('value')} knots.`
  }
  else {
    wind_str += '.' // it's a sentence, need to end it properly :^)
  }
  table.addRow("Wind", wind_str);

  // TODO: visibility
  table.setTag("visibility");
  table.addRow("Visibility", `${table.getAttr("value")} SM`);

  // RVR. Not always there.
  table.setTag("rvr");
  let runway_attr = table.getAttr("runway");
  if (runway_attr !== "None") {
    let rvr_str = "";
    rvr_str += `Runway: ${runway_attr}\n`;
    rvr_str += `Distance: ${table.getAttr("distance")}`;
    let trend_attr = table.getAttr("trend");
    if (trend_attr !== "None") {
      rvr_str += `\nTrend: ${trend_attr}`;
    }
    table.addRow("Runway Visual Range", rvr_str);
  }

  //always None until parser gets updated.
  table.setTag("wxconditions");
  table.addRow("Conditions", "N/A (not implemented)");

  let layers = table.setTag("layer");
  let cloud_str = ""
  for (let i = 0; i < layers.length; i++) {
    let coverage_attr = layers[i].getAttribute("coverage");
    if (coverage_attr !== "None") {
      let height_attr = layers[i].getAttribute("height");
      cloud_str += `${coverage_attr} at ${height_attr} FT, `
    }
  }
  if (cloud_str === "") {
    cloud_str = "None";
  }
  table.addRow("Cloud Coverage", cloud_str);

  table.setTag("temperature");
  table.addRow("Temperature", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("dewpoint");
  table.addRow("Dewpoint", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("altimeter");
  table.addRow("Altimeter", table.getAttr("value") + " " + table.getAttr("unit"));

  table.setTag("remarks");
  table.addRow("Remarks", table.getAttr("value"));

  return table.getFullTableString();
}
