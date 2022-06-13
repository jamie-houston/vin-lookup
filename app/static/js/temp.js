function getResult(x){
    return x + 2;
}

function doIt(){
    var x = getResult(3);
    document.getElementById("result").innerText = x;
}

console.log(getResult(2));
