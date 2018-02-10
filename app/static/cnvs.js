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

var srcImgX = new Array(0,187,0,187);
var srcImgY = new Array(0,0,119,119);
var dstImgX = new Array(0,187,0,187);
var dstImgY = new Array(0,0,119,119);

function setCookie()
{


}

function cnvsClick(e, cnvsId, selectId, inputId)
{
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    var select=document.getElementById(selectId);
    var index=select.selectedIndex ;
    var text="";
    if(cnvsId === "srcImageCanvas")
    {
        srcImgX[index]=x;
        srcImgY[index]=y;
        text="("+srcImgX[0]+", "+srcImgY[0]+"), " +
            "("+srcImgX[1]+", "+srcImgY[1]+"), " +
            "("+srcImgX[2]+", "+srcImgY[2]+"), " +
            "("+srcImgX[3]+", "+srcImgY[3]+")";
    }
    else if(cnvsId === "dstImageCanvas")
    {
        dstImgX[index]=x;
        dstImgY[index]=y;
        text="("+dstImgX[0]+", "+dstImgY[0]+"), " +
            "("+dstImgX[1]+", "+dstImgY[1]+"), " +
            "("+dstImgX[2]+", "+dstImgY[2]+"), " +
            "("+dstImgX[3]+", "+dstImgY[3]+")";

    }
    document.getElementById(inputId).value=text;
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

function cnvsDraw(cnvsId)
{
    var canvas=document.getElementById(cnvsId);
    if(cnvsId === "srcImageCanvas")
    {
        for (var k=0; k<4; k++)
        {
            cxtDrawCircleX(canvas, srcImgX[k], srcImgY[k]);
        }
    }
    else if(cnvsId === "dstImageCanvas")
    {
        for (var i=0; i<4; i++)
        {
            cxtDrawCircleX(canvas, dstImgX[i], dstImgY[i]);
        }
    }




}