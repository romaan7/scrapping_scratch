javascript: (function() {
    if (window.location.href.includes("scratch.mit.edu")) {

        var loggedin = document.getElementsByClassName("logged-in")[0];
        if (loggedin) {
            if (document.title === "Scratch - Imagine, Program, Share") {

                if (document.contains(document.getElementById("recommendations"))) {
                    document.getElementById("recommendations").remove();
                    document.getElementById("loader-style").remove();
                    document.getElementsByClassName("loader")[0].remove();
                } else {

                    function addStyle(styles) {
                        var css = document.createElement('style');
                        css.setAttribute("id", "loader-style");
                        css.type = 'text/css';

                        if (css.styleSheet)
                            css.styleSheet.cssText = styles;
                        else
                            css.appendChild(document.createTextNode(styles));

                        document.getElementsByTagName("head")[0].appendChild(css);
                    }

                    var styles = '.loader {margin-top:2%; border: 16px solid #f3f3f3;border-top: 16px solid #3498db;border-radius: 50%;width: 120px;z-index:9999;height: 120px;animation: spin 2s linear infinite;display:inline-block;}';
                    styles += '@keyframes spin {0% { transform: rotate(0deg); }100% { transform: rotate(360deg); }}';
                    styles += '.loader-container h1 {display:inline-block;}';
                    styles += '.loader-container {margin: 2.5% auto;text-align: center;}';
                    styles += 'body {background-color:#fcfcfc;}';

                    var username = document.getElementsByClassName("profile-name")[0].innerHTML;
                    var container = document.getElementsByClassName("inner mod-splash");

                    new_box = document.createElement("div");
                    new_box.setAttribute("class", "box");
                    new_box.setAttribute("id", "recommendations");

                    var new_box_header = document.createElement("div");
                    new_box_header.setAttribute("class", "box-header");

                    var h = document.createElement("h4");
                    var t = document.createTextNode("Personalized Recommendation");
                    h.appendChild(t);
                    new_box_header.appendChild(h);

                    var new_box_content = document.createElement("div");
                    new_box_content.setAttribute("class", "box-content");

                    new_box_content.setAttribute("id", "box-content-recommendation");

                    new_box.appendChild(new_box_header);
                    new_box.appendChild(new_box_content);

                    new_loader_container = document.createElement("div");
                    new_loader_container.setAttribute("class", "loader-container");

                    new_loader = document.createElement("div");
                    new_loader.setAttribute("class", "loader");

                    new_loader_text = document.createElement("div");

                    new_loader_text.innerHTML = "<h1>Getting personalized recommendation for user : " + username + "</h1>";

                    new_loader_container.appendChild(new_loader);
                    new_loader_container.appendChild(new_loader_text);

                    document.getElementsByTagName("body")[0].insertBefore(new_loader_container, document.getElementsByTagName("body")[0].firstChild);

                    addStyle(styles);
                    const Http = new XMLHttpRequest();
                    const url = 'http://localhost:8000/?username=' + username;
                    var data;
                    Http.open("GET", url);
                    Http.send();
                    Http.onreadystatechange = function() {
                        if (Http.readyState === 4 && Http.status === 200) {
                            data = JSON.parse(Http.responseText);
                            for (var i = 0, len = data.length; i < len; ++i) {
                                var projectName = data[i];
                                var new_thumbnail_title = document.createElement("div");
                                new_thumbnail_title.setAttribute("class", "thumbnail-title");
                                new_thumbnail_title.innerHTML = "<b>" + (i + 1) + ". &nbsp;</b><a href='/projects/" + projectName.id + "/' title='" + projectName.title + "'>" + projectName.title + "</a>" + projectName.reason+", (recommendation score:" + projectName.score + ")</i>";
                                new_box_content.appendChild(new_thumbnail_title);
                            };
                            container[0].insertBefore(new_box, container[0].firstChild);
                            new_loader_container.style.display = 'none';
                        } else if (Http.readyState === 4 && Http.status === 0) {
                            window.alert("Cannot connect to server!!. Please check if server is up and running.");
                            new_loader_container.style.display = 'none';
                        }

                    };

                }
            } else {
                window.alert("You are not on the home page!!.");
            }
        } else {
            window.alert("You are not on logged in!");
        }
    } else {
        window.alert("You are not on scratch.mit.edu!");
    }

})();