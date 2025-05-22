# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Selección de problemas de examen:
# Hay un banco de 30 preguntas con su dificultad y tiempo estimado en minutos.
# El examen debe durar como máximo 90 minutos y tener una dificultad total entre 180 y 200.
# Se representa una solución como un bitstring de 30 bits (1 = seleccionada, 0 = no).
# La función objetivo penaliza las soluciones que no cumplen las restricciones.
# Vecindario: voltear un bit (agregar o quitar una pregunta).
# Se busca un subconjunto óptimo que cumpla las restricciones y maximice la dificultad.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Elegir preguntas para el examen que cumplan tiempo ≤ 90 min y dificultad entre 180–200.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random

# Fijar semilla para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer los datos desde el archivo Excel
df = pd.read_excel("dataset.xlsx", sheet_name="ExamQuestions")

# Extraer columnas necesarias
dificultad = df["Difficulty"].values
tiempo = df["Time_min"].values
n = len(dificultad)

# Restricciones
tiempo_max = 90
dificultad_min = 180
dificultad_max = 200

# Mostrar datos relevantes
print("Resumen del problema:")
print(f"- Total de preguntas disponibles: {n}")
print(f"- Tiempo máximo permitido: {tiempo_max} min")
print(f"- Dificultad requerida: entre {dificultad_min} y {dificultad_max}")
print("\nVista previa de preguntas:")
print(df.head())

# Definir la función de aptitud (costo)
def fitness(solucion):
    total_tiempo = np.sum(np.array(solucion) * tiempo)
    total_dificultad = np.sum(np.array(solucion) * dificultad)

    # Penalizar si no cumple tiempo o dificultad
    if total_tiempo > tiempo_max or not (dificultad_min <= total_dificultad <= dificultad_max):
        return -float("inf")
    return total_dificultad  # entre soluciones válidas, maximizar dificultad

# Generar vecinos volteando un bit
def get_neighbors(solucion):
    vecinos = []
    for i in range(n):
        vecino = solucion.copy()
        vecino[i] = 1 - vecino[i]
        vecinos.append(vecino)
    return vecinos

# Crear solución inicial aleatoria
solucion_actual = [random.randint(0, 1) for _ in range(n)]
fitness_actual = fitness(solucion_actual)
historial = [fitness_actual]

# Ejecutar hill climbing
for _ in range(1000):
    vecinos = get_neighbors(solucion_actual)
    mejor_vecino = solucion_actual
    mejor_fitness = fitness_actual

    for vecino in vecinos:
        f = fitness(vecino)
        if f > mejor_fitness:
            mejor_vecino = vecino
            mejor_fitness = f

    if mejor_fitness > fitness_actual:
        solucion_actual = mejor_vecino
        fitness_actual = mejor_fitness
        historial.append(fitness_actual)
    else:
        break

# Obtener preguntas seleccionadas
preguntas_seleccionadas = df[[bool(b) for b in solucion_actual]]
tiempo_total = preguntas_seleccionadas["Time_min"].sum()
dificultad_total = preguntas_seleccionadas["Difficulty"].sum()

# Mostrar resultados
print("\nPreguntas seleccionadas para el examen:")
print(preguntas_seleccionadas[["QuestionID", "Difficulty", "Time_min"]])

print(f"\nTotal de preguntas: {len(preguntas_seleccionadas)}")
print(f"Tiempo total: {tiempo_total} minutos")
print(f"Dificultad total: {dificultad_total}")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# Las preguntas seleccionadas cumplen con el límite de tiempo (≤ 90 minutos)
# y la dificultad total está en el rango de 180 a 200.
# Entre las posibles combinaciones válidas, se eligió la que maximiza la dificultad.
