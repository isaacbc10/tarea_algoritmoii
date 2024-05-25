from flask import Flask, render_template, request, redirect, url_for
from models import Planner

app = Flask(__name__)
planner = Planner()

@app.route('/')
def index():
    return render_template('index.html', tareas=planner.tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    try:
        descripcion = request.form['descripcion']
        fecha_limite = request.form['fecha_limite']
        prioridad = request.form['prioridad']
        tags = request.form['tags'].split(', ')
        progreso = request.form['progreso']
        notas = request.form['notas']
        planner.agregar_tarea(descripcion, fecha_limite, prioridad, tags, progreso, notas)
    except KeyError as e:
        return f"Missing field: {e}", 400

    return redirect(url_for('index'))

@app.route('/editar', methods=['POST'])
def editar():
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
    resultados = planner.buscar_tarea(query) if query else []
    return render_template('index.html', tareas=resultados, query=query)

@app.route('/eliminar', methods=['POST'])
def eliminar_tarea():
    try:
        descripcion = request.form['original_descripcion']
        if planner.eliminar_tarea(descripcion):
            return redirect(url_for('index'))
        else:
            return "Tarea no encontrada", 404
    except KeyError as e:
        return f"Missing field: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)