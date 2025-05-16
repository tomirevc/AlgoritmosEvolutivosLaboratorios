'''
Un estudiante quiere distribuir su tiempo de estudio semanal 
(máx. 20 horas) entre 5 materias diferentes. 
Cada materia aporta un valor estimado de rendimiento académico 
(por puntaje de prácticas) y tiene una carga mínima de horas 
necesarias para rendir bien. 
El objetivo es encontrar 
la mejor combinación de horas por materia que maximice 
el rendimiento total sin pasarse del tiempo disponible.
'''
import random
from deap import base, creator, tools, algorithms
import numpy as np
import pandas as pd

# Crear datos simulados
materias = pd.DataFrame({
    'Materia': ['Mate', 'Fisica', 'Quimica', 'Historia', 'Lengua'],
    'HorasMin': [2, 3, 2, 1, 1],
    'Rendimiento': [8, 7, 6, 5, 4]
})
print("--------------------------------------")
print(materias)
print("--------------------------------------")
print("ESTADISTICAS EVOLUTIVAS")
print("")
MAX_HORAS = 20  # límite semanal de estudio

# Paso 1: Definir la función de evaluación
def evaluar(individuo):
    horas_totales = sum(individuo)
    if horas_totales > MAX_HORAS:
        return 0,  # penalización
    rendimiento_total = sum(h * r for h, r in zip(individuo, materias['Rendimiento']))
    return rendimiento_total,

# Paso 2: Definir el tipo de problema (maximización)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Paso 3: Definir herramientas evolutivas
toolbox = base.Toolbox()
toolbox.register("attr_int", lambda: random.randint(0, 6))  # Cada materia entre 0 y 6h
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=5)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluar)
toolbox.register("mate", tools.cxTwoPoint)  # Cruce
toolbox.register("mutate", tools.mutUniformInt, low=0, up=6, indpb=0.4)
toolbox.register("select", tools.selTournament, tournsize=3)

# Paso 4: Ejecutar el algoritmo genético
def algoritmo_genetico():
    random.seed(42)
    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.6, mutpb=0.3, ngen=40, 
                                stats=stats, halloffame=hof, verbose=True)

    return hof[0], log

# Ejecutar
mejor, log = algoritmo_genetico()

# Mostrar resultados
print("--------------------------------------")
print("Mejor solucion encontrada:")
for i, h in enumerate(mejor):
    print(f"{materias['Materia'][i]}: {h}h")

print("--------------------------------------")
print(f"\nRendimiento total: {sum(h * r for h, r in zip(mejor, materias['Rendimiento']))}")
