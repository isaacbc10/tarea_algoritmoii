from flask import Flask, render_template, request, redirect, url_for
from models import Planner

app = Flask(__name__)
planner = Planner()

@app.route('/')
def index():
    return render_template('index.html', tareas=planner.tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    descripcion = request.form['descripcion']
    fecha_inicio = request.form['fecha_inicio']
    fecha_limite = request.form['fecha_limite']
    prioridad = request.form['prioridad']
    tags = request.form['tags'].split(',')
    estado = request.form['estado']
    notas = request.form['notas']
    planner.agregar_tarea(descripcion, fecha_inicio, fecha_limite, prioridad, tags, estado, notas)
    return redirect(url_for('index'))

@app.route('/eliminar/<descripcion>')
def eliminar(descripcion):
    planner.eliminar_tarea(descripcion)
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tarea = planner.buscar_tarea(descripcion)
        if tarea:
            return render_template('index.html', tareas=[tarea])
        else:
            return render_template('index.html', tareas=planner.tareas, error="Tarea no encontrada")
    return render_template('buscar.html')

if __name__ == '__main__':
    app.run(debug=True)
