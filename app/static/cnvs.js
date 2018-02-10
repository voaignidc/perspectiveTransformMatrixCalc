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
    document.getElementById(textId).innerHTML="("+x+", "+y+")";
}

function cnvsClick(e, cnvsId, textId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    document.getElementById(textId).value="("+x+", "+y+")";
}

function cnvsDraw(e, cnvsId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    var cxt=canvas.getContext("2d");
    cxt.fillStyle="#ff0000";
    cxt.beginPath();
    cxt.arc(x,y,6,0,Math.PI*2);
    cxt.closePath();
    cxt.fill();
}