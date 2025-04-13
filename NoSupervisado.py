from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Clase Estacion
class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = {}

    def agregar_conexion(self, linea, estacion_destino, tiempo_viaje):
        self.conexiones[linea] = (estacion_destino, tiempo_viaje)

    def __repr__(self):
        return self.nombre


# Generar datos a partir de las conexiones especificadas
def generar_datos(estaciones):
    data = {
        "Estacion Origen": [],
        "Estacion Destino": [],
        "Linea": [],
        "Tiempo (min)": [],
    }

    for estacion in estaciones.values():
        for linea, (destino, tiempo) in estacion.conexiones.items():
            data["Estacion Origen"].append(estacion.nombre)
            data["Estacion Destino"].append(destino.nombre)
            data["Linea"].append(linea)
            data["Tiempo (min)"].append(tiempo)

    # Crear un DataFrame
    df = pd.DataFrame(data)
    return df


# Preparar los datos para el modelo no supervisado
def preparar_datos(df):
    # Transformar columnas categóricas en valores numéricos
    le = LabelEncoder()
    df["Estacion Origen"] = le.fit_transform(df["Estacion Origen"])
    df["Estacion Destino"] = le.fit_transform(df["Estacion Destino"])
    df["Linea"] = le.fit_transform(df["Linea"])

    # Escalar las características numéricas
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    return df_scaled


# Aplicar K-Means para el agrupamiento
def aplicar_kmeans(df, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["Cluster"] = kmeans.fit_predict(df)
    return df, kmeans


# Visualizar los resultados
def visualizar_agrupamiento(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Tiempo (min)", y="Estacion Origen", hue="Cluster", palette="viridis", s=100)
    plt.title("Agrupamiento de Rutas (K-Means)", fontsize=16)
    plt.xlabel("Tiempo (min)", fontsize=12)
    plt.ylabel("Estacion Origen (Codificada)", fontsize=12)
    plt.legend(title="Cluster", fontsize=10)
    plt.show()


# Main
if __name__ == "__main__":
    # Definir estaciones y conexiones
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

    # Agregar todas las conexiones especificadas
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

    # Generar datos a partir de las conexiones
    df = generar_datos(estaciones_data)
    print("Datos generados:\n", df)

    # Preparar los datos
    df_preparado = preparar_datos(df)
    print("\nDatos preparados para el modelo:\n", df_preparado)

    # Aplicar K-Means
    df_clusters, modelo_kmeans = aplicar_kmeans(df_preparado, n_clusters=3)
    print("\nDatos con clústeres asignados:\n", df_clusters)

    # Visualizar los resultados
    visualizar_agrupamiento(df_clusters)