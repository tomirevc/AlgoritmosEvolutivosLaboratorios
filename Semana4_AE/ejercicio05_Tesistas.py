# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Horarios de defensas de tesis:
# Se tiene un DataFrame con 15 tesistas y su disponibilidad en 6 franjas horarias (F1 a F6).
# Hay 6 salas disponibles y se deben programar las defensas sin solapamientos, sin exceder 4 horas continuas de uso por sala,
# y minimizando los huecos y conflictos.
# Cada solución se codifica como una asignación (tesista → sala, franja).
# Se parte de una asignación secuencial. El vecindario se genera moviendo un tesista a otra franja y/o sala.
# Se reporta el calendario final y las métricas de huecos.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Asignar cada tesista a una franja y sala válida, minimizando huecos y solapamientos.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random

# Fijar semillas para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer datos desde el archivo Excel, hoja "Tesistas"
df = pd.read_excel("dataset.xlsx", sheet_name="Tesistas")

# Obtener nombres de tesistas y disponibilidad (F1-F6)
tesistas = df["TesistaID"].tolist()
disponibilidad = df.iloc[:, 1:].values  # columnas F1 a F6

num_tesistas = len(tesistas)
num_franjas = 6
num_salas = 6
franjas = ["F1", "F2", "F3", "F4", "F5", "F6"]
salas = list(range(num_salas))

# Mostrar resumen del problema
print("Resumen del problema:")
print(f"- Total de tesistas: {num_tesistas}")
print(f"- Total de franjas horarias: {num_franjas} ({franjas})")
print(f"- Total de salas disponibles: {num_salas}")
print("\nVista previa de disponibilidad (1=disponible, 0=no disponible):")
print(df.head())

# Generar solución inicial: asignar cada tesista a primera franja disponible y a una sala ciclada
def generar_solucion_inicial():
    solucion = []
    for i, dispo in enumerate(disponibilidad):
        for f_index, disponible in enumerate(dispo):
            if disponible == 1:
                sala = i % num_salas  # asignar sala ciclando
                solucion.append((i, sala, f_index))  # (tesista, sala, franja)
                break
    return solucion

# Calcular número de solapamientos (más de 1 tesista en misma sala y franja)
def contar_solapamientos(solucion):
    ocupacion = {}
    for _, sala, franja in solucion:
        clave = (sala, franja)
        ocupacion[clave] = ocupacion.get(clave, 0) + 1
    solapamientos = sum([v - 1 for v in ocupacion.values() if v > 1])
    return solapamientos

# Calcular exceso de uso por sala (más de 4 franjas ocupadas)
def contar_salas_excedidas(solucion):
    uso_salas = {sala: set() for sala in salas}
    for _, sala, franja in solucion:
        uso_salas[sala].add(franja)
    return sum([1 for uso in uso_salas.values() if len(uso) > 4])

# Calcular métricas de calidad de la solución
def evaluar(solucion):
    solapamientos = contar_solapamientos(solucion)
    excedidas = contar_salas_excedidas(solucion)
    penalidad = solapamientos * 100 + excedidas * 50  # ponderar fuerte solapamientos
    return -penalidad  # mayor valor es mejor

# Generar vecinos cambiando aleatoriamente sala o franja de un tesista
def get_neighbors(solucion):
    vecinos = []
    for i in range(len(solucion)):
        original = solucion[i]
        for nueva_sala in salas:
            for nueva_franja in range(num_franjas):
                if disponibilidad[original[0]][nueva_franja] == 1:
                    if (nueva_sala != original[1]) or (nueva_franja != original[2]):
                        nuevo = solucion.copy()
                        nuevo[i] = (original[0], nueva_sala, nueva_franja)
                        vecinos.append(nuevo)
    return vecinos

# Ejecutar hill climbing
solucion_actual = generar_solucion_inicial()
fitness_actual = evaluar(solucion_actual)
historial = [fitness_actual]

for _ in range(1000):
    vecinos = get_neighbors(solucion_actual)
    mejor_vecino = solucion_actual
    mejor_fitness = fitness_actual

    for vecino in vecinos:
        f = evaluar(vecino)
        if f > mejor_fitness:
            mejor_vecino = vecino
            mejor_fitness = f

    if mejor_fitness > fitness_actual:
        solucion_actual = mejor_vecino
        fitness_actual = mejor_fitness
        historial.append(fitness_actual)
    else:
        break  # detener si no mejora

# Mostrar solución final
print("\nHorario final asignado (Tesista, Sala, Franja):")
for t, sala, franja in solucion_actual:
    print(f"- {tesistas[t]} → Sala {sala}, Franja {franjas[franja]}")

# Calcular métricas
solapamientos_final = contar_solapamientos(solucion_actual)
salas_excedidas_final = contar_salas_excedidas(solucion_actual)

print(f"\nMétricas finales:")
print(f"- Solapamientos: {solapamientos_final}")
print(f"- Salas que exceden 4 horas: {salas_excedidas_final}")

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El horario muestra cómo fue asignado cada tesista a una sala y franja horaria según su disponibilidad.
# Las métricas indican si hubo conflictos (solapamientos) o exceso de uso por sala.
# El objetivo era minimizar ambos y lograr un calendario factible y eficiente.
