// Canvas setup
var canvas = new fabric.Canvas('canvas');
canvas.isDrawingMode = true;
canvas.freeDrawingBrush.width = 40;
canvas.freeDrawingBrush.color = "#000000";
canvas.backgroundColor = "#ffffff";
canvas.renderAll();


// Clear button callback
function clear_canvas() {
    canvas.clear();
    canvas.backgroundColor = "#ffffff";
    canvas.renderAll();
    document.getElementById("status").classList = [];
}

// Predict button callback
function send_req() {
    console.log("in req");
    document.getElementById("status").classList = ["fa", "fa-spinner", "fa-spin"];

    // Get canvas contents as url
    var fac = (1.) / 13.;
    var url = canvas.toDataURL('png', fac);

    var jq = $.post('/find-similar/', url)
        .done(function (json) {
                console.log(json);
                for(ii = 0; ii < 9; ii++){
                    var img_element = document.getElementById("img" + (ii+1).toString());
                    console.log("img" + ii.toString());
                    img_element.setAttribute("src", json[ii].image);
                }
            }
        ).fail(function(xhr, textStatus, error){
            document.getElementById("status").classList = ["fa", "fa-exclamation-triangle"];
            console.log("POST Error: " + xhr.responseText + ", " + textStatus + ", " + error);
        });

}

if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}