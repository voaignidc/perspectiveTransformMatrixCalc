function windowToCanvas(canvas, x, y)
{
    var bbox = canvas.getBoundingClientRect();
    return{
        x: x - bbox.left * (canvas.width / bbox.width),
        y: y - bbox.top * (canvas.height / bbox.height)
    };
}



function cnvsMouseMove(e, cnvsId, textId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    document.getElementById(textId).innerHTML="鼠标滑过的坐标:("+x+", "+y+")";
}

var srcImgX = new Array();
var srcImgY = new Array();
function cnvsClick(e, cnvsId, textId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    document.getElementById(textId).value="("+x+", "+y+")";
}

function cxtDrawCircleX(canvas, x, y)
{
    var cxt=canvas.getContext("2d");
    cxt.strokeStyle="#ff0000";

    cxt.beginPath();
    cxt.arc(x,y,6,0,Math.PI*2);
    cxt.closePath();
    cxt.stroke();

    cxt.beginPath();
    cxt.moveTo(x-4, y-4);
    cxt.lineTo(x+4, y+4);
    cxt.closePath();
    cxt.stroke();

    cxt.beginPath();
    cxt.moveTo(x-4, y+4);
    cxt.lineTo(x+4, y-4);
    cxt.closePath();
    cxt.stroke();
}

function cnvsDraw(e, cnvsId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    cxtDrawCircleX(canvas, x, y);

}