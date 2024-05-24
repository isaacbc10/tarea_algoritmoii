class Tarea:
    def __init__(self, descripcion, fecha_limite, prioridad, tags=None, progreso=None, notas=None):
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.prioridad = prioridad
        self.progreso = progreso if progreso is not None else "No iniciado"
        self.tags = tags if tags is not None else []
        self.notas = notas if notas is not None else ""
        self.sub_tareas = []

    def agregar_sub_tarea(self, sub_tarea):
        self.sub_tareas.append(sub_tarea)

    def eliminar_sub_tarea(self, descripcion):
        for sub_tarea in self.sub_tareas:
            if sub_tarea.descripcion == descripcion:
                self.sub_tareas.remove(sub_tarea)
                return True
            if sub_tarea.eliminar_sub_tarea(descripcion):
                return True
        return False

class Planner:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, descripcion, fecha_limite, prioridad, tags=None, progreso=None, notas=None):
        nueva_tarea = Tarea(descripcion, fecha_limite, prioridad, tags, progreso, notas)
        self.tareas.append(nueva_tarea)
        return nueva_tarea

    def eliminar_tarea(self, descripcion):
        for tarea in self.tareas:
            if tarea.descripcion == descripcion:
                self.tareas.remove(tarea)
                return True
            if tarea.eliminar_sub_tarea(descripcion):
                return True
        return False

    def buscar_tarea(self, descripcion, nodo=None):
        if nodo is None:
            for tarea in self.tareas:
                resultado = self.buscar_tarea(descripcion, tarea)
                if resultado:
                    return resultado
            return None
        if nodo.descripcion == descripcion:
            return nodo
        for sub_tarea in nodo.sub_tareas:
            resultado = self.buscar_tarea(descripcion, sub_tarea)
            if resultado:
                return resultado
        return None

    def mostrar_tareas(self):
        for tarea in self.tareas:
            self._mostrar_tarea(tarea, 0)

    def _mostrar_tarea(self, tarea, nivel):
        indentacion = ' ' * (nivel * 4)
        print(f"{indentacion}Descripción: {tarea.descripcion}, Fecha Inicio: {tarea.fecha_inicio}, Fecha Límite: {tarea.fecha_limite}, Prioridad: {tarea.prioridad}, Estado: {tarea.progreso}, Tags: {tarea.tags}, Notas: {tarea.notas}")
        for sub_tarea in tarea.sub_tareas:
            self._mostrar_tarea(sub_tarea, nivel + 1)