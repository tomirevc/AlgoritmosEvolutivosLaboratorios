# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Curva de notas de Parciales:
# Dado un Excel con calificaciones de 120 alumnos, usar hill climbing para encontrar
# un offset entre –5 y +5 puntos que aumente el % de aprobados (nota final ≥ 11),
# sin que el promedio de la clase pase de 14. Se usan pasos de 0.5 y se penaliza
# si el promedio final excede 14.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Buscar cuántos puntos se pueden sumar a las notas para que más alumnos aprueben,
# sin que el promedio de la clase suba de 14, usando el algoritmo hill climbing.

# ------------------ CÓDIGO ------------------

# Dependencia para leer el dataset: openpyxl (Se usa en todos los ejercicios)

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Fijar la semilla para asegurar resultados reproducibles
random.seed(42)
np.random.seed(42)

# Leer los datos desde el archivo Excel (hoja 'Grades')
df = pd.read_excel("dataset.xlsx", sheet_name="Grades")

# Calcular la nota final como el promedio de los tres parciales
df["Final"] = df[["Parcial1", "Parcial2", "Parcial3"]].mean(axis=1)

# ------------------ IMPRIMIR DATOS RELEVANTES ------------------
print("Total de estudiantes:", len(df))
print(f"Promedio original de notas: {df['Final'].mean():.2f}")
print(f"Porcentaje de aprobados antes del ajuste: {(df['Final'] >= 11).mean() * 100:.2f}%\n")

# Definir la función de aptitud (fitness): porcentaje de aprobados con penalización si el promedio > 14
def fitness(offset):
    # Sumar el offset a las notas y limitar entre 0 y 20
    ajustadas = np.clip(df["Final"] + offset, 0, 20)
    promedio = ajustadas.mean()

    # Penalizar si el promedio supera 14
    if promedio > 14:
        return 0
    # Calcular porcentaje de aprobados (notas ≥ 11)
    aprobados = (ajustadas >= 11).sum()
    return aprobados / len(ajustadas)

# Definir vecinos: offsets posibles a ±0.5 del actual, sin salirse del rango [-5, 5]
def get_neighbors(actual):
    paso = 0.5
    vecinos = []
    if actual - paso >= -5:
        vecinos.append(round(actual - paso, 1))
    if actual + paso <= 5:
        vecinos.append(round(actual + paso, 1))
    return vecinos

# Elegir un offset inicial aleatorio dentro del rango permitido
offset_actual = round(random.uniform(-5, 5), 1)
mejor_fitness = fitness(offset_actual)

# Guardar el historial para graficar la convergencia
historial = [(offset_actual, mejor_fitness)]

# Ejecutar el algoritmo hill climbing por un máximo de 100 iteraciones
for _ in range(100):
    vecinos = get_neighbors(offset_actual)
    nuevo_offset = offset_actual
    nuevo_fitness = mejor_fitness

    # Evaluar cada vecino y quedarse con el que tenga mejor fitness
    for v in vecinos:
        f = fitness(v)
        if f > nuevo_fitness:
            nuevo_offset = v
            nuevo_fitness = f
    
    # Si hay mejora, actualizar la solución actual
    if nuevo_fitness > mejor_fitness:
        offset_actual = nuevo_offset
        mejor_fitness = nuevo_fitness
        historial.append((offset_actual, mejor_fitness))
    else:
        # Si no mejora, detener (óptimo local)
        break

# Aplicar el mejor offset a las notas y limitar entre 0 y 20
df["Final Ajustado"] = np.clip(df["Final"] + offset_actual, 0, 20)

# Imprimir los resultados finales
print(f"Offset óptimo encontrado: {offset_actual}")
print(f"Porcentaje de aprobados: {mejor_fitness * 100:.2f}%")
print(f"Promedio final ajustado: {df['Final Ajustado'].mean():.2f}")

# Mostrar resumen estadístico de las notas ajustadas
print("\nResumen de notas ajustadas:")
print(df["Final Ajustado"].describe())

# Graficar cómo fue mejorando el porcentaje de aprobados con cada offset
offsets, scores = zip(*historial)
plt.plot(offsets, scores, marker='o')
plt.title("Convergencia del Hill Climbing")
plt.xlabel("Offset aplicado")
plt.ylabel("Porcentaje de aprobados")
plt.grid(True)
plt.show()

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El valor de offset óptimo muestra cuántos puntos se pueden sumar sin que el promedio pase de 14.
# El porcentaje de aprobados indica cuántos estudiantes superan la nota mínima (11) con ese ajuste.
# Esto sirve para justificar un posible "curvado" de notas que mejore el rendimiento sin inflar el promedio.
