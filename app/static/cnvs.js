function windowToCanvas(canvas, x, y) {
    var bbox = canvas.getBoundingClientRect();
    return{
        x: x - bbox.left * (canvas.width / bbox.width),
        y: y - bbox.top * (canvas.height / bbox.height)
    };
}

function cnvsMouseMove(e, cnvsId, textId) {
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    document.getElementById(textId).innerHTML="鼠标滑过的坐标:("+x+", "+y+")";
}

var srcImgCoord_X = new Array(0,187,0,187);
var srcImgCoord_Y = new Array(0,0,119,119);
var dstImgCoord_X = new Array(0,187,0,187);
var dstImgCoord_Y = new Array(0,0,119,119);

function initCoordInputAsCnvsWH(cnvsId, inputId) {
    var imageC = document.getElementById(cnvsId);
    var imageCxt = imageC.getContext("2d");

    var text ="";
    srcImgCoord_X[1] = imageCxt.canvas.width-1;
    srcImgCoord_X[3] = imageCxt.canvas.width-1;
    srcImgCoord_Y[2] = imageCxt.canvas.height-1;
    srcImgCoord_Y[3] = imageCxt.canvas.height-1;

    dstImgCoord_X[1] = imageCxt.canvas.width-1;
    dstImgCoord_X[3] = imageCxt.canvas.width-1;
    dstImgCoord_Y[2] = imageCxt.canvas.height-1;
    dstImgCoord_Y[3] = imageCxt.canvas.height-1;

    if(inputId === "srcImgCoordInput") {
        text = "(" + srcImgCoord_X[0] + ", " + srcImgCoord_Y[0] + "); " +
            "(" + srcImgCoord_X[1] + ", " + srcImgCoord_Y[1] + "); " +
            "(" + srcImgCoord_X[2] + ", " + srcImgCoord_Y[2] + "); " +
            "(" + srcImgCoord_X[3] + ", " + srcImgCoord_Y[3] + ")";
    }
    else {
        text = "(" + dstImgCoord_X[0] + ", " + dstImgCoord_Y[0] + "); " +
            "(" + dstImgCoord_X[1] + ", " + dstImgCoord_Y[1] + "); " +
            "(" + dstImgCoord_X[2] + ", " + dstImgCoord_Y[2] + "); " +
            "(" + dstImgCoord_X[3] + ", " + dstImgCoord_Y[3] + ")";
    }
    document.getElementById(inputId).value=text;
}

function initSizeInputAsCnvsWH(cnvsId, inputId) {
    var imageC = document.getElementById(cnvsId);
    var imageCxt = imageC.getContext("2d");

    var text ="";
    var w = imageCxt.canvas.width-1;
    var h = imageCxt.canvas.height-1;
    text = "(" + w + ", " + h + ")";
    document.getElementById(inputId).value=text;
}

function coordInputToCoordXY(inputId) {
    var rawStr = document.getElementById(inputId).value;
    if(rawStr === "") {
        initCoordInputAsCnvsWH("srcImageCanvas", "srcImgCoordInput");
        initCoordInputAsCnvsWH("dstImageCanvas", "dstImgCoordInput");
        initSizeInputAsCnvsWH("rstImageCanvas", "rstImgSizeInput");
    }
    var pattern = /\(/g;
    var noBracketStr = rawStr.replace(pattern, "");
    pattern = /\)/g;
    noBracketStr = noBracketStr.replace(pattern, "");
    pattern = /\s/g;
    var noBracketNoSpaceStr = noBracketStr.replace(pattern, "");
    var i = 0;
    if(inputId === "srcImgCoordInput") {
        for (i = 0; i < 4; i++) {
            srcImgCoord_X[i] = parseInt(noBracketNoSpaceStr.split(";")[i].split(",")[0]);
            srcImgCoord_Y[i] = parseInt(noBracketNoSpaceStr.split(";")[i].split(",")[1]);
        }
    }
    else if(inputId === "dstImgCoordInput") {
        for (i = 0; i < 4; i++) {
            dstImgCoord_X[i] = parseInt(noBracketNoSpaceStr.split(";")[i].split(",")[0]);
            dstImgCoord_Y[i] = parseInt(noBracketNoSpaceStr.split(";")[i].split(",")[1]);
        }
    }
}

function cnvsClick(e, cnvsId, selectId, inputId) {
    var canvas=document.getElementById(cnvsId);
    var loc=windowToCanvas(canvas, e.clientX, e.clientY);
    var x=parseInt(loc.x);
    var y=parseInt(loc.y);
    var select=document.getElementById(selectId);
    var index=select.selectedIndex ;
    var text="";
    if(cnvsId === "srcImageCanvas") {
        srcImgCoord_X[index]=x;
        srcImgCoord_Y[index]=y;
        text="("+srcImgCoord_X[0]+", "+srcImgCoord_Y[0]+"); " +
            "("+srcImgCoord_X[1]+", "+srcImgCoord_Y[1]+"); " +
            "("+srcImgCoord_X[2]+", "+srcImgCoord_Y[2]+"); " +
            "("+srcImgCoord_X[3]+", "+srcImgCoord_Y[3]+")";
    }
    else if(cnvsId === "dstImageCanvas") {
        dstImgCoord_X[index]=x;
        dstImgCoord_Y[index]=y;
        text="("+dstImgCoord_X[0]+", "+dstImgCoord_Y[0]+"); " +
            "("+dstImgCoord_X[1]+", "+dstImgCoord_Y[1]+"); " +
            "("+dstImgCoord_X[2]+", "+dstImgCoord_Y[2]+"); " +
            "("+dstImgCoord_X[3]+", "+dstImgCoord_Y[3]+")";

    }
    document.getElementById(inputId).value=text;
}

function cxtDrawCircleX(canvas, x, y) {
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

function cnvsDraw(cnvsId) {
    var canvas=document.getElementById(cnvsId);
    if(cnvsId === "srcImageCanvas") {
        for (var k=0; k<4; k++) {
            cxtDrawCircleX(canvas, srcImgCoord_X[k], srcImgCoord_Y[k]);
        }
    }
    else if(cnvsId === "dstImageCanvas") {
        for (var i=0; i<4; i++) {
            cxtDrawCircleX(canvas, dstImgCoord_X[i], dstImgCoord_Y[i]);
        }
    }
}
