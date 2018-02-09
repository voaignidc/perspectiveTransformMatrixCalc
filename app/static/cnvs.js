function windowTocanvas(canvas, x, y)
{
    var bbox = canvas.getBoundingClientRect();
    return{
        x: x - bbox.left * (canvas.width / bbox.width),
        y: y - bbox.top * (canvas.height / bbox.height)
    };
}

function cnvs_getXY(e, cid, tid)
{
    var canvas=document.getElementById(cid);
    var loc=windowTocanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    document.getElementById(tid).innerHTML="("+x+", "+y+")";
}