var openHistorial = document.getElementById("open-historial");
var openMascotas = document.getElementById("open-mascotas");
var openPerfil = document.getElementById("open-perfil");

var contenido = document.getElementById("content");

openHistorial.addEventListener("click", function(){
    contenido.textContent = "Historial";
    console.log("Presionaste openHistorial");
});

openMascotas.addEventListener("click", function(){
    contenido.textContent = "Mascotas";
    console.log("Presionaste Mascotas");
});

openPerfil.addEventListener("click", function(){
    contenido.textContent = "Perfil";
    console.log("Presionaste openPerfil");
});



















/*var cardContent = document.getElementById("cardContent")

openPerfil.addEventListener("click", function(){
  // Obtener los datos de la tabla "Peluquera/o"
  fetch("/peluqueras/")  // Reemplaza "/peluqueras/" con la URL correcta para obtener los datos de la tabla Peluquera
    .then(response => response.json())
    .then(data => {
      // Construir el contenido HTML con los nombres de las peluqueras
      var htmlContent = "<h3>Nombres de Peluqueras:</h3>";
      for (var i = 0; i < data.length; i++) {
        htmlContent += "<p>" + + i + '. ' +data[i].nombre + "</p>";
      }
      // Mostrar el contenido HTML en el card
      cardContent.innerHTML = htmlContent;
    });
    console.log("Presionaste openPerfil");
});*/