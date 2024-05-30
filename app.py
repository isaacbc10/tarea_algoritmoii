from flask import Flask, render_template, request, redirect, url_for
from models import Planner

app = Flask(__name__)
planner = Planner()

@app.route('/')
def index():
    proyectos = planner.obtener_todos_proyectos()
    return render_template('index.html', proyectos=proyectos)

@app.route('/agregar_proyecto', methods=['POST'])
def agregar_proyecto():
    try:
        descripcion = request.form['descripcion']
        descripcion_general = request.form['descripcion_general']
        planner.agregar_proyecto(descripcion, descripcion_general)
    except KeyError as e:
        return f"Missing field: {e}", 400

    return redirect(url_for('index'))

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    try:
        descripcion = request.form['descripcion']
        fecha_limite = request.form['fecha_limite']
        prioridad = request.form['prioridad']
        tags = request.form['tags'].split(', ')
        progreso = request.form['progreso']
        notas = request.form['notas']
        proyecto_descripcion = request.form['proyecto_id']

        planner.agregar_tarea(descripcion, fecha_limite, prioridad, tags, progreso, notas, proyecto_descripcion)
    except KeyError as e:
        return f"Missing field: {e}", 400

    return redirect(url_for('index'))

@app.route('/editar_tarea', methods=['POST'])
def editar_tarea():
    try:
        original_descripcion = request.form['original_descripcion']
        descripcion = request.form['descripcion']
        fecha_limite = request.form['fecha_limite']
        prioridad = request.form['prioridad']
        tags = request.form['tags'].split(', ')
        progreso = request.form['progreso']
        notas = request.form['notas']
        
        tarea = planner.buscar_tarea(original_descripcion)
        if tarea:
            tarea.descripcion = descripcion
            tarea.fecha_limite = fecha_limite
            tarea.prioridad = prioridad
            tarea.tags = tags
            tarea.progreso = progreso
            tarea.notas = notas
    except KeyError as e:
        return f"Missing field: {e}", 400

    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query')
    resultados = []
    if query:
        for proyecto in planner.obtener_todos_proyectos():
            if query.lower() in proyecto.descripcion.lower() or query.lower() in proyecto.descripcion_general.lower():
                resultados.append(proyecto)
            for tarea in proyecto.tareas:
                if query.lower() in tarea.descripcion.lower():
                    resultados.append(tarea)
    else:
        resultados = planner.obtener_todos_proyectos()
    return render_template('index.html', proyectos=resultados, query=query)

@app.route('/eliminar_proyecto', methods=['POST'])
def eliminar_proyecto():
    try:
        descripcion = request.form['descripcion']
        if planner.eliminar_proyecto(descripcion):
            return redirect(url_for('index'))
        else:
            return "Proyecto no encontrado", 404
    except KeyError as e:
        return f"Missing field: {e}", 400

@app.route('/eliminar_tarea', methods=['POST'])
def eliminar_tarea():
    try:
        descripcion = request.form['original_descripcion']
        proyectos = planner.obtener_todos_proyectos()
        for proyecto in proyectos:
            for tarea in proyecto.tareas:
                if tarea.descripcion == descripcion:
                    proyecto.tareas.remove(tarea)
                    return redirect(url_for('index'))
        return "Tarea no encontrada", 404
    except KeyError as e:
        return f"Missing field: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
