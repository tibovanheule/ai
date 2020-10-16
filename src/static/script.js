function fadeOut(element) {
    let op = 1;
    let timer = setInterval(() => {
        if (op <= 0.1){
            clearInterval(timer);
            element.style.display = 'none';
        }else{
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.2;
	}
    }, 40);
}

function fadeIn(element) {
    element.style.display = 'block'
    let op = 0.1;  // initial opacity
    let timer = setInterval(() => {
        if (op > 0.95){
            clearInterval(timer);
	    element.style.opacity = 1;
        }else{
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.2;
	}
    }, 40);
}

function analyse(){
	if(document.getElementById("tweet").textLength){
	fadeOut(document.getElementById("text_input"))
	
	fetch('https://ai.tibovanheule.space/api/analyse',{
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
       body: JSON.stringify({message:document.getElementById("tweet").value}) // body data type must match "Content-Type" header
  })
  .then(data=> data.text())
  .then(data => {
console.log(data);
document.getElementById("response").innerHTML = data;
fadeIn(document.getElementById("validate"));
});
	
	
	}
}