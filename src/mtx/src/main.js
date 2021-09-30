'use strict';

// Click the button, get a new message.
var metarParsed = document.getElementById("SubmitButton");
metarParsed.onclick = function() {

  // Get the value from the text box (in this case, the metar)
  var textFromTextBox = document.getElementById("TextBox").value

  // Checking to ensure that there isn't anything there.
  if (!textFromTextBox) {
    console.log("nothing is there!");
    string_to_show = "No METAR inputted."
  }
  else {
    var string_to_show = `
      METAR: ${textFromTextBox}<br>
      <table>
        <tr>
          <th>Item</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Input</td>
          <td>${textFromTextBox}</td>
        </tr>
      </table>
    `
  }

  document.getElementById('display_metar').innerHTML = string_to_show;
}
