# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Ruta de revisión de laboratorios:
# El docente debe visitar 10 laboratorios caminando, y se quiere minimizar
# la distancia total recorrida. La información se encuentra en una matriz simétrica
# de distancias entre laboratorios (10 x 10). Usar hill climbing para encontrar
# el mejor orden posible de visita. La vecindad se genera intercambiando dos laboratorios.
# Se realizan 1000 iteraciones como máximo.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Buscar el orden óptimo para visitar los 10 laboratorios,
# de forma que se camine la menor distancia posible.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random

# Fijar semilla para asegurar reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer la matriz de distancias desde la hoja 'LabDistances'
df = pd.read_excel("dataset.xlsx", sheet_name="LabDistances", index_col=0)
matriz_distancias = df.values  # Convertir a matriz de numpy

num_labs = len(matriz_distancias)

# ------------------ IMPRIMIR DATOS RELEVANTES ------------------
print(f"Número de laboratorios: {num_labs}")
print("Laboratorios:")
print(" - " + "\n - ".join(df.columns))
distancias_no_cero = np.count_nonzero(matriz_distancias)
print(f"Número de valores distintos de cero en la matriz: {distancias_no_cero}")
print(f"Distancia promedio entre laboratorios: {matriz_distancias.mean():.2f} metros\n")

# Calcular la distancia total de una ruta (suma de distancias entre nodos consecutivos + retorno)
def calcular_distancia(ruta):
    distancia = 0
    for i in range(num_labs - 1):
        distancia += matriz_distancias[ruta[i]][ruta[i + 1]]
    # Agregar distancia de regreso al primer laboratorio (cierre del ciclo)
    distancia += matriz_distancias[ruta[-1]][ruta[0]]
    return distancia

# Generar vecinos intercambiando dos laboratorios en la ruta
def get_neighbors(ruta_actual):
    vecinos = []
    for i in range(num_labs):
        for j in range(i + 1, num_labs):
            vecino = ruta_actual.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

# Generar una ruta inicial aleatoria (permutación)
ruta_actual = list(range(num_labs))
random.shuffle(ruta_actual)
distancia_actual = calcular_distancia(ruta_actual)

# Guardar historial para observar convergencia
historial = [distancia_actual]

# Ejecutar hill climbing por 1000 iteraciones
for _ in range(1000):
    vecinos = get_neighbors(ruta_actual)
    mejor_vecino = ruta_actual
    mejor_distancia = distancia_actual

    # Buscar al vecino con la menor distancia
    for vecino in vecinos:
        d = calcular_distancia(vecino)
        if d < mejor_distancia:
            mejor_vecino = vecino
            mejor_distancia = d

    # Si hubo mejora, actualizar ruta
    if mejor_distancia < distancia_actual:
        ruta_actual = mejor_vecino
        distancia_actual = mejor_distancia
        historial.append(distancia_actual)
    else:
        break  # detener si no mejora (óptimo local)

# Traducir los índices a nombres de laboratorios
nombres_labs = df.columns.tolist()
ruta_final = [nombres_labs[i] for i in ruta_actual]

# Mostrar resultados
print("Orden óptimo de visita:")
print(" → ".join(ruta_final))
print(f"\nDistancia total recorrida: {distancia_actual} metros")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El orden óptimo de visita muestra por qué laboratorio empezar y en qué orden
# continuar para recorrer todos con la menor distancia total posible.
# Esto ayuda al docente a planificar una ruta más eficiente para revisar laboratorios.
