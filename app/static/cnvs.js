function fakeClick(obj)
{  
  var ev = document.createEvent("MouseEvents");  
  ev.initMouseEvent(  
      "click", true, false, window, 0, 0, 0, 0, 0  
      , false, false, false, false, 0, null  
      );  
  obj.dispatchEvent(ev);  
} 

function savaFile(data, filename)
{
    var saveLink = document.createElement('a');
    saveLink.href = data;
    saveLink.download = filename;
    fakeClick(saveLink); 
}

function inputFileButtonChecked()
{

  var fileInput = document.getElementById("inputFileId").files[0];
  var reader = new FileReader(); 
  reader.readAsDataURL(fileInput);//将文件以Data URL形式读入页面

  reader.onload = function()
  { 
    var c = document.getElementById("srcImageCanvas"); 
    var cxt = c.getContext("2d");
    var img = new Image();
    
    img.onload = function()
    {
      cxt.drawImage(img,0,0);
    }
    img.src = reader.result;
    savaFile(reader.result, "aaa.bmp");//将图片保存到本地
  }   
}