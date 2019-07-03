
'use strict';


chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.executeScript(
        tabs[0].id,
        {code: 'var container = document.getElementsByClassName("inner mod-splash"); new_box = document.createElement("div");var new_box_header = document.createElement("div");new_box_header.setAttribute("class", "box-header");  var h = document.createElement("H4");var t = document.createTextNode("Your Personalised recommendation");h.appendChild(t);new_box_header.appendChild(h);var new_box_content = document.createElement("div");new_box_content.setAttribute("class", "box-content");new_box.setAttribute("id", "recommendations");new_box.setAttribute("class", "box");new_box.appendChild(new_box_header);new_box.appendChild(new_box_content);container[0].insertBefore(new_box, container[0].firstChild);'});
		
  });


changeColor.onclick = function myFunction() {
  var x = document.getElementById("recommendations");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
