document.getElementById("boton-user").addEventListener("click", function() {
    console.log("Me tocaste desgenerado");
});

var boton1 = document.getElementById("boton1");
var boton2 = document.getElementById("boton2");
var content = document.getElementById("content");
var openClinica = document.getElementById("open-clinica");


openClinica.addEventListener("click", function(){
    content.textContent="hola";
});

boton2.addEventListener("click", function(){
    content.textContent="Ciao";
});
