var httpStatusSuccess = 200
var httpStatusBadrequest = 400
var httpStatusForbidden = 404
var httpStatusFailure = 420
var httpStatusServererror = 500

function requestCode() {
    httpGetAsync("/icloud/authentication/2fa/code/request", "POST", null, requestCode_callback);
}
function requestCode_callback(result, response={}) {
    if (result==httpStatusSuccess) {
        document.getElementById("alert_request").className = "alert alert-success";
        document.getElementById("alert_request").innerHTML = "Code requested";
    } else if (result==httpStatusFailure) {
        document.getElementById("alert_request").className = "alert alert-warning";
        document.getElementById("alert_request").innerHTML = response.error;
    } else {
        document.getElementById("alert_request").className = "alert alert-danger";
        document.getElementById("alert_request").innerHTML = "An error has occurred, please try again.";
    }
    document.getElementById("alert_request").style.visibility = "inherit";
}

function validateCode() {
    var code = document.getElementById("codeInput").value;
    httpGetAsync("/icloud/authentication/2fa/code/validate", "POST", {'2fa_code': code}, validateCode_callback);
}
function validateCode_callback(result, response={}) {
    if (httpStatusSuccess) {
        document.getElementById("alert_validate").className = "alert alert-success";
        document.getElementById("alert_validate").innerHTML = "Code validation successful";
    } else {
        document.getElementById("alert_validate").className = "alert alert-danger";
        document.getElementById("alert_validate").innerHTML = "An error has occurred, please try again.";
    }
    document.getElementById("alert_validate").style.visibility = "inherit";
}

function httpGetAsync(theUri, method, body, callback) {
    //
    //var service_header_clientid_label = "jarvis.client-service";
    //var service_id = "icloud_2fa";
    //
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == httpStatusSuccess) {
                // operation success
                callback(httpStatusSuccess);
            } else if (xmlHttp.status == httpStatusFailure) {
                // operation failure
                callback(httpStatusFailure, JSON.parse(xmlHttp.responseText));
            } else if (xmlHttp.status == httpStatusBadrequest ||
                        xmlHttp.status == httpStatusForbidden ||
                        xmlHttp.status == httpStatusServererror) {
                // failures such as forbidden, server error, etc.
                callback(false);
            }
         }
    }
    xmlHttp.open(method, theUri, true); // true for asynchronous
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    //xmlHttp.setRequestHeader(service_header_clientid_label, service_id);
    if (body) {
        xmlHttp.send(JSON.stringify(body));
    } else {
        xmlHttp.send(null);
    }
    //
}