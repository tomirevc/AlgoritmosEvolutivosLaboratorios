# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Optimización de presupuesto de proyectos:
# Se tiene una tabla con 8 proyectos estudiantiles, cada uno con un costo (S/) y un beneficio estimado.
# El presupuesto total disponible es S/ 10,000.
# El objetivo es seleccionar un subconjunto de proyectos que maximice el beneficio sin exceder el presupuesto.
# Representamos soluciones como bitstrings de 8 bits (1 = seleccionado, 0 = no seleccionado).
# Si una solución excede el presupuesto, su valor de aptitud es -infinito.
# Vecindario: cambiar (voltear) un solo bit. Usamos hill climbing.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Seleccionar proyectos sin pasarse del presupuesto, buscando la mayor ganancia posible.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random

# Fijar semilla para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer datos desde la hoja "Projects"
df = pd.read_excel("dataset.xlsx", sheet_name="Projects")

# Extraer listas de costos y beneficios
costos = df["Cost_Soles"].values
beneficios = df["Benefit_Soles"].values

presupuesto = 10000
n = len(costos)  # número de proyectos

# Imprimir datos relevantes antes de resolver
print("Resumen del problema:")
print(f"- Número de proyectos: {n}")
print(f"- Presupuesto máximo: S/ {presupuesto}")
print("\nVista previa de los proyectos:")
print(df[["ProjectID", "Cost_Soles", "Benefit_Soles"]])

# Calcular la aptitud de una solución (beneficio total si cumple el presupuesto)
def fitness(solucion):
    costo_total = np.sum(np.array(solucion) * costos)
    beneficio_total = np.sum(np.array(solucion) * beneficios)
    if costo_total > presupuesto:
        return -float('inf')  # penalizar si se excede
    return beneficio_total

# Generar vecinos volteando un bit
def get_neighbors(solucion):
    vecinos = []
    for i in range(n):
        vecino = solucion.copy()
        vecino[i] = 1 - vecino[i]  # cambiar de 0 a 1 o de 1 a 0
        vecinos.append(vecino)
    return vecinos

# Generar solución inicial aleatoria (bitstring de 0s y 1s)
solucion_actual = [random.randint(0, 1) for _ in range(n)]
fitness_actual = fitness(solucion_actual)

# Guardar historial de fitness para observar convergencia
historial = [fitness_actual]

# Ejecutar hill climbing por 1000 iteraciones
for _ in range(1000):
    vecinos = get_neighbors(solucion_actual)
    mejor_vecino = solucion_actual
    mejor_fitness = fitness_actual

    # Buscar el mejor vecino que no exceda presupuesto
    for vecino in vecinos:
        f = fitness(vecino)
        if f > mejor_fitness:
            mejor_vecino = vecino
            mejor_fitness = f

    # Si se mejora, actualizar
    if mejor_fitness > fitness_actual:
        solucion_actual = mejor_vecino
        fitness_actual = mejor_fitness
        historial.append(fitness_actual)
    else:
        break  # detener si no hay mejora

# Obtener proyectos seleccionados
proyectos_seleccionados = df[ [bool(b) for b in solucion_actual] ]

# Mostrar resultados
print("\nProyectos seleccionados:")
print(proyectos_seleccionados[["ProjectID", "Cost_Soles", "Benefit_Soles"]])

print(f"\nBeneficio total: S/ {fitness_actual:.2f}")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# La lista de proyectos seleccionados representa la mejor combinación encontrada
# dentro del presupuesto de S/ 10,000. El beneficio total indica la ganancia obtenida
# con esta selección. Si quedan proyectos fuera, es porque agregarlos superaría el presupuesto.
