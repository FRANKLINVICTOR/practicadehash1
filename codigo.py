import pandas as pd
import time
import matplotlib.pyplot as plt

# --- ESTRUCTURAS DE DATOS MANUALES ---

class HashTableChaining:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def hash_function(self, key):
        # Usamos el hash nativo de Python y lo ajustamos al tamaño de la tabla
        return abs(hash(str(key))) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if len(self.table[index]) > 0:
            self.collisions += 1
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size

class HashTableLinearProbing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    def hash_function(self, key):
        return abs(hash(str(key))) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index] is not None:
            self.collisions += 1
            index = (index + 1) % self.size
            # Evitar bucle infinito si la tabla se llena
        self.table[index] = (key, value)

    def search(self, key):
        index = self.hash_function(key)
        start = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start:
                break
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size

# --- PROCESAMIENTO DE DATOS (2019.csv) ---

# Cargar dataset
try:
    df = pd.read_csv("2019.csv")
    df = df.dropna()
    # Claves: Nombres de países, Valores: Puntuación de felicidad
    keys = df["Country or region"].astype(str).tolist()
    data_records = df.to_dict('records')
    
    table_size = 311  # Número primo para reducir colisiones
    
    # 1. Prueba con Encadenamiento Separado
    hash_chain = HashTableChaining(table_size)
    start_time = time.time()
    for i, key in enumerate(keys):
        hash_chain.insert(key, data_records[i])
    insert_time_chain = time.time() - start_time

    start_time = time.time()
    for key in keys:
        hash_chain.search(key)
    search_time_chain = time.time() - start_time

    # 2. Prueba con Sondeo Lineal
    hash_linear = HashTableLinearProbing(table_size)
    start_time = time.time()
    for i, key in enumerate(keys):
        hash_linear.insert(key, data_records[i])
    insert_time_linear = time.time() - start_time

    start_time = time.time()
    for key in keys:
        hash_linear.search(key)
    search_time_linear = time.time() - start_time

    # 3. Diccionario Nativo de Python
    native_dict = {}
    start_time = time.time()
    for i, key in enumerate(keys):
        native_dict[key] = data_records[i]
    insert_time_dict = time.time() - start_time

    start_time = time.time()
    for key in keys:
        native_dict.get(key)
    search_time_dict = time.time() - start_time

    # --- REPORTE Y GRÁFICOS ---

    results = pd.DataFrame({
        "Metodo": ["Encadenamiento", "Sondeo lineal", "Diccionario Python"],
        "Tiempo insercion": [insert_time_chain, insert_time_linear, insert_time_dict],
        "Tiempo busqueda": [search_time_chain, search_time_linear, search_time_dict],
        "Colisiones": [hash_chain.collisions, hash_linear.collisions, 0],
        "Factor de carga": [hash_chain.load_factor(len(keys)), hash_linear.load_factor(len(keys)), len(keys)/table_size]
    })

    print("\n--- RESULTADOS DE LA PRÁCTICA 3 (Dataset 2019) ---")
    print(results)

    # Gráfico Comparativo
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].bar(results["Metodo"], results["Tiempo insercion"], color='skyblue')
    ax[0].set_title("Tiempo de Inserción (s)")
    ax[0].set_ylabel("Segundos")

    ax[1].bar(results["Metodo"], results["Tiempo busqueda"], color='salmon')
    ax[1].set_title("Tiempo de Búsqueda (s)")
    ax[1].set_ylabel("Segundos")

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("Error: No se encontró el archivo '2019.csv'.")
