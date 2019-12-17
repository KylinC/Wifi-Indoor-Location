$(function (){
	if(!levels){
		levels = [0.1,0.3,0.7,0.8,1.6]
	};
	if(!gradient){
		gradient =  {     
		 .45: "rgb(0,0,255)",
        .55: "rgb(0,255,255)",
        .65: "rgb(0,255,0)",
        .95: "yellow",
        1: "rgb(255,0,0)"}
	}
	var levelShow = document.createElement("div");
	levelShow.style.position = "absolute",
	levelShow.style.left = "18px",
	levelShow.style.bottom = "10px",
	levelShow.style.zIndex = 999;
	levelShow.style.width = "300px"
	levelShow.style.height = "30px"
	var title = document.createElement("div");
	title.style.float = "left";
	title.style.height = "40px";
	title.style.width = "50px";
	title.style.color = "#fff";
	title.style.fontFamily = "Microsoft Yahei"
	levelShow.appendChild(title);

	var span1 = document.createElement("span");
	span1.style.display = "block";
	span1.innerText = "密度";
	span1.style.fontSize = "10px";
	title.appendChild(span1);

	var span2 = document.createElement("span");
	span2.style.display = "block";
	span2.innerText = "人/平米";
	span2.style.fontSize = "10px";
    title.appendChild(span2);
    var colors = [];
    var count = 0;
    for (var j in gradient){
  		var obj = {
  			density:j,
  			color:gradient[j]
  		}
  		colors.push(obj);
    }
    colors.sort(compare("density"));
    for(var i =0;i<levels.length;i++){
    	var block = document.createElement("div");
	    block.style.backgroundColor = colors[i].color;
		block.style.width = "50px";
		block.style.height = "10px";
		block.style.float = "left";
		block.style.color = "#fff";
		block.style.textAlign = "center";
		block.innerText  = levels[i];
		block.style.borderRight = "1px solid #000"
		block.style.lineHeight = "40px";
		levelShow.appendChild(block)
    }
	document.getElementsByTagName("body")[0].appendChild(levelShow);
})
    function compare(property){
    	return function(a ,b ){
    		var value1 = a[property];
    		var value2 = b[property];
    		return value1 - value2;
    	}
    }