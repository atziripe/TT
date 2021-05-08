	
function noback(){
	window.location.hash="";
	window.location.hash="Again-" //chrome
	window.onhashchange=function(){window.location.hash="";}
}