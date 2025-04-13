from collections import deque

class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = {}

    def agregar_conexion(self, linea, estacion_destino, tiempo_viaje):
        self.conexiones[linea] = (estacion_destino, tiempo_viaje)

    def __repr__(self):
        return self.nombre


class SistemaBasadoEnReglas:
    def __init__(self):
        self.reglas = []  # Lista de reglas (condición, acción)
        self.hechos = []  # Lista de hechos iniciales

    def agregar_regla(self, condicion, accion):
        """
        Agrega una regla al sistema.
        - condicion: Función que evalúa si la regla se puede aplicar.
        - accion: Función que se ejecuta si la condición es verdadera.
        """
        self.reglas.append((condicion, accion))

    def agregar_hecho(self, hecho):
        """
        Agrega un hecho inicial al sistema.
        """
        self.hechos.append(hecho)

    def ejecutar(self):
        """
        Ejecuta el sistema, aplicando reglas a los hechos hasta que no se puedan aplicar más reglas.
        """
        cambios = True
        while cambios:
            cambios = False
            for condicion, accion in self.reglas:
                if condicion(self.hechos):
                    nuevos_hechos = accion(self.hechos)
                    for hecho in nuevos_hechos:
                        if hecho not in self.hechos:
                            self.hechos.append(hecho)
                            cambios = True


def sistema_transporte(estaciones):
    """
    Implementa el sistema de transporte masivo basado en reglas.
    """
    # Crear un sistema basado en reglas
    sistema = SistemaBasadoEnReglas()

    # Base de conocimientos: conexiones entre estaciones
    conexiones = []
    for estacion in estaciones.values():
        for linea, (destino, tiempo) in estacion.conexiones.items():
            conexiones.append((estacion.nombre, destino.nombre, linea, tiempo))

    # Regla 1: Si hay una conexión directa entre dos estaciones, entonces la ruta incluye esa conexión
    def regla_conexion_directa(hechos):
        for origen, destino, linea, tiempo in conexiones:
            if (origen, destino) not in [(h[0], h[1]) for h in hechos]:
                return True
        return False

    def accion_conexion_directa(hechos):
        nuevos_hechos = []
        for origen, destino, linea, tiempo in conexiones:
            if (origen, destino) not in [(h[0], h[1]) for h in hechos]:
                nuevos_hechos.append((origen, destino, linea, tiempo))
        return nuevos_hechos

    sistema.agregar_regla(regla_conexion_directa, accion_conexion_directa)

    # Regla 2: Si no hay conexión directa entre dos estaciones, busca una estación intermedia
    def regla_conexion_indirecta(hechos):
        for h1 in hechos:
            for h2 in hechos:
                if h1[1] == h2[0] and (h1[0], h2[1]) not in [(h[0], h[1]) for h in hechos]:
                    if h1[3] + h2[3] <= 120:  # Verificar que el tiempo total no exceda 120 minutos
                        return True
        return False

    def accion_conexion_indirecta(hechos):
        nuevos_hechos = []
        for h1 in hechos:
            for h2 in hechos:
                if h1[1] == h2[0] and (h1[0], h2[1]) not in [(h[0], h[1]) for h in hechos]:
                    tiempo_total = h1[3] + h2[3]
                    if tiempo_total <= 120:  # Añadir la ruta solo si el tiempo total es <= 120 minutos
                        nuevos_hechos.append((h1[0], h2[1], f"{h1[2]} + {h2[2]}", tiempo_total))
        return nuevos_hechos

    sistema.agregar_regla(regla_conexion_indirecta, accion_conexion_indirecta)

    # Hechos iniciales: conexiones directas conocidas
    for origen, destino, linea, tiempo in conexiones:
        sistema.agregar_hecho((origen, destino, linea, tiempo))

    # Ejecutar el sistema
    sistema.ejecutar()

    # Mostrar todas las rutas encontradas
    print("\nRutas encontradas:")
    for hecho in sistema.hechos:
        print(f"Ruta: {hecho[0]} -> {hecho[1]} (Línea: {hecho[2]}, Tiempo: {hecho[3]} minutos)")


if __name__ == "__main__":
    # Definir estaciones y sus conexiones
    estaciones_data = {
        "Tatooine": Estacion("Tatooine"),
        "Alderaan": Estacion("Alderaan"),
        "Yavin IV": Estacion("Yavin IV"),
        "Hoth": Estacion("Hoth"),
        "Dagobah": Estacion("Dagobah"),
        "Bespin": Estacion("Bespin"),
        "Endor": Estacion("Endor"),
        "Naboo": Estacion("Naboo"),
        "Coruscant": Estacion("Coruscant"),
        "Kamino": Estacion("Kamino"),
        "Mandalore": Estacion("Mandalore"),
    }
 
    # Agregar conexiones entre estaciones
    estaciones_data["Tatooine"].agregar_conexion("Ruta 1", estaciones_data["Alderaan"], 10)
    estaciones_data["Alderaan"].agregar_conexion("Ruta 2", estaciones_data["Yavin IV"], 20)
    estaciones_data["Yavin IV"].agregar_conexion("Ruta 3", estaciones_data["Hoth"], 30)
    estaciones_data["Hoth"].agregar_conexion("Ruta 4", estaciones_data["Dagobah"], 40)
    estaciones_data["Dagobah"].agregar_conexion("Ruta 5", estaciones_data["Bespin"], 50)
    estaciones_data["Bespin"].agregar_conexion("Ruta 6", estaciones_data["Endor"], 60)
    estaciones_data["Endor"].agregar_conexion("Ruta 7", estaciones_data["Naboo"], 70)
    estaciones_data["Naboo"].agregar_conexion("Ruta 8", estaciones_data["Coruscant"], 80)
    estaciones_data["Coruscant"].agregar_conexion("Ruta 9", estaciones_data["Kamino"], 90)
    estaciones_data["Kamino"].agregar_conexion("Ruta 10", estaciones_data["Mandalore"], 100)

    # Ejecutar el sistema basado en reglas
    sistema_transporte(estaciones_data)