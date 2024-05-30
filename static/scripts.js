document.addEventListener('DOMContentLoaded', function () {
    const editarTareaButtons = document.querySelectorAll('.editar-tarea');
    editarTareaButtons.forEach(button => {
        button.addEventListener('click', function () {
            const tareaId = this.getAttribute('data-id');
            const tareaElement = document.querySelector(`.titulo-tarea[data-id="${tareaId}"]`);
            if (tareaElement) {
                const descripcion = prompt('Nueva descripción:', tareaElement.querySelector('span').textContent);
                if (descripcion !== null) {
                    fetch('/editar_tarea', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: new URLSearchParams({
                            'original_descripcion': tareaId,
                            'descripcion': descripcion,
                            'fecha_limite': tareaElement.querySelector('.fecha_limite').textContent,
                            'prioridad': tareaElement.querySelector('.prioridad').textContent,
                            'progreso': tareaElement.querySelector('.progreso').textContent,
                            'notas': tareaElement.querySelector('.notas').textContent,
                            'tags': tareaElement.querySelector('.tags').textContent.split(', ').join(', ')
                        })
                    }).then(response => {
                        if (response.ok) {
                            location.reload();
                        } else {
                            alert('Error al editar la tarea');
                        }
                    });
                }
            }
        });
    });
});
