var words=new Array("lorem","ipsum","dolor","sit","amet","consectetuer","adipiscing","elit","suspendisse","eget","diam","quis","diam","consequat","interdum");function AddFillerLink(){if(!document.getElementById||!document.createElement){return}var c,a;for(c=0;c<arguments.length;c++){if(document.getElementById(arguments[c])){a=document.createElement("a");a.href="#";a.appendChild(document.createTextNode("Add Text"));a.onclick=function(){AddText(this);return(false)};document.getElementById(arguments[c]).appendChild(a);b=document.createTextNode(" | ");document.getElementById(arguments[c]).appendChild(b);r=document.createElement("a");r.href="#";r.appendChild(document.createTextNode("Remove Text"));r.onclick=function(){RemoveText(this);return(false)};document.getElementById(arguments[c]).appendChild(r)}}}function AddText(e){var d="",f,c;f=RandomNumber(20,80);for(c=0;c<f;c++){d+=words[RandomNumber(0,words.length-1)]+" "}var a=document.createElement("p");a.setAttribute("class","added");a.appendChild(document.createTextNode(d));e.parentNode.insertBefore(a,e)}function RemoveText(e){var d=e.parentNode;for(var c=0;c<d.childNodes.length;c++){var a=d.childNodes[c];if(a.nodeName=="P"&&a.getAttribute("class")=="added"){d.removeChild(a);break}}}function RandomNumber(c,a){return(Math.floor(Math.random()*(a-c))+c)};