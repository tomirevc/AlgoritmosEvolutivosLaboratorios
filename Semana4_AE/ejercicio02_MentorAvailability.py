# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Asignación de tutores-pares:
# Tenemos una tabla de disponibilidad de mentores (1 = disponible, 0 = no disponible)
# en 10 bloques horarios. Cada mentor debe ser asignado a 1 bloque de 2 horas (es decir, 1 slot).
# El objetivo es asignar a cada mentor un horario sin que se solapen (choques).
# Usamos hill climbing para minimizar la cantidad de choques (mentores asignados a la misma hora).
# Si se puede, encontrar una solución sin choques.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Asignar a cada mentor un horario en el que está disponible, evitando que dos mentores
# tengan el mismo horario. Buscar una solución sin choques usando hill climbing.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random

# Fijar la semilla para que los resultados sean reproducibles
random.seed(42)
np.random.seed(42)

# Leer la hoja "MentorAvailability" del archivo Excel
df = pd.read_excel("dataset.xlsx", sheet_name="MentorAvailability")

# Extraer solo los slots (slot1 a slot10)
slots = [col for col in df.columns if col.startswith("Slot")]
disponibilidad = df[slots].values  # matriz de 20x10

num_mentores, num_slots = disponibilidad.shape

# ------------------ IMPRIMIR DATOS RELEVANTES ------------------
print(f"Número de mentores: {num_mentores}")
print(f"Número de horarios disponibles (slots): {num_slots}")
mentores_sin_horario = (disponibilidad.sum(axis=1) == 0).sum()
print(f"Mentores sin ninguna disponibilidad: {mentores_sin_horario}")
print(f"Disponibilidades totales en la tabla: {int(disponibilidad.sum())}\n")

# Función de costo: contar cuántos mentores están asignados al mismo horario (choques)
def contar_choques(asignacion):
    conteo = {}
    for i, slot in enumerate(asignacion):
        if slot not in conteo:
            conteo[slot] = 1
        else:
            conteo[slot] += 1
    # Sumar cuántos mentores extras hay por cada horario (eso son los choques)
    choques = sum(v - 1 for v in conteo.values() if v > 1)
    return choques

# Generar una solución inicial aleatoria (respetando disponibilidad)
def generar_solucion():
    asignacion = []
    for i in range(num_mentores):
        disponibles = [j for j in range(num_slots) if disponibilidad[i][j] == 1]
        if disponibles:
            slot = random.choice(disponibles)
        else:
            slot = -1  # si no tiene disponibilidad, marcamos -1
        asignacion.append(slot)
    return asignacion

# Generar vecinos cambiando el horario de un solo mentor
def get_neighbors(solucion_actual):
    vecinos = []
    for i in range(num_mentores):
        disponibles = [j for j in range(num_slots) if disponibilidad[i][j] == 1 and j != solucion_actual[i]]
        for nuevo_slot in disponibles:
            vecino = solucion_actual.copy()
            vecino[i] = nuevo_slot
            vecinos.append(vecino)
    return vecinos

# Crear solución inicial válida
solucion_actual = generar_solucion()
costo_actual = contar_choques(solucion_actual)

# Guardar historial de costos para analizar convergencia
historial = [costo_actual]

# Ejecutar hill climbing por un máximo de 1000 iteraciones
for _ in range(1000):
    vecinos = get_neighbors(solucion_actual)
    mejor_vecino = solucion_actual
    mejor_costo = costo_actual

    # Buscar entre los vecinos el que tenga menos choques
    for vecino in vecinos:
        costo = contar_choques(vecino)
        if costo < mejor_costo:
            mejor_vecino = vecino
            mejor_costo = costo

    # Si hay mejora, actualizar
    if mejor_costo < costo_actual:
        solucion_actual = mejor_vecino
        costo_actual = mejor_costo
        historial.append(costo_actual)
    else:
        break  # si no mejora, detener (óptimo local)

# Crear dataframe con resultado final
resultado = pd.DataFrame({
    "MentorID": df["MentorID"],
    "Horario Asignado": solucion_actual
})

# Mostrar resultado
print("Asignación final de horarios:")
print(resultado)

print(f"\nNúmero total de choques: {costo_actual}")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# Si el número de choques es 0, se logró asignar un horario distinto y disponible a cada mentor.
# Si hay choques > 0, algunos mentores están asignados al mismo horario, lo que genera conflicto.
# Esto puede deberse a limitaciones de disponibilidad.
