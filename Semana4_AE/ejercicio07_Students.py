# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Balanceo de equipos de proyecto:
# Hay 20 estudiantes, y se deben formar 5 equipos de 4 personas.
# Cada estudiante tiene un GPA (numérico) y una habilidad (Skill, como categoría).
# La función de aptitud busca minimizar la suma de varianzas de GPA entre equipos
# y penaliza si las habilidades están desbalanceadas entre los equipos.
# Se representa la solución como una lista de listas con los índices de estudiantes por equipo.
# El vecindario se define intercambiando dos estudiantes entre equipos diferentes.
# Se busca una configuración equilibrada de equipos.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Formar 5 equipos de 4 estudiantes equilibrando el GPA y la distribución de habilidades.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random
from collections import Counter

# Fijar semilla para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer datos desde el archivo
df = pd.read_excel("dataset.xlsx", sheet_name="Students")

# Obtener columnas necesarias
gpas = df["GPA"].values
skills = df["Skill"].values
n_estudiantes = len(df)

# Mostrar resumen del problema
print("Resumen del problema:")
print(f"- Total de estudiantes: {n_estudiantes}")
print(f"- Equipos requeridos: 5 equipos de 4 estudiantes")
print("\nVista previa de los datos:")
print(df.head())

# Verificar que hay 20 alumnos y 5 equipos de 4
assert n_estudiantes == 20, "Debe haber exactamente 20 estudiantes"

# Generar solución inicial aleatoria
indices = list(range(n_estudiantes))
random.shuffle(indices)
equipos = [indices[i::5] for i in range(5)]  # 5 equipos

# Calcular varianza de GPAs por equipo
def varianza_gpa(equipos):
    return sum(np.var([gpas[i] for i in equipo]) for equipo in equipos)

# Penalización por desequilibrio de habilidades
def penalizar_skills(equipos):
    total_penalidad = 0
    for equipo in equipos:
        habilidades = [skills[i] for i in equipo]
        conteo = Counter(habilidades)
        max_cantidad = max(conteo.values())
        min_cantidad = min(conteo.values())
        total_penalidad += (max_cantidad - min_cantidad)  # penalizar si hay desbalance
    return total_penalidad

# Función de aptitud
def fitness(equipos):
    return - (varianza_gpa(equipos) + penalizar_skills(equipos))  # negativo porque queremos minimizar

# Generar vecinos intercambiando 2 estudiantes de diferentes equipos
def get_neighbors(equipos):
    vecinos = []
    for i in range(len(equipos)):
        for j in range(i+1, len(equipos)):
            for a in range(len(equipos[i])):
                for b in range(len(equipos[j])):
                    nuevo = [equipo.copy() for equipo in equipos]
                    nuevo[i][a], nuevo[j][b] = nuevo[j][b], nuevo[i][a]
                    vecinos.append(nuevo)
    return vecinos

# Ejecutar hill climbing
fitness_actual = fitness(equipos)
mejor_solucion = equipos
historial = [fitness_actual]

for _ in range(1000):
    vecinos = get_neighbors(mejor_solucion)
    mejor_vecino = mejor_solucion
    mejor_fitness = fitness_actual

    for vecino in vecinos:
        f = fitness(vecino)
        if f > mejor_fitness:
            mejor_vecino = vecino
            mejor_fitness = f

    if mejor_fitness > fitness_actual:
        mejor_solucion = mejor_vecino
        fitness_actual = mejor_fitness
        historial.append(fitness_actual)
    else:
        break

# Mostrar equipos finales
print("\nComposición final de los equipos:")
for idx, equipo in enumerate(mejor_solucion):
    print(f"\nEquipo {idx+1}:")
    subdf = df.iloc[equipo][["StudentID", "GPA", "Skill"]]
    print(subdf.to_string(index=False))

# Calcular métricas
var_gpa_total = varianza_gpa(mejor_solucion)
penalizacion_skills = penalizar_skills(mejor_solucion)

print(f"\nMétrica final:")
print(f"- Suma de varianzas de GPA entre equipos: {var_gpa_total:.4f}")
print(f"- Penalización por desbalance de habilidades: {penalizacion_skills}")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# Se han formado 5 equipos con 4 estudiantes cada uno.
# El algoritmo intentó minimizar la diferencia de GPA dentro de cada equipo (equilibrio académico)
# y evitar que las habilidades se concentren en algunos equipos (equilibrio de capacidades).
# Las métricas finales muestran qué tan bien se logró ese equilibrio.
