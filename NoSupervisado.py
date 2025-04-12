from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Generar datos simulados (puedes usar el dataset generado previamente)
def generar_datos():
    data = {
        "Estacion Origen": ["Tatooine", "Alderaan", "Yavin IV", "Hoth", "Dagobah", "Bespin", "Endor", "Naboo", "Coruscant", "Kamino"],
        "Estacion Destino": ["Alderaan", "Yavin IV", "Hoth", "Dagobah", "Bespin", "Endor", "Naboo", "Coruscant", "Kamino", "Mandalore"],
        "Linea": ["Ruta 1", "Ruta 2", "Ruta 3", "Ruta 4", "Ruta 5", "Ruta 6", "Ruta 7", "Ruta 8", "Ruta 9", "Ruta 10"],
        "Tiempo (min)": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    }

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
    # Generar datos simulados
    df = generar_datos()
    print("Datos generados:\n", df)

    # Preparar los datos
    df_preparado = preparar_datos(df)
    print("\nDatos preparados para el modelo:\n", df_preparado)

    # Aplicar K-Means
    df_clusters, modelo_kmeans = aplicar_kmeans(df_preparado, n_clusters=3)
    print("\nDatos con clústeres asignados:\n", df_clusters)

    # Visualizar los resultados
    visualizar_agrupamiento(df_clusters)