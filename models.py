class Tarea:
    def __init__(self, descripcion, fecha_limite, prioridad, tags, progreso, notas):
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.prioridad = prioridad
        self.tags = tags
        self.progreso = progreso
        self.notas = notas
        self.izquierda = None
        self.derecha = None

class Proyecto:
    def __init__(self, descripcion, descripcion_general):
        self.descripcion = descripcion
        self.descripcion_general = descripcion_general
        self.raiz_tarea = None
        self.izquierda = None
        self.derecha = None

    def agregar_tarea(self, tarea):
        if self.raiz_tarea is None:
            self.raiz_tarea = tarea
        else:
            self._insertar_tarea(self.raiz_tarea, tarea)

    def _insertar_tarea(self, nodo_actual, nueva_tarea):
        if nueva_tarea.descripcion < nodo_actual.descripcion:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nueva_tarea
            else:
                self._insertar_tarea(nodo_actual.izquierda, nueva_tarea)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nueva_tarea
            else:
                self._insertar_tarea(nodo_actual.derecha, nueva_tarea)

class Planner:
    def __init__(self):
        self.raiz = None

    def agregar_proyecto(self, descripcion, descripcion_general):
        nuevo_proyecto = Proyecto(descripcion, descripcion_general)
        if self.raiz is None:
            self.raiz = nuevo_proyecto
        else:
            self._insertar_proyecto(self.raiz, nuevo_proyecto)

    def _insertar_proyecto(self, nodo_actual, nuevo_proyecto):
        if nuevo_proyecto.descripcion < nodo_actual.descripcion:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nuevo_proyecto
            else:
                self._insertar_proyecto(nodo_actual.izquierda, nuevo_proyecto)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nuevo_proyecto
            else:
                self._insertar_proyecto(nodo_actual.derecha, nuevo_proyecto)

    def agregar_tarea(self, descripcion, fecha_limite, prioridad, tags, progreso, notas, proyecto_descripcion):
        nueva_tarea = Tarea(descripcion, fecha_limite, prioridad, tags, progreso, notas)
        proyecto = self.buscar_proyecto(proyecto_descripcion)
        if proyecto:
            proyecto.agregar_tarea(nueva_tarea)
        else:
            raise ValueError("Proyecto no encontrado")

    def obtener_todos_proyectos(self):
        proyectos = []
        self._inorden_proyectos(self.raiz, proyectos)
        return proyectos

    def _inorden_proyectos(self, nodo_actual, proyectos):
        if nodo_actual is not None:
            self._inorden_proyectos(nodo_actual.izquierda, proyectos)
            proyectos.append(nodo_actual)
            self._inorden_proyectos(nodo_actual.derecha, proyectos)

    def buscar_proyecto(self, descripcion):
        return self._buscar_proyecto(self.raiz, descripcion)

    def _buscar_proyecto(self, nodo_actual, descripcion):
        if nodo_actual is None:
            return None
        if nodo_actual.descripcion == descripcion:
            return nodo_actual
        elif descripcion < nodo_actual.descripcion:
            return self._buscar_proyecto(nodo_actual.izquierda, descripcion)
        else:
            return self._buscar_proyecto(nodo_actual.derecha, descripcion)

    def eliminar_proyecto(self, descripcion):
        self.raiz, deleted = self._eliminar_proyecto(self.raiz, descripcion)
        return deleted

    def _eliminar_proyecto(self, nodo_actual, descripcion):
        if nodo_actual is None:
            return nodo_actual, False

        deleted = False
        if descripcion < nodo_actual.descripcion:
            nodo_actual.izquierda, deleted = self._eliminar_proyecto(nodo_actual.izquierda, descripcion)
        elif descripcion > nodo_actual.descripcion:
            nodo_actual.derecha, deleted = self._eliminar_proyecto(nodo_actual.derecha, descripcion)
        else:
            deleted = True
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha, deleted
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda, deleted

            min_larger_node = self._encontrar_minimo(nodo_actual.derecha)
            nodo_actual.descripcion = min_larger_node.descripcion
            nodo_actual.descripcion_general = min_larger_node.descripcion_general
            nodo_actual.raiz_tarea = min_larger_node.raiz_tarea
            nodo_actual.derecha, _ = self._eliminar_proyecto(nodo_actual.derecha, min_larger_node.descripcion)

        return nodo_actual, deleted

    def _encontrar_minimo(self, nodo_actual):
        while nodo_actual.izquierda is not None:
            nodo_actual = nodo_actual.izquierda
        return nodo_actual

    def buscar_tarea(self, descripcion):
        proyectos = self.obtener_todos_proyectos()
        for proyecto in proyectos:
            tarea = self._buscar_tarea(proyecto.raiz_tarea, descripcion)
            if tarea:
                return tarea
        return None

    def _buscar_tarea(self, nodo_actual, descripcion):
        if nodo_actual is None:
            return None
        if nodo_actual.descripcion == descripcion:
            return nodo_actual
        elif descripcion < nodo_actual.descripcion:
            return self._buscar_tarea(nodo_actual.izquierda, descripcion)
        else:
            return self._buscar_tarea(nodo_actual.derecha, descripcion)
