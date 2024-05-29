document.addEventListener("DOMContentLoaded", function() {
    var titulosTarea = document.querySelectorAll(".titulo-tarea");

    titulosTarea.forEach(function(titulo) {
        titulo.addEventListener("click", function() {
            var id = this.getAttribute("data-id");
            var detalleTarea = document.querySelector('.detalle-tarea[data-id="' + id + '"]');

            // Alternar la visibilidad del detalle de la tarea
            if (detalleTarea.style.display === "none") {
                detalleTarea.style.display = "block";
            } else {
                detalleTarea.style.display = "none";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("editModal");
    var span = document.getElementsByClassName("close")[0];
    var editarTareaBotones = document.querySelectorAll(".editar-tarea");

    editarTareaBotones.forEach(function(boton) {
        boton.addEventListener("click", function() {
            var tareaId = this.getAttribute("data-id");
            var detalleTarea = document.querySelector(".detalle-tarea[data-id='" + tareaId + "']");

            document.getElementById("original_descripcion").value = tareaId;
            document.getElementById("edit_descripcion").value = detalleTarea.querySelector("p:nth-of-type(1)").textContent.replace('Descripción: ', '');
            document.getElementById("edit_fecha_limite").value = detalleTarea.querySelector("p:nth-of-type(2)").textContent.replace('Fecha Límite: ', '');
            document.getElementById("edit_prioridad").value = detalleTarea.querySelector("p:nth-of-type(3)").textContent.replace('Prioridad: ', '');
            document.getElementById("edit_progreso").value = detalleTarea.querySelector("p:nth-of-type(4)").textContent.replace('Progreso: ', '');
            document.getElementById("edit_tags").value = detalleTarea.querySelector("p:nth-of-type(5)").textContent.replace('Tags: ', '').split(' #').join(' ').trim();
            document.getElementById("edit_notas").value = detalleTarea.querySelector("p:nth-of-type(6)").textContent.replace('Notas: ', '');

            modal.style.display = "block";
        });
    });

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});


var eliminarTareaBtn = document.getElementById("eliminarTareaBtn");

eliminarTareaBtn.addEventListener("click", function() {
    // Confirmar la eliminación de la tarea
    var confirmar = confirm("¿Estás seguro de que quieres eliminar esta tarea?");
    if (confirmar) {
        // Obtener la descripción de la tarea
        var originalDescripcion = document.getElementById("original_descripcion").value;
        // Crear un campo oculto con la descripción de la tarea
        var form = document.getElementById("editForm");
        var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", "original_descripcion");
        input.setAttribute("value", originalDescripcion);
        form.appendChild(input);
        // Establecer la acción del formulario para eliminar y enviar el formulario
        form.action = "/eliminar";
        form.submit();
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const proyectos = document.querySelectorAll(".proyecto");
    proyectos.forEach(proyecto => {
        proyecto.addEventListener("click", function() {
            this.querySelector(".subtareas").classList.toggle("mostrar");
        });
    });
});
