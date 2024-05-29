class Tarea:
    def __init__(self, descripcion, fecha_limite, prioridad, tags, progreso, notas, proyecto_id=None):
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.prioridad = prioridad
        self.tags = tags
        self.progreso = progreso
        self.notas = notas
        self.proyecto_id = proyecto_id  # Identificador del proyecto padre (si es una subtarea)
        self.subtareas = []
        self.izquierda = None
        self.derecha = None

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)

class Planner:
    def __init__(self):
        self.raiz = None

    def agregar_tarea(self, descripcion, fecha_limite, prioridad, tags, progreso, notas, proyecto_id=None):
        nueva_tarea = Tarea(descripcion, fecha_limite, prioridad, tags, progreso, notas, proyecto_id)
        if proyecto_id is None:
            if self.raiz is None:
                self.raiz = nueva_tarea
            else:
                self._insertar(self.raiz, nueva_tarea)
        else:
            proyecto = self.buscar_tarea(proyecto_id)
            if proyecto:
                proyecto.agregar_subtarea(nueva_tarea)
            else:
                raise ValueError("Proyecto no encontrado")

    def _insertar(self, nodo_actual, nueva_tarea):
        if nueva_tarea.descripcion < nodo_actual.descripcion:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nueva_tarea
            else:
                self._insertar(nodo_actual.izquierda, nueva_tarea)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nueva_tarea
            else:
                self._insertar(nodo_actual.derecha, nueva_tarea)

    def obtener_todas_tareas(self):
        tareas = []
        self._inorden(self.raiz, tareas)
        return tareas

    def _inorden(self, nodo_actual, tareas):
        if nodo_actual is not None:
            self._inorden(nodo_actual.izquierda, tareas)
            tareas.append(nodo_actual)
            for subtarea in nodo_actual.subtareas:
                tareas.append(subtarea)
            self._inorden(nodo_actual.derecha, tareas)

    def buscar_tarea(self, descripcion):
        return self._buscar(self.raiz, descripcion)

    def _buscar(self, nodo_actual, descripcion):
        if nodo_actual is None:
            return None
        if nodo_actual.descripcion == descripcion:
            return nodo_actual
        elif descripcion < nodo_actual.descripcion:
            return self._buscar(nodo_actual.izquierda, descripcion)
        else:
            return self._buscar(nodo_actual.derecha, descripcion)

    def eliminar_tarea(self, descripcion):
        self.raiz, deleted = self._eliminar(self.raiz, descripcion)
        return deleted

    def _eliminar(self, nodo_actual, descripcion):
        if nodo_actual is None:
            return nodo_actual, False

        deleted = False
        if descripcion < nodo_actual.descripcion:
            nodo_actual.izquierda, deleted = self._eliminar(nodo_actual.izquierda, descripcion)
        elif descripcion > nodo_actual.descripcion:
            nodo_actual.derecha, deleted = self._eliminar(nodo_actual.derecha, descripcion)
        else:
            deleted = True
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha, deleted
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda, deleted

            min_larger_node = self._encontrar_minimo(nodo_actual.derecha)
            nodo_actual.descripcion = min_larger_node.descripcion
            nodo_actual.fecha_limite = min_larger_node.fecha_limite
            nodo_actual.prioridad = min_larger_node.prioridad
            nodo_actual.tags = min_larger_node.tags
            nodo_actual.progreso = min_larger_node.progreso
            nodo_actual.notas = min_larger_node.notas
            nodo_actual.derecha, _ = self._eliminar(nodo_actual.derecha, min_larger_node.descripcion)

        return nodo_actual, deleted

    def _encontrar_minimo(self, nodo_actual):
        while nodo_actual.izquierda is not None:
            nodo_actual = nodo_actual.izquierda
        return nodo_actual
