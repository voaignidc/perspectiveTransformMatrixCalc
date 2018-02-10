function windowTocanvas(canvas, x, y)
{
    var bbox = canvas.getBoundingClientRect();
    return{
        x: x - bbox.left * (canvas.width / bbox.width),
        y: y - bbox.top * (canvas.height / bbox.height)
    };
}

function cnvs_getXY(e, cnvsId, textId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowTocanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    //document.getElementById(textId).innerHTML="("+x+", "+y+")";
    document.getElementById(textId).value="("+x+", "+y+")";
}